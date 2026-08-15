# Backend

The worker is `backend/src/agent.py`. Services in `backend/src/services/` wrap that worker. They do not replace it.

Canonical spec: [23 Backend Platform](../engineering/23_BACKEND_PLATFORM.md).

## Shape

```text
API / CLI / Worker
        │
        ▼
  AI Orchestrator
        │
   Voice · Learning Engine · Adaptive Engine · Knowledge Fabric · Agents
        │
        ▼
  Repositories → memory.db / analytics.db / knowledge JSON
        │
        ▼
  Provider Registry → LiveKit / Murf / Deepgram / Gemini
```

`agent.py` still constructs the live Voice Pipeline.

## AI Orchestrator

`AIOrchestrator.run(intent)` records latency and fallback, then delegates. Adaptive Engine and Agent Runtime call **SpecialistRouter**. The orchestrator is not a second router.

## Provider Registry

Live adapters: LiveKit, Murf, Deepgram, Google. Other names may be registered disabled. Do not call providers outside adapters except the construction that already lives in `agent.py`.

## Production package

Python cannot use a package named `platform` (stdlib). Production helpers live in `salora_platform`: config, auth, RBAC, health, observability, security.

## Related

- [Voice Pipeline](voice-platform.md)
- [22 Production Platform](../engineering/22_PRODUCTION_PLATFORM.md)
- [05 Backend Constitution](../engineering/05_BACKEND_CONSTITUTION.md)
