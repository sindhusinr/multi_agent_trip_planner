from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from multi_agent_trip_planner.graph.state import TravelState
from multi_agent_trip_planner.graph.routing import (
    route_after_guardrail,
    route_from_supervisor,
    route_after
)

from multi_agent_trip_planner.agents.guardrail_agent import guardrail_agent
from multi_agent_trip_planner.agents.supervisor_agent import supervisor_agent
from multi_agent_trip_planner.agents.trip_validator import trip_validator

from multi_agent_trip_planner.agents.flight_agent import flight_agent
from multi_agent_trip_planner.agents.hotel_agent import hotel_agent
from multi_agent_trip_planner.agents.weather_agent import weather_agent
from multi_agent_trip_planner.agents.budget_agent import budget_agent
from multi_agent_trip_planner.agents.itinerary_agent import itinerary_agent
from multi_agent_trip_planner.agents.final_response_agent import (
    final_response_agent
)


def build_graph(checkpointer: PostgresSaver):
    """
    Build the multi-agent travel planning graph.
    """

    builder = StateGraph(TravelState)

    # Core orchestration nodes.
    builder.add_node("guardrail", guardrail_agent)
    builder.add_node("supervisor", supervisor_agent)
    builder.add_node("trip_validator", trip_validator)

    # Specialist agents.
    builder.add_node("flight_agent", flight_agent)
    builder.add_node("hotel_agent", hotel_agent)
    builder.add_node("weather_agent", weather_agent)
    builder.add_node("budget_agent", budget_agent)
    builder.add_node("itinerary_agent", itinerary_agent)

    # Final synthesis layer.
    builder.add_node(
        "final_response_agent",
        final_response_agent
    )

    # Start with travel-domain validation.
    builder.add_edge(START, "guardrail")

    builder.add_conditional_edges(
        "guardrail",
        route_after_guardrail,
        {
            "supervisor": "supervisor",
            END: END
        }
    )

    # Supervisor extracts trip details and selects agents.
    # Validator handles missing required information before execution.
    builder.add_edge(
        "supervisor",
        "trip_validator"
    )

    builder.add_conditional_edges(
        "trip_validator",
        route_from_supervisor,
        {
            "flight_agent": "flight_agent",
            "hotel_agent": "hotel_agent",
            "weather_agent": "weather_agent",
            "budget_agent": "budget_agent",
            "itinerary_agent": "itinerary_agent",
            "final_response_agent": "final_response_agent"
        }
    )

    # Continue through selected specialist agents in execution order.
    builder.add_conditional_edges(
        "flight_agent",
        route_after("flight_agent"),
        {
            "hotel_agent": "hotel_agent",
            "weather_agent": "weather_agent",
            "budget_agent": "budget_agent",
            "itinerary_agent": "itinerary_agent",
            "final_response_agent": "final_response_agent"
        }
    )

    builder.add_conditional_edges(
        "hotel_agent",
        route_after("hotel_agent"),
        {
            "weather_agent": "weather_agent",
            "budget_agent": "budget_agent",
            "itinerary_agent": "itinerary_agent",
            "final_response_agent": "final_response_agent"
        }
    )

    builder.add_conditional_edges(
        "weather_agent",
        route_after("weather_agent"),
        {
            "budget_agent": "budget_agent",
            "itinerary_agent": "itinerary_agent",
            "final_response_agent": "final_response_agent"
        }
    )

    builder.add_conditional_edges(
        "budget_agent",
        route_after("budget_agent"),
        {
            "itinerary_agent": "itinerary_agent",
            "final_response_agent": "final_response_agent"
        }
    )

    # Itinerary is the final domain agent before response synthesis.
    builder.add_edge(
        "itinerary_agent",
        "final_response_agent"
    )

    builder.add_edge(
        "final_response_agent",
        END
    )

    return builder.compile(
        checkpointer=checkpointer
    )