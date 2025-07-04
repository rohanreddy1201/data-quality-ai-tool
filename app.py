import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (API keys, etc.)
load_dotenv()

# Streamlit page config
st.set_page_config(
    page_title="DQ Tool - Data Quality Automation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for tabs and overall look
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #e9ecef;
        border-radius: 6px;
        padding: 0.2rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: black !important;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: black !important;
        border-radius: 6px 6px 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App header
st.title("🔍 Data Quality Automation Tool")
st.subheader("AI-powered data validation & monitoring.")

# Import your page modules
from dq_pages import (
    page_ingestion,
    page_checks,
    page_anomalies,
    page_incidents,
    page_contract,
    chatbot
)

# Create tabs for navigation
tabs = st.tabs([
    "📥 Ingestion",
    "✅ Checks",
    "📊 Anomalies",
    "🚨 Incidents",
    "📄 Contract",
    "🤖 Chatbot"
])

# Render content for each tab
with tabs[0]:
    page_ingestion.render()

with tabs[1]:
    page_checks.render()

with tabs[2]:
    page_anomalies.render()

with tabs[3]:
    page_incidents.render()

with tabs[4]:
    page_contract.render()

with tabs[5]:
    chatbot.render()
