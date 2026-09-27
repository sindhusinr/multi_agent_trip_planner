import json

from multi_agent_trip_planner.mcp.mcp_client import (
    get_mcp_tools
)


def normalize_hotel(hotel: dict) -> dict:
    """Convert VistaLink hotel into our internal format."""

    price = hotel.get("price") or {}

    return {
        "hotel_id": hotel.get("hotel_id", ""),
        "name": hotel.get("name", ""),
        "city": hotel.get("city", ""),
        "country": hotel.get("country", ""),
        "address": hotel.get("address", ""),

        "star_rating": hotel.get("star_rating"),
        "review_score": hotel.get("review_score"),

        "price_min": price.get("min"),
        "price_max": price.get("max"),
        "currency": price.get("currency", ""),

        "amenities": hotel.get("amenities", []),
        "website_url": hotel.get("website_url"),

        "description": hotel.get("description", ""),
        "review_highlight": hotel.get(
            "review_highlight"
        )
    }


async def search_hotels(
    city: str,
    guests: int = 1,
    check_in: str = "",
    check_out: str = ""
) -> dict:
    """Search VistaLink MCP for hotels."""

    try:
        tools = await get_mcp_tools("vistalink")

        hotel_tool = next(
            (
                tool for tool in tools
                if tool.name == "search_hotels"
            ),
            None
        )

        if not hotel_tool:
            return {
                "success": False,
                "provider": "VistaLink",
                "error": "search_hotels tool not found."
            }

        arguments = {
            "city": city,
            "guests": guests,
            "currency": "INR",
            "limit": 5,
            "include_rates": False
        }

        if check_in:
            arguments["check_in"] = check_in

        if check_out:
            arguments["check_out"] = check_out

        result = await hotel_tool.ainvoke(
            arguments
        )

        if not result:
            return {
                "success": False,
                "provider": "VistaLink",
                "error": "No response received from VistaLink."
            }

        text_content = result[0].get(
            "text",
            "{}"
        )

        data = json.loads(text_content)

        hotels = [
            normalize_hotel(hotel)
            for hotel in data.get("hotels", [])[:5]
        ]

        return {
            "success": True,
            "provider": "VistaLink",
            "city": city,
            "total_results": data.get(
                "total",
                len(hotels)
            ),
            "hotels": hotels
        }

    except Exception as e:
        return {
            "success": False,
            "provider": "VistaLink",
            "error": str(e)
        }