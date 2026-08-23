from langchain_core.messages import AIMessage

from multi_agent_trip_planner.tools.location_tool import extract_destination
from multi_agent_trip_planner.tools.weather_tool import get_weather


def weather_agent(state: dict) -> dict:
    destination = extract_destination(state["user_query"])

    weather_results = get_weather(destination)

    return {
        "weather_results": weather_results,
        "messages": [
            AIMessage(content="Weather information generated.")
        ]
    }