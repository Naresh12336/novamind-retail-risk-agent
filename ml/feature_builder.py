# ==========================================
# FEATURE BUILDER
# ==========================================

def build_feature_vector(
    event: dict,
    partial_result: dict
):

    # --------------------------------------
    # SIGNAL COLLECTION
    # --------------------------------------
    graph_signals = partial_result.get(
        "graph_signals",
        []
    )

    velocity_clusters = partial_result.get(
        "velocity_clusters",
        []
    )

    ato_findings = partial_result.get(
        "ato_findings",
        []
    )

    geo_signals = partial_result.get(
        "geo_signals",
        []
    )

    asn_signals = partial_result.get(
        "asn_signals",
        []
    )

    threat_signals = partial_result.get(
        "threat_signals",
        []
    )

    trust_signals = partial_result.get(
        "trust_signals",
        []
    )

    merchant_signals = partial_result.get(
        "merchant_signals",
        []
    )

    # --------------------------------------
    # EVIDENCE
    # --------------------------------------
    evidence = partial_result.get(
        "evidence",
        {}
    )

    textual = evidence.get(
        "textual_signals",
        {}
    )

    behavioral = evidence.get(
        "behavioral_signals",
        {}
    )

    honeypot = evidence.get(
        "honeypot_signals",
        {}
    )

    # ======================================
    # FEATURE VECTOR
    # ======================================
    features = {

        # ==================================
        # BASE RISK
        # ==================================
        "risk_score":
            partial_result.get(
                "risk_score",
                0
            ),

        # ==================================
        # INFRASTRUCTURE SCORES
        # ==================================
        "graph_score":
            partial_result.get(
                "graph_score",
                0
            ),

        "velocity_score":
            partial_result.get(
                "velocity_score",
                0
            ),

        "ato_score":
            partial_result.get(
                "ato_score",
                0
            ),

        "geo_score":
            partial_result.get(
                "geo_score",
                0
            ),

        "asn_score":
            partial_result.get(
                "asn_score",
                0
            ),

        "threat_score":
            partial_result.get(
                "threat_score",
                0
            ),

        "trust_score":
            partial_result.get(
                "trust_score",
                0
            ),

        "merchant_score":
            partial_result.get(
                "merchant_score",
                0
            ),

        # ==================================
        # NLP FEATURES
        # ==================================
        "keyword_count":
            textual.get(
                "keyword_count",
                0
            ),

        "urgency_flag":
            int(
                textual.get(
                    "urgency_flag",
                    False
                )
            ),

        "text_length":
            textual.get(
                "text_length",
                0
            ),

        # ==================================
        # BEHAVIORAL
        # ==================================
        "amount":
            behavioral.get(
                "amount",
                0
            ),

        "refund_count_last_30_days":
            behavioral.get(
                "refund_count_last_30_days",
                0
            ),

        "account_age_days":
            behavioral.get(
                "account_age_days",
                0
            ),

        # ==================================
        # HONEYPOT
        # ==================================
        "honeypot_tactic_count":
            honeypot.get(
                "tactic_count",
                0
            ),

        # ==================================
        # SIGNAL COUNTS
        # ==================================
        "graph_signal_count":
            len(graph_signals),

        "velocity_signal_count":
            len(
                velocity_clusters
            ),

        "ato_signal_count":
            len(
                ato_findings
            ),

        "geo_signal_count":
            len(
                geo_signals
            ),

        "asn_signal_count":
            len(
                asn_signals
            ),

        "threat_signal_count":
            len(
                threat_signals
            ),

        "trust_signal_count":
            len(
                trust_signals
            ),

        "merchant_signal_count":
            len(
                merchant_signals
            ),

        # ==================================
        # REPUTATION
        # ==================================
        "reputation_before":
            partial_result.get(
                "reputation_before",
                50
            ),

        # ==================================
        # TRAINING LABELS
        # ==================================
        "is_high_risk":
            int(
                partial_result.get(
                    "risk_category"
                ) == "High"
            ),

        "was_blocked":
            int(
                partial_result.get(
                    "recommended_action"
                )
                ==
                "Auto Block Transaction"
            )
    }

    return features