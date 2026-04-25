def adaptive_decide_action(
    score: int,
    confidence_level: str,
    event: dict,
    reputation_before: int,
    graph_signals: list,
    velocity_clusters: list,
    ato_findings: list
):
    """
    Context-aware fraud decision engine
    """

    block_threshold = 75
    review_threshold = 40
    verify_threshold = 30

    # ======================================
    # CUSTOMER REPUTATION
    # ======================================
    if reputation_before <= 30:
        block_threshold -= 10
        review_threshold -= 8
        verify_threshold -= 5

    elif reputation_before >= 75:
        block_threshold += 10
        review_threshold += 8

    # ======================================
    # TRANSACTION TYPE
    # ======================================
    tx_type = str(event.get("transaction_type", "")).lower()

    if "refund" in tx_type:
        block_threshold -= 8
        review_threshold -= 5

    # ======================================
    # HIGH VALUE TRANSACTION
    # ======================================
    amount = float(event.get("amount", 0))

    if amount >= 500:
        block_threshold -= 8
        review_threshold -= 5

    elif amount >= 250:
        block_threshold -= 4
        review_threshold -= 3

    # ======================================
    # NEW ACCOUNT RISK
    # ======================================
    age = int(event.get("account_age_days", 0))

    if age <= 7:
        block_threshold -= 8
        review_threshold -= 5

    elif age <= 30:
        block_threshold -= 4

    # ======================================
    # STRONG INFRA SIGNALS
    # ======================================
    if graph_signals:
        block_threshold -= min(12, len(graph_signals) * 3)

    if velocity_clusters:
        block_threshold -= 10
        review_threshold -= 5

    if ato_findings:
        block_threshold -= 15
        review_threshold -= 10

    # safety floor
    block_threshold = max(35, block_threshold)
    review_threshold = max(20, review_threshold)
    verify_threshold = max(10, verify_threshold)

    # ======================================
    # FINAL DECISION
    # ======================================
    if score >= block_threshold:
        return "Auto Block Transaction"

    if score >= review_threshold:
        if confidence_level == "High":
            return "Manual Review Required"
        return "Request Customer Verification"

    if score >= verify_threshold:
        return "Request Customer Verification"

    return "Allow Transaction"