"""
engine/models/preprocessing_config.py

Configuration for the NovaMind NLP preprocessing pipeline.

This module contains immutable configuration objects used by
TextPreprocessor. It intentionally contains no NLP logic.

Responsibilities
----------------
- spaCy model configuration
- Text normalization settings
- Token filtering rules
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
    Controls basic text normalization.
    """

    lowercase: bool = True
    strip_whitespace: bool = True
    normalize_whitespace: bool = True

    preserve_numbers: bool = True
    preserve_urls: bool = True
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
# SPACY CONFIGURATION
# ==========================================================

@dataclass(frozen=True, slots=True)
class SpacyConfig:
    """
    Configuration for spaCy.
    """

    model_name: str = "en_core_web_sm"

    enable_sentence_segmentation: bool = True
    enable_lemmatization: bool = True
    enable_pos_tagging: bool = True
    enable_named_entities: bool = False


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
    Language-specific preprocessing settings.
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
    Master preprocessing configuration.
    """

    normalization: NormalizationConfig = field(
        default_factory=NormalizationConfig
    )

    token_filter: TokenFilterConfig = field(
        default_factory=TokenFilterConfig
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
# GLOBAL CONFIGURATION INSTANCE
# ==========================================================

PREPROCESSING_CONFIG = PreprocessingConfig()


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [
    "NormalizationConfig",
    "TokenFilterConfig",
    "SpacyConfig",
    "PatternConfig",
    "LanguageConfig",
    "PreprocessingConfig",
    "PREPROCESSING_CONFIG",
]