"""Phases 21-29 consumers. One search. One automation. No new memory."""

from __future__ import annotations

from services.automation import AutomationService, WorkflowAutomationService
from services.clients import DesktopService, MobileService
from services.cloud import CloudService
from services.events import recent_events, reset_events
from services.governance import GovernanceService
from services.productivity import ProductivityService
from services.search import DiscoveryService, SearchService


def setup_function() -> None:
    reset_events()


def test_search_reuses_knowledge_and_catalog() -> None:
    result = SearchService().search("english", mode="hybrid")
    assert result.mode == "hybrid"
    sources = {hit.source for hit in result.hits}
    assert "knowledge.search" in sources or result.hits == ()
    alias = DiscoveryService().search("english")
    assert alias.mode == "hybrid"
    assert recent_events("SearchStarted")


def test_automation_is_one_engine() -> None:
    assert WorkflowAutomationService is AutomationService
    engine = AutomationService()
    wf = engine.create("teacher", "LearningFinished")
    engine.execute(wf)
    assert recent_events("WorkflowCreated")
    assert recent_events("WorkflowCompleted")


def test_productivity_wraps_studio() -> None:
    snap = ProductivityService().snapshot("teacher")
    assert snap.source == "studio"
    assert ProductivityService().mail.spec()["client"] is False


def test_clients_share_sdk_modules() -> None:
    mobile = MobileService().session()
    desktop = DesktopService().session()
    assert mobile.kind == "mobile"
    assert desktop.kind == "desktop"
    assert "voice" in mobile.modules
    assert "voice" in desktop.modules


def test_governance_refuses_utterance_and_hipaa_default() -> None:
    gov = GovernanceService()
    pack = gov.audit_pack()
    assert pack["utterance_column"] is False
    assert gov.compliance.check("GDPR").ok is True
    assert gov.compliance.check("HIPAA").ok is False
    assert gov.apply("org_1", "retention", "guest") is False
    assert gov.apply("org_1", "retention", "enterprise_admin") is True


def test_cloud_uses_existing_health() -> None:
    cloud = CloudService()
    cluster = cloud.clusters.snapshot()
    assert cluster["liveness"] == "ok"
    assert cloud.deployments.strategy()["rollback"] == "previous_image_and_env"
    cloud.backups.run()
    assert recent_events("BackupCompleted")
