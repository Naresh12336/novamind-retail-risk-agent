import requests
import random

URL = "http://127.0.0.1:8000/analyze-transaction"

def attack_case(i):
    return {
        "transaction_id": f"A{i}",
        "customer_id": f"F{i}",
        "transaction_type": "refund",
        "description": random.choice([
            "refund immediately or complaint",
            "legal action if not refunded",
            "urgent refund now",
            "return processed refund now",
            "refund or I escalate"
        ]),
        "amount": random.randint(100, 800),
        "account_age_days": random.randint(1, 20),
        "refund_count_last_30_days": random.randint(3, 8),
        "timestamp": "2026-02-16T10:00:00Z"
    }

detected = 0
N = 30

for i in range(N):
    r = requests.post(URL, json=attack_case(i)).json()
    if r["risk_category"] == "High":
        detected += 1

print("Attack Detection Rate:", detected / N)
