def decide_action(risk_category: str, confidence: str, score: int) -> str:

    # --- HIGH RISK ---
    if risk_category == "High":

        if score >= 90:
            return "Auto Block Transaction"

        if confidence == "High":
            return "Manual Review Required"

        if confidence == "Medium":
            return "Request Customer Verification"

        return "Monitor Activity"

    # --- MEDIUM RISK ---
    if risk_category == "Medium":

        if score >= 50 and confidence == "High":
            return "Step-Up Authentication"

        if score >= 45:
            return "Request Customer Verification"

        return "Monitor Activity"

    # --- LOW RISK ---
    return "Allow Transaction"
