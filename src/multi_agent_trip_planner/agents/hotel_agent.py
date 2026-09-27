from langchain_core.messages import AIMessage

from multi_agent_trip_planner.tools.hotel_tool import (
    search_hotels
)


async def hotel_agent(state: dict) -> dict:
    """Search hotels using validated trip details."""

    print("\n>>> HOTEL AGENT")

    trip_details = state.get(
        "trip_details",
        {}
    )

    destination = trip_details.get(
        "destination",
        ""
    )

    adults = trip_details.get(
        "adults",
        1
    )

    print(
        f"Searching hotels in {destination}"
    )

    hotel_results = await search_hotels(
        city=destination,
        guests=adults
    )

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(
                content="Hotel search completed."
            )
        ]
    }