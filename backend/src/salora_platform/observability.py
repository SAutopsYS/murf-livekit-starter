"""Structured privacy-safe logs and in-process metrics. Does not replace stdlib loggers."""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Any

FORBIDDEN = re.compile(
    r"transcript|utterance|otp|phone|secret|password|token|api[_-]?key|prompt",
    re.IGNORECASE,
)

_counts: dict[str, float] = {}


def _redact(fields: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key, value in fields.items():
        if FORBIDDEN.search(key):
            continue
        if isinstance(value, str) and FORBIDDEN.search(value) and len(value) > 24:
            continue
        clean[key] = value
    return clean


def emit(level: str, event: str, **fields: Any) -> None:
    line = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        "event": event,
        **_redact(fields),
    }
    logging.getLogger("salora.platform").log(
        getattr(logging, level.upper(), logging.INFO),
        json.dumps(line, default=str),
    )


def record_metric(name: str, value: float = 1.0) -> None:
    _counts[name] = _counts.get(name, 0.0) + value


def metric_snapshot() -> dict[str, float]:
    return dict(_counts)


def reset_metrics() -> None:
    _counts.clear()


def heartbeat(service: str = "backend") -> None:
    record_metric("heartbeat")
    emit("info", "heartbeat", service=service)
