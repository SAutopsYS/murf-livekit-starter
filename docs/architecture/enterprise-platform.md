# Enterprise Platform

Orgs, workspaces, catalog, contracts, presence, and agent hosting. Same RBAC as the rest of the OS.

## Enterprise Cloud

Canonical: [28 Enterprise Cloud](../engineering/28_ENTERPRISE_CLOUD_PLATFORM.md).

Organizations, workspaces, memberships map onto existing `Role`. Isolation today is RBAC plus in-memory tenant records. Identity issuance still waits on a roster. `AUTH_REQUIRED` defaults false so anonymous voice stays first-class.

Control Center lives at `/enterprise`.

## Marketplace

Canonical: [27 Marketplace](../engineering/27_MARKETPLACE_PLATFORM.md).

Plugin catalog. `may_execute` is false. Verified is not runnable.

## SDK

Canonical: [29 AI SDK](../engineering/29_AI_SDK_PLATFORM.md). Public wrap: [45 Public API](../engineering/45_PUBLIC_API_PLATFORM.md).

`ApiEnvelope` v1. Tokens via existing token service. No developer portal UI.

## Collaboration

Canonical: [30 Collaboration](../engineering/30_COLLABORATION_PLATFORM.md).

Presence only. `crdt` is false. Voice stays on the Voice Pipeline.

## Agent Runtime

Canonical: [31 Agent Runtime](../engineering/31_AGENT_RUNTIME_PLATFORM.md).

Hosts the live tutor and registered guests. `may_autonomous_loop` is false. SpecialistRouter remains the routing authority.

## Education and mentors

Teacher / student / parent and mentor suites consume the engines above. They do not add dashboards on the hall.

- [42 Education Experience](../engineering/42_EDUCATION_EXPERIENCE_PLATFORM.md)
- [43 AI Mentor Suite](../engineering/43_AI_MENTOR_SUITE_PLATFORM.md)

## Related

- [Governance](governance.md)
- [api/sdk.md](../api/sdk.md)
