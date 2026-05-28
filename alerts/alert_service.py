import logging
import json

logger = logging.getLogger("alerts")


def emit_alert(result: dict, event: dict):

    # ======================================
    # PRIMARY ALERT PAYLOAD
    # ======================================
    payload = {

        "decision_id": result.get(
            "decision_id"
        ),

        "transaction_id": result.get(
            "transaction_id"
        ),

        "customer_id": result.get(
            "customer_id"
        ),

        "risk_score": result.get(
            "risk_score"
        ),

        "risk_category": result.get(
            "risk_category"
        ),

        "confidence_level": result.get(
            "confidence_level"
        ),

        "recommended_action": result.get(
            "recommended_action"
        ),

        # ----------------------------------
        # ML
        # ----------------------------------
        "ml_prediction": result.get(
            "ml_prediction"
        ),

        "ml_probability": result.get(
            "ml_probability"
        ),

        # ----------------------------------
        # INFRASTRUCTURE
        # ----------------------------------
        "graph_score": result.get(
            "graph_score"
        ),

        "velocity_score": result.get(
            "velocity_score"
        ),

        "ato_score": result.get(
            "ato_score"
        ),

        "geo_score": result.get(
            "geo_score"
        ),

        "asn_score": result.get(
            "asn_score"
        )
    }

    logger.warning(
        json.dumps(payload)
    )

    # ======================================
    # GRAPH SIGNALS
    # ======================================
    graph_signals = result.get(
        "graph_signals",
        []
    )

    for signal in graph_signals:

        logger.critical(
            json.dumps({

                "type":
                    "GRAPH_CLUSTER_DETECTED",

                "cluster_type":
                    signal
            })
        )

    # ======================================
    # GEO SIGNALS
    # ======================================
    geo_signals = result.get(
        "geo_signals",
        []
    )

    if geo_signals:

        logger.critical(
            json.dumps({

                "type":
                    "GEO_RISK_DETECTED",

                "signals":
                    geo_signals,

                "geo_profile":
                    result.get(
                        "geo_profile"
                    )
            })
        )

    # ======================================
    # ASN SIGNALS
    # ======================================
    asn_signals = result.get(
        "asn_signals",
        []
    )

    if asn_signals:

        logger.critical(
            json.dumps({

                "type":
                    "ASN_RISK_DETECTED",

                "signals":
                    asn_signals,

                "asn_profile":
                    result.get(
                        "asn_profile"
                    )
            })
        )

    # ======================================
    # VELOCITY ALERTS
    # ======================================
    velocity_clusters = result.get(
        "velocity_clusters",
        []
    )

    for item in velocity_clusters:

        logger.critical(
            json.dumps({

                "type":
                    item.get("type"),

                "entity":
                    item.get("entity"),

                "count":
                    item.get("count"),

                "window_minutes":
                    item.get(
                        "window_minutes"
                    ),

                "severity":
                    item.get(
                        "severity"
                    )
            })
        )

    # ======================================
    # ACCOUNT TAKEOVER
    # ======================================
    ato_findings = result.get(
        "ato_findings",
        []
    )

    for item in ato_findings:

        logger.critical(
            json.dumps(item)
        )

    # ======================================
    # ML EXPLAINABILITY
    # ======================================
    ml_explanation = result.get(
        "ml_explanation",
        []
    )

    if ml_explanation:

        logger.critical(
            json.dumps({

                "type":
                    "ML_EXPLAINABILITY",

                "top_contributors":
                    ml_explanation,

                "transaction_id":
                    result.get(
                        "transaction_id"
                    )
            })
        )

    # ======================================
    # ML ESCALATION
    # ======================================
    ml_probability = result.get(
        "ml_probability",
        0
    )

    if ml_probability >= 0.95:

        logger.critical(
            json.dumps({

                "type":
                    "ML_HIGH_CONFIDENCE_FRAUD",

                "ml_probability":
                    ml_probability,

                "transaction_id":
                    result.get(
                        "transaction_id"
                    )
            })
        )