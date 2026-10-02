import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from multi_agent_trip_planner.memory.long_term import (
    add_user_memory,
    search_user_memories
)

load_dotenv()


class MemoryExtraction(BaseModel):
    memories: list[str] = Field(default_factory=list)


llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY")
)

memory_llm = llm.with_structured_output(
    MemoryExtraction
)


def memory_retrieval_agent(state: dict) -> dict:
    """
    Retrieve relevant long-term user preferences.
    """

    print("\n>>> MEMORY RETRIEVAL")

    user_id = state.get("user_id", "")
    user_query = state.get("user_query", "")

    if not user_id or not user_query:
        return {
            "user_memories": []
        }

    results = search_user_memories(
        user_query,
        user_id
    )

    memories = [
        item.get("memory", "")
        for item in results
        if item.get("memory")
    ]

    print("Retrieved memories:", memories)

    return {
        "user_memories": memories[:5]
    }


def memory_extraction_agent(state: dict) -> dict:
    """
    Store only stable travel preferences.
    """

    print("\n>>> MEMORY EXTRACTION")

    user_id = state.get("user_id", "")
    user_query = state.get("user_query", "")

    if not user_id or not user_query:
        return {}

    prompt = f"""
Extract stable long-term travel preferences explicitly
stated by the user.

User message:
{user_query}

Store only reusable preferences that may be useful
for future trips.

Examples worth remembering:
- preferred cabin class
- preferred hotel type
- preferred travel style
- food preferences
- activity preferences
- transport preferences

Do NOT store temporary trip information:
- destination for this trip
- travel dates
- trip duration
- budget for this trip
- current flight or hotel results
- temporary requests

Do not infer preferences that the user did not state.

If there is nothing worth remembering,
return an empty memories list.

Each memory must be a short standalone statement.
"""

    try:
        result = memory_llm.invoke(
            [HumanMessage(content=prompt)]
        )

        print(
            "Extracted memories:",
            result.memories
        )

        for memory_text in result.memories:
            add_user_memory(
                memory_text,
                user_id
            )

    except Exception as e:
        # Memory is non-critical; keep the main workflow running.
        print(
            "Memory extraction skipped:",
            str(e)
        )

    return {}