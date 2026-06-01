from llm.reasoning_templates import (
    RISK_PATTERNS
)


def generate_investigation_report(
    packet
):

    evidence = packet.get(
        "evidence",
        {}
    )

    findings = []

    # ==========================
    # GRAPH
    # ==========================
    if evidence.get(
        "graph_signals"
    ):

        findings.append(
            RISK_PATTERNS[
                "graph_signals"
            ]
        )

    # ==========================
    # GEO
    # ==========================
    if evidence.get(
        "geo_signals"
    ):

        findings.append(
            RISK_PATTERNS[
                "geo_signals"
            ]
        )

    # ==========================
    # ASN
    # ==========================
    if evidence.get(
        "asn_signals"
    ):

        findings.append(
            RISK_PATTERNS[
                "asn_signals"
            ]
        )

    # ==========================
    # ATO
    # ==========================
    if evidence.get(
        "ato_findings"
    ):

        findings.append(
            RISK_PATTERNS[
                "ato_findings"
            ]
        )

    # ==========================
    # ML
    # ==========================
    ml_explanation = evidence.get(
        "ml_explanation",
        []
    )

    if ml_explanation:

        top_feature = (
            ml_explanation[0]
        )

        findings.append(

            f"Machine learning identified "
            f"{top_feature['feature']} "
            f"as the strongest fraud signal."
        )

    # ==========================
    # ASN REPUTATION
    # ==========================
    asn_rep = packet.get(
        "asn_reputation"
    )

    if asn_rep:

        findings.append(

            f"ASN infrastructure has "
            f"{asn_rep.get('high_risk_transactions',0)} "
            f"high-risk transactions."
        )

    # ==========================
    # REPUTATION
    # ==========================
    reputation = packet.get(
        "reputation",
        50
    )

    if reputation < 30:

        findings.append(

            "Customer reputation is severely degraded."
        )

    # ==========================
    # FINAL REPORT
    # ==========================
    report = {

        "case_id":
            packet.get(
                "case_id"
            ),

        "executive_summary":
            " ".join(findings),

        "recommendation":
            packet.get(
                "recommended_action"
            )
    }

    return report