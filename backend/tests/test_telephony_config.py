"""Day 6 Phase 1: telephony configuration and health checks."""

from __future__ import annotations

import pytest

from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.service import TelephonyService


@pytest.fixture(autouse=True)
def _reset_telephony_env(monkeypatch: pytest.MonkeyPatch):
    clear_telephony_config_cache()
    for key in (
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_PHONE_NUMBER",
        "OUTBOUND_CALLER_NAME",
        "DEFAULT_COUNTRY_CODE",
        "LIVEKIT_SIP_OUTBOUND_TRUNK_ID",
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_telephony_config_cache()


def test_configuration_loads(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("OUTBOUND_CALLER_NAME", "VoiceForBharat Tutor")
    monkeypatch.setenv("DEFAULT_COUNTRY_CODE", "+91")

    config = get_telephony_config(force_reload=True)
    assert config.is_valid is True
    assert config.outbound_caller_name == "VoiceForBharat Tutor"
    assert config.default_country_code == "+91"

    cached = get_telephony_config()
    assert cached is config


def test_missing_livekit_values_handled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    # Missing key/secret.
    config = get_telephony_config(force_reload=True)
    assert config.is_valid is False

    service = TelephonyService(config)
    assert service.is_ready() is False
    health = service.health()
    assert health["ready"] is False
    assert health["provider"] == "twilio"
    assert health["caller_name"] == "VoiceForBharat Tutor"


def test_health_and_ready_with_valid_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "sid")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "token")
    monkeypatch.setenv("TWILIO_PHONE_NUMBER", "+10000000000")

    service = TelephonyService(get_telephony_config(force_reload=True))
    assert service.is_ready() is True
    health = service.health()
    assert health["ready"] is True
    assert health["provider"] == "twilio"
    assert health["caller_name"] == "VoiceForBharat Tutor"
    assert health["livekit_configured"] is True
    assert health["twilio_configured"] is True
    assert isinstance(health.get("metrics"), dict)
    # Secrets must never appear in health payloads.
    dumped = str(health)
    assert "secret" not in dumped
    assert "token" not in dumped
