import streamlit as st
from dq_core.ai_engine import generate_contract_from_prompt, generate_full_contract


def render():
    st.header("📄 Data Contracts")

    if "raw_data" not in st.session_state:
        st.warning("⚠️ Please ingest data first (via Ingestion tab).")
        return

    df = st.session_state["raw_data"]

    # Ensure session state keys
    if "contract_rules" not in st.session_state:
        st.session_state["contract_rules"] = {}
    if "dataset_rules" not in st.session_state:
        st.session_state["dataset_rules"] = {}

    st.markdown("Use AI to define and refine validation rules before data reaches business dashboards.")

    # --- Full Contract Generation ---
    st.subheader("🧠 Auto-generate Full Contract with AI")

    ai_prompt = st.text_input(
        "Prompt (e.g., 'Validate this product catalog for analytics')",
        placeholder="Describe your validation intent..."
    )

    if st.button("🚀 Generate Contract with AI"):
        if ai_prompt.strip() == "":
            st.warning("Please provide a prompt before generating the contract.")
        else:
            with st.spinner("Asking OpenAI to generate a full contract..."):
                contract = generate_full_contract(ai_prompt, df)

            if contract:
                st.session_state["dataset_rules"] = contract.get("dataset_checks", {})
                st.session_state["contract_rules"] = contract.get("column_checks", {})
                st.success("✅ AI-generated contract loaded.")
            else:
                st.error("❌ Failed to generate contract.")

    # --- Dataset Rules View ---
    st.markdown("### 📊 Dataset-Level Rules")
    if st.session_state["dataset_rules"]:
        st.json(st.session_state["dataset_rules"])
    else:
        st.info("No dataset-level contract yet.")

    # --- Column Rules Section ---
    st.markdown("### 📋 Column-Level Rules")

    selected_col = st.selectbox("Select Column", df.columns)

    with st.form(key="contract_form"):
        st.write(f"Define rules for **{selected_col}** using natural language:")
        col_prompt = st.text_input("Column Rule Prompt", key="rule_prompt")

        submit = st.form_submit_button("🤖 Generate Rule for Column")
        if submit:
            if not col_prompt.strip():
                st.warning("Please enter a rule description.")
            else:
                with st.spinner("Generating column rule via AI..."):
                    result = generate_contract_from_prompt(col_prompt, df[selected_col])

                if result:
                    st.session_state["contract_rules"][selected_col] = result
                    st.success(f"✅ Rule for **{selected_col}** added.")
                else:
                    st.error("❌ AI generation failed.")

    if st.session_state["contract_rules"]:
        st.markdown("### 📌 Current Column Rules")
        st.json(st.session_state["contract_rules"])
    else:
        st.info("No column rules defined yet.")
