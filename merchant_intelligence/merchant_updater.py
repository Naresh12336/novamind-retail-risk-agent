from merchant_intelligence.merchant_reputation_service import (
    merchant_profiles
)

from config.fraud_policy import (
    INITIAL_MERCHANT_TRUST,
    MERCHANT_REWARD,
    MERCHANT_PENALTY
)


# ==========================================
# MERCHANT PROFILE UPDATE
# ==========================================
def update_merchant_profile(
    event: dict,
    result: dict
):

    merchant_id = event.get(
        "merchant_id"
    )

    if not merchant_id:
        return

    profile = merchant_profiles[
        merchant_id
    ]

    # ======================================
    # BASIC STATISTICS
    # ======================================
    profile[
        "total_transactions"
    ] += 1

    amount = event.get(
        "amount",
        0
    )

    total = profile[
        "total_transactions"
    ]

    previous_average = profile[
        "average_order_value"
    ]

    profile[
        "average_order_value"
    ] = (

        (
            previous_average
            * (total - 1)
        )

        + amount

    ) / total

    # ======================================
    # HIGH RISK
    # ======================================
    if (
        result.get(
            "risk_category"
        )
        == "High"
    ):

        profile[
            "high_risk_transactions"
        ] += 1

    # ======================================
    # BLOCKED
    # ======================================
    if (
        result.get(
            "recommended_action"
        )
        == "Auto Block Transaction"
    ):

        profile[
            "blocked_transactions"
        ] += 1

    # ======================================
    # REFUND EVENTS
    # ======================================
    if event.get(
        "transaction_type"
    ) in (

        "refund",

        "refund_request"

    ):

        profile[
            "refund_events"
        ] += 1

    # ======================================
    # CHARGEBACK EVENTS
    # ======================================
    if event.get(
        "chargeback",
        False
    ):

        profile[
            "chargeback_events"
        ] += 1

    # ======================================
    # LINKED FRAUD ENTITIES
    # ======================================
    if (
        result.get(
            "risk_category"
        )
        == "High"
    ):

        customer = event.get(
            "customer_id"
        )

        if customer:

            profile[
                "linked_fraud_customers"
            ].add(customer)

        device = event.get(
            "device_id"
        )

        if device:

            profile[
                "linked_fraud_devices"
            ].add(device)

        payment = event.get(
            "payment_method_hash"
        )

        if payment:

            profile[
                "linked_fraud_cards"
            ].add(payment)

    # ======================================
    # TRUST UPDATE
    # ======================================
    trust = profile.get(
        "trust_score",
        INITIAL_MERCHANT_TRUST
    )

    if (
        result.get(
            "risk_category"
        )
        == "High"
    ):

        trust -= MERCHANT_PENALTY

    else:

        trust += MERCHANT_REWARD

    profile[
        "trust_score"
    ] = max(
        0,
        min(100, trust)
    )