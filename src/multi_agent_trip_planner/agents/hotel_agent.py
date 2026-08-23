from langchain_core.messages import AIMessage
from multi_agent_trip_planner.tools.tavily_tool import tavily_search


def hotel_agent(state: dict) -> dict:
    query = f"Best hotels for {state['user_query']}"

    hotels = tavily_search(query)

    return {
        "hotel_results": hotels,
        "messages": [
            AIMessage(content="Hotel information generated.")
        ]
    }