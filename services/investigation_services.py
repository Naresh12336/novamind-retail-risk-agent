import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "decision_history.jsonl"


def get_decision_by_id(decision_id: str):
    if not LOG_FILE.exists():
        return None

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if record.get("decision_id") == decision_id:
                return record

    return None
