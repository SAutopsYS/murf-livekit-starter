"""Strip secrets and learner content from enterprise payloads."""

from __future__ import annotations

import re
from typing import Any

BLOCKED_KEYS = frozenset(
    {
        "transcript",
        "transcripts",
        "spoken_answer",
        "learner_answer",
        "phone",
        "phone_number",
        "otp",
        "password",
        "secret",
        "api_key",
        "token",
        "chain_of_thought",
        "hidden_reasoning",
        "reasoning",
        "cot",
    }
)

_SECRET_PATTERN = re.compile(
    r"(?i)\b(otp|password|api[_-]?key|secret|bearer)\b\s*[:=]?\s*\S+"
)


def is_blocked_key(key: str) -> bool:
    lowered = key.lower().replace("-", "_")
    return lowered in BLOCKED_KEYS or any(part in lowered for part in BLOCKED_KEYS)


def sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return _SECRET_PATTERN.sub("[redacted]", value)
    if isinstance(value, dict):
        return sanitize_payload(value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    return value


def sanitize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key, value in payload.items():
        if is_blocked_key(str(key)):
            continue
        clean[str(key)] = sanitize_value(value)
    return clean
