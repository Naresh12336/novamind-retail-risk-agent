import json
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "decision_history.jsonl"


def load():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def metrics(records):
    total = len(records)

    risk = Counter(r["risk_category"] for r in records)
    actions = Counter(r["action"] for r in records)

    high_rate = risk["High"] / total if total else 0
    block_rate = actions["Auto Block Transaction"] / total if total else 0

    print("\n=== SYSTEM HEALTH ===")
    print("Total decisions:", total)
    print("High risk rate:", round(high_rate, 2))
    print("Block rate:", round(block_rate, 2))


if __name__ == "__main__":
    metrics(load())
