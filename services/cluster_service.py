from collections import defaultdict
from pathlib import Path
import json

LOG_FILE = Path("../logs/decision_history.jsonl")

MIN_CLUSTER_SIZE = 4
REFUND_BUCKET_SIZE = 3


def bucket(value, size):
    return (value // size) * size


def detect_live_cluster(current_record: dict):
    if not LOG_FILE.exists():
        return None

    primary = current_record.get("primary_factor")
    if not primary:
        return None

    signature = (
        primary,
        bucket(current_record.get("refund_count_last_30_days", 0), REFUND_BUCKET_SIZE)
    )

    clusters = defaultdict(set)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)

            if r.get("risk_category") != "High":
                continue

            if r.get("primary_factor") != signature[0]:
                continue

            sig = (
                r.get("primary_factor"),
                bucket(r.get("refund_count_last_30_days", 0), REFUND_BUCKET_SIZE)
            )

            if sig == signature:
                clusters[sig].add(r.get("customer_id"))

    customers = clusters.get(signature, set())

    if len(customers) >= MIN_CLUSTER_SIZE:
        return {
            "signature": signature,
            "customers": list(customers),
            "cluster_size": len(customers)
        }
    print("LIVE CLUSTER CHECK TRIGGERED")

    return None