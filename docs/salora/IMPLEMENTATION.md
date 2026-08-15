# SALORA Implementation Plan

Evolve the working Murf + LiveKit tutor. Do not rewrite the kernel.

Public docs: [../README.md](../README.md). Release: [../engineering/release.md](../engineering/release.md).

## Audit (done)

Reusable and must stay:

- LiveKit session + Murf Falcon (`Anisha`) — one voice path
- Memory, knowledge tools, scoring, telephony, escalation
- Specialist router (Math live; others registered)
- Analytics `/analytics` and Control Center `/enterprise`
- Next.js App Router, shadcn/agents-ui, wave visualizer

Gaps Phase 1 closes:

- Murf logos 404 → SALORA mark
- Sky challenge skin → sage pulse tokens
- Theme toggle hover-only → always visible
- No brand source of truth in code

## Milestones

| Stage | Status | Rule |
|---|---|---|
| A Foundation (docs) | Written | Target monorepo; voice stays Python |
| B Core Platform (docs) | Written | Shared identity later; do not fork now |
| C Learning Engine (docs) | Written | Engine is domain; voice is client |
| **Phase 1 Brand** | **Done** | Identity, tokens, README. No pipeline change |
| **Phase 2 Design system** | **Done** | Tokens expanded. `ui` + `system`. Instruments migrated |
| **Phase 3 Workspace shell** | **Done** | `OsShell` wraps routes. Session stays. ⌘K |
| **Phase 4 Voice foundation** | **Done** | One state machine + events. Wave stays |
| **Phase 5 Living AI Core** | **Done** | Visual host on the existing wave. No second engine |
| **Phase 6 Learning intelligence** | **Done** | Engine projects existing APIs. No XP UI |
| **Phase 7 Adaptive engine** | **Done** | Decisions + mastery + revision. Router stays authority |
| **Phase 8 Knowledge fabric** | **Done** | Semantic memory projection. No graph UI |
| Phase 9–10 | Later | Add on services. No XP that shames. Guests keep one voice family |
| **Phase 11 Production** | **Done** | Auth, RBAC, config, observe, Docker, CI. Product surfaces untouched |
| **Phase 12 Backend platform** | **Done** | Services wrap worker. Router stays authority |
| **Phase 13 AI Studio** | **Done** | Architecture + commands. No editor |
| **Phase 14 Whiteboard** | **Done** | Canvas model. No renderer |
| **Phase 15 Memory Graph** | **Done** | Explores fabric. No second memory |
| **Phase 16 Marketplace** | **Done** | Plugin catalog. No payments, no exec |
| **Phase 17 Enterprise Cloud** | **Done** | Orgs and workspaces. Same RBAC |
| **Phase 18 AI SDK** | **Done** | Envelopes + adapters. No portal UI |
| **Phase 19 Collaboration** | **Done** | Presence. No CRDT. Voice stays |
| **Phase 20 Agent runtime** | **Done** | Hosts agents. Router stays authority |
| **Phase 21–27 Search + automation** | **Done** | One search. One workflow engine |
| **Phase 23–25 Clients** | **Done** | Productivity / mobile / desktop contracts |
| **Phase 28–29 Governance + cloud** | **Done** | Compliance wrap. Region spec |
| **Phase 30 v1.0 freeze** | **Done** | [41](../engineering/41_SALORA_OS_V1_RELEASE.md) |
| **Phase 31–39 Experiences** | **Done** | Education, mentors, solutions, API, infra, ecosystem |
| **Phase 40 v2 vision** | **Done** | [51](../engineering/51_SALORA_OS_V2_VISION.md) — no implementation |

## After every milestone

App still talks. Tests still run. No second STT/TTS. No utterance column.

## Now

Phases 1–40 are documented. v1 kernel is frozen. v2 is vision only. New work consumes contracts. Do not add a second search, automation, router, voice path, or memory store.
