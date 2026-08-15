# 23 — Backend Platform

Permanent AI service layer behind **SALORA OS**.  
Wraps the LiveKit worker. Does not replace it.

Law: [05 Backend Constitution](05_BACKEND_CONSTITUTION.md), [06 AI Architecture Bible](06_AI_ARCHITECTURE_BIBLE.md), [22 Production Platform](22_PRODUCTION_PLATFORM.md).

---

## Service architecture

```
API / CLI / Worker
        │
        ▼
  AIOrchestrator
        │
   ┌────┼────┬──────────┬──────────┐
   ▼    ▼    ▼          ▼          ▼
 Voice Learn Adaptive Knowledge Agents
        │
        ▼
   Repositories  →  existing SQLite / JSON
        │
        ▼
   ProviderRegistry → LiveKit / Murf / Deepgram / Gemini
```

Package: `backend/src/services/`.

Business logic does not grow in Next routes. Workers call services. Services call adapters. Adapters describe providers. `agent.py` still constructs the live pipeline.

---

## Provider architecture

`ProviderRegistry` lists live adapters (`livekit`, `murf`, `deepgram`, `google`, `openai`) from existing env names.

Future names are registered **disabled**: Claude, Groq, DeepSeek, Llama, Azure OpenAI, Bedrock, Vertex.

No provider-specific calls outside adapters. Murf/LiveKit construction stays in `agent.py`.

---

## Orchestration

`AIOrchestrator.run(intent)` chooses a provider capability, records latency/retries/fallback, and delegates to Voice / Learning / Adaptive / Knowledge / Agent services.

It does **not** replace `SpecialistRouter`. Adaptive and Agent services call the router.

---

## Repositories

Ports wrap existing modules:

- `MemoryRepositoryAdapter` → `memory.repository`
- `AnalyticsRepositoryAdapter` → `analytics.repository`
- `KnowledgeRepositoryAdapter` → `knowledge.repository`
- `InMemoryDocumentStore` → Studio / Whiteboard until a table exists

No SQL in services. SQLite today. Postgres later. Same ports.

---

## API contracts

`services.api`: `ApiEnvelope`, `CursorPage`, `ApiError`, `API_VERSION=v1`.

Existing `/api/analytics` and `/api/enterprise` stay. Future SDK uses envelopes. Do not redesign those routes in this phase.

---

## Events

In-process bus: `publish` / `subscribe`. Privacy-safe (no utterance keys).

Session, learning, knowledge, agent, provider, studio, whiteboard, and graph names live in one catalog.

Specialist events stay in `specialists.events` (allow-list). Platform bus is additive.

---

## Background jobs

`JOB_CATALOG` only. Kinds: reports, embeddings, memory consolidation, analytics rollup, notifications, enterprise export, recommendation refresh, whiteboard/graph index.

No Redis. No Celery. Specs so a queue can plug in later.

---

## Observability

Every service records `ServiceMetrics`: latency, failures, provider, token usage, cost, cache hit, retries.

Consumed later by Grafana / OpenTelemetry. Extends [22](22_PRODUCTION_PLATFORM.md).

---

## Scaling strategy

- Worker scale = LiveKit jobs (unchanged)
- Services are process-local facades
- Document store becomes SQL through the same port
- Provider pool is the registry, not a second client

Voice latency must stay the LiveKit path. Orchestrator never sits on the audio wire.

---

## Future providers

Add a `ProviderAdapter(live=True)` when keys exist. Do not fork `agent.py` per vendor.
