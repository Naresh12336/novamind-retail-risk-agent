import logging
import json

logger = logging.getLogger("alerts")


def emit_alert(result: dict, event: dict):

    # ======================================
    # PRIMARY ALERT
    # ======================================
    payload = {
        "decision_id": result.get("decision_id"),
        "transaction_id": result.get("transaction_id"),
        "customer_id": result.get("customer_id"),

        "risk_score": result.get("risk_score"),
        "risk_category": result.get("risk_category"),
        "confidence_level": result.get("confidence_level"),
        "recommended_action": result.get("recommended_action"),

        "reputation_before": result.get("reputation_before"),
        "reputation_adjustment": result.get("reputation_adjustment")
    }

    logger.warning(json.dumps(payload))

    # ======================================
    # GRAPH CLUSTERS
    # ======================================
    for cluster in result.get("graph_clusters", []):
        logger.critical(json.dumps(cluster))

    # ======================================
    # GRAPH COMMUNITY
    # ======================================
    community = result.get("graph_community")

    if community:
        logger.critical(json.dumps(community))

    # ======================================
    # VELOCITY ALERTS
    # ======================================
    for item in result.get("velocity_clusters", []):
        logger.critical(json.dumps(item))

    # ======================================
    # ACCOUNT TAKEOVER ALERTS
    # ======================================
    for item in result.get("ato_findings", []):
        logger.critical(json.dumps(item))

    # ======================================
    # GEO ALERTS
    # ======================================
    geo_signals = result.get("geo_signals", [])
    geo_profile = result.get("geo_profile", {})

    if geo_signals:
        logger.critical(json.dumps({
            "type": "GEO_RISK_DETECTED",
            "signals": geo_signals,
            "location": geo_profile
        }))

    # ======================================
    # ASN ALERTS (NEW)
    # ======================================
    asn_signals = result.get("asn_signals", [])
    asn_profile = result.get("asn_profile", {})

    if asn_signals:
        logger.critical(json.dumps({
            "type": "ASN_RISK_DETECTED",
            "signals": asn_signals,
            "asn_profile": asn_profile
        }))