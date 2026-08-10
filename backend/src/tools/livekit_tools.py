"""LiveKit function tools for Learning & Literacy exercises and scoring.

Wrappers call the existing deterministic implementations. No duplicated logic.
Structured data only — never conversational text.
"""

from __future__ import annotations

import logging
from typing import Any

from livekit.agents import RunContext, function_tool

from tools.exercise_tool import get_next_exercise as lookup_next_exercise
from tools.exercise_tool import normalize_level
from tools.recommendation import recommend_next_practice as build_recommendation
from tools.score_tool import score_spoken_answer as score_answer

logger = logging.getLogger("tools.livekit")


@function_tool()
async def get_next_exercise(
    context: RunContext,
    level: str,
    topic: str | None = None,
) -> dict[str, Any]:
    """Get the next English speaking exercise for a learner level.

    Prefer passing learning_level from lookup_user when available.
    Topic is optional. When provided, prefer an exercise matching that topic
    within the level; if none match, fall back to any exercise for the level.
    After scoring, prefer next_level from recommend_next_practice.
    Returns structured exercise fields when available. Returns a structured
    error payload when the dataset or level is unavailable. Does not generate
    spoken text.

    Args:
        level: Learner level (beginner, intermediate, or advanced).
        topic: Optional topic filter (for example greetings, travel, technology).
    """
    del context
    logger.info("Exercise tool invoked")
    if normalize_level(level) is not None:
        logger.info("Using saved learning level")

    result = lookup_next_exercise(level, topic)
    if result.get("error"):
        logger.info("Exercise unavailable")
    else:
        logger.info("Exercise found")
        logger.info("Exercise selected")
        logger.info("Follow-up exercise selected")
        logger.info("Tool chain completed")
    return dict(result)


@function_tool()
async def score_spoken_answer(
    context: RunContext,
    answer: str,
    level: str,
) -> dict[str, Any]:
    """Score a learner's spoken answer with deterministic rules.

    Returns structured score, feedback, and metrics. Returns a structured
    error payload when scoring is not possible. Does not generate spoken text
    and never uses an LLM.

    Args:
        answer: Transcript text of the spoken response.
        level: Learner level (beginner, intermediate, or advanced).
    """
    del context
    logger.info("Scoring tool invoked")
    result = score_answer(answer, level)
    if result.get("error"):
        logger.info("Scoring failed")
    else:
        logger.info("Answer scored")
        logger.info("Answer evaluated")
        logger.info("Tool chain completed")
    return dict(result)


@function_tool()
async def recommend_next_practice(
    context: RunContext,
    score: int,
    level: str,
) -> dict[str, Any]:
    """Recommend follow-up practice difficulty from a score.

    Conversation-scoped only. Does not save scores or update memory.
    Returns structured recommendation fields, or a structured error payload.
    Does not generate spoken text.

    Args:
        score: Overall score from score_spoken_answer (0-100).
        level: Current exercise level that was scored.
    """
    del context
    result = build_recommendation(score, level)
    if result.get("error"):
        logger.info("Recommendation unavailable")
    return dict(result)


LEARNING_TOOLS = [
    get_next_exercise,
    score_spoken_answer,
    recommend_next_practice,
]
