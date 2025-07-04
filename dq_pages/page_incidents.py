import streamlit as st
import pandas as pd


def render():
    st.header("🚨 Incident Tracker")

    st.markdown("This section displays a running log of failed checks, anomalies, and schema issues identified during this session.")

    # Ensure incident_log exists
    if "incident_log" not in st.session_state:
        st.session_state["incident_log"] = []

    incident_log = st.session_state["incident_log"]

    if not incident_log:
        st.success("✅ No incidents logged yet in this session.")
        return

    st.markdown(f"### 🔎 {len(incident_log)} Incident(s) Logged")

    for i, entry in enumerate(reversed(incident_log), start=1):
        st.error(
            f"**#{i}:** `{entry.get('type', 'Unknown')}` in **{entry.get('column', 'N/A')}** → {entry.get('message', 'No details')}"
        )

    st.markdown("---")

    if st.button("🧹 Clear Incident Log"):
        st.session_state["incident_log"] = []
        st.success("✅ Incident log cleared.")
