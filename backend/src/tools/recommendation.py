"""Deterministic follow-up practice recommendations.

Conversation-scoped only. Does not persist scores or update memory.
"""

from __future__ import annotations

import logging
from typing import Literal, TypedDict

from tools.exercise_tool import VALID_LEVELS, normalize_level
from tools.metrics import track_tool_call

logger = logging.getLogger("tools.recommendation")

RecommendationKind = Literal[
    "repeat_same_level",
    "continue_same_level",
    "advance_level",
]

_LEVEL_ORDER = ("beginner", "intermediate", "advanced")

_RECOMMENDATION_UNAVAILABLE = {
    "error": True,
    "message": "Practice recommendation unavailable.",
}


class RecommendationResult(TypedDict):
    """Structured follow-up practice recommendation."""

    recommendation: RecommendationKind
    reason: str
    next_level: str


class RecommendationError(TypedDict):
    """Structured failure payload for recommendation requests."""

    error: bool
    message: str


def _next_higher_level(level: str) -> str | None:
    try:
        index = _LEVEL_ORDER.index(level)
    except ValueError:
        return None
    if index >= len(_LEVEL_ORDER) - 1:
        return None
    return _LEVEL_ORDER[index + 1]


def _recommend_next_practice_impl(
    score: int,
    level: str,
) -> RecommendationResult | RecommendationError:
    if not isinstance(score, int) or isinstance(score, bool):
        return dict(_RECOMMENDATION_UNAVAILABLE)  # type: ignore[return-value]
    if score < 0 or score > 100:
        return dict(_RECOMMENDATION_UNAVAILABLE)  # type: ignore[return-value]

    normalized = normalize_level(level)
    if normalized is None or normalized not in VALID_LEVELS:
        return dict(_RECOMMENDATION_UNAVAILABLE)  # type: ignore[return-value]

    if score < 50:
        result: RecommendationResult = {
            "recommendation": "repeat_same_level",
            "reason": "Learner should practice more before advancing.",
            "next_level": normalized,
        }
        logger.info("Recommendation generated")
        logger.info("Repeating level")
        return result

    if score < 80:
        result = {
            "recommendation": "continue_same_level",
            "reason": "Learner is progressing and should continue at the current level.",
            "next_level": normalized,
        }
        logger.info("Recommendation generated")
        logger.info("Repeating level")
        return result

    higher = _next_higher_level(normalized)
    if higher is None:
        result = {
            "recommendation": "continue_same_level",
            "reason": "Learner is performing well at the highest available level.",
            "next_level": normalized,
        }
        logger.info("Recommendation generated")
        logger.info("Repeating level")
        return result

    result = {
        "recommendation": "advance_level",
        "reason": "Learner is ready for a more challenging speaking exercise.",
        "next_level": higher,
    }
    logger.info("Recommendation generated")
    logger.info("Advancing learner")
    return result


def recommend_next_practice(score: int, level: str) -> RecommendationResult | RecommendationError:
    """Recommend the next practice difficulty from a spoken-answer score.

    Args:
        score: Overall score from 0 to 100.
        level: Current learner level used for the scored exercise.

    Returns:
        Structured recommendation data, or a structured error payload.
    """
    return track_tool_call(
        "recommendation_tool",
        _recommend_next_practice_impl,
        score,
        level,
    )
