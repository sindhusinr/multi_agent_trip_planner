from langgraph.graph import StateGraph, START, END

from multi_agent_trip_planner.graph.state import TravelState
from multi_agent_trip_planner.graph.routing import (
    route_from_supervisor,
    route_after
)

from multi_agent_trip_planner.agents.supervisor_agent import supervisor_agent
from multi_agent_trip_planner.agents.flight_agent import flight_agent
from multi_agent_trip_planner.agents.hotel_agent import hotel_agent
from multi_agent_trip_planner.agents.weather_agent import weather_agent
from multi_agent_trip_planner.agents.budget_agent import budget_agent
from multi_agent_trip_planner.agents.itinerary_agent import itinerary_agent

graph = StateGraph(TravelState)

graph.add_node("supervisor", supervisor_agent)
graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("weather_agent", weather_agent)
graph.add_node("budget_agent", budget_agent)
graph.add_node("itinerary_agent", itinerary_agent)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges(
    "supervisor",
    route_from_supervisor
)
graph.add_conditional_edges(
    "flight_agent",
    route_after("flight_agent")
)
graph.add_conditional_edges(
    "hotel_agent",
    route_after("hotel_agent")
)
graph.add_conditional_edges(
    "weather_agent",
    route_after("weather_agent")
)
graph.add_conditional_edges(
    "budget_agent",
    route_after("budget_agent")
)
graph.add_edge("itinerary_agent", END)

travel_graph = graph.compile()