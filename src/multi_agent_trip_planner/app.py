import os
import uuid

from dotenv import load_dotenv
from psycopg import Connection
from psycopg.rows import dict_row

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import Command

from multi_agent_trip_planner.graph.travel_graph import build_graph


load_dotenv()


def run_graph(graph, graph_input, config):
    """
    Run the graph and handle HITL interruptions.
    """

    result = graph.invoke(
        graph_input,
        config=config
    )

    # Continue until all HITL interruptions are resolved.
    while "__interrupt__" in result:

        interrupts = result["__interrupt__"]

        interrupt_data = interrupts[0].value

        question = interrupt_data.get(
            "question",
            "Please provide the missing information."
        )

        print(f"\nAssistant: {question}")

        user_answer = input("You: ").strip()

        # Resume the same interrupted graph execution.
        result = graph.invoke(
            Command(resume=user_answer),
            config=config
        )

    return result


def main():

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is not configured in the .env file."
        )

    # One PostgreSQL connection is used by the LangGraph checkpointer.
    with Connection.connect(
        database_url,
        autocommit=True,
        row_factory=dict_row
    ) as connection:

        checkpointer = PostgresSaver(connection)

        # Run once when initializing the checkpoint tables.
        checkpointer.setup()

        graph = build_graph(checkpointer)

        # One thread represents one continuous conversation.
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
                result = run_graph(
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
                print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()