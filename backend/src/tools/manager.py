"""Centralized execution pipeline for Learning & Literacy tools.

Internal orchestration only. LiveKit registration remains unchanged.
"""

from __future__ import annotations

import logging
from typing import Any

from tools.registry import ToolRegistry, get_tool_registry
from tools.validator import ExerciseValidator, get_exercise_validator

logger = logging.getLogger("tools.manager")

_EXECUTION_UNAVAILABLE = {
    "error": True,
    "message": "Tool execution unavailable.",
}


class ToolManager:
    """Execute registered learning tools through one standardized pipeline."""

    def __init__(
        self,
        registry: ToolRegistry | None = None,
        validator: ExerciseValidator | None = None,
    ) -> None:
        self._registry = registry or get_tool_registry()
        self._validator = validator or get_exercise_validator()

    def _validate_input(self, name: str, params: dict[str, Any]) -> bool:
        if name == "get_next_exercise":
            level = params.get("level")
            return isinstance(level, str) and bool(level.strip())
        if name == "score_spoken_answer":
            return isinstance(params.get("answer"), str) and isinstance(
                params.get("level"),
                str,
            )
        if name == "recommend_next_practice":
            score = params.get("score")
            level = params.get("level")
            return isinstance(score, int) and not isinstance(score, bool) and isinstance(
                level,
                str,
            )
        return False

    def _validate_output(self, name: str, result: Any) -> dict[str, Any]:
        if not isinstance(result, dict):
            logger.info("Tool execution failed")
            return dict(_EXECUTION_UNAVAILABLE)

        if result.get("error") is True:
            return result

        if name == "get_next_exercise":
            validated = self._validator.validate(result)
            if not validated["valid"]:
                logger.info("Tool execution failed")
                return dict(_EXECUTION_UNAVAILABLE)
            logger.info("Response validated")
            merged = dict(result)
            merged.update(validated["exercise"])  # type: ignore[index]
            logger.info("Sanitized exercise delivered")
            return merged

        logger.info("Response validated")
        return result

    def execute(self, name: str, **params: Any) -> dict[str, Any]:
        """Run one registered tool through the centralized pipeline."""
        logger.info("Tool execution started")
        if not self._validate_input(name, params):
            logger.info("Tool execution failed")
            return dict(_EXECUTION_UNAVAILABLE)

        fn = self._registry.get_callable(name)
        if fn is None:
            logger.info("Tool execution failed")
            return dict(_EXECUTION_UNAVAILABLE)

        try:
            raw = fn(**params)
        except Exception:
            logger.info("Tool execution failed")
            return dict(_EXECUTION_UNAVAILABLE)

        logger.info("Metrics recorded")
        result = self._validate_output(name, raw)
        if result.get("error") is True:
            logger.info("Tool execution failed")
            return result

        logger.info("Tool execution completed")
        return result


_default_manager: ToolManager | None = None


def get_tool_manager() -> ToolManager:
    """Return the process-wide tool manager."""
    global _default_manager
    if _default_manager is None:
        _default_manager = ToolManager()
    return _default_manager
