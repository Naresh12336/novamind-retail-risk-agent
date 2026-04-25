from engine.nlp import extract_signals
from engine.adaptive_policy import adaptive_decide_action
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

from services.ato_service import (
    update_account_behavior,
    detect_account_takeover
)

from services.reputation_service import (
    get_reputation,
    get_reputation_adjustment,
    update_reputation
)

import uuid

print("PROCESSING EVENT")


def process_transaction(event: dict):

    if "customer_id" not in event:
        raise ValueError("customer_id missing in event")

    customer_id = event["customer_id"]

    # ======================================
    # GRAPH
    # ======================================
    update_graph(event)

    graph_result = get_graph_risk_score(event)

    graph_score = graph_result.get("score", 0)
    graph_signals = graph_result.get("signals", [])
    graph_clusters = graph_result.get("clusters", [])
    graph_community = graph_result.get("community")

    # ======================================
    # VELOCITY
    # ======================================
    update_velocity(event)
    velocity_clusters = detect_velocity_cluster(event)
    velocity_score = len(velocity_clusters) * 15

    # ======================================
    # ATO
    # ======================================
    update_account_behavior(event)
    ato_findings = detect_account_takeover(event)

    ato_score = 0
    for item in ato_findings:
        if item["type"] == "ACCOUNT_TAKEOVER_RISK":
            ato_score += 35
        else:
            ato_score += 15

    # ======================================
    # NLP + HONEYPOT
    # ======================================
    description = event.get("description", "")
    signals = extract_signals(description)
    honeypot = analyze_honeypot_text(description)

    # ======================================
    # BASE MODEL
    # ======================================
    infra_score = graph_score + velocity_score + ato_score

    score, category, confidence_score, confidence_level = calculate_risk(
        signals=signals,
        honeypot=honeypot,
        event=event,
        graph_signal=infra_score
    )

    # ======================================
    # REPUTATION MODIFIER
    # ======================================
    reputation_before = get_reputation(customer_id)
    rep_adjustment = get_reputation_adjustment(customer_id)

    score += rep_adjustment

    if score > 100:
        score = 100
    if score < 0:
        score = 0

    # Recalculate category
    if score >= 75:
        category = "High"
    elif score >= 40:
        category = "Medium"
    else:
        category = "Low"

    # ======================================
    # REASONING
    # ======================================
    if category in ["Medium", "High"]:
        reasoning = generate_reasoning(signals, score, category)
    else:
        reasoning = "Low risk transaction based on current signals."

    contribution = derive_contribution(signals, honeypot, event)

    decision_id = str(uuid.uuid4())
    action = adaptive_decide_action(
        score=score,
        confidence_level=confidence_level,
        event=event,
        reputation_before=reputation_before,
        graph_signals=graph_signals,
        velocity_clusters=velocity_clusters,
        ato_findings=ato_findings
    )

    print("ADAPTIVE DECISION:", action)
    print("BASE SCORE:", score)
    print("REPUTATION:", reputation_before)
    print("GRAPH SIGNAL COUNT:", len(graph_signals))
    print("VELOCITY COUNT:", len(velocity_clusters))
    print("ATO COUNT:", len(ato_findings))

    # ======================================
    # RESULT
    # ======================================
    result = {
        "decision_id": decision_id,
        "transaction_id": event.get("transaction_id"),
        "customer_id": customer_id,

        "risk_score": score,
        "risk_category": category,
        "confidence_score": round(confidence_score, 2),
        "confidence_level": confidence_level,
        "recommended_action": action,
        "reasoning": reasoning,

        "reputation_before": reputation_before,
        "reputation_adjustment": rep_adjustment,

        "graph_score": graph_score,
        "graph_signals": graph_signals,
        "graph_clusters": graph_clusters,
        "graph_community": graph_community,

        "velocity_score": velocity_score,
        "velocity_clusters": velocity_clusters,

        "ato_score": ato_score,
        "ato_findings": ato_findings,

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

    # ======================================
    # UPDATE REPUTATION AFTER DECISION
    # ======================================
    update_reputation(customer_id, result)

    print("DECISION:", action)
    print("REPUTATION BEFORE:", reputation_before)
    print("REPUTATION ADJUSTMENT:", rep_adjustment)

    log_decision(event, result, signals, honeypot)

    if action in ["Manual Review Required", "Auto Block Transaction"]:
        emit_alert(result, event)

    return result