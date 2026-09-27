from typing import TypedDict, Annotated, Any
import operator

from langchain_core.messages import AnyMessage


class TravelState(TypedDict, total=False):
    # Conversation state accumulated across graph execution.
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str

    # Guardrail state.
    allowed: bool
    guardrail_reason: str

    # Trip information extracted and preserved across turns.
    trip_details: dict[str, Any]

    # Supervisor routing decisions.
    selected_agents: list[str]
    supervisor_reasoning: str

    # HITL state used when required trip information is missing.
    missing_fields: list[str]
    clarification_question: str

    # Structured outputs produced by specialist agents.
    flight_results: dict[str, Any]
    hotel_results: dict[str, Any]
    weather_results: dict[str, Any]
    budget_results: dict[str, Any]

    # User-facing planning outputs.
    itinerary: str
    final_response: str