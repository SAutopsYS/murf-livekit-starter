"""Intelligence services. Wrap existing modules. No second calculations."""

from __future__ import annotations

import time

from analytics.service import get_analytics_service
from enterprise.platform import ControlCenterService
from enterprise.visualization import (
    MemoryGraphService as EnterpriseMemoryGraph,
)
from enterprise.visualization import TimelineService as EnterpriseTimeline
from knowledge.search import search_knowledge
from services.contracts import (
    AdaptiveDecision,
    AgentRecommendation,
    AnalyticsSnapshot,
    EnterpriseSnapshot,
    InsightRecord,
    KnowledgeHit,
    KnowledgeSnapshot,
    LearningSnapshot,
    TimelineRecord,
    VoiceResponse,
)
from services.events import publish
from services.observe import record_service
from services.providers import get_provider_registry
from services.repositories import MemoryRepositoryAdapter
from specialists.router import SpecialistRouter


class VoiceService:
    """Describes the live voice path. Does not start LiveKit or Murf."""

    def status(self) -> VoiceResponse:
        started = time.perf_counter()
        registry = get_provider_registry()
        livekit = registry.get("livekit")
        murf = registry.get("murf")
        deepgram = registry.get("deepgram")
        ready = livekit.configured and murf.configured and deepgram.configured
        result = VoiceResponse(
            status="ready" if ready else "degraded",
            provider="livekit",
            transport="livekit",
            tts="murf",
            stt="deepgram",
            ready=ready,
        )
        record_service(
            "voice",
            latency_ms=round((time.perf_counter() - started) * 1000, 2),
            provider="livekit",
        )
        return result


class LearningService:
    def snapshot(self) -> LearningSnapshot:
        started = time.perf_counter()
        analytics = get_analytics_service().get_summary()
        if analytics.get("error"):
            analytics = {"total_calls": 0, "success_rate": 0.0}
        consented = len(MemoryRepositoryAdapter().list_consented())
        participation = int(analytics.get("total_calls") or 0)
        phase = "new" if participation == 0 else "active"
        result = LearningSnapshot(
            phase=phase,
            consented_profiles=consented,
            participation=participation,
            success_rate=float(analytics.get("success_rate") or 0.0),
            source="analytics+memory",
        )
        record_service(
            "learning", latency_ms=round((time.perf_counter() - started) * 1000, 2)
        )
        publish("LearningUpdated", phase=phase)
        return result


class AdaptiveService:
    """Advice only. SpecialistRouter remains routing authority."""

    def __init__(self, router: SpecialistRouter | None = None) -> None:
        self._router = router or SpecialistRouter()

    def decide(self, text: str = "") -> AdaptiveDecision:
        started = time.perf_counter()
        routed = self._router.route(text or "practice")
        specialist = routed.get("specialist_id") or "tutor"
        result = AdaptiveDecision(
            action="recommend_specialist"
            if routed.get("specialist_id")
            else "continue",
            specialist=specialist,
            live=specialist in {"tutor", "math", "math_practice_specialist"},
            reason=str(routed.get("reason") or "host"),
            confidence=0.7 if routed.get("specialist_id") else 0.5,
            source="specialist.router",
        )
        record_service(
            "adaptive", latency_ms=round((time.perf_counter() - started) * 1000, 2)
        )
        return result


class KnowledgeService:
    def search(self, query: str, limit: int = 5) -> KnowledgeSnapshot:
        started = time.perf_counter()
        rows = search_knowledge(query, limit=limit) if query.strip() else []
        hits = tuple(
            KnowledgeHit(topic=entry["topic"], title=entry["title"], score=index + 1)
            for index, entry in enumerate(rows)
        )
        result = KnowledgeSnapshot(
            hits=hits, count=len(hits), source="knowledge.search"
        )
        record_service(
            "knowledge", latency_ms=round((time.perf_counter() - started) * 1000, 2)
        )
        if hits:
            publish("KnowledgeUpdated", count=len(hits))
        return result


class AgentService:
    def __init__(self, router: SpecialistRouter | None = None) -> None:
        self._router = router or SpecialistRouter()

    def recommend(self, text: str) -> AgentRecommendation:
        routed = self._router.route(text)
        rec = AgentRecommendation(
            target=str(routed.get("target") or "MAIN_AGENT"),
            specialist_id=routed.get("specialist_id"),
            fallback_used=bool(routed.get("fallback_used")),
            reason=str(routed.get("reason") or ""),
        )
        publish("AgentTransferred", target=rec.target)
        return rec


class MemoryService:
    def consented_count(self) -> int:
        return len(MemoryRepositoryAdapter().list_consented())


class AnalyticsServiceFacade:
    def snapshot(self) -> AnalyticsSnapshot:
        started = time.perf_counter()
        raw = get_analytics_service().get_summary()
        if raw.get("error"):
            result = AnalyticsSnapshot(0, 0, 0, 0.0, "analytics.unavailable")
        else:
            result = AnalyticsSnapshot(
                total_calls=int(raw.get("total_calls") or 0),
                successful_calls=int(raw.get("successful_calls") or 0),
                failed_calls=int(raw.get("failed_calls") or 0),
                success_rate=float(raw.get("success_rate") or 0.0),
                source="analytics.service",
            )
        record_service(
            "analytics", latency_ms=round((time.perf_counter() - started) * 1000, 2)
        )
        return result


class EnterpriseService:
    def snapshot(self) -> EnterpriseSnapshot:
        started = time.perf_counter()
        raw = ControlCenterService().snapshot()
        agents = raw.get("agents") if isinstance(raw, dict) else None
        count = len(agents) if isinstance(agents, list) else 0
        keys = tuple(sorted(raw.keys())) if isinstance(raw, dict) else ()
        result = EnterpriseSnapshot(
            agent_count=count, source="enterprise.platform", keys=keys
        )
        record_service(
            "enterprise", latency_ms=round((time.perf_counter() - started) * 1000, 2)
        )
        return result


class RecommendationService:
    def from_adaptive(self, decision: AdaptiveDecision) -> InsightRecord:
        publish("RecommendationCreated", action=decision.action)
        return InsightRecord(
            kind="recommendation", title=decision.action, source="adaptive"
        )


class InsightService:
    def from_learning(self, learning: LearningSnapshot) -> InsightRecord:
        title = "New learner" if learning.phase == "new" else "Active practice"
        publish("InsightCreated", phase=learning.phase)
        return InsightRecord(kind="insight", title=title, source="learning")


class TimelineService:
    def recent(self, limit: int = 8) -> tuple[TimelineRecord, ...]:
        raw = EnterpriseTimeline().build()
        items = raw.get("items") if isinstance(raw, dict) else []
        rows = []
        for item in (items or [])[:limit]:
            rows.append(
                TimelineRecord(
                    event=str(item.get("event") or item.get("label") or "event"),
                    at=str(item.get("timestamp")) if item.get("timestamp") else None,
                    source="enterprise.timeline",
                )
            )
        return tuple(rows)


class GraphProjectionService:
    """Wraps enterprise MemoryGraphService. Does not write memory."""

    def build(self) -> dict[str, object]:
        return EnterpriseMemoryGraph().build()
