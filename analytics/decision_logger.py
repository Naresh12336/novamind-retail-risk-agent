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
# MAIN LOGGER
# ==========================================
def log_decision(
    event: dict,
    result: dict,
    signals: dict,
    honeypot: dict
):

    record = {

        # ----------------------------------
        # METADATA
        # ----------------------------------
        "timestamp": datetime.utcnow().isoformat(),

        "transaction_id": result.get(
            "transaction_id"
        ),

        "customer_id": event.get(
            "customer_id"
        ),

        # ----------------------------------
        # FINAL DECISION
        # ----------------------------------
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

        # ----------------------------------
        # INFRASTRUCTURE SCORES
        # ----------------------------------
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

        # ----------------------------------
        # SIGNALS
        # ----------------------------------
        "graph_signals": result.get(
            "graph_signals",
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

        "velocity_clusters": result.get(
            "velocity_clusters",
            []
        ),

        "ato_findings": result.get(
            "ato_findings",
            []
        ),

        # ----------------------------------
        # BEHAVIORAL
        # ----------------------------------
        "amount": event.get(
            "amount"
        ),

        "account_age_days": event.get(
            "account_age_days"
        ),

        "refund_count_last_30_days": event.get(
            "refund_count_last_30_days"
        ),

        # ----------------------------------
        # TEXTUAL
        # ----------------------------------
        "keyword_count": signals.get(
            "keyword_count"
        ),

        "urgency_flag": signals.get(
            "urgency_flag"
        ),

        "text_length": signals.get(
            "text_length"
        ),

        # ----------------------------------
        # HONEYPOT
        # ----------------------------------
        "tactic_count": honeypot.get(
            "tactic_count"
        ),

        "detected_tactics": honeypot.get(
            "detected_tactics",
            []
        ),

        # ----------------------------------
        # REPUTATION
        # ----------------------------------
        "reputation_before": result.get(
            "reputation_before",
            50
        ),

        "reputation_adjustment": result.get(
            "reputation_adjustment",
            0
        ),

        # ----------------------------------
        # CONTRIBUTION
        # ----------------------------------
        "primary_factor": result.get(
            "contribution",
            {}
        ).get("primary_factor"),

        "secondary_factor": result.get(
            "contribution",
            {}
        ).get("secondary_factor"),

        "supporting_factor": result.get(
            "contribution",
            {}
        ).get("supporting_factor")
    }

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