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
    Create an activity itinerary for the destination.
    """

    print("\n>>> ITINERARY AGENT")

    trip_details = state.get(
        "trip_details",
        {}
    )

    destination = trip_details.get(
        "primary_city"
    ) or trip_details.get(
        "destination",
        ""
    )

    duration = trip_details.get(
        "duration",
        ""
    )

    travel_style = trip_details.get(
        "travel_style",
        ""
    )

    prompt = f"""
Create a travel activity itinerary.

Destination:
{destination}

Duration:
{duration}

Travel Style:
{travel_style}

User Request:
{state.get("user_query", "")}

Your responsibility is ONLY itinerary planning.

Rules:

- Focus only on activities, attractions,
  sightseeing and experiences.
- Do not recommend flights.
- Do not recommend airlines.
- Do not provide flight schedules or prices.
- Do not recommend hotels.
- Do not provide hotel prices.
- Do not calculate trip budget.
- Do not provide weather forecasts.
- Do not invent bookings or reservations.

If Duration is provided:

- Create a day-by-day itinerary.
- Match the itinerary to the provided duration.
- Organize activities into morning,
  afternoon and evening.
- Keep nearby activities together when possible.
- Do not generate exact opening hours,
  event schedules or reservation times.
- Avoid exact clock-time schedules unless
  explicitly provided in the input.
- Treat activities as suggestions, not confirmed bookings.

If Duration is not provided:

- Do not assume a number of days.
- Do not create Day 1, Day 2, etc.
- Provide a concise list of suggested
  activities for the destination.

Keep the itinerary practical,
concise and easy to read.
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