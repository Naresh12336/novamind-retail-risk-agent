from services.graph_service import (
    update_graph,
    get_graph_risk_score
)

from services.velocity_service import (
    update_velocity,
    detect_velocity_cluster
)

from services.ato_service import (
    update_account_behavior,
    detect_account_takeover
)

from services.geo_service import (
    evaluate_geo_risk
)

from services.geo_asn_service import (
    evaluate_asn_risk
)

from threat_intelligence.threat_feed_service import (
    evaluate_threat_intelligence
)

from trust_engine.trust_service import (
    evaluate_trust
)

from config.fraud_policy import (
    VELOCITY_CLUSTER_SCORE,
    ATO_HIGH_SCORE,
    ATO_MEDIUM_SCORE
)


# ==========================================
# INFRASTRUCTURE INTELLIGENCE
# ==========================================
def evaluate_infrastructure(event: dict):

    # --------------------------------------
    # GRAPH
    # --------------------------------------
    update_graph(event)

    graph_result = get_graph_risk_score(event)

    graph_score = graph_result["score"]

    graph_signals = graph_result["signals"]

    # --------------------------------------
    # VELOCITY
    # --------------------------------------
    update_velocity(event)

    velocity_clusters = detect_velocity_cluster(event)

    velocity_score = (

        len(velocity_clusters)

        * VELOCITY_CLUSTER_SCORE

    )

    # --------------------------------------
    # ACCOUNT TAKEOVER
    # --------------------------------------
    update_account_behavior(event)

    ato_findings = detect_account_takeover(event)

    ato_score = 0

    for finding in ato_findings:

        if finding == "account_takeover":

            ato_score += ATO_HIGH_SCORE

        else:

            ato_score += ATO_MEDIUM_SCORE

    # --------------------------------------
    # GEO
    # --------------------------------------
    geo_result = evaluate_geo_risk(event)

    geo_score = geo_result["score"]

    geo_signals = geo_result["signals"]

    geo_profile = geo_result["profile"]

    # --------------------------------------
    # ASN
    # --------------------------------------
    asn_result = evaluate_asn_risk(event)

    asn_score = asn_result["score"]

    asn_signals = asn_result["signals"]

    asn_profile = asn_result["profile"]

    # --------------------------------------
    # THREAT
    # --------------------------------------
    threat_result = evaluate_threat_intelligence(event)

    threat_score = threat_result["score"]

    threat_signals = threat_result["signals"]

    threat_profile = threat_result["profile"]

    # --------------------------------------
    # TRUST
    # --------------------------------------
    trust_result = evaluate_trust(event)

    trust_score = trust_result["score"]

    trust_signals = trust_result["signals"]

    # --------------------------------------
    # INFRASTRUCTURE SCORE
    # --------------------------------------
    infrastructure_score = (

        graph_score

        + velocity_score

        + ato_score

        + geo_score

        + asn_score

        + threat_score

        + trust_score

    )

    # --------------------------------------
    # RETURN
    # --------------------------------------
    return {

        # Graph
        "graph_score": graph_score,
        "graph_signals": graph_signals,
        "graph_clusters": graph_result["clusters"],
        "community": graph_result["community"],

        # Velocity
        "velocity_score": velocity_score,
        "velocity_clusters": velocity_clusters,

        # ATO
        "ato_score": ato_score,
        "ato_findings": ato_findings,

        # Geo
        "geo_score": geo_score,
        "geo_signals": geo_signals,
        "geo_profile": geo_profile,

        # ASN
        "asn_score": asn_score,
        "asn_signals": asn_signals,
        "asn_profile": asn_profile,

        # Threat
        "threat_score": threat_score,
        "threat_signals": threat_signals,
        "threat_profile": threat_profile,

        # Trust
        "trust_score": trust_score,
        "trust_signals": trust_signals,
        "trust_profile": trust_result,

        # Aggregate
        "infrastructure_score": infrastructure_score
    }