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

from services.velocity_service import (
    update_velocity,
    detect_velocity_cluster
)

import uuid

print("PROCESSING EVENT")


def process_transaction(event: dict) -> dict:

    if "customer_id" not in event:
        raise ValueError("customer_id missing in event")

    # =====================================
    # GRAPH INTELLIGENCE
    # =====================================
    update_graph(event)
    graph_result = get_graph_risk_score(event)

    graph_score = graph_result["score"]
    graph_signals = graph_result["signals"]

    # =====================================
    # VELOCITY INTELLIGENCE
    # =====================================
    update_velocity(event)
    velocity_clusters = detect_velocity_cluster(event)

    velocity_score = 0

    if velocity_clusters:
        velocity_score = len(velocity_clusters) * 15

    # =====================================
    # NLP + HONEYPOT
    # =====================================
    description = event.get("description", "")

    signals = extract_signals(description)
    honeypot = analyze_honeypot_text(description)

    # =====================================
    # RISK MODEL
    # =====================================
    score, category, confidence_score, confidence_level = calculate_risk(
        signals=signals,
        honeypot=honeypot,
        event=event,
        graph_signal=graph_score + velocity_score
    )

    # =====================================
    # REASONING
    # =====================================
    if category in ["Medium", "High"]:
        reasoning = generate_reasoning(signals, score, category)
    else:
        reasoning = "Low risk transaction based on current signals."

    # =====================================
    # CONTRIBUTION
    # =====================================
    contribution = derive_contribution(signals, honeypot, event)

    decision_id = str(uuid.uuid4())
    action = decide_action(category, confidence_level, score)

    # =====================================
    # RESULT
    # =====================================
    result = {
        "decision_id": decision_id,
        "transaction_id": event.get("transaction_id"),
        "customer_id": event.get("customer_id"),

        "risk_score": score,
        "risk_category": category,
        "confidence_score": round(confidence_score, 2),
        "confidence_level": confidence_level,
        "recommended_action": action,
        "reasoning": reasoning,

        "graph_score": graph_score,
        "graph_signals": graph_signals,

        "velocity_score": velocity_score,
        "velocity_clusters": velocity_clusters,

        "evidence": {
            "textual_signals": signals,
            "honeypot_signals": honeypot,
            "behavioral_signals": {
                "refund_count_last_30_days": event.get("refund_count_last_30_days", 0),
                "account_age_days": event.get("account_age_days", 0),
                "amount": event.get("amount", 0)
            }
        },

        "contribution": contribution
    }

    print("DECISION:", action)
    print("GRAPH SCORE:", graph_score)
    print("VELOCITY SCORE:", velocity_score)
    print("VELOCITY CLUSTERS:", velocity_clusters)

    # =====================================
    # LOGGING
    # =====================================
    log_decision(event, result, signals, honeypot)

    # =====================================
    # ALERTING
    # =====================================
    if action in ["Manual Review Required", "Auto Block Transaction"]:
        emit_alert(result, event)

    return result