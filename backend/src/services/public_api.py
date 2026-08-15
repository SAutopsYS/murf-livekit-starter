"""Public API. Wraps SDKService. No portal UI. No second auth."""

from __future__ import annotations

from salora_platform.auth import Role
from services.events import publish
from services.sdk import ApiTokenRecord, APITokenService, GatewayService, SDKService


class OAuthService:
    def grant(self, client_id: str) -> dict[str, str]:
        publish("OAuthGranted", client=client_id)
        return {"client": client_id, "status": "architected", "protocol": "oauth2.1"}


class APIDocumentationService:
    def spec(self) -> dict[str, object]:
        return {"openapi": "architected", "version": "v1", "portal_ui": False}


class PublicAPIService:
    def __init__(self) -> None:
        self.sdk = SDKService()
        self.gateway = GatewayService()
        self.oauth = OAuthService()
        self.docs = APIDocumentationService()
        self.tokens = APITokenService()

    def issue_key(self, owner: str, role: Role) -> ApiTokenRecord | None:
        token = self.tokens.issue(owner, None, role)
        if token:
            publish("APIKeyIssued", id=token.id)
        return token

    def register_client(self, name: str) -> dict[str, str]:
        publish("ClientRegistered", name=name)
        return {"name": name, "status": "architected"}


class APIConsole:
    def spec(self) -> dict[str, bool]:
        return {"ui": False}


class DeveloperPortalArchitecture:
    def spec(self) -> dict[str, object]:
        return {"portal_ui": False, "sdk": True, "oauth": "architected"}


PublicAPIProvider = PublicAPIService
PublicGateway = GatewayService
OAuthRegistry = OAuthService
