"""Typed platform errors. Voice fail-closed stays in specialists/recovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Domain = Literal["user", "developer", "ai", "voice", "network", "auth", "config"]
Recovery = Literal["retry", "fallback", "reconnect", "none"]


@dataclass(frozen=True)
class PlatformError(Exception):
    code: str
    domain: Domain
    message: str
    user_message: str
    retryable: bool
    recovery: Recovery
    status: int

    def __str__(self) -> str:
        return self.message


ERRORS = {
    "AUTH_REQUIRED": PlatformError(
        "AUTH_REQUIRED",
        "auth",
        "Authentication required.",
        "Sign in to open this instrument.",
        False,
        "none",
        401,
    ),
    "AUTH_FORBIDDEN": PlatformError(
        "AUTH_FORBIDDEN",
        "auth",
        "Role cannot use this instrument.",
        "This role cannot open this surface.",
        False,
        "none",
        403,
    ),
    "CONFIG_MISSING": PlatformError(
        "CONFIG_MISSING",
        "config",
        "Required configuration is missing.",
        "The worker is not ready.",
        False,
        "none",
        500,
    ),
    "NETWORK": PlatformError(
        "NETWORK",
        "network",
        "Upstream unavailable.",
        "Temporarily unavailable.",
        True,
        "retry",
        503,
    ),
    "AI_FALLBACK": PlatformError(
        "AI_FALLBACK",
        "ai",
        "Provider failed closed.",
        "The host stayed on the line.",
        True,
        "fallback",
        503,
    ),
    "VOICE_SESSION": PlatformError(
        "VOICE_SESSION",
        "voice",
        "Voice session failed.",
        "The session ended.",
        True,
        "reconnect",
        503,
    ),
}


def platform_error(code: str) -> PlatformError:
    return ERRORS[code]
