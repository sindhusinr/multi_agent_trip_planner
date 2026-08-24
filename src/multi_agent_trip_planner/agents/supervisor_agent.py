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
    - Extract trip details
    """

    prompt = f"""
You are the supervisor of a multi-agent travel planning system.

Available agents:
- flight_agent
- hotel_agent
- weather_agent
- budget_agent
- itinerary_agent

Rules:

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

Return VALID JSON only.

Schema:

{{
  "selected_agents": [],
  "reasoning": "",
  "trip_details": {{
      "origin": "",
      "destination": "",
      "primary_city": "",
      "duration": "",
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
                content="Return valid JSON only. No markdown."
            ),
            HumanMessage(content=prompt)
        ])

        result = json.loads(response.content)

        print("\n>>> SUPERVISOR")
        print(result)

        return {
            "selected_agents": result.get("selected_agents", []),
            "supervisor_reasoning": result.get("reasoning", ""),
            "trip_details": result.get("trip_details", {})
        }

    except Exception as e:

        print("\n>>> SUPERVISOR FALLBACK")
        print(e)

        return {
            "selected_agents": FALLBACK_AGENTS,
            "supervisor_reasoning": f"Fallback routing used: {e}",
            "trip_details": {
                "origin": "",
                "destination": "",
                "primary_city": "",
                "duration": "",
                "budget": "",
                "travel_style": ""
            }
        }