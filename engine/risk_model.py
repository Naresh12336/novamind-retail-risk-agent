def calculate_risk(signals: dict, honeypot: dict) -> tuple:
    score = 0

    # Keyword-based risk
    score += signals.get("keyword_count", 0) * 15

    # Urgency signal
    if signals.get("urgency_flag"):
        score += 25

    # Short vague descriptions increase uncertainty
    if signals.get("text_length", 0) < 20:
        score += 10

    # Honeypot intelligence boost
    score += honeypot.get("tactic_count", 0) * 20

    # Cap score
    score = min(score, 100)

    if score >= 60:
        category = "High"
    elif score >= 30:
        category = "Medium"
    else:
        category = "Low"

    return score, category
