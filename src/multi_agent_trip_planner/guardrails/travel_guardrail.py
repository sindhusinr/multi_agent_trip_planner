def validate_query(
    query: str,
    trip_details: dict | None = None
) -> dict:

    query_lower = query.lower()

    blocked_keywords = [
        "ignore previous instructions",
        "ignore all instructions",
        "system prompt",
        "developer prompt",
        "reveal prompt",
        "show hidden prompt",
        "jailbreak",
        "bypass guardrails",
        "override instructions",
        "forget previous instructions",
    ]

    travel_keywords = [
        "trip",
        "travel",
        "vacation",
        "holiday",
        "itinerary",
        "flight",
        "hotel",
        "visit",
        "tour",
        "destination",
    ]

    # Security checks always run first
    for pattern in blocked_keywords:

        if pattern in query_lower:

            return {
                "allowed": False,
                "reason": (
                    "Prompt injection attempt detected."
                )
            }

    # Existing trip context exists
    if trip_details:

        return {
            "allowed": True,
            "reason": (
                "Follow-up trip request."
            )
        }

    # First message must be travel related
    if not any(
        keyword in query_lower
        for keyword in travel_keywords
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