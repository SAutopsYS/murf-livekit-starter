"""Enterprise cloud / multi-tenant. Organization-aware. No billing UI."""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Literal
from uuid import uuid4

from salora_platform.auth import Role, can, role_from_enterprise_ui
from services.events import publish
from services.repositories import InMemoryDocumentStore

TenantKind = Literal[
    "tenant",
    "organization",
    "workspace",
    "department",
    "school",
    "classroom",
    "team",
    "project",
    "group",
    "division",
]
WorkspaceKind = Literal[
    "personal",
    "organization",
    "classroom",
    "team",
    "enterprise",
    "shared",
]
MembershipKind = Literal[
    "owner",
    "administrator",
    "manager",
    "teacher",
    "parent",
    "student",
    "developer",
    "guest",
    "observer",
]
PolicyKind = Literal[
    "ai",
    "learning",
    "voice",
    "security",
    "retention",
    "marketplace",
    "plugin",
    "studio",
    "whiteboard",
]


MEMBER_TO_ROLE: dict[MembershipKind, Role] = {
    "owner": "enterprise_admin",
    "administrator": "enterprise_admin",
    "manager": "teacher",
    "teacher": "teacher",
    "parent": "parent",
    "student": "student",
    "developer": "developer",
    "guest": "guest",
    "observer": "guest",
}


@dataclass
class OrganizationRecord:
    id: str
    name: str
    slug: str
    owner: str
    kind: TenantKind
    plan: str
    settings: dict[str, str]
    metadata: dict[str, str]
    created_at: float
    updated_at: float


@dataclass
class WorkspaceRecord:
    id: str
    organization_id: str
    name: str
    kind: WorkspaceKind
    owner: str
    created_at: float
    updated_at: float


@dataclass
class MembershipRecord:
    id: str
    organization_id: str
    subject: str
    membership: MembershipKind
    role: Role
    status: str
    created_at: float


@dataclass
class PolicyRecord:
    kind: PolicyKind
    organization_id: str
    enabled: bool
    body: str


@dataclass
class BillingSpec:
    """Architecture only. No payment."""

    subscription: bool = True
    usage: bool = True
    quotas: bool = True
    seats: bool = True
    licenses: bool = True
    storage: bool = True
    ai_credits: bool = True
    feature_access: bool = True


def _slug(name: str) -> str:
    return name.lower().strip().replace(" ", "-")[:48]


class OrganizationService:
    def __init__(self, store: InMemoryDocumentStore | None = None) -> None:
        self._store = store or InMemoryDocumentStore()

    def create(self, name: str, owner: str) -> OrganizationRecord:
        stamp = time()
        record = OrganizationRecord(
            id=f"org_{uuid4().hex[:10]}",
            name=name,
            slug=_slug(name),
            owner=owner,
            kind="organization",
            plan="standard",
            settings={},
            metadata={},
            created_at=stamp,
            updated_at=stamp,
        )
        self._store.put(record.id, record.__dict__)
        publish("OrganizationCreated", id=record.id)
        return record

    def get(self, org_id: str) -> OrganizationRecord | None:
        raw = self._store.get(org_id)
        return OrganizationRecord(**raw) if raw else None


class WorkspaceService:
    def create(
        self, organization_id: str, name: str, kind: WorkspaceKind, owner: str
    ) -> WorkspaceRecord:
        stamp = time()
        record = WorkspaceRecord(
            id=f"ws_{uuid4().hex[:10]}",
            organization_id=organization_id,
            name=name,
            kind=kind,
            owner=owner,
            created_at=stamp,
            updated_at=stamp,
        )
        publish("WorkspaceCreated", id=record.id, org=organization_id)
        return record


class MembershipService:
    def invite(
        self, organization_id: str, subject: str, membership: MembershipKind
    ) -> MembershipRecord:
        record = MembershipRecord(
            id=f"mem_{uuid4().hex[:8]}",
            organization_id=organization_id,
            subject=subject,
            membership=membership,
            role=MEMBER_TO_ROLE[membership],
            status="invited",
            created_at=time(),
        )
        publish("MemberInvited", id=record.id, org=organization_id)
        return record

    def join(self, record: MembershipRecord) -> MembershipRecord:
        record.status = "active"
        publish("MemberJoined", id=record.id)
        return record

    def remove(self, record: MembershipRecord) -> None:
        record.status = "removed"
        publish("MemberRemoved", id=record.id)

    def role_for(self, membership: MembershipKind) -> Role:
        return MEMBER_TO_ROLE[membership]


class InvitationService:
    def approve(self, record: MembershipRecord) -> MembershipRecord:
        return MembershipService().join(record)


class PolicyService:
    def set(
        self, organization_id: str, kind: PolicyKind, enabled: bool, body: str = ""
    ) -> PolicyRecord:
        record = PolicyRecord(
            kind=kind, organization_id=organization_id, enabled=enabled, body=body
        )
        publish("PolicyUpdated", org=organization_id, kind=kind)
        return record


class DirectoryService:
    def members(self, rows: list[MembershipRecord]) -> list[MembershipRecord]:
        return [row for row in rows if row.status == "active"]


class AuditService:
    def may_admin(self, role: Role) -> bool:
        return can(role, "enterprise.admin")


class TenantService:
    def __init__(self) -> None:
        self.organizations = OrganizationService()
        self.workspaces = WorkspaceService()
        self.memberships = MembershipService()
        self.invitations = InvitationService()
        self.policies = PolicyService()
        self.directory = DirectoryService()
        self.audit = AuditService()
        self.billing = BillingSpec()

    def map_ui_role(self, value: str) -> Role:
        return role_from_enterprise_ui(value)
