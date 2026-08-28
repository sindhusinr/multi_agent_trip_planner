import asyncio

from multi_agent_trip_planner.mcp.test_aviation_mcp import (
    get_mcp_tools
)


async def main():

    tools = await get_mcp_tools()

    for tool in tools:
        print(tool.name)


asyncio.run(main())