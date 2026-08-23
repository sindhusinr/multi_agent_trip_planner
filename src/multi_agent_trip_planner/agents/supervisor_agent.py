import json
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY")
)

def supervisor_agent(state: dict) -> dict:

    prompt = f"""
You are a travel planning supervisor.

Available agents:

- flight_agent
- hotel_agent
- weather_agent
- itinerary_agent

Select only the required agents.

Return valid JSON:

{{
  "selected_agents": [],
  "reasoning": ""
}}

User Query:
{state["user_query"]}
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    try:
        data = json.loads(response.content)

        return {
            "selected_agents": data["selected_agents"],
            "supervisor_reasoning": data["reasoning"]
        }

    except Exception:

        return {
            "selected_agents": [
                "flight_agent",
                "hotel_agent",
                "weather_agent",
                "itinerary_agent"
            ],
            "supervisor_reasoning": "Fallback routing."
        }