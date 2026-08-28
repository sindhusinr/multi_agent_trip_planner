import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import (
    MultiServerMCPClient
)

load_dotenv()


async def main():

    client = MultiServerMCPClient(
        {
            "aviationstack": {
                "transport": "stdio",
                "command": "uvx",
                "args": [
                    "aviationstack-mcp"
                ],
                "env": {
                    "AVIATION_STACK_API_KEY":
                        os.getenv(
                            "AVIATIONSTACK_API_KEY"
                        )
                }
            }
        }
    )

    tools = await client.get_tools(
        server_name="aviationstack"
    )

    for tool in tools:
        print(tool.name)


asyncio.run(main())