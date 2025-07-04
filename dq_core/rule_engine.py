# dq_core/rule_engine.py

import pandas as pd
import re

def run_basic_checks(df: pd.DataFrame, contract_rules: dict = None):
    results = []

    if df.empty:
        return results

    for col in df.columns:
        series = df[col]
        col_results = []
        col_contract = contract_rules.get(col, {}) if contract_rules else {}

        non_null_series = series.dropna()
        total_len = len(series)

        # --- Basic Null Check ---
        null_ratio = series.isnull().mean()
        col_results.append({
            "column": col,
            "check": "Null Check",
            "status": "FAIL" if null_ratio > 0 else "PASS",
            "message": f"{null_ratio:.2%} of values are null" if null_ratio > 0 else "No nulls found",
            "severity": "medium" if null_ratio > 0.05 else "low"
        })

        # --- Basic Uniqueness Check ---
        unique_ratio = non_null_series.nunique() / total_len if total_len else 0
        col_results.append({
            "column": col,
            "check": "Uniqueness Check",
            "status": "PASS" if unique_ratio >= 0.99 else "FAIL",
            "message": f"{unique_ratio:.2%} unique values",
            "severity": "low" if unique_ratio >= 0.95 else "medium"
        })

        # --- Contract: Not Null ---
        if col_contract.get("not_null") and null_ratio > 0:
            col_results.append({
                "column": col,
                "check": "Contract - Not Null",
                "status": "FAIL",
                "message": f"Contract failed: {null_ratio:.2%} nulls found",
                "severity": "high"
            })

        # --- Contract: Unique ---
        if col_contract.get("unique") and unique_ratio < 1.0:
            col_results.append({
                "column": col,
                "check": "Contract - Unique",
                "status": "FAIL",
                "message": f"Contract failed: Only {unique_ratio:.2%} unique values",
                "severity": "high"
            })

        # --- Contract: Regex Pattern ---
        regex = col_contract.get("regex")
        if regex:
            try:
                mismatch_ratio = non_null_series.apply(lambda x: not re.fullmatch(regex, str(x))).mean()
                if mismatch_ratio > 0:
                    col_results.append({
                        "column": col,
                        "check": "Contract - Regex",
                        "status": "FAIL",
                        "message": f"{mismatch_ratio:.2%} values do not match pattern `{regex}`",
                        "severity": "medium"
                    })
                else:
                    col_results.append({
                        "column": col,
                        "check": "Contract - Regex",
                        "status": "PASS",
                        "message": "All values match the expected pattern",
                        "severity": "low"
                    })
            except re.error as e:
                col_results.append({
                    "column": col,
                    "check": "Contract - Regex",
                    "status": "FAIL",
                    "message": f"Invalid regex pattern: {e}",
                    "severity": "high"
                })

        # --- Contract: Numeric Bounds ---
        if series.dtype.kind in "iufc":
            val_min = col_contract.get("min")
            val_max = col_contract.get("max")

            if val_min is not None:
                below_min = (series < val_min).sum()
                if below_min > 0:
                    col_results.append({
                        "column": col,
                        "check": "Contract - Min Value",
                        "status": "FAIL",
                        "message": f"{below_min} values below minimum ({val_min})",
                        "severity": "medium"
                    })
                else:
                    col_results.append({
                        "column": col,
                        "check": "Contract - Min Value",
                        "status": "PASS",
                        "message": f"All values above minimum ({val_min})",
                        "severity": "low"
                    })

            if val_max is not None:
                above_max = (series > val_max).sum()
                if above_max > 0:
                    col_results.append({
                        "column": col,
                        "check": "Contract - Max Value",
                        "status": "FAIL",
                        "message": f"{above_max} values above maximum ({val_max})",
                        "severity": "medium"
                    })
                else:
                    col_results.append({
                        "column": col,
                        "check": "Contract - Max Value",
                        "status": "PASS",
                        "message": f"All values below maximum ({val_max})",
                        "severity": "low"
                    })

        results.extend(col_results)

    return results
