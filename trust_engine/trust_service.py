from trust_engine.trust_scoring import (
    get_trust_score
)


# ==========================================
# EVALUATE TRUST
# ==========================================
def evaluate_trust(
    event
):

    customer_score = (
        get_trust_score(
            f"customer:"
            f"{event.get('customer_id')}"
        )
    )

    ip_score = (
        get_trust_score(
            f"ip:"
            f"{event.get('ip_address')}"
        )
    )

    device_score = (
        get_trust_score(
            f"device:"
            f"{event.get('device_id')}"
        )
    )

    email_score = (
        get_trust_score(
            f"email:"
            f"{event.get('email_hash')}"
        )
    )

    average_trust = (

        customer_score

        + ip_score

        + device_score

        + email_score

    ) / 4

    trust_penalty = 0

    signals = []

    if average_trust < 20:

        trust_penalty = 35

        signals.append(
            "critical_trust_network"
        )

    elif average_trust < 35:

        trust_penalty = 20

        signals.append(
            "low_trust_network"
        )

    elif average_trust < 50:

        trust_penalty = 10

        signals.append(
            "degrading_trust"
        )

    return {

        "score":
            trust_penalty,

        "signals":
            signals,

        "average_trust":
            round(
                average_trust,
                2
            ),

        "entities": {

            "customer":
                customer_score,

            "ip":
                ip_score,

            "device":
                device_score,

            "email":
                email_score
        }
    }