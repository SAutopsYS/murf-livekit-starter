# SALORA OS — Implementation Foundation

Stage A.

The Master Constitution is the law.  
The Product Blueprint is what exists.  
The Design System is how it is experienced.  
The AI System is intelligence.  
The Platform Constitution is infrastructure principle.

This file is how SALORA is physically built.

Not a tutorial.  
Not boilerplate.  
Not a GitHub template.

The permanent Implementation Foundation Blueprint.  
Every engineer reads this before writing production code.

The living repo today is `backend/` (Python LiveKit worker), `frontend/` (Next.js), `docs/`, `scripts/`.  
This file is the target shape those trees migrate into.  
Migration does not mint a second voice pipeline. The worker remains the one path into the room.

If a folder, service, or dependency cannot name its owner, its data class, and the law it obeys, it does not enter the tree.

---

# Volume I — Foundation Philosophy

**Engineering as architecture**  
A line of code is a wall in the hall. We place walls on purpose. A clever shortcut that smuggles speech is a hole.

**Code serves learning**  
If the change does not make the next attempt cheaper, clearer, more honest, or more possible to run, it waits.

**Simplicity over cleverness**  
A boring module that fails toward the host beats a beautiful graph that drops the person.

**Explicit over implicit**  
Names are honest. `handoff` is not `reconnect`. `memory` is not `transcript`. Magic is a defect.

**Fail safely**  
Guest dies, host continues. Network dies, we tell the truth. A throw does not become a stack in the lesson.

**Modular by default**  
Apps consume packages. Packages do not import apps. Services do not reach across a neighbor’s table.

**Stable foundations**  
Frameworks are guests. The kernel (host, license, session, stop, fail-closed) does not move when a framework does.

**Long-term maintainability**  
A stranger in a decade must find the refuse. Readable code is respect.

**Developer experience**  
A developer can run the host path without a child’s data. Sandbox is synthetic.

**Production-first engineering**  
We do not design a demo that cannot forget, pin, or roll back. Production constraints are the default, not a later coat.

---

# Volume II — Repository Architecture

**Monorepo philosophy**  
One repository for the OS. Many deployables. One review law. One forbidden-column list.  
A second repo that speaks to a learner still obeys this file or it is not ours.

**Ownership**  
Every top-level path has a named function (Engineering Constitution). Vacancy is an incident for kernel paths.

**Applications (`apps/`)** — Deployable user surfaces: web, mobile, operator consoles.

**Packages (`packages/`)** — Shared libraries: tokens, contracts, SDK, eslint, tsconfig. No business side doors.

**Services (`services/`)** — Deployable backends: control plane, workers, voice runtime.

**Shared libraries** — Live in `packages/`. A service that copies a type instead of importing the contract will drift into an utterance field.

**Version strategy**  
The repo versions as a whole for apps that ship together. Packages that are public contracts semver. Production **pins** models, prompts, guests, content — “latest” is not a pin.

**Dependency rules**  
Apps → packages, services.  
Services → packages. Not to apps.  
Packages → packages only downward. No cycles.  
Voice runtime may call control-plane APIs. Control plane does not embed a second STT/TTS stack.

**Module isolation**  
A module names its data class. Learning does not import a speech buffer.

**Build strategy**  
Task runner at root. Affected builds. Voice worker builds in its own toolchain (Python). JS/TS in one toolchain. Mobile in Flutter’s. Infra as code in `infra/`.

---

# Volume III — Monorepo Structure

Target tree. Current `frontend/`, `backend/`, `docs/`, `scripts/` map into it; they are not a second OS.

```
apps/
  web/                 # Next.js — learner, teacher, parent, school, enterprise surfaces
  mobile/              # Flutter — Core attempt, stop, voice, back
  operator/            # optional — AI workspace / control center (no tapes)
packages/
  contracts/           # API types, error codes, event names — no utterance fields
  tokens/              # Design tokens (Design System Volume XIII)
  sdk/                 # typed client for control plane
  config/              # eslint, tsconfig, prettier, ruff shared
  testing/             # harnesses, fixtures (synthetic)
services/
  api/                 # NestJS control plane
  worker/              # queues, jobs, spacing — no speech summary into the graph
  voice/               # LiveKit Agents + Murf — THE one voice path
infra/
  terraform/
  k8s/
  docker/
configs/               # env schemas, not secrets
docs/
  salora/              # constitutions
scripts/               # generators, checks — do not vendor node_modules
tools/                 # codegen, lint wrappers
tests/                 # repo-level e2e and contracts
```

**Naming** — kebab-case directories. Honest service names. No `tmp`, no `misc`, no `new-api-2`.

**Ownership** — `CODEOWNERS` per path. `services/voice` and `services/api` identity/memory/forget are Sev-1 paths.

**Imports** — Public barrels only. No deep imports into another service’s internals. No `apps/web` import from `apps/mobile`.

**Visibility** — Packages export a public API. Internal folders are not a contract.

**Dependency direction**

```
apps → packages
apps → services (via HTTP/SDK only)
services → packages
services/voice → services/api (API only)
services/api ↛ voice internals
packages ↛ apps, services
infra ↛ application code
```

No folder exists without a purpose paragraph in this volume or an amendment.

**Migration note**  
Until the move: `frontend/` is `apps/web`. `backend/` is `services/voice` plus the seeds of `services/api`. Do not add a parallel Next token route that becomes a second identity. Do not add a NestJS WebSocket voice.

---

# Volume IV — Backend Foundation

Two runtimes. One kernel.

## Control plane — NestJS (`services/api`)

Owns identity, tenancy, learning state, licensed memory, content metadata, assessment records, credentials, projections, flags, guest registry.

**Domain-driven design** — Bounded contexts match Platform services: Identity, Learning, Memory, Assessment, Content, Teacher, Parent, Enterprise, Audit. A context does not own a neighbor’s table.

**Clean architecture** — Domain → application → infrastructure. The domain does not import Nest, Prisma, or a cloud SDK. Controllers are thin.

**CQRS** — Commands change state (assign, forget, score closed item). Queries read projections. A query does not mint memory. Eventual read models may exist; they honor forget.

**Modules** — One Nest module per bounded context. Public interface only.

**Services** — Application services orchestrate. Domain services hold rules (guest ≤ host ≤ consent).

**Controllers** — HTTP/GraphQL adapters. Authz on the server. No utterance DTO.

**Workers / queues / jobs** (`services/worker`) — Spacing, index, export, deletion aging. Idempotent. No job that “summarizes speech into the graph.”

**Events** — Event names from Data Constitution. No payload of speech.

**API gateway** — Edge auth, rate limit, tenancy. Not a place to log bodies.

**Scheduler** — Due revisions, backup aging, pin checks. Not a streak threat engine.

## Voice runtime — LiveKit Agents (`services/voice`)

The one pipeline: STT → host/guest → TTS (Murf).  
Handoff is named guest. Reconnect is the same room.  
It calls the control plane for license, state, and tools.  
It does not become a second user database.  
It does not grow a NestJS twin.

A third backend “for AI” is forbidden.

---

# Volume V — Frontend Foundation

**Next.js App Router** (`apps/web`) — The web OS. Not a brochure.

**Workspaces as route groups** — Learner, teacher, parent, school, enterprise, settings. Instruments never replace the attempt.

**Server Components** — Default for read of allowed projections. No speech in a server log.

**Client Components** — Voice controls, live session, command palette. Smallest island.

**Routing** — Deep links confirm before replacing a live attempt.

**Layouts** — One primary. Stop reachable. Tokens only.

**State** — Server state from the API layer. Session UI state local. No global store of utterances.

**API layer** — `packages/sdk` only. No ad-hoc `fetch` of secret-shaped fields.

**Design tokens** — `packages/tokens`. Magic numbers are drift.

**Accessibility** — Labels, focus, keyboard, contrast, reduced motion in the same PR.

**Offline** — Honest banner. Cached last lesson and licensed snapshot. No pretend guest.

Existing `frontend/` follows this law now. Folder move is later. Law is now.

---

# Volume VI — Mobile Foundation

**Flutter** (`apps/mobile`) — Core: attempt, stop, voice, back. Density yields. Enterprise density does not ship on a watch-sized lie.

**Folder structure** — `lib/features/<workspace>`, `lib/core` (tokens, sdk, offline), `lib/voice` (client of the one pipeline, not a second engine).

**Shared models** — `packages/contracts` generated or mirrored. No hand-grown utterance class.

**Offline-first** — Encrypted cache of last lesson and licensed snapshot. Sync idempotent. No duplicate attempt.

**Secure storage** — Tokens and cache keys. Not a diary.

**Background sync** — State and due, not mouths.

**Push** — Quiet. One fact. Not a second tutor. Marketing never.

**Native bridges** — Mic, audio session, Stop. Camera never required. No silent capture.

A React Native fork is not a second OS. If it appears, it is a variant, not a new kernel.

---

# Volume VII — Database Foundation

| Store | Holds | Must not |
|---|---|---|
| **PostgreSQL** | Identity, tenancy, learning state, memory fields, assessment outcomes, credentials, audit, consent receipts | Utterance text, recordings |
| **Redis** | Live session flags, rate limits, idempotency, short cache | Profiles, speech, “tmp” biographies |
| **Neo4j** | Knowledge and learning graphs (typed edges) | Learner mouths, secret diaries |
| **Object storage** | Licensed content media, exports they asked for | Ambient home capture, lesson tapes by default |
| **Search** | Index of allowed taxonomy objects | Transcript search |

**Cache strategy** — Redis is a cache and a lock, not a source of truth for memory. Cache dies with permission.

**Transactions** — Forget and score writes are transactional in Postgres. Graph updates that `supersede` are versioned.

**Backups** — Encrypted. Restore identity, license, learning, content. Do not restore a lake we refused.

**Migrations** — Expand/contract. A migration that adds `transcript` is rejected in review.

**Data isolation** — Tenancy in every learner-shaped row. Research plane separate.

---

# Volume VIII — Infrastructure Foundation

Obeys Platform & Infrastructure Constitution. Here the tools:

**Docker** — One image per deployable. Voice image separate. No secrets in layers.

**Kubernetes** — Host/voice fleet preempts guest jobs. Tenancy isolation. Public buckets forbidden.

**Terraform** — Reproducible. Reviewed. State protected.

**Networking** — Least path. Voice path documented. No quiet mirror of lessons.

**Secrets** — Manager, rotation, not in git, not in `configs/`.

**Environments** — `dev`, `staging`, `prod`, `sandbox`, `research`. No real child roster outside prod/staging-with-contract.

**Load balancing** — Sticky only if the live attempt requires it; takeover still one session.

**Service discovery** — Internal. Clients use the gateway.

**CDN** — Content twins, never a private memory edit.

**IaC** — The only way prod changes. A console click that opens a bucket is an incident.

---

# Volume IX — Identity Foundation

**Authentication** — Control plane issues and validates. School SSO where contracted. Auth session ≠ lesson session.

**Authorization** — Server RBAC. UI is not the control.

**RBAC** — `learner`, `parent`, `teacher`, `school_admin`, `enterprise_admin`, `researcher`, `operator`. Guest agent is not a human role.

**Organizations / schools / enterprises** — Tenancies. Policy and roster. Not a speech toy.

**Teachers / students / parents** — Typed edges (`teaches`, `cares-for`, `enrolls`). Projections only.

**Sessions** — Auth session and lesson visit are different objects. Ending auth ends capabilities.

**Devices** — New device asks to take over. Not a new authority over memory.

No shared child logins as a workaround.  
No face as identity to learn.

---

# Volume X — Engineering Standards

Complements Engineering Constitution. Concrete rules:

**Naming** — Honest. Files match exports. No `utils2`.

**Folder rules** — Volume III. New top-level needs amendment.

**Imports** — Dependency direction. Lint-enforced.

**Dependency rules** — New dep has an owner and a reason. No surprise model in the client.

**Module boundaries** — Lint or generate boundaries (e.g. module rules). Learning cannot import voice buffers.

**Code reviews** — Engineering Volume IX questions. “We’ll add tests later” on kernel is refuse.

**Documentation** — How to run, fail, forget, add a guest. In repo.

**Comments** — Why, not what. No commented-out graves.

**Error handling** — Structured. Speakable at the edge. No stack in the lesson.

**Logging** — Event names, route ids. No prompt body, utterance, phone, OTP, secret.

Python in `services/voice`: ruff, 88 columns, as today.  
TS in apps/packages/api: eslint + the shared `packages/config`.  
Dart: analyzer + the same privacy log law.

---

# Volume XI — API Foundation

**REST** — Default for control plane. Smallest payload. Version in path or header. No utterance fields.

**GraphQL** — Optional for dense teacher/enterprise reads. Same authz. Same forbidden fields. No open introspection in prod.

**Events** — Names from Data Constitution. At-least-once + idempotency keys.

**WebSockets** — Not a second voice path. Allowed for presence and live instruments. Lesson audio stays on the LiveKit path.

**Pagination / filtering** — Cursor for lists. Filters are taxonomy, not “full text of what they said.”

**Versioning** — Breaking changes version. The person is not a breaking change.

**Error contracts** — `{ code, message, retryable }` safe message. No stack.

**API documentation** — Generated from contracts. Examples synthetic.

**SDK generation** — `packages/sdk` from `packages/contracts`. Mobile and web consume it.

Token endpoint and enterprise CLIs that exist today must move behind this contract, not grow a side door.

---

# Volume XII — Testing Foundation

Every module is testable without a child.

**Unit** — Domain rules: forget, guest ≤ host, reconnect ≠ handoff.

**Integration** — API + Postgres + Redis. No prod data.

**End-to-end** — Web Core path: start, stop, resume without new hello (staged). Voice e2e in sandbox.

**Contract** — OpenAPI/GraphQL and event schemas. Forbidden-field tests.

**Load** — School-day shape. Synthetic.

**Performance** — p95 first useful audio is a product number. Budgets on cheap phone.

**Accessibility** — Keyboard and label checks in CI for new controls.

**AI** — Eval gates for seats. Live listen still required for voice host swap.

**Security** — Authz bypass, secret scan, no utterance column in migrations.

A red privacy test does not merge.

Existing backend tests (fail-closed, handback, privacy logs) remain the pattern. They move with `services/voice`; they are not deleted for a green Nest folder.

---

# Volume XIII — Deployment Foundation

**Development** — Local host path. Synthetic data. `.env` not committed.

**Staging** — Pins. Contract testers. No surprise child roster.

**Production** — Pinned model, prompt, guest, content, client.

**CI/CD** — Lint, types, unit, contract, privacy, build. Voice worker and API are separate pipelines that share contract tests.

**Rollback** — First-class. Skipped review rolls back.

**Blue/green or canary** — Allowed for API and web. Voice canary cannot split one live session into two tutors.

**Feature flags** — Real for risk. Safety and forget not optional in prod.

**Release approval** — Governance Volume IV for kernel. Engineering release law for the rest.

---

# Volume XIV — Observability Foundation

**Structured logging** — JSON events. No content of speech.

**Metrics** — Host start, fail-closed, first useful audio, forget completion, guest retry, saturation.

**Distributed tracing** — Route, seat, tool name, latency. No prompt body.

**Dashboards** — Operators and enterprise. No child as a row of speech.

**Alerts** — Host down, leak class, forget fail, region fail. Not engagement.

**Error monitoring** — Stacks in operator space, never in the lesson.

**Health checks** — Can the host start? Can forget complete? Can a guest fail closed?

**SLA / SLO** — Host SLO is the SLO.

**Incident response** — Sev-1 law. Commander named. No growth first.

---

# Volume XV — Foundation Manifesto

Architecture is an educational responsibility.

A child may speak into what we build. That makes a folder an ethical object. A queue is an ethical object. A column is an ethical object. We do not get to call them “just infra.”

Foundations outlive frameworks. Nest, Next, Flutter, Postgres, Neo4j, Kubernetes — these are today’s guests. The kernel is older than they are and will be younger than their replacements: one host, one license, one voice path, forget that completes, tests that refuse a tape.

Readable code is a form of respect — for the next engineer, for the teacher who will debug a class at night, for the person whose name sits in a row. Cleverness that needs a priest is contempt.

Maintainability is a product feature. A hall we cannot change without restarting people is already broken. A monorepo we cannot explain is a second curriculum of confusion.

Engineering must protect learners before optimizing systems. A faster leak is not an optimization. A cheaper lake is not an optimization. A prettier dashboard of mouths is not an optimization.

What must never change, even when languages, clouds, and repos rename:

One monorepo law.  
One voice path.  
No utterance column.  
Dependency arrows that do not cycle into a tape.  
Pins in production.  
Tests for forget and fail-closed in the same change.  
A developer path that does not need a child.  
A restore that does not resurrect a sin.

The current tree may still say `frontend/` and `backend/`.  
The law already says `apps/web` and `services/voice`.

Build toward the tree.  
Do not build a second hall beside it.

Stay on the line.  
Lay the floor.  
Then write the room.
