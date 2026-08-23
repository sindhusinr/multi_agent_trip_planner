from typing import Annotated, Any, TypedDict
from langchain_core.messages import AnyMessage
import operator


class TravelState(TypedDict, total=False):
    # Chat history
    messages: Annotated[list[AnyMessage], operator.add]

    # User request
    user_query: str

    # Guardrail
    guardrail_allowed: bool
    guardrail_reason: str

    # Supervisor
    selected_agents: list[str]
    supervisor_reasoning: str

    # Agent outputs
    flight_results: str
    hotel_results: str
    weather_results: str
    budget_results: str
    itinerary: str

    # HITL
    approval_request: str
    approved: bool
    human_feedback: str

    # Final answer
    final_response: str

    # Metrics
    llm_calls: int

    # Extra metadata
    trip_constraints: dict[str, Any]