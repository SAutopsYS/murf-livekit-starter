"""Day 7 Phase 5: duplicate escalation detection."""

from __future__ import annotations

from typing import Any

import pytest

from escalation.notifier import EscalationNotifier
from escalation.repository import EscalationRepository
from escalation.status import EscalationStatusManager
from escalation.tools import create_escalation_request


@pytest.fixture()
def repo() -> EscalationRepository:
    return EscalationRepository()


def _notifier(counter: list[int] | None = None) -> EscalationNotifier:
    calls = counter if counter is not None else []

    def poster(url: str, payload: dict[str, Any]) -> tuple[bool, int]:
        del url, payload
        calls.append(1)
        return True, 204

    return EscalationNotifier(webhook_url="https://example.com/hook", poster=poster)


def test_first_escalation_creates_new(repo: EscalationRepository) -> None:
    result = create_escalation_request(
        reason="teacher_help",
        summary="I need help from a teacher",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    assert result["duplicate"] is False
    assert result["reference_id"] == "ESC-000001"
    assert result["notification"] == "delivered"


def test_duplicate_returns_existing_reference(repo: EscalationRepository) -> None:
    calls: list[int] = []
    first = create_escalation_request(
        reason="teacher_help",
        summary="I need help from a teacher",
        consent=True,
        repository=repo,
        notifier=_notifier(calls),
    )
    second = create_escalation_request(
        reason="teacher_help",
        summary="I need help from a teacher",
        consent=True,
        repository=repo,
        notifier=_notifier(calls),
    )
    assert second["reference_id"] == first["reference_id"]
    assert second["duplicate"] is True
    assert second["notification"] == "already_sent"
    assert len(repo.list_open()) == 1
    assert len(calls) == 1


def test_summary_normalization(repo: EscalationRepository) -> None:
    first = create_escalation_request(
        reason="teacher_help",
        summary=" I need help from a teacher ",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    second = create_escalation_request(
        reason="teacher_help",
        summary="I NEED HELP FROM A TEACHER",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    assert second["reference_id"] == first["reference_id"]
    assert second["duplicate"] is True


def test_different_reason_or_summary_creates_new(repo: EscalationRepository) -> None:
    first = create_escalation_request(
        reason="teacher_help",
        summary="Grammar help",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    by_reason = create_escalation_request(
        reason="learner_upset",
        summary="Grammar help",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    by_summary = create_escalation_request(
        reason="teacher_help",
        summary="Vocabulary help",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    assert by_reason["reference_id"] != first["reference_id"]
    assert by_summary["reference_id"] != first["reference_id"]
    assert len(repo.list_open()) == 3


def test_resolved_does_not_block_new_request(repo: EscalationRepository) -> None:
    first = create_escalation_request(
        reason="teacher_help",
        summary="Same issue",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    EscalationStatusManager(repo).update_status(first["reference_id"], "resolved")
    second = create_escalation_request(
        reason="teacher_help",
        summary="Same issue",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    assert second["duplicate"] is False
    assert second["reference_id"] != first["reference_id"]


def test_urgency_upgrade_keeps_reference(repo: EscalationRepository) -> None:
    calls: list[int] = []
    first = create_escalation_request(
        reason="teacher_help",
        summary="Need help now",
        urgency="medium",
        consent=True,
        repository=repo,
        notifier=_notifier(calls),
    )
    second = create_escalation_request(
        reason="teacher_help",
        summary="Need help now",
        urgency="high",
        consent=True,
        repository=repo,
        notifier=_notifier(calls),
    )
    assert second["reference_id"] == first["reference_id"]
    assert second["urgency"] == "high"
    assert second["duplicate"] is True
    stored = repo.get(first["reference_id"])
    assert stored is not None
    assert stored.urgency == "high"
    # Initial create + upgrade notify.
    assert len(calls) == 2


def test_lower_urgency_does_not_downgrade(repo: EscalationRepository) -> None:
    first = create_escalation_request(
        reason="learner_upset",
        summary="Upset and needs help",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    assert first["urgency"] == "high"
    second = create_escalation_request(
        reason="learner_upset",
        summary="Upset and needs help",
        urgency="low",
        consent=True,
        repository=repo,
        notifier=_notifier(),
    )
    assert second["reference_id"] == first["reference_id"]
    assert second["urgency"] == "high"
    assert second["notification"] == "already_sent"
