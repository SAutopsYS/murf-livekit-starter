"""Exercise validation and sanitization for Learning & Literacy tools.

One validator for API and local sources. No LiveKit code and no prompt logic.
"""

from __future__ import annotations

import logging
from typing import Any, TypedDict

logger = logging.getLogger("tools.validator")


class ValidationSuccess(TypedDict):
    """Successful validation payload."""

    valid: bool
    exercise: dict[str, str]


class ValidationFailure(TypedDict):
    """Failed validation payload."""

    valid: bool
    reason: str


class ExerciseValidator:
    """Validate and sanitize exercise objects before delivery."""

    REQUIRED_FIELDS = ("id", "topic", "title", "exercise")

    def validate(self, payload: Any) -> ValidationSuccess | ValidationFailure:
        """Validate structure and return a sanitized exercise when valid."""
        if not isinstance(payload, dict):
            logger.info("Invalid provider response")
            return {"valid": False, "reason": "not_an_object"}

        sanitized: dict[str, str] = {}
        for field in self.REQUIRED_FIELDS:
            if field not in payload:
                logger.info("Invalid provider response")
                return {"valid": False, "reason": f"missing_{field}"}
            value = payload[field]
            if not isinstance(value, str):
                logger.info("Invalid provider response")
                return {"valid": False, "reason": f"invalid_type_{field}"}
            cleaned = value.strip()
            if not cleaned:
                logger.info("Invalid provider response")
                return {"valid": False, "reason": f"empty_{field}"}
            sanitized[field] = cleaned

        # Optional passthrough fields used by the exercise pipeline.
        for optional in ("level", "source"):
            raw = payload.get(optional)
            if isinstance(raw, str) and raw.strip():
                sanitized[optional] = raw.strip()

        logger.info("Exercise validated")
        return {"valid": True, "exercise": sanitized}

    def sanitize(self, payload: Any) -> dict[str, str] | None:
        """Return a sanitized exercise dict, or None when invalid."""
        result = self.validate(payload)
        if not result["valid"]:
            return None
        return result["exercise"]  # type: ignore[return-value]


_default_validator = ExerciseValidator()


def get_exercise_validator() -> ExerciseValidator:
    """Return the shared exercise validator."""
    return _default_validator
