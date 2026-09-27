import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
OPEN_WEATHER_BASE_URL = os.getenv("OPEN_WEATHER_BASE_URL")

def get_weather(city: str) -> dict:
    """Fetch current weather and return structured data."""

    if not OPEN_WEATHER_API_KEY:
        return {
            "success": False,
            "error": "OPEN_WEATHER_API_KEY not configured."
        }

    params = {
        "q": city,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            OPEN_WEATHER_BASE_URL,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        # Keep API data structured for downstream agents.
        return {
            "success": True,
            "city": data.get("name", city),
            "condition": data["weather"][0]["description"],
            "temperature_c": data["main"]["temp"],
            "humidity_percent": data["main"]["humidity"],
            "wind_speed_mps": data["wind"]["speed"]
        }

    except Exception as e:
        return {
            "success": False,
            "city": city,
            "error": str(e)
        }