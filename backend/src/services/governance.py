"""Governance and compliance. Wraps existing privacy + RBAC. No new auth."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from salora_platform.auth import Role, can
from salora_platform.security import PRIVACY_RULES, audit
from services.events import publish
from services.tenants import PolicyKind, PolicyService

Framework = Literal["GDPR", "COPPA", "FERPA", "SOC2", "ISO27001", "HIPAA", "AI"]


@dataclass(frozen=True)
class ComplianceCheck:
    framework: Framework
    ok: bool
    source: str


class ConsentService:
    def grant(self, subject: str) -> dict[str, str]:
        publish("ConsentGranted", subject=subject)
        return {"subject": subject, "status": "granted"}


class ComplianceService:
    def check(self, framework: Framework) -> ComplianceCheck:
        ok = bool(
            PRIVACY_RULES["no_utterance_fields"]
            and PRIVACY_RULES["consent_before_memory"]
        )
        if framework == "HIPAA":
            ok = False
        publish("ComplianceChecked", framework=framework)
        return ComplianceCheck(
            framework=framework, ok=ok, source="salora_platform.security"
        )


class GovernanceService:
    def __init__(self) -> None:
        self.compliance = ComplianceService()
        self.consent = ConsentService()
        self.policies = PolicyService()

    def apply(self, organization_id: str, kind: PolicyKind, role: Role) -> bool:
        if not can(role, "enterprise.admin"):
            return False
        self.policies.set(organization_id, kind, True)
        publish("PolicyApplied", org=organization_id, kind=kind)
        audit("governance.policy", org=organization_id, kind=kind)
        return True

    def audit_pack(self) -> dict[str, object]:
        publish("AuditGenerated")
        return {"privacy": dict(PRIVACY_RULES), "utterance_column": False}


class RiskService:
    def hipaa_claimed(self) -> bool:
        return False


class AuditCenter:
    def pack(self) -> dict[str, object]:
        return GovernanceService().audit_pack()


CertificationService = ComplianceService
CertificationEngine = ComplianceService
ComplianceProvider = GovernanceService
