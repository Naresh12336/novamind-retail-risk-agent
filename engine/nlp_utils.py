"""
engine/nlp_utils.py

Shared utility functions for the NovaMind NLP Engine.

This module contains reusable helper functions used across multiple NLP
components. It intentionally contains no fraud-specific logic.

Responsibilities
----------------
- Dataclass serialization
- JSON serialization
- Text normalization
- Collection utilities
- Basic validation
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, is_dataclass
from typing import Any, Iterable, List


# ==========================================================
# SERIALIZATION
# ==========================================================

def dataclass_to_dict(obj: Any) -> dict:
    """
    Convert a dataclass instance into a dictionary.

    Raises
    ------
    TypeError
        If obj is not a dataclass instance.
    """
    if not is_dataclass(obj):
        raise TypeError(
            f"Expected dataclass instance, received {type(obj).__name__}."
        )

    return asdict(obj)


def dataclass_to_json(
    obj: Any,
    *,
    indent: int = 4,
    sort_keys: bool = False,
) -> str:
    """
    Serialize a dataclass instance into a JSON string.
    """
    return json.dumps(
        dataclass_to_dict(obj),
        indent=indent,
        sort_keys=sort_keys,
        ensure_ascii=False,
    )


# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

_WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_whitespace(text: str) -> str:
    """
    Collapse multiple whitespace characters into a single space.
    """
    return _WHITESPACE_PATTERN.sub(" ", text).strip()


def normalize_text(text: str) -> str:
    """
    Perform lightweight text normalization.

    Current operations:
    - Trim leading/trailing whitespace
    - Convert to lowercase
    - Normalize internal whitespace

    Heavy NLP preprocessing belongs in TextPreprocessor.
    """
    text = text.lower()
    text = normalize_whitespace(text)

    return text


# ==========================================================
# COLLECTION UTILITIES
# ==========================================================

def unique_preserve_order(items: Iterable[Any]) -> List[Any]:
    """
    Remove duplicates while preserving insertion order.
    """
    seen = set()
    result = []

    for item in items:
        if item in seen:
            continue

        seen.add(item)
        result.append(item)

    return result


def flatten(iterables: Iterable[Iterable[Any]]) -> List[Any]:
    """
    Flatten an iterable of iterables into a single list.
    """
    return [item for iterable in iterables for item in iterable]


# ==========================================================
# VALIDATION
# ==========================================================

def validate_text(text: str) -> str:
    """
    Validate text before NLP processing.

    Raises
    ------
    TypeError
        If text is not a string.

    ValueError
        If text is empty after stripping.
    """
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    text = text.strip()

    if not text:
        raise ValueError("Input text cannot be empty.")

    return text


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [
    "dataclass_to_dict",
    "dataclass_to_json",
    "flatten",
    "normalize_text",
    "normalize_whitespace",
    "unique_preserve_order",
    "validate_text",
]