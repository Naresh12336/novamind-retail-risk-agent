
"""Pattern-based extraction of email addresses and URLs."""

import re
from typing import List

from engine.models.preprocessing_config import PREPROCESSING_CONFIG
from engine.nlp_types import NamedEntity
from engine.nlp_utils import validate_text


class PatternExtractor:
    """Extract email and URL candidates from raw text."""

    def __init__(self) -> None:
        self.config = PREPROCESSING_CONFIG.patterns
        self.email_regex = re.compile(self.config.email_pattern)
        self.url_regex = re.compile(self.config.url_pattern)

    @staticmethod
    def _make_entity(
        text: str,
        label: str,
        start: int,
        end: int,
    ) -> NamedEntity:
        return NamedEntity(
            text=text,
            normalized_text=text.strip().casefold(),
            label=label,
            start_char=start,
            end_char=end,
            start_token=-1,
            end_token=-1,
        )

    @staticmethod
    def _trim_url_punctuation(
            candidate: str,
    ) -> str:
        """Remove trailing sentence punctuation from a URL candidate."""
        while candidate and candidate[-1] in ".,!?;:":
            candidate = candidate[:-1]

        # Remove unmatched closing parentheses or brackets.
        pairs = {")": "(", "]": "["}

        while candidate and candidate[-1] in pairs:
            closing = candidate[-1]
            opening = pairs[closing]

            if candidate.count(closing) > candidate.count(opening):
                candidate = candidate[:-1]
            else:
                break

        return candidate

    def extract(self, text: str) -> List[NamedEntity]:
        """Extract email and URL candidates with original-text offsets."""
        text = validate_text(text)
        entities: List[NamedEntity] = []

        for match in self.email_regex.finditer(text):
            candidate = match.group(0)

            entities.append(
                self._make_entity(
                    text=candidate,
                    label="EMAIL",
                    start=match.start(),
                    end=match.end(),
                )
            )

        for match in self.url_regex.finditer(text):
            raw_candidate = match.group(0)
            candidate = self._trim_url_punctuation(raw_candidate)

            if not candidate:
                continue

            entities.append(
                self._make_entity(
                    text=candidate,
                    label="URL",
                    start=match.start(),
                    end=match.start() + len(candidate),
                )
            )

        return sorted(
            entities,
            key=lambda entity: (
                entity.start_char,
                entity.end_char,
                entity.label,
            ),
        )


