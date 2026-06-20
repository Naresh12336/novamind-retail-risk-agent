from threat_intelligence.reputation_memory import (
    email_reputation
)


# ==========================================
# UPDATE EMAIL REPUTATION
# ==========================================
def update_email_reputation(
    email_hash,
    customer_id,
    result
):

    if not email_hash:
        return

    profile = email_reputation[
        email_hash
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
# EVALUATE EMAIL REPUTATION
# ==========================================
def evaluate_email_reputation(
    email_hash
):

    if not email_hash:

        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }

    profile = email_reputation.get(
        email_hash
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
    # FRAUD HEAVY EMAIL
    # ==========================
    if fraud_ratio > 0.5:

        score += 15

        signals.append(
            "fraud_heavy_email"
        )

    # ==========================
    # BLOCKED EMAIL
    # ==========================
    if block_ratio > 0.4:

        score += 15

        signals.append(
            "blocked_email"
        )

    # ==========================
    # SHARED EMAIL NETWORK
    # ==========================
    if customer_count > 3:

        score += 10

        signals.append(
            "shared_email_network"
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