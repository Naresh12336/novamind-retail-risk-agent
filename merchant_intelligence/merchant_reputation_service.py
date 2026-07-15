from collections import defaultdict

from config.fraud_policy import (
    INITIAL_MERCHANT_TRUST,
    LOW_MERCHANT_TRUST,
    CRITICAL_MERCHANT_TRUST,
    MERCHANT_MIN_TRANSACTIONS,
    HIGH_CHARGEBACK_RATIO,
    HIGH_REFUND_RATIO
)

# ==========================================
# MERCHANT MEMORY STORE
# ==========================================
merchant_profiles = defaultdict(
    lambda: {
        "total_transactions": 0,
        "high_risk_transactions": 0,
        "blocked_transactions": 0,
        "refund_events": 0,
        "chargeback_events": 0,
        "average_order_value": 0.0,
        "trust_score": INITIAL_MERCHANT_TRUST,
        "linked_fraud_customers": set(),
        "linked_fraud_devices": set(),
        "linked_fraud_cards": set()
    }
)


# ==========================================
# MERCHANT RISK EVALUATION
# ==========================================
def evaluate_merchant_risk(
    merchant_id
):

    if not merchant_id:

        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }

    profile = merchant_profiles[
        merchant_id
    ]

    signals = []

    score = 0

    total = max(
        profile["total_transactions"],
        1
    )

    # --------------------------------------
    # NEW MERCHANT
    # --------------------------------------
    if (
        profile["total_transactions"]
        < MERCHANT_MIN_TRANSACTIONS
    ):

        signals.append(
            "new_merchant"
        )

    # --------------------------------------
    # FRAUD RATIO
    # --------------------------------------
    fraud_ratio = (

        profile[
            "high_risk_transactions"
        ]

        / total

    )

    if fraud_ratio >= 0.40:

        score += 30

        signals.append(
            "fraud_heavy_merchant"
        )

    elif fraud_ratio >= 0.20:

        score += 15

        signals.append(
            "moderate_fraud_history"
        )

    # --------------------------------------
    # BLOCK RATIO
    # --------------------------------------
    block_ratio = (

        profile[
            "blocked_transactions"
        ]

        / total

    )

    if block_ratio >= 0.30:

        score += 25

        signals.append(
            "high_block_rate"
        )

    elif block_ratio >= 0.15:

        score += 10

        signals.append(
            "moderate_block_rate"
        )

    # --------------------------------------
    # REFUND RATIO
    # --------------------------------------
    refund_ratio = (

        profile[
            "refund_events"
        ]

        / total

    )

    if refund_ratio >= HIGH_REFUND_RATIO:

        score += 15

        signals.append(
            "high_refund_rate"
        )

    # --------------------------------------
    # CHARGEBACK RATIO
    # --------------------------------------
    chargeback_ratio = (

        profile[
            "chargeback_events"
        ]

        / total

    )

    if chargeback_ratio >= HIGH_CHARGEBACK_RATIO:

        score += 20

        signals.append(
            "high_chargeback_rate"
        )

    # --------------------------------------
    # CONTINUOUS TRUST PENALTY
    # --------------------------------------
    trust = profile[
        "trust_score"
    ]

    trust_penalty = max(
        0,
        (
            INITIAL_MERCHANT_TRUST
            - trust
        ) // 2
    )

    score += int(
        trust_penalty
    )

    if trust <= CRITICAL_MERCHANT_TRUST:

        signals.append(
            "critical_merchant_trust"
        )

    elif trust <= LOW_MERCHANT_TRUST:

        signals.append(
            "low_merchant_trust"
        )

    # --------------------------------------
    # CAP SCORE
    # --------------------------------------
    score = min(
        score,
        100
    )

    # --------------------------------------
    # SERIALIZABLE PROFILE
    # --------------------------------------
    serializable_profile = {

        **profile,

        "linked_fraud_customers": list(
            profile[
                "linked_fraud_customers"
            ]
        ),

        "linked_fraud_devices": list(
            profile[
                "linked_fraud_devices"
            ]
        ),

        "linked_fraud_cards": list(
            profile[
                "linked_fraud_cards"
            ]
        )

    }

    return {

        "score": score,

        "signals": signals,

        "profile": serializable_profile

    }