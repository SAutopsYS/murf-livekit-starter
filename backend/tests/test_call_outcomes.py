"""Day 6 Phase 7: outbound call outcome classification."""

from __future__ import annotations

import pytest

from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.outcomes import CallOutcomeManager
from telephony.service import TelephonyService


@pytest.fixture(autouse=True)
def _reset_telephony_env(monkeypatch: pytest.MonkeyPatch):
    clear_telephony_config_cache()
    yield
    clear_telephony_config_cache()


@pytest.mark.parametrize(
    ("provider_status", "expected_status", "retry", "completed"),
    [
        ("answered", "answered", False, True),
        ("busy", "busy", True, False),
        ("no_answer", "no_answer", True, False),
        ("voicemail", "voicemail", False, False),
        ("rejected", "rejected", False, False),
        ("failed", "failed", True, False),
    ],
)
def test_outcome_mapping(
    provider_status: str,
    expected_status: str,
    retry: bool,
    completed: bool,
) -> None:
    result = CallOutcomeManager().classify(provider_status)
    assert result["status"] == expected_status
    assert result["retry_recommended"] is retry
    assert result["completed"] is completed
    assert result["next_action"]


def test_invalid_status_handled() -> None:
    result = CallOutcomeManager().classify("???")
    assert result["status"] == "failed"
    assert result["retry_recommended"] is True


def test_service_handle_call_outcome(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    service = TelephonyService(get_telephony_config(force_reload=True))
    result = service.handle_call_outcome("busy")
    assert result["status"] == "busy"
    assert result["retry_recommended"] is True
    assert result["next_action"] == "retry_later"
