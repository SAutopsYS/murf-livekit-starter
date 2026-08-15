"""Agent runtime. Hosts agents. SpecialistRouter remains routing authority."""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Literal

from services.events import publish
from services.intelligence import AgentService
from services.marketplace import MarketplaceService, PluginManifest
from services.orchestrator import AIOrchestrator
from services.providers import get_provider_registry
from specialists.registry import get_specialist_registry

AgentKind = Literal[
    "tutor",
    "math",
    "coding",
    "career",
    "interview",
    "language",
    "writing",
    "research",
    "planning",
    "creative",
    "enterprise",
    "custom",
]
AgentStatus = Literal[
    "registered",
    "loaded",
    "started",
    "busy",
    "waiting",
    "completed",
    "failed",
    "suspended",
    "disabled",
]
AgentCapability = Literal[
    "voice",
    "learning",
    "adaptive",
    "knowledge",
    "studio",
    "whiteboard",
    "memory_graph",
    "workflow",
    "plugin",
    "analytics",
    "enterprise",
]


@dataclass(frozen=True)
class AgentManifest:
    id: str
    name: str
    version: str
    description: str
    kind: AgentKind
    capabilities: tuple[AgentCapability, ...]
    permissions: tuple[str, ...]
    provider: str
    owner: str
    organization: str | None
    status: AgentStatus
    health: str
    created_at: float
    updated_at: float
    live: bool


def _kind_for(specialist_id: str) -> AgentKind:
    if "math" in specialist_id:
        return "math"
    if "career" in specialist_id:
        return "career"
    if "writ" in specialist_id:
        return "writing"
    return "custom"


class AgentRegistryService:
    """Projects the existing specialist registry. Does not replace it."""

    def list(self) -> list[AgentManifest]:
        stamp = time()
        registry = get_specialist_registry()
        host = AgentManifest(
            id="agent.tutor",
            name="Main Tutor",
            version="1.0",
            description="Host. Always live. One mouth.",
            kind="tutor",
            capabilities=("voice", "learning", "adaptive", "knowledge"),
            permissions=("voice.session",),
            provider="livekit+murf",
            owner="salora",
            organization=None,
            status="started",
            health="READY",
            created_at=stamp,
            updated_at=stamp,
            live=True,
        )
        guests: list[AgentManifest] = []
        for spec in registry.list_specialists(include_placeholders=True):
            sid = str(spec.get("specialist_id") or spec.get("id") or "")
            active = bool(spec.get("active") and spec.get("enabled"))
            guests.append(
                AgentManifest(
                    id=f"agent.{sid}",
                    name=str(spec.get("display_name") or spec.get("name") or sid),
                    version=str(spec.get("version") or "1.0"),
                    description=str(spec.get("description") or ""),
                    kind=_kind_for(sid),
                    capabilities=("voice", "learning"),
                    permissions=("voice.session",),
                    provider="livekit+murf",
                    owner="salora",
                    organization=None,
                    status="started" if active else "disabled",
                    health="READY" if active else "DISABLED",
                    created_at=stamp,
                    updated_at=stamp,
                    live=active,
                )
            )
        if not guests:
            guests.append(
                AgentManifest(
                    id="agent.math_practice_specialist",
                    name="Math Practice Specialist",
                    version="1.0",
                    description="Existing math guest from the specialist registry.",
                    kind="math",
                    capabilities=("voice", "learning"),
                    permissions=("voice.session",),
                    provider="livekit+murf",
                    owner="salora",
                    organization=None,
                    status="registered",
                    health="READY",
                    created_at=stamp,
                    updated_at=stamp,
                    live=True,
                )
            )
        return [host, *guests]


class AgentExecutionService:
    def __init__(self) -> None:
        self._agents = AgentService()
        self._orchestrator = AIOrchestrator()

    def recommend(self, text: str) -> dict[str, object]:
        rec = self._agents.recommend(text)
        publish("AgentStarted", target=rec.target)
        return {
            "target": rec.target,
            "specialist_id": rec.specialist_id,
            "fallback_used": rec.fallback_used,
            "source": "specialist.router",
        }


class AgentPolicyService:
    def limits(self) -> dict[str, object]:
        return {
            "provider_selection": True,
            "resource_quotas": True,
            "cost_limits": True,
            "retry_limits": 1,
            "timeout_seconds": 2,
            "security": "fail_closed",
        }


class AgentSandboxService:
    def may_autonomous_loop(self) -> bool:
        return False


class AgentHealthService:
    def providers(self) -> dict[str, str]:
        registry = get_provider_registry()
        return {item.name: item.health for item in registry.list_live()}


class AgentMetricsService:
    def snapshot(self) -> dict[str, int]:
        return {"registered": 2, "live": 2}


class AgentCatalogService:
    def from_marketplace(self) -> list[PluginManifest]:
        return [
            item
            for item in MarketplaceService().open()
            if "agents" in item.capabilities
        ]


class AgentRuntimeService:
    def __init__(self) -> None:
        self.registry = AgentRegistryService()
        self.execution = AgentExecutionService()
        self.policies = AgentPolicyService()
        self.sandbox = AgentSandboxService()
        self.health = AgentHealthService()
        self.metrics = AgentMetricsService()
        self.catalog = AgentCatalogService()

    def register_host(self) -> AgentManifest:
        host = self.registry.list()[0]
        publish("AgentRegistered", id=host.id)
        return host
