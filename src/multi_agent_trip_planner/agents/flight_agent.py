from langchain_core.messages import AIMessage

from multi_agent_trip_planner.tools.flight_tool import search_flights
from multi_agent_trip_planner.tools.airport_tool import get_iata


def flight_agent(state: dict) -> dict:
    print(">>> FLIGHT AGENT")

    trip_details = state.get("trip_details", {})

    origin = trip_details.get("origin", "")
    destination = (
    trip_details.get("primary_city")
    or trip_details.get("destination")
)

    origin_iata = get_iata(origin)
    destination_iata = get_iata(destination)

    flight_results = search_flights(
        origin_iata,
        destination_iata
    )

    return {
        "flight_results": flight_results,
        "messages": [
            AIMessage(
                content="Flight recommendations generated."
            )
        ]
    }