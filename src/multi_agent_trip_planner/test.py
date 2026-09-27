import asyncio

from multi_agent_trip_planner.mcp.mcp_client import (
    get_mcp_tools
)


async def main():

    tools = await get_mcp_tools("vistalink")

    hotel_tool = next(
        (
            tool for tool in tools
            if tool.name == "search_hotels"
        ),
        None
    )

    if not hotel_tool:
        print("search_hotels tool not found.")
        return

    result = await hotel_tool.ainvoke({
        "city": "Mumbai",
        "guests": 1,
        "currency": "INR",
        "limit": 5,
        "include_rates": False
    })

    print("\n>>> RAW VISTALINK HOTEL RESULT")
    print("TYPE:", type(result))
    print("RESULT:", result)


asyncio.run(main())