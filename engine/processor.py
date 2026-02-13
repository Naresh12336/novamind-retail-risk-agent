from engine.nlp import extract_signals
from engine.honeypot import analyze_honeypot_text
from engine.risk_model import calculate_risk
from engine.reasoning import generate_reasoning
from engine.decision_policy import decide_action
from alerts.alert_service import emit_alert


def process_transaction(event: dict) -> dict:
    description = event.get("description", "")

    # --- Intelligence Extraction ---
    signals = extract_signals(description)
    honeypot = analyze_honeypot_text(description)

    # --- Risk Evaluation ---
    score, category, confidence_score, confidence_level = calculate_risk(
        signals, honeypot, event
    )

    # --- Reasoning Policy (invoke reasoning only when needed) ---
    if category in ["Medium", "High"]:
        reasoning = generate_reasoning(signals, score, category)
    else:
        reasoning = "Low risk transaction based on current signals."

    # --- Decision Policy ---
    action = decide_action(category, confidence_level)

    # --- Response Object ---
    result = {
        "transaction_id": event.get("transaction_id"),
        "risk_score": score,
        "risk_category": category,
        "confidence_score": round(confidence_score, 2),
        "confidence_level": confidence_level,
        "reasoning": reasoning,
        "recommended_action": action,
    }

    # --- Alert Routing ---
    if category == "High" and confidence_level in ["High", "Medium"]:
        emit_alert(result)

    return result
