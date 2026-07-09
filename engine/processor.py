from engine.nlp import extract_signals
from engine.adaptive_policy import adaptive_decide_action
from engine.honeypot import analyze_honeypot_text
from engine.risk_model import calculate_risk
from engine.reasoning import generate_reasoning
from alerts.alert_service import emit_alert
from analytics.decision_logger import log_decision
from engine.contribution import derive_contribution

from services.infrastructure_intelligence import (
    evaluate_infrastructure
)

from services.asn_reputation_service import (
    update_asn_profile
)

from services.reputation_service import (
    get_reputation,
    get_reputation_adjustment,
    update_reputation
)

from ml.inference_service import (
    predict_fraud_risk
)

from ml.explainability_service import (
    explain_prediction
)

from case_management.case_service import (
        create_case
    )

from threat_intelligence.update_threat_intelligence import (
    update_threat_intelligence
)


from trust_engine.trust_updater import (
    update_entity_trust
)

from engine.ml_decision_policy import (
    apply_ml_policy
)

import uuid


print("PROCESSING EVENT")


def process_transaction(event: dict):

    if "customer_id" not in event:
        raise ValueError("customer_id missing in event")

    customer_id = event["customer_id"]

    infra = evaluate_infrastructure(event)

    graph_score = infra["graph_score"]
    graph_signals = infra["graph_signals"]
    graph_clusters = infra["graph_clusters"]
    community = infra["community"]

    velocity_score = infra["velocity_score"]
    velocity_clusters = infra["velocity_clusters"]

    ato_score = infra["ato_score"]
    ato_findings = infra["ato_findings"]

    geo_score = infra["geo_score"]
    geo_signals = infra["geo_signals"]
    geo_profile = infra["geo_profile"]

    asn_score = infra["asn_score"]
    asn_signals = infra["asn_signals"]
    asn_profile = infra["asn_profile"]

    threat_score = infra["threat_score"]
    threat_signals = infra["threat_signals"]
    threat_profile = infra["threat_profile"]

    trust_score = infra["trust_score"]
    trust_signals = infra["trust_signals"]
    trust_result = infra["trust_profile"]

    infra_score = infra["infrastructure_score"]


    # ======================================
    # NLP + HONEYPOT
    # ======================================
    description = event.get("description", "")
    signals = extract_signals(description)
    honeypot = analyze_honeypot_text(description)
    evidence = {

        "textual_signals": signals,

        "behavioral_signals": {

            "amount": event.get(
                "amount",
                0
            ),

            "refund_count_last_30_days": event.get(
                "refund_count_last_30_days",
                0
            ),

            "account_age_days": event.get(
                "account_age_days",
                0
            )
        },

        "honeypot_signals": honeypot
    }

    # ======================================
    # BASE MODEL
    # ======================================

    score, category, confidence_score, confidence_level = calculate_risk(
        signals=signals,
        honeypot=honeypot,
        event=event,
        infrastructure_score=infra_score
    )


    # ======================================
    # REPUTATION MODIFIER
    # ======================================
    reputation_before = get_reputation(customer_id)
    rep_adjustment = get_reputation_adjustment(customer_id)

    score += rep_adjustment

    if score > 100:
        score = 100
    if score < 0:
        score = 0

    # Recalculate category
    if score >= 75:
        category = "High"
    elif score >= 40:
        category = "Medium"
    else:
        category = "Low"

    # ======================================
    # ML INFERENCE LAYER
    # ======================================
    partial_result = {

        "risk_score": score,

        "risk_category": category,

        "graph_score": graph_score,
        "velocity_score": velocity_score,
        "ato_score": ato_score,
        "geo_score": geo_score,
        "asn_score": asn_score,

        "graph_signals": graph_signals,

        "velocity_clusters": velocity_clusters,

        "ato_findings": ato_findings,

        "geo_signals": geo_signals,

        "asn_signals": asn_signals,

        "threat_score": threat_score,

        "threat_signals": threat_signals,

        "trust_score": trust_score,

        "trust_signals": trust_signals,

        "reputation_before": reputation_before,

        "evidence": evidence,

        "infrastructure_score": infra_score,

    }

    ml_result = predict_fraud_risk(
        event,
        partial_result
    )

    ml_prediction = ml_result.get(
        "prediction",
        0
    )

    ml_probability = ml_result.get(
        "fraud_probability",
        0
    )

    # ======================================
    # ML EXPLAINABILITY
    # ======================================
    ml_explanation = explain_prediction(
        ml_result.get(
            "features",
            {}
        )
    )

    top_ml_contributors = (
        ml_explanation.get(
            "top_contributors",
            []
        )
    )

    # ======================================
    # REASONING
    # ======================================
    if category in ["Medium", "High"]:
        reasoning = generate_reasoning(signals, score, category)
    else:
        reasoning = "Low risk transaction based on current signals."

    contribution = derive_contribution(signals, honeypot, event)

    decision_id = str(uuid.uuid4())
    action = adaptive_decide_action(
        score=score,
        confidence_level=confidence_level,
        event={
            **event,
            "geo_signals": geo_signals,
            "asn_signals": asn_signals
        },
        reputation_before=reputation_before,
        graph_signals=graph_signals,
        velocity_clusters=velocity_clusters,
        ato_findings=ato_findings
    )

    print("GRAPH SIGNAL COUNT:", len(graph_signals))
    print("VELOCITY COUNT:", len(velocity_clusters))
    print("ATO COUNT:", len(ato_findings))
    print("GEO SCORE:", geo_score)
    print("GEO SIGNALS:", geo_signals)
    print("GEO PROFILE:", geo_profile)
    print("ASN SCORE:", asn_score)
    print("ASN SIGNALS:", asn_signals)
    print("ASN PROFILE:", asn_profile)
    print("THREAT SCORE:", threat_score)
    print("THREAT SIGNALS:", threat_signals)
    print("THREAT PROFILE:", threat_profile)
    print("TRUST SCORE:", trust_score)
    print("TRUST SIGNALS:", trust_signals)
    print("TRUST PROFILE:", trust_result)
    print("ML PREDICTION:", ml_prediction)
    print("ML FRAUD PROBABILITY:", ml_probability)
    print("ML TOP CONTRIBUTORS:", top_ml_contributors)
    print("ADAPTIVE DECISION:", action)
    print("BASE SCORE:", score)
    print("REPUTATION:", reputation_before)



    # ======================================
    # RESULT
    # ======================================
    result = {
        "decision_id": decision_id,
        "transaction_id": event.get("transaction_id"),
        "customer_id": customer_id,

        "risk_score": score,
        "risk_category": category,
        "confidence_score": round(confidence_score, 2),
        "confidence_level": confidence_level,
        "recommended_action": action,
        "reasoning": reasoning,

        "reputation_before": reputation_before,
        "reputation_adjustment": rep_adjustment,

        "graph_score": graph_score,
        "graph_signals": graph_signals,
        "graph_clusters": graph_clusters,
        "graph_community": community,

        "velocity_score": velocity_score,
        "velocity_clusters": velocity_clusters,

        "ato_score": ato_score,
        "ato_findings": ato_findings,

        "geo_score": geo_score,
        "geo_signals": geo_signals,
        "geo_profile": geo_profile,

        "asn_score": asn_score,
        "asn_signals": asn_signals,
        "asn_profile": asn_profile,

        "threat_score": threat_score,
        "threat_signals":threat_signals,
        "threat_profile":threat_profile,

        "trust_score": trust_score,
        "trust_signals": trust_signals,
        "trust_profile": trust_result,

        "evidence": evidence,

        "contribution": contribution,

        "ml_prediction": ml_prediction,
        "ml_probability": ml_probability,
        "ml_explanation": top_ml_contributors,
        "ml_result": ml_result,
        "infrastructure_score": infra_score,
    }

    result = apply_ml_policy(result)

    final_action = result["recommended_action"]

    if final_action in [

        "Manual Review Required",

        "Request Customer Verification",

        "Auto Block Transaction"

    ]:
        case = create_case(result)
        result["case"] = case

    # ======================================
    # UPDATE ASN REPUTATION
    # ======================================
    update_asn_profile(
        asn_number=asn_profile.get("asn"),
        result=result,
        geo_signals=geo_signals,
        graph_signals=graph_signals,
        ato_findings=ato_findings
    )

    # ======================================
    # UPDATE THREAT INTELLIGENCE
    # ======================================
    update_threat_intelligence(event,result)

    update_entity_trust(event,result)

    # ======================================
    # UPDATE CUSTOMER REPUTATION
    # ======================================
    update_reputation(customer_id,result)

    print("FINAL DECISION:", result["recommended_action"])
    print("REPUTATION BEFORE:", reputation_before)
    print("REPUTATION ADJUSTMENT:", rep_adjustment)

    # ======================================
    # LOG DECISION
    # ======================================
    log_decision(event, result,signals,honeypot)

    if final_action in ["Manual Review Required", "Auto Block Transaction"]:
        emit_alert(result, event)

    return result