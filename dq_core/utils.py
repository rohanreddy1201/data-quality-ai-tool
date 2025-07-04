import pandas as pd

def format_check_result(result: dict) -> str:
    """
    Formats a single check result for display.
    """
    status_icon = "✅" if result["status"] == "PASS" else "❌"
    return f"{status_icon} **{result['check']}**: {result['message']}"


def highlight_failures(df: pd.DataFrame, failed_columns: list) -> pd.DataFrame:
    """
    Highlights columns that failed checks by marking them.
    """
    styled_df = df.copy()
    for col in failed_columns:
        if col in styled_df.columns:
            styled_df[col] = styled_df[col].astype(str) + " ❗"
    return styled_df


def extract_failed_columns(results: list) -> list:
    """
    Extracts column names from failed check results.
    """
    return list({r["column"] for r in results if r.get("status") == "FAIL" and r.get("column")})
