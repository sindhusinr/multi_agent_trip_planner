def validate_query(
    query: str,
    trip_details: dict | None = None
) -> dict:

    query_lower = query.lower().strip()

    # ==========================================================
    # BLOCKED KEYWORDS / PROMPT INJECTION
    # ==========================================================

    blocked_keywords = [
        # Instruction manipulation
        "ignore previous instructions",
        "ignore my previous instructions",
        "ignore all instructions",
        "ignore my instructions",
        "ignore the previous instructions",
        "ignore everything above",
        "ignore everything before",
        "forget previous instructions",
        "forget my previous instructions",
        "disregard previous instructions",
        "disregard my previous instructions",
        "disregard all instructions",
        "discard previous instructions",
        "discard my previous instructions",
        "discard my instruction",
        "discard the instruction",

        # Prompt extraction
        "system prompt",
        "system message",
        "developer prompt",
        "developer message",
        "reveal prompt",
        "reveal the prompt",
        "show prompt",
        "show me the prompt",
        "show hidden prompt",
        "hidden prompt",
        "hidden instructions",

        # Jailbreak / guardrail manipulation
        "jailbreak",
        "bypass guardrails",
        "bypass the guardrails",
        "bypass restrictions",
        "bypass safety",
        "override instructions",
        "override the instructions",
        "override system instructions",
        "override developer instructions",

        # Role / mode manipulation
        "developer mode",
        "admin mode",
        "developer override",
    ]

    # ==========================================================
    # TRAVEL KEYWORDS
    # ==========================================================

    travel_keywords = [
        "trip",
        "travel",
        "vacation",
        "holiday",
        "itinerary",
        "flight",
        "flights",
        "hotel",
        "hotels",
        "visit",
        "tour",
        "destination",
    ]

    # ==========================================================
    # TRAVEL INFORMATION KEYWORDS
    # ==========================================================

    travel_info_keywords = [
        "weather",
        "temperature",
        "forecast",
        "climate",
        "things to do",
        "places to visit",
        "sightseeing",
        "attractions",
        "restaurant",
        "restaurants",
        "visa",
        "currency",
        "airport",
        "transport",
        "transportation",
        "tourist",
    ]

    # ==========================================================
    # SECURITY CHECK
    # ==========================================================

    # Security checks ALWAYS run first.
    # This must happen before checking trip_details.

    for pattern in blocked_keywords:

        if pattern in query_lower:

            return {
                "allowed": False,
                "guardrail_reason": """
✈️ I'm an AI Travel Assistant.

I can help with:

• ✈️ Flight information
• 🏨 Hotel recommendations
• 🌦 Weather updates
• 💰 Trip budget planning
• 🗺 Travel itineraries

Try asking:

• Weather in Chennai
• Flights from Delhi to Dubai
• Best hotels in Goa
• Plan a 5 day trip to Kerala
• Budget for a Bali vacation

Please ask a travel-related question.
"""
            }

    # ==========================================================
    # ADDITIONAL INSTRUCTION MANIPULATION CHECK
    # ==========================================================

    instruction_words = [
        "ignore",
        "disregard",
        "forget",
        "override",
        "bypass",
    ]

    instruction_targets = [
        "instruction",
        "instructions",
        "prompt",
        "prompts",
        "rules",
        "guardrail",
        "guardrails",
        "system",
        "developer",
    ]

    has_instruction_word = any(
        word in query_lower
        for word in instruction_words
    )

    has_instruction_target = any(
        word in query_lower
        for word in instruction_targets
    )

    if (
        has_instruction_word
        and has_instruction_target
    ):

        return {
            "allowed": False,
            "guardrail_reason": """
✈️ I'm an AI Travel Assistant.

I can only help with travel-related requests such as:

• ✈️ Flights
• 🏨 Hotels
• 🌦 Weather
• 💰 Trip budgets
• 🗺 Travel itineraries

Please ask a travel-related question.
"""
        }

    # ==========================================================
    # EXISTING TRIP CONTEXT
    # ==========================================================

    # Security checks have already been completed above.
    # Therefore a blocked query cannot bypass the guardrail
    # just because trip_details already exists.

    if trip_details:

        return {
            "allowed": True,
            "guardrail_reason": "Follow-up trip request."
        }

    # ==========================================================
    # FIRST MESSAGE MUST BE TRAVEL RELATED
    # ==========================================================

    if not any(
        keyword in query_lower
        for keyword in (
            travel_keywords +
            travel_info_keywords
        )
    ):

        return {
            "allowed": False,
            "guardrail_reason": """
✈️ I'm an AI Travel Assistant.

I can help with:

• ✈️ Flight information
• 🏨 Hotel recommendations
• 🌦 Weather updates
• 💰 Trip budget planning
• 🗺 Travel itineraries

Examples:

• What's the weather in Bangalore?
• Find flights from Chennai to Mumbai
• Suggest hotels in Dubai
• Plan a 3-day Goa itinerary
• Estimate budget for a Europe trip

Please ask a travel-related question.
"""
        }

    # ==========================================================
    # VALIDATION PASSED
    # ==========================================================

    return {
        "allowed": True,
        "guardrail_reason": "Validation passed."
    }