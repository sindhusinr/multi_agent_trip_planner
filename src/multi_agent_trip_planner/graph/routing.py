from langgraph.graph import END
AGENT_ORDER = [
    "flight_agent",
    "hotel_agent",
    "weather_agent",
    "budget_agent",
]


def route_from_supervisor(state):
    selected = state.get("selected_agents", [])

    for agent in AGENT_ORDER:
        if agent in selected:
            return agent

    if "itinerary_agent" in selected:
        return "itinerary_agent"

    return END


def route_after(current_agent):
    def router(state):

        selected = state.get("selected_agents", [])

        current_index = AGENT_ORDER.index(current_agent)

        for agent in AGENT_ORDER[current_index + 1:]:
            if agent in selected:
                return agent

        if "itinerary_agent" in selected:
            return "itinerary_agent"

        return END

    return router