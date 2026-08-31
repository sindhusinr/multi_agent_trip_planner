# Multi-Agent Trip Planner

An agentic ✈️ travel planning application built with **LangGraph** that dynamically coordinates specialized agents for flights, hotels, weather, budget analysis, and itinerary generation.

The system uses a **supervisor-based multi-agent architecture**, **guardrails**, **conditional graph routing**, **PostgreSQL-backed LangGraph persistence**, and **Tavily Remote MCP** for web-based hotel research.

A Streamlit interface provides an interactive travel assistant, while a CLI entry point is also available for testing and development.

## Overview

Planning a trip typically requires gathering information from multiple sources such as flights, accommodation, weather, budget, and activities.

Instead of sending every request to every service, this application uses a supervisor-driven workflow to determine which specialized agents are actually required for the user's request.

For example:

- A flight-only request invokes the flight agent.
- A weather request invokes the weather agent.
- A complete trip request can invoke multiple specialized agents.
- A request that requires itinerary generation uses the information collected by the preceding agents.
- Invalid or unsafe requests are stopped by the guardrail before reaching the supervisor.

The application also maintains trip information across conversational turns using **LangGraph checkpointing with PostgreSQL**.

## Key Features

- Multi-agent travel planning with LangGraph
- Supervisor-based agent selection
- Conditional agent routing
- Query guardrails
- Flight search using AviationStack
- Airport/city to IATA code resolution
- Weather information using OpenWeather
- Hotel research using Tavily Remote MCP
- Budget analysis
- LLM-generated travel itineraries
- Structured supervisor output using Pydantic
- Persistent conversation/trip state using PostgreSQL
- Streamlit chat interface
- CLI interface for development/testing
- Environment-based configuration
- Optional LangSmith tracing support

## Architecture

The application follows a supervisor-based multi-agent architecture.
<img width="1536" height="1024" alt="trip_planner" src="https://github.com/user-attachments/assets/f7a41f73-0393-472f-9180-9515eb1bf0a0" />

## 🏗️ Architecture Overview

- **Guardrail Agent** validates that user requests are travel-related.
- **Supervisor Agent** determines which specialized agents should be executed.
- **Flight Agent** retrieves flight information.
- **Hotel Agent** provides hotel recommendations.
- **Weather Agent** retrieves destination weather details.
- **Budget Agent** estimates travel expenses.
- **Itinerary Agent** generates the final travel itinerary.
- **LangGraph** orchestrates agent execution and routing.
- **PostgreSQL Checkpointer** maintains conversation state and memory.
- **Streamlit UI** provides a conversational chat interface for end users.

## How It Works

1. User submits a travel request.
2. Guardrail validates the request.
3. Supervisor extracts trip details and selects required agents.
4. Selected agents execute conditionally based on the request.
5. Results are stored in the shared LangGraph state.
6. The Itinerary Agent synthesizes the available information when required.
7. PostgreSQL checkpointing preserves trip state across conversation turns.

## Tech Stack

**Python · LangGraph · LangChain · Groq · Pydantic · PostgreSQL · MCP · Tavily · AviationStack · OpenWeather · Streamlit · uv · LangSmith**

## Observability

**LangSmith** can be enabled for tracing and monitoring LangChain/LangGraph executions.

Configure the following variables in `.env`:

```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=multi-agent-trip-planner
```
When enabled, LangSmith provides visibility into agent execution, LLM calls, and LangGraph runs.
## 🚀 Setup

### Prerequisites

Before running the application, ensure the following are installed and configured:

- Python 3.13+
- PostgreSQL
- UV Package Manager
- Required API Keys (Groq, Tavily, AviationStack, OpenWeather)

---

### Install Dependencies

Install all project dependencies using UV:

```bash
uv sync
```

### Configure Environment Variables

Create a `.env` file from the provided template and add your API keys along with the PostgreSQL connection string.

```bash
cp .env.example .env
```

Update the `.env` file with the required values:


### Run the Streamlit Application

Launch the chat-based Multi-Agent Travel Assistant UI:

```bash
uv run streamlit run src/multi_agent_trip_planner/ui/streamlit.py
```

The application will be available at:

```text
http://localhost:8501
```

### Run the CLI Application

Run the travel assistant from the command line:

```bash
uv run python src/multi_agent_trip_planner/app.py
```
