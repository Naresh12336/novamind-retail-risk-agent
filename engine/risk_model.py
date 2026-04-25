# risk_model.py

def calculate_risk(
    signals: dict,
    honeypot: dict,
    event: dict,
    graph_signal=None,
    graph_score=0
):
    """
    Enterprise fraud scoring engine.

    Inputs:
        NLP signals
        Honeypot tactics
        Behavioral data
        Graph intelligence

    Returns:
        score, category, confidence_score, confidence_level
    """

    score = 0

    # ==================================================
    # NLP SIGNALS
    # ==================================================
    keyword_count = signals.get("keyword_count", 0)
    urgency_flag = signals.get("urgency_flag", False)
    text_length = signals.get("text_length", 0)

    score += min(keyword_count * 6, 24)

    if urgency_flag:
        score += 12

    if text_length <= 3:
        score += 6

    # ==================================================
    # HONEYPOT SIGNALS
    # ==================================================
    tactic_count = honeypot.get("tactic_count", 0)

    score += min(tactic_count * 8, 24)

    # ==================================================
    # BEHAVIORAL SIGNALS
    # ==================================================
    refund_count = event.get("refund_count_last_30_days", 0)
    account_age = event.get("account_age_days", 9999)
    amount = event.get("amount", 0)

    # refund abuse
    if refund_count >= 7:
        score += 28
    elif refund_count >= 5:
        score += 20
    elif refund_count >= 3:
        score += 12

    # new account risk
    if account_age <= 7:
        score += 20
    elif account_age <= 14:
        score += 12
    elif account_age <= 30:
        score += 6

    # suspicious transaction amount
    if amount >= 500:
        score += 12
    elif amount >= 250:
        score += 7
    elif amount >= 150:
        score += 4

    # ==================================================
    # GRAPH INTELLIGENCE
    # ==================================================
    score += graph_score

    # bonus if community detected
    if graph_signal == "fraud_network_community":
        score += 10

    # ==================================================
    # CAP SCORE
    # ==================================================
    score = min(score, 100)

    # ==================================================
    # CATEGORY
    # ==================================================
    if score >= 75:
        category = "High"
    elif score >= 45:
        category = "Medium"
    else:
        category = "Low"

    # ==================================================
    # CONFIDENCE SCORE
    # ==================================================
    confidence_score = 0.35

    confidence_score += min(keyword_count * 0.04, 0.16)

    if urgency_flag:
        confidence_score += 0.08

    confidence_score += min(tactic_count * 0.05, 0.15)

    if refund_count >= 5:
        confidence_score += 0.10

    if account_age <= 14:
        confidence_score += 0.08

    if graph_score >= 20:
        confidence_score += 0.10

    if graph_score >= 40:
        confidence_score += 0.08

    if graph_signal == "fraud_network_community":
        confidence_score += 0.05

    confidence_score = round(min(confidence_score, 0.99), 2)

    # ==================================================
    # CONFIDENCE LEVEL
    # ==================================================
    if confidence_score >= 0.75:
        confidence_level = "High"
    elif confidence_score >= 0.55:
        confidence_level = "Medium"
    else:
        confidence_level = "Low"

    return score, category, confidence_score, confidence_level