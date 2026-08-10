"""Day 6 Phase 6: outbound speaking evaluation session."""

from __future__ import annotations

import pytest

from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.service import TelephonyService
from telephony.session import OutboundLearningSession


@pytest.fixture(autouse=True)
def _reset_telephony_env(monkeypatch: pytest.MonkeyPatch):
    clear_telephony_config_cache()
    for key in (
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "LIVEKIT_SIP_OUTBOUND_TRUNK_ID",
    ):
        monkeypatch.delenv(key, raising=False)
    yield
    clear_telephony_config_cache()


def test_speaking_evaluation_and_follow_up() -> None:
    session = OutboundLearningSession(
        lookup_user_fn=lambda _uid: {"learning_level": "beginner"},
        score_fn=lambda _answer, level: {
            "score": 88,
            "level": level,
            "feedback": ["Good"],
            "metrics": {"word_count": 20, "unique_words": 15, "sentence_count": 3},
            "source": "rule_based",
        },
        recommend_fn=lambda score, level: {
            "recommendation": "advance_level",
            "reason": "ready",
            "next_level": "intermediate",
            "score": score,
            "level": level,
        },
        get_next_exercise_fn=lambda level, **_k: {
            "level": level,
            "topic": "Travel",
            "title": "Booking a Hotel",
            "exercise": "Describe booking a hotel.",
            "source": "local_dataset",
            "id": "i1",
        },
    )
    result = session.evaluate_practice(
        "learner_1",
        "This is a long enough spoken practice answer for scoring.",
    )
    assert result.get("error") is not True
    assert result["score"] == 88
    assert result["recommendation"] == "advance_level"
    assert result["follow_up"] == {
        "topic": "Travel",
        "title": "Booking a Hotel",
        "level": "intermediate",
    }


def test_error_handling_for_failed_score() -> None:
    session = OutboundLearningSession(
        lookup_user_fn=lambda _uid: {"learning_level": "beginner"},
        score_fn=lambda *_a, **_k: {
            "error": True,
            "message": "Unable to score the spoken answer.",
        },
    )
    result = session.evaluate_practice("learner_1", "short")
    assert result == {
        "error": True,
        "message": "Unable to evaluate spoken answer.",
    }


def test_service_integration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")

    service = TelephonyService(
        get_telephony_config(force_reload=True),
        learning_session=OutboundLearningSession(
            lookup_user_fn=lambda _uid: {"learning_level": "beginner"},
            score_fn=lambda _a, level: {
                "score": 60,
                "level": level,
                "feedback": [],
                "metrics": {"word_count": 12, "unique_words": 10, "sentence_count": 2},
                "source": "rule_based",
            },
            recommend_fn=lambda score, level: {
                "recommendation": "continue_same_level",
                "reason": "ok",
                "next_level": level,
            },
            get_next_exercise_fn=lambda level, **_k: {
                "level": level,
                "topic": "Greetings",
                "title": "Introduce Yourself",
                "exercise": "Introduce yourself.",
                "id": "b1",
                "source": "local_dataset",
            },
        ),
    )
    result = service.evaluate_outbound_session(
        "learner_1",
        "Hello there this is my spoken answer for practice today.",
    )
    assert result["score"] == 60
    assert result["recommendation"] == "continue_same_level"
    assert "follow_up" in result
