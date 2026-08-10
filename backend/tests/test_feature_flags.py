"""Day 6 Bonus 7: telephony feature flags and runtime controls."""

from __future__ import annotations

from typing import Any

import pytest

from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.features import (
    TelephonyFeatureFlags,
    clear_telephony_feature_flags,
    get_telephony_feature_flags,
)
from telephony.metrics import reset_telephony_metrics
from telephony.service import TelephonyService


class _FakeDialer:
    def place_outbound_call(
        self,
        *,
        phone_number: str,
        purpose: str,
        language: str,
        room_name: str | None = None,
    ) -> dict[str, Any]:
        del phone_number, room_name
        return {
            "status": "calling",
            "provider": "livekit",
            "call_id": "SCL_flags_1",
            "purpose": purpose,
            "language": language,
        }


@pytest.fixture(autouse=True)
def _reset(monkeypatch: pytest.MonkeyPatch):
    clear_telephony_config_cache()
    clear_telephony_feature_flags()
    reset_telephony_metrics()
    for key in (
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "LIVEKIT_SIP_OUTBOUND_TRUNK_ID",
        "TELEPHONY_ENABLED",
        "OUTBOUND_CALLING_ENABLED",
        "BOOTSTRAP_ENABLED",
        "LEARNING_ENABLED",
        "EVALUATION_ENABLED",
        "METRICS_ENABLED",
        "AUDIT_ENABLED",
        "DIAGNOSTICS_ENABLED",
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_telephony_config_cache()
    clear_telephony_feature_flags()
    reset_telephony_metrics()


def test_flags_load_defaults() -> None:
    flags = TelephonyFeatureFlags().snapshot()
    assert flags["telephony_enabled"] is True
    assert flags["outbound_calling_enabled"] is True
    assert flags["bootstrap_enabled"] is True
    assert flags["diagnostics_enabled"] is True


def test_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OUTBOUND_CALLING_ENABLED", "false")
    monkeypatch.setenv("BOOTSTRAP_ENABLED", "0")
    flags = TelephonyFeatureFlags().snapshot()
    assert flags["outbound_calling_enabled"] is False
    assert flags["bootstrap_enabled"] is False


def test_reload_updates_cached_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    manager = get_telephony_feature_flags()
    assert manager.flags.outbound_calling_enabled is True
    monkeypatch.setenv("OUTBOUND_CALLING_ENABLED", "false")
    manager.reload()
    assert manager.flags.outbound_calling_enabled is False
    snap = manager.snapshot()
    assert snap["outbound_calling_enabled"] is False


def test_disabled_feature_returns_structured_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID", "ST_test")
    monkeypatch.setenv("OUTBOUND_CALLING_ENABLED", "false")
    clear_telephony_feature_flags()
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        dialer=_FakeDialer(),
        feature_flags=get_telephony_feature_flags(force_reload=True),
    )
    result = service.place_call("9876543210", purpose="daily_practice")
    assert result == {"error": True, "message": "Feature disabled."}


def test_bootstrap_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("BOOTSTRAP_ENABLED", "false")
    clear_telephony_feature_flags()
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        feature_flags=get_telephony_feature_flags(force_reload=True),
    )
    result = service.build_outbound_intro(None, "daily_practice")
    assert result == {"error": True, "message": "Feature disabled."}
