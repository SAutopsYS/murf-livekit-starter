"""Outbound call audit logger (in-memory logging only).

Never persists data. Never logs learner PII, phone numbers, or secrets.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

logger = logging.getLogger("telephony.audit")

SUPPORTED_EVENTS: frozenset[str] = frozenset(
    {
        "call_started",
        "bootstrap_completed",
        "learning_started",
        "exercise_prepared",
        "evaluation_completed",
        "recommendation_generated",
        "follow_up_prepared",
        "outcome_processed",
        "call_completed",
        "call_failed",
    }
)

_SENSITIVE_KEYS: frozenset[str] = frozenset(
    {
        "phone_number",
        "learner_id",
        "learner_name",
        "spoken_answer",
        "transcript",
        "token",
        "api_key",
        "api_secret",
        "auth_token",
        "password",
        "secret",
    }
)


def sanitize_metadata(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    """Return a sanitized, deterministic metadata dict (no sensitive keys)."""
    if not metadata:
        return {}
    cleaned: dict[str, Any] = {}
    for key in sorted(metadata.keys()):
        if key is None:
            continue
        name = str(key)
        if name.lower() in _SENSITIVE_KEYS:
            continue
        value = metadata[key]
        if value is None:
            continue
        cleaned[name] = value
    return cleaned


def log_event(
    event: str,
    metadata: Mapping[str, Any] | None = None,
) -> None:
    """Emit one structured audit log line."""
    name = (event or "").strip()
    if not name:
        return
    safe = sanitize_metadata(metadata)
    if safe:
        logger.info("Audit event: %s | %s", name, safe)
    else:
        logger.info("Audit event: %s", name)


class CallAuditLogger:
    """Record outbound call lifecycle events as structured logs."""

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = enabled
        logger.info("Call audit logger initialized")

    @property
    def enabled(self) -> bool:
        return self._enabled

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def log_event(
        self,
        event: str,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        """Record a supported lifecycle event (no-op when disabled)."""
        if not self._enabled:
            return
        name = (event or "").strip()
        if name not in SUPPORTED_EVENTS:
            return
        log_event(name, metadata)
