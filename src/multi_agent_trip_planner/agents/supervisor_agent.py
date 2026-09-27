import json
import os
from typing import List, Literal

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel

load_dotenv()


# Structured trip information extracted from the user's request.
class TripDetails(BaseModel):
    origin: str = ""
    destination: str = ""
    primary_city: str = ""

    departure_date: str = ""
    return_date: str = ""
    duration: str = ""

    # None/empty means the user did not explicitly update these fields.
    adults: int | None = None
    cabin_class: str = ""

    budget: str = ""
    travel_style: str = ""
    additional_city: str = ""


# Structured supervisor response used for reliable routing.
class SupervisorOutput(BaseModel):
    action: Literal["create_trip", "modify_trip"]
    selected_agents: List[str]
    reasoning: str = ""
    trip_details: TripDetails


llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY")
)

# Prevents raw/malformed JSON from reaching graph routing logic.
structured_llm = llm.with_structured_output(SupervisorOutput)

FALLBACK_AGENTS = [
    "hotel_agent",
    "weather_agent",
    "itinerary_agent"
]


def supervisor_agent(state: dict) -> dict:
    """
    Extract trip details and select the agents required for the request.
    """

    # Existing values are preserved across conversation turns.
    current_trip = state.get("trip_details", {})

    prompt = f"""
You are the supervisor of a multi-agent travel planning system.

AVAILABLE AGENTS:

- flight_agent
- hotel_agent
- weather_agent
- budget_agent
- itinerary_agent

CURRENT TRIP DETAILS:

{json.dumps(current_trip, indent=2)}

USER QUERY:

{state["user_query"]}

TASKS:

1. Determine the action:
   - create_trip
   - modify_trip

2. Extract trip details explicitly provided by the user.

3. Preserve the meaning of the existing trip.

4. Select only the agents required for the user's current request.

TRIP DETAILS:

Extract when available:

- origin
- destination
- primary_city
- departure_date
- return_date
- duration
- adults
- cabin_class
- budget
- travel_style
- additional_city

TRIP UPDATE RULES:

- Return all trip_details fields.
- Do not invent missing trip information.
- Values not provided in the current request may remain empty.
- Existing values are preserved by the application after extraction.
- Never leave primary_city empty when destination is known.
- If destination is a city, normally use it as primary_city.

LOCATION RULES:

- "from X" means origin = X.
- "to X" means destination = X.
- If only one location is mentioned and no origin is specified,
  normally treat it as destination.

Examples:

"Plan a trip to Chennai"
origin = ""
destination = "Chennai"
primary_city = "Chennai"

"Plan a trip from Chennai to Singapore"
origin = "Chennai"
destination = "Singapore"
primary_city = "Singapore"

"Flights from Bangalore to Chennai"
origin = "Bangalore"
destination = "Chennai"
primary_city = "Chennai"

COUNTRY TO PRIMARY CITY EXAMPLES:

Japan -> Tokyo
France -> Paris
Thailand -> Bangkok
Singapore -> Singapore
UAE -> Dubai
Italy -> Rome
Germany -> Berlin

DATE RULES:

- Extract departure_date when a travel start/departure date is provided.
- Extract return_date when an end/return date is provided.
- Extract duration when trip length is provided.
- Store exact dates in YYYY-MM-DD format.
- Do not invent departure_date or return_date.
- If a date is required but missing, leave it empty.

PASSENGER RULES:

- Extract adults only when the user specifies the number of adult travelers.
- Otherwise leave adults unset.
- Do not guess the number of travelers.

CABIN CLASS RULES:

Recognize values such as:
- economy
- premium economy
- business
- first

Only extract cabin_class when the user provides it.
Otherwise leave it empty.

FLIGHT AGENT RULES:

Select flight_agent when:
- the user explicitly asks for flights, OR
- flight search is required for a full trip-planning request.

The flight agent may be selected even when required flight information
such as departure_date is missing.

Do not invent missing flight information.

A separate validation/HITL step will handle missing required fields
before the flight search executes.

AGENT SELECTION RULES:

Weather-only request:
["weather_agent"]

Hotel-only request:
["hotel_agent"]

Flight-only request:
["flight_agent"]

Budget-only or budget-change request:
["budget_agent"]

Itinerary-only or itinerary-change request:
["itinerary_agent"]

Full trip-planning request:
Select:
- flight_agent when transportation from an origin is relevant
- hotel_agent
- weather_agent
- itinerary_agent

Also select budget_agent when the user provides a budget or explicitly
asks for budget/cost analysis.

IMPORTANT:

- Select agents based on the user's intent.
- Do not select unnecessary agents.
- Missing required fields must not prevent selection of an agent
  that the user actually requested.
- Missing information will be handled by the validation/HITL layer.
"""

    try:
        result = structured_llm.invoke(
            [HumanMessage(content=prompt)]
        )

        print("\n>>> SUPERVISOR")
        print(result.model_dump())

        trip_details = result.trip_details.model_dump()

        # Preserve previously known values unless this turn updates them.
        merged_trip = current_trip.copy()

        for key, value in trip_details.items():
            if value not in ("", None):
                merged_trip[key] = value

        # Application defaults, not LLM extraction defaults.
        merged_trip.setdefault("adults", 1)
        merged_trip.setdefault("cabin_class", "economy")

        # Ensure all expected fields exist in persisted trip state.
        defaults = {
            "origin": "",
            "destination": "",
            "primary_city": "",
            "departure_date": "",
            "return_date": "",
            "duration": "",
            "budget": "",
            "travel_style": "",
            "additional_city": ""
        }

        for key, value in defaults.items():
            merged_trip.setdefault(key, value)

        return {
            "action": result.action,
            "selected_agents": result.selected_agents,
            "supervisor_reasoning": result.reasoning,
            "trip_details": merged_trip
        }

    except Exception as e:
        print("\n>>> SUPERVISOR FALLBACK")
        print(e)

        return {
            "action": "create_trip",
            "selected_agents": FALLBACK_AGENTS,
            "supervisor_reasoning": f"Fallback routing used: {e}",
            "trip_details": current_trip
        }