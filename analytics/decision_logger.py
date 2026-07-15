import json
from datetime import datetime
from pathlib import Path

# ==========================================
# PATHS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FILE = (
    BASE_DIR / "logs" / "decision_history.jsonl"
)


# ==========================================
# JSON SERIALIZATION HELPER
# ==========================================
def make_json_serializable(obj):

    if isinstance(obj, dict):

        return {

            key: make_json_serializable(value)

            for key, value in obj.items()

        }

    if isinstance(obj, list):

        return [

            make_json_serializable(item)

            for item in obj

        ]

    if isinstance(obj, tuple):

        return [

            make_json_serializable(item)

            for item in obj

        ]

    if isinstance(obj, set):

        return sorted(

            make_json_serializable(item)

            for item in obj

        )

    return obj


# ==========================================
# MAIN LOGGER
# ==========================================
def log_decision(
    event: dict,
    result: dict,
    signals: dict,
    honeypot: dict
):

    record = {

        # ==================================
        # METADATA
        # ==================================
        "timestamp": datetime.utcnow().isoformat(),

        "transaction_id": result.get(
            "transaction_id"
        ),

        "customer_id": event.get(
            "customer_id"
        ),

        "merchant_id": event.get(
            "merchant_id"
        ),

        # ==================================
        # FINAL DECISION
        # ==================================
        "risk_score": result.get(
            "risk_score"
        ),

        "risk_category": result.get(
            "risk_category"
        ),

        "confidence_score": result.get(
            "confidence_score"
        ),

        "confidence_level": result.get(
            "confidence_level"
        ),

        "action": result.get(
            "recommended_action"
        ),

        "ml_prediction": result.get(
            "ml_prediction"
        ),

        "ml_probability": result.get(
            "ml_probability"
        ),

        # ==================================
        # INFRASTRUCTURE
        # ==================================
        "graph_score": result.get(
            "graph_score",
            0
        ),

        "velocity_score": result.get(
            "velocity_score",
            0
        ),

        "ato_score": result.get(
            "ato_score",
            0
        ),

        "geo_score": result.get(
            "geo_score",
            0
        ),

        "asn_score": result.get(
            "asn_score",
            0
        ),

        "threat_score": result.get(
            "threat_score",
            0
        ),

        "trust_score": result.get(
            "trust_score",
            0
        ),

        "merchant_score": result.get(
            "merchant_score",
            0
        ),

        "infrastructure_score": result.get(
            "infrastructure_score",
            0
        ),

        # ==================================
        # SIGNALS
        # ==================================
        "graph_signals": result.get(
            "graph_signals",
            []
        ),

        "velocity_clusters": result.get(
            "velocity_clusters",
            []
        ),

        "ato_findings": result.get(
            "ato_findings",
            []
        ),

        "geo_signals": result.get(
            "geo_signals",
            []
        ),

        "asn_signals": result.get(
            "asn_signals",
            []
        ),

        "threat_signals": result.get(
            "threat_signals",
            []
        ),

        "trust_signals": result.get(
            "trust_signals",
            []
        ),

        "merchant_signals": result.get(
            "merchant_signals",
            []
        ),

        # ==================================
        # PROFILES
        # ==================================
        "geo_profile": result.get(
            "geo_profile",
            {}
        ),

        "asn_profile": result.get(
            "asn_profile",
            {}
        ),

        "trust_profile": result.get(
            "trust_profile",
            {}
        ),

        "merchant_profile": result.get(
            "merchant_profile",
            {}
        ),

        # ==================================
        # BEHAVIORAL
        # ==================================
        "amount": event.get(
            "amount",
            0
        ),

        "account_age_days": event.get(
            "account_age_days",
            0
        ),

        "refund_count_last_30_days": event.get(
            "refund_count_last_30_days",
            0
        ),

        "transaction_type": event.get(
            "transaction_type"
        ),

        # ==================================
        # TEXTUAL
        # ==================================
        "keyword_count": signals.get(
            "keyword_count",
            0
        ),

        "urgency_flag": signals.get(
            "urgency_flag",
            False
        ),

        "text_length": signals.get(
            "text_length",
            0
        ),

        # ==================================
        # HONEYPOT
        # ==================================
        "tactic_count": honeypot.get(
            "tactic_count",
            0
        ),

        "detected_tactics": honeypot.get(
            "detected_tactics",
            []
        ),

        # ==================================
        # REPUTATION
        # ==================================
        "reputation_before": result.get(
            "reputation_before",
            50
        ),

        "reputation_adjustment": result.get(
            "reputation_adjustment",
            0
        ),

        # ==================================
        # EXPLAINABILITY
        # ==================================
        "primary_factor": result.get(
            "contribution",
            {}
        ).get(
            "primary_factor"
        ),

        "secondary_factor": result.get(
            "contribution",
            {}
        ).get(
            "secondary_factor"
        ),

        "supporting_factor": result.get(
            "contribution",
            {}
        ).get(
            "supporting_factor"
        )
    }

    record = make_json_serializable(
        record
    )

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(record) + "\n"
        )


# ==========================================
# DECISION HISTORY
# ==========================================
def get_decision_history():

    if not LOG_FILE.exists():

        return []

    history = []

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:

                history.append(
                    json.loads(line)
                )

            except Exception:
                continue

    return history


# ==========================================
# CUSTOMER HISTORY
# ==========================================
def get_customer_history(
    customer_id
):

    history = get_decision_history()

    return [

        record

        for record in history

        if record.get(
            "customer_id"
        ) == customer_id

    ]


# ==========================================
# MERCHANT HISTORY
# ==========================================
def get_merchant_history(
    merchant_id
):

    history = get_decision_history()

    return [

        record

        for record in history

        if record.get(
            "merchant_id"
        ) == merchant_id

    ]