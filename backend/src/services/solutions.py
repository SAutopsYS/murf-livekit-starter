"""Industry solutions. Org-scoped profiles. No new tenant engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from services.events import publish
from services.tenants import OrganizationRecord, TenantService

Industry = Literal[
    "school",
    "university",
    "coaching",
    "corporate",
    "government",
    "ngo",
    "healthcare_education",
]


@dataclass(frozen=True)
class IndustryProfile:
    industry: Industry
    workspace: str
    policies: tuple[str, ...]


PROFILES: tuple[IndustryProfile, ...] = (
    IndustryProfile("school", "classroom", ("learning", "voice", "coppa")),
    IndustryProfile("university", "organization", ("learning", "ferpa")),
    IndustryProfile("coaching", "team", ("learning", "marketplace")),
    IndustryProfile("corporate", "enterprise", ("security", "retention")),
    IndustryProfile("government", "enterprise", ("security", "residency")),
    IndustryProfile("ngo", "shared", ("learning",)),
    IndustryProfile("healthcare_education", "organization", ("hipaa_arch", "consent")),
)


class SchoolService:
    def profile(self) -> IndustryProfile:
        return PROFILES[0]


class UniversityService:
    def profile(self) -> IndustryProfile:
        return PROFILES[1]


class CorporateService:
    def profile(self) -> IndustryProfile:
        return PROFILES[3]


class GovernmentService:
    def profile(self) -> IndustryProfile:
        return PROFILES[4]


class SolutionService:
    def __init__(self) -> None:
        self.tenants = TenantService()
        self.schools = SchoolService()
        self.universities = UniversityService()
        self.corporate = CorporateService()
        self.government = GovernmentService()

    def deploy(self, industry: Industry, owner: str) -> OrganizationRecord:
        org = self.tenants.organizations.create(industry, owner)
        publish("SolutionDeployed", industry=industry, org=org.id)
        return org

    def profiles(self) -> tuple[IndustryProfile, ...]:
        return PROFILES


class DeploymentProfiles:
    def spec(self) -> dict[str, str]:
        return {"tenants": "TenantService", "rollback": "previous_image_and_env"}


EnterpriseSolutionProvider = SolutionService
SolutionEngine = SolutionService
IndustryProfiles = PROFILES
