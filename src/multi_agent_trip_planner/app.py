from multi_agent_trip_planner.graph.travel_graph import travel_graph

result = travel_graph.invoke(
    {
        "user_query": "Plan a 7 day Japan trip from Chennai",
        "messages": [],
        "llm_calls": 0
    }
)

print(result["itinerary"])