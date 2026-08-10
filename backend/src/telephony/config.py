"""Cached telephony configuration loader.

Independent of memory/, knowledge/, tools/, and agent.py.
Never logs secrets.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

logger = logging.getLogger("telephony.config")

DEFAULT_CALLER_NAME = "VoiceForBharat Tutor"
DEFAULT_COUNTRY_CODE = "+91"


@dataclass(frozen=True)
class TelephonyConfig:
    """Typed telephony configuration for outbound calling readiness."""

    livekit_url: str
    livekit_api_key: str
    livekit_api_secret: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    outbound_caller_name: str
    default_country_code: str
    sip_outbound_trunk_id: str

    @property
    def livekit_ready(self) -> bool:
        """Return True when required LiveKit credentials are present."""
        return bool(
            self.livekit_url
            and self.livekit_api_key
            and self.livekit_api_secret
        )

    @property
    def twilio_ready(self) -> bool:
        """Return True when Twilio credentials needed for later phases exist."""
        return bool(
            self.twilio_account_sid
            and self.twilio_auth_token
            and self.twilio_phone_number
        )

    @property
    def outbound_ready(self) -> bool:
        """Return True when LiveKit credentials and SIP outbound trunk are set."""
        return self.livekit_ready and bool(self.sip_outbound_trunk_id)

    @property
    def is_valid(self) -> bool:
        """Phase 1 readiness requires LiveKit configuration."""
        return self.livekit_ready


_config_cache: TelephonyConfig | None = None


def _read_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _read_telephony_config() -> TelephonyConfig:
    country = _read_env("DEFAULT_COUNTRY_CODE", DEFAULT_COUNTRY_CODE)
    if country and not country.startswith("+"):
        country = f"+{country.lstrip('+')}"

    config = TelephonyConfig(
        livekit_url=_read_env("LIVEKIT_URL"),
        livekit_api_key=_read_env("LIVEKIT_API_KEY"),
        livekit_api_secret=_read_env("LIVEKIT_API_SECRET"),
        twilio_account_sid=_read_env("TWILIO_ACCOUNT_SID"),
        twilio_auth_token=_read_env("TWILIO_AUTH_TOKEN"),
        twilio_phone_number=_read_env("TWILIO_PHONE_NUMBER"),
        outbound_caller_name=(
            _read_env("OUTBOUND_CALLER_NAME", DEFAULT_CALLER_NAME)
            or DEFAULT_CALLER_NAME
        ),
        default_country_code=country or DEFAULT_COUNTRY_CODE,
        sip_outbound_trunk_id=_read_env("LIVEKIT_SIP_OUTBOUND_TRUNK_ID"),
    )

    if config.is_valid:
        logger.info("Telephony configuration loaded")
    else:
        logger.info("Telephony configuration invalid")
    return config


def get_telephony_config(*, force_reload: bool = False) -> TelephonyConfig:
    """Read telephony configuration once and cache the result."""
    global _config_cache
    if _config_cache is None or force_reload:
        _config_cache = _read_telephony_config()
    return _config_cache


def clear_telephony_config_cache() -> None:
    """Clear cached telephony configuration (used by tests)."""
    global _config_cache
    _config_cache = None
