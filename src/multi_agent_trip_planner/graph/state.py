from typing import Annotated, TypedDict
import operator

from langchain_core.messages import AnyMessage

class TravelState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], operator.add]

    user_query: str

    selected_agents: list[str]
    supervisor_reasoning: str

    flight_results: str
    hotel_results: str
    weather_results: str

    itinerary: str