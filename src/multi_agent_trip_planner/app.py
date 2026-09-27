import uuid
from multi_agent_trip_planner.graph.travel_graph import travel_graph

def main():
    # One thread_id represents one conversation and preserves state across turns.
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    print(f"\nSession ID: {config['configurable']['thread_id']}")

    while True:
        question = input("\nQuestion: ")
        if question.lower() == "exit":
            break

        result = {}

        # Streams each LangGraph node output so routing/execution can be debugged.
        for event in travel_graph.stream(
            {"user_query": question, "messages": []},
            config=config
        ):
            print("\nEVENT:", event)

            # Combines individual node outputs for easier terminal inspection.
            if isinstance(event, dict):
                for value in event.values():
                    if isinstance(value, dict):
                        result.update(value)

        # Guardrail-blocked requests do not continue to travel agents.
        if result.get("allowed") is False:
            print("\n==== GUARDRAIL BLOCKED ====")
            print(result.get("guardrail_reason", ""))
            continue

        print("\n==== SELECTED AGENTS ====")
        print(result.get("selected_agents", []))

        # Raw specialist outputs are kept for backend debugging.
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

        # This is the only response that will eventually be shown to the end user.
        if result.get("final_response"):
            print("\n==== FINAL RESPONSE ====")
            print(result["final_response"])

        # Reads the persisted thread state from PostgreSQL checkpointing.
        state = travel_graph.get_state(config)
        print("\n==== STORED TRIP DETAILS ====")
        print(state.values.get("trip_details", {}))

if __name__ == "__main__":
    main()