from engine.nlp import extract_signals
from engine.honeypot import analyze_honeypot_text
from engine.risk_model import calculate_risk
from engine.reasoning import generate_reasoning
from alerts.alert_service import emit_alert



def get_action(category: str) -> str:
    if category == "High":
        return "Manual Review Required"
    elif category == "Medium":
        return "Additional Verification Needed"
    else:
        return "Approve"


def process_transaction(event: dict) -> dict:
    description = event.get("description", "")

    # Intelligence layers
    signals = extract_signals(description)
    honeypot = analyze_honeypot_text(description)

    # Risk scoring
    score, category = calculate_risk(signals, honeypot)

    # Controlled Nova invocation policy
    if category in ["Medium", "High"]:
        reasoning = generate_reasoning(signals, score, category)
    else:
        reasoning = "Low risk transaction based on current signals."

    action = get_action(category)

    result = {
        "transaction_id": event.get("transaction_id"),
        "risk_score": score,
        "risk_category": category,
        "reasoning": reasoning,
        "recommended_action": action,
    }

    if category == "High":
        emit_alert(result)

    return result
