import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "decision_history.jsonl"


def log_decision(event: dict, result: dict, signals: dict, honeypot: dict):

    record = {
        # --- Core Metadata ---
        "timestamp": datetime.utcnow().isoformat(),
        "transaction_id": result.get("transaction_id"),
        "customer_id": event.get("customer_id"),

        # --- Risk Output ---
        "risk_score": result.get("risk_score"),
        "risk_category": result.get("risk_category"),
        "confidence_score": result.get("confidence_score"),
        "confidence_level": result.get("confidence_level"),
        "action": result.get("recommended_action"),

        # --- Behavioral Signals ---
        "amount": event.get("amount"),
        "account_age_days": event.get("account_age_days"),
        "refund_count_last_30_days": event.get("refund_count_last_30_days"),

        # --- NLP Signals ---
        "keyword_count": signals.get("keyword_count"),
        "urgency_flag": signals.get("urgency_flag"),

        # --- Honeypot Signals ---
        "tactic_count": honeypot.get("tactic_count"),

        # --- Contribution Factors ---
        "primary_factor": result.get("contribution", {}).get("primary_factor"),
        "secondary_factor": result.get("contribution", {}).get("secondary_factor"),
        "supporting_factor": result.get("contribution", {}).get("supporting_factor"),

        # =========================================================
        # CRITICAL: GRAPH ENTITY PERSISTENCE (FIXES YOUR ISSUE)
        # =========================================================
        "device_id": event.get("device_id"),
        "ip_address": event.get("ip_address"),
        "payment_method_hash": event.get("payment_method_hash"),
        "shipping_address_hash": event.get("shipping_address_hash"),
        "email_hash": event.get("email_hash"),
        "phone_hash": event.get("phone_hash"),
        "browser_fingerprint": event.get("browser_fingerprint"),
    }

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")