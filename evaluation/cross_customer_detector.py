from collections import defaultdict
from pathlib import Path
import json

LOG_FILE = Path("../logs/decision_history.jsonl")

def load():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def bucket(value, size):
    return (value // size) * size

def detect():
    records = load()
    clusters = defaultdict(list)

    for r in records:
        if r.get("risk_category") != "High":
            continue

        customer_id = r.get("customer_id")
        primary = r.get("primary_factor")

        if not customer_id or not primary:
            continue

        signature = (
            primary,
            bucket(r.get("refund_count_last_30_days", 0), 3)
        )

        clusters[signature].append(customer_id)

    print("\n=== CROSS-CUSTOMER CLUSTERS ===")

    for sig, customers in clusters.items():
        unique_customers = set(customers)
        print("SIGNATURE DISTRIBUTION:")
        for sig, customers in clusters.items():
            print(sig, "→", len(set(customers)))
        if len(unique_customers) >= 4:
            print("Coordinated Cluster Detected:")
            print("Signature:", sig)
            print("Customers:", list(unique_customers))

if __name__ == "__main__":
    detect()