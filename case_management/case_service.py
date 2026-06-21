import uuid
from datetime import datetime

from case_management.case_store import (
    case_db,
    customer_case_index,
    transaction_case_index
)


def create_case(result):

    case_id = str(uuid.uuid4())

    case = {

        "case_id": case_id,

        "created_at":
            datetime.utcnow().isoformat(),

        "status":
            "OPEN",

        "priority":
            determine_priority(result),

        "customer_id":
            result.get("customer_id"),

        "transaction_id":
            result.get("transaction_id"),

        "risk_score":
            result.get("risk_score"),

        "risk_category":
            result.get("risk_category"),

        "recommended_action":
            result.get("recommended_action"),

        "evidence":
            build_evidence(result)
    }

    case_db[case_id] = case

    customer_case_index[
        result.get("customer_id")
    ].append(case_id)

    transaction_case_index[
        result.get("transaction_id")
    ].append(case_id)

    return case


def determine_priority(result):

    score = result.get(
        "risk_score",
        0
    )

    ml_prob = result.get(
        "ml_probability",
        0
    )

    if score >= 95 or ml_prob >= 0.98:
        return "CRITICAL"

    if score >= 80:
        return "HIGH"

    if score >= 60:
        return "MEDIUM"

    return "LOW"


def build_evidence(result):

    return {

        "graph_signals":
            result.get(
                "graph_signals",
                []
            ),

        "geo_signals":
            result.get(
                "geo_signals",
                []
            ),

        "geo_profile":
            result.get(
                "geo_profile",
                {}
            ),

        "asn_signals":
            result.get(
                "asn_signals",
                []
            ),

        "asn_profile":
            result.get(
                "asn_profile",
                {}
            ),

        "trust_profile":
            result.get(
                "trust_profile",
                {}
            ),

        "trust_signals":
            result.get(
                "trust_signals",
                []
            ),

        "ato_findings":
            result.get(
                "ato_findings",
                []
            ),

        "ml_explanation":
            result.get(
                "ml_explanation",
                []
            )
    }