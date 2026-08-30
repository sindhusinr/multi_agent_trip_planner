import json
import os
from typing import List, Literal

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel


# ============================================================================
# SUPERVISOR OUTPUT SCHEMA
# ============================================================================
# WHY:
# Previously the supervisor returned raw JSON text.
#
# Problems:
# - Invalid JSON
# - Extra markdown
# - Missing fields
# - json.loads() failures
#
# Structured output validates responses before
# they reach the application logic.
# ============================================================================

class TripDetails(BaseModel):
    origin: str = ""
    destination: str = ""
    primary_city: str = ""
    duration: str = ""
    budget: str = ""
    travel_style: str = ""
    additional_city: str = ""


class SupervisorOutput(BaseModel):
    action: Literal[
        "create_trip",
        "modify_trip"
    ]
    selected_agents: List[str]
    reasoning: str = ""
    trip_details: TripDetails


load_dotenv()

llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY")
)

# WHY:
# LangChain converts the model response
# directly into a validated Pydantic object.
#
# Benefits:
# - No json.loads()
# - No malformed JSON
# - Type-safe access
# - More reliable routing decisions
structured_llm = llm.with_structured_output(
    SupervisorOutput
)

FALLBACK_AGENTS = [
    "hotel_agent",
    "weather_agent",
    "itinerary_agent"
]


def supervisor_agent(state: dict) -> dict:
    """
    Main orchestration agent.

    Responsibilities:
    - Detect new trips
    - Detect trip modifications
    - Extract trip details
    - Select required agents
    """

    # Previously stored trip details
    current_trip = state.get(
        "trip_details",
        {}
    )

    prompt = f"""
You are the supervisor of a multi-agent travel planning system.

Available Agents:

- flight_agent
- hotel_agent
- weather_agent
- budget_agent
- itinerary_agent

Current Trip Details:

{json.dumps(current_trip, indent=2)}

Tasks:

1. Determine action:
   - create_trip
   - modify_trip

2. Extract trip details.

3. Select only the required agents.

Trip Update Rules:

- Preserve existing values.
- Update only fields explicitly mentioned.
- Always return trip_details.

Flight Rules:

DO NOT select flight_agent unless BOTH
origin and destination are known.

Examples:

Origin: Chennai
Destination: Empty

Selected Agents:
[]

Origin: Empty
Destination: Singapore

Selected Agents:
[
    "hotel_agent",
    "weather_agent",
    "itinerary_agent"
]

Origin: Chennai
Destination: Singapore

Selected Agents:
[
    "flight_agent",
    "hotel_agent",
    "weather_agent",
    "itinerary_agent"
]

User:
Flights from Chennai to Singapore

Selected Agents:
[
    "flight_agent"
]

Important:

If either origin or destination is missing:

- Do not select flight_agent.
- Wait for the user to provide the
  missing location.

Agent Selection Rules:

Full Trip Planning:

- hotel_agent
- weather_agent
- itinerary_agent

Add flight_agent only if Flight Rules match.

Weather Only:

- weather_agent

Hotel Only:

- hotel_agent

Flight Only:

- flight_agent

Budget Change:

- budget_agent

Itinerary Change:

- itinerary_agent

Trip Detail Rules:

- Always return trip_details.
- Never leave primary_city empty when
  destination is known.
- If destination is a city,
  use that city as primary_city.

Location Extraction Rules:

- If the user says "from X",
  store X as origin.

- If the user says "to X",
  store X as destination.

- If only one location is mentioned
  and no origin is specified,
  treat it as destination.

Examples:

Plan a trip to Chennai

origin = ""
destination = "Chennai"
primary_city = "Chennai"

Plan a trip from Chennai

origin = "Chennai"
destination = ""

Plan a trip from Chennai to Japan

origin = "Chennai"
destination = "Japan"
primary_city = "Tokyo"

Flights from Bangalore to Chennai

origin = "Bangalore"
destination = "Chennai"
primary_city = "Chennai"

Country Mapping:

Japan -> Tokyo
France -> Paris
Thailand -> Bangkok
Singapore -> Singapore
UAE -> Dubai
Italy -> Rome
Germany -> Berlin

User Query:

{state["user_query"]}
"""

    try:

        # WHY:
        # Response is automatically validated
        # against SupervisorOutput schema.
        result = structured_llm.invoke(
            [
                HumanMessage(
                    content=prompt
                )
            ]
        )

        print("\n>>> SUPERVISOR")
        print(result.model_dump())

        # Convert Pydantic object into dict
        # for LangGraph state storage.
        trip_details = (
            result.trip_details.model_dump()
        )

        # WHY:
        # Users usually provide trip details
        # across multiple messages.
        #
        # Example:
        # "Trip to Japan"
        # "Budget 1 lakh"
        #
        # Preserve previous values if they
        # are not provided in the current turn.
        merged_trip = {
            "origin": (
                trip_details.get("origin")
                or current_trip.get(
                    "origin",
                    ""
                )
            ),
            "destination": (
                trip_details.get("destination")
                or current_trip.get(
                    "destination",
                    ""
                )
            ),
            "primary_city": (
                trip_details.get("primary_city")
                or current_trip.get(
                    "primary_city",
                    ""
                )
            ),
            "duration": (
                trip_details.get("duration")
                or current_trip.get(
                    "duration",
                    ""
                )
            ),
            "budget": (
                trip_details.get("budget")
                or current_trip.get(
                    "budget",
                    ""
                )
            ),
            "travel_style": (
                trip_details.get(
                    "travel_style"
                )
                or current_trip.get(
                    "travel_style",
                    ""
                )
            ),
            "additional_city": (
                trip_details.get(
                    "additional_city"
                )
                or current_trip.get(
                    "additional_city",
                    ""
                )
            )
        }

        return {
            "action": result.action,
            "selected_agents": result.selected_agents,
            "supervisor_reasoning": result.reasoning,
            "trip_details": merged_trip
        }

    except Exception as e:

        print(
            "\n>>> SUPERVISOR FALLBACK"
        )

        print(e)

        return {
            "action": "create_trip",
            "selected_agents":
                FALLBACK_AGENTS,
            "supervisor_reasoning": (
                f"Fallback routing used: {e}"
            ),
            "trip_details": current_trip
        }