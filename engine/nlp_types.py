"""
engine/nlp_types.py

Core data models used by the NovaMind NLP Engine.

This module defines ONLY immutable data structures.
No preprocessing, NLP, or fraud detection logic belongs here.

Pipeline
--------
Raw Text
    ↓
PreprocessedText
    ↓
RuleFeatures
    ↓
FeatureBundle
    ↓
NLPResult

Design Principles
-----------------
- PreprocessedText contains linguistic annotations only.
- RuleFeatures contains deterministic fraud indicators.
- FeatureBundle aggregates outputs from NLP analyzers.
- NLPResult remains the stable public API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ==========================================================
# TOKEN INFORMATION
# ==========================================================

@dataclass(slots=True, frozen=True)
class TokenInfo:
    """
    Linguistic information for a single token.
    """

    text: str
    lemma: str
    pos: str


# ==========================================================
# NAMED ENTITY
# ==========================================================

@dataclass(slots=True, frozen=True)
class NamedEntity:
    """
    Named entity extracted from text.
    """

    text: str
    label: str

    start_char: int
    end_char: int

    start_token: int
    end_token: int


# ==========================================================
# DEPENDENCY RELATION
# ==========================================================

@dataclass(slots=True, frozen=True)
class DependencyRelation:
    """
    Dependency relation between two tokens.
    """

    token: str
    head: str
    dependency: str


# ==========================================================
# NEGATION
# ==========================================================

@dataclass(slots=True, frozen=True)
class NegationMarker:
    """
    Represents a detected negation.
    """

    negation_word: str
    target: str


# ==========================================================
# PREPROCESSED TEXT
# ==========================================================

@dataclass(slots=True)
class PreprocessedText:
    """
    Complete linguistic representation produced by TextPreprocessor.

    Contains only language annotations and document statistics.
    No fraud intelligence belongs here.
    """

    # ------------------------------------------------------
    # Raw Text
    # ------------------------------------------------------

    original_text: str

    clean_text: str

    # ------------------------------------------------------
    # Token-Level Information
    # ------------------------------------------------------

    tokens: List[TokenInfo] = field(default_factory=list)

    sentences: List[str] = field(default_factory=list)

    # ------------------------------------------------------
    # Linguistic Annotations
    # ------------------------------------------------------

    named_entities: List[NamedEntity] = field(default_factory=list)

    dependency_relations: List[DependencyRelation] = field(
        default_factory=list
    )

    noun_chunks: List[str] = field(default_factory=list)

    negations: List[NegationMarker] = field(default_factory=list)

    # ------------------------------------------------------
    # Document Statistics
    # ------------------------------------------------------

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
    """

    keyword_hits: List[str] = field(default_factory=list)

    matched_categories: List[str] = field(default_factory=list)

    keyword_count: int = 0

    category_count: int = 0

    urgency_flag: bool = False

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
    Aggregates outputs from all NLP analyzers.
    """

    preprocessing: Optional[PreprocessedText] = None

    rule_features: Optional[RuleFeatures] = None

    # Future Intelligence Modules
    #
    # semantic_features: Optional[SemanticFeatures] = None
    # embedding_features: Optional[EmbeddingFeatures] = None
    # llm_features: Optional[LLMFeatures] = None
    # confidence_features: Optional[ConfidenceFeatures] = None


# ==========================================================
# NLP RESULT
# ==========================================================

@dataclass(slots=True)
class NLPResult:
    """
    Stable public API returned by NLPEngine.
    """

    features: FeatureBundle

    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [
    "TokenInfo",
    "NamedEntity",
    "DependencyRelation",
    "NegationMarker",
    "PreprocessedText",
    "RuleFeatures",
    "FeatureBundle",
    "NLPResult",
]