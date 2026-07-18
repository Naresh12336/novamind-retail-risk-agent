"""
engine/text_preprocessor.py

Production-grade text preprocessing component for the NovaMind NLP Engine.

Responsibilities
----------------
- Input validation
- Text normalization
- spaCy document creation
- Token extraction
- Lemma extraction
- POS tag extraction
- Sentence segmentation

This module performs no fraud detection or scoring.
Its sole responsibility is converting raw text into a structured
PreprocessedText object.
"""

from __future__ import annotations

from typing import List

import spacy
from spacy.language import Language
from spacy.tokens import Doc

from engine.models.preprocessing_config import PREPROCESSING_CONFIG
from engine.nlp_types import PreprocessedText
from engine.nlp_utils import (
    normalize_text,
    validate_text,
)


class TextPreprocessor:
    """
    Performs deterministic preprocessing on raw transaction text.
    """

    def __init__(self) -> None:
        self.config = PREPROCESSING_CONFIG
        self.nlp = self._load_spacy_model()

    def _load_spacy_model(self) -> Language:
        """
        Load the configured spaCy language model.

        Raises
        ------
        RuntimeError
            If the configured model cannot be loaded.
        """

        model_name = self.config.spacy.model_name

        try:
            return spacy.load(model_name)

        except OSError as exc:
            raise RuntimeError(
                f"Unable to load spaCy model '{model_name}'. "
                "Install it using:\n"
                f"python -m spacy download {model_name}"
            ) from exc

    def _normalize_text(self, text: str) -> str:
        """
        Normalize input text according to preprocessing configuration.
        """

        text = validate_text(text)

        if self.config.normalization.lowercase:
            text = text.lower()

        if self.config.normalization.normalize_whitespace:
            text = normalize_text(text)

        return text

    @staticmethod
    def _extract_sentences(doc: Doc) -> List[str]:
        """
        Extract sentence strings from a spaCy document.
        """

        return [
            sentence.text.strip()
            for sentence in doc.sents
            if sentence.text.strip()
        ]

    @staticmethod
    def _extract_token_features(
            doc: Doc,
    ) -> tuple[List[str], List[str], List[str]]:
        """
        Extract token texts, lemmas and POS tags in a single pass.
        """

        tokens: List[str] = []
        lemmas: List[str] = []
        pos_tags: List[str] = []

        for token in doc:

            if token.is_space:
                continue

            tokens.append(token.text)
            lemmas.append(token.lemma_)
            pos_tags.append(token.pos_)

        return tokens, lemmas, pos_tags

    @staticmethod
    def _build_preprocessed_text(
        original_text: str,
        clean_text: str,
        tokens: List[str],
        lemmas: List[str],
        pos_tags: List[str],
        sentences: List[str],
    ) -> PreprocessedText:
        """
        Build the final immutable PreprocessedText object.
        """

        return PreprocessedText(
            original_text=original_text,
            clean_text=clean_text,
            tokens=tokens,
            lemmas=lemmas,
            pos_tags=pos_tags,
            sentences=sentences,
            token_count=len(tokens),
            sentence_count=len(sentences),
            character_count=len(clean_text),
            unique_token_count=len(set(tokens)),
        )

    def process(self, text: str) -> PreprocessedText:
        """
        Perform complete preprocessing.

        Parameters
        ----------
        text
            Raw transaction description.

        Returns
        -------
        PreprocessedText
            Structured preprocessing result.
        """

        original_text = text

        clean_text = self._normalize_text(text)

        doc = self.nlp(clean_text)

        sentences = self._extract_sentences(doc)

        tokens, lemmas, pos_tags = self._extract_token_features(doc)

        return self._build_preprocessed_text(
            original_text=original_text,
            clean_text=clean_text,
            tokens=tokens,
            lemmas=lemmas,
            pos_tags=pos_tags,
            sentences=sentences,
        )