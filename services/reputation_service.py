from collections import defaultdict

# ==========================================
# CUSTOMER REPUTATION STORE
# ==========================================
# customer_id -> score
reputation_store = defaultdict(lambda: 50)

MAX_SCORE = 100
MIN_SCORE = 0


# ==========================================
# HELPERS
# ==========================================
def clamp(value):
    return max(MIN_SCORE, min(MAX_SCORE, value))


def get_reputation(customer_id: str):

    if not customer_id:
        return 50

    return reputation_store[customer_id]


# ==========================================
# UPDATE AFTER DECISION
# ==========================================
def update_reputation(customer_id: str, result: dict):

    if not customer_id:
        return

    score = reputation_store[customer_id]

    risk = result.get("risk_category")
    action = result.get("recommended_action")

    graph_signals = result.get("graph_signals", [])
    velocity_clusters = result.get("velocity_clusters", [])
    ato_findings = result.get("ato_findings", [])

    # ----------------------------------
    # Positive Behavior
    # ----------------------------------
    if risk == "Low":
        score += 3

    elif risk == "Medium":
        score += 0

    # ----------------------------------
    # Negative Behavior
    # ----------------------------------
    if risk == "High":
        score -= 8

    if action == "Manual Review Required":
        score -= 5

    if action == "Request Customer Verification":
        score -= 4

    if action == "Auto Block Transaction":
        score -= 12

    # ----------------------------------
    # Network / Infra Risk
    # ----------------------------------
    score -= len(graph_signals) * 4
    score -= len(velocity_clusters) * 5
    score -= len(ato_findings) * 6

    reputation_store[customer_id] = clamp(score)


# ==========================================
# RISK MODIFIER
# ==========================================
def get_reputation_adjustment(customer_id: str):

    score = get_reputation(customer_id)

    # Trusted customer
    if score >= 80:
        return -12

    if score >= 70:
        return -8

    if score >= 60:
        return -4

    # Neutral
    if score >= 40:
        return 0

    # Suspicious
    if score >= 25:
        return 8

    if score >= 10:
        return 15

    # Very risky
    return 25