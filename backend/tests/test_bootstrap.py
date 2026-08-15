"""Day 6 Phase 4: outbound conversation bootstrap."""

from __future__ import annotations

import pytest

from telephony.bootstrap import ConversationBootstrap
from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.service import TelephonyService


@pytest.fixture(autouse=True)
def _reset_telephony_env(monkeypatch: pytest.MonkeyPatch):
    clear_telephony_config_cache()
    for key in (
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "LIVEKIT_SIP_OUTBOUND_TRUNK_ID",
        "OUTBOUND_CALLER_NAME",
        "DEFAULT_COUNTRY_CODE",
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_telephony_config_cache()


def test_intro_generated_with_purpose_and_stop() -> None:
    bootstrap = ConversationBootstrap()
    result = bootstrap.build_intro(
        learner_name=None,
        purpose="daily_practice",
        language="en-IN",
    )
    assert result["purpose"] == "daily_practice"
    assert result["language"] == "en-IN"
    assert "VoiceForBharat Tutor" in result["intro"]
    assert "daily english speaking practice" in result["intro"].lower()
    assert "stop" in result["intro"].lower()
    assert result["includes_stop_instruction"] is True


def test_english_unchanged() -> None:
    intro = ConversationBootstrap().build_intro(None, "daily_practice", "en-IN")[
        "intro"
    ]
    assert "Hello" in intro
    assert "नमस्ते" not in intro


def test_hindi_uses_devanagari() -> None:
    intro = ConversationBootstrap().build_intro(None, "daily_practice", "hi-IN")[
        "intro"
    ]
    assert "नमस्ते" in intro
    assert "VoiceForBharat Tutor" in intro
    assert "Namaste" not in intro
    assert "बंद" in intro


def test_service_integration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    service = TelephonyService(get_telephony_config(force_reload=True))
    result = service.build_outbound_intro(
        learner_name=None,
        purpose="speaking_practice",
        language="en-IN",
    )
    assert result.get("error") is not True
    assert "intro" in result
    assert result["purpose"] == "speaking_practice"
