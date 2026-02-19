from engine.nlp import extract_signals
from engine.honeypot import analyze_honeypot_text
from engine.risk_model import calculate_risk
from engine.reasoning import generate_reasoning
from engine.decision_policy import decide_action
from alerts.alert_service import emit_alert
from analytics.decision_logger import log_decision
from engine.contribution import derive_contribution
import uuid



def process_transaction(event: dict) -> dict:
    description = event.get("description", "")

    # --- Intelligence Extraction ---
    signals = extract_signals(description)
    honeypot = analyze_honeypot_text(description)

    # --- Risk Evaluation ---
    score, category, confidence_score, confidence_level = calculate_risk(
        signals, honeypot, event
    )

    # Evidence aggregation (single investigation object)
    evidence = {
        "textual_signals": signals,
        "behavioral_signals": {
            "refund_count_last_30_days": event.get("refund_count_last_30_days", 0),
            "account_age_days": event.get("account_age_days", 0),
            "amount": event.get("amount", 0)
        },
        "honeypot_signals": honeypot
    }

    # --- Reasoning Policy (invoke reasoning only when needed) ---
    if category in ["Medium", "High"]:
        reasoning = generate_reasoning(signals, score, category)
    else:
        reasoning = "Low risk transaction based on current signals."


    # --- Contribution Summary ---
    contribution = derive_contribution(signals, honeypot, event)

    decision_id = str(uuid.uuid4())

    # Decision layer (ONLY place action is decided)
    action = decide_action(category, confidence_level, score)

    result = {
        "decision_id": decision_id,
        "transaction_id": event.get("transaction_id"),
        "customer_id": event.get("customer_id"),
        "risk_score": score,
        "risk_category": category,
        "confidence_score": round(confidence_score, 2),
        "confidence_level": confidence_level,
        "reasoning": reasoning,
        "recommended_action": action,
        "evidence": evidence,
        "contribution": contribution
    }

    # Alert MUST depend on result, not local variables
    if result["recommended_action"] in ["Manual Review Required", "Auto Block Transaction"]:
        emit_alert(result)

    log_decision(event, result, signals, honeypot)

    return result
