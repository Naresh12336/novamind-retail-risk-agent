"""
engine/nlp.py

Top-level orchestration layer for the NovaMind NLP Engine.

This module coordinates every NLP component while remaining
free of NLP business logic itself.

Pipeline
--------
Raw Text
    │
    ▼
TextPreprocessor
    │
    ▼
PreprocessedText
    │
    ▼
RuleEngine
    │
    ▼
RuleFeatures
    │
    ▼
FeatureBundle
    │
    ▼
NLPResult

Future versions will integrate additional NLP modules such as:

    - IntentDetector
    - EntityExtractor
    - SentimentAnalyzer
    - StyleAnalyzer
    - EmbeddingEngine
    - ConfidenceAnalyzer
"""

from __future__ import annotations

from datetime import datetime

from engine.nlp_types import (
    FeatureBundle,
    NLPResult,
)

from engine.rule_engine import RuleEngine
from engine.text_preprocessor import TextPreprocessor


class NLPEngine:
    """
    Coordinates all NLP components.

    This class intentionally contains no NLP algorithms.
    It simply executes each processing stage and aggregates
    the resulting features.
    """

    def __init__(self) -> None:
        """
        Initialize all NLP modules.
        """

        self.preprocessor = TextPreprocessor()

        self.rule_engine = RuleEngine()

    def _extract_features(
        self,
        text: str,
    ) -> FeatureBundle:
        """
        Execute every NLP component and collect
        their outputs into a FeatureBundle.
        """

        bundle = FeatureBundle()

        #
        # Stage 1
        #
        preprocessing = self.preprocessor.process(text)

        bundle.preprocessing = preprocessing

        #
        # Stage 2
        #
        rule_features = self.rule_engine.extract(preprocessing)

        bundle.rule_features = rule_features

        #
        # Future stages
        #
        # bundle.intent_features = ...
        # bundle.entity_features = ...
        # bundle.sentiment_features = ...
        # bundle.embedding_features = ...

        return bundle

    def process(
        self,
        text: str,
    ) -> NLPResult:
        """
        Execute the complete NLP pipeline.

        Parameters
        ----------
        text
            Raw transaction text.

        Returns
        -------
        NLPResult
            Complete NLP analysis result.
        """

        features = self._extract_features(text)

        metadata = {
            "pipeline": "NovaMind NLP Engine",
            "version": "1.0",
            "processed_at": datetime.utcnow().isoformat(),
        }

        return NLPResult(
            features=features,
            metadata=metadata,
        )