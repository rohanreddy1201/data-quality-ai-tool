# dq_core/ingestion.py

import pandas as pd

def read_csv_from_path(path: str, low_memory: bool = False) -> pd.DataFrame:
    """
    Reads a CSV file from a local path and returns a DataFrame.

    Args:
        path (str): Path to the CSV file.
        low_memory (bool): Whether to internally process file in chunks (avoids dtype issues).

    Returns:
        pd.DataFrame: Loaded DataFrame, or empty if error occurs.
    """
    try:
        df = pd.read_csv(path, low_memory=low_memory)
        print(f"[Ingestion] ✅ Loaded CSV from {path} with {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except Exception as e:
        print(f"[Ingestion Error] ❌ Failed to read {path}: {e}")
        return pd.DataFrame()
