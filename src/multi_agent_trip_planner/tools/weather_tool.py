import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
OPEN_WEATHER_BASE_URL = os.getenv("OPEN_WEATHER_BASE_URL")
def get_weather(city: str) -> str:
    """
    Fetch current weather for a city.
    """

    if not OPEN_WEATHER_API_KEY:
        return "OPEN_WEATHER_API_KEY not configured."

    params = {
        "q": city,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(OPEN_WEATHER_BASE_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        return (
            f"City: {city}\n"
            f"Weather: {weather}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s"
        )

    except Exception as e:
        return f"Weather API error: {e}"