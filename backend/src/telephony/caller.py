"""Outbound call preparation helpers.

No network calls, Twilio SDK, or LiveKit telephony APIs in this phase.
"""

from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any, TypedDict

logger = logging.getLogger("telephony.caller")

_E164_RE = re.compile(r"^\+[1-9]\d{7,14}$")
_DIGITS_RE = re.compile(r"\D+")


class PhoneValidationError(TypedDict):
    """Structured phone validation failure."""

    error: bool
    message: str


@dataclass(frozen=True)
class OutboundCallRequest:
    """Prepared outbound call metadata (not yet dialed)."""

    phone_number: str
    caller_name: str
    purpose: str
    language: str = "en-IN"
    status: str = "prepared"
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable structured payload."""
        return asdict(self)


def normalize_phone_number(
    phone_number: str,
    *,
    default_country_code: str = "+91",
) -> str | PhoneValidationError:
    """Normalize a phone number toward E.164.

    Never raises. Returns a structured error payload when invalid.
    """
    if not isinstance(phone_number, str):
        logger.info("Invalid phone number")
        return {"error": True, "message": "Invalid phone number."}

    cleaned = phone_number.strip()
    if not cleaned:
        logger.info("Invalid phone number")
        return {"error": True, "message": "Invalid phone number."}

    # Reject clearly non-numeric junk early.
    if re.fullmatch(r"[+\s()-]*", cleaned) or re.search(r"[A-Za-z]", cleaned):
        logger.info("Invalid phone number")
        return {"error": True, "message": "Invalid phone number."}

    if cleaned.startswith("00"):
        cleaned = f"+{cleaned[2:]}"

    if cleaned.startswith("+"):
        digits = _DIGITS_RE.sub("", cleaned[1:])
        candidate = f"+{digits}"
    else:
        digits = _DIGITS_RE.sub("", cleaned)
        # Common local form: leading 0 then national number.
        if digits.startswith("0"):
            digits = digits[1:]
        country_digits = default_country_code.lstrip("+")
        if digits.startswith(country_digits):
            candidate = f"+{digits}"
        else:
            candidate = f"+{country_digits}{digits}"

    if not _E164_RE.fullmatch(candidate):
        logger.info("Invalid phone number")
        return {"error": True, "message": "Invalid phone number."}

    logger.info("Phone number validated")
    return candidate


class OutboundCaller:
    """Prepare outbound call requests without placing calls."""

    def __init__(
        self,
        *,
        caller_name: str,
        default_country_code: str = "+91",
    ) -> None:
        self.caller_name = caller_name
        self.default_country_code = default_country_code

    def prepare(
        self,
        phone_number: str,
        purpose: str,
        language: str = "en-IN",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Validate inputs and return structured prepared-call metadata."""
        logger.info("Preparing outbound call")

        if not isinstance(purpose, str) or not purpose.strip():
            return {"error": True, "message": "Invalid call purpose."}
        if not isinstance(language, str) or not language.strip():
            return {"error": True, "message": "Invalid call language."}

        normalized = normalize_phone_number(
            phone_number,
            default_country_code=self.default_country_code,
        )
        if isinstance(normalized, dict) and normalized.get("error"):
            return normalized

        request = OutboundCallRequest(
            phone_number=str(normalized),
            caller_name=self.caller_name,
            purpose=purpose.strip(),
            language=language.strip(),
            status="prepared",
            metadata=dict(metadata or {}),
        )
        logger.info("Outbound call prepared")
        return request.as_dict()
