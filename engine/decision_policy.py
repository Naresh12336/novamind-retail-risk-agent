def decide_action(risk_category: str, confidence: str) -> str:

    if risk_category == "High":
        if confidence == "High":
            return "Auto Block Transaction"
        elif confidence == "Medium":
            return "Manual Review Required"
        else:
            return "Request Customer Verification"

    if risk_category == "Medium":
        if confidence == "High":
            return "Step-Up Authentication"
        else:
            return "Monitor Activity"

    return "Allow Transaction"
