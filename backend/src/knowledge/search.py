"""Keyword search over the Learning & Literacy knowledge base."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from knowledge.repository import KnowledgeEntry, get_all_entries

logger = logging.getLogger("knowledge.search")

_TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in _TOKEN_RE.findall(text)]


def _score_entry(query_tokens: list[str], entry: KnowledgeEntry) -> int:
    if not query_tokens:
        return 0

    # Ignore very short tokens/keywords to avoid false matches (for example "a" in "quantum").
    query_tokens = [token for token in query_tokens if len(token) >= 3]
    if not query_tokens:
        return 0

    title = entry["title"].lower()
    topic = entry["topic"].lower()
    content = entry["content"].lower()
    keywords = [
        keyword.lower() for keyword in entry["keywords"] if len(keyword.strip()) >= 3
    ]
    score = 0

    for token in query_tokens:
        if token in title:
            score += 3
        if token in topic:
            score += 2
        if token in content:
            score += 1
        for keyword in keywords:
            if token == keyword or token in keyword or keyword in token:
                score += 4
                break

    return score


def search_knowledge(
    query: str,
    *,
    limit: int = 3,
    resource_path: Path | None = None,
) -> list[KnowledgeEntry]:
    """Case-insensitive partial keyword search. Returns top matches."""
    logger.info("Knowledge search started")
    entries = get_all_entries(resource_path)
    query_tokens = _tokenize(query)
    if not query_tokens:
        logger.info("Knowledge not found")
        return []

    ranked: list[tuple[int, KnowledgeEntry]] = []
    for entry in entries:
        score = _score_entry(query_tokens, entry)
        if score > 0:
            ranked.append((score, entry))

    ranked.sort(key=lambda item: (-item[0], item[1]["title"]))
    results = [entry for _, entry in ranked[:limit]]

    if results:
        logger.info("Knowledge results found")
    else:
        logger.info("Knowledge not found")
    return results
