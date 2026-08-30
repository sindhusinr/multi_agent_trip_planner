import uuid
import streamlit as st
from multi_agent_trip_planner.graph.travel_graph import travel_graph

st.set_page_config(page_title="AI Travel Assistant", page_icon="✈️", layout="wide")
st.title("✈️ AI Travel Assistant")
st.caption("Flights • Hotels • Weather • Budgets • Itineraries")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "trip_details" not in st.session_state:
    st.session_state.trip_details = {}
if "selected_agents" not in st.session_state:
    st.session_state.selected_agents = []
if "last_result" not in st.session_state:
    st.session_state.last_result = {}
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "guardrail_allowed" not in st.session_state:
    st.session_state.guardrail_allowed = None
if "guardrail_reason" not in st.session_state:
    st.session_state.guardrail_reason = ""

with st.sidebar:
    st.title("🧳 Trip Planner")

    if st.button("➕ New Trip", use_container_width=True):
        st.session_state.messages = []
        st.session_state.trip_details = {}
        st.session_state.selected_agents = []
        st.session_state.last_result = {}
        st.session_state.guardrail_allowed = None
        st.session_state.guardrail_reason = ""
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.divider()

    with st.expander("⚙️ Developer Details", expanded=False):
        st.subheader("Guardrail")
        if st.session_state.guardrail_allowed is None:
            st.write("Not evaluated yet.")
        else:
            st.json({
                "allowed": st.session_state.guardrail_allowed,
                "reason": st.session_state.guardrail_reason
            })

        st.subheader("Selected Agents")
        st.json(st.session_state.selected_agents)

        st.subheader("Supervisor Reasoning")
        st.write(st.session_state.last_result.get("supervisor_reasoning", "N/A"))

        st.subheader("Thread ID")
        st.code(st.session_state.thread_id)

        st.subheader("Trip Details")
        st.json(st.session_state.trip_details)

        st.subheader("Raw Result")
        st.json(st.session_state.last_result)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input(
    "Ask me about flights, hotels, weather or trip planning..."
)

if user_query:
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        with st.chat_message("assistant"):
            response_parts = []
            final_result = {}

            status = st.empty()

            for event in travel_graph.stream(
                {"user_query": user_query},
                config={
                    "configurable": {
                        "thread_id": st.session_state.thread_id
                    }
                },
                stream_mode="updates"
            ):
                print("\n===== STREAM EVENT =====")
                print(event)
                print("========================\n")

                for node_name, node_result in event.items():

                    if not isinstance(node_result, dict):
                        continue

                    final_result.update(node_result)

                    if node_name == "guardrail":
                        allowed = node_result.get("allowed")
                        reason = node_result.get("guardrail_reason", "")

                        st.session_state.guardrail_allowed = allowed
                        st.session_state.guardrail_reason = reason

                        if allowed is False:
                            response_parts.append(reason)
                            st.markdown(reason)

                            st.session_state.last_result = final_result
                            st.session_state.trip_details = {}
                            st.session_state.selected_agents = []

                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": reason
                            })

                            status.empty()
                            st.rerun()

                        status.write("🔎 Guardrail passed...")

                    elif node_name == "supervisor":
                        st.session_state.selected_agents = node_result.get(
                            "selected_agents",
                            []
                        )
                        st.session_state.last_result.update(node_result)
                        status.write("🧠 Planning your trip...")

                    elif node_name == "flight_agent":
                        result = node_result.get("flight_results", "")
                        if result:
                            text = f"### ✈️ Flight Information\n\n{result}"
                            response_parts.append(text)
                            st.markdown(text)
                        status.write("✈️ Flight information received...")

                    elif node_name == "hotel_agent":
                        result = node_result.get("hotel_results", "")
                        if result:
                            text = f"### 🏨 Hotel Recommendations\n\n{result}"
                            response_parts.append(text)
                            st.markdown(text)
                        status.write("🏨 Hotel information received...")

                    elif node_name == "weather_agent":
                        result = node_result.get("weather_results", "")
                        if result:
                            text = f"### 🌦 Weather\n\n{result}"
                            response_parts.append(text)
                            st.markdown(text)
                        status.write("🌦 Weather information received...")

                    elif node_name == "budget_agent":
                        result = node_result.get("budget_results", "")
                        if result:
                            text = f"### 💰 Budget Analysis\n\n{result}"
                            response_parts.append(text)
                            st.markdown(text)
                        status.write("💰 Budget analysis received...")

                    elif node_name == "itinerary_agent":
                        result = node_result.get("itinerary", "")
                        if result:
                            text = f"### 🗺 Travel Plan\n\n{result}"
                            response_parts.append(text)
                            st.markdown(text)
                        status.write("🗺 Travel plan completed...")

            status.empty()

            st.session_state.last_result = final_result
            st.session_state.trip_details = final_result.get(
                "trip_details",
                {}
            )

            st.session_state.selected_agents = final_result.get(
                "selected_agents",
                st.session_state.selected_agents
            )

            if not response_parts:
                response_parts.append(
                    "The selected agents returned no response."
                )
                st.markdown(response_parts[0])

            assistant_message = "\n\n".join(response_parts)

            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message
            })

            st.rerun()

    except Exception as e:
        error_message = f"❌ Error: {str(e)}"
        st.error(error_message)

        st.session_state.messages.append({
            "role": "assistant",
            "content": error_message
        })