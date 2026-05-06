from collections import defaultdict

# ==========================================
# ASN MEMORY STORE
# ==========================================
asn_stats = defaultdict(lambda: {
    "total_transactions": 0,
    "high_risk_transactions": 0,
    "ato_events": 0,
    "geo_anomalies": 0,
    "graph_associations": 0
})

# ==========================================
# UPDATE ASN PROFILE
# ==========================================
def update_asn_profile(
    asn_number,
    result,
    geo_signals,
    graph_signals,
    ato_findings
):

    if not asn_number:
        return

    stats = asn_stats[asn_number]

    stats["total_transactions"] += 1

    # --------------------------------------
    # HIGH RISK TX
    # --------------------------------------
    if result.get("risk_category") == "High":
        stats["high_risk_transactions"] += 1

    # --------------------------------------
    # GEO ANOMALIES
    # --------------------------------------
    if geo_signals:
        stats["geo_anomalies"] += len(geo_signals)

    # --------------------------------------
    # GRAPH ASSOCIATIONS
    # --------------------------------------
    if graph_signals:
        stats["graph_associations"] += len(graph_signals)

    # --------------------------------------
    # ACCOUNT TAKEOVER EVENTS
    # --------------------------------------
    if ato_findings:
        stats["ato_events"] += len(ato_findings)


# ==========================================
# DYNAMIC ASN RISK EVALUATION
# ==========================================
def evaluate_dynamic_asn_risk(asn_number):

    if not asn_number:
        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }

    stats = asn_stats.get(asn_number)

    if not stats:
        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }

    total = stats["total_transactions"]

    if total < 3:
        return {
            "score": 0,
            "signals": [],
            "profile": stats
        }

    signals = []
    score = 0

    # --------------------------------------
    # RATIOS
    # --------------------------------------
    fraud_ratio = (
        stats["high_risk_transactions"] / total
    )

    ato_ratio = (
        stats["ato_events"] / total
    )

    graph_ratio = (
        stats["graph_associations"] / total
    )

    geo_ratio = (
        stats["geo_anomalies"] / total
    )

    # --------------------------------------
    # DYNAMIC SCORING
    # --------------------------------------
    if fraud_ratio > 0.4:
        signals.append("fraud_heavy_asn")
        score += 20

    if ato_ratio > 0.3:
        signals.append("ato_heavy_asn")
        score += 18

    if graph_ratio > 0.3:
        signals.append("fraud_network_asn")
        score += 15

    if geo_ratio > 0.4:
        signals.append("geo_anomaly_asn")
        score += 10

    return {
        "score": score,
        "signals": signals,
        "profile": stats
    }