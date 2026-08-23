import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_destination(query: str) -> str:
    prompt = f"""
Extract the primary travel destination from the user query.

Return only the city or country name.

Query:
{query}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()