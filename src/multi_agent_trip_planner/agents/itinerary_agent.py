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

    flight_results = state.get(
        "flight_results",
        ""
    )

    hotel_results = state.get(
        "hotel_results",
        ""
    )

    weather_results = state.get(
        "weather_results",
        ""
    )

    duration = trip_details.get(
        "duration",
        ""
    )

    # =========================================================================
    # WHY:
    # We do not want the itinerary model to guess
    # airlines, airports, routes or flight durations
    # when Flight Agent failed.
    # =========================================================================
    flight_available = True

    if (
        not flight_results
        or "No flights found" in flight_results
        or "Unable to find airport code" in flight_results
        or "Flight API error" in flight_results
    ):
        flight_available = False

    prompt = f"""
Create a travel itinerary.

Trip Details:

{trip_details}

User Request:

{state["user_query"]}

Flight Available:

{flight_available}

Duration Value:

{duration}

Flight Information:

{flight_results}

Hotel Information:

{hotel_results}

Weather Information:

{weather_results}

Transportation Rules:

- Do not assume flights.
- Do not invent origin cities.
- Do not invent destination cities.
- Use only information explicitly provided.
- If destination is a country,
  use primary_city.

Flight Rules:

IF Flight Available = False

THEN:

- State:
  "Flight information is currently unavailable."

- Do NOT mention:
  - airlines
  - airports
  - airport transfers
  - flight durations
  - layovers
  - ticket prices
  - suggested flight routes

- Do NOT mention:
  Narita
  Haneda
  Singapore Airlines
  Emirates
  Air India
  ANA
  JAL

- Do NOT create transportation
  recommendations related to flights.

IF Flight Available = True

THEN:

- Use only information contained
  in Flight Information.
- Do not invent additional
  flight details.

Duration Rules:

IF Duration Value is empty

THEN:

- Do NOT create:
  Day 1
  Day 2
  Day 3
  Day 4
  Day 5

- Do NOT assume:
  3 days
  5 days
  7 days
  1 week

- Create:

  Suggested Activities
  Morning Ideas
  Afternoon Ideas
  Evening Ideas

- Clearly state:

  "Trip duration was not provided."

IF Duration Value is present

THEN:

- Create a day-by-day itinerary
  matching the provided duration.

Hotel Rules:

- Use hotels only from
  Hotel Information.
- Never invent hotels.
- Never invent hotel pricing.

Weather Rules:

- Use weather only from
  Weather Information.
- Never invent forecasts.

Generate:

1. Trip Summary
2. Transportation Recommendations
3. Hotel Recommendation
4. Suggested Activities
5. Travel Tips

Important:

- Never invent transportation.
- Never invent routes.
- Never invent airlines.
- Never invent airports.
- Never invent schedules.
- Never invent prices.
- Never invent weather.
- Never invent hotels.

- If information is unavailable,
  explicitly say it is unavailable.

Keep the response realistic,
practical and easy to read.
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