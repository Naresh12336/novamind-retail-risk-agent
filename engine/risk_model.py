"""
engine/risk_model.py

Enterprise Risk Assessment Engine for NovaMind.

This module fuses intelligence from multiple subsystems into
a unified fraud risk assessment.

Current Intelligence Sources
----------------------------
- NLP Intelligence
- Behavioral Intelligence
- Honeypot Intelligence
- Infrastructure Intelligence

Future versions may integrate:

- Graph Intelligence
- Merchant Intelligence
- Threat Intelligence
- Device Intelligence
- Geolocation Intelligence

The module contains only risk scoring logic.
"""

from __future__ import annotations

from engine.nlp_types import RuleFeatures

from datetime import datetime, UTC

from engine.risk_types import (
    BehavioralFeatures,
    HoneypotFeatures,
    InfrastructureFeatures,
    RiskBreakdown,
    RiskResult,
)


class RiskModel:
    """
    Enterprise fraud risk assessment engine.

    This class combines intelligence from multiple
    independent subsystems into a single risk score.
    """

    def __init__(self) -> None:
        """
        Initialize the risk model.

        Reserved for future configuration such as
        scoring weights, thresholds and external
        configuration loading.
        """

        pass

    # ======================================================
    # NLP INTELLIGENCE
    # ======================================================

    def _score_nlp(
        self,
        rule_features: RuleFeatures,
    ) -> int:
        """
        Calculate the contribution from deterministic
        NLP intelligence.
        """

        score = 0

        score += min(
            rule_features.keyword_count * 6,
            24,
        )

        if rule_features.urgency_flag:
            score += 12

        return score

    # ======================================================
    # BEHAVIORAL INTELLIGENCE
    # ======================================================

    def _score_behavior(
        self,
        behavioral: BehavioralFeatures,
    ) -> int:
        """
        Calculate the contribution from behavioral
        intelligence.
        """

        score = 0

        #
        # Refund abuse
        #
        if behavioral.refund_count_last_30_days >= 7:

            score += 28

        elif behavioral.refund_count_last_30_days >= 5:

            score += 20

        elif behavioral.refund_count_last_30_days >= 3:

            score += 12

        #
        # Account age
        #
        if behavioral.account_age_days <= 7:

            score += 20

        elif behavioral.account_age_days <= 14:

            score += 12

        elif behavioral.account_age_days <= 30:

            score += 6

        #
        # Transaction amount
        #
        if behavioral.transaction_amount >= 500:

            score += 12

        elif behavioral.transaction_amount >= 250:

            score += 7

        elif behavioral.transaction_amount >= 150:

            score += 4

        return score

    # ======================================================
    # HONEYPOT INTELLIGENCE
    # ======================================================

    def _score_honeypot(
        self,
        honeypot: HoneypotFeatures,
    ) -> int:
        """
        Calculate the contribution from honeypot
        intelligence.
        """

        score = 0

        score += min(
            honeypot.tactic_count * 8,
            24,
        )

        return score

    # ======================================================
    # INFRASTRUCTURE INTELLIGENCE
    # ======================================================

    def _score_infrastructure(
        self,
        infrastructure: InfrastructureFeatures,
    ) -> int:
        """
        Calculate the contribution from infrastructure
        intelligence.
        """

        return infrastructure.infrastructure_score

    # ======================================================
    # CONFIDENCE
    # ======================================================

    def _calculate_confidence(
        self,
        rule_features: RuleFeatures,
        behavioral: BehavioralFeatures,
        honeypot: HoneypotFeatures,
        infrastructure: InfrastructureFeatures,
    ) -> tuple[float, str]:
        """
        Calculate the confidence of the overall
        risk assessment.
        """

        confidence = 0.35

        #
        # NLP confidence
        #
        confidence += min(
            rule_features.keyword_count * 0.04,
            0.16,
        )

        if rule_features.urgency_flag:
            confidence += 0.08

        #
        # Honeypot confidence
        #
        confidence += min(
            honeypot.tactic_count * 0.05,
            0.15,
        )

        #
        # Behavioral confidence
        #
        if behavioral.refund_count_last_30_days >= 5:
            confidence += 0.10

        if behavioral.account_age_days <= 14:
            confidence += 0.08

        #
        # Infrastructure confidence
        #
        if infrastructure.infrastructure_score >= 20:
            confidence += 0.10

        if infrastructure.infrastructure_score >= 40:
            confidence += 0.08

        confidence = round(
            min(confidence, 0.99),
            2,
        )

        if confidence >= 0.75:

            level = "High"

        elif confidence >= 0.55:

            level = "Medium"

        else:

            level = "Low"

        return confidence, level

    # ======================================================
    # RISK CATEGORY
    # ======================================================

    def _assign_risk_category(
        self,
        score: int,
    ) -> str:
        """
        Convert the numerical risk score into
        a categorical risk level.
        """

        if score >= 75:

            return "High"

        if score >= 45:

            return "Medium"

        return "Low"

    # ======================================================
    # PUBLIC API
    # ======================================================

    def evaluate(
        self,
        rule_features: RuleFeatures,
        behavioral: BehavioralFeatures,
        honeypot: HoneypotFeatures,
        infrastructure: InfrastructureFeatures,
    ) -> RiskResult:
        """
        Evaluate fraud risk by combining intelligence from
        multiple subsystems into a unified assessment.
        """

        try:
            #
            # Individual intelligence scores
            #
            nlp_score = self._score_nlp(rule_features)

            behavioral_score = self._score_behavior(
                behavioral,
            )

            honeypot_score = self._score_honeypot(
                honeypot,
            )

            infrastructure_score = self._score_infrastructure(
                infrastructure,
            )

            #
            # Aggregate score
            #
            total_score = (
                nlp_score
                + behavioral_score
                + honeypot_score
                + infrastructure_score
            )

            #
            # Confidence
            #
            confidence_score, confidence_level = (
                self._calculate_confidence(
                    rule_features,
                    behavioral,
                    honeypot,
                    infrastructure,
                )
            )

            #
            # Risk category
            #
            risk_category = self._assign_risk_category(
                total_score,
            )

            #
            # Score breakdown
            #
            breakdown = RiskBreakdown(
                nlp_score=nlp_score,
                behavioral_score=behavioral_score,
                honeypot_score=honeypot_score,
                infrastructure_score=infrastructure_score,
                total_score=total_score,
            )

            #
            # Metadata
            #
            metadata = {
                "pipeline": "Risk Assessment Engine",
                "version": "1.0",
                "evaluated_at": datetime.now(UTC).isoformat(),
            }

            #
            # Final result
            #
            return RiskResult(
                breakdown=breakdown,
                risk_score=total_score,
                risk_category=risk_category,
                confidence_score=confidence_score,
                confidence_level=confidence_level,
                metadata=metadata,
            )

        except Exception as exc:
            raise RuntimeError(
                "Risk assessment failed."
            ) from exc