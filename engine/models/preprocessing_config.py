"""
engine/models/preprocessing_config.py

Configuration for the NovaMind NLP preprocessing pipeline.

This module contains immutable configuration objects used by
TextPreprocessor. It intentionally contains no NLP logic.

Responsibilities
----------------
- spaCy pipeline configuration
- Text normalization settings
- Token filtering rules
- Linguistic feature extraction configuration
- Pattern configuration
- Language settings
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


# ==========================================================
# NORMALIZATION CONFIGURATION
# ==========================================================

@dataclass(frozen=True, slots=True)
class NormalizationConfig:
    """
    Controls input text normalization.
    """

    lowercase: bool = True
    strip_whitespace: bool = True
    normalize_whitespace: bool = True

    preserve_numbers: bool = True
    preserve_urls: bool =True
    preserve_emails: bool = True

    remove_html: bool = True


# ==========================================================
# TOKEN FILTER CONFIGURATION
# ==========================================================

@dataclass(frozen=True, slots=True)
class TokenFilterConfig:
    """
    Controls token filtering behaviour.
    """

    remove_stopwords: bool = False
    remove_punctuation: bool = False
    remove_symbols: bool = False

    minimum_token_length: int = 1
    maximum_token_length: int = 100


# ==========================================================
# LINGUISTIC FEATURE CONFIGURATION
# ==========================================================

@dataclass(frozen=True, slots=True)
class LinguisticFeatureConfig:
    """
    Controls which linguistic annotations are extracted from
    the spaCy document.

    These are descriptive annotations rather than fraud
    intelligence.
    """

    extract_tokens: bool = True

    extract_lemmas: bool = True

    extract_pos_tags: bool = True

    extract_sentences: bool = True

    extract_named_entities: bool = True

    extract_dependencies: bool = True

    extract_noun_chunks: bool = False

    extract_negations: bool = True


# ==========================================================
# SPACY CONFIGURATION
# ==========================================================

@dataclass(frozen=True, slots=True)
class SpacyConfig:
    """
    Configuration for the spaCy language pipeline.
    """

    model_name: str = "en_core_web_lg"

    disable_components: FrozenSet[str] = field(
        default_factory=frozenset
    )


# ==========================================================
# PATTERN CONFIGURATION
# ==========================================================

@dataclass(frozen=True, slots=True)
class PatternConfig:
    """
    Regular-expression patterns used during preprocessing.
    """

    email_pattern: str = (
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    url_pattern: str = (
        r"https?://\S+|www\.\S+"
    )

    whitespace_pattern: str = r"\s+"


# ==========================================================
# LANGUAGE CONFIGURATION
# ==========================================================

@dataclass(frozen=True, slots=True)
class LanguageConfig:
    """
    Language-specific preprocessing configuration.
    """

    language: str = "en"

    supported_languages: FrozenSet[str] = field(
        default_factory=lambda: frozenset({
            "en",
        })
    )


# ==========================================================
# MASTER CONFIGURATION
# ==========================================================

@dataclass(frozen=True, slots=True)
class PreprocessingConfig:
    """
    Master configuration for the preprocessing pipeline.
    """

    normalization: NormalizationConfig = field(
        default_factory=NormalizationConfig
    )

    token_filter: TokenFilterConfig = field(
        default_factory=TokenFilterConfig
    )

    linguistic: LinguisticFeatureConfig = field(
        default_factory=LinguisticFeatureConfig
    )

    spacy: SpacyConfig = field(
        default_factory=SpacyConfig
    )

    patterns: PatternConfig = field(
        default_factory=PatternConfig
    )

    language: LanguageConfig = field(
        default_factory=LanguageConfig
    )


# ==========================================================
# GLOBAL CONFIGURATION
# ==========================================================

PREPROCESSING_CONFIG = PreprocessingConfig()


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [
    "NormalizationConfig",
    "TokenFilterConfig",
    "LinguisticFeatureConfig",
    "SpacyConfig",
    "PatternConfig",
    "LanguageConfig",
    "PreprocessingConfig",
    "PREPROCESSING_CONFIG",
]