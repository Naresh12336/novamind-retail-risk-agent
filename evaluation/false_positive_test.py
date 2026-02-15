import requests
import random

URL = "http://127.0.0.1:8000/analyze-transaction"

def legit_transaction(i):
    return {
        "transaction_id": f"L{i}",
        "customer_id": f"C{i}",
        "transaction_type": "purchase",
        "description": "normal purchase order",
        "amount": random.randint(20, 200),
        "account_age_days": random.randint(100, 1000),
        "refund_count_last_30_days": 0,
        "timestamp": "2026-02-16T10:00:00Z"
    }

flagged = 0
N = 30

for i in range(N):
    r = requests.post(URL, json=legit_transaction(i)).json()
    if r["risk_category"] != "Low":
        flagged += 1

print("False Positive Rate:", flagged / N)
