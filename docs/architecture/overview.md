# Architecture overview

SALORA OS is a voice-first learning product. The browser talks to LiveKit. The Python worker talks to LiveKit. They do not call each other for audio.

Detailed specs stay in [engineering/](../engineering/README.md). This page is the map. Mermaid: [diagrams.md](diagrams.md).

## Layers

```text
Browser (Workspace Shell)
  hall  → Voice Pipeline UI
  /analytics, /enterprise → instruments
        │
        │  JWT token  ·  health  ·  CLI analytics
        ▼
Next.js API  +  salora_platform (auth, RBAC, config)
        │
        ▼
LiveKit Cloud
        │
        ▼
Python worker (agent.py)
  Voice Pipeline: Deepgram → Gemini → Murf Falcon
  SpecialistRouter (only routing authority)
  memory.db (consented profile)  ·  analytics.db (anonymous ops)
        │
        ▼
Service facades (AI Orchestrator, Search, Automation, tenants, …)
```

## Component map

| Component | Job | Does not |
| --- | --- | --- |
| Workspace Shell | Nav, command palette, theme, error boundary | Own the voice session |
| Voice Pipeline | One STT → LLM → TTS path | Persist transcripts |
| AI Orchestrator | Intent and provider facade | Replace SpecialistRouter |
| Learning Engine | Project progress from existing APIs | Write scores onto `User` |
| Adaptive Engine | Advise next action | Route specialists |
| Knowledge Fabric | Semantic view of knowledge search | Create a second memory DB |
| Search Platform | One query across knowledge, catalog, agents | Stand up a vector store |
| Automation Platform | One workflow engine | Add a second queue runtime |
| Agent Runtime | Host tutor + registered guests | Run autonomous loops |
| Enterprise Platform | Orgs, workspaces, same RBAC | Fork auth |
| Marketplace | Signed catalog | Execute plugins |
| SDK | `ApiEnvelope` v1 | Ship a portal UI |
| Collaboration | Presence | CRDT or a second voice path |

## Data stores

| Store | Holds | Never holds |
| --- | --- | --- |
| `memory.db` | Consented learner profile | Scores, transcripts, OTPs |
| `analytics.db` | Anonymous call ops | Identity join to `User` |
| Knowledge JSON | Lesson tips | Speech |

Do not join `memory.db` to `analytics.db` by learner identity.

## Frozen rules

- One Voice Pipeline
- One SpecialistRouter
- One Search Platform
- One Automation Platform
- One event bus
- One RBAC (`can(role, permission)`)
- No utterance column

v1 freeze: [41 SALORA OS v1.0](../engineering/41_SALORA_OS_V1_RELEASE.md).
