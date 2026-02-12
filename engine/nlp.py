import re
from collections import Counter

SCAM_KEYWORDS = [
    "urgent", "refund", "chargeback", "immediately", "fraud",
    "fake", "complaint", "threat", "lawsuit", "cancel", "return"
]

def extract_signals(text: str) -> dict:
    text_lower = text.lower()

    # Keyword hits
    keyword_hits = [kw for kw in SCAM_KEYWORDS if kw in text_lower]

    # Urgency patterns
    urgency_flag = bool(re.search(r"\b(urgent|immediately|asap|now)\b", text_lower))

    # Length-based heuristic
    text_length = len(text.split())

    return {
        "keyword_hits": keyword_hits,
        "keyword_count": len(keyword_hits),
        "urgency_flag": urgency_flag,
        "text_length": text_length
    }
