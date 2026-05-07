def build_feature_vector(event: dict, result: dict):

    graph_signals = result.get("graph_signals", [])
    velocity_clusters = result.get("velocity_clusters", [])
    ato_findings = result.get("ato_findings", [])
    geo_signals = result.get("geo_signals", [])
    asn_signals = result.get("asn_signals", [])

    evidence = result.get("evidence", {})

    textual = evidence.get("textual_signals", {})
    behavioral = evidence.get("behavioral_signals", {})
    honeypot = evidence.get("honeypot_signals", {})

    # ======================================
    # FEATURE VECTOR
    # ======================================
    features = {

        # ----------------------------------
        # BASE RISK
        # ----------------------------------
        "risk_score": result.get("risk_score", 0),

        "graph_score": result.get("graph_score", 0),
        "velocity_score": result.get("velocity_score", 0),
        "ato_score": result.get("ato_score", 0),
        "geo_score": result.get("geo_score", 0),
        "asn_score": result.get("asn_score", 0),

        # ----------------------------------
        # TEXT FEATURES
        # ----------------------------------
        "keyword_count": textual.get("keyword_count", 0),

        "urgency_flag": int(
            textual.get("urgency_flag", False)
        ),

        "text_length": textual.get("text_length", 0),

        # ----------------------------------
        # BEHAVIORAL
        # ----------------------------------
        "amount": behavioral.get("amount", 0),

        "refund_count_last_30_days": behavioral.get(
            "refund_count_last_30_days",
            0
        ),

        "account_age_days": behavioral.get(
            "account_age_days",
            0
        ),

        # ----------------------------------
        # HONEYPOT
        # ----------------------------------
        "honeypot_tactic_count": honeypot.get(
            "tactic_count",
            0
        ),

        # ----------------------------------
        # SIGNAL COUNTS
        # ----------------------------------
        "graph_signal_count": len(graph_signals),

        "velocity_signal_count": len(
            velocity_clusters
        ),

        "ato_signal_count": len(
            ato_findings
        ),

        "geo_signal_count": len(
            geo_signals
        ),

        "asn_signal_count": len(
            asn_signals
        ),

        # ----------------------------------
        # REPUTATION
        # ----------------------------------
        "reputation_before": result.get(
            "reputation_before",
            50
        ),

        # ----------------------------------
        # DECISION LABELS
        # ----------------------------------
        "is_high_risk": int(
            result.get("risk_category") == "High"
        ),

        "was_blocked": int(
            result.get("recommended_action")
            == "Auto Block Transaction"
        )
    }

    return features