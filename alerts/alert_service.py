import logging
import json
from collections import Counter
from services.investigation_services import get_recent_customer_events
from services.cluster_service import detect_live_cluster

logger = logging.getLogger("alerts")


def emit_alert(result: dict):

    customer_id = result.get("customer_id")
    if not customer_id:
        logger.error("ALERT EMISSION FAILED: missing customer_id")
        return

    # --- Enrichment: recent customer activity ---
    history = get_recent_customer_events(customer_id)

    alert_payload = {
        "decision_id": result.get("decision_id"),
        "transaction_id": result.get("transaction_id"),
        "customer_id": customer_id,
        "risk_category": result.get("risk_category"),
        "confidence_level": result.get("confidence_level"),
        "recommended_action": result.get("recommended_action"),
        "recent_activity": history
    }

    # --- Emit standard alert ---
    logger.warning(json.dumps(alert_payload))

    # --- Coordinated Attack Wave Detection ---
    try:
        event_date = result.get("timestamp", "")[:10]

        same_day_high = [
            e for e in history
            if e.get("timestamp", "")[:10] == event_date
            and e.get("risk_category") == "High"
        ]

        primary_factors = [
            e.get("primary_factor")
            for e in same_day_high
            if e.get("primary_factor")
        ]

        counter = Counter(primary_factors)

        for tactic, count in counter.items():
            if count >= 5:
                logger.critical(
                    json.dumps({
                        "type": "COORDINATED_ATTACK_WAVE",
                        "date": event_date,
                        "dominant_tactic": tactic,
                        "case_count": count
                    })
                )

    except Exception as e:
        logger.error(f"Wave detection error: {str(e)}")

    cluster = detect_live_cluster(result)

    if cluster:
        logger.critical(
            json.dumps({
                "type": "FRAUD_RING_DETECTED",
                "signature": cluster["signature"],
                "affected_customers": cluster["customers"],
                "cluster_size": cluster["cluster_size"]
            })
        )

