from collections import defaultdict
from statistics import mean
from pathlib import Path
import json
from datetime import datetime

LOG_FILE = Path("../logs/decision_history.jsonl")

def load():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def monitor():
    records = load()

    daily = defaultdict(list)

    for r in records:
        date = r["timestamp"][:10]
        daily[date].append(r)

    rates = {}

    for d, recs in daily.items():
        high = sum(1 for r in recs if r["risk_category"] == "High")
        rates[d] = high / len(recs)

    baseline = mean(rates.values())

    print("\n=== DRIFT MONITOR ===")
    MIN_VOLUME = 5
    SPIKE_MULTIPLIER = 1.5

    for d, recs in daily.items():
        high = sum(1 for r in recs if r["risk_category"] == "High")
        rate = high / len(recs)

        if len(recs) >= MIN_VOLUME and rate > baseline * SPIKE_MULTIPLIER:
            print(f"Anomaly detected on {d}: Spike ({rate:.2f}, volume={len(recs)})")
        else:
            print(f"{d}: Normal ({rate:.2f}, volume={len(recs)})")

if __name__ == "__main__":
    monitor()