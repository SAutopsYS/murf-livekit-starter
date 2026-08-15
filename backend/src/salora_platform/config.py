"""Typed umbrella configuration. Reuses existing env names. One parse."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

EnvironmentProfile = Literal["development", "staging", "production"]


def _read(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _read_bool(name: str, default: bool) -> bool:
    raw = _read(name)
    if not raw:
        return default
    return raw.lower() not in {"0", "false", "no", "off"}


def _profile() -> EnvironmentProfile:
    explicit = _read("SALORA_PROFILE")
    if explicit in {"development", "staging", "production"}:
        return explicit  # type: ignore[return-value]
    if os.getenv("NODE_ENV") == "production" or _read("ENV") == "production":
        return "production"
    return "development"


@dataclass(frozen=True)
class PlatformConfig:
    profile: EnvironmentProfile
    auth_required: bool
    auth_secret: str
    livekit_url: str
    livekit_api_key: str
    livekit_api_secret: str
    murf_api_key: str
    deepgram_api_key: str
    google_api_key: str
    openai_api_key: str
    feature_analytics: bool
    feature_enterprise: bool
    feature_learning: bool

    @property
    def livekit_ready(self) -> bool:
        return bool(
            self.livekit_url and self.livekit_api_key and self.livekit_api_secret
        )

    @property
    def murf_ready(self) -> bool:
        return bool(self.murf_api_key)

    @property
    def stt_ready(self) -> bool:
        return bool(self.deepgram_api_key)

    @property
    def llm_ready(self) -> bool:
        return bool(self.google_api_key or self.openai_api_key)

    def provider_status(self) -> dict[str, bool]:
        return {
            "livekit": self.livekit_ready,
            "murf": self.murf_ready,
            "deepgram": self.stt_ready,
            "google": bool(self.google_api_key),
            "openai": bool(self.openai_api_key),
        }


_cache: PlatformConfig | None = None


def get_platform_config(*, force_reload: bool = False) -> PlatformConfig:
    global _cache
    if _cache is not None and not force_reload:
        return _cache
    _cache = PlatformConfig(
        profile=_profile(),
        auth_required=_read_bool("AUTH_REQUIRED", False),
        auth_secret=_read("SALORA_AUTH_SECRET") or _read("SESSION_SECRET"),
        livekit_url=_read("LIVEKIT_URL"),
        livekit_api_key=_read("LIVEKIT_API_KEY"),
        livekit_api_secret=_read("LIVEKIT_API_SECRET"),
        murf_api_key=_read("MURF_API_KEY"),
        deepgram_api_key=_read("DEEPGRAM_API_KEY"),
        google_api_key=_read("GOOGLE_API_KEY"),
        openai_api_key=_read("OPENAI_API_KEY"),
        feature_analytics=_read_bool("FEATURE_ANALYTICS", True),
        feature_enterprise=_read_bool("FEATURE_ENTERPRISE", True),
        feature_learning=_read_bool("FEATURE_LEARNING", True),
    )
    return _cache


def clear_platform_config() -> None:
    global _cache
    _cache = None
