"""LiveKit function tools for learner memory.

Tools orchestrate repository calls only. SQL stays in repository.py.
The LLM must use these functions for memory access; do not embed memory in prompts.
"""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Any

from livekit.agents import RunContext, function_tool

from memory.models import User
from memory.repository import (
    create_user,
    delete_user,
    get_user_by_id,
    update_user,
)
from memory.repository import (
    update_last_interaction as repo_update_last_interaction,
)

logger = logging.getLogger("memory.tools")


def _user_payload(user: User) -> dict[str, Any]:
    """Return structured user data for tool results."""
    return asdict(user)


def fetch_user_memory(user_id: str) -> dict[str, Any] | None:
    """Lookup helper used by the tool and silent session orchestration."""
    user = get_user_by_id(user_id)
    if user is None:
        logger.info("Memory lookup: New learner")
        return None
    logger.info("Memory lookup: Found learner")
    return _user_payload(user)


def touch_last_interaction(user_id: str) -> dict[str, Any] | None:
    """Update only last_interaction via the repository."""
    updated = repo_update_last_interaction(user_id)
    if updated is None:
        return None
    logger.info("Updated last interaction")
    return _user_payload(updated)


@function_tool()
async def lookup_user(
    context: RunContext,
    user_id: str,
) -> dict[str, Any] | None:
    """Look up a learner profile by user_id.

    Returns structured user fields when found. Returns null when the user
    does not exist. Does not generate spoken text.

    Args:
        user_id: Stable learner identifier to look up.
    """
    del context  # Required by LiveKit tool signature; unused here.
    return fetch_user_memory(user_id)


@function_tool()
async def save_user_memory(
    context: RunContext,
    user_id: str,
    name: str | None = None,
    language_preference: str | None = None,
    learning_level: str | None = None,
    grammar_level: str | None = None,
    speaking_confidence: str | None = None,
    common_mistakes: list[str] | None = None,
    last_topics: list[str] | None = None,
    consent: bool | None = None,
) -> dict[str, Any] | None:
    """Create or update a learner memory profile after consent.

    Creates the user when missing; otherwise updates the existing profile.
    Requires consent=true for this call, or an existing profile that already
    has consent granted. Returns structured user data, a consent_required
    result, or null on failure.

    Args:
        user_id: Stable learner identifier.
        name: Learner display name.
        language_preference: Preferred language (for example english, hindi, hinglish).
        learning_level: Overall learning level.
        grammar_level: Grammar level.
        speaking_confidence: Speaking confidence level.
        common_mistakes: List of common mistakes to remember.
        last_topics: List of recent practice topics.
        consent: Set true only after the learner clearly agrees to save memory.
    """
    del context

    existing = get_user_by_id(user_id)
    has_consent = bool(consent) or (existing is not None and existing.consent)
    if not has_consent:
        logger.info("Consent denied")
        return {
            "saved": False,
            "reason": "consent_required",
            "user_id": user_id,
        }

    if existing is not None:
        if name is not None:
            existing.name = name
        if language_preference is not None:
            existing.language_preference = language_preference
        if learning_level is not None:
            existing.learning_level = learning_level
        if grammar_level is not None:
            existing.grammar_level = grammar_level
        if speaking_confidence is not None:
            existing.speaking_confidence = speaking_confidence
        if common_mistakes is not None:
            existing.common_mistakes = common_mistakes
        if last_topics is not None:
            existing.last_topics = last_topics
        existing.consent = True
        saved = update_user(existing)
    else:
        saved = create_user(
            User(
                user_id=user_id,
                name=name or "",
                language_preference=language_preference or "",
                learning_level=learning_level or "",
                grammar_level=grammar_level or "",
                speaking_confidence=speaking_confidence or "",
                common_mistakes=list(common_mistakes or []),
                last_topics=list(last_topics or []),
                consent=True,
            )
        )

    if saved is None:
        logger.warning("Memory save failed")
        return None
    logger.info("Memory saved")
    return _user_payload(saved)


@function_tool()
async def update_last_interaction(
    context: RunContext,
    user_id: str,
) -> dict[str, Any] | None:
    """Update only the learner's last_interaction timestamp.

    Returns the updated structured user data, or null when the user is missing.

    Args:
        user_id: Stable learner identifier.
    """
    del context
    return touch_last_interaction(user_id)


@function_tool()
async def forget_user_memory(
    context: RunContext,
    user_id: str,
) -> dict[str, Any]:
    """Permanently delete a learner's stored learning profile.

    Returns structured data only. Does not generate spoken text.

    Args:
        user_id: Stable learner identifier to forget.
    """
    del context

    existing = get_user_by_id(user_id)
    if existing is None:
        logger.info("No stored profile found")
        logger.info("Forget request completed")
        return {
            "deleted": False,
            "reason": "not_found",
            "user_id": user_id,
        }

    removed = delete_user(user_id)
    if not removed:
        logger.info("No stored profile found")
        logger.info("Forget request completed")
        return {
            "deleted": False,
            "reason": "not_found",
            "user_id": user_id,
        }

    logger.info("Memory deleted")
    logger.info("Forget request completed")
    return {
        "deleted": True,
        "user_id": user_id,
    }


MEMORY_TOOLS = [
    lookup_user,
    save_user_memory,
    update_last_interaction,
    forget_user_memory,
]
