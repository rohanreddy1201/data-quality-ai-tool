import streamlit as st
from dq_core.chatbot_agent import chat_with_data_context


def render():
    st.header("🤖 Data Quality Chat Assistant")

    # Ensure data exists
    df = st.session_state.get("raw_data")
    if df is None or df.empty:
        st.warning("⚠️ Please ingest data first to enable the assistant.")
        return

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Greeting
    st.chat_message("assistant").write("Hi! I'm your DQ Assistant. Ask me anything about the dataset or validation results.")

    # Render previous messages
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    # User input
    user_input = st.chat_input("Ask about data issues, columns, rules, etc...")

    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            response = chat_with_data_context(user_input, df)

        st.chat_message("assistant").write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
