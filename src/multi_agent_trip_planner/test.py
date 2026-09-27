import asyncio

from multi_agent_trip_planner.mcp.mcp_client import (
    get_mcp_tools
)


async def main():
    print("Starting Kiwi MCP test...")

    tools = await get_mcp_tools("kiwi")

    print(f"Tools found: {len(tools)}")
    print("\n=== KIWI MCP TOOLS ===")

    for tool in tools:
        print("\nTool:", tool.name)
        print("Description:", tool.description)
        print("Schema:", tool.args_schema)
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())