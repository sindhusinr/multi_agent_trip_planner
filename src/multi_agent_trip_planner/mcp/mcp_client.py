import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


async def get_mcp_tools():

    # Load Tavily API key from .env
    tavily_key = os.getenv("TAVILY_API_KEY")

    # Create MCP client
    client = MultiServerMCPClient(
        {
            "tavily": {

                # Tavily is a remote MCP server
                # so communication happens over HTTP
                "transport": "streamable_http",

                # Tavily MCP endpoint
                "url": (
                    f"https://mcp.tavily.com/mcp/"
                    f"?tavilyApiKey={tavily_key}"
                )
            }
        }
    )

    # Discover tools exposed by Tavily MCP
    tools = await client.get_tools()

    # Return tools such as:
    # tavily_search
    # tavily_extract
    # tavily_crawl
    # tavily_map
    # tavily_research
    return tools