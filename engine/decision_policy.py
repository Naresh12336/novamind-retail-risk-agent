from config.fraud_policy import (
    AUTO_BLOCK_SCORE,
    STEP_UP_SCORE,
    CUSTOMER_VERIFICATION_SCORE
)

# ==========================================
# DECISION POLICY
# ==========================================
def decide_action(
    risk_category: str,
    confidence: str,
    score: int
) -> str:

    # ======================================
    # HIGH RISK
    # ======================================
    if risk_category == "High":

        if score >= AUTO_BLOCK_SCORE:
            return "Auto Block Transaction"

        elif confidence == "High":
            return "Manual Review Required"

        elif confidence == "Medium":
            return "Request Customer Verification"

        else:
            return "Monitor Activity"

    # ======================================
    # MEDIUM RISK
    # ======================================
    elif risk_category == "Medium":

        if (
            score >= STEP_UP_SCORE
            and confidence == "High"
        ):
            return "Step-Up Authentication"

        elif score >= CUSTOMER_VERIFICATION_SCORE:
            return "Request Customer Verification"

        else:
            return "Monitor Activity"

    # ======================================
    # LOW RISK
    # ======================================
    return "Allow Transaction"