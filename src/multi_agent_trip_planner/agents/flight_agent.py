from langchain_core.messages import AIMessage
from multi_agent_trip_planner.tools.flight_tool import search_flights


def flight_agent(state: dict) -> dict:
    """
    Flight specialist agent.

    Retrieves flight information
    relevant to the travel request.
    """

    flight_results = search_flights(state["user_query"])

    return {
        "flight_results": flight_results,
        "messages": [
            AIMessage(content="Flight recommendations generated.")
        ]
    }