from collections import defaultdict, Counter
from pathlib import Path
import json

LOG_FILE = Path("../logs/decision_history.jsonl")

def load():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def detect():
    records = load()

    daily_tactics = defaultdict(list)

    for r in records:
        date = r["timestamp"][:10]
        tactics = r.get("tactic_count", 0)
        primary = r.get("contribution", {}).get("primary_factor")
        if primary:
            daily_tactics[date].append(primary)

    print("\n=== TACTIC WAVE DETECTION ===")

    for date, tactics in daily_tactics.items():
        counter = Counter(tactics)
        total = sum(counter.values())

        for tactic, count in counter.items():
            if total >= 5 and count / total > 0.6:
                print(f"Coordinated pattern on {date}: {tactic} dominance ({count}/{total})")

if __name__ == "__main__":
    detect()