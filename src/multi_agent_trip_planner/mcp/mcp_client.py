import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


def get_mcp_client():
    """
    Create a shared MCP client for configured remote MCP servers.
    """

    tavily_key = os.getenv("TAVILY_API_KEY")
    kiwi_mcp_url = os.getenv("KIWI_MCP_URL")

    servers = {}

    # Tavily Remote MCP
    if tavily_key:
        servers["tavily"] = {
            "transport": "streamable_http",
            "url": (
                f"https://mcp.tavily.com/mcp/"
                f"?tavilyApiKey={tavily_key}"
            )
        }

    # Kiwi Remote MCP
    if kiwi_mcp_url:
        servers["kiwi"] = {
            "transport": "streamable_http",
            "url": kiwi_mcp_url
        }

    if not servers:
        raise ValueError("No MCP servers are configured.")

    return MultiServerMCPClient(servers)


async def get_mcp_tools(server_name: str | None = None):
    """
    Discover tools from all MCP servers or one specific server.
    """

    client = get_mcp_client()

    if server_name:
        return await client.get_tools(
            server_name=server_name
        )

    return await client.get_tools()