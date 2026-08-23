from .state import TravelState


def default_state(user_query: str) -> TravelState:
    return {
        "user_query": user_query,
        "guardrail_allowed": True,
        "guardrail_reason": "",
        "selected_agents": [],
        "supervisor_reasoning": "",
        "flight_results": "",
        "hotel_results": "",
        "weather_results": "",
        "budget_results": "",
        "itinerary": "",
        "approval_request": "",
        "approved": False,
        "human_feedback": "",
        "final_response": "",
        "llm_calls": 0,
        "trip_constraints": {},
    }