import json
import os
from datetime import datetime

ALERT_FILE = "logs/high_risk_alerts.json"


def emit_alert(result: dict):
    from services.investigation_services import get_recent_customer_events

    customer_id = result["customer_id"]
    history = get_recent_customer_events(customer_id)

    print("\n=== ALERT TRIGGERED ===")
    print({
        "decision_id": result["decision_id"],
        "customer_id": customer_id,
        "risk": result["risk_category"],
        "action": result["recommended_action"],
        "recent_activity": history
    })