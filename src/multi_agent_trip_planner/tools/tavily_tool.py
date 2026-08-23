import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file")


tavily_search_tool = TavilySearch(
    max_results=5,
    tavily_api_key=TAVILY_API_KEY
)


def tavily_search(query: str) -> str:
    """
    Search the web using Tavily and return formatted results.
    """

    try:
        response = tavily_search_tool.invoke(query)

        results = []

        for i, result in enumerate(response["results"], start=1):
            title = result.get("title", "No Title")
            url = result.get("url", "")
            content = result.get("content", "")

            if len(content) > 300:
                content = content[:300] + "..."

            results.append(
                f"{i}. {title}\n"
                f"URL: {url}\n"
                f"{content}"
            )

        return "\n\n".join(results)

    except Exception as e:
        return f"Tavily search failed: {e}"


if __name__ == "__main__":
    print(tavily_search("Best hotels in Tokyo"))