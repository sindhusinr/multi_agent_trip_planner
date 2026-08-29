import asyncio

from langchain_core.messages import AIMessage

from multi_agent_trip_planner.tools.tavily_tool import (
    tavily_search
)


def hotel_agent(state: dict) -> dict:

    destination = (
        state["trip_details"]
        .get("destination", "")
    )

    # Build the search query
    query = (
        f"Best hotels in {destination}"
    )

    # Fetch hotel recommendations from Tavily MCP
    hotels = asyncio.run(
        tavily_search(query)
    )

    return {
        "hotel_results": hotels,
        "messages": [
            AIMessage(
                content=(
                    "Hotel information generated."
                )
            )
        ]
    }