# processor.py

from engine.nlp import extract_signals
from engine.honeypot import analyze_honeypot_text
from engine.risk_model import calculate_risk
from engine.reasoning import generate_reasoning
from engine.decision_policy import decide_action
from alerts.alert_service import emit_alert
from analytics.decision_logger import log_decision
from engine.contribution import derive_contribution

# SINGLE SOURCE OF TRUTH
from services.graph_service import (
    update_graph,
    detect_graph_cluster,
    get_graph_risk_signal,
    detect_fraud_community
)

import uuid

print("PROCESSING EVENT")


def process_transaction(event: dict) -> dict:

    if "customer_id" not in event:
        raise ValueError("customer_id missing in event")

    # =====================================
    # GRAPH LAYER
    # =====================================
    update_graph(event)

    graph_cluster = detect_graph_cluster(event)
    graph_community = detect_fraud_community(event.get("customer_id"))

    graph_signal = get_graph_risk_signal(event)

    if graph_community:
        graph_signal = "fraud_network_community"
    elif graph_cluster:
        graph_signal = graph_cluster["type"].lower()

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
        signals, honeypot, event, graph_signal
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

    # =====================================
    # DECISION
    # =====================================
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
        "graph_signal": graph_signal,
        "evidence": {
            "textual_signals": signals,
            "behavioral_signals": {
                "refund_count_last_30_days": event.get("refund_count_last_30_days", 0),
                "account_age_days": event.get("account_age_days", 0),
                "amount": event.get("amount", 0)
            },
            "honeypot_signals": honeypot,
            "graph": {
                "cluster": graph_cluster,
                "community": graph_community
            }
        },
        "contribution": contribution
    }

    print("DECISION:", action)

    log_decision(event, result, signals, honeypot)

    print("CHECKING ALERT CONDITION")

    if action in ["Manual Review Required", "Auto Block Transaction"]:
        print("ALERT CONDITION PASSED")
        emit_alert(result, event)

    print("GRAPH SIGNAL:", graph_signal)
    print("GRAPH CLUSTER:", graph_cluster)
    print("GRAPH COMMUNITY:", graph_community)

    return result