from multi_agent_trip_planner.guardrails.travel_guardrail import (
    validate_query
)


def guardrail_agent(state: dict) -> dict:

    print(">>> GUARDRAIL")

    result = validate_query(
        query=state["user_query"],
        trip_details=state.get(
            "trip_details"
        )
    )

    return {
        "allowed": result["allowed"],
        "guardrail_reason": result["reason"]
    }