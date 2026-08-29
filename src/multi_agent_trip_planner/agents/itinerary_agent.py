import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY")
)


def itinerary_agent(state: dict) -> dict:
    """
    Creates a complete itinerary using
    available trip details and agent outputs.
    """

    trip_details = state.get(
        "trip_details",
        {}
    )

    prompt = f"""
Create a travel itinerary.

Trip Details:

{trip_details}

Transportation Rules:

- Do not assume flights.
- Do not invent an origin city.
- Do not invent a destination.
- Only include flight information when
  flight_results are available.
- If origin is empty, do not mention
  departure airports or flights.
- If destination is a city, build the
  itinerary around that city.
- If destination is a country, use
  primary_city for recommendations.

User Request:

{state["user_query"]}

Flight Information:

{state.get("flight_results", "")}

Hotel Information:

{state.get("hotel_results", "")}

Weather Information:

{state.get("weather_results", "")}

Generate:

1. Trip Summary
2. Transportation Recommendations
3. Hotel Recommendation
4. Suggested Day-by-Day Plan
5. Travel Tips

Important:

- Never create fictional flight routes.
- Never create departure cities.
- Never assume the traveler starts
  from Mumbai, Delhi, Chennai,
  Bangalore, or any other city.
- If flight information is unavailable,
  omit the Flight Recommendation section.
- Keep recommendations aligned with
  the provided destination only.

Keep the response practical and easy to read.
"""

    response = llm.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )

    return {
        "itinerary": response.content
    }