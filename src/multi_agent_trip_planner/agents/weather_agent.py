from langchain_core.messages import AIMessage

from multi_agent_trip_planner.tools.weather_tool import get_weather


def weather_agent(state: dict) -> dict:
    city = state.get("trip_details", {}).get("primary_city", "")

    weather_results = get_weather(city)

    return {
        "weather_results": weather_results,
        "messages": [
            AIMessage(content="Weather information generated.")
        ]
    }