"""
Flight search utilities.

This module is responsible for:
1. Calling AviationStack
2. Formatting flight results
3. Returning travel-friendly flight data

Used by:
- Flight Agent
- Budget Agent (future)
- Itinerary Agent (future)
"""

import os
import requests
import certifi
from dotenv import load_dotenv

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
AVIATIONSTACK_BASE_URL = os.getenv("AVIATIONSTACK_BASE_URL")
def format_flight(flight: dict) -> str:
    """
    Convert raw AviationStack
    response into readable text.
    """

    airline = (
        flight.get("airline", {})
        .get("name", "Unknown Airline")
    )

    departure = (
        flight.get("departure", {})
        .get("airport", "Unknown")
    )

    arrival = (
        flight.get("arrival", {})
        .get("airport", "Unknown")
    )

    status = flight.get(
        "flight_status",
        "Unknown"
    )

    return f"""
Airline: {airline}
Departure: {departure}
Arrival: {arrival}
Status: {status}
""".strip()

def search_flights(query: str, limit: int = 5) -> str:
    if not AVIATIONSTACK_API_KEY:
        return "AVIATIONSTACK_API_KEY not configured."

    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "limit": limit
    }

    try:
        response = requests.get(
            AVIATIONSTACK_BASE_URL,
            params=params,
            timeout=30,
            verify = False
        )

        response.raise_for_status()
        data = response.json()

    except Exception as e:
        return f"Flight API error: {e}"

    flights = data.get("data", [])

    if not flights:
        return "No live flight data available."

    return "\n\n".join(
        format_flight(flight)
        for flight in flights[:limit]
    )

if __name__ == "__main__":
    print(search_flights("Plan a 7 day Japan trip from Chennai"))