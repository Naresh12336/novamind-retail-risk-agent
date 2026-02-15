import json
from pathlib import Path
from statistics import mean

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "decision_history.jsonl"

print("LOG FILE:", LOG_FILE)


def load():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def safe_mean(records, key):
    values = [r.get(key) for r in records if r.get(key) is not None]
    return round(mean(values), 2) if values else 0


def analyze(records):
    print("TOTAL RECORDS:", len(records))

    high = [
        r for r in records
        if str(r.get("risk_category", "")).strip().lower() == "high"
    ]

    if not high:
        print("No high-risk records found.")
        print("Available categories:",
              {r.get('risk_category') for r in records})
        return

    print("\n=== HIGH RISK ATTRIBUTION ===")
    print("Count:", len(high))

    print("\nAverage Features:")
    print("keyword_count:", safe_mean(high, "keyword_count"))
    print("tactic_count:", safe_mean(high, "tactic_count"))
    print("refund_count_last_30_days:", safe_mean(high, "refund_count_last_30_days"))
    print("account_age_days:", safe_mean(high, "account_age_days"))
    print("amount:", safe_mean(high, "amount"))


if __name__ == "__main__":
    records = load()
    analyze(records)
