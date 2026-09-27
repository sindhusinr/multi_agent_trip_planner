from langgraph.types import interrupt


# Required fields for each specialist agent.
AGENT_REQUIRED_FIELDS = {
    "flight_agent": [
        "origin",
        "destination",
        "departure_date"
    ],
    "hotel_agent": [
        "destination"
    ],
    "weather_agent": [
        "primary_city"
    ],
    "itinerary_agent": [
        "destination"
    ]
}


# User-friendly questions for missing trip information.
FIELD_QUESTIONS = {
    "origin": "What city are you departing from?",
    "destination": "What is your destination?",
    "primary_city": "Which city are you traveling to?",
    "departure_date": "What is your departure date? Please use DD/MM/YYYY format."
}


def trip_validator(state: dict) -> dict:
    """
    Validate required fields before specialist agents execute.
    Pauses the graph when required information is missing.
    """

    trip_details = state.get("trip_details", {}).copy()
    selected_agents = state.get("selected_agents", [])

    # Collect required fields based on selected agents.
    required_fields = []

    for agent in selected_agents:
        for field in AGENT_REQUIRED_FIELDS.get(agent, []):
            if field not in required_fields:
                required_fields.append(field)

    # Ask for missing fields one at a time.
    for field in required_fields:

        if not trip_details.get(field):

            question = FIELD_QUESTIONS.get(
                field,
                f"Please provide {field}."
            )

            # Pause graph execution and wait for user input.
            user_answer = interrupt({
                "missing_field": field,
                "question": question
            })

            # Resume value becomes the missing trip value.
            trip_details[field] = str(user_answer).strip()

            # Keep destination and primary_city aligned.
            if field == "destination" and not trip_details.get("primary_city"):
                trip_details["primary_city"] = str(user_answer).strip()

    return {
        "trip_details": trip_details,
        "missing_fields": [],
        "clarification_question": ""
    }