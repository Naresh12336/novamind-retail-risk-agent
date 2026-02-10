def generate_reasoning(signals: dict, score: int, category: str) -> str:
    """
    This function will later call Amazon Nova.
    For now, it returns a structured reasoning template.
    """

    reasons = []

    if signals.get("keyword_count", 0) > 0:
        reasons.append(
            f"{signals['keyword_count']} risk-related keywords were detected."
        )

    if signals.get("urgency_flag"):
        reasons.append("Urgent language patterns were observed.")

    if signals.get("text_length", 0) < 20:
        reasons.append(
            "The transaction description is brief, increasing uncertainty."
        )

    if not reasons:
        reasons.append(
            "No strong scam indicators were detected in the transaction text."
        )

    reasoning_text = (
        f"Based on the analysis, the transaction is classified as {category} risk "
        f"with a score of {score}. "
        + " ".join(reasons)
    )

    return reasoning_text
