import json
import os

from dotenv import load_dotenv
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
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
    - Detect new trip requests
    - Detect trip modifications
    - Select required agents
    - Extract structured trip details
    """

    current_trip = state.get(
        "trip_details",
        {}
    )

    prompt = f"""
You are the supervisor of a multi-agent travel planning system.

Available agents:

- flight_agent
- hotel_agent
- weather_agent
- budget_agent
- itinerary_agent

Current Trip Details:

{json.dumps(current_trip, indent=2)}

You may receive either:

1. A brand new trip request
2. A modification to an existing trip

Determine the action:

- create_trip
- modify_trip

If trip details already exist:

- Preserve existing values
- Update only fields explicitly changed
  by the user

Examples:

Current Trip:
{{
  "destination": "Japan",
  "primary_city": "Tokyo",
  "duration": "5 days",
  "budget": ""
}}

User:
Increase budget to 2 lakhs

Result:
{{
  "action": "modify_trip",
  "trip_details": {{
    "destination": "Japan",
    "primary_city": "Tokyo",
    "duration": "5 days",
    "budget": "2 lakhs"
  }}
}}

User:
Add Kyoto

Result:
{{
  "action": "modify_trip",
  "trip_details": {{
    "destination": "Japan",
    "primary_city": "Tokyo",
    "duration": "5 days",
    "budget": "",
    "additional_city": "Kyoto"
  }}
}}

Agent Selection Rules:

1. Full trip planning requests:

   - flight_agent
   - hotel_agent
   - weather_agent
   - itinerary_agent

2. Weather only:

   - weather_agent

3. Hotel only:

   - hotel_agent

4. Flight only:

   - flight_agent

5. Budget change:

   - budget_agent

6. Itinerary modifications:

   - itinerary_agent

Trip Detail Extraction Rules:

- Always return trip_details
- Never leave primary_city empty
  when destination is known

Country Mapping:

Japan -> Tokyo
France -> Paris
Thailand -> Bangkok
Singapore -> Singapore
UAE -> Dubai
Italy -> Rome
Germany -> Berlin

Return VALID JSON ONLY.

Example:

{{
    "action": "create_trip",
    "selected_agents": [
        "flight_agent",
        "hotel_agent",
        "weather_agent",
        "itinerary_agent"
    ],
    "reasoning": "Complete trip planning request.",
    "trip_details": {{
        "origin": "Chennai",
        "destination": "Japan",
        "primary_city": "Tokyo",
        "duration": "7 days",
        "budget": "",
        "travel_style": ""
    }}
}}

User Query:

{state["user_query"]}
"""

    try:

        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Return only valid JSON. "
                        "Do not use markdown."
                    )
                ),
                HumanMessage(content=prompt)
            ]
        )

        result = json.loads(
            response.content
        )

        print("\n>>> SUPERVISOR")
        print(result)

        trip_details = result.get(
            "trip_details",
            {}
        )

        return {
            "action": result.get(
                "action",
                "create_trip"
            ),
            "selected_agents": result.get(
                "selected_agents",
                []
            ),
            "supervisor_reasoning": result.get(
                "reasoning",
                ""
            ),
            "trip_details": {
                "origin": trip_details.get(
                    "origin",
                    current_trip.get(
                        "origin",
                        ""
                    )
                ),
                "destination": trip_details.get(
                    "destination",
                    current_trip.get(
                        "destination",
                        ""
                    )
                ),
                "primary_city": trip_details.get(
                    "primary_city",
                    current_trip.get(
                        "primary_city",
                        ""
                    )
                ),
                "duration": trip_details.get(
                    "duration",
                    current_trip.get(
                        "duration",
                        ""
                    )
                ),
                "budget": trip_details.get(
                    "budget",
                    current_trip.get(
                        "budget",
                        ""
                    )
                ),
                "travel_style": trip_details.get(
                    "travel_style",
                    current_trip.get(
                        "travel_style",
                        ""
                    )
                ),
                "additional_city": trip_details.get(
                    "additional_city",
                    current_trip.get(
                        "additional_city",
                        ""
                    )
                )
            }
        }

    except Exception as e:

        print("\n>>> SUPERVISOR FALLBACK")
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