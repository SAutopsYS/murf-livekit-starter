"""In-memory provider health cache with cooldown.

No LiveKit code and no prompt logic. Health is process-local only.
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass

logger = logging.getLogger("tools.provider_health")

DEFAULT_COOLDOWN_SECONDS = 30.0


@dataclass(frozen=True)
class ProviderHealthConfig:
    """Cooldown configuration for the external exercise provider."""

    cooldown_seconds: float


_health_config_cache: ProviderHealthConfig | None = None


def _read_health_config() -> ProviderHealthConfig:
    raw = os.getenv(
        "EXERCISE_PROVIDER_COOLDOWN_SECONDS",
        str(DEFAULT_COOLDOWN_SECONDS),
    )
    try:
        cooldown = float(raw)
    except ValueError:
        cooldown = DEFAULT_COOLDOWN_SECONDS
    if cooldown < 0:
        cooldown = DEFAULT_COOLDOWN_SECONDS
    return ProviderHealthConfig(cooldown_seconds=cooldown)


def get_provider_health_config(*, force_reload: bool = False) -> ProviderHealthConfig:
    """Read provider cooldown configuration once (cached)."""
    global _health_config_cache
    if _health_config_cache is None or force_reload:
        _health_config_cache = _read_health_config()
    return _health_config_cache


def clear_provider_health_config_cache() -> None:
    """Clear cached cooldown configuration (used by tests)."""
    global _health_config_cache
    _health_config_cache = None


class ProviderHealth:
    """Track external provider availability and cooldown windows."""

    def __init__(self, cooldown_seconds: float | None = None) -> None:
        config = get_provider_health_config()
        self._cooldown_seconds = (
            config.cooldown_seconds
            if cooldown_seconds is None
            else float(cooldown_seconds)
        )
        self._unavailable_until: float | None = None
        self._was_in_cooldown = False

    @property
    def cooldown_seconds(self) -> float:
        return self._cooldown_seconds

    def is_available(self, *, now: float | None = None) -> bool:
        """Return True when API calls are allowed."""
        current = time.monotonic() if now is None else now
        if self._unavailable_until is None:
            return True

        if current < self._unavailable_until:
            logger.info("Cooldown active")
            self._was_in_cooldown = True
            return False

        logger.info("Cooldown expired")
        self._unavailable_until = None
        self._was_in_cooldown = True
        return True

    def mark_failure(self, *, now: float | None = None) -> None:
        """Mark the provider unavailable and start/restart cooldown."""
        current = time.monotonic() if now is None else now
        self._unavailable_until = current + self._cooldown_seconds
        self._was_in_cooldown = True
        logger.info("Exercise provider unavailable")
        logger.info("Cooldown started")

    def mark_success(self) -> None:
        """Reset health after a successful API response."""
        recovered = self._unavailable_until is not None or self._was_in_cooldown
        self._unavailable_until = None
        if recovered:
            logger.info("Provider recovered")
            self._was_in_cooldown = False
        else:
            logger.info("Exercise provider healthy")

    def reset(self) -> None:
        """Clear cooldown state (used by tests)."""
        self._unavailable_until = None
        self._was_in_cooldown = False


_default_health: ProviderHealth | None = None


def get_provider_health() -> ProviderHealth:
    """Return the process-wide provider health cache."""
    global _default_health
    if _default_health is None:
        _default_health = ProviderHealth()
    return _default_health


def reset_provider_health() -> None:
    """Reset the process-wide provider health cache (used by tests)."""
    global _default_health
    if _default_health is None:
        _default_health = ProviderHealth()
    else:
        _default_health.reset()
