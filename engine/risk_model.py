def calculate_risk(signals: dict, honeypot: dict, event: dict) -> tuple:
    score = 0
    signal_strength = 0

    # --- Textual signals ---
    keyword_count = signals.get("keyword_count", 0)
    urgency = signals.get("urgency_flag", False)
    text_length = signals.get("text_length", 0)

    score += keyword_count * 15
    signal_strength += keyword_count

    if urgency:
        score += 20
        signal_strength += 1

    if text_length < 20:
        score += 10

    # --- Honeypot signals ---
    tactic_count = honeypot.get("tactic_count", 0)
    score += tactic_count * 20
    signal_strength += tactic_count

    # --- Behavioral signals ---
    refund_count = event.get("refund_count_last_30_days", 0)
    account_age = event.get("account_age_days", 0)
    amount = event.get("amount", 0)

    behavioral_hits = 0

    if refund_count > 3:
        score += 25
        behavioral_hits += 1

    if account_age < 7:
        score += 20
        behavioral_hits += 1

    if amount > 2000:
        score += 15
        behavioral_hits += 1

    signal_strength += behavioral_hits

    score = min(score, 100)

    # --- Category ---
    if score >= 60:
        category = "High"
    elif score >= 30:
        category = "Medium"
    else:
        category = "Low"

    # --- Confidence Calculation ---
    # Normalize signal strength
    # --- Quantitative Confidence ---
    # --- Dimension-Based Confidence ---
    # --- Weighted Confidence Calculation ---

    # Normalize each dimension to [0,1]
    textual_score = min((keyword_count * 0.2) + (0.3 if urgency else 0), 1.0)
    honeypot_score = min(tactic_count * 0.3, 1.0)
    behavioral_score = min(behavioral_hits * 0.4, 1.0)

    # Weighted aggregation
    confidence_score = (
            0.35 * textual_score +
            0.30 * honeypot_score +
            0.35 * behavioral_score
    )

    confidence_score = round(confidence_score, 2)

    if confidence_score >= 0.75:
        confidence_level = "High"
    elif confidence_score >= 0.4:
        confidence_level = "Medium"
    else:
        confidence_level = "Low"

    return score, category, confidence_score, confidence_level

