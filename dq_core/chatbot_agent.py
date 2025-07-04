# dq_core/chatbot_agent.py

import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize client with correct model
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4.1-mini"

def chat_with_data_context(user_input: str, df: pd.DataFrame) -> str:
    """
    Takes user input and returns a GPT-4.1-powered response with context from a sampled DataFrame.
    """
    try:
        sample_rows = df.sample(min(5, len(df))).to_dict(orient="records")
        context = f"Data sample (5 rows):\n{json.dumps(sample_rows, indent=2)}"

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful data assistant that answers questions "
                    "related to data quality, column statistics, anomalies, and rule validation. "
                    "You only use the context provided in the data sample."
                )
            },
            {
                "role": "user",
                "content": f"{user_input}\n\n{context}"
            }
        ]

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.4
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Chatbot error: {e}"
