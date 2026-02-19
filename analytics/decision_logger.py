import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "decision_history.jsonl"


def log_decision(event: dict, result: dict, signals: dict, honeypot: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "transaction_id": result.get("transaction_id"),
        "customer_id": event.get("customer_id"),
        "risk_score": result.get("risk_score"),
        "risk_category": result.get("risk_category"),
        "confidence_score": result.get("confidence_score"),
        "confidence_level": result.get("confidence_level"),
        "action": result.get("recommended_action"),

        # behavioral
        "amount": event.get("amount"),
        "account_age_days": event.get("account_age_days"),
        "refund_count_last_30_days": event.get("refund_count_last_30_days"),

        # textual
        "keyword_count": signals.get("keyword_count"),
        "urgency_flag": signals.get("urgency_flag"),

        # adversarial
        "tactic_count": honeypot.get("tactic_count"),

    }

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
