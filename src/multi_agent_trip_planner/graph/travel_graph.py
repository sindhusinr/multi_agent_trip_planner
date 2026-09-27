from langgraph.graph import StateGraph, START, END
import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from langgraph.checkpoint.postgres import PostgresSaver

from multi_agent_trip_planner.graph.state import TravelState
from multi_agent_trip_planner.graph.routing import route_after_guardrail, route_from_supervisor, route_after
from multi_agent_trip_planner.agents.guardrail_agent import guardrail_agent
from multi_agent_trip_planner.agents.supervisor_agent import supervisor_agent
from multi_agent_trip_planner.agents.flight_agent import flight_agent
from multi_agent_trip_planner.agents.hotel_agent import hotel_agent
from multi_agent_trip_planner.agents.weather_agent import weather_agent
from multi_agent_trip_planner.agents.budget_agent import budget_agent
from multi_agent_trip_planner.agents.itinerary_agent import itinerary_agent
from multi_agent_trip_planner.agents.final_response_agent import final_response_agent

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Persistent PostgreSQL connection used by LangGraph to save thread state/checkpoints.
_conn = psycopg.connect(DATABASE_URL, autocommit=True, row_factory=dict_row)
checkpointer = PostgresSaver(_conn)
checkpointer.setup()

# StateGraph defines the multi-agent workflow using the shared TravelState.
graph = StateGraph(TravelState)

# Each node represents one responsibility in the travel planning workflow.
graph.add_node("guardrail", guardrail_agent)
graph.add_node("supervisor", supervisor_agent)
graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("weather_agent", weather_agent)
graph.add_node("budget_agent", budget_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_response_agent", final_response_agent)

# Every request first passes through the guardrail before agent execution.
graph.add_edge(START, "guardrail")

# Block invalid requests; valid travel requests continue to the supervisor.
graph.add_conditional_edges("guardrail", route_after_guardrail, {
    "supervisor": "supervisor",
    END: END
})

# Supervisor dynamically selects the first required specialist agent.
graph.add_conditional_edges("supervisor", route_from_supervisor, {
    "flight_agent": "flight_agent",
    "hotel_agent": "hotel_agent",
    "weather_agent": "weather_agent",
    "budget_agent": "budget_agent",
    "itinerary_agent": "itinerary_agent",
    "final_response_agent": "final_response_agent"
})

# After each specialist finishes, routing finds the next selected agent.
graph.add_conditional_edges("flight_agent", route_after("flight_agent"), {
    "hotel_agent": "hotel_agent",
    "weather_agent": "weather_agent",
    "budget_agent": "budget_agent",
    "itinerary_agent": "itinerary_agent",
    "final_response_agent": "final_response_agent"
})

graph.add_conditional_edges("hotel_agent", route_after("hotel_agent"), {
    "weather_agent": "weather_agent",
    "budget_agent": "budget_agent",
    "itinerary_agent": "itinerary_agent",
    "final_response_agent": "final_response_agent"
})

graph.add_conditional_edges("weather_agent", route_after("weather_agent"), {
    "budget_agent": "budget_agent",
    "itinerary_agent": "itinerary_agent",
    "final_response_agent": "final_response_agent"
})

graph.add_conditional_edges("budget_agent", route_after("budget_agent"), {
    "itinerary_agent": "itinerary_agent",
    "final_response_agent": "final_response_agent"
})

# Itinerary is already the last specialist, so send it directly for final synthesis.
graph.add_edge("itinerary_agent", "final_response_agent")

# Only the synthesized final response completes the successful workflow.
graph.add_edge("final_response_agent", END)

# Compile with PostgreSQL checkpointing for persistent thread-level state.
travel_graph = graph.compile(checkpointer=checkpointer)