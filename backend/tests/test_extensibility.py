"""Marketplace, tenants, SDK, collaboration, agent runtime — consumers only."""

from __future__ import annotations

from services.agent_runtime import AgentRuntimeService
from services.collaboration import CollaborationService
from services.events import recent_events, reset_events
from services.marketplace import MarketplaceService
from services.sdk import SDKService
from services.tenants import TenantService


def setup_function() -> None:
    reset_events()


def test_marketplace_catalog_no_execution() -> None:
    market = MarketplaceService()
    catalog = market.open()
    assert catalog
    assert market.sandbox.may_execute() is False
    assert market.may_browse("developer") is True
    assert market.may_browse("anonymous") is False
    assert recent_events("MarketplaceOpened")


def test_tenant_maps_membership_to_rbac() -> None:
    cloud = TenantService()
    org = cloud.organizations.create("North School", "admin")
    member = cloud.memberships.invite(org.id, "t1", "teacher")
    assert member.role == "teacher"
    cloud.memberships.join(member)
    assert cloud.audit.may_admin("enterprise_admin") is True
    assert cloud.billing.subscription is True


def test_sdk_exposes_typed_envelopes() -> None:
    sdk = SDKService()
    voice = sdk.voice()
    assert voice.ok is True
    assert voice.data is not None
    assert voice.data.transport == "livekit"
    assert sdk.tokens.issue("dev", None, "guest") is None
    token = sdk.tokens.issue("dev", None, "developer")
    assert token is not None
    assert "slack" in sdk.adapters.names()


def test_collaboration_has_no_crdt() -> None:
    collab = CollaborationService()
    session = collab.sessions.create("studio", "ws_1", "teacher")
    collab.participants.join(session.id, "u1")
    assert session.kind == "studio"
    assert collab.may_join("teacher", "editor") is True
    assert recent_events("SessionCreated")


def test_agent_runtime_does_not_replace_router() -> None:
    runtime = AgentRuntimeService()
    agents = runtime.registry.list()
    assert agents[0].kind == "tutor"
    assert runtime.sandbox.may_autonomous_loop() is False
    rec = runtime.execution.recommend("multiply fractions")
    assert rec["source"] == "specialist.router"
