import streamlit as st
from dq_core.anomaly_engine import scan_for_anomalies


def render():
    st.header("📊 Anomaly Scan")

    # Ensure data exists
    df = st.session_state.get("raw_data")
    if df is None or df.empty:
        st.warning("⚠️ Please ingest data first (via Ingestion tab).")
        return

    st.markdown("Use this tool to detect unusual patterns, outliers, or statistical anomalies before business impact.")

    if st.button("🔍 Run Anomaly Scan"):
        with st.spinner("Scanning for anomalies..."):
            anomalies = scan_for_anomalies(df)
            st.session_state["anomaly_results"] = anomalies  # Store results in session state

        if anomalies:
            st.error(f"❗ {len(anomalies)} potential anomalies detected:")
            for item in anomalies:
                st.markdown(
                    f"""
                    <div style="padding: 6px; border-left: 5px solid orange; margin-bottom: 6px;">
                    <strong>{item['column']}</strong><br>
                    {item['issue']}<br>
                    Mean: {item['mean']}, Std Dev: {item['std_dev']}<br>
                    Bounds: {item['bounds'][0]} to {item['bounds'][1]}<br>
                    Severity: **{item['severity'].capitalize()}**
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.session_state["anomaly_results"] = []
            st.success("✅ No anomalies found.")
    else:
        # Show last results if present
        if "anomaly_results" in st.session_state and st.session_state["anomaly_results"]:
            st.warning("⚠️ Previous anomaly scan results:")
            for item in st.session_state["anomaly_results"]:
                st.markdown(f"- **{item['column']}**: {item['issue']}")
        else:
            st.info("Click the button above to run a basic anomaly scan.")
