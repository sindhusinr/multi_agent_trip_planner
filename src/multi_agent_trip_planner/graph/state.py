from typing import TypedDict, Annotated, Any
import operator

from langchain_core.messages import AnyMessage


class TravelState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], operator.add]

    user_query: str

    trip_details: dict[str, Any]

    selected_agents: list[str]
    supervisor_reasoning: str

    flight_results: str
    hotel_results: str
    weather_results: str
    budget_results: str

    itinerary: str
    final_response: str