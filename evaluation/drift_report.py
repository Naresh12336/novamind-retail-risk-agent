import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "decision_history.jsonl"


def load():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def bucket_day(ts):
    return datetime.fromisoformat(ts).date()


def analyze(records):
    daily = defaultdict(list)

    for r in records:
        day = bucket_day(r["timestamp"])
        daily[day].append(r)

    print("\n=== DAILY RISK DISTRIBUTION ===")

    for day in sorted(daily):
        day_records = daily[day]
        high = sum(1 for r in day_records if r["risk_category"] == "High")
        total = len(day_records)

        print(day, "High Risk Rate:", round(high / total, 2))


if __name__ == "__main__":
    analyze(load())
