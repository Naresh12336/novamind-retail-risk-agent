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
from spacy.tokens import Doc, Token

from engine.models.preprocessing_config import PREPROCESSING_CONFIG
from engine.nlp_types import (
    DependencyRelation,
    NamedEntity,
    NegationMarker,
    PreprocessedText,
    TokenInfo,
)
from engine.nlp_utils import (
    normalize_text,
    validate_text,
)

from engine.pattern_extractor import PatternExtractor


class TextPreprocessor:
    """
    Performs deterministic preprocessing on raw transaction text.
    """

    def __init__(self) -> None:
        self.config = PREPROCESSING_CONFIG
        self.nlp = self._load_spacy_model()
        self.pattern_extractor = PatternExtractor()

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
            return spacy.load(
                model_name,
                disable=list(
                    self.config.spacy.disable_components
                ),
            )

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

        if self.config.normalization.strip_whitespace:
            text = text.strip()

        if self.config.normalization.lowercase:
            text = text.lower()

        if self.config.normalization.normalize_whitespace:
            text = normalize_text(text)

        return text

    def _should_keep_token(
            self,
            token: Token,
    ) -> bool:
        """
        Determine whether a token should be included in
        linguistic analysis.
        """

        filter_config = self.config.token_filter

        if token.is_space:
            return False

        if (
                filter_config.remove_stopwords
                and token.is_stop
        ):
            return False

        if (
                filter_config.remove_punctuation
                and token.is_punct
        ):
            return False

        if (
                filter_config.remove_symbols
                and token.is_currency
        ):
            return False

        token_length = len(token.text)

        if token_length < filter_config.minimum_token_length:
            return False

        if token_length > filter_config.maximum_token_length:
            return False

        return True

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

    def _extract_named_entities(
            self,
            doc: Doc,
    ) -> List[NamedEntity]:
        """
        Extract named entities from a spaCy document.

        Each entity contains its text, entity label,
        character offsets, and token offsets.
        """

        if not self.config.linguistic.extract_named_entities:
            return []

        entities: List[NamedEntity] = []

        for entity in doc.ents:
            entities.append(
                NamedEntity(
                    text=entity.text,
                    normalized_text=entity.text.strip().casefold(),
                    label=entity.label_,
                    start_char=entity.start_char,
                    end_char=entity.end_char,
                    start_token=entity.start,
                    end_token=entity.end,
                )
            )

        return entities

    def _extract_dependencies(
            self,
            doc: Doc,
    ) -> List[DependencyRelation]:
        """
        Extract grammatical dependency relations from a spaCy document.

        Each relation records the dependent token, its syntactic
        head, and the dependency label assigned by spaCy.
        """

        if not self.config.linguistic.extract_dependencies:
            return []

        dependencies: List[DependencyRelation] = []

        for token in doc:
            if token.is_space:
                continue

            dependencies.append(
                DependencyRelation(
                    token=token.text,
                    head=token.head.text,
                    dependency=token.dep_,
                )
            )

        return dependencies

    def _extract_noun_chunks(
            self,
            doc: Doc,
    ) -> List[str]:
        """
        Extract noun chunks from a spaCy document.
        """

        if not self.config.linguistic.extract_noun_chunks:
            return []

        return [
            chunk.text
            for chunk in doc.noun_chunks
        ]

    def _extract_negations(
            self,
            doc: Doc,
    ) -> List[NegationMarker]:
        """
        Extract negation markers and their associated targets.
        """

        if not self.config.linguistic.extract_negations:
            return []

        negations: List[NegationMarker] = []

        for token in doc:
            if token.is_space:
                continue

            is_dependency_negation = token.dep_ == "neg"

            is_determiner_no = (
                    token.lower_ == "no"
                    and token.pos_ == "DET"
                    and token.dep_ == "det"
            )

            if not (
                    is_dependency_negation
                    or is_determiner_no
            ):
                continue

            target_token = token.head

            negations.append(
                NegationMarker(
                    negation_word=token.text,
                    target=target_token.text,
                )
            )

        return negations

    def _extract_tokens(
            self,
            doc: Doc,
    ) -> List[TokenInfo]:
        """
        Extract structured token information from a spaCy document.

        Each retained spaCy token is converted into a TokenInfo object
        containing its text, lemma, and part-of-speech tag.
        """

        tokens: List[TokenInfo] = []

        for token in doc:

            if not self._should_keep_token(token):
                continue

            tokens.append(
                TokenInfo(
                    text=token.text,
                    lemma=token.lemma_,
                    pos=token.pos_,
                )
            )

        return tokens

    @staticmethod
    def _build_preprocessed_text(
            original_text: str,
            clean_text: str,
            tokens: List[TokenInfo],
            sentences: List[str],
            named_entities: List[NamedEntity],
            dependency_relations: List[DependencyRelation],
            noun_chunks: List[str],
            negations: List[NegationMarker],
    ) -> PreprocessedText:
        """
        Build the final PreprocessedText object from extracted
        linguistic information.
        """

        return PreprocessedText(
            original_text=original_text,
            clean_text=clean_text,
            tokens=tokens,
            sentences=sentences,
            named_entities=named_entities,
            dependency_relations=dependency_relations,
            noun_chunks=noun_chunks,
            negations=negations,
            token_count=len(tokens),
            sentence_count=len(sentences),
            character_count=len(clean_text),
            unique_token_count=len(
                {token.text for token in tokens}
            ),
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

        tokens = self._extract_tokens(doc)

        ner_doc = self.nlp(original_text)

        named_entities = self._extract_named_entities(ner_doc)

        pattern_entities = self.pattern_extractor.extract(original_text)

        named_entities.extend(pattern_entities)

        named_entities.sort(
            key=lambda entity: (
                entity.start_char,
                entity.end_char,
                entity.label,
            )
        )

        dependency_relations = self._extract_dependencies(doc)

        noun_chunks = self._extract_noun_chunks(doc)

        negations = self._extract_negations(doc)

        return self._build_preprocessed_text(
            original_text=original_text,
            clean_text=clean_text,
            tokens=tokens,
            sentences=sentences,
            named_entities=named_entities,
            dependency_relations=dependency_relations,
            noun_chunks=noun_chunks,
            negations=negations,
        )
