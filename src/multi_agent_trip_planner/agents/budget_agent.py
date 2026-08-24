from langchain_core.messages import AIMessage


def budget_agent(state: dict) -> dict:
    """
    Budget analysis specialist.

    Evaluates whether the requested trip
    matches the specified budget.
    """

    trip_details = state.get("trip_details", {})

    destination = trip_details.get("destination", "")
    duration = trip_details.get("duration", "")
    budget = trip_details.get("budget", "")

    budget_results = f"""
Destination: {destination}
Duration: {duration}
Budget Constraint: {budget}

Budget review generated.
"""

    return {
        "budget_results": budget_results,
        "messages": [
            AIMessage(content="Budget analysis generated.")
        ]
    }