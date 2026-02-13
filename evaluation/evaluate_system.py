import json
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "decision_history.jsonl"


def load_records():
    if not LOG_FILE.exists():
        print("No decision history found.")
        return []

    records = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    return records


def summarize(records):
    total = len(records)
    if total == 0:
        print("No data.")
        return

    risk_dist = Counter(r["risk_category"] for r in records)
    action_dist = Counter(r["action"] for r in records)
    confidence_dist = Counter(r["confidence_level"] for r in records)

    avg_score = sum(r["risk_score"] for r in records) / total
    avg_conf = sum(r["confidence_score"] for r in records) / total

    print("\n=== SYSTEM SUMMARY ===")
    print("Total Transactions:", total)

    print("\nRisk Distribution:")
    for k, v in risk_dist.items():
        print(f"  {k}: {v} ({v/total:.2%})")

    print("\nAction Distribution:")
    for k, v in action_dist.items():
        print(f"  {k}: {v} ({v/total:.2%})")

    print("\nConfidence Distribution:")
    for k, v in confidence_dist.items():
        print(f"  {k}: {v} ({v/total:.2%})")

    print("\nAverages:")
    print("  Avg Risk Score:", round(avg_score, 2))
    print("  Avg Confidence:", round(avg_conf, 2))


def detect_anomalies(records):
    print("\n=== SANITY CHECKS ===")

    high_low_conf = [
        r for r in records
        if r["risk_category"] == "High" and r["confidence_level"] == "Low"
    ]

    low_high_conf = [
        r for r in records
        if r["risk_category"] == "Low" and r["confidence_level"] == "High"
    ]

    print("High Risk + Low Confidence:", len(high_low_conf))
    print("Low Risk + High Confidence:", len(low_high_conf))


if __name__ == "__main__":
    records = load_records()
    summarize(records)
    detect_anomalies(records)
