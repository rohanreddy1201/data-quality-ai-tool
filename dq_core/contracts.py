# dq_core/contracts.py

import json
import os
from typing import Dict


DEFAULT_CONTRACT_PATH = "saved_contract.json"


def save_contract(contract: Dict, path: str = DEFAULT_CONTRACT_PATH) -> None:
    """
    Saves the generated contract dictionary as JSON to the specified file path.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(contract, f, indent=2)
        print(f"[Contract Saved] ✅ File saved to: {path}")
    except Exception as e:
        print(f"[Contract Save Error] ❌ {e}")


def load_contract(path: str = DEFAULT_CONTRACT_PATH) -> Dict:
    """
    Loads a contract JSON file from the specified path, or returns an empty dictionary.
    """
    if not os.path.exists(path):
        print(f"[Contract Load] ⚠️ File not found: {path}")
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Contract Load Error] ❌ {e}")
        return {}
