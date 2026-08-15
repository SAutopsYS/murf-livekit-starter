"""Exercise lookup with API failover, cooldown, rotation, cache, and topics.

LiveKit registration stays in livekit_tools. This module returns structured data
only and never raises to the agent layer.
"""

from __future__ import annotations

import logging
import random
from typing import Literal, TypedDict

from tools.dataset import ExerciseItem, load_exercise_dataset
from tools.metrics import track_tool_call
from tools.provider import (
    ExerciseProvider,
    build_exercise_provider,
    get_exercise_config,
)
from tools.provider_health import ProviderHealth, get_provider_health
from tools.request_cache import RequestCache, get_request_cache
from tools.session_cache import SessionExerciseCache, get_session_exercise_cache
from tools.validator import ExerciseValidator, get_exercise_validator

logger = logging.getLogger("tools.exercise")

VALID_LEVELS = ("beginner", "intermediate", "advanced")
LevelName = Literal["beginner", "intermediate", "advanced"]

_DATASET_UNAVAILABLE = {
    "error": True,
    "message": "Exercise dataset unavailable.",
}


class ExerciseResult(TypedDict):
    """Successful exercise lookup payload."""

    id: str
    level: str
    topic: str
    title: str
    exercise: str
    source: str


class ExerciseError(TypedDict):
    """Structured failure payload for the agent/tool layer."""

    error: bool
    message: str


def normalize_level(level: str) -> LevelName | None:
    """Normalize a learner level to beginner/intermediate/advanced."""
    if not isinstance(level, str):
        return None
    normalized = level.strip().lower()
    if normalized in VALID_LEVELS:
        return normalized  # type: ignore[return-value]
    return None


def normalize_topic(topic: str | None) -> str | None:
    """Normalize an optional topic filter."""
    if topic is None:
        return None
    if not isinstance(topic, str):
        return None
    cleaned = topic.strip().lower()
    return cleaned or None


def topic_matches(item_topic: str, item_title: str, topic: str) -> bool:
    """Return True when topic partially matches item topic/title."""
    needle = topic.strip().lower()
    if not needle:
        return True
    return needle in item_topic.lower() or needle in item_title.lower()


def filter_items_by_topic(
    items: list[ExerciseItem],
    topic: str | None,
) -> list[ExerciseItem]:
    """Filter exercises by topic with case-insensitive partial matching."""
    normalized = normalize_topic(topic)
    if normalized is None:
        return list(items)

    logger.info("Topic requested")
    matched = [
        item
        for item in items
        if topic_matches(item["topic"], item["title"], normalized)
    ]
    if matched:
        logger.info("Topic matched")
        return matched

    logger.info("Topic unavailable")
    logger.info("Falling back to level exercises")
    return list(items)


def _pick_exercise(items: list[ExerciseItem]) -> ExerciseItem | None:
    if not items:
        return None
    return random.choice(items)


def _to_result(item: ExerciseItem, *, level: str, source: str) -> ExerciseResult:
    return {
        "id": item["id"],
        "level": level,
        "topic": item["topic"],
        "title": item["title"],
        "exercise": item["exercise"],
        "source": source,
    }


def _deliver(
    result: ExerciseResult,
    *,
    validator: ExerciseValidator,
) -> ExerciseResult | ExerciseError:
    validated = validator.validate(result)
    if not validated["valid"]:
        logger.info("Invalid local exercise")
        return dict(_DATASET_UNAVAILABLE)  # type: ignore[return-value]
    sanitized = validated["exercise"]
    delivered: ExerciseResult = {
        "id": sanitized["id"],
        "level": result["level"],
        "topic": sanitized["topic"],
        "title": sanitized["title"],
        "exercise": sanitized["exercise"],
        "source": result["source"],
    }
    logger.info("Sanitized exercise delivered")
    return delivered


def get_local_exercise(
    level: str,
    *,
    topic: str | None = None,
    cache: SessionExerciseCache | None = None,
    validator: ExerciseValidator | None = None,
) -> ExerciseResult | ExerciseError:
    """Load one unused local exercise for a normalized level."""
    normalized = normalize_level(level)
    if normalized is None:
        logger.info("Unknown exercise level: %r", level)
        return dict(_DATASET_UNAVAILABLE)  # type: ignore[return-value]

    active_validator = validator or get_exercise_validator()

    try:
        dataset = load_exercise_dataset()
    except (FileNotFoundError, OSError, ValueError, TypeError) as exc:
        logger.warning("Exercise dataset unavailable: %s", exc)
        return dict(_DATASET_UNAVAILABLE)  # type: ignore[return-value]
    except Exception as exc:  # includes json.JSONDecodeError
        logger.warning("Exercise dataset unavailable: %s", exc)
        return dict(_DATASET_UNAVAILABLE)  # type: ignore[return-value]

    items = filter_items_by_topic(dataset.get(normalized, []), topic)
    if not items:
        logger.info("No exercises for level: %s", normalized)
        return dict(_DATASET_UNAVAILABLE)  # type: ignore[return-value]

    active_cache = cache or get_session_exercise_cache()
    unused = active_cache.unused(normalized, items)
    if not unused:
        active_cache.reset_level(normalized)
        unused = list(items)

    chosen = _pick_exercise(unused)
    if chosen is None:
        logger.info("No exercises for level: %s", normalized)
        return dict(_DATASET_UNAVAILABLE)  # type: ignore[return-value]

    result = _to_result(chosen, level=normalized, source="local_dataset")
    delivered = _deliver(result, validator=active_validator)
    if delivered.get("error"):
        return delivered  # type: ignore[return-value]

    active_cache.mark_served(normalized, delivered["id"])  # type: ignore[index]
    logger.info("Exercise selected")
    return delivered  # type: ignore[return-value]


