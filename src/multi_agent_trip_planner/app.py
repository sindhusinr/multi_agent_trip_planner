import uuid

from multi_agent_trip_planner.graph.travel_graph import (
    travel_graph
)


def main():
    # New thread per app run.
    # Context is preserved during the session,
    # but not across application restarts.
    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    print(
        f"\nSession ID: "
        f"{config['configurable']['thread_id']}"
    )

    while True:

        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        result = {}

        # Stream graph execution events
        for event in travel_graph.stream(
            {
                "user_query": question,
                "messages": []
            },
            config=config
        ):

            print(event)

            # Merge node outputs into a
            # single response dictionary
            if isinstance(event, dict):

                for value in event.values():

                    if isinstance(value, dict):
                        result.update(value)

        # Stop processing if blocked
        if result.get("allowed") is False:

            print(
                "\n==== GUARDRAIL BLOCKED ===="
            )

            print(
                result.get(
                    "guardrail_reason",
                    ""
                )
            )

            continue

        print(
            "\n==== SELECTED AGENTS ===="
        )

        print(
            result.get(
                "selected_agents",
                []
            )
        )

        if result.get("flight_results"):

            print(
                "\n==== FLIGHTS ===="
            )

            print(
                result["flight_results"]
            )

        if result.get("hotel_results"):

            print(
                "\n==== HOTEL ===="
            )

            print(
                result["hotel_results"]
            )

        if result.get("weather_results"):

            print(
                "\n==== WEATHER ===="
            )

            print(
                result["weather_results"]
            )

        if result.get("budget_results"):

            print(
                "\n==== BUDGET ===="
            )

            print(
                result["budget_results"]
            )

        if result.get("itinerary"):

            print(
                "\n==== ITINERARY ===="
            )

            print(
                result["itinerary"]
            )

        # Display current trip memory
        state = travel_graph.get_state(
            config
        )

        print(
            "\n==== STORED TRIP DETAILS ===="
        )

        print(
            state.values.get(
                "trip_details",
                {}
            )
        )


if __name__ == "__main__":
    main()