"""
engine/rule_engine.py

Deterministic rule-based feature extraction for the NovaMind NLP pipeline.

This module identifies fraud-related keywords and categories using the
configured keyword registry. It does not perform risk scoring or decision-making.

Pipeline
--------
PreprocessedText
        │
        ▼
RuleEngine
        │
        ▼
RuleFeatures
"""

from __future__ import annotations

from typing import List

from engine.models.keyword_config import KEYWORD_CATEGORIES
from engine.nlp_types import (
    PreprocessedText,
    RuleFeatures,
)


class RuleEngine:
    """
    Extract deterministic fraud indicators from preprocessed text.
    """

    def __init__(self) -> None:
        self.categories = KEYWORD_CATEGORIES

    def _extract_rule_features(
            self,
            preprocessed: PreprocessedText,
    ) -> RuleFeatures:
        """
        Extract deterministic rule-based features from preprocessed text.
        """

        keyword_hits: list[str] = []

        matched_categories: set[str] = set()

        money_terms: list[str] = []
        payment_terms: list[str] = []
        account_terms: list[str] = []
        security_terms: list[str] = []
        legal_terms: list[str] = []
        scam_terms: list[str] = []

        for token in preprocessed.tokens:

            token = token.lower()

            for category in self.categories.values():

                if token not in category.keywords:
                    continue

                keyword_hits.append(token)

                matched_categories.add(category.name)

                if category.name == "BANKING":
                    money_terms.append(token)

                elif category.name == "PAYMENT":
                    payment_terms.append(token)

                elif category.name == "ACCOUNT":
                    account_terms.append(token)

                elif category.name == "SECURITY":
                    security_terms.append(token)

                elif category.name == "LEGAL":
                    legal_terms.append(token)

                elif category.name in (
                        "PHISHING",
                        "IMPERSONATION",
                        "SOCIAL_ENGINEERING",
                ):
                    scam_terms.append(token)

        return RuleFeatures(
            keyword_hits=sorted(set(keyword_hits)),
            matched_categories=sorted(matched_categories),

            keyword_count=len(keyword_hits),
            category_count=len(matched_categories),

            urgency_flag="URGENCY" in matched_categories,

            money_terms=sorted(set(money_terms)),
            payment_terms=sorted(set(payment_terms)),
            account_terms=sorted(set(account_terms)),
            security_terms=sorted(set(security_terms)),
            legal_terms=sorted(set(legal_terms)),
            scam_terms=sorted(set(scam_terms)),
        )

    @staticmethod
    def _build_rule_features(
            matched_keywords: List[str],
            matched_categories: List[str],
    ) -> RuleFeatures:

        category_set = set(matched_categories)

        return RuleFeatures(
            keyword_hits=matched_keywords,
            matched_categories=matched_categories,

            keyword_count=len(matched_keywords),
            category_count=len(matched_categories),

            urgency_flag="URGENCY" in category_set,
        )

    def extract(
            self,
            preprocessed: PreprocessedText,
    ) -> RuleFeatures:
        """
        Public API for deterministic rule extraction.
        """

        return self._extract_rule_features(preprocessed)