"""Typed service contracts. Never return raw provider payloads to callers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

VoiceStatus = Literal["ready", "degraded", "unavailable"]
JobStatus = Literal["queued", "running", "done", "failed", "cancelled"]


@dataclass(frozen=True)
class VoiceResponse:
    status: VoiceStatus
    provider: str
    transport: str
    tts: str
    stt: str
    ready: bool
    latency_ms: float | None = None


@dataclass(frozen=True)
class LearningSnapshot:
    phase: str
    consented_profiles: int
    participation: int
    success_rate: float
    source: str


@dataclass(frozen=True)
class AdaptiveDecision:
    action: str
    specialist: str
    live: bool
    reason: str
    confidence: float
    source: str


@dataclass(frozen=True)
class KnowledgeHit:
    topic: str
    title: str
    score: int


@dataclass(frozen=True)
class KnowledgeSnapshot:
    hits: tuple[KnowledgeHit, ...]
    count: int
    source: str


@dataclass(frozen=True)
class AgentRecommendation:
    target: str
    specialist_id: str | None
    fallback_used: bool
    reason: str


@dataclass(frozen=True)
class AnalyticsSnapshot:
    total_calls: int
    successful_calls: int
    failed_calls: int
    success_rate: float
    source: str


@dataclass(frozen=True)
class EnterpriseSnapshot:
    agent_count: int
    source: str
    keys: tuple[str, ...]


@dataclass(frozen=True)
class InsightRecord:
    kind: str
    title: str
    source: str


@dataclass(frozen=True)
class TimelineRecord:
    event: str
    at: str | None
    source: str


@dataclass(frozen=True)
class OrchestratorResult:
    intent: str
    provider: str
    ok: bool
    latency_ms: float
    retries: int
    fallback_used: bool
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ServiceMetrics:
    service: str
    latency_ms: float
    failures: int
    retries: int
    cache_hit: bool
    provider: str
    token_usage: int
    cost_units: float
