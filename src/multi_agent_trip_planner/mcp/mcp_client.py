import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


def get_mcp_client():

    tavily_key = os.getenv("TAVILY_API_KEY")
    kiwi_mcp_url = os.getenv("KIWI_MCP_URL")

    vistalink_key = os.getenv("VISTALINK_API_KEY")
    vistalink_mcp_url = os.getenv("VISTALINK_MCP_URL")

    servers = {}

    # Tavily Remote MCP
    if tavily_key:
        servers["tavily"] = {
            "transport": "streamable_http",
            "url": (
                "https://mcp.tavily.com/mcp/"
                f"?tavilyApiKey={tavily_key}"
            )
        }

    # Kiwi Remote MCP
    if kiwi_mcp_url:
        servers["kiwi"] = {
            "transport": "streamable_http",
            "url": kiwi_mcp_url
        }

    # VistaLink Remote MCP
    if vistalink_key and vistalink_mcp_url:
        servers["vistalink"] = {
            "transport": "streamable_http",
            "url": vistalink_mcp_url,
            "headers": {
                "Authorization": f"Bearer {vistalink_key}"
            }
        }

    if not servers:
        raise ValueError(
            "No MCP servers are configured."
        )

    return MultiServerMCPClient(servers)


async def get_mcp_tools(
    server_name: str | None = None
):

    client = get_mcp_client()

    if server_name:
        return await client.get_tools(
            server_name=server_name
        )

    return await client.get_tools()