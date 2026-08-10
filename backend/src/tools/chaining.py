"""Helpers for memory-aware learning tool chaining.

No LiveKit registration here. The LLM still decides when to call tools.
These helpers encode shared fallback rules for tests and future reuse.
"""

from __future__ import annotations

from typing import Any, Mapping

from tools.exercise_tool import VALID_LEVELS, normalize_level

LEVEL_FALLBACK_QUESTION = (
    "What is your English level? Beginner, Intermediate, or Advanced?"
)


def resolve_exercise_level(profile: Mapping[str, Any] | None) -> str | None:
    """Return a usable exercise level from a memory profile, if present.

    Args:
        profile: Structured learner profile from lookup_user, or None.

    Returns:
        Normalized beginner/intermediate/advanced, or None when missing/invalid.
    """
    if not profile:
        return None

    raw = profile.get("learning_level")
    if raw is None:
        return None
    if not isinstance(raw, str):
        raw = str(raw)

    normalized = normalize_level(raw)
    if normalized in VALID_LEVELS:
        return normalized
    return None


def should_ask_for_level(profile: Mapping[str, Any] | None) -> bool:
    """Return True when the tutor should ask the learner for their level."""
    return resolve_exercise_level(profile) is None