def _get_next_exercise_impl(
    level: str,
    topic: str | None = None,
    *,
    provider: ExerciseProvider | None = None,
    source: str | None = None,
    health: ProviderHealth | None = None,
    cache: SessionExerciseCache | None = None,
    request_cache: RequestCache | None = None,
    validator: ExerciseValidator | None = None,
) -> ExerciseResult | ExerciseError:
    normalized = normalize_level(level)
    if normalized is None:
        logger.info("Unknown exercise level: %r", level)
        return dict(_DATASET_UNAVAILABLE)  # type: ignore[return-value]

    config = get_exercise_config()
    active_source = (source or config.source).strip().lower()
    if active_source not in {"local", "api"}:
        active_source = "local"

    active_health = health or get_provider_health()
    active_cache = cache or get_session_exercise_cache()
    active_request_cache = request_cache or get_request_cache()
    active_validator = validator or get_exercise_validator()
    active_topic = normalize_topic(topic)

    cache_key = RequestCache.make_key(normalized, active_source, active_topic)
    cached = active_request_cache.get(cache_key)
    if cached is not None and cached.get("error") is not True:
        return cached  # type: ignore[return-value]

    if active_source == "api":
        if not active_health.is_available():
            logger.info("Using local exercise")
        else:
            logger.info("Exercise provider: API")
            active_provider = provider or build_exercise_provider(config)
            if active_provider is not None:
                remote = active_provider.fetch_exercise(normalized)
                if remote is not None:
                    if not str(remote.get("id", "")).strip():
                        title_hint = (
                            str(remote.get("title", "exercise")).strip() or "exercise"
                        )
                        remote = {
                            **remote,
                            "id": f"api:{normalized}:{title_hint}",
                        }
                    validated = active_validator.validate(remote)
                    if not validated["valid"]:
                        logger.info("Invalid provider response")
                        logger.info("Falling back after validation failure")
                        active_health.mark_failure()
                    else:
                        sanitized = validated["exercise"]
                        exercise_id = sanitized["id"]
                        remote_topic = sanitized["topic"]
                        remote_title = sanitized["title"]
                        if active_topic and not topic_matches(
                            remote_topic,
                            remote_title,
                            active_topic,
                        ):
                            logger.info("Topic unavailable")
                            logger.info("Falling back to level exercises")
                            active_health.mark_success()
                        elif exercise_id and active_cache.has_seen(
                            normalized,
                            exercise_id,
                        ):
                            logger.info("Skipping previously served exercise")
                            local_duplicate = get_local_exercise(
                                normalized,
                                topic=active_topic,
                                cache=active_cache,
                                validator=active_validator,
                            )
                            if not local_duplicate.get("error"):
                                active_health.mark_success()
                                active_request_cache.set(cache_key, local_duplicate)
                                logger.info("Exercise delivered")
                                return local_duplicate  # type: ignore[return-value]
                            active_health.mark_success()
                        else:
                            result: ExerciseResult = {
                                "id": exercise_id,
                                "level": normalized,
                                "topic": remote_topic,
                                "title": remote_title,
                                "exercise": sanitized["exercise"],
                                "source": remote.get("source", "external_api"),
                            }
                            active_health.mark_success()
                            active_cache.mark_served(normalized, result["id"])
                            active_request_cache.set(cache_key, result)
                            logger.info("Exercise selected")
                            logger.info("Sanitized exercise delivered")
                            logger.info("Exercise delivered")
                            return result
                else:
                    active_health.mark_failure()
            else:
                active_health.mark_failure()
            logger.info("Using local exercise")
    else:
        logger.info("Using local exercise")

    local = get_local_exercise(
        normalized,
        topic=active_topic,
        cache=active_cache,
        validator=active_validator,
    )
    if local.get("error"):
        return local  # type: ignore[return-value]

    active_request_cache.set(cache_key, local)
    logger.info("Exercise delivered")
    return local  # type: ignore[return-value]


def get_next_exercise(
    level: str,
    topic: str | None = None,
    *,
    provider: ExerciseProvider | None = None,
    source: str | None = None,
    health: ProviderHealth | None = None,
    cache: SessionExerciseCache | None = None,
    request_cache: RequestCache | None = None,
    validator: ExerciseValidator | None = None,
) -> ExerciseResult | ExerciseError:
    """Return one speaking exercise for the given learner level.

    Optional topic filters within the level. When EXERCISE_SOURCE=api, try the
    external provider first (with retries and cooldown). Fall back to local data
    on failure. Session rotation and request caching apply within the session.
    """
    return track_tool_call(
        "exercise_tool",
        _get_next_exercise_impl,
        level,
        topic,
        provider=provider,
        source=source,
        health=health,
        cache=cache,
        request_cache=request_cache,
        validator=validator,
    )
