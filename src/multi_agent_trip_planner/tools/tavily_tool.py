import json

from multi_agent_trip_planner.mcp.mcp_client import get_mcp_tools


async def tavily_search(query: str) -> dict:
    """Search Tavily MCP and return structured hotel results."""

    try:
        tools = await get_mcp_tools("tavily")

        search_tool = next(
            (
                tool for tool in tools
                if tool.name == "tavily_search"
            ),
            None
        )

        if not search_tool:
            return {
                "success": False,
                "error": "Tavily search tool not found."
            }

        result = await search_tool.ainvoke(
            {"query": query}
        )

        if not result:
            return {
                "success": False,
                "error": "No response received from Tavily."
            }

        # MCP returns JSON inside a text block.
        payload = json.loads(
            result[0].get("text", "{}")
        )

        hotels = []

        # Keep top 5 results.
        for item in payload.get("results", [])[:5]:
            hotels.append({
                "name": item.get("title", ""),
                "description": item.get("content", "")[:300],
                "url": item.get("url", "")
            })

        return {
            "success": True,
            "provider": "Tavily",
            "hotels": hotels
        }

    except Exception as e:
        return {
            "success": False,
            "provider": "Tavily",
            "error": str(e)
        }