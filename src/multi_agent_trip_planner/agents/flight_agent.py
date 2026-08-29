from langchain_core.messages import AIMessage

from multi_agent_trip_planner.tools.flight_tool import (
    search_flights
)
from multi_agent_trip_planner.tools.airport_tool import (
    get_iata
)


def flight_agent(state: dict) -> dict:

    print(">>> FLIGHT AGENT")

    trip_details = state.get(
        "trip_details",
        {}
    )

    # Departure location
    origin = trip_details.get(
        "origin",
        ""
    )

    # Prefer primary_city for flight searches
    destination = (
        trip_details.get(
            "primary_city",
            ""
        )
        or trip_details.get(
            "destination",
            ""
        )
    )

    # Origin is required
    if not origin:
        return {
            "flight_results": (
                "Please provide your departure city."
            ),
            "messages": [
                AIMessage(
                    content="Origin city missing."
                )
            ]
        }

    # Destination is required
    if not destination:
        return {
            "flight_results": (
                "Please provide your destination."
            ),
            "messages": [
                AIMessage(
                    content="Destination missing."
                )
            ]
        }

    origin_iata = get_iata(origin)
    destination_iata = get_iata(destination)

    # Validate origin airport
    if not origin_iata:
        return {
            "flight_results": (
                f"Unable to find airport code "
                f"for '{origin}'."
            ),
            "messages": [
                AIMessage(
                    content="Origin airport not found."
                )
            ]
        }

    # Validate destination airport
    if not destination_iata:
        return {
            "flight_results": (
                f"Unable to find airport code "
                f"for '{destination}'."
            ),
            "messages": [
                AIMessage(
                    content="Destination airport not found."
                )
            ]
        }

    print(
        f"\nSearching flights: "
        f"{origin_iata} -> {destination_iata}"
    )

    flight_results = search_flights(
        origin_iata,
        destination_iata
    )

    return {
        "flight_results": flight_results,
        "messages": [
            AIMessage(
                content=(
                    "Flight recommendations generated."
                )
            )
        ]
    }