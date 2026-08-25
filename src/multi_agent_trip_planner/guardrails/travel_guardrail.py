from multi_agent_trip_planner.guardrails.constants import (
    TRAVEL_KEYWORDS,
    BLOCKED_KEYWORDS,
)


def validate_query(query: str) -> dict:
    """
    Validate whether the query should enter
    the travel planning workflow.
    """

    query_lower = query.lower()

    # Prompt injection checks
    for pattern in BLOCKED_KEYWORDS:
        if pattern in query_lower:
            return {
                "allowed": False,
                "reason": (
                    "Prompt injection attempt detected."
                )
            }

    # Travel domain check
    if not any(
        keyword in query_lower
        for keyword in TRAVEL_KEYWORDS
    ):
        return {
            "allowed": False,
            "reason": (
                "Query is outside the travel domain."
            )
        }

    return {
        "allowed": True,
        "reason": "Validation passed."
    }