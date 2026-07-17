import json
import logging

from analytics.decision_logger import (
    make_json_serializable
)

logger = logging.getLogger("alerts")


# ==========================================
# SAFE LOGGER
# ==========================================
def log_payload(
    level: str,
    payload: dict
):
    try:

        payload = make_json_serializable(
            payload
        )

        message = json.dumps(
            payload,
            default=str
        )

        if level == "warning":

            logger.warning(message)

        elif level == "critical":

            logger.critical(message)

        else:

            logger.info(message)


    except Exception as e:

        print("\n==============================")

        print("ALERT SERIALIZATION ERROR")

        print("==============================")

        print(type(payload))

        print(payload)

        print(e)

        raise


# ==========================================
# MAIN ALERT
# ==========================================
def emit_alert(
    result: dict,
    event: dict
):

    # ======================================
    # PRIMARY ALERT
    # ======================================
    log_payload(
        "warning",
        {

            "decision_id":
                result.get(
                    "decision_id"
                ),

            "transaction_id":
                result.get(
                    "transaction_id"
                ),

            "customer_id":
                result.get(
                    "customer_id"
                ),

            "risk_score":
                result.get(
                    "risk_score"
                ),

            "risk_category":
                result.get(
                    "risk_category"
                ),

            "confidence_level":
                result.get(
                    "confidence_level"
                ),

            "recommended_action":
                result.get(
                    "recommended_action"
                ),

            "ml_prediction":
                result.get(
                    "ml_prediction"
                ),

            "ml_probability":
                result.get(
                    "ml_probability"
                ),

            "graph_score":
                result.get(
                    "graph_score"
                ),

            "velocity_score":
                result.get(
                    "velocity_score"
                ),

            "ato_score":
                result.get(
                    "ato_score"
                ),

            "geo_score":
                result.get(
                    "geo_score"
                ),

            "asn_score":
                result.get(
                    "asn_score"
                )
        }
    )

    # ======================================
    # GRAPH
    # ======================================
    for signal in result.get(
        "graph_signals",
        []
    ):

        log_payload(
            "critical",
            {

                "type":
                    "GRAPH_CLUSTER_DETECTED",

                "cluster_type":
                    signal

            }
        )

    # ======================================
    # GEO
    # ======================================
    if result.get(
        "geo_signals"
    ):

        log_payload(
            "critical",
            {

                "type":
                    "GEO_RISK_DETECTED",

                "signals":
                    result.get(
                        "geo_signals"
                    ),

                "geo_profile":
                    result.get(
                        "geo_profile"
                    )

            }
        )

    # ======================================
    # ASN
    # ======================================
    if result.get(
        "asn_signals"
    ):

        log_payload(
            "critical",
            {

                "type":
                    "ASN_RISK_DETECTED",

                "signals":
                    result.get(
                        "asn_signals"
                    ),

                "asn_profile":
                    result.get(
                        "asn_profile"
                    )

            }
        )

    # ======================================
    # MERCHANT
    # ======================================
    if result.get(
        "merchant_signals"
    ):

        log_payload(
            "critical",
            {

                "type":
                    "MERCHANT_RISK_DETECTED",

                "signals":
                    result.get(
                        "merchant_signals"
                    ),

                "merchant_profile":
                    result.get(
                        "merchant_profile"
                    )

            }
        )

    # ======================================
    # THREAT
    # ======================================
    if result.get(
        "threat_signals"
    ):

        log_payload(
            "critical",
            {

                "type":
                    "THREAT_INTELLIGENCE",

                "signals":
                    result.get(
                        "threat_signals"
                    ),

                "threat_profile":
                    result.get(
                        "threat_profile"
                    )

            }
        )

    # ======================================
    # TRUST
    # ======================================
    if result.get(
        "trust_signals"
    ):

        log_payload(
            "critical",
            {

                "type":
                    "TRUST_NETWORK",

                "signals":
                    result.get(
                        "trust_signals"
                    ),

                "trust_profile":
                    result.get(
                        "trust_profile"
                    )

            }
        )

    # ======================================
    # VELOCITY
    # ======================================
    for cluster in result.get(
        "velocity_clusters",
        []
    ):

        log_payload(
            "critical",
            {

                "type":
                    cluster.get(
                        "type"
                    ),

                "entity":
                    cluster.get(
                        "entity"
                    ),

                "count":
                    cluster.get(
                        "count"
                    ),

                "window_minutes":
                    cluster.get(
                        "window_minutes"
                    ),

                "severity":
                    cluster.get(
                        "severity"
                    )

            }
        )

    # ======================================
    # ACCOUNT TAKEOVER
    # ======================================
    for finding in result.get(
        "ato_findings",
        []
    ):

        log_payload(
            "critical",
            finding
        )

    # ======================================
    # ML EXPLAINABILITY
    # ======================================
    explanation = result.get(
        "ml_explanation",
        []
    )

    if explanation:

        log_payload(
            "critical",
            {

                "type":
                    "ML_EXPLAINABILITY",

                "top_contributors":
                    explanation,

                "transaction_id":
                    result.get(
                        "transaction_id"
                    )

            }
        )

    # ======================================
    # HIGH CONFIDENCE ML
    # ======================================
    probability = result.get(
        "ml_probability",
        0
    )

    if probability >= 0.95:

        log_payload(
            "critical",
            {

                "type":
                    "ML_HIGH_CONFIDENCE_FRAUD",

                "ml_probability":
                    probability,

                "transaction_id":
                    result.get(
                        "transaction_id"
                    )

            }
        )