"""Education, mentors, solutions, public API, infra, ecosystem — consumers only."""

from __future__ import annotations

from services.cloud import CloudService, GlobalDeploymentService
from services.ecosystem import EcosystemService
from services.education import EducationService, ExperienceEngine, ExperiencePolicies
from services.events import recent_events, reset_events
from services.governance import (
    CertificationService,
    ComplianceService,
    GovernanceService,
)
from services.infrastructure import InfrastructureService
from services.mentors import MentorService
from services.optimization import OptimizationService
from services.public_api import PublicAPIService
from services.solutions import SolutionService


def setup_function() -> None:
    reset_events()


def test_education_wraps_learning_and_enterprise() -> None:
    assert ExperienceEngine is EducationService
    assert ExperiencePolicies().spec()["scores_persist"] is False
    edu = EducationService()
    student = edu.students.snapshot()
    assert student.source == "learning.service"
    teacher = edu.teachers.console()
    assert "students" in teacher
    assert "count" in teacher
    edu.assignments.submit("Practice")
    assert recent_events("AssignmentSubmitted")


def test_mentors_use_agent_runtime() -> None:
    mentors = MentorService()
    session = mentors.tutor.start()
    assert session.source == "agent.runtime"
    assert session.kind == "tutor"
    rec = mentors.recommend("fractions")
    assert rec["source"] == "specialist.router"
    assert recent_events("RecommendationGenerated")


def test_solutions_and_public_api() -> None:
    org = SolutionService().deploy("school", "admin")
    assert org.kind == "organization"
    api = PublicAPIService()
    assert api.issue_key("x", "guest") is None
    token = api.issue_key("dev", "developer")
    assert token is not None
    assert api.docs.spec()["portal_ui"] is False


def test_infra_opt_cloud_gov_aliases() -> None:
    infra = InfrastructureService().catalog()
    assert all(item.implemented is False for item in infra)
    assert OptimizationService().plan().voice_untouched is True
    assert GlobalDeploymentService is CloudService
    assert CertificationService is ComplianceService
    pack = GovernanceService().audit_pack()
    assert pack["utterance_column"] is False
    assert EcosystemService().verify("pkg.math-specialist")["execute"] is False
