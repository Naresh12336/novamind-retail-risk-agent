# ==========================================
# ML DECISION POLICY
# ==========================================

def apply_ml_policy(result: dict):

    # ======================================
    # CURRENT DECISION
    # ======================================
    original_action = result.get(
        "recommended_action",
        "Allow Transaction"
    )

    action = original_action

    risk = result.get(
        "risk_category",
        "Low"
    )

    # ======================================
    # ML
    # ======================================
    ml_prediction = result.get(
        "ml_prediction",
        0
    )

    ml_probability = result.get(
        "ml_probability",
        0.0
    )

    # ======================================
    # INFRASTRUCTURE INTELLIGENCE
    # ======================================
    graph_score = result.get(
        "graph_score",
        0
    )

    velocity_score = result.get(
        "velocity_score",
        0
    )

    ato_score = result.get(
        "ato_score",
        0
    )

    geo_score = result.get(
        "geo_score",
        0
    )

    asn_score = result.get(
        "asn_score",
        0
    )

    threat_score = result.get(
        "threat_score",
        0
    )

    trust_score = result.get(
        "trust_score",
        0
    )

    infra_score = result.get(
        "infrastructure_score",
        0
    )

    # ======================================
    # DECISION POLICY
    # ======================================

    # --------------------------
    # STRONG INFRASTRUCTURE
    # --------------------------
    if infra_score >= 60:

        if action in [

            "Allow Transaction",

            "Monitor Activity"

        ]:

            action = (
                "Manual Review Required"
            )

    # --------------------------
    # EXTREME ML CONFIDENCE
    # --------------------------
    if (

        ml_prediction == 1

        and

        ml_probability >= 0.98

    ):

        if infra_score >= 40:

            action = (
                "Auto Block Transaction"
            )

        elif action == (
            "Allow Transaction"
        ):

            action = (
                "Manual Review Required"
            )

    # --------------------------
    # HIGH ML CONFIDENCE
    # --------------------------
    elif (

        ml_prediction == 1

        and

        ml_probability >= 0.90

    ):

        if action == (
            "Allow Transaction"
        ):

            action = (
                "Request Customer Verification"
            )

    # --------------------------
    # VERY LOW ML FRAUD
    # --------------------------
    elif (

        ml_prediction == 0

        and

        ml_probability <= 0.20

    ):

        if (

            risk == "Medium"

            and

            infra_score < 20

            and

            action == (
                "Manual Review Required"
            )

        ):

            action = (
                "Monitor Activity"
            )

    # ======================================
    # SAVE DECISION
    # ======================================
    result[
        "original_recommended_action"
    ] = original_action

    result[
        "recommended_action"
    ] = action

    result[
        "ml_decision_override"
    ] = (

        original_action != action

    )

    result[
        "infrastructure_score"
    ] = infra_score

    return result