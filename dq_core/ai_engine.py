# dq_core/ai_engine.py

import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ---------------------- Constants ----------------------

RULE_GEN_PROMPT = """
You are a data quality assistant. A user has described a rule for a column:

Description: {prompt}

Here are 5 sample values from the column:
{samples}

Please return a JSON object of contract rules. Example format:
{{
  "not_null": true,
  "unique": false,
  "regex": "^[A-Z]{{2}}\\d{{4}}$",
  "min": 0,
  "max": 100
}}
Only include relevant keys. No explanations.
"""

EXPLANATION_PROMPT = """
A validation check failed with this summary:
"{summary}"

Here are some sample values from the column:
{samples}

Explain the potential issue in plain English.
"""

FULL_CONTRACT_PROMPT = """
You are an expert data quality assistant. Your task is to generate a complete data validation contract.

User prompt: "{prompt}"

Here is a preview of the dataset (10 rows):
{preview}

Return a JSON with:
- dataset_checks: general rules like row count minimum, schema enforcement, etc.
- column_checks: rules per column (nulls, unique, type, ranges, patterns)

Only return a JSON object like this:
{{
  "dataset_checks": {{
    "row_count_min": 1000,
    "schema_match": true
  }},
  "column_checks": {{
    "column1": {{ "not_null": true, "unique": true }},
    "column2": {{ "regex": "...", "min": 0 }}
  }}
}}
Do not include any explanation or notes.
"""

# ---------------------- Utility ----------------------

def get_sample_values(series: pd.Series, n=5):
    return series.dropna().astype(str).sample(min(n, len(series))).tolist()

# ---------------------- AI Logic ----------------------

def generate_contract_from_prompt(prompt: str, column_data: pd.Series) -> dict:
    samples = get_sample_values(column_data)
    input_str = RULE_GEN_PROMPT.format(prompt=prompt, samples=samples)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a JSON rule generator for data validation."},
                {"role": "user", "content": input_str}
            ],
            temperature=0.3
        )
        json_output = response.choices[0].message.content.strip()
        return json.loads(json_output)
    except Exception as e:
        print(f"[AI ERROR] Rule generation failed: {e}")
        return {}

def explain_failure(summary: str, column_data: pd.Series) -> str:
    samples = get_sample_values(column_data)
    input_str = EXPLANATION_PROMPT.format(summary=summary, samples=samples)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a data validation assistant that explains data issues."},
                {"role": "user", "content": input_str}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ AI explanation failed: {e}"

def generate_full_contract(prompt: str, df: pd.DataFrame) -> dict:
    sample_rows = df.sample(min(10, len(df)))
    preview = sample_rows.to_dict(orient="records")
    input_str = FULL_CONTRACT_PROMPT.format(prompt=prompt, preview=preview)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You generate JSON validation contracts for datasets."},
                {"role": "user", "content": input_str}
            ],
            temperature=0.3
        )
        contract_json = response.choices[0].message.content.strip()
        return json.loads(contract_json)
    except Exception as e:
        print(f"[AI ERROR] Contract generation failed: {e}")
        return {}
