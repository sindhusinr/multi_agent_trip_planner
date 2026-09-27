from langchain_core.messages import AIMessage

from multi_agent_trip_planner.tools.flight_tool import (
    search_flights
)


async def flight_agent(state: dict) -> dict:
    """
    Search live flight offers using validated trip details.
    """

    print("\n>>> FLIGHT AGENT")

    trip_details = state.get(
        "trip_details",
        {}
    )

    origin = trip_details.get(
        "origin",
        ""
    )

    destination = trip_details.get(
        "destination",
        ""
    )

    departure_date = trip_details.get(
        "departure_date",
        ""
    )

    return_date = trip_details.get(
        "return_date",
        ""
    )

    adults = trip_details.get(
        "adults",
        1
    )

    cabin_class = trip_details.get(
        "cabin_class",
        "economy"
    )

    print(
        f"Searching flights: "
        f"{origin} -> {destination} "
        f"on {departure_date}"
    )

    flight_results = await search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        adults=adults,
        cabin_class=cabin_class,
        return_date=return_date
    )

    return {
        "flight_results": flight_results,
        "messages": [
            AIMessage(
                content="Flight search completed."
            )
        ]
    }