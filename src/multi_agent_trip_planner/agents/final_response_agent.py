import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY")
)


def final_response_agent(state: dict) -> dict:
    """
    Build the final response using only grounded state data.
    """

    selected_agents = state.get(
        "selected_agents",
        []
    )

    trip_details = state.get(
        "trip_details",
        {}
    )

    prompt = f"""
You are the final response agent for a travel planning application.

Your responsibility is ONLY to organize, summarize and format
information already produced by the system.

User Request:
{state.get("user_query", "")}

Trip Details:
{trip_details}

Selected Agents:
{selected_agents}

Flight Results:
{state.get("flight_results", "")}

Hotel Results:
{state.get("hotel_results", "")}

Weather Results:
{state.get("weather_results", "")}

Budget Results:
{state.get("budget_results", "")}

Itinerary:
{state.get("itinerary", "")}

GROUNDING RULES:

1. Use ONLY facts explicitly present in:
   - Trip Details
   - Flight Results
   - Hotel Results
   - Weather Results
   - Budget Results
   - Itinerary

2. Do NOT add facts from your own knowledge.

3. Do NOT invent or infer:
   - dates
   - return dates
   - prices
   - exchange rates
   - weather
   - flights
   - hotels
   - transportation
   - visa information
   - safety advice
   - tipping advice
   - SIM or connectivity advice
   - booking information

4. Do not calculate missing values unless the calculated
   value is explicitly present in the provided results.

5. If a result has success=False, briefly explain the
   provided error. Do not replace it with your own answer.

6. Preserve currencies exactly as returned by the provider.
   Do not perform currency conversion.

7. Do not expose:
   - agent names
   - routing
   - internal state
   - internal reasoning

8. Do not repeat information.

9. Do not add generic travel tips.

10. The Itinerary may contain activity suggestions.
    Present those suggestions as provided, but do not add
    additional places, restaurants or activities.

RESPONSE RULES:

For a simple request:
- Answer only the requested information.
- Keep the response concise.

For a complete trip-planning request:
Include only relevant sections that contain information:

- Trip Overview
- Flights
- Stay
- Weather
- Budget
- Itinerary

If a section has no information and was not requested,
omit it.

If requested information is unavailable,
state that briefly.

Return only the final user-facing response.
"""

    response = llm.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )

    return {
        "final_response": response.content
    }