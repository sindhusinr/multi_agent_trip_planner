from langgraph.graph import StateGraph, START, END

from multi_agent_trip_planner.graph.state import TravelState
from multi_agent_trip_planner.agents.flight_agent import flight_agent
from multi_agent_trip_planner.agents.hotel_agent import hotel_agent
from multi_agent_trip_planner.agents.itinerary_agent import itinerary_agent


graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", END)

travel_graph = graph.compile()