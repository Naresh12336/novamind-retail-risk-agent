def derive_contribution(signals: dict, honeypot: dict, event: dict) -> dict:
    keyword_count = signals.get("keyword_count", 0)
    urgency = signals.get("urgency_flag", False)
    tactic_count = honeypot.get("tactic_count", 0)

    refund_count = event.get("refund_count_last_30_days", 0)
    account_age = event.get("account_age_days", 0)
    amount = event.get("amount", 0)

    factors = []

    # Behavioral abuse
    if refund_count > 3:
        factors.append("repeat_refund_behavior")

    if account_age < 7:
        factors.append("new_account_risk")

    if amount > 2000:
        factors.append("high_value_transaction")

    # Adversarial communication
    if tactic_count >= 2:
        factors.append("pressure_or_threat_language")

    # Linguistic suspicion
    if keyword_count >= 2 or urgency:
        factors.append("suspicious_language_pattern")

    # Low information content
    if signals.get("text_length", 100) < 6:
        factors.append("low_context_description")

    # Rank importance
    if not factors:
        return {
            "primary_factor": "normal_behavior",
            "secondary_factor": None,
            "supporting_factor": None
        }

    primary = factors[0]
    secondary = factors[1] if len(factors) > 1 else None
    supporting = factors[2] if len(factors) > 2 else None

    return {
        "primary_factor": primary,
        "secondary_factor": secondary,
        "supporting_factor": supporting
    }
