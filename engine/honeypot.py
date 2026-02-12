SCAM_TACTIC_PATTERNS = {
    "refund_abuse": ["refund", "already refunded", "reimburse"],
    "urgency_pressure": ["urgent", "immediately", "now", "asap"],
    "threat_language": ["lawsuit", "legal action", "complaint"],
}

def analyze_honeypot_text(text: str) -> dict:
    """
    Passive analysis of scam-like language patterns.
    No interaction. No response generation.
    """

    text_lower = text.lower()
    detected_tactics = []

    for tactic, patterns in SCAM_TACTIC_PATTERNS.items():
        for p in patterns:
            if p in text_lower:
                detected_tactics.append(tactic)
                break

    return {
        "detected_tactics": list(set(detected_tactics)),
        "tactic_count": len(set(detected_tactics))
    }
