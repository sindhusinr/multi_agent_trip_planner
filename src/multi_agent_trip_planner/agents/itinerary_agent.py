import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY")
)


def itinerary_agent(state: dict) -> dict:
    """
    Combines flight and hotel information
    into a complete travel itinerary.
    """

    prompt = f"""
Create a travel itinerary.

User Request:
{state['user_query']}

Flight Information:
{state.get('flight_results', '')}

Hotel Information:
{state.get('hotel_results', '')}

Generate:

1. Trip Summary
2. Flight Recommendation
3. Hotel Recommendation
4. Suggested Day-by-Day Plan
5. Travel Tips

Keep the response practical and easy to read.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        "itinerary": response.content
    }