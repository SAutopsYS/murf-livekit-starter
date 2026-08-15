# 22 — Production Platform

Permanent operational foundation for **SALORA OS**.  
This is infrastructure. It does not replace LiveKit, Murf, the Workspace Shell, Voice, Learning, Analytics, Enterprise, or Knowledge Fabric.

Law: [13 Security Standard](13_SECURITY_STANDARD.md), [11 Testing Standard](11_TESTING_STANDARD.md), [12 Performance Standard](12_PERFORMANCE_STANDARD.md), Master laws V–VII, X.

---

## Production architecture

```
                    ┌─────────────────────────────┐
   Browser          │  Next.js  (frontend)        │
   / hall           │  OsShell · Voice · Instruments│
   /analytics       │  /api/token  /api/health     │
   /enterprise      │  /api/analytics /enterprise  │
                    └─────────────┬───────────────┘
                                  │ execFile CLI + LiveKit JWT
                    ┌─────────────▼───────────────┐
   Worker           │  LiveKit Agent (backend)    │
                    │  agent.py · Murf · Deepgram │
                    │  Gemini · specialists       │
                    │  memory.db · analytics.db   │
                    └─────────────┬───────────────┘
                                  │
                         LiveKit Cloud / SIP
```

Platform modules sit **beside** the product, not on top of the voice path:

| Layer | Frontend | Backend |
|---|---|---|
| Config | `lib/platform/config.ts` | `salora_platform/config.py` |
| Auth / RBAC | `lib/platform/auth.ts` + `rbac.ts` | `salora_platform/auth.py` |
| Observability | `lib/platform/observability.ts` | `salora_platform/observability.py` |
| Errors | `lib/platform/errors.ts` | `salora_platform/errors.py` |
| Security | `lib/platform/security.ts` | `salora_platform/security.py` |
| Health | `/api/health` `/api/ready` | `python -m salora_platform.health` |

Python cannot own a package named `platform` (stdlib). The worker package is `salora_platform`.

Telephony feature flags stay in `telephony/features.py`. Branding stays in `app-config.ts`. Token minting stays LiveKit `AccessToken`.

---

## Deployment flow

1. Clone. Copy `backend/.env.example` → `backend/.env.local` and `frontend/.env.example` → `frontend/.env.local`.
2. Local: `start_app.ps1` / `start_app.sh` (unchanged).
3. Verify: `scripts/ci.ps1` or `scripts/ci.sh`.
4. Containers: `docker compose up --build`. Frontend `:3000`. Backend is the LiveKit worker (no public HTTP). SQLite lives on volume `salora-data` → `/app/data`.
5. Promote: set `SALORA_PROFILE=staging` then `production`. Flip `AUTH_REQUIRED=true` only after identity is issued.
6. Health: frontend `GET /api/health` (liveness), `GET /api/ready` (LiveKit env present). Worker `python -m salora_platform.health` and `--ready`.
7. Rollback: previous image tag + previous env. Compose `restart: unless-stopped`. Zero-downtime: run two frontend replicas behind a load balancer; drain; LiveKit rooms are sticky to the worker that accepted the job — scale workers horizontally, do not interrupt an in-flight room.

`start_app.*` remains the developer path. Compose is the production-shaped path. Do not invent a third orchestrator.

---

## Authentication

Supported now:

- **Anonymous voice** — `/api/token` stays public (rate-limited, same-origin). Guest identity is a random LiveKit participant. This is a product path, not a hole.
- **JWT access** — HS256 via `jose` (already a dependency). Default 15 minutes.
- **Refresh** — longer-lived refresh JWT. Same secret. `typ=refresh`.
- **Cookie session** — `salora_session` cookie name. Same access token.
- **Roles on the session** — `anonymous | guest | student | parent | teacher | enterprise_admin | developer | operator`.
- **Organizations** — `OrganizationRef` on the session. Empty until a tenant store exists.

`AUTH_REQUIRED` defaults **false**. Instruments stay open for the current demo. When true, analytics/enterprise/learning routes require a role that `can()` the permission.

No login UI in this phase.

Future providers (typed, not implemented): SSO, OAuth, passkeys. They must mint the same `PlatformSession`. Do not add a second auth stack.

---

## Authorization

One matrix. `can(role, permission)`. Routes call `authorizeRequest` / `platformRoute`. The enterprise Control Center role select (`admin|teacher|parent`) maps through `roleFromEnterpriseUi`. UI is not authority.

Permissions:

- `voice.session`
- `analytics.read` / `analytics.export`
- `enterprise.read` / `enterprise.export` / `enterprise.admin`
- `learning.read`
- `developer.sdk`
- `marketplace.browse` / `studio.access` (gated off)

Feature flags (`FEATURE_*`) turn surfaces off without deleting routes.

---

## Configuration

`SALORA_PROFILE=development|staging|production`.

One parse per process. Existing names reused: `LIVEKIT_*`, `MURF_API_KEY`, `DEEPGRAM_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`, `AGENT_NAME`.

New optional names (placeholders in `.env.example` only):

