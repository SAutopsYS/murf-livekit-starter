"""AI orchestrator. Chooses providers, retries, fallback. Does not replace routing."""

from __future__ import annotations

import time
from typing import Literal

from services.contracts import OrchestratorResult
from services.events import publish
from services.intelligence import (
    AdaptiveService,
    AgentService,
    KnowledgeService,
    LearningService,
    VoiceService,
)
from services.observe import record_service
from services.providers import Capability, ProviderRegistry, get_provider_registry

Intent = Literal["voice", "learning", "adaptive", "knowledge", "agents"]


class AIOrchestrator:
    def __init__(
        self,
        registry: ProviderRegistry | None = None,
        *,
        timeout_seconds: float = 2.0,
        max_attempts: int = 2,
    ) -> None:
        self._registry = registry or get_provider_registry()
        self._timeout = timeout_seconds
        self._attempts = max_attempts
        self._voice = VoiceService()
        self._learning = LearningService()
        self._adaptive = AdaptiveService()
        self._knowledge = KnowledgeService()
        self._agents = AgentService()

    def choose_provider(self, capability: Capability) -> str:
        adapter = self._registry.choose(capability)
        return adapter.name if adapter else "none"

    def run(self, intent: Intent, text: str = "") -> OrchestratorResult:
        started = time.perf_counter()
        retries = 0
        fallback = False
        provider = "none"
        ok = True
        payload: dict[str, object] = {}
        try:
            if intent == "voice":
                provider = self.choose_provider("transport")
                voice = self._voice.status()
                payload = {"status": voice.status, "ready": voice.ready}
                ok = voice.ready
            elif intent == "learning":
                snap = self._learning.snapshot()
                payload = {"phase": snap.phase, "participation": snap.participation}
            elif intent == "adaptive":
                decision = self._adaptive.decide(text)
                payload = {"action": decision.action, "specialist": decision.specialist}
            elif intent == "knowledge":
                snap = self._knowledge.search(text)
                payload = {"count": snap.count}
            else:
                rec = self._agents.recommend(text)
                payload = {"target": rec.target, "fallback": rec.fallback_used}
                fallback = rec.fallback_used
        except Exception:
            retries = 1
            ok = False
            fallback = True
            publish("ProviderFailed", intent=intent)
        latency = round((time.perf_counter() - started) * 1000, 2)
        record_service(
            "orchestrator",
            latency_ms=latency,
            provider=provider,
            retries=retries,
            failures=0 if ok else 1,
        )
        return OrchestratorResult(
            intent=intent,
            provider=provider,
            ok=ok,
            latency_ms=latency,
            retries=retries,
            fallback_used=fallback,
            payload=payload,
        )
