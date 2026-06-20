from threat_intelligence.reputation_memory import (
    device_reputation
)


# ==========================================
# UPDATE DEVICE REPUTATION
# ==========================================
def update_device_reputation(
    device_id,
    customer_id,
    result
):

    if not device_id:
        return

    profile = device_reputation[
        device_id
    ]

    profile[
        "total_transactions"
    ] += 1

    profile[
        "linked_customers"
    ].add(customer_id)

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


# ==========================================
# EVALUATE DEVICE REPUTATION
# ==========================================
def evaluate_device_reputation(
    device_id
):

    if not device_id:

        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }

    profile = device_reputation.get(
        device_id
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

    score = 0
    signals = []

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

    # ==========================
    # FRAUD HEAVY DEVICE
    # ==========================
    if fraud_ratio > 0.5:

        score += 18

        signals.append(
            "fraud_heavy_device"
        )

    # ==========================
    # BLOCKED DEVICE
    # ==========================
    if block_ratio > 0.4:

        score += 18

        signals.append(
            "blocked_device"
        )

    # ==========================
    # SHARED DEVICE NETWORK
    # ==========================
    if customer_count > 3:

        score += 12

        signals.append(
            "shared_device_network"
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