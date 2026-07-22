"""
engine/risk_types.py

Core data models used by the NovaMind Risk Assessment Engine.

This module contains ONLY data structures.
No risk scoring logic belongs here.

Pipeline
--------
FeatureBundle
      ↓
BehavioralFeatures
InfrastructureFeatures
HoneypotFeatures
      ↓
RiskBreakdown
      ↓
RiskResult

Future versions may extend this module with:

    - GraphFeatures
    - MerchantFeatures
    - ThreatFeatures
    - DeviceFeatures
    - GeolocationFeatures

without changing existing interfaces.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


# ==========================================================
# BEHAVIORAL FEATURES
# ==========================================================

@dataclass(slots=True)
class BehavioralFeatures:
    """
    Behavioral signals describing customer activity.
    """

    refund_count_last_30_days: int = 0

    account_age_days: int = 0

    transaction_amount: float = 0.0


# ==========================================================
# HONEYPOT FEATURES
# ==========================================================

@dataclass(slots=True)
class HoneypotFeatures:
    """
    Intelligence produced by the honeypot subsystem.
    """

    tactic_count: int = 0


# ==========================================================
# INFRASTRUCTURE FEATURES
# ==========================================================

@dataclass(slots=True)
class InfrastructureFeatures:
    """
    Intelligence produced by infrastructure analysis.
    """

    infrastructure_score: int = 0


# ==========================================================
# RISK BREAKDOWN
# ==========================================================

@dataclass(slots=True)
class RiskBreakdown:
    """
    Individual contributions from each intelligence source.
    """

    nlp_score: int = 0

    behavioral_score: int = 0

    honeypot_score: int = 0

    infrastructure_score: int = 0

    total_score: int = 0


# ==========================================================
# RISK RESULT
# ==========================================================

@dataclass(slots=True)
class RiskResult:
    """
    Final output returned by RiskModel.
    """

    breakdown: RiskBreakdown

    risk_score: int

    risk_category: str

    confidence_score: float

    confidence_level: str

    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [
    "BehavioralFeatures",
    "HoneypotFeatures",
    "InfrastructureFeatures",
    "RiskBreakdown",
    "RiskResult",
]