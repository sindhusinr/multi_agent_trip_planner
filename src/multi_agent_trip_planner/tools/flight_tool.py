"""
Flight search utilities.

This module is responsible for:
1. Calling AviationStack
2. Filtering flights by route
3. Formatting flight results
4. Returning travel-friendly flight data

Used by:
- Flight Agent
- Budget Agent (future)
- Itinerary Agent (future)
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

AVIATIONSTACK_BASE_URL = os.getenv(
    "AVIATIONSTACK_BASE_URL",
    "https://api.aviationstack.com/v1/flights"
)


def format_flight(flight: dict) -> str:
    """
    Convert raw AviationStack response
    into readable text.
    """

    airline = (
        flight.get("airline", {})
        .get("name", "Unknown Airline")
    )

    departure_airport = (
        flight.get("departure", {})
        .get("airport", "Unknown")
    )

    departure_iata = (
        flight.get("departure", {})
        .get("iata", "N/A")
    )

    arrival_airport = (
        flight.get("arrival", {})
        .get("airport", "Unknown")
    )

    arrival_iata = (
        flight.get("arrival", {})
        .get("iata", "N/A")
    )

    status = flight.get(
        "flight_status",
        "Unknown"
    )

    return (
        f"Airline: {airline}\n"
        f"Departure: {departure_airport} ({departure_iata})\n"
        f"Arrival: {arrival_airport} ({arrival_iata})\n"
        f"Status: {status}"
    )


def search_flights(
    origin_iata: str,
    destination_iata: str,
    limit: int = 5
) -> str:
    """
    Search flights between two airports.

    Example:

    search_flights("MAA", "NRT")
    """

    if not AVIATIONSTACK_API_KEY:
        return "AVIATIONSTACK_API_KEY not configured."

    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "dep_iata": origin_iata,
        "arr_iata": destination_iata,
        "limit": limit
    }

    try:
        response = requests.get(
            AVIATIONSTACK_BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        flights = data.get("data", [])

        print("\n=== AVIATIONSTACK ROUTE SEARCH ===")
        print(
            f"Searching: "
            f"{origin_iata} -> {destination_iata}"
        )

        if flights:
            print("\n=== FIRST MATCH ===")
            print(flights[0])

    except Exception as e:
        return f"Flight API error: {e}"

    if not flights:
        return (
            f"No flights found for route "
            f"{origin_iata} -> {destination_iata}"
        )

    return "\n\n".join(
        format_flight(flight)
        for flight in flights[:limit]
    )


if __name__ == "__main__":
    print(
        search_flights(
            "MAA",
            "NRT"
        )
    )