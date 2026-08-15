"""Universal search. Fans out to existing retrieval. No new memory database."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Literal

from knowledge.search import search_knowledge
from services.agent_runtime import AgentRuntimeService
from services.events import publish
from services.jobs import job_for
from services.marketplace import MarketplaceService
from services.observe import record_service

SearchKind = Literal[
    "document",
    "knowledge",
    "skill",
    "project",
    "whiteboard",
    "workflow",
    "plugin",
    "agent",
    "learning",
    "timeline",
    "recommendation",
    "organization",
]
SearchMode = Literal[
    "keyword", "semantic", "hybrid", "context", "ai", "filtered", "organization"
]


@dataclass(frozen=True)
class SearchHit:
    kind: SearchKind
    id: str
    title: str
    score: float
    source: str


@dataclass(frozen=True)
class SearchResult:
    query: str
    mode: SearchMode
    hits: tuple[SearchHit, ...]
    latency_ms: float


class IndexService:
    """Lazy / incremental. Does not create a second store."""

    def refresh(self) -> dict[str, str]:
        spec = job_for("search_index")
        publish("SearchIndexed", job=spec.kind)
        publish("IndexUpdated", job=spec.kind)
        return {"status": "lazy", "store": "existing"}


class RankingService:
    def rank(self, hits: list[SearchHit]) -> tuple[SearchHit, ...]:
        return tuple(sorted(hits, key=lambda item: item.score, reverse=True))


class SuggestionService:
    def from_hits(self, hits: tuple[SearchHit, ...]) -> tuple[str, ...]:
        titles = tuple(item.title for item in hits[:5])
        if titles:
            publish("SuggestionGenerated", count=len(titles))
        return titles


class QueryService:
    def knowledge(self, text: str, limit: int) -> list[SearchHit]:
        rows = search_knowledge(text, limit=limit) if text.strip() else []
        return [
            SearchHit(
                "knowledge",
                row["title"],
                row["title"],
                float(3 - index),
                "knowledge.search",
            )
            for index, row in enumerate(rows)
        ]

    def plugins(self, text: str) -> list[SearchHit]:
        rows = MarketplaceService().catalog.search(text)
        return [
            SearchHit("plugin", item.id, item.name, 1.5, "marketplace.catalog")
            for item in rows
        ]

    def agents(self, text: str) -> list[SearchHit]:
        needle = text.lower().strip()
        hits: list[SearchHit] = []
        for agent in AgentRuntimeService().registry.list():
            hay = f"{agent.name} {agent.id}".lower()
            if not needle or needle in hay:
                hits.append(
                    SearchHit(
                        "agent",
                        agent.id,
                        agent.name,
                        2.0 if agent.live else 0.5,
                        "agent.runtime",
                    )
                )
        return hits


class SearchService:
    def __init__(self) -> None:
        self.index = IndexService()
        self.queries = QueryService()
        self.ranking = RankingService()
        self.suggestions = SuggestionService()

    def search(
        self, text: str, *, mode: SearchMode = "hybrid", limit: int = 8
    ) -> SearchResult:
        started = perf_counter()
        publish("SearchStarted", mode=mode)
        hits = self.queries.knowledge(text, limit)
        if mode in {"hybrid", "filtered", "ai", "context"}:
            hits.extend(self.queries.plugins(text))
            hits.extend(self.queries.agents(text))
        ranked = self.ranking.rank(hits)[:limit]
        latency = round((perf_counter() - started) * 1000, 2)
        record_service("search", latency_ms=latency)
        publish("SearchCompleted", count=len(ranked))
        publish("SearchExecuted", count=len(ranked))
        return SearchResult(query=text, mode=mode, hits=ranked, latency_ms=latency)


class DiscoveryService:
    """Phase 27 alias. Same engine."""

    def __init__(self) -> None:
        self._inner = SearchService()

    def search(self, text: str, mode: SearchMode = "hybrid") -> SearchResult:
        return self._inner.search(text, mode=mode)
