"""Input checks, privacy rules, audit. Complements escalation/sanitizer.py."""

from __future__ import annotations

import re

from salora_platform.observability import emit

SAFE_TOKEN = re.compile(r"^[a-zA-Z0-9_-]{0,64}$")
SAFE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

PRIVACY_RULES = {
    "no_utterance_fields": True,
    "no_transcript_logs": True,
    "consent_before_memory": True,
    "forget_must_complete": True,
    "analytics_anonymous": True,
}


def valid_token(value: str | None) -> bool:
    if value is None or value == "":
        return True
    return bool(SAFE_TOKEN.match(value))


def valid_date(value: str | None) -> bool:
    if value is None or value == "":
        return True
    return bool(SAFE_DATE.match(value))


def audit(event: str, **fields: object) -> None:
    emit("info", f"audit.{event}", **fields)
