import os

from dotenv import load_dotenv
from mem0 import Memory

load_dotenv()


def create_memory():
    """
    Create Mem0 long-term memory.
    """

    config = {
        "llm": {
            "provider": "groq",
            "config": {
                "model": os.getenv("MEMORY_LLM_MODEL"),
                "api_key": os.getenv("GROQ_API_KEY"),
                "temperature": 0.1
            }
        },

        "embedder": {
            "provider": "huggingface",
            "config": {
                "model": "multi-qa-MiniLM-L6-cos-v1",
                "embedding_dims": 384
            }
        },

        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "travel_memories",
                "embedding_model_dims": 384,
                "path": "./qdrant_data"
            }
        }
    }

    return Memory.from_config(config)


memory = create_memory()


def get_user_memories(user_id: str) -> list:
    """
    Retrieve all long-term memories for a user.
    """

    result = memory.get_all(
        user_id=user_id
    )

    return result.get("results", [])


def search_user_memories(
    query: str,
    user_id: str
) -> list:
    """
    Search memories relevant to the current request.
    """

    result = memory.search(
        query=query,
        filters={
            "user_id": user_id
        }
    )

    return result.get("results", [])


def add_user_memory(
    text: str,
    user_id: str
):
    """
    Store an already validated long-term memory.
    """

    return memory.add(
        text,
        user_id=user_id,
        infer=False
    )