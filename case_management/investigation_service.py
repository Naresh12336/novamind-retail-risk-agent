from services.graph_service import (
    detect_fraud_community
)

from services.reputation_service import (
    reputation_store
)

from services.asn_reputation_service import (
    get_asn_profile
)

from case_management.case_store import (
    case_db
)

from llm.investigation_narrator import (
    generate_investigation_report
)


# ==================================================
# BUILD INVESTIGATION PACKET
# ==================================================
def build_investigation_packet(case_id):

    case = case_db.get(case_id)

    if not case:
        return None

    customer_id = case.get("customer_id")

    # ==========================================
    # COMMUNITY ANALYSIS
    # ==========================================
    community = detect_fraud_community(
        customer_id
    )

    # ==========================================
    # CUSTOMER REPUTATION
    # ==========================================
    reputation = reputation_store.get(
        customer_id,
        50
    )

    # ==========================================
    # ASN INFORMATION
    # ==========================================
    asn_number = (
        case.get("evidence", {})
            .get("asn_profile", {})
            .get("asn")
    )

    asn_reputation = get_asn_profile(
        asn_number
    )

    # ==========================================
    # INVESTIGATION SUMMARY
    # ==========================================
    summary = generate_summary(
        case=case,
        community=community,
        reputation=reputation,
        asn_reputation=asn_reputation
    )

    # ==========================================
    # INVESTIGATION PACKET
    # ==========================================
    packet = {

        "case_id":
            case.get("case_id"),

        "customer_id":
            customer_id,

        "status":
            case.get("status"),

        "priority":
            case.get("priority"),

        "risk_score":
            case.get("risk_score"),

        "risk_category":
            case.get("risk_category"),

        "recommended_action":
            case.get("recommended_action"),

        # --------------------------
        # COMMUNITY
        # --------------------------
        "community":
            community,

        # --------------------------
        # REPUTATION
        # --------------------------
        "reputation":
            reputation,

        # --------------------------
        # ASN
        # --------------------------
        "asn_reputation":
            asn_reputation,

        # --------------------------
        # EVIDENCE
        # --------------------------
        "evidence":
            case.get(
                "evidence",
                {}
            ),

        # --------------------------
        # ANALYST SUMMARY
        # --------------------------
        "investigation_summary":
            summary
    }
    packet[
        "llm_report"
    ] = generate_investigation_report(
        packet
    )

    return packet


# ==================================================
# SUMMARY GENERATOR
# ==================================================
def generate_summary(
    case,
    community,
    reputation,
    asn_reputation
):

    findings = []

    # ==========================================
    # COMMUNITY FINDINGS
    # ==========================================
    if community:

        findings.append(
            f"Customer linked to fraud community "
            f"containing "
            f"{community.get('community_size', 0)} "
            f"accounts"
        )

    # ==========================================
    # REPUTATION FINDINGS
    # ==========================================
    if reputation < 20:

        findings.append(
            "Customer reputation is critical"
        )

    elif reputation < 40:

        findings.append(
            "Customer reputation is degraded"
        )

    # ==========================================
    # ASN FINDINGS
    # ==========================================
    if asn_reputation:

        total_tx = asn_reputation.get(
            "total_transactions",
            0
        )

        high_risk_tx = asn_reputation.get(
            "high_risk_transactions",
            0
        )

        if total_tx > 0:

            fraud_ratio = (
                high_risk_tx / total_tx
            )

            if fraud_ratio > 0.4:

                findings.append(
                    "ASN has elevated fraud concentration"
                )

        if asn_reputation.get(
            "ato_events",
            0
        ) > 0:

            findings.append(
                "ASN associated with account takeover activity"
            )

        if asn_reputation.get(
            "graph_associations",
            0
        ) > 0:

            findings.append(
                "ASN linked to fraud network infrastructure"
            )

    # ==========================================
    # SIGNAL FINDINGS
    # ==========================================
    evidence = case.get(
        "evidence",
        {}
    )

    if evidence.get("geo_signals"):

        findings.append(
            "Geo anomalies detected"
        )

    if evidence.get("graph_signals"):

        findings.append(
            "Graph intelligence indicates linked entities"
        )

    if evidence.get("asn_signals"):

        findings.append(
            "ASN intelligence produced risk signals"
        )

    if evidence.get("ato_findings"):

        findings.append(
            "Account takeover indicators detected"
        )

    # ==========================================
    # ML FINDINGS
    # ==========================================
    ml_explanation = evidence.get(
        "ml_explanation",
        []
    )

    if ml_explanation:

        top_feature = ml_explanation[0]

        findings.append(
            f"ML model's strongest signal: "
            f"{top_feature.get('feature')}"
        )

    # ==========================================
    # FALLBACK
    # ==========================================
    if not findings:

        findings.append(
            "No significant supporting evidence found"
        )

    return findings