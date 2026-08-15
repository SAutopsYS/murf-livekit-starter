"""Day 6 Phase 3: LiveKit outbound call integration (mocked network)."""

from __future__ import annotations

from typing import Any

import pytest

from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.livekit_client import LiveKitTelephonyClient
from telephony.service import TelephonyService


class _FakeDialer:
    def __init__(
        self, result: dict[str, Any] | None = None, *, fail: bool = False
    ) -> None:
        self.fail = fail
        self.result = result or {
            "status": "calling",
            "provider": "livekit",
            "call_id": "SCL_test_123",
            "purpose": "daily_practice",
            "language": "en-IN",
            "room_name": "outbound-daily_practice-test",
            "participant_identity": "sip-outbound-test",
        }
        self.calls: list[dict[str, Any]] = []

    def place_outbound_call(
        self,
        *,
        phone_number: str,
        purpose: str,
        language: str,
        room_name: str | None = None,
    ) -> dict[str, Any]:
        self.calls.append(
            {
                "phone_number": phone_number,
                "purpose": purpose,
                "language": language,
                "room_name": room_name,
            }
        )
        if self.fail:
            raise RuntimeError("livekit down")
        return dict(self.result)


@pytest.fixture(autouse=True)
def _reset_telephony_env(monkeypatch: pytest.MonkeyPatch):
    clear_telephony_config_cache()
    for key in (
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "LIVEKIT_SIP_OUTBOUND_TRUNK_ID",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_PHONE_NUMBER",
        "OUTBOUND_CALLER_NAME",
        "DEFAULT_COUNTRY_CODE",
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_telephony_config_cache()


def _set_ready(monkeypatch: pytest.MonkeyPatch, *, trunk: bool = True) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("DEFAULT_COUNTRY_CODE", "+91")
    if trunk:
        monkeypatch.setenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID", "ST_test_trunk")


def test_livekit_client_initializes(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_ready(monkeypatch)
    client = LiveKitTelephonyClient(get_telephony_config(force_reload=True))
    assert client.is_configured() is True


def test_successful_outbound_request(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_ready(monkeypatch)
    dialer = _FakeDialer()
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        dialer=dialer,
    )
    result = service.place_call(
        phone_number="9876543210",
        purpose="daily_practice",
        language="en-IN",
    )
    assert result.get("error") is not True
    assert result["status"] == "calling"
    assert result["provider"] == "livekit"
    assert result["call_id"] == "SCL_test_123"
    assert result["purpose"] == "daily_practice"
    assert "bootstrap" in result
    assert dialer.calls
    assert dialer.calls[0]["phone_number"] == "+919876543210"


def test_configuration_failure_handled(monkeypatch: pytest.MonkeyPatch) -> None:
    # Missing LiveKit credentials.
    service = TelephonyService(
        get_telephony_config(force_reload=True), dialer=_FakeDialer()
    )
    result = service.place_call("9876543210", purpose="daily_practice")
    assert result == {
        "error": True,
        "message": "Unable to place outbound call.",
    }


def test_missing_trunk_handled(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_ready(monkeypatch, trunk=False)
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        dialer=LiveKitTelephonyClient(get_telephony_config()),
    )
    result = service.place_call("9876543210", purpose="daily_practice")
    assert result["error"] is True


def test_livekit_failure_handled(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_ready(monkeypatch)
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        dialer=_FakeDialer(fail=True),
    )
    result = service.place_call("9876543210", purpose="daily_practice")
    assert result == {
        "error": True,
        "message": "Unable to place outbound call.",
    }


def test_structured_error_for_invalid_destination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_ready(monkeypatch)
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        dialer=_FakeDialer(),
    )
    result = service.place_call("abcd", purpose="daily_practice")
    assert result["error"] is True
    assert "Unable to place outbound call." in result["message"]
