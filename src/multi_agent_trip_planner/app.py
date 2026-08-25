from multi_agent_trip_planner.graph.travel_graph import travel_graph


def main():

    config = {
        "configurable": {
            "thread_id": "sindhu"
        }
    }

    while True:

        question = input("Question: ")

        if question.lower() == "exit":
            break

        result = {}

        for event in travel_graph.stream(
            {
                "user_query": question,
                "messages": []
            },
            config=config
        ):
            print(event)

            if isinstance(event, dict):
                for value in event.values():
                    if isinstance(value, dict):
                        result.update(value)

        if result.get("allowed") is False:
            print("\n==== GUARDRAIL BLOCKED ====")
            print(result.get("guardrail_reason"))
            continue

        print("\n==== SELECTED AGENTS ====")
        print(result.get("selected_agents"))

        if result.get("flight_results"):
            print("\n==== FLIGHTS ====")
            print(result["flight_results"])

        if result.get("hotel_results"):
            print("\n==== HOTEL ====")
            print(result["hotel_results"])

        if result.get("weather_results"):
            print("\n==== WEATHER ====")
            print(result["weather_results"])

        if result.get("budget_results"):
            print("\n==== BUDGET ====")
            print(result["budget_results"])

        if result.get("itinerary"):
            print("\n==== ITINERARY ====")
            print(result["itinerary"])

        state = travel_graph.get_state(config)

        print("\n==== STORED TRIP DETAILS ====")
        print(
            state.values.get(
                "trip_details",
                {}
            )
        )


if __name__ == "__main__":
    main()