import logging
import json
from collections import Counter
from services.investigation_services import get_recent_customer_events
from services.cluster_service import detect_live_cluster
from services.graph_service import detect_graph_cluster

logger = logging.getLogger("alerts")


def emit_alert(result: dict, event:dict):

    customer_id = result.get("customer_id")

    if not customer_id:
        logger.error("Missing customer_id in alert")
        return

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

    logger.warning(json.dumps(alert_payload))

    # --- Wave Detection ---
    try:

        primary_factors = [
            e.get("primary_factor")
            for e in history
            if e.get("risk_category") == "High"
        ]

        counter = Counter(primary_factors)

        for tactic, count in counter.items():

            if count >= 5:
                logger.critical(
                    json.dumps({
                        "type": "COORDINATED_ATTACK_WAVE",
                        "dominant_tactic": tactic,
                        "case_count": count
                    })
                )

    except Exception as e:
        logger.error(f"Wave detection error: {str(e)}")

    # --- Cluster Detection ---
    cluster_input = {
        "customer_id": result.get("customer_id"),
        "primary_factor": result.get("contribution", {}).get("primary_factor"),
        "refund_count_last_30_days": result.get("evidence", {})
        .get("behavioral_signals", {})
        .get("refund_count_last_30_days", 0)
    }

    cluster = detect_live_cluster(cluster_input)

    print("RUNNING CLUSTER CHECK")
    print("CLUSTER RESULT:", cluster)

    if cluster:

        logger.critical(
            json.dumps({
                "type": "FRAUD_RING_DETECTED",
                "signature": cluster["signature"],
                "affected_customers": cluster["customers"],
                "cluster_size": cluster["cluster_size"]
            })
        )

    graph_input = {
        "customer_id": result.get("customer_id"),
        "device_id": result.get("device_id"),
        "ip_address": result.get("ip_address"),
        "payment_method_hash": result.get("payment_method_hash"),
        "shipping_address_hash": result.get("shipping_address_hash"),
        "email_hash": result.get("email_hash"),
        "phone_hash": result.get("phone_hash")
    }

    graph_cluster = detect_graph_cluster(event)

    if graph_cluster:
        logger.critical(
            json.dumps({
                "type": "FRAUD_NETWORK_DETECTED",
                "cluster_type": graph_cluster["type"],
                "entity": graph_cluster["entity"],
                "affected_customers": graph_cluster["customers"],
                "cluster_size": graph_cluster["cluster_size"]
            })
        )