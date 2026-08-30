from multi_agent_trip_planner.guardrails.travel_guardrail import (
    validate_query
)


def guardrail_agent(state: dict) -> dict:

    print("\n==============================")
    print(">>> GUARDRAIL START")
    print("==============================")

    print("USER QUERY:")
    print(state.get("user_query"))

    print("TRIP DETAILS:")
    print(state.get("trip_details"))

    result = validate_query(
        query=state["user_query"],
        trip_details=state.get("trip_details")
    )

    print("VALIDATE QUERY RESULT:")
    print(result)

    output = {
        "allowed": result["allowed"],
        "guardrail_reason": result["guardrail_reason"]
    }

    print("GUARDRAIL OUTPUT:")
    print(output)

    print("==============================")
    print(">>> GUARDRAIL END")
    print("==============================\n")

    return output