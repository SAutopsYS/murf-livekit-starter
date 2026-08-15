"""Official SDK + gateway + webhooks. Exposes existing services. No portal UI."""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Literal, get_args
from uuid import uuid4

from salora_platform.auth import Role, can
from services.api import API_VERSION, ApiEnvelope, ok
from services.contracts import (
    AdaptiveDecision,
    AnalyticsSnapshot,
    KnowledgeSnapshot,
    LearningSnapshot,
    VoiceResponse,
)
from services.events import publish
from services.intelligence import (
    AdaptiveService,
    AnalyticsServiceFacade,
    KnowledgeService,
    LearningService,
    VoiceService,
)
from services.orchestrator import AIOrchestrator

SdkModule = Literal[
    "voice",
    "learning",
    "adaptive",
    "knowledge",
    "studio",
    "whiteboard",
    "memory_graph",
    "analytics",
    "enterprise",
    "marketplace",
    "agents",
]

IntegrationName = Literal[
    "google_workspace",
    "microsoft_365",
    "slack",
    "discord",
    "notion",
    "obsidian",
    "github",
    "gitlab",
    "jira",
    "canvas_lms",
    "moodle",
    "salesforce",
    "sap",
]


@dataclass(frozen=True)
class SdkManifest:
    module: SdkModule
    version: str
    contract: str


@dataclass(frozen=True)
class GatewayPolicy:
    version: str
    auth: str
    rate_limit: str
    health: str


@dataclass(frozen=True)
class WebhookSpec:
    event: str
    url_required: bool
    batch: bool


@dataclass
class ApiTokenRecord:
    id: str
    owner: str
    organization: str | None
    scopes: tuple[str, ...]
    created_at: float


SDK_MODULES: tuple[SdkManifest, ...] = (
    SdkManifest("voice", API_VERSION, "VoiceResponse"),
    SdkManifest("learning", API_VERSION, "LearningSnapshot"),
    SdkManifest("adaptive", API_VERSION, "AdaptiveDecision"),
    SdkManifest("knowledge", API_VERSION, "KnowledgeSnapshot"),
    SdkManifest("studio", API_VERSION, "StudioRecord"),
    SdkManifest("whiteboard", API_VERSION, "CanvasRecord"),
    SdkManifest("memory_graph", API_VERSION, "GraphQueryResult"),
    SdkManifest("analytics", API_VERSION, "AnalyticsSnapshot"),
    SdkManifest("enterprise", API_VERSION, "EnterpriseSnapshot"),
    SdkManifest("marketplace", API_VERSION, "PluginManifest"),
    SdkManifest("agents", API_VERSION, "AgentRecommendation"),
)

WEBHOOKS: tuple[WebhookSpec, ...] = (
    WebhookSpec("LearningUpdated", True, True),
    WebhookSpec("KnowledgeUpdated", True, True),
    WebhookSpec("ProjectCreated", True, False),
    WebhookSpec("CanvasCreated", True, False),
    WebhookSpec("PluginInstalled", True, False),
    WebhookSpec("OrganizationCreated", True, False),
    WebhookSpec("RecommendationCreated", True, True),
    WebhookSpec("AgentTransferred", True, False),
    WebhookSpec("SessionEnded", True, False),
)


class GatewayService:
    def policy(self) -> GatewayPolicy:
        return GatewayPolicy(
            version=API_VERSION,
            auth="jwt+api_key",
            rate_limit="platform.security",
            health="/api/health",
        )


class WebhookService:
    def catalog(self) -> tuple[WebhookSpec, ...]:
        return WEBHOOKS

    def deliver(self, event: str) -> dict[str, str]:
        publish("WebhookDelivered", event=event)
        return {"event": event, "status": "architected"}


class IntegrationService:
    def register(self, name: IntegrationName) -> dict[str, str]:
        publish("IntegrationRegistered", name=name)
        return {"name": name, "status": "adapter_only"}


class AdapterService:
    def names(self) -> tuple[str, ...]:
        return get_args(IntegrationName)


class CredentialService:
    def rotate(self, token_id: str) -> dict[str, str]:
        return {"id": token_id, "status": "rotated_architected"}


class APITokenService:
    def issue(
        self, owner: str, organization: str | None, role: Role
    ) -> ApiTokenRecord | None:
        if not can(role, "developer.sdk"):
            return None
        record = ApiTokenRecord(
            id=f"tok_{uuid4().hex[:12]}",
            owner=owner,
            organization=organization,
            scopes=("developer.sdk",),
            created_at=time(),
        )
        publish("ApiTokenIssued", id=record.id)
        return record


class DeveloperService:
    def portal_spec(self) -> dict[str, bool]:
        return {
            "api_keys": True,
            "oauth_clients": True,
            "service_accounts": True,
            "sdk_downloads": True,
            "webhooks": True,
            "usage": True,
            "docs": True,
            "samples": True,
            "ui": False,
        }


class SDKService:
    def __init__(self) -> None:
        self.gateway = GatewayService()
        self.webhooks = WebhookService()
        self.integrations = IntegrationService()
        self.adapters = AdapterService()
        self.credentials = CredentialService()
        self.tokens = APITokenService()
        self.developers = DeveloperService()
        self._voice = VoiceService()
        self._learning = LearningService()
        self._adaptive = AdaptiveService()
        self._knowledge = KnowledgeService()
        self._analytics = AnalyticsServiceFacade()
        self._orchestrator = AIOrchestrator()

    def modules(self) -> tuple[SdkManifest, ...]:
        return SDK_MODULES

    def voice(self) -> ApiEnvelope[VoiceResponse]:
        return ok(self._voice.status())

    def learning(self) -> ApiEnvelope[LearningSnapshot]:
        return ok(self._learning.snapshot())

    def adaptive(self, text: str = "") -> ApiEnvelope[AdaptiveDecision]:
        return ok(self._adaptive.decide(text))

    def knowledge(self, query: str) -> ApiEnvelope[KnowledgeSnapshot]:
        return ok(self._knowledge.search(query))

    def analytics(self) -> ApiEnvelope[AnalyticsSnapshot]:
        return ok(self._analytics.snapshot())
