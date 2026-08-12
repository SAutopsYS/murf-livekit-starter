"""Discord webhook delivery for human-help escalation notifications."""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any, Callable

from escalation.sanitizer import EscalationSanitizer

logger = logging.getLogger("escalation.notifier")

WebhookPoster = Callable[[str, dict[str, Any]], tuple[bool, int]]


def _env_webhook_url() -> str:
    return (os.getenv("ESCALATION_WEBHOOK_URL") or "").strip()


def _default_poster(webhook_url: str, payload: dict[str, Any]) -> tuple[bool, int]:
    """POST JSON content to the webhook. Returns (ok, status_code)."""
    body = json.dumps({"content": json.dumps(payload, ensure_ascii=False)}).encode(
        "utf-8"
    )
    request = urllib.request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        return 200 <= int(response.status) < 300, int(response.status)


class EscalationNotifier:
    """Send sanitized escalation payloads to a human-help webhook."""

    def __init__(
        self,
        webhook_url: str | None = None,
        *,
        sanitizer: EscalationSanitizer | None = None,
        poster: WebhookPoster | None = None,
    ) -> None:
        self._webhook_url = (
            webhook_url.strip() if isinstance(webhook_url, str) else _env_webhook_url()
        )
        self._sanitizer = sanitizer or EscalationSanitizer()
        self._poster = poster or _default_poster

    @property
    def configured(self) -> bool:
        """True when a webhook URL is present."""
        return bool(self._webhook_url)

    def send(self, escalation: dict[str, Any]) -> dict[str, Any]:
        """Sanitize then notify. Never exposes secrets or raises to callers."""
        logger.info("Human-help notification started")

        safe = self._sanitizer.sanitize_escalation(escalation)
        if safe is None:
            logger.info("Human-help notification unavailable")
            return {"notification": "unavailable"}

        if not self._webhook_url:
            logger.info("Human-help notification unavailable")
            return {"notification": "unavailable", "payload": safe}

        try:
            ok, _status = self._poster(self._webhook_url, safe)
            if not ok:
                logger.info("Human-help notification unavailable")
                return {"notification": "unavailable", "payload": safe}
            logger.info("Human-help notification delivered")
            return {"notification": "delivered", "payload": safe}
        except (urllib.error.URLError, TimeoutError, OSError, ValueError, TypeError):
            logger.info("Human-help notification unavailable")
            return {"notification": "unavailable", "payload": safe}
        except Exception:
            logger.info("Human-help notification unavailable")
            return {"notification": "unavailable", "payload": safe}
