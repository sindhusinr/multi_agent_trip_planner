from datetime import datetime

from langchain_core.messages import AIMessage

from multi_agent_trip_planner.tools.weather_tool import (
    get_weather
)


def parse_trip_date(value: str):
    """Parse supported trip date formats."""

    for date_format in (
        "%d/%m/%Y",
        "%Y-%m-%d"
    ):
        try:
            return datetime.strptime(
                value,
                date_format
            ).date()

        except ValueError:
            continue

    return None


def weather_agent(state: dict) -> dict:
    """Return weather only when supported by the API."""

    print("\n>>> WEATHER AGENT")

    trip_details = state.get(
        "trip_details",
        {}
    )

    city = trip_details.get(
        "primary_city",
        ""
    )

    departure_date = trip_details.get(
        "departure_date",
        ""
    )

    trip_date = parse_trip_date(
        departure_date
    )

    # Current-weather API cannot answer future-date requests.
    if (
        trip_date
        and trip_date > datetime.now().date()
    ):
        return {
            "weather_results": {
                "success": False,
                "city": city,
                "requested_date": departure_date,
                "error": (
                    "Weather is unavailable for this "
                    "future trip date because the current "
                    "weather API does not provide forecasts "
                    "for that date."
                )
            },
            "messages": [
                AIMessage(
                    content="Future weather unavailable."
                )
            ]
        }

    weather_results = get_weather(city)

    return {
        "weather_results": weather_results,
        "messages": [
            AIMessage(
                content="Weather information generated."
            )
        ]
    }