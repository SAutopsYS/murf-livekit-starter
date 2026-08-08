"""Lightweight JSON knowledge repository. Data-only, no LLM logic."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, TypedDict

logger = logging.getLogger("knowledge.repository")

RESOURCES_DIR = Path(__file__).resolve().parent / "resources"
DEFAULT_RESOURCE_PATH = RESOURCES_DIR / "english_basics.json"


class KnowledgeEntry(TypedDict):
    topic: str
    title: str
    keywords: list[str]
    content: str


_entries_cache: list[KnowledgeEntry] | None = None
_cache_path: Path | None = None


def _normalize_entry(raw: dict[str, Any]) -> KnowledgeEntry | None:
    topic = str(raw.get("topic", "")).strip()
    title = str(raw.get("title", "")).strip()
    content = str(raw.get("content", "")).strip()
    keywords_raw = raw.get("keywords", [])
    if not topic or not title or not content:
        return None
    if not isinstance(keywords_raw, list):
        keywords_raw = []
    keywords = [str(item).strip() for item in keywords_raw if str(item).strip()]
    return {
        "topic": topic,
        "title": title,
        "keywords": keywords,
        "content": content,
    }


def load_entries(resource_path: Path | None = None) -> list[KnowledgeEntry]:
    """Load knowledge entries from JSON, using an in-memory cache."""
    global _entries_cache, _cache_path

    path = resource_path or DEFAULT_RESOURCE_PATH
    if _entries_cache is not None and _cache_path == path:
        logger.info("Knowledge cache hit")
        return _entries_cache

    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, list):
        raise ValueError("Knowledge resource must be a JSON list")

    entries: list[KnowledgeEntry] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        entry = _normalize_entry(item)
        if entry is not None:
            entries.append(entry)

    _entries_cache = entries
    _cache_path = path
    return entries


def clear_cache() -> None:
    """Clear the in-memory knowledge cache (used by tests)."""
    global _entries_cache, _cache_path
    _entries_cache = None
    _cache_path = None


def get_all_entries(resource_path: Path | None = None) -> list[KnowledgeEntry]:
    """Return all cached knowledge entries."""
    return list(load_entries(resource_path))
