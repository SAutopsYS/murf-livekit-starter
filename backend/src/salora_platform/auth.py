"""Server-side roles and permissions. Mirrors frontend/lib/platform/rbac.ts."""

from __future__ import annotations

from typing import Literal

Role = Literal[
    "anonymous",
    "guest",
    "student",
    "parent",
    "teacher",
    "enterprise_admin",
    "developer",
    "operator",
]

Permission = Literal[
    "voice.session",
    "analytics.read",
    "analytics.export",
    "enterprise.read",
    "enterprise.export",
    "enterprise.admin",
    "learning.read",
    "developer.sdk",
    "marketplace.browse",
    "studio.access",
    "whiteboard.access",
    "memory_graph.read",
]

ROLES: tuple[Role, ...] = (
    "anonymous",
    "guest",
    "student",
    "parent",
    "teacher",
    "enterprise_admin",
    "developer",
    "operator",
)

PERMISSIONS: tuple[Permission, ...] = (
    "voice.session",
    "analytics.read",
    "analytics.export",
    "enterprise.read",
    "enterprise.export",
    "enterprise.admin",
    "learning.read",
    "developer.sdk",
    "marketplace.browse",
    "studio.access",
    "whiteboard.access",
    "memory_graph.read",
)

_ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    "anonymous": frozenset({"voice.session"}),
    "guest": frozenset({"voice.session"}),
    "student": frozenset({"voice.session", "learning.read"}),
    "parent": frozenset(
        {"voice.session", "learning.read", "analytics.read", "enterprise.read"}
    ),
    "teacher": frozenset(
        {
            "voice.session",
            "learning.read",
            "analytics.read",
            "analytics.export",
            "enterprise.read",
            "studio.access",
            "whiteboard.access",
            "memory_graph.read",
        }
    ),
    "enterprise_admin": frozenset(
        {
            "voice.session",
            "learning.read",
            "analytics.read",
            "analytics.export",
            "enterprise.read",
            "enterprise.export",
            "enterprise.admin",
            "studio.access",
            "whiteboard.access",
            "memory_graph.read",
            "marketplace.browse",
        }
    ),
    "developer": frozenset(
        {
            "voice.session",
            "analytics.read",
            "developer.sdk",
            "learning.read",
            "studio.access",
            "memory_graph.read",
            "marketplace.browse",
        }
    ),
    "operator": frozenset(PERMISSIONS),
}

_UI_ROLES = {
    "admin": "enterprise_admin",
    "teacher": "teacher",
    "parent": "parent",
}


def role_from_enterprise_ui(value: str | None) -> Role:
    if not value:
        return "guest"
    mapped = _UI_ROLES.get(value)
    if mapped in ROLES:
        return mapped  # type: ignore[return-value]
    if value in ROLES:
        return value  # type: ignore[return-value]
    return "guest"


def can(role: Role, permission: Permission) -> bool:
    return permission in _ROLE_PERMISSIONS[role]


def authorize(
    role: Role, permission: Permission, *, auth_required: bool
) -> tuple[bool, int]:
    """Return (allowed, http_status). Auth off keeps instrument reads open."""
    open_optional = {
        "analytics.read",
        "analytics.export",
        "enterprise.read",
        "enterprise.export",
        "learning.read",
    }
    if not auth_required and permission in open_optional:
        return True, 200
    if role == "anonymous" and permission != "voice.session":
        return False, 401
    if not can(role, permission):
        return False, 403
    return True, 200
