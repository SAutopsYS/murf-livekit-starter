"""Plugin + Marketplace. Catalog and manifests only. No execution, no payments."""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Literal

from salora_platform.auth import Role, can
from services.events import publish
from services.repositories import InMemoryDocumentStore

Capability = Literal[
    "voice",
    "learning",
    "adaptive",
    "knowledge",
    "studio",
    "whiteboard",
    "memory_graph",
    "analytics",
    "enterprise",
    "developer",
    "commands",
    "providers",
    "workflows",
    "agents",
]

PluginKind = Literal[
    "plugin",
    "extension",
    "package",
    "module",
    "command",
    "tool",
    "action",
    "provider",
    "integration",
    "workflow",
    "adapter",
]


@dataclass(frozen=True)
class PluginManifest:
    id: str
    name: str
    version: str
    author: str
    publisher: str
    license: str
    permissions: tuple[str, ...]
    capabilities: tuple[Capability, ...]
    dependencies: tuple[str, ...]
    entrypoint: str
    icon: str
    description: str
    organization: str | None
    kind: PluginKind
    created_at: float
    updated_at: float
    signed: bool = False
    enabled: bool = False


@dataclass(frozen=True)
class SandboxPolicy:
    permission_isolation: bool = True
    capability_isolation: bool = True
    api_isolation: bool = True
    storage_isolation: bool = True
    network_policy: str = "deny_by_default"
    resource_limits: str = "cpu_mem_quota"
    execution_policy: str = "no_arbitrary_code"
    lifecycle_hooks: tuple[str, ...] = ("install", "enable", "disable", "remove")


SEED_CATALOG: tuple[PluginManifest, ...] = (
    PluginManifest(
        id="pkg.math-specialist",
        name="Math Practice Specialist",
        version="1.0",
        author="SALORA",
        publisher="salora",
        license="MIT",
        permissions=("voice.session",),
        capabilities=("agents", "learning", "voice"),
        dependencies=("specialists.router",),
        entrypoint="specialists.math_specialist",
        icon="function",
        description="Existing math guest. Install records a catalog row only.",
        organization=None,
        kind="package",
        created_at=0,
        updated_at=0,
        signed=True,
        enabled=True,
    ),
    PluginManifest(
        id="pkg.analytics-export",
        name="Analytics JSON Export",
        version="1.0",
        author="SALORA",
        publisher="salora",
        license="MIT",
        permissions=("analytics.export",),
        capabilities=("analytics",),
        dependencies=("analytics.service",),
        entrypoint="analytics.service",
        icon="chart",
        description="Wraps the existing privacy-safe export. No new store.",
        organization=None,
        kind="adapter",
        created_at=0,
        updated_at=0,
        signed=True,
        enabled=True,
    ),
)


class CapabilityService:
    def allowed(self, role: Role, capability: Capability) -> bool:
        mapping: dict[Capability, str] = {
            "voice": "voice.session",
            "learning": "learning.read",
            "analytics": "analytics.read",
            "enterprise": "enterprise.read",
            "studio": "studio.access",
            "whiteboard": "whiteboard.access",
            "memory_graph": "memory_graph.read",
            "developer": "developer.sdk",
            "agents": "voice.session",
        }
        permission = mapping.get(capability)
        if permission is None:
            return can(role, "marketplace.browse")
        return can(role, permission)  # type: ignore[arg-type]


class SandboxService:
    def policy(self) -> SandboxPolicy:
        return SandboxPolicy()

    def may_execute(self) -> bool:
        return False


class PluginService:
    def __init__(self, store: InMemoryDocumentStore | None = None) -> None:
        self._store = store or InMemoryDocumentStore()
        for item in SEED_CATALOG:
            self._store.put(item.id, item.__dict__)

    def list(self) -> list[PluginManifest]:
        return [PluginManifest(**row) for row in self._store.list()]

    def get(self, plugin_id: str) -> PluginManifest | None:
        raw = self._store.get(plugin_id)
        return PluginManifest(**raw) if raw else None

    def enable(self, plugin_id: str) -> PluginManifest | None:
        item = self.get(plugin_id)
        if item is None:
            return None
        updated = PluginManifest(
            **{**item.__dict__, "enabled": True, "updated_at": time()}
        )
        self._store.put(plugin_id, updated.__dict__)
        publish("PluginEnabled", id=plugin_id)
        return updated


class CatalogService:
    def __init__(self, plugins: PluginService) -> None:
        self._plugins = plugins

    def search(self, query: str) -> list[PluginManifest]:
        needle = query.lower().strip()
        rows = self._plugins.list()
        if not needle:
            return rows
        return [
            item for item in rows if needle in item.name.lower() or needle in item.id
        ]


class InstallService:
    def install(self, manifest: PluginManifest) -> PluginManifest:
        publish("PluginInstalled", id=manifest.id)
        publish("PackageDownloaded", id=manifest.id)
        return manifest

    def remove(self, plugin_id: str) -> None:
        publish("PluginRemoved", id=plugin_id)


class UpdateService:
    def update(self, plugin_id: str, version: str) -> dict[str, str]:
        publish("PluginUpdated", id=plugin_id, version=version)
        return {"id": plugin_id, "version": version, "status": "architected"}


class PackageService:
    def publish(self, manifest: PluginManifest) -> PluginManifest:
        publish("PackagePublished", id=manifest.id)
        return manifest


class ExtensionService:
    def from_manifest(self, manifest: PluginManifest) -> PluginManifest:
        return manifest


class MarketplaceService:
    def __init__(self) -> None:
        self.plugins = PluginService()
        self.catalog = CatalogService(self.plugins)
        self.installs = InstallService()
        self.updates = UpdateService()
        self.packages = PackageService()
        self.extensions = ExtensionService()
        self.capabilities = CapabilityService()
        self.sandbox = SandboxService()

    def open(self) -> list[PluginManifest]:
        publish("MarketplaceOpened")
        return self.catalog.search("")

    def may_browse(self, role: Role) -> bool:
        return can(role, "marketplace.browse")
