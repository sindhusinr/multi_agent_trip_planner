from langchain_core.messages import AIMessage
from multi_agent_trip_planner.tools.flight_tool import search_flights


def flight_agent(state: dict) -> dict:
    """
    Flight specialist agent.

    Takes user query from state,
    retrieves flight information,
    stores result back into state.
    """

    flights = search_flights(state["user_query"])

    return {
        "flight_results": flights,
        "messages": [
            AIMessage(content="Flight information generated.")
        ]
    }