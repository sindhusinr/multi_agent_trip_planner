from langgraph.graph import END


# Execution priority for specialist agents.
AGENT_ORDER = [
    "flight_agent",
    "hotel_agent",
    "weather_agent",
    "budget_agent"
]


def route_from_supervisor(state):
    """
    Route to the first selected specialist after validation.
    """

    selected = state.get("selected_agents", [])

    for agent in AGENT_ORDER:
        if agent in selected:
            return agent

    if "itinerary_agent" in selected:
        return "itinerary_agent"

    return "final_response_agent"


def route_after(current_agent):
    """
    Find the next selected specialist agent.
    """

    def router(state):

        selected = state.get("selected_agents", [])
        current_index = AGENT_ORDER.index(current_agent)

        for agent in AGENT_ORDER[current_index + 1:]:
            if agent in selected:
                return agent

        if "itinerary_agent" in selected:
            return "itinerary_agent"

        return "final_response_agent"

    return router


def route_after_guardrail(state):
    """
    Continue valid requests to the supervisor.
    """

    if state.get("allowed"):
        return "supervisor"

    return END