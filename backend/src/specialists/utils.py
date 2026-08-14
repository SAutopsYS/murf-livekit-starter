"""Shared specialist helpers. Reuses existing learning utilities."""

from __future__ import annotations

import re
from typing import Any

from specialists.prompts import LANGUAGE_RULES
from tools.chaining import resolve_exercise_level
from tools.exercise_tool import get_next_exercise as lookup_next_exercise
from tools.exercise_tool import normalize_level

_DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")
_ROMAN_HINDI_RE = re.compile(
    r"\b(mujhe|karni|karna|hai|hain|kya|kaise|chahiye|bahut|theek|"
    r"namaste|dhanyavaad|kripya|samajh|ganit)\b",
    re.IGNORECASE,
)


def inherit_language_policy() -> str:
    """Return the shared multilingual policy used by the Main Tutor."""
    return LANGUAGE_RULES


def normalize_language(value: str | None) -> str:
    """Normalize a language preference to en or hi."""
    if not isinstance(value, str) or not value.strip():
        return "en"
    lowered = value.strip().lower()
    if lowered in {"hi", "hindi", "hin", "devanagari"}:
        return "hi"
    if "hindi" in lowered:
        return "hi"
    return "en"


def detect_language(text: str, fallback: str = "en") -> str:
    """Detect en/hi from text. Devanagari or Hindi preference wins."""
    if not isinstance(text, str) or not text.strip():
        return normalize_language(fallback)
    if _DEVANAGARI_RE.search(text):
        return "hi"
    return normalize_language(fallback)


def contains_devanagari(text: str) -> bool:
    """Return True when text includes Devanagari characters."""
    return bool(isinstance(text, str) and _DEVANAGARI_RE.search(text))


def contains_romanized_hindi(text: str) -> bool:
    """Return True when text uses Romanized Hindi tokens."""
    return bool(isinstance(text, str) and _ROMAN_HINDI_RE.search(text))


def language_script_is_valid(text: str, language: str) -> bool:
    """Hindi replies must use Devanagari and must not be Roman-only."""
    if normalize_language(language) != "hi":
        return isinstance(text, str) and bool(text.strip())
    return contains_devanagari(text) and not contains_romanized_hindi(text)


def reuse_exercise_lookup(
    level: str,
    topic: str | None = None,
) -> dict[str, Any]:
    """Reuse the existing exercise repository. Does not generate exercises."""
    resolved = normalize_level(level) or resolve_exercise_level(
        {"learning_level": level}
    )
    if resolved is None:
        return {"error": True, "message": "Exercise dataset unavailable."}
    return dict(lookup_next_exercise(resolved, topic))


def reuse_knowledge_search(query: str) -> list[dict[str, Any]]:
    """Reuse the existing knowledge repository. Read-only."""
    from knowledge.search import search_knowledge

    if not isinstance(query, str) or not query.strip():
        return []
    return list(search_knowledge(query))
