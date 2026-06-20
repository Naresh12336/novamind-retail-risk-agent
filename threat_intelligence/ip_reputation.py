from threat_intelligence.reputation_memory import (
    ip_reputation
)


def update_ip_reputation(
    ip_address,
    customer_id,
    result
):

    if not ip_address:
        return

    profile = ip_reputation[ip_address]

    profile["total_transactions"] += 1

    profile["linked_customers"].add(
        customer_id
    )

    if result.get(
        "risk_category"
    ) == "High":

        profile[
            "high_risk_transactions"
        ] += 1

    if result.get(
        "recommended_action"
    ) == "Auto Block Transaction":

        profile[
            "blocked_transactions"
        ] += 1


def evaluate_ip_reputation(
    ip_address
):

    if not ip_address:

        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }

    profile = ip_reputation.get(
        ip_address
    )

    if not profile:

        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }

    total = profile[
        "total_transactions"
    ]

    if total < 3:

        return {
            "score": 0,
            "signals": [],
            "profile": profile
        }

    signals = []

    score = 0

    fraud_ratio = (
        profile[
            "high_risk_transactions"
        ] / total
    )

    block_ratio = (
        profile[
            "blocked_transactions"
        ] / total
    )

    customer_count = len(
        profile[
            "linked_customers"
        ]
    )

    if fraud_ratio > 0.5:

        score += 15

        signals.append(
            "fraud_heavy_ip"
        )

    if block_ratio > 0.4:

        score += 15

        signals.append(
            "blocked_ip"
        )

    if customer_count > 5:

        score += 10

        signals.append(
            "shared_ip_network"
        )

    return {

        "score": score,

        "signals": signals,

        "profile": {
            **profile,
            "linked_customers":
                customer_count
        }
    }