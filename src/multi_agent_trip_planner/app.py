import uuid
import asyncio
import traceback
import selectors

from langgraph.types import Command

from multi_agent_trip_planner.graph.travel_graph import build_graph
from multi_agent_trip_planner.memory.checkpoint import (
    create_postgres_checkpointer
)


async def run_graph(graph, graph_input, config):
    """
    Run the graph and handle HITL interruptions.
    """

    result = await graph.ainvoke(
        graph_input,
        config=config
    )

    while "__interrupt__" in result:

        interrupt_data = result[
            "__interrupt__"
        ][0].value

        question = interrupt_data.get(
            "question",
            "Please provide the missing information."
        )

        print(f"\nAssistant: {question}")

        user_answer = input("You: ").strip()

        result = await graph.ainvoke(
            Command(resume=user_answer),
            config=config
        )

    return result


async def main():

    connection, checkpointer = (
        await create_postgres_checkpointer()
    )

    try:
        graph = build_graph(checkpointer)

        # One thread for the complete CLI conversation.
        thread_id = str(uuid.uuid4())

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        print("\nMulti-Agent Trip Planner")
        print("Type 'exit' to stop.\n")

        while True:

            user_query = input("You: ").strip()

            if user_query.lower() in {
                "exit",
                "quit"
            }:
                print("Goodbye.")
                break

            if not user_query:
                continue

            graph_input = {
                "user_query": user_query
            }

            try:
                result = await run_graph(
                    graph,
                    graph_input,
                    config
                )

                final_response = result.get(
                    "final_response",
                    ""
                )

                if final_response:
                    print(
                        f"\nAssistant:\n"
                        f"{final_response}\n"
                    )

                else:
                    print(
                        "\nAssistant: "
                        "I couldn't generate a response.\n"
                    )

            except Exception as e:

                print("\n========== ERROR ==========")
                print(
                    "ERROR TYPE:",
                    type(e).__name__
                )
                print("ERROR:", repr(e))

                print("\nFULL TRACEBACK:")
                traceback.print_exc()

                print("===========================\n")

    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(
        main(),
        loop_factory=lambda: asyncio.SelectorEventLoop(
            selectors.SelectSelector()
        )
    )