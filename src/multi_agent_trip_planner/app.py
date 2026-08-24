from multi_agent_trip_planner.graph.travel_graph import travel_graph
#to write
mermaid = travel_graph.get_graph().draw_mermaid()
with open("graph.mmd", "w") as f:
    f.write(mermaid)
user_query = input("Question: ")
state = {
    "user_query": user_query,
    "messages": []
}

result = travel_graph.invoke(state)

print("\n==== SELECTED AGENTS ====")
print(result.get("selected_agents"))

if result.get("itinerary"):
    print("\n==== ITINERARY ====")
    print(result["itinerary"])

elif result.get("budget_results"):
    print("\n==== BUDGET ====")
    print(result["budget_results"])

elif result.get("weather_results"):
    print("\n==== WEATHER ====")
    print(result["weather_results"])

elif result.get("hotel_results"):
    print("\n==== HOTEL ====")
    print(result["hotel_results"])

elif result.get("flight_results"):
    print("\n==== FLIGHT ====")
    print(result["flight_results"])