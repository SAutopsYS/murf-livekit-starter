"""Call-lifecycle helpers that delegate to AnalyticsService.

Isolated from LiveKit session architecture. Failures never raise to callers.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from analytics.service import AnalyticsService, get_analytics_service

logger = logging.getLogger("analytics.integration")


def _safe_call_id(call_id: str | None) -> str:
    if isinstance(call_id, str) and call_id.strip():
        return call_id.strip()
    return f"call-{uuid.uuid4()}"


def start_call_analytics(
    call_id: str | None,
    channel: str,
    language: str,
    *,
    service: AnalyticsService | None = None,
) -> dict[str, Any]:
    """Create an analytics start record. Never raises."""
    analytics = service or get_analytics_service()
    try:
        result = analytics.start_call(
            call_id=_safe_call_id(call_id),
            channel=channel,
            language=language or "en-IN",
        )
        if result.get("error"):
            logger.info("Analytics integration unavailable")
            return result
        logger.info("Call analytics started")
        return result
    except Exception:
        logger.info("Analytics integration unavailable")
        return {"error": True, "message": "Analytics integration unavailable."}


def complete_call_analytics(
    call_id: str | None,
    outcome: str,
    *,
    failure_type: str | None = None,
    service: AnalyticsService | None = None,
) -> dict[str, Any]:
    """Complete an analytics record with an explicit outcome. Never raises."""
    if not isinstance(call_id, str) or not call_id.strip():
        logger.info("Analytics integration unavailable")
        return {"error": True, "message": "Call record unavailable."}
    analytics = service or get_analytics_service()
    try:
        result = analytics.complete_call(
            call_id=call_id.strip(),
            outcome=outcome,
            failure_type=failure_type,
        )
        if result.get("error"):
            logger.info("Analytics integration unavailable")
            return result
        logger.info("Call analytics completed")
        return result
    except Exception:
        logger.info("Analytics integration unavailable")
        return {"error": True, "message": "Analytics integration unavailable."}


def mark_first_response_analytics(
    call_id: str | None,
    *,
    service: AnalyticsService | None = None,
) -> dict[str, Any]:
    if not isinstance(call_id, str) or not call_id.strip():
        return {"error": True, "message": "Call record unavailable."}
    analytics = service or get_analytics_service()
    try:
        return analytics.mark_first_response(call_id.strip())
    except Exception:
        logger.info("Analytics integration unavailable")
        return {"error": True, "message": "Analytics integration unavailable."}
