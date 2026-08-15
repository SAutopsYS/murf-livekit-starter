# 31 — Agent Runtime Platform

Hosts every current and future agent. **Does not route.**

`SpecialistRouter` remains authority. `AIOrchestrator` remains provider choice. This runtime is the catalog + lifecycle + sandbox around them.

---

## Runtime architecture

```
AgentRuntimeService
    │
    ├─ registry  → specialists.registry + host tutor
    ├─ execution → AgentService.recommend() → router
    ├─ catalog   → Marketplace packages with capability "agents"
    └─ sandbox   → no autonomous loops
```

---

## Agent model

Kinds: tutor, math, coding, career, interview, language, writing, research, planning, creative, enterprise, custom.

Host is always `agent.tutor`, live. Math guest projects `math_practice_specialist`. Placeholders from the specialist registry appear as disabled.

---

## Capabilities

voice, learning, adaptive, knowledge, studio, whiteboard, memory_graph, workflow, plugin, analytics, enterprise.

Access through contracts. No direct `memory.db` from a guest.

---

## Lifecycle

registered → loaded → started → busy / waiting → completed | failed | suspended | disabled.

Events on the platform bus. Specialist allow-list logger still owns handoff names.

---

## Marketplace integration

`AgentCatalogService` filters marketplace packages with `agents` capability. Discover/install/enable are marketplace events. No visual store.

---

## Policies

Provider selection, quotas, cost, org policy, one retry, timeout, fail-closed. Numbers come from the orchestrator, not a new loop.

`may_autonomous_loop()` is **false**.

---

## Security

RBAC + capability isolation + plugin sandbox + org id + signed manifests. Same as Marketplace + Enterprise Cloud.

---

## Future

Autonomous agents, if ever allowed, must flip the sandbox flag **and** keep one mouth. A background loop that speaks is a defect.
