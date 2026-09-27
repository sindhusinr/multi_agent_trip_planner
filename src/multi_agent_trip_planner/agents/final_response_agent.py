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
    selected_agents = state.get("selected_agents", [])
    trip_details = state.get("trip_details", {})

    prompt = f"""
You are the final response agent for a travel planning application.

Your job is to create ONE clean user-facing response from the results
produced by specialist agents.

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

RULES:

1. Answer only what is relevant to the user's request.
2. Do not expose internal agent names, routing, state or reasoning.
3. Do not invent flights, hotels, prices, weather or trip details.
4. Use only information available in the provided results.
5. Do not repeat the same information in multiple sections.
6. If information is unavailable, say so briefly.
7. Keep simple requests concise.
8. Use a detailed response only when the user requested trip planning.

FORMATTING:

For a weather-only request:
- Location
- Current weather details
- Brief practical note

For a flight-only request:
- Route
- Available flight information

For a hotel-only request:
- Destination
- Hotel recommendations

For a complete trip-planning request:
- Trip Overview
- Flights
- Stay
- Weather
- Budget
- Itinerary
- Travel Notes

Only include sections for information that is relevant and available.

Return only the final user-facing response.
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "final_response": response.content
    }