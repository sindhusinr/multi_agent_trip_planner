import json

from multi_agent_trip_planner.mcp.mcp_client import get_mcp_tools


CABIN_CLASS_MAP = {
    "economy": "M",
    "premium economy": "W",
    "business": "C",
    "first": "F"
}


def normalize_flight(itinerary: dict) -> dict:
    """
    Convert Kiwi itinerary into our internal flight format.
    """

    outbound = itinerary.get("outbound", {})
    segments = outbound.get("segments", [])

    first_segment = segments[0] if segments else {}
    last_segment = segments[-1] if segments else {}

    return {
        "airline": first_segment.get("carrierName", ""),
        "flight_number": first_segment.get("flightNumber", ""),

        "departure_airport": outbound.get("from", ""),
        "arrival_airport": outbound.get("to", ""),

        "departure_city": first_segment.get("fromCity", ""),
        "arrival_city": last_segment.get("toCity", ""),

        "departure_time": outbound.get("departureTime", ""),
        "arrival_time": outbound.get("arrivalTime", ""),

        "duration_seconds": outbound.get(
            "durationSeconds"
        ),

        "stops": outbound.get("stops", 0),

        "cabin_class": outbound.get(
            "cabinClass",
            ""
        ),

        "price": itinerary.get("price"),
        "price_formatted": itinerary.get(
            "priceFormatted",
            ""
        ),

        "booking_url": itinerary.get(
            "bookingUrl",
            ""
        ),

        "baggage": itinerary.get(
            "baggage",
            {}
        )
    }


async def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    adults: int = 1,
    cabin_class: str = "economy",
    return_date: str = ""
) -> dict:
    """
    Search Kiwi MCP and return normalized flight results.
    """

    try:
        tools = await get_mcp_tools("kiwi")

        flight_tool = next(
            (
                tool for tool in tools
                if tool.name == "search-flight"
            ),
            None
        )

        if not flight_tool:
            return {
                "success": False,
                "provider": "Kiwi.com",
                "error": "Kiwi search-flight tool not found."
            }

        arguments = {
            "flyFrom": origin,
            "flyTo": destination,
            "departureDate": departure_date,
            "adults": adults,
            "currency": "INR",
            "locale": "en",
            "sort": "price"
        }

        cabin_code = CABIN_CLASS_MAP.get(
            cabin_class.lower()
        )

        if cabin_code:
            arguments["cabinClass"] = cabin_code

        if return_date:
            arguments["returnDate"] = return_date

        # Call Kiwi Remote MCP.
        result = await flight_tool.ainvoke(arguments)

        # MCP returns a list containing a text block.
        if not result:
            return {
                "success": False,
                "provider": "Kiwi.com",
                "error": "No response received from Kiwi."
            }

        text_content = result[0].get(
            "text",
            "{}"
        )

        kiwi_data = json.loads(text_content)

        itineraries = kiwi_data.get(
            "itineraries",
            []
        )

        # Keep only top 5 results to reduce downstream tokens.
        flights = [
            normalize_flight(itinerary)
            for itinerary in itineraries[:5]
        ]

        return {
            "success": True,
            "provider": "Kiwi.com",

            "origin": origin,
            "destination": destination,

            "departure_date": departure_date,
            "return_date": return_date,

            "adults": adults,
            "cabin_class": cabin_class,

            "currency": kiwi_data.get(
                "currency",
                "INR"
            ),

            "total_results": kiwi_data.get(
                "resultsCount",
                len(itineraries)
            ),

            "flights": flights
        }

    except Exception as e:
        return {
            "success": False,
            "provider": "Kiwi.com",
            "error": str(e)
        }