"""Day 6 Phase 5: outbound learning coordinator."""

from __future__ import annotations

from typing import Any

import pytest

from telephony.config import clear_telephony_config_cache, get_telephony_config
from telephony.coordinator import OutboundConversationCoordinator
from telephony.service import TelephonyService


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


def test_existing_learner_starts_practice() -> None:
    coordinator = OutboundConversationCoordinator(
        lookup_user_fn=lambda _uid: {
            "user_id": "learner_1",
            "learning_level": "beginner",
        },
        get_next_exercise_fn=lambda level, **_kwargs: {
            "level": level,
            "topic": "Greetings",
            "title": "Introduce Yourself",
            "exercise": "Introduce yourself.",
            "source": "local_dataset",
            "id": "b1",
        },
    )
    result = coordinator.start_daily_practice("learner_1")
    assert result == {
        "status": "ready",
        "level": "beginner",
        "exercise": {
            "topic": "Greetings",
            "title": "Introduce Yourself",
        },
    }


def test_missing_learner_handled_gracefully() -> None:
    coordinator = OutboundConversationCoordinator(
        lookup_user_fn=lambda _uid: None,
        get_next_exercise_fn=lambda *_a, **_k: {"error": True},
    )
    result = coordinator.start_daily_practice("unknown")
    assert result == {
        "status": "needs_setup",
        "reason": "learning_level_missing",
    }


def test_service_integration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LIVEKIT_URL", "wss://example.livekit.cloud")
    monkeypatch.setenv("LIVEKIT_API_KEY", "key")
    monkeypatch.setenv("LIVEKIT_API_SECRET", "secret")

    def _exercise(level: str, **_kwargs: Any) -> dict[str, Any]:
        return {
            "level": level,
            "topic": "Travel",
            "title": "Dream Vacation",
            "exercise": "Describe your dream vacation.",
            "source": "local_dataset",
            "id": "i2",
        }

    service = TelephonyService(
        get_telephony_config(force_reload=True),
        coordinator=OutboundConversationCoordinator(
            lookup_user_fn=lambda _uid: {"learning_level": "intermediate"},
            get_next_exercise_fn=_exercise,
        ),
    )
    result = service.start_outbound_learning("learner_2")
    assert result["status"] == "ready"
    assert result["level"] == "intermediate"
    assert result["exercise"]["topic"] == "Travel"
