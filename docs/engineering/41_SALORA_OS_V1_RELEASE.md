# 41 — SALORA OS v1.0 Release

Architecture freeze. No new product surface. Validate Phases 1–40.

---

## Final architecture

```
Clients (Web / Mobile spec / Desktop spec)
        │
   SDK envelopes v1 + Gateway policy
        │
   Universal Search ── Automation (one engine)
        │
   Studio / Whiteboard / Fabric / Learning / Adaptive
        │
   Agent Runtime ──► SpecialistRouter (authority)
        │
   Marketplace catalog (no exec) · Org tenants · Collaboration presence
        │
   salora_platform (auth, RBAC, config, observe, health)
        │
   LiveKit worker + Murf + Deepgram + Gemini
```

One voice path. One router. One event bus. One RBAC. One config parse. One search. One automation.

---

## System overview

| Layer | Source of truth |
|---|---|
| Voice | LiveKit + Murf (`agent.py`) |
| Learning / Adaptive / Fabric | Frontend engines + backend facades |
| Memory | `memory.db` consented profile only |
| Analytics | `analytics.db` anonymous |
| Knowledge lessons | JSON `knowledge.search` |
| AuthZ | `can(role, permission)` |
| Extensions | Marketplace manifests, `may_execute=false` |
| Agents | Specialist registry + runtime host |

---

## Deployment

`start_app.*` for dev. `docker compose up --build` for shaped prod. CI: `.github/workflows/ci.yml`. Health: `/api/health`, `/api/ready`, `python -m salora_platform.health`.

---

## Operations

Structured logs. Service metrics. No utterance in traces. Rollback = image + env.

---

## Security / governance

Anonymous voice first-class. `AUTH_REQUIRED` default false. Privacy rules forbid speech columns. HIPAA not claimed.

---

## Enterprise readiness

Control Center lives. Org/tenant models exist. Billing is a spec. Identity issuance still waits on a roster.

---

## Scaling

Frontend replicas. LiveKit worker scale. SQLite until a single writer saturates — same schema laws. Redis when rate-limit needs multi-instance.

---

## Future roadmap (consume, do not rewrite)

1. Identity + `AUTH_REQUIRED=true`
2. Studio editor / Whiteboard renderer / Graph view as instruments
3. Queue behind `JOB_CATALOG`
4. OTel exporter
5. Signed plugin crypto
6. Mobile/desktop implementations of these contracts

---

## Version

**SALORA OS v1.0.0-rc** — architecture frozen. Semver: breaking contract = v2 envelope, not a kernel fork.
