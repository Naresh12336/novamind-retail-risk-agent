import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/decision_history.jsonl")


def log_decision(event: dict, result: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "transaction_id": result.get("transaction_id"),
        "risk_score": result.get("risk_score"),
        "risk_category": result.get("risk_category"),
        "confidence_score": result.get("confidence_score"),
        "confidence_level": result.get("confidence_level"),
        "action": result.get("recommended_action"),
        "amount": event.get("amount"),
        "account_age_days": event.get("account_age_days"),
        "refund_count_last_30_days": event.get("refund_count_last_30_days"),
    }

    LOG_FILE.parent.mkdir(exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
