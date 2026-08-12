"""Deterministic duplicate detection for open human-help escalations."""

from __future__ import annotations

import logging
import re

from escalation.models import EscalationRequest
from escalation.repository import EscalationRepository, get_escalation_repository

logger = logging.getLogger("escalation.deduplication")

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_summary(summary: str) -> str:
    """Normalize a summary for exact duplicate comparison."""
    if not isinstance(summary, str):
        return ""
    return _WHITESPACE_RE.sub(" ", summary.strip().lower())


class EscalationDeduplicator:
    """Find equivalent open/in-progress escalations using repository data."""

    def __init__(self, repository: EscalationRepository | None = None) -> None:
        self._repository = repository or get_escalation_repository()

    def find_duplicate(
        self,
        reason: str,
        summary: str,
    ) -> EscalationRequest | None:
        """Return an active matching escalation when one exists."""
        logger.info("Escalation duplicate check")
        reason_key = reason.strip().lower() if isinstance(reason, str) else ""
        summary_key = normalize_summary(summary)
        if not reason_key or not summary_key:
            return None

        for existing in self._repository.list_active():
            if existing.reason.strip().lower() != reason_key:
                continue
            if normalize_summary(existing.summary) != summary_key:
                continue
            logger.info("Duplicate escalation found")
            return existing
        return None
