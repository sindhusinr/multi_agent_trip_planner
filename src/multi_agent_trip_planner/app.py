import os
import uuid
import asyncio
import traceback
import selectors
from dotenv import load_dotenv
from psycopg import AsyncConnection
from psycopg.rows import dict_row

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.types import Command

from multi_agent_trip_planner.graph.travel_graph import build_graph


load_dotenv()


async def run_graph(graph, graph_input, config):
    """
    Run the graph asynchronously and handle HITL interruptions.
    """

    result = await graph.ainvoke(
        graph_input,
        config=config
    )

    # Resume the same graph after HITL input.
    while "__interrupt__" in result:

        interrupt_data = result["__interrupt__"][0].value

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

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is not configured in the .env file."
        )

    # Async PostgreSQL connection for async LangGraph execution.
    async with await AsyncConnection.connect(
        database_url,
        autocommit=True,
        row_factory=dict_row
    ) as connection:

        checkpointer = AsyncPostgresSaver(connection)

        # Create checkpoint tables if required.
        await checkpointer.setup()

        graph = build_graph(checkpointer)

        # Same thread is used for the complete CLI conversation.
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
                        f"\nAssistant:\n{final_response}\n"
                    )

                else:
                    print(
                        "\nAssistant: "
                        "I couldn't generate a response.\n"
                    )

            except Exception as e:

                print("\n========== ERROR ==========")
                print("ERROR TYPE:", type(e).__name__)
                print("ERROR:", repr(e))

                print("\nFULL TRACEBACK:")
                traceback.print_exc()

                print("===========================\n")


if __name__ == "__main__":
    asyncio.run(
        main(),
        loop_factory=lambda: asyncio.SelectorEventLoop(
            selectors.SelectSelector()
        )
    )