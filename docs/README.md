# Documentation

Public map for SALORA OS. Numbered engineering files and constitutions stay as the archive. Do not add a second Voice Pipeline, SpecialistRouter, Search Platform, or Automation Platform.

If a guide and a constitution disagree, the [Master Constitution](salora/00-master-constitution.md) wins.

**Implemented** — hall, worker, or instrument.  
**Architected** — facade or contract; not the live audio path.  
**Planned** — [41 SALORA OS v1](engineering/41_SALORA_OS_V1_RELEASE.md).

## Start here

| Need | Document |
| --- | --- |
| Run the app | [guides/installation.md](guides/installation.md) |
| Environment variables | [guides/configuration.md](guides/configuration.md) |
| Architecture | [architecture/overview.md](architecture/overview.md) |
| Diagrams | [architecture/diagrams.md](architecture/diagrams.md) |
| Showcase | [salora/SALORA_OS_SHOWCASE.md](salora/SALORA_OS_SHOWCASE.md) |
| Something broke | [guides/troubleshooting.md](guides/troubleshooting.md) |

## Terminology

| Term | Meaning |
| --- | --- |
| Workspace Shell | `OsShell` around hall and instrument routes |
| Voice Pipeline | LiveKit + Deepgram STT + Gemini + Murf Falcon TTS in `agent.py` |
| AI Orchestrator | Intent/provider facade. Does not route specialists |
| SpecialistRouter | Only routing authority for specialist handoff |
| Learning Engine | Projects analytics and memory. Does not store scores on `User` |
| Adaptive Engine | Advises. SpecialistRouter still decides |
| Knowledge Fabric | Semantic projection over existing knowledge search |
| Search Platform | One search. `DiscoveryService` is an alias |
| Automation Platform | One workflow engine. Doc 37 is an alias of 33 |
| Agent Runtime | Hosts agent manifests. No autonomous loops |
| Enterprise Platform | Orgs, workspaces, RBAC. Same `can(role, permission)` |
| Marketplace | Catalog only. `may_execute` is false |
| SDK | Envelope contracts. No portal UI |
| Collaboration | Presence. No CRDT. Voice stays on the Voice Pipeline |

## Tree

```text
docs/
├── README.md                 # This index
├── architecture/             # How components interact
├── engineering/              # Standards + numbered archive (01–51)
├── guides/                   # Install, config, deploy, develop
├── api/                      # HTTP and SDK contracts
├── assets/                   # Screenshots and diagram notes
└── salora/                   # Product constitutions (law)
```

---

## Architecture

| Document | Covers |
| --- | --- |
| [overview.md](architecture/overview.md) | Layers and data flow |
| [diagrams.md](architecture/diagrams.md) | Mermaid maps |
| [backend.md](architecture/backend.md) | Services, providers, orchestrator facade |
| [governance.md](architecture/governance.md) | Privacy, RBAC, compliance |

## Backend

| Document | Covers |
| --- | --- |
| [architecture/backend.md](architecture/backend.md) | Worker and facades |
| [api/backend.md](api/backend.md) | Next.js routes and worker health |
| [backend/README.md](../backend/README.md) | Package setup |

## Frontend

| Document | Covers |
| --- | --- |
| [frontend/README.md](../frontend/README.md) | Hall, instruments, shell |
| [salora/BRAND.md](salora/BRAND.md) | Identity and pulse |
| [engineering/foundations.md](engineering/foundations.md) | UI and coding standards |

## Voice

| Document | Covers |
| --- | --- |
| [voice-platform.md](architecture/voice-platform.md) | Voice Pipeline |
| [17 Voice Architecture](engineering/17_VOICE_ARCHITECTURE.md) | Archive spec |

## AI

| Document | Covers |
| --- | --- |
| [06 AI Architecture](engineering/06_AI_ARCHITECTURE_BIBLE.md) | Archive |
| [18 Living AI Core](engineering/18_LIVING_AI_CORE.md) | Visual host on the existing wave |
| [31 Agent Runtime](engineering/31_AGENT_RUNTIME_PLATFORM.md) | Runtime host; no autonomous loops |

## Learning

| Document | Covers |
| --- | --- |
| [learning-platform.md](architecture/learning-platform.md) | Learning, Adaptive, Fabric |
| [19 Learning Engine](engineering/19_LEARNING_ENGINE.md) | Archive |
| [20 Adaptive Engine](engineering/20_ADAPTIVE_LEARNING_ENGINE.md) | Advice only |
| [21 Knowledge Fabric](engineering/21_KNOWLEDGE_FABRIC.md) | Projection |

## Enterprise

| Document | Covers |
| --- | --- |
| [enterprise-platform.md](architecture/enterprise-platform.md) | Control Center, tenants, collaboration |
| [governance.md](architecture/governance.md) | RBAC and privacy |

## SDK

| Document | Covers |
| --- | --- |
| [api/sdk.md](api/sdk.md) | Envelope v1 and tokens |
| [29 AI SDK](engineering/29_AI_SDK_PLATFORM.md) | Archive |

## Marketplace

| Document | Covers |
| --- | --- |
| [enterprise-platform.md](architecture/enterprise-platform.md) | Catalog; `may_execute` false |
| [27 Marketplace](engineering/27_MARKETPLACE_PLATFORM.md) | Archive |

## Deployment

| Document | Covers |
| --- | --- |
| [guides/installation.md](guides/installation.md) | First run |
| [guides/configuration.md](guides/configuration.md) | Environment variables |
| [guides/deployment.md](guides/deployment.md) | Compose, health, rollback |
| [guides/troubleshooting.md](guides/troubleshooting.md) | Common failures |

## Testing

| Document | Covers |
| --- | --- |
| [guides/development.md](guides/development.md) | Pytest, ruff, tsc, vitest |
| [11 Testing Standard](engineering/11_TESTING_STANDARD.md) | Archive |

## Release

| Document | Covers |
| --- | --- |
| [engineering/release.md](engineering/release.md) | v1 freeze |
| [41 SALORA OS v1](engineering/41_SALORA_OS_V1_RELEASE.md) | Roadmap (consume, do not rewrite) |
| [CHANGELOG.md](../CHANGELOG.md) | Days 1–9 + unreleased |
| [Showcase](salora/SALORA_OS_SHOWCASE.md) | Evidence and checklist |
| [Public release](salora/SALORA_OS_PUBLIC_RELEASE.md) | Final readiness |
| [Evidence](salora/SALORA_OS_EVIDENCE.md) | Inventory and capture list |
| [VoiceForBharat blog](salora/DAY10_BLOG.md) | Official submission post |

## Constitutions and archive

Product law: [salora/](salora/README.md). Full numbered index: [engineering/README.md](engineering/README.md). Challenge history: [salora/VOICEFORBHARAT.md](salora/VOICEFORBHARAT.md).

## Assets

[assets/](assets/README.md). Capture list: [salora/SALORA_OS_SHOWCASE.md](salora/SALORA_OS_SHOWCASE.md) §5.

## Contribute

[CONTRIBUTING.md](../CONTRIBUTING.md)
