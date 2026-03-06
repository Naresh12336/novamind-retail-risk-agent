from engine.nlp import extract_signals
from engine.honeypot import analyze_honeypot_text
from engine.risk_model import calculate_risk
from engine.reasoning import generate_reasoning
from engine.decision_policy import decide_action
from alerts.alert_service import emit_alert
from analytics.decision_logger import log_decision
from engine.contribution import derive_contribution
from services.graph_service import update_graph
import uuid

print("PROCESSING EVENT")


def process_transaction(event: dict) -> dict:

    if "customer_id" not in event:
        raise ValueError("customer_id missing in event")

    update_graph(event)
    description = event.get("description", "")

    signals = extract_signals(description)
    honeypot = analyze_honeypot_text(description)


    score, category, confidence_score, confidence_level = calculate_risk(
        signals, honeypot, event
    )

    evidence = {
        "textual_signals": signals,
        "behavioral_signals": {
            "refund_count_last_30_days": event.get("refund_count_last_30_days", 0),
            "account_age_days": event.get("account_age_days", 0),
            "amount": event.get("amount", 0)
        },
        "honeypot_signals": honeypot
    }

    if category in ["Medium", "High"]:
        reasoning = generate_reasoning(signals, score, category)
    else:
        reasoning = "Low risk transaction based on current signals."

    contribution = derive_contribution(signals, honeypot, event)

    decision_id = str(uuid.uuid4())

    action = decide_action(category, confidence_level, score)

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
        "evidence": evidence,
        "contribution": contribution
    }

    print("DECISION:", action)

    # Persist first
    log_decision(event, result, signals, honeypot)

    print("CHECKING ALERT CONDITION")

    if action in ["Manual Review Required", "Auto Block Transaction"]:
        print("ALERT CONDITION PASSED")
        emit_alert(result, event)

    return result