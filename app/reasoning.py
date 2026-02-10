def generate_reasoning(signals: dict, score: int, category: str) -> str:
    """
    Generates an explanation for the risk decision.
    If Amazon Nova is available, it should be used here.
    Otherwise, fall back to deterministic reasoning.
    """

    try:
        # --- PLACEHOLDER FOR AMAZON NOVA CALL ---
        # Example (pseudo-code):
        #
        # response = nova_client.generate(
        #     prompt=formatted_prompt,
        #     model="amazon-nova-reasoning"
        # )
        # return response.text
        #
        # ----------------------------------------

        raise NotImplementedError("Nova not configured")

    except Exception:
        # Deterministic fallback (guaranteed)
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

        if honeypot := signals.get("honeypot_tactics"):
            reasons.append(
                f"Observed scam tactics similar to known abuse patterns: {honeypot}."
            )

        if not reasons:
            reasons.append(
                "No strong scam indicators were detected in the transaction text."
            )

        return (
            f"Based on the analysis, the transaction is classified as {category} risk "
            f"with a score of {score}. " + " ".join(reasons)
        )
