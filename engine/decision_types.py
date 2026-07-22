"""
engine/decision_types.py

Core data models used by the NovaMind Decision Policy Engine.

This module contains ONLY data structures.
No decision-making logic belongs here.

Pipeline
--------
RiskResult
      ↓
DecisionPolicy
      ↓
DecisionBreakdown
      ↓
DecisionResult
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


# ==========================================================
# ACTION TYPES
# ==========================================================

class ActionType(Enum):
    """
    Supported fraud prevention actions.
    """

    ALLOW = "Allow Transaction"

    MONITOR = "Monitor Activity"

    VERIFY = "Request Customer Verification"

    STEP_UP = "Step-Up Authentication"

    REVIEW = "Manual Review Required"

    BLOCK = "Auto Block Transaction"


# ==========================================================
# REASON SEVERITY
# ==========================================================

class ReasonSeverity(Enum):
    """
    Severity level of an individual decision reason.
    """

    LOW = "Low"

    MEDIUM = "Medium"

    HIGH = "High"


# ==========================================================
# DECISION REASON
# ==========================================================

@dataclass(slots=True)
class DecisionReason:
    """
    Structured explanation supporting a decision.
    """

    title: str

    description: str

    severity: ReasonSeverity


# ==========================================================
# DECISION BREAKDOWN
# ==========================================================

@dataclass(slots=True)
class DecisionBreakdown:
    """
    Structured summary of how the decision was made.
    """

    risk_score: int

    risk_category: str

    confidence_score: float

    confidence_level: str

    applied_policy: str

    action: ActionType


# ==========================================================
# DECISION RESULT
# ==========================================================

@dataclass(slots=True)
class DecisionResult:
    """
    Final output returned by DecisionPolicy.
    """

    action: ActionType

    breakdown: DecisionBreakdown

    reasons: List[DecisionReason] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [
    "ActionType",
    "ReasonSeverity",
    "DecisionReason",
    "DecisionBreakdown",
    "DecisionResult",
]