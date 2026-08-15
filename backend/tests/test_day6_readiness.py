"""Day 6 Final Phase: outbound telephony production-readiness smoke tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from telephony.bootstrap import ConversationBootstrap
from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.coordinator import OutboundConversationCoordinator
from telephony.livekit_client import LiveKitTelephonyClient
from telephony.outcomes import CallOutcomeManager
from telephony.service import TelephonyService, get_telephony_service
from telephony.session import OutboundLearningSession
from tools import get_tool_manager, get_tool_metrics, list_tools, reset_tool_metrics
from tools.request_cache import RequestCache
from tools.session_cache import SessionExerciseCache


class _FakeDialer:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.calls = 0

    def place_outbound_call(
        self,
        *,
        phone_number: str,
        purpose: str,
        language: str,
        room_name: str | None = None,
    ) -> dict[str, Any]:
        del phone_number, room_name
        self.calls += 1
        if self.fail:
            return {"error": True, "message": "Unable to place outbound call."}
        return {
            "status": "calling",
            "provider": "livekit",
            "call_id": "SCL_ready_1",
            "purpose": purpose,
            "language": language,
            "room_name": "outbound-ready",
            "participant_identity": "sip-outbound-ready",
        }


@pytest.fixture(autouse=True)
def _reset_env(monkeypatch: pytest.MonkeyPatch):
    clear_telephony_config_cache()
    reset_tool_metrics()
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
    reset_tool_metrics()


def _ready(monkeypatch: pytest.MonkeyPatch, *, trunk: bool = True) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")
    monkeypatch.setenv("OUTBOUND_CALLER_NAME", "VoiceForBharat Tutor")
    monkeypatch.setenv("DEFAULT_COUNTRY_CODE", "+91")
    if trunk:
        monkeypatch.setenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID", "ST_test")


def test_scenario_telephony_startup(monkeypatch: pytest.MonkeyPatch) -> None:
    _ready(monkeypatch)
    config = get_telephony_config(force_reload=True)
    assert config.is_valid is True
    service = TelephonyService(config)
    assert service.is_ready() is True
    health = service.health()
    assert health["ready"] is True
    assert health["caller_name"] == "VoiceForBharat Tutor"
    assert "secret" not in str(health)


def test_scenario_outbound_call_structured(monkeypatch: pytest.MonkeyPatch) -> None:
    _ready(monkeypatch)
    dialer = _FakeDialer()
    service = TelephonyService(get_telephony_config(force_reload=True), dialer=dialer)
    result = service.place_call("9876543210", purpose="daily_practice")
    assert result.get("error") is not True
    assert result["status"] == "calling"
    assert result["provider"] == "livekit"
    assert result["call_id"]
    assert "CreateSIPParticipant" not in str(result)
    assert dialer.calls == 1


def test_scenario_bootstrap_scripts() -> None:
    en = ConversationBootstrap().build_intro(None, "daily_practice", "en-IN")
    hi = ConversationBootstrap().build_intro(None, "daily_practice", "hi-IN")
    assert "VoiceForBharat Tutor" in en["intro"]
    assert "stop" in en["intro"].lower()
    assert "नमस्ते" in hi["intro"]
    assert "Namaste" not in hi["intro"]


def test_scenario_daily_practice_and_missing_learner() -> None:
    ready = OutboundConversationCoordinator(
        lookup_user_fn=lambda _uid: {"learning_level": "beginner"},
        get_next_exercise_fn=lambda level, **_k: {
            "level": level,
            "topic": "Greetings",
            "title": "Introduce Yourself",
            "exercise": "Introduce yourself.",
            "id": "b1",
            "source": "local_dataset",
        },
    ).start_daily_practice("learner_1")
    assert ready["status"] == "ready"
    assert ready["exercise"]["topic"] == "Greetings"

    missing = OutboundConversationCoordinator(
        lookup_user_fn=lambda _uid: None,
    ).start_daily_practice("unknown")
    assert missing == {
        "status": "needs_setup",
        "reason": "learning_level_missing",
    }


def test_scenario_speaking_evaluation() -> None:
    result = OutboundLearningSession(
        lookup_user_fn=lambda _uid: {"learning_level": "beginner"},
        score_fn=lambda _a, level: {
            "score": 82,
            "level": level,
            "feedback": [],
            "metrics": {"word_count": 20, "unique_words": 14, "sentence_count": 3},
            "source": "rule_based",
        },
        recommend_fn=lambda score, level: {
            "recommendation": "advance_level",
            "reason": "ready",
            "next_level": "intermediate",
        },
        get_next_exercise_fn=lambda level, **_k: {
            "level": level,
            "topic": "Travel",
            "title": "Booking a Hotel",
            "exercise": "Describe booking a hotel.",
            "id": "i1",
            "source": "local_dataset",
        },
    ).evaluate_practice(
        "learner_1", "A long enough spoken answer for evaluation today."
    )
    assert result["score"] == 82
    assert result["recommendation"] == "advance_level"
    assert result["follow_up"]["title"] == "Booking a Hotel"
    assert "score_spoken_answer" not in str(result)


def test_scenario_call_outcomes() -> None:
    manager = CallOutcomeManager()
    mapping = {
        "answered": (False, True),
        "busy": (True, False),
        "rejected": (False, False),
        "voicemail": (False, False),
        "failed": (True, False),
        "no_answer": (True, False),
    }
    for status, (retry, completed) in mapping.items():
        result = manager.classify(status)
        assert result["status"] in {status, "no_answer"}
        assert result["retry_recommended"] is retry
        assert result["completed"] is completed


def test_scenario_livekit_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    _ready(monkeypatch)
    service = TelephonyService(
        get_telephony_config(force_reload=True),
        dialer=_FakeDialer(fail=True),
    )
    result = service.place_call("9876543210", purpose="daily_practice")
    assert result == {
        "error": True,
        "message": "Unable to place outbound call.",
    }


def test_scenario_restart_reloads_config(monkeypatch: pytest.MonkeyPatch) -> None:
    _ready(monkeypatch)
    first = get_telephony_service(force_reload=True)
    assert first.is_ready() is True
    monkeypatch.setenv("OUTBOUND_CALLER_NAME", "Reloaded Tutor")
    second = get_telephony_service(force_reload=True)
    assert second.config.outbound_caller_name == "Reloaded Tutor"


def test_day5_layers_still_active() -> None:
    assert len(list_tools()) == 3
    managed = get_tool_manager().execute("get_next_exercise", level="beginner")
    assert managed.get("error") is not True
    metrics = get_tool_metrics()
    assert metrics["exercise_tool"]["calls"] >= 1

    cache = SessionExerciseCache()
    request_cache = RequestCache(ttl_seconds=0)
    from tools.exercise_tool import get_next_exercise

    one = get_next_exercise(
        "beginner",
        source="local",
        cache=cache,
        request_cache=request_cache,
    )
    two = get_next_exercise(
        "beginner",
        source="local",
        cache=cache,
        request_cache=request_cache,
    )
    assert one["id"] != two["id"]


def test_datasets_and_client_surface() -> None:
    root = Path(__file__).resolve().parents[1] / "src"
    assert (root / "tools" / "resources" / "exercises.json").exists()
    assert (root / "knowledge" / "resources" / "english_basics.json").exists()
    assert hasattr(LiveKitTelephonyClient, "place_outbound_call")
