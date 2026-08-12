"""Deterministic PII / sensitive-data sanitization for escalations."""

from __future__ import annotations

import logging
import re
from typing import Any

from escalation.models import NOTIFICATION_FIELDS

logger = logging.getLogger("escalation.sanitizer")

_REDACTED = "[REDACTED]"
_REFERENCE_ID_RE = re.compile(r"\bESC-\d{6,}\b", re.IGNORECASE)

# Preserve reference IDs while redacting surrounding sensitive content.
_LABELLED_SECRET_RE = re.compile(
    r"(?i)\b("
    r"otp|one[-\s]?time\s*password|pin|password|passwd|passcode|"
    r"account\s*(?:number|no\.?|#)?|card\s*(?:number|no\.?|#)?|"
    r"auth(?:entication)?\s*token|access\s*token|api\s*key|secret"
    r")\b(\s*(?:is|=|:)\s*)[\"']?([^\s,\"']+)"
)
_CARD_RE = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
_LONG_NUMERIC_RE = re.compile(r"\b\d{8,}\b")
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(
    r"(?<!\w)(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{4}(?!\w)"
)
_TOKEN_RE = re.compile(r"\b(?:Bearer\s+)?[A-Za-z0-9_-]{24,}\b")


class EscalationSanitizer:
    """Detect and redact obvious sensitive values from escalation text."""

    def sanitize_summary(self, summary: str) -> str:
        """Return a redacted summary. Never raises."""
        try:
            if not isinstance(summary, str):
                return ""
            text = summary
            placeholders: dict[str, str] = {}

            def _protect(match: re.Match[str]) -> str:
                key = f"__ESC_REF_{len(placeholders)}__"
                placeholders[key] = match.group(0)
                return key

            text = _REFERENCE_ID_RE.sub(_protect, text)
            redacted_any = False

            def _labelled(match: re.Match[str]) -> str:
                nonlocal redacted_any
                redacted_any = True
                return f"{match.group(1)}{match.group(2)}{_REDACTED}"

            text = _LABELLED_SECRET_RE.sub(_labelled, text)

            for pattern in (
                _CARD_RE,
                _EMAIL_RE,
                _PHONE_RE,
                _TOKEN_RE,
                _LONG_NUMERIC_RE,
            ):
                updated, count = pattern.subn(_REDACTED, text)
                if count:
                    redacted_any = True
                    text = updated

            for key, value in placeholders.items():
                text = text.replace(key, value)

            if redacted_any:
                logger.info("Sensitive data redacted")
            return text
        except Exception:
            return _REDACTED

    def sanitize_escalation(self, escalation: dict[str, Any]) -> dict[str, Any] | None:
        """Return a new sanitized notification payload. Never mutates input."""
        try:
            if not isinstance(escalation, dict):
                return None
            source = dict(escalation)
            summary = self.sanitize_summary(str(source.get("summary", "")))
            safe: dict[str, Any] = {
                "reference_id": str(source.get("reference_id", "")),
                "reason": str(source.get("reason", "")),
                "summary": summary,
                "urgency": str(source.get("urgency", "medium")),
                "language": str(source.get("language", "en")),
                "status": str(source.get("status", "open")),
            }
            # Drop anything outside the approved notification fields.
            safe = {key: safe[key] for key in NOTIFICATION_FIELDS}
            logger.info("Escalation sanitized")
            return safe
        except Exception:
            return None
