"""Outbound learning session evaluation using Day 5 tools.

No LiveKit/Twilio code and no prompt logic.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from memory.tools import fetch_user_memory
from tools.chaining import resolve_exercise_level
from tools.exercise_tool import get_next_exercise
from tools.recommendation import recommend_next_practice
from tools.score_tool import score_spoken_answer

logger = logging.getLogger("telephony.session")

_EVAL_UNAVAILABLE = {
    "error": True,
    "message": "Unable to evaluate spoken answer.",
}

LookupFn = Callable[[str], dict[str, Any] | None]
ScoreFn = Callable[[str, str], dict[str, Any]]
RecommendFn = Callable[[int, str], dict[str, Any]]
ExerciseFn = Callable[..., dict[str, Any]]


class OutboundLearningSession:
    """Coordinate scoring and follow-up practice for one outbound session."""

    def __init__(
        self,
        *,
        lookup_user_fn: LookupFn | None = None,
        score_fn: ScoreFn | None = None,
        recommend_fn: RecommendFn | None = None,
        get_next_exercise_fn: ExerciseFn | None = None,
    ) -> None:
        self._lookup_user = lookup_user_fn or fetch_user_memory
        self._score = score_fn or score_spoken_answer
        self._recommend = recommend_fn or recommend_next_practice
        self._get_next_exercise = get_next_exercise_fn or get_next_exercise

    def evaluate_practice(
        self,
        learner_id: str,
        spoken_answer: str,
    ) -> dict[str, Any]:
        """Score an answer, recommend next practice, optionally fetch follow-up.

        Returns structured session results. Never raises.
        """
        logger.info("Outbound evaluation started")

        if not isinstance(learner_id, str) or not learner_id.strip():
            return dict(_EVAL_UNAVAILABLE)
        if not isinstance(spoken_answer, str) or not spoken_answer.strip():
            return dict(_EVAL_UNAVAILABLE)

        try:
            profile = self._lookup_user(learner_id.strip())
            level = resolve_exercise_level(profile)
            if level is None:
                return dict(_EVAL_UNAVAILABLE)

            scored = self._score(spoken_answer, level)
            if not isinstance(scored, dict) or scored.get("error"):
                return dict(_EVAL_UNAVAILABLE)

            logger.info("Answer evaluated")
            score_value = scored.get("score")
            if not isinstance(score_value, int):
                return dict(_EVAL_UNAVAILABLE)

            recommendation = self._recommend(score_value, level)
            if not isinstance(recommendation, dict) or recommendation.get("error"):
                return dict(_EVAL_UNAVAILABLE)

            logger.info("Recommendation generated")
            next_level = str(recommendation.get("next_level") or level)
            recommendation_kind = str(
                recommendation.get("recommendation") or "continue_same_level"
            )

            payload: dict[str, Any] = {
                "score": score_value,
                "recommendation": recommendation_kind,
                "level": level,
            }

            # Offer a follow-up exercise for continue/repeat/advance recommendations.
            if recommendation_kind in {
                "repeat_same_level",
                "continue_same_level",
                "advance_level",
            }:
                follow_up = self._get_next_exercise(next_level)
                if isinstance(follow_up, dict) and not follow_up.get("error"):
                    payload["follow_up"] = {
                        "topic": follow_up.get("topic", ""),
                        "title": follow_up.get("title", ""),
                        "level": follow_up.get("level", next_level),
                    }
                    logger.info("Follow-up exercise prepared")

            logger.info("Outbound session completed")
            return payload
        except Exception:
            return dict(_EVAL_UNAVAILABLE)
