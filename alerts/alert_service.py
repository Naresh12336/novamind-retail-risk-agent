import logging
import json
from services.investigation_services import get_recent_customer_events

logger = logging.getLogger("alerts")

def emit_alert(result: dict):

    customer_id = result["customer_id"]
    history = get_recent_customer_events(customer_id)

    alert_payload = {
        "decision_id": result["decision_id"],
        "transaction_id": result["transaction_id"],
        "customer_id": customer_id,
        "risk_category": result["risk_category"],
        "confidence_level": result["confidence_level"],
        "recommended_action": result["recommended_action"],
        "recent_activity": history
    }

    logger.warning(json.dumps(alert_payload))