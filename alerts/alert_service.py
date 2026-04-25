import logging
import json

logger = logging.getLogger("alerts")


def emit_alert(result: dict, event: dict):

    payload = {
        "decision_id": result.get("decision_id"),
        "transaction_id": result.get("transaction_id"),
        "customer_id": result.get("customer_id"),
        "risk_score": result.get("risk_score"),
        "risk_category": result.get("risk_category"),
        "confidence_level": result.get("confidence_level"),
        "recommended_action": result.get("recommended_action")
    }

    logger.warning(json.dumps(payload))

    # GRAPH CLUSTERS
    for cluster in result.get("graph_clusters", []):
        logger.critical(json.dumps(cluster))

    # GRAPH COMMUNITY
    community = result.get("graph_community")

    if community:
        logger.critical(json.dumps(community))

    # VELOCITY
    for item in result.get("velocity_clusters", []):
        logger.critical(json.dumps(item))

    # ATO
    for item in result.get("ato_findings", []):
        logger.critical(json.dumps(item))