# dq_core/profiler.py

import pandas as pd

def profile_dataframe(df: pd.DataFrame) -> dict:
    """
    Profiles the DataFrame and returns summary stats useful for AI and validation checks.

    Args:
        df (pd.DataFrame): The DataFrame to profile.

    Returns:
        dict: A dictionary containing dataset-level and column-level profiling details.
    """
    profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": {}
    }

    for col in df.columns:
        series = df[col]
        col_profile = {
            "dtype": str(series.dtype),
            "null_ratio": round(series.isnull().mean(), 4),
            "unique_ratio": round(series.nunique(dropna=True) / len(series), 4)
        }

        if series.dtype.kind in "iufc":  # Numeric
            col_profile.update({
                "min": round(series.min(), 2),
                "max": round(series.max(), 2),
                "mean": round(series.mean(), 2),
                "std_dev": round(series.std(), 2)
            })
        elif series.dtype == object:
            sample = series.dropna().astype(str)
            col_profile["sample_values"] = sample.sample(min(5, len(sample))).tolist() if not sample.empty else []

        profile["columns"][col] = col_profile

    return profile
