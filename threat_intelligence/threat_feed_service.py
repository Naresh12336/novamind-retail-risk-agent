from threat_intelligence.ip_reputation import (
    evaluate_ip_reputation
)

from threat_intelligence.email_reputation import (
    evaluate_email_reputation
)

from threat_intelligence.device_reputation import (
    evaluate_device_reputation
)


# ==========================================
# THREAT INTELLIGENCE AGGREGATOR
# ==========================================
def evaluate_threat_intelligence(
    event
):

    ip_result = evaluate_ip_reputation(
        event.get("ip_address")
    )

    email_result = evaluate_email_reputation(
        event.get("email_hash")
    )

    device_result = evaluate_device_reputation(
        event.get("device_id")
    )

    total_score = (

        ip_result["score"]

        + email_result["score"]

        + device_result["score"]
    )

    all_signals = (

        ip_result["signals"]

        + email_result["signals"]

        + device_result["signals"]
    )

    profile = {

        "ip":
            ip_result["profile"],

        "email":
            email_result["profile"],

        "device":
            device_result["profile"]
    }

    return {

        "score":
            total_score,

        "signals":
            all_signals,

        "profile":
            profile
    }