"""Day 7 Phase 6: escalation status tracking."""

from __future__ import annotations

import pytest

from escalation.notifier import EscalationNotifier
from escalation.repository import EscalationRepository
from escalation.status import EscalationStatusManager
from escalation.tools import create_escalation_request, get_escalation_status_data


@pytest.fixture()
def repo() -> EscalationRepository:
    return EscalationRepository()


def _create(repo: EscalationRepository) -> dict:
    return create_escalation_request(
        reason="teacher_help",
        summary="Need teacher support",
        consent=True,
        repository=repo,
        notifier=EscalationNotifier(webhook_url=""),
    )


def test_new_escalation_starts_open(repo: EscalationRepository) -> None:
    created = _create(repo)
    assert created["status"] == "open"
    status = get_escalation_status_data(created["reference_id"], repository=repo)
    assert status == {
        "reference_id": created["reference_id"],
        "status": "open",
        "next_action": "await_human_review",
    }


def test_open_to_in_progress(repo: EscalationRepository) -> None:
    created = _create(repo)
    manager = EscalationStatusManager(repo)
    result = manager.update_status(created["reference_id"], "in_progress")
    assert result["status"] == "in_progress"
    assert result["next_action"] == "human_review_in_progress"


def test_open_to_resolved(repo: EscalationRepository) -> None:
    created = _create(repo)
    result = EscalationStatusManager(repo).update_status(
        created["reference_id"],
        "resolved",
    )
    assert result["status"] == "resolved"
    assert result["next_action"] == "issue_resolved"


def test_in_progress_to_resolved(repo: EscalationRepository) -> None:
    created = _create(repo)
    manager = EscalationStatusManager(repo)
    manager.update_status(created["reference_id"], "in_progress")
    result = manager.update_status(created["reference_id"], "resolved")
    assert result["status"] == "resolved"


@pytest.mark.parametrize("target", ["open", "in_progress"])
def test_resolved_cannot_reopen(repo: EscalationRepository, target: str) -> None:
    created = _create(repo)
    manager = EscalationStatusManager(repo)
    manager.update_status(created["reference_id"], "resolved")
    result = manager.update_status(created["reference_id"], target)
    assert result == {
        "error": True,
        "message": "Unable to update escalation status.",
    }
    assert repo.get(created["reference_id"]).status == "resolved"


def test_invalid_status_rejected(repo: EscalationRepository) -> None:
    created = _create(repo)
    result = EscalationStatusManager(repo).update_status(
        created["reference_id"],
        "pending",
    )
    assert result["error"] is True


def test_unknown_reference_structured_error(repo: EscalationRepository) -> None:
    result = EscalationStatusManager(repo).get_status("ESC-999999")
    assert result == {
        "error": True,
        "message": "Escalation not found.",
    }


def test_duplicate_blocks_open_and_in_progress(repo: EscalationRepository) -> None:
    first = _create(repo)
    EscalationStatusManager(repo).update_status(first["reference_id"], "in_progress")
    second = create_escalation_request(
        reason="teacher_help",
        summary="Need teacher support",
        consent=True,
        repository=repo,
        notifier=EscalationNotifier(webhook_url=""),
    )
    assert second["duplicate"] is True
    assert second["reference_id"] == first["reference_id"]


def test_duplicate_allows_after_resolved(repo: EscalationRepository) -> None:
    first = _create(repo)
    EscalationStatusManager(repo).update_status(first["reference_id"], "resolved")
    second = create_escalation_request(
        reason="teacher_help",
        summary="Need teacher support",
        consent=True,
        repository=repo,
        notifier=EscalationNotifier(webhook_url=""),
    )
    assert second["duplicate"] is False
    assert second["reference_id"] != first["reference_id"]


def test_urgency_still_works_with_status(repo: EscalationRepository) -> None:
    created = create_escalation_request(
        reason="learner_upset",
        summary="Upset learner needs help",
        consent=True,
        repository=repo,
        notifier=EscalationNotifier(webhook_url=""),
    )
    assert created["urgency"] == "high"
    assert created["status"] == "open"
