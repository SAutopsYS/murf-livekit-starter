# Architecture diagrams

Mermaid maps of what this repository actually runs. Facades that are **not** on the live audio path are drawn with dashed edges.

Source of truth for the voice hop: `backend/src/agent.py` (`my_agent`). Overview prose: [overview.md](overview.md).

**Implemented** — hall, worker, or instrument you can open.  
**Architected** — module exists; not inserted into `AgentSession`.  
**Planned** — written in [41 SALORA OS v1](../engineering/41_SALORA_OS_V1_RELEASE.md); not running here (Redis, Kafka, OTel, Playwright e2e).

---

## Overall architecture

Browser and worker meet in LiveKit Cloud. Next.js mints a token and serves instruments. It does not carry microphone audio after join.

```mermaid
flowchart TB
  subgraph browser [Browser]
    Hall["/ hall LiveKit client"]
    Analytics["/analytics"]
    Enterprise["/enterprise"]
    Shell["Workspace Shell"]
  end

  subgraph next [Next.js]
    Token["POST /api/token"]
    Health["/api/health /ready"]
    Instr["analytics / enterprise routes"]
  end

  LK[LiveKit Cloud]

  subgraph worker [Python worker]
    Agent["agent.py AgentSession"]
    Tools["AGENT_TOOLS"]
    Router["SpecialistRouter"]
  end

  subgraph data [Data]
    Mem["memory.db consented profile"]
    Anon["analytics.db anonymous ops"]
    JSON["knowledge JSON"]
  end

  subgraph facades [Facades - not in audio path]
    Orch["AIOrchestrator"]
    Search["SearchService"]
    Auto["AutomationService"]
  end

  Hall --> Token
  Token --> Hall
  Hall <--> LK
  Agent <--> LK
  Agent --> Tools
  Agent --> Router
  Tools --> Mem
  Tools --> JSON
  Agent --> Anon
  Analytics --> Instr
  Enterprise --> Instr
  Instr --> Anon
  Orch -.-> Agent
  Search -.-> JSON
  Auto -.-> Orch
```

---

## Voice Pipeline

This is the only path that produces sound. No orchestrator, Learning Engine, Search Platform, or Fabric hop.

```mermaid
flowchart LR
  Mic[User speech] --> LK[LiveKit room]
  LK --> STT["Deepgram nova-3 language=multi"]
  STT --> LLM["Gemini 3.5 Flash Lite"]
  LLM -->|optional| Tools[Function tools]
  Tools --> LLM
  LLM --> TTS["Murf Falcon Anisha"]
  TTS --> LK
  LK --> Spk[User hears]
```

Session knobs in `agent.py`: `max_output_tokens=120`, `thinking_level=minimal`, `text_pacing=False`, endpointing 0.3–1.5s, `preemptive_generation=True`. Silero VAD is prewarmed. There is no custom barge-in API.

---

## Agent flow

Dispatch name is `my-agent`. Math is the only live guest. Other specialists register disabled. One retry, then host.

```mermaid
flowchart TD
  Pre[prewarm Silero VAD] --> Job["rtc_session my-agent"]
  Job --> Enter[on_enter]
  Enter --> Look[SessionMemoryLookup background]
  Enter --> Greet[Spoken greeting]
  Greet --> Turn[User speech]
  Turn --> STT[Deepgram]
  STT --> Gemini[Gemini + AGENT_TOOLS]
  Gemini --> Speak[Murf]
  Speak --> Turn
  Gemini -->|math intent| R{SpecialistRouter}
  R -->|MAIN or clarify| Gemini
  R -->|MATH| Handoff[handoff_to_math_specialist]
  Handoff --> Retry[start_specialist_with_retry]
  Retry -->|ok| Math[Math guest same room]
  Retry -->|fail after 1| Host[Assistant host]
  Math --> Back[handback]
  Back --> Host
  Turn --> Exit[on_exit + analytics complete]
```

---

## Knowledge flow

Hall retrieval is the JSON tool. Fabric and Memory Graph project the same search. They must not write `memory.db`.

```mermaid
flowchart LR
  JSON[english_basics.json] --> KS[knowledge.search]
  KS --> Tool[search_learning_knowledge]
  KS --> Fabric[Knowledge Fabric projection]
  Fabric --> Graph["Memory Graph - no memory.db writes"]
  KS --> Search[SearchService facade]
  MDB[(memory.db consent)] --> Learn[Learning snapshot]
  ADB[(analytics.db anonymous)] --> Learn
```

Do not join `memory.db` to `analytics.db` by learner identity.

---

## Search flow

Architected. One `SearchHit` contract. No vector database in Compose. Learners do not get a search box on `/`.

```mermaid
flowchart TD
  Q[SearchService.search] --> K[knowledge.search]
  Q --> P[marketplace catalog]
  Q --> A[agent runtime list]
  K --> Rank[RankingService]
  P --> Rank
  A --> Rank
  Rank --> Hits[SearchHit list]
```

`DiscoveryService` is an alias of the same class. Evidence: `backend/src/services/search.py`, `backend/tests/test_os_v1.py`.

---

## Automation flow

Architected. One engine. `WorkflowAutomationService` is the same class. Jobs are a catalog, not Kafka.

```mermaid
flowchart LR
  C[AutomationService.create] --> E[execute]
  E --> St[Studio workflow stub]
  E --> Ev[WorkflowCreated / Completed]
  J[JOB_CATALOG] -.->|no broker| E
```

Evidence: `backend/src/services/automation.py`. `may_execute` on marketplace plugins stays false.

---

## Event bus

In-process. History cap 200. No disk, no retry, no broker. Forbidden keys and long forbidden values are dropped.

```mermaid
flowchart LR
  P["publish(name, fields)"] --> C[_clean_fields]
  C --> H[history cap 200]
  H --> N[handlers for name]
  H --> S[handlers for star]
  P -->|unknown name| W[emit event.unknown]
```

Specialist logging is a separate allow-list logger that drops extra kwargs. It is not a second bus. Evidence: `backend/src/services/events.py`.

---

## Authentication

`AUTH_REQUIRED` defaults **false** so anonymous voice works. Token mint is CSRF-checked and rate-limited. It does not require a logged-in roster.

```mermaid
flowchart TD
  Req[HTTP request] --> CSRF{csrf and same origin?}
  CSRF -->|fail| F403[403]
  CSRF --> RL{rate limit}
  RL -->|fail| F429[429]
  RL --> Auth{AUTH_REQUIRED?}
  Auth -->|false| H[handler]
  Auth -->|true| JWT{valid session?}
  JWT -->|no| F401[401]
  JWT --> Can
  Can{can role permission}
  Can -->|no| F403b[403]
  Can --> H
  Voice[POST /api/token] --> CSRF
```

Flip `AUTH_REQUIRED=true` only after identity exists. Documented in [41](../engineering/41_SALORA_OS_V1_RELEASE.md).

---

## RBAC

One function: `can(role, permission)`. Python (`salora_platform.auth`) and TypeScript (`lib/platform/rbac.ts`) share the idea. UI selects are not authority.

```mermaid
flowchart LR
  Role[role] --> Can["can(role, permission)"]
  Perm[permission] --> Can
  Can -->|true| Allow[handler]
  Can -->|false| Deny[403]
```

---

## Enterprise isolation

`/enterprise` reads operational aggregates. Tenant records in the later layer are in-memory. Speech columns are forbidden. Profile store and ops store stay unjoined.

```mermaid
flowchart TB
  Hall[Hall voice session] --> LK[LiveKit]
  LK --> Worker[agent.py]
  Worker --> Mem[(memory.db)]
  Worker --> Anon[(analytics.db)]
  Ent["/enterprise"] --> API[Next enterprise routes]
  API --> Anon
  Ent -.->|must not join by identity| Mem
  Tenants[In-memory org records] -.-> Ent
```

HIPAA checks return `ok: False`. That is a lock, not a missing claim.

---

## Repository structure

```mermaid
flowchart TB
  Root[SALORA OS]
  Root --> BE[backend]
  Root --> FE[frontend]
  Root --> Docs[docs]
  Root --> Compose[docker-compose.yml]
  Root --> Start[start_app.ps1 / start_app.sh]
  BE --> Agent[src/agent.py]
  BE --> Mem[src/memory]
  BE --> Know[src/knowledge]
  BE --> Spec[src/specialists]
  BE --> Svc[src/services facades]
  BE --> Plat[src/salora_platform]
  BE --> Tests[tests]
  FE --> App["app / /analytics /enterprise"]
  FE --> OS[components/os]
  FE --> Lib[lib engines]
  Docs --> Arch[architecture]
  Docs --> Guides[guides]
  Docs --> Eng[engineering archive]
  Docs --> Salora[salora constitutions]
```
