"""
engine/decision_policy.py

Enterprise Decision Policy Engine for NovaMind.

This module converts a fraud risk assessment into a business
decision according to configurable fraud policies.

The module contains only decision-making logic.
"""

from __future__ import annotations

from config.fraud_policy import (
    AUTO_BLOCK_SCORE,
    CUSTOMER_VERIFICATION_SCORE,
    STEP_UP_SCORE,
)

from engine.decision_types import (
    ActionType,
    DecisionBreakdown,
    DecisionReason,
    ReasonSeverity,
)

from engine.risk_types import RiskResult


class DecisionPolicy:
    """
    Enterprise fraud decision engine.

    Converts a RiskResult into an appropriate
    business action.
    """

    def __init__(self) -> None:
        """
        Initialize the decision policy.

        Reserved for future configuration such as
        dynamic policy loading, feature flags,
        customer-specific rules, etc.
        """

        pass

    # ======================================================
    # HIGH RISK
    # ======================================================

    def _decide_high_risk(
        self,
        risk: RiskResult,
    ) -> ActionType:
        """
        Determine the action for high-risk transactions.
        """

        if risk.risk_score >= AUTO_BLOCK_SCORE:
            return ActionType.BLOCK

        if risk.confidence_level == "High":
            return ActionType.REVIEW

        if risk.confidence_level == "Medium":
            return ActionType.VERIFY

        return ActionType.MONITOR

    # ======================================================
    # MEDIUM RISK
    # ======================================================

    def _decide_medium_risk(
        self,
        risk: RiskResult,
    ) -> ActionType:
        """
        Determine the action for medium-risk transactions.
        """

        if (
            risk.risk_score >= STEP_UP_SCORE
            and risk.confidence_level == "High"
        ):
            return ActionType.STEP_UP

        if (
            risk.risk_score >= CUSTOMER_VERIFICATION_SCORE
        ):
            return ActionType.VERIFY

        return ActionType.MONITOR

    # ======================================================
    # LOW RISK
    # ======================================================

    def _decide_low_risk(
        self,
        risk: RiskResult,
    ) -> ActionType:
        """
        Determine the action for low-risk transactions.
        """

        return ActionType.ALLOW

    # ======================================================
    # DECISION REASONS
    # ======================================================

    def _build_reasons(
        self,
        risk: RiskResult,
        action: ActionType,
    ) -> list[DecisionReason]:
        """
        Build structured reasons explaining why
        the policy selected the given action.
        """

        reasons: list[DecisionReason] = []

        if action == ActionType.BLOCK:

            reasons.append(
                DecisionReason(
                    title="Auto Block Policy",
                    description=(
                        "Risk score exceeded the automatic "
                        "blocking threshold."
                    ),
                    severity=ReasonSeverity.HIGH,
                )
            )

        elif action == ActionType.REVIEW:

            reasons.append(
                DecisionReason(
                    title="Manual Review Policy",
                    description=(
                        "High-risk transaction with high "
                        "confidence requires analyst review."
                    ),
                    severity=ReasonSeverity.HIGH,
                )
            )

        elif action == ActionType.STEP_UP:

            reasons.append(
                DecisionReason(
                    title="Step-Up Authentication",
                    description=(
                        "Additional customer authentication "
                        "is required."
                    ),
                    severity=ReasonSeverity.MEDIUM,
                )
            )

        elif action == ActionType.VERIFY:

            reasons.append(
                DecisionReason(
                    title="Customer Verification",
                    description=(
                        "Customer verification is required "
                        "before approval."
                    ),
                    severity=ReasonSeverity.MEDIUM,
                )
            )

        elif action == ActionType.MONITOR:

            reasons.append(
                DecisionReason(
                    title="Monitoring",
                    description=(
                        "Transaction is permitted but "
                        "will be monitored."
                    ),
                    severity=ReasonSeverity.LOW,
                )
            )

        else:

            reasons.append(
                DecisionReason(
                    title="Approved",
                    description=(
                        "Transaction satisfies the "
                        "current fraud policy."
                    ),
                    severity=ReasonSeverity.LOW,
                )
            )

        return reasons

    # ======================================================
    # DECISION BREAKDOWN
    # ======================================================

    def _build_breakdown(
        self,
        risk: RiskResult,
        action: ActionType,
    ) -> DecisionBreakdown:
        """
        Build a structured summary of the
        decision process.
        """

        return DecisionBreakdown(
            risk_score=risk.risk_score,
            risk_category=risk.risk_category,
            confidence_score=risk.confidence_score,
            confidence_level=risk.confidence_level,
            applied_policy="Fraud Policy v1.0",
            action=action,
        )