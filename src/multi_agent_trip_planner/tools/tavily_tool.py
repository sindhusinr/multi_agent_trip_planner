import asyncio

from multi_agent_trip_planner.mcp.mcp_client import (
    get_mcp_tools
)


async def tavily_search(query: str) -> str:

    # Discover tools exposed by Tavily MCP
    tools = await get_mcp_tools()

    # Select tavily_search tool
    search_tool = next(
        tool
        for tool in tools
        if tool.name == "tavily_search"
    )

    # Execute search through remote MCP
    result = await search_tool.ainvoke(
        {
            "query": query
        }
    )

    return str(result)