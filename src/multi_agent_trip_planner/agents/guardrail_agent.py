from multi_agent_trip_planner.guardrails.travel_guardrail import (
    validate_query
)


def guardrail_agent(state: dict) -> dict:
    print(">>> GUARDRAIL")

    result = validate_query(
        state["user_query"]
    )

    return {
        "allowed": result["allowed"],
        "guardrail_reason": result["reason"]
    }