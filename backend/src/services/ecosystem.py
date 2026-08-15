"""SALORA ecosystem. Marketplace + Studio templates. No second catalog."""

from __future__ import annotations

from services.events import publish
from services.marketplace import MarketplaceService, PluginManifest
from services.studio import TemplateService as StudioTemplateService


class CommunityService:
    def plugins(self) -> list[PluginManifest]:
        return MarketplaceService().open()


class TemplateHub:
    def __init__(self) -> None:
        self._templates = StudioTemplateService()

    def apply(self, title: str, owner: str) -> object:
        return self._templates.apply(title, owner)


class EcosystemService:
    def __init__(self) -> None:
        self.community = CommunityService()
        self.templates = TemplateHub()
        self.marketplace = MarketplaceService()

    def verify(self, plugin_id: str) -> dict[str, object]:
        item = self.marketplace.plugins.get(plugin_id)
        publish("ExtensionVerified", id=plugin_id)
        return {"id": plugin_id, "signed": bool(item and item.signed), "execute": False}


EcosystemProvider = EcosystemService
CommunityRegistry = CommunityService
ExtensionHub = EcosystemService
TemplateRegistry = TemplateHub
TemplateService = StudioTemplateService