- `AUTH_REQUIRED`, `SALORA_AUTH_SECRET`, `AUTH_ACCESS_TTL_SECONDS`, `AUTH_REFRESH_TTL_SECONDS`
- `ALLOWED_ORIGINS`, `RATE_LIMIT_TOKEN_PER_MIN`, `RATE_LIMIT_API_PER_MIN`
- `FEATURE_ANALYTICS`, `FEATURE_ENTERPRISE`, `FEATURE_LEARNING`, `FEATURE_STUDIO`, `FEATURE_MARKETPLACE`, `FEATURE_DEVELOPERS`

Do not parse the same env in a third module. Telephony keeps its own cached loader.

---

## Observability

Structured JSON logs. Forbidden keys: transcript, utterance, OTP, phone, secret, password, token, API key, prompt.

Metrics names for future dashboards:

- `voice.session.start` / `voice.session.end`
- `voice.latency.connect_ms` / `voice.latency.first_audio_ms`
- `api.request` / `api.latency_ms` / `api.error`
- `learning.projection` / `adaptive.decision` / `knowledge.retrieval`
- `agent.handoff` / `agent.handback`
- `heartbeat`

Existing in-process collectors stay: `tools/metrics.py`, `telephony/metrics.py`, `specialists/metrics.py`. New code records through the platform helpers. Do not start a second metrics database.

Traces are in-process spans (`startSpan` / `endSpan`). OpenTelemetry can wrap these later without a rewrite.

---

## Performance

Unchanged voice path. Hall route must not gain new heavy libraries.

This phase:

- `next.config` `compress`, `standalone` output, `optimizePackageImports` for Phosphor
- AVIF/WebP image formats
- App Router already splits `/`, `/analytics`, `/enterprise`
- `PlatformErrorBoundary` is a class boundary, not a new visual system
- In-memory rate limit and metric ring are process-local

Voice latency budget in [12](12_PERFORMANCE_STANDARD.md) still wins.

---

## Security

- Security headers on every Next path. Microphone stays `self` (voice). Camera off by default.
- HSTS only when `SALORA_PROFILE=production`.
- CSRF: POST `/api/token` requires same-origin or `ALLOWED_ORIGINS`.
- Rate limits: token and API buckets (in-memory; Redis later for multi-instance).
- Query validation on analytics/enterprise filters.
- Audit events: `audit.api.access` with role, never speech.
- Privacy rules match memory/analytics law: no utterance column, consent before long-term, Forget Me must complete.
- Secrets never in git. `.env.example` placeholders only.

`useAgentErrors` remains the LiveKit session failure surface.

---

## Testing

| Kind | Where |
|---|---|
| Backend unit / integration | `backend/tests` (existing + `test_platform.py`) |
| Frontend unit | `frontend/lib/**/*.test.ts` via Vitest |
| Learning / adaptive / fabric | engine tests — projections only |
| Voice | existing pytest + manual hall (no committed learner audio) |
| LLM-as-judge | `tests/test_agent.py` — **not** in default CI (needs provider secrets) |
| E2E / a11y / perf | architecture in [11](11_TESTING_STANDARD.md); Playwright later, do not mock a second LiveKit |

Local: `scripts/ci.ps1`. Coverage: kernel packages aim ≥ 80%. Do not log speech for assertions.

---

## CI/CD

Root workflow: `.github/workflows/ci.yml`

- Backend: `ruff` + `pytest --ignore=tests/test_agent.py`
- Frontend: `tsc --noEmit`, lint, Vitest, production build
- Privacy: refuse `utterance`/`transcript` SQL columns in memory/analytics stores

Nested starter workflows (`frontend/.github`, `backend/.github`) remain. The monorepo gate is the root file.

Promotion: main is production-shaped. Staging is env, not a fork. Rollback is image + env, not a schema rewrite.

---

## Disaster recovery

| Asset | Rule |
|---|---|
| `memory.db` | Consented profile only. Back up encrypted. Forget Me must still apply after restore. |
| `analytics.db` | Anonymous ops. No join to `User`. |
| LiveKit / Murf / Deepgram / Gemini | Provider outage → fail closed to the host. No second mouth. |
| Auth secret rotation | Issue new `SALORA_AUTH_SECRET`. Old JWTs die at TTL. Voice anonymous still works. |
| Region loss | Redeploy compose/K8s in the next region. Rooms do not migrate mid-sentence. |

Do not invent a speech lake as a “backup.”

---

## Scaling strategy

- **Frontend:** stateless Next replicas. Rate-limit store becomes Redis when replica count > 1.
- **Worker:** LiveKit Agents horizontal scale. One job, one worker. Prewarm VAD as today.
- **SQLite:** process-local. Move analytics/memory to managed SQL when a single writer saturates — same schema laws.
- **Voice:** scale rooms, not a second pipeline.
- **Enterprise / Learning / Fabric:** projections. They scale with the APIs they read.

---

## Future enterprise deployment

Plug in without a rewrite:

- Multi-tenant `OrganizationRef` on the session
- SSO / OAuth / passkeys as `AuthProviderKind`
- Marketplace / Studio feature gates
- Developer SDK behind `developer.sdk`
- Compliance dashboards consume metric names above
- Global deploy: same images, different `SALORA_PROFILE` + secrets

If a feature needs a new auth system, a new voice stack, or a transcript column, it is refused.
