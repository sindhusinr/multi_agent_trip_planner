from multi_agent_trip_planner.memory.long_term import (
    add_user_memory,
    search_user_memories
)

user_id = "test_user"

add_user_memory(
    "I prefer economy flights and budget hotels.",
    user_id
)

results = search_user_memories(
    "What are my travel preferences?",
    user_id
)

print(results)