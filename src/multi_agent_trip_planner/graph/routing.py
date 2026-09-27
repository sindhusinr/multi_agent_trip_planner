from langgraph.graph import END

# Defines execution priority when multiple specialist agents are selected.
AGENT_ORDER = ["flight_agent", "hotel_agent", "weather_agent", "budget_agent"]

# Routes supervisor output to the first selected specialist agent.
def route_from_supervisor(state):
    selected = state.get("selected_agents", [])

    for agent in AGENT_ORDER:
        if agent in selected:
            return agent

    if "itinerary_agent" in selected:
        return "itinerary_agent"

    # Even when no specialist is required, generate one user-facing response.
    return "final_response_agent"

# After one specialist finishes, finds the next selected agent in execution order.
def route_after(current_agent):
    def router(state):
        selected = state.get("selected_agents", [])
        current_index = AGENT_ORDER.index(current_agent)

        for agent in AGENT_ORDER[current_index + 1:]:
            if agent in selected:
                return agent

        if "itinerary_agent" in selected:
            return "itinerary_agent"

        # All selected agents completed; move to final response synthesis.
        return "final_response_agent"

    return router

# Allows valid travel queries to continue; blocked queries terminate immediately.
def route_after_guardrail(state):
    if state.get("allowed"):
        return "supervisor"

    return END