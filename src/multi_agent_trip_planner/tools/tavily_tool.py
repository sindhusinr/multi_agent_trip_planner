import json

from multi_agent_trip_planner.mcp.mcp_client import (
    get_mcp_tools
)


async def tavily_search(query: str) -> str:
    """
    Search Tavily MCP and return a clean
    summary of hotel recommendations.
    """

    # Retrieve available MCP tools
    tools = await get_mcp_tools()

    # Locate the Tavily search tool
    search_tool = next(
        tool
        for tool in tools
        if tool.name == "tavily_search"
    )

    # Execute the Tavily search
    result = await search_tool.ainvoke(
        {
            "query": query
        }
    )

    try:

        # Extract the JSON payload
        payload = json.loads(
            result[0]["text"]
        )

        hotel_summaries = []

        # Process the top hotel recommendations
        for item in payload.get(
            "results",
            []
        )[:5]:

            title = item.get(
                "title",
                "Unknown Hotel"
            )

            content = item.get(
                "content",
                ""
            )[:300]

            hotel_summaries.append(
                f"Hotel: {title}\n"
                f"Details: {content}"
            )

        # Return a clean formatted string
        return "\n\n".join(
            hotel_summaries
        )

    except Exception as e:

        print(
            f"Tavily parsing error: {e}"
        )

        return (
            "Unable to retrieve hotel "
            "recommendations."
        )