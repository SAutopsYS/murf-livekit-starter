"""Fault-tolerant specialist start with one retry and Main Tutor fallback."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from specialists.events import log_specialist_event
from specialists.metrics import record_retry
from specialists.prompts import handoff_fallback_notice
from specialists.schemas import SpecialistContext

SpecialistFactory = Callable[..., Any]

STRUCTURED_FAILURES = {
    "not_registered": "specialist_unavailable",
    "disabled": "specialist_disabled",
    "timeout": "specialist_timeout",
    "init": "specialist_start_failed",
    "prompt": "prompt_load_failed",
    "context": "context_validation_failed",
    "runtime": "specialist_runtime_error",
}


def classify_failure(exc: BaseException | None, code: str = "") -> str:
    """Map exceptions to structured codes. Never expose stack traces."""
    if code in STRUCTURED_FAILURES.values():
        return code
    if code in STRUCTURED_FAILURES:
        return STRUCTURED_FAILURES[code]
    if isinstance(exc, TimeoutError):
        return "specialist_timeout"
    if exc is None:
        return "specialist_unavailable"
    text = str(exc).lower()
    if "prompt" in text:
        return "prompt_load_failed"
    if "context" in text:
        return "context_validation_failed"
    return "specialist_start_failed"


def start_specialist_with_retry(
    factory: SpecialistFactory | None,
    context: SpecialistContext,
    *,
    allow_retry: bool = True,
) -> tuple[Any | None, dict[str, Any]]:
    """Start a specialist. Retry once. Return structured error on failure."""
    if factory is None:
        log_specialist_event("recovery_triggered")
        return None, {
            "error": True,
            "code": "specialist_unavailable",
            "retried": False,
            "message": handoff_fallback_notice(context.language),
        }

    last_code = "specialist_start_failed"
    attempts = 0
    max_attempts = 2 if allow_retry else 1
    while attempts < max_attempts:
        attempts += 1
        if attempts > 1:
            log_specialist_event("retry_attempted")
            record_retry()
        try:
            agent = factory(context)
        except Exception as exc:
            last_code = classify_failure(exc)
            continue
        if agent is None:
            last_code = "specialist_start_failed"
            continue
        return agent, {"error": False, "retried": attempts > 1, "attempts": attempts}

    log_specialist_event("recovery_triggered")
    log_specialist_event("fallback_used")
    return None, {
        "error": True,
        "code": last_code,
        "retried": attempts > 1,
        "attempts": attempts,
        "message": handoff_fallback_notice(context.language),
    }
