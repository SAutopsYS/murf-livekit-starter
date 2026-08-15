"""SALORA AI service platform. Wraps existing modules. Does not replace them."""

from services.api import API_VERSION, fail, ok, paginate
from services.contracts import (
    AdaptiveDecision,
    AgentRecommendation,
    AnalyticsSnapshot,
    EnterpriseSnapshot,
    KnowledgeSnapshot,
    LearningSnapshot,
    VoiceResponse,
)
from services.events import publish, recent_events, reset_events, subscribe
from services.intelligence import (
    AdaptiveService,
    AgentService,
    AnalyticsServiceFacade,
    EnterpriseService,
    InsightService,
    KnowledgeService,
    LearningService,
    MemoryService,
    RecommendationService,
    TimelineService,
    VoiceService,
)
from services.jobs import JOB_CATALOG, job_for
from services.orchestrator import AIOrchestrator
from services.providers import ProviderRegistry, get_provider_registry

__all__ = [
    "API_VERSION",
    "JOB_CATALOG",
    "AIOrchestrator",
    "AdaptiveDecision",
    "AdaptiveService",
    "AgentRecommendation",
    "AgentService",
    "AnalyticsServiceFacade",
    "AnalyticsSnapshot",
    "EnterpriseService",
    "EnterpriseSnapshot",
    "InsightService",
    "KnowledgeService",
    "KnowledgeSnapshot",
    "LearningService",
    "LearningSnapshot",
    "MemoryService",
    "ProviderRegistry",
    "RecommendationService",
    "TimelineService",
    "VoiceResponse",
    "VoiceService",
    "fail",
    "get_provider_registry",
    "job_for",
    "ok",
    "paginate",
    "publish",
    "recent_events",
    "reset_events",
    "subscribe",
]
