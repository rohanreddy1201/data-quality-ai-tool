import streamlit as st
from collections import defaultdict
from dq_core.rule_engine import run_basic_checks


def render():
    st.header("✅ Run Checks")

    if "raw_data" not in st.session_state:
        st.warning("⚠️ Please ingest data first (via Ingestion tab).")
        return

    df = st.session_state["raw_data"]
    contract_rules = st.session_state.get("contract_rules", {})
    dataset_rules = st.session_state.get("dataset_rules", {})

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    if st.button("▶️ Run Validation"):
        with st.spinner("Running validation checks..."):
            check_results = run_basic_checks(df, contract_rules)

            # --- Dataset-level Checks ---
            if dataset_rules:
                # Row Count Minimum
                if "row_count_min" in dataset_rules:
                    row_count = len(df)
                    min_count = dataset_rules["row_count_min"]
                    status = "PASS" if row_count >= min_count else "FAIL"
                    msg = f"{row_count} rows found. Minimum expected: {min_count}."
                    check_results.append({
                        "check": "Dataset: Row Count Minimum",
                        "status": status,
                        "column": "_dataset",
                        "message": msg
                    })
                    if status == "FAIL":
                        st.session_state.setdefault("incident_log", []).append({
                            "type": "Dataset Check",
                            "column": "row_count",
                            "message": msg
                        })

                # Schema Match
                if dataset_rules.get("schema_match") is True:
                    expected_cols = set(contract_rules.keys())
                    actual_cols = set(df.columns)
                    missing = expected_cols - actual_cols
                    extra = actual_cols - expected_cols

                    if not missing and not extra:
                        check_results.append({
                            "check": "Dataset: Schema Match",
                            "status": "PASS",
                            "column": "_dataset",
                            "message": "Schema matches expected columns."
                        })
                    else:
                        diff_msg = f"Missing: {list(missing)} | Extra: {list(extra)}"
                        check_results.append({
                            "check": "Dataset: Schema Match",
                            "status": "FAIL",
                            "column": "_dataset",
                            "message": diff_msg
                        })
                        st.session_state.setdefault("incident_log", []).append({
                            "type": "Schema Check",
                            "column": "schema",
                            "message": diff_msg
                        })

            # Save results in session for reuse
            st.session_state["validation_results"] = check_results

        # --- Summary ---
        passed = sum(1 for r in check_results if r["status"] == "PASS")
        failed = sum(1 for r in check_results if r["status"] == "FAIL")

        st.metric("Total Checks", len(check_results))
        st.metric("✅ Passed", passed)
        st.metric("❌ Failed", failed)

        # --- Grouped Display ---
        grouped = defaultdict(list)
        for r in check_results:
            grouped[r.get("column", "unknown")].append(r)

        st.markdown("### 📌 Validation Results")
        for col, checks in grouped.items():
            col_name = col if col != "_dataset" else "🗂️ Dataset-Level Checks"
            st.markdown(f"#### 📁 **{col_name}**")

            for r in checks:
                color = "#28a745" if r["status"] == "PASS" else "#dc3545"
                st.markdown(
                    f"""
                    <div style="
                        background-color: #1e1e1e;
                        padding: 0.75em 1em;
                        margin: 10px 0;
                        border-left: 5px solid {color};
                        border-radius: 6px;
                    ">
                        <div style="font-weight: bold;">🔍 {r['check']} — {r['status']}</div>
                        <div style="color: #ccc;">{r['message']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:
        # Show past results if any
        if "validation_results" in st.session_state:
            st.info("⚙️ Showing last validation results.")
            check_results = st.session_state["validation_results"]

            grouped = defaultdict(list)
            for r in check_results:
                grouped[r.get("column", "unknown")].append(r)

            st.markdown("### 📌 Validation Results")
            for col, checks in grouped.items():
                col_name = col if col != "_dataset" else "🗂️ Dataset-Level Checks"
                st.markdown(f"#### 📁 **{col_name}**")
                for r in checks:
                    color = "#28a745" if r["status"] == "PASS" else "#dc3545"
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #1e1e1e;
                            padding: 0.75em 1em;
                            margin: 10px 0;
                            border-left: 5px solid {color};
                            border-radius: 6px;
                        ">
                            <div style="font-weight: bold;">🔍 {r['check']} — {r['status']}</div>
                            <div style="color: #ccc;">{r['message']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.info("Click the button above to run validation.")
