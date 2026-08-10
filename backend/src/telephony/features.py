"""Runtime feature flags for the telephony subsystem.

Loaded from environment variables. Cached in-process. No persistence.
"""

from __future__ import annotations

import logging
import os
from dataclasses import asdict, dataclass
from typing import Any

logger = logging.getLogger("telephony.features")


def _read_bool(name: str, default: bool = True) -> bool:
    raw = os.getenv(name)
    if raw is None or not str(raw).strip():
        return default
    value = str(raw).strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    return default


@dataclass(frozen=True)
class FeatureFlags:
    """Typed telephony feature flag snapshot."""

    telephony_enabled: bool = True
    outbound_calling_enabled: bool = True
    bootstrap_enabled: bool = True
    learning_enabled: bool = True
    evaluation_enabled: bool = True
    metrics_enabled: bool = True
    audit_enabled: bool = True
    diagnostics_enabled: bool = True

    def snapshot(self) -> dict[str, bool]:
        return asdict(self)


class TelephonyFeatureFlags:
    """Load and cache telephony feature flags from the environment."""

    def __init__(self) -> None:
        self._flags = self._load()
        logger.info("Feature flags loaded")

    def _load(self) -> FeatureFlags:
        return FeatureFlags(
            telephony_enabled=_read_bool("TELEPHONY_ENABLED", True),
            outbound_calling_enabled=_read_bool("OUTBOUND_CALLING_ENABLED", True),
            bootstrap_enabled=_read_bool("BOOTSTRAP_ENABLED", True),
            learning_enabled=_read_bool("LEARNING_ENABLED", True),
            evaluation_enabled=_read_bool("EVALUATION_ENABLED", True),
            metrics_enabled=_read_bool("METRICS_ENABLED", True),
            audit_enabled=_read_bool("AUDIT_ENABLED", True),
            diagnostics_enabled=_read_bool("DIAGNOSTICS_ENABLED", True),
        )

    @property
    def flags(self) -> FeatureFlags:
        return self._flags

    def snapshot(self) -> dict[str, bool]:
        logger.info("Feature snapshot requested")
        return self._flags.snapshot()

    def reload(self) -> None:
        self._flags = self._load()
        logger.info("Feature flags reloaded")

    def is_enabled(self, feature: str) -> bool:
        mapping = self._flags.snapshot()
        return bool(mapping.get(feature, True))


_default_flags: TelephonyFeatureFlags | None = None


def get_telephony_feature_flags(*, force_reload: bool = False) -> TelephonyFeatureFlags:
    """Return the process-wide feature flag cache."""
    global _default_flags
    if _default_flags is None:
        _default_flags = TelephonyFeatureFlags()
    elif force_reload:
        _default_flags.reload()
    return _default_flags


def clear_telephony_feature_flags() -> None:
    """Clear cached feature flags (tests)."""
    global _default_flags
    _default_flags = None


def feature_disabled_response() -> dict[str, Any]:
    """Structured error returned when a telephony feature is disabled."""
    logger.info("Feature disabled")
    return {
        "error": True,
        "message": "Feature disabled.",
    }
