# processor.py

from engine.nlp import extract_signals
from engine.honeypot import analyze_honeypot_text
from engine.risk_model import calculate_risk
from engine.reasoning import generate_reasoning
from engine.decision_policy import decide_action
from alerts.alert_service import emit_alert
from analytics.decision_logger import log_decision
from engine.contribution import derive_contribution

from services.graph_service import (
    update_graph,
    get_graph_risk_score
)

import uuid

print("PROCESSING EVENT")


def process_transaction(event: dict) -> dict:

    if "customer_id" not in event:
        raise ValueError("customer_id missing in event")

    # ==================================================
    # STEP 1 — UPDATE GRAPH MEMORY
    # ==================================================
    update_graph(event)

    # ==================================================
    # STEP 2 — GET GRAPH INTELLIGENCE
    # ==================================================
    graph_result = get_graph_risk_score(event)

    graph_signals = graph_result["signals"]
    graph_score = graph_result["score"]
    graph_clusters = graph_result["clusters"]
    graph_community = graph_result["community"]

    # backward compatibility single label
    graph_signal = graph_signals[0] if graph_signals else None

    # ==================================================
    # STEP 3 — NLP SIGNALS
    # ==================================================
    description = event.get("description", "")

    signals = extract_signals(description)
    honeypot = analyze_honeypot_text(description)

    # ==================================================
    # STEP 4 — RISK MODEL
    # ==================================================
    score, category, confidence_score, confidence_level = calculate_risk(
        signals=signals,
        honeypot=honeypot,
        event=event,
        graph_signal=graph_signal,
        graph_score=graph_score
    )

    # ==================================================
    # STEP 5 — REASONING
    # ==================================================
    if category in ["Medium", "High"]:
        reasoning = generate_reasoning(signals, score, category)
    else:
        reasoning = "Low risk transaction based on current signals."

    # ==================================================
    # STEP 6 — CONTRIBUTION
    # ==================================================
    contribution = derive_contribution(signals, honeypot, event)

    # ==================================================
    # STEP 7 — DECISION
    # ==================================================
    action = decide_action(category, confidence_level, score)

    result = {
        "decision_id": str(uuid.uuid4()),
        "transaction_id": event.get("transaction_id"),
        "customer_id": event.get("customer_id"),

        "risk_score": score,
        "risk_category": category,
        "confidence_score": round(confidence_score, 2),
        "confidence_level": confidence_level,

        "recommended_action": action,
        "reasoning": reasoning,

        # graph outputs
        "graph_signal": graph_signal,
        "graph_signals": graph_signals,
        "graph_score": graph_score,

        "evidence": {
            "textual_signals": signals,
            "behavioral_signals": {
                "refund_count_last_30_days": event.get(
                    "refund_count_last_30_days", 0
                ),
                "account_age_days": event.get(
                    "account_age_days", 0
                ),
                "amount": event.get("amount", 0)
            },
            "honeypot_signals": honeypot,
            "graph": {
                "signals": graph_signals,
                "score": graph_score,
                "clusters": graph_clusters,
                "community": graph_community
            }
        },

        "contribution": contribution
    }

    print("DECISION:", action)

    # ==================================================
    # STEP 8 — LOGGING
    # ==================================================
    log_decision(event, result, signals, honeypot)

    # ==================================================
    # STEP 9 — ALERTING
    # ==================================================
    print("CHECKING ALERT CONDITION")

    if action in ["Manual Review Required", "Auto Block Transaction"]:
        print("ALERT CONDITION PASSED")
        emit_alert(result, event)

    # ==================================================
    # DEBUG TERMINAL VISIBILITY
    # ==================================================
    print("GRAPH SIGNALS:", graph_signals)
    print("GRAPH SCORE:", graph_score)
    print("GRAPH CLUSTERS:", graph_clusters)
    print("GRAPH COMMUNITY:", graph_community)

    return result