import json
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY")
)

FALLBACK_AGENTS = [
    "flight_agent",
    "hotel_agent",
    "weather_agent",
    "budget_agent",
    "itinerary_agent"
]


def supervisor_agent(state: dict) -> dict:
    """
    Main orchestration agent.

    Responsibilities:
    - Understand user intent
    - Select required agents
    - Extract structured trip details
    """

    prompt = f"""
You are the supervisor of a multi-agent travel planning system.

Available agents:
- flight_agent
- hotel_agent
- weather_agent
- budget_agent
- itinerary_agent

Agent Selection Rules:

1. Full trip planning requests should include:
   - flight_agent
   - hotel_agent
   - weather_agent
   - itinerary_agent

2. Weather-only queries should include:
   - weather_agent

3. Hotel-only queries should include:
   - hotel_agent

4. Flight-only queries should include:
   - flight_agent

5. Budget-related queries should include:
   - budget_agent

6. Include itinerary_agent ONLY when a complete trip plan is requested.

Trip Detail Extraction Rules:

- Always extract trip_details.
- Never leave primary_city empty when destination is known.
- primary_city should be the main city used for flight
  and weather lookups.

Examples:

Japan -> Tokyo
France -> Paris
Thailand -> Bangkok
Singapore -> Singapore
UAE -> Dubai
Italy -> Rome
Germany -> Berlin

If a city is explicitly mentioned:

Tokyo -> Tokyo
Kyoto -> Kyoto
Osaka -> Osaka
Chennai -> Chennai

Return VALID JSON ONLY.

Example Output:

{{
    "selected_agents": [
        "flight_agent",
        "hotel_agent",
        "weather_agent",
        "itinerary_agent"
    ],
    "reasoning": "User requested a complete trip plan.",
    "trip_details": {{
        "origin": "Chennai",
        "destination": "Japan",
        "primary_city": "Tokyo",
        "duration": "7 days",
        "budget": "",
        "travel_style": ""
    }}
}}

User Query:
{state["user_query"]}
"""

    try:
        response = llm.invoke([
            SystemMessage(
                content=(
                    "Return only valid JSON. "
                    "Do not wrap in markdown."
                )
            ),
            HumanMessage(content=prompt)
        ])

        result = json.loads(response.content)

        print("\n>>> SUPERVISOR")
        print(result)

        trip_details = result.get("trip_details", {})

        return {
            "selected_agents": result.get(
                "selected_agents",
                []
            ),
            "supervisor_reasoning": result.get(
                "reasoning",
                ""
            ),
            "trip_details": {
                "origin": trip_details.get(
                    "origin",
                    ""
                ),
                "destination": trip_details.get(
                    "destination",
                    ""
                ),
                "primary_city": trip_details.get(
                    "primary_city",
                    ""
                ),
                "duration": trip_details.get(
                    "duration",
                    ""
                ),
                "budget": trip_details.get(
                    "budget",
                    ""
                ),
                "travel_style": trip_details.get(
                    "travel_style",
                    ""
                )
            }
        }

    except Exception as e:

        print("\n>>> SUPERVISOR FALLBACK")
        print(e)

        return {
            "selected_agents": FALLBACK_AGENTS,
            "supervisor_reasoning": (
                f"Fallback routing used: {e}"
            ),
            "trip_details": {
                "origin": "",
                "destination": "",
                "primary_city": "",
                "duration": "",
                "budget": "",
                "travel_style": ""
            }
        }