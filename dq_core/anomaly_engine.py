import pandas as pd

def scan_for_anomalies(
    df: pd.DataFrame,
    z_threshold: float = 3.0,
    outlier_pct_limit: float = 0.01
) -> list:
    """
    Scans the numeric columns of a DataFrame for anomalies based on Z-score.

    Args:
        df (pd.DataFrame): Input data.
        z_threshold (float): Threshold beyond which values are considered outliers.
        outlier_pct_limit (float): Minimum proportion of outliers required to flag column.

    Returns:
        List of anomaly dictionaries for flagged columns.
    """
    anomalies = []

    numeric_cols = df.select_dtypes(include=["number"]).columns

    for col in numeric_cols:
        series = df[col].dropna()

        if series.empty:
            continue

        mean = series.mean()
        std = series.std()

        if std == 0:
            continue  # No deviation

        upper_bound = mean + z_threshold * std
        lower_bound = mean - z_threshold * std

        outliers = series[(series < lower_bound) | (series > upper_bound)]
        outlier_ratio = len(outliers) / len(series)

        if outlier_ratio > outlier_pct_limit:
            severity = (
                "high" if outlier_ratio > 0.1 else
                "medium" if outlier_ratio > 0.03 else
                "low"
            )

            anomalies.append({
                "column": col,
                "issue": f"{outlier_ratio:.2%} of values are outliers (±{z_threshold}σ)",
                "outlier_count": int(len(outliers)),
                "total_count": int(len(series)),
                "severity": severity,
                "mean": round(mean, 2),
                "std_dev": round(std, 2),
                "bounds": [round(lower_bound, 2), round(upper_bound, 2)]  # standardized key
            })

    # Optional: sort by severity and outlier count descending
    severity_order = {"high": 0, "medium": 1, "low": 2}
    anomalies.sort(key=lambda x: (severity_order[x["severity"]], -x["outlier_count"]))

    return anomalies
