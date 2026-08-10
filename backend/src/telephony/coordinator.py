"""Outbound conversation coordinator bridging telephony and Day 5 learning tools.

No LiveKit SDK, Twilio, or prompt generation.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from memory.tools import fetch_user_memory
from tools.chaining import resolve_exercise_level
from tools.exercise_tool import get_next_exercise

logger = logging.getLogger("telephony.coordinator")

LookupFn = Callable[[str], dict[str, Any] | None]
ExerciseFn = Callable[..., dict[str, Any]]


class OutboundConversationCoordinator:
    """Start an outbound daily-practice learning session using existing tools."""

    def __init__(
        self,
        *,
        lookup_user_fn: LookupFn | None = None,
        get_next_exercise_fn: ExerciseFn | None = None,
    ) -> None:
        # lookup_user LiveKit tool delegates to fetch_user_memory; reuse that path.
        self._lookup_user = lookup_user_fn or fetch_user_memory
        self._get_next_exercise = get_next_exercise_fn or get_next_exercise

    def start_daily_practice(self, learner_id: str) -> dict[str, Any]:
        """Lookup learner level and prepare the next speaking exercise.

        Returns structured conversation state. Never raises.
        """
        logger.info("Outbound learning started")

        if not isinstance(learner_id, str) or not learner_id.strip():
            return {
                "status": "needs_setup",
                "reason": "learning_level_missing",
            }

        try:
            profile = self._lookup_user(learner_id.strip())
        except Exception:
            return {
                "status": "needs_setup",
                "reason": "learning_level_missing",
            }

        if profile is not None:
            logger.info("Learner profile located")

        level = resolve_exercise_level(profile)
        if level is None:
            return {
                "status": "needs_setup",
                "reason": "learning_level_missing",
            }

        try:
            exercise = self._get_next_exercise(level)
        except Exception:
            return {
                "status": "needs_setup",
                "reason": "learning_level_missing",
            }

        if not isinstance(exercise, dict) or exercise.get("error"):
            return {
                "status": "needs_setup",
                "reason": "learning_level_missing",
            }

        logger.info("Exercise prepared")
        logger.info("Outbound tutor ready")
        return {
            "status": "ready",
            "level": level,
            "exercise": {
                "topic": exercise.get("topic", ""),
                "title": exercise.get("title", ""),
            },
        }
