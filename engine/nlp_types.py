"""
engine/nlp_types.py

Core data models used by the NovaMind NLP Engine.

This module contains ONLY data structures.
No NLP processing logic belongs here.

Current Pipeline
----------------
Raw Text
    ↓
PreprocessedText
    ↓
RuleFeatures
    ↓
FeatureBundle
    ↓
NLPResult

Future versions will extend FeatureBundle with:
    - IntentFeatures
    - EntityFeatures
    - StyleFeatures
    - SentimentFeatures
    - EmbeddingFeatures
    - ConfidenceFeatures

NLPResult should remain stable even as new
feature extractors are introduced.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ==========================================================
# PREPROCESSED TEXT
# ==========================================================

@dataclass(slots=True)
class PreprocessedText:
    """
    Output produced by TextPreprocessor.

    This object contains normalized linguistic information
    extracted from the raw transaction description.
    """

    # Original user input
    original_text: str

    # Normalized text
    clean_text: str

    # Linguistic features
    tokens: List[str] = field(default_factory=list)
    lemmas: List[str] = field(default_factory=list)
    pos_tags: List[str] = field(default_factory=list)
    sentences: List[str] = field(default_factory=list)

    # Basic statistics
    token_count: int = 0
    sentence_count: int = 0
    character_count: int = 0
    unique_token_count: int = 0


# ==========================================================
# RULE FEATURES
# ==========================================================

@dataclass(slots=True)
class RuleFeatures:
    """
    Deterministic features extracted by RuleEngine.

    These features are fully explainable and contain
    no machine learning predictions.
    """

    # Matched keywords
    keyword_hits: List[str] = field(default_factory=list)

    # Matched fraud categories
    matched_categories: List[str] = field(default_factory=list)

    # Summary statistics
    keyword_count: int = 0
    category_count: int = 0

    # Important fraud indicators
    urgency_flag: bool = False

    # Category-specific keyword collections
    money_terms: List[str] = field(default_factory=list)
    payment_terms: List[str] = field(default_factory=list)
    account_terms: List[str] = field(default_factory=list)
    security_terms: List[str] = field(default_factory=list)
    legal_terms: List[str] = field(default_factory=list)
    scam_terms: List[str] = field(default_factory=list)


# ==========================================================
# FEATURE BUNDLE
# ==========================================================

@dataclass(slots=True)
class FeatureBundle:
    """
    Internal aggregation object used by NLPEngine.

    Every NLP module contributes its output here.
    As new analyzers are added, only this class
    grows while NLPResult remains unchanged.
    """

    preprocessing: Optional[PreprocessedText] = None

    rule_features: Optional[RuleFeatures] = None

    # Future modules
    #
    # intent_features: Optional[IntentFeatures] = None
    # entity_features: Optional[EntityFeatures] = None
    # style_features: Optional[StyleFeatures] = None
    # sentiment_features: Optional[SentimentFeatures] = None
    # embedding_features: Optional[EmbeddingFeatures] = None
    # confidence_features: Optional[ConfidenceFeatures] = None


# ==========================================================
# NLP RESULT
# ==========================================================

@dataclass(slots=True)
class NLPResult:
    """
    Final output returned by NLPEngine.

    The public interface remains stable while
    FeatureBundle evolves as additional NLP
    modules are introduced.
    """

    features: FeatureBundle

    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [
    "PreprocessedText",
    "RuleFeatures",
    "FeatureBundle",
    "NLPResult",
]