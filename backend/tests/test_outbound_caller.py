"""Day 6 Phase 2: outbound call preparation (no real dialing)."""

from __future__ import annotations

import pytest

from telephony.caller import OutboundCaller, normalize_phone_number
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


def _ready_service(monkeypatch: pytest.MonkeyPatch) -> TelephonyService:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("DEFAULT_COUNTRY_CODE", "+91")
    return TelephonyService(get_telephony_config(force_reload=True))


def test_valid_phone_number() -> None:
    result = normalize_phone_number("+919876543210")
    assert result == "+919876543210"


def test_invalid_phone_number() -> None:
    for raw in ("12345", "abcd", "+++++", ""):
        result = normalize_phone_number(raw)
        assert isinstance(result, dict)
        assert result["error"] is True


def test_default_country_code_applied() -> None:
    result = normalize_phone_number("9876543210", default_country_code="+91")
    assert result == "+919876543210"

    with_zero = normalize_phone_number("09876543210", default_country_code="+91")
    assert with_zero == "+919876543210"


def test_prepare_call_returns_expected_structure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _ready_service(monkeypatch)
    prepared = service.prepare_call(
        phone_number="9876543210",
        purpose="daily_practice",
        language="en-IN",
    )
    assert prepared.get("error") is not True
    assert prepared["phone_number"] == "+919876543210"
    assert prepared["caller_name"] == "VoiceForBharat Tutor"
    assert prepared["purpose"] == "daily_practice"
    assert prepared["language"] == "en-IN"
    assert prepared["status"] == "prepared"


def test_prepare_call_respects_configuration_validation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    # Missing key/secret → not ready.
    service = TelephonyService(get_telephony_config(force_reload=True))
    result = service.prepare_call("9876543210", purpose="daily_practice")
    assert result["error"] is True
    assert "configuration" in result["message"].lower()


def test_outbound_caller_direct_invalid_purpose() -> None:
    caller = OutboundCaller(caller_name="VoiceForBharat Tutor")
    result = caller.prepare("+919876543210", purpose="   ")
    assert result["error"] is True
