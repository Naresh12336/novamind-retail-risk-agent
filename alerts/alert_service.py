import logging
import json
from collections import Counter

from services.investigation_services import get_recent_customer_events
from services.cluster_service import detect_live_cluster
from services.graph_service import (
    detect_graph_cluster,
    detect_fraud_community
)

logger = logging.getLogger("alerts")


def emit_alert(result: dict, event: dict):

    customer_id = result.get("customer_id")

    if not customer_id:
        logger.error("ALERT FAILED: missing customer_id")
        return

    # ==================================================
    # CUSTOMER HISTORY
    # ==================================================
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

    # ==================================================
    # CLASSIC FRAUD RING DETECTION
    # ==================================================
    cluster_input = {
        "customer_id": customer_id,
        "primary_factor": result.get("contribution", {}).get("primary_factor"),
        "refund_count_last_30_days": result.get(
            "evidence", {}
        ).get(
            "behavioral_signals", {}
        ).get(
            "refund_count_last_30_days", 0
        )
    }

    cluster = detect_live_cluster(cluster_input)

    if cluster:
        logger.critical(json.dumps({
            "type": "FRAUD_RING_DETECTED",
            "signature": cluster["signature"],
            "affected_customers": cluster["customers"],
            "cluster_size": cluster["cluster_size"]
        }))

    # ==================================================
    # GRAPH CLUSTER DETECTION
    # ==================================================
    graph_clusters = detect_graph_cluster(event)

    if graph_clusters:
        for cluster in graph_clusters:
            logger.critical(json.dumps({
                "type": "GRAPH_CLUSTER_DETECTED",
                "cluster_type": cluster["type"],
                "entity": cluster["entity"],
                "customers": cluster["customers"],
                "cluster_size": cluster["cluster_size"]
            }))

    velocity_clusters = result.get("velocity_clusters", [])

    for item in velocity_clusters:
        logger.critical(json.dumps({
            "type": item["type"],
            "entity": item["entity"],
            "count": item["count"],
            "window_minutes": item["window_minutes"],
            "severity": item["severity"]
        }))

    # ==================================================
    # GRAPH COMMUNITY DETECTION
    # ==================================================
    community = detect_fraud_community(customer_id)

    if community:
        logger.critical(json.dumps({
            "type": "FRAUD_NETWORK_COMMUNITY",
            "customers": community["customers"],
            "community_size": community["community_size"]
        }))