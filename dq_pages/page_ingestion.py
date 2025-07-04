import streamlit as st
import pandas as pd
import snowflake.connector
from snowflake.connector.errors import ProgrammingError

def render():
    st.header("📥 Ingest Data")

    st.markdown("Upload a CSV file or connect to a Snowflake table.")

    # --- File Upload ---
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, low_memory=False)
            st.session_state["raw_data"] = df
            st.success(f"✅ Uploaded `{uploaded_file.name}` successfully.")
            st.subheader("🔍 Data Preview")
            st.dataframe(df.head(20), use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

    # --- Snowflake Connection ---
    with st.expander("🔒 Connect to Snowflake"):
        account = st.text_input("Account")
        user = st.text_input("User")
        password = st.text_input("Password", type="password")
        warehouse = st.text_input("Warehouse")
        database = st.text_input("Database")
        schema = st.text_input("Schema")
        table = st.text_input("Table")

        if st.button("Load from Snowflake"):
            if not all([account, user, password, warehouse, database, schema, table]):
                st.error("Please fill in all Snowflake connection details.")
            else:
                try:
                    conn = snowflake.connector.connect(
                        user=user,
                        password=password,
                        account=account,
                        warehouse=warehouse,
                        database=database,
                        schema=schema,
                    )
                    query = f"SELECT * FROM {schema}.{table} LIMIT 10000"
                    df = pd.read_sql(query, conn)
                    conn.close()
                    st.session_state["raw_data"] = df
                    st.success(f"✅ Loaded table `{table}` from Snowflake.")
                    st.subheader("🔍 Data Preview")
                    st.dataframe(df.head(20), use_container_width=True)
                except ProgrammingError as e:
                    st.error(f"Snowflake error: {e}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # --- Load Status ---
    if "raw_data" in st.session_state:
        st.info("📦 Data loaded and ready for validation.")
    else:
        st.warning("⚠️ No data loaded yet.")
