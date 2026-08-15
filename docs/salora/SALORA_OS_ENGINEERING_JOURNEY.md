# SALORA OS — Engineering journey

Challenges, decisions, and lessons. Only what the repo, git, tests, and docs support.

Git on `origin/main` is Days 1–9. The OS facades, shell, and docs 01–51 are largely local. I will not pretend this was a multi-year product calendar. It is a ten-day challenge kernel plus a platform layer grown on top of it.

There are no `TODO` / `FIXME` markers in `backend/src`. Planned work lives in `41_SALORA_OS_V1_RELEASE.md` and the constitutions.

---

## 1. Engineering journey

I started from the Murf LiveKit starter. Day 1 was “does it talk.” Day 2 was “is it a tutor.” Day 3 was “can a person use the hall.” After that, every day added a capability without opening a second mouth.

| Recorded milestone | What landed | Evidence |
| --- | --- | --- |
| Starter / Day 1 | LiveKit worker + Murf | `git log`: Day 1 commits |
| Day 2 | Tutor prompt, greeting, Hinglish, guardrails | `SYSTEM_PROMPT`; Day 2 commits |
| Day 3 | Session screens, wave, suggestions | `welcome-view.tsx`; Day 3 commits |
| Day 4 | Consented SQLite, Forget Me, knowledge tool | `memory/`, `knowledge/` |
| Day 5 | Exercises, deterministic score, failover | `tools/`, Day 5 tests |
| Day 6 | Outbound telephony as a **separate** path | `telephony/`; browser pipeline unchanged |
| Day 7 | Human-help after consent | `escalation/` |
| Day 8 | `analytics.db`, `/analytics` | `analytics/`; privacy tests |
| Day 9 | SpecialistRouter, Math guest, `/enterprise` | `specialists/`, `enterprise/` |
| Local after 9 | Shell, `salora_platform`, service facades, docs | working tree; `IMPLEMENTATION.md` |
| Stabilization | Event-value redact, DB init logs, compose volume, ruff/prettier | `services/events.py`, `agent.py`, `docker-compose.yml` |
| Docs cleanup | Public `docs/` tree; Day 10 briefs | `docs/README.md` |

The rule that survived every day is in the Product Bible: reuse the working system; do not rewrite the kernel.

---

## 2. Major challenges

### Spoken latency

**What.** Gemini 3.x wanted to “think” after tools. Murf pacing delayed short tutor lines. Turns felt late.

**Why.** Voice dies if the model narrates thinking. Falcon pacing helps long prose; this tutor answers in one breath.

**Considered.** A realtime model is commented in `agent.py` and not enabled. A second TTS was never acceptable.

**Chosen.** `thinking_level=minimal`, `max_output_tokens=120`, `text_pacing=False`, endpointing 0.3–1.5s, `preemptive_generation=True`. Prompt: do not stall or call tools before a simple reply.

**Trade-off.** Replies stay short. Not a lecture. No published millisecond number — I will not invent one.

Evidence: `agent.py` comments at the LLM and TTS blocks.

### Hindi in the mouth and in the log

**What.** Learners mix Hindi and English. Windows consoles default to cp1252. Romanized Hindi is still Hindi mixing.

**Chosen.** Prompt: mirror the mix; Hindi → Devanagari; never default Roman. Worker reconfigures stdout/stderr to UTF-8. Deepgram `language="multi"`.

**Trade-off.** The model can still slip. Tests cover tools and router more than live bilingual judgement (`test_agent.py` is the LLM judge and CI skips it).

Evidence: `agent.py` lines 1–8 and LANGUAGE blocks; Deepgram kwargs.

### Privacy versus “useful dashboard”

**What.** Analytics wants a story. Voice products want a tape.

**Considered.** One database with a transcript column. Rejected. CI now forbids `utterance` / `transcript` columns in memory and analytics.

**Chosen.** Two files. Memory is consent profile. Analytics is anonymous ops. Scores stay in the conversation. Escalation sanitizes before webhook.

**Trade-off.** You cannot replay what was said. That is the point.

Evidence: `analytics/repository.py` schema; `.github/workflows/ci.yml` privacy job; `test_analytics_integration.py`; `PRIVACY_RULES`.

### Specialists without a second pipeline

**What.** Day 9 needed math. A second LiveKit session or second Murf would have been the easy fork.

**Chosen.** Same room. Host announces. `SpecialistRouter` is deterministic. One retry, then host. Shared context is read-only and strips transcript keys. Handback does not greet again.

**Trade-off.** Only math is live. Other specialists register disabled. Ambiguous “help me” must clarify before handoff.

Evidence: `specialists/recovery.py`, `shared_context.py` `BLOCKED_KEYS`, `test_specialist_handback.py`.

### Tools that chatter

**What.** Function tools make models announce “I will now look that up.”

**Chosen.** Prompt law: never say tool names; do not call tools to look busy; lookup once at session start. `SessionMemoryLookup` caches the SQLite read.

Evidence: `SYSTEM_PROMPT`; `memory/async_lookup.py`.

### Exercise provider failure

**What.** Optional HTTP exercises fail.

**Chosen.** Local JSON fallback, retry, cooldown (`provider_health`). Request cache TTL.

Evidence: `tools/provider_health.py`, `test_exercise_provider.py`.

### Escalation that fires too often

**What.** “I’m stuck” is not “get me a teacher.”

**Chosen.** Consent, allow-listed reasons, urgency without invented emergencies, dedupe, honest “webhook missing.”

Evidence: `escalation/`; `test_escalation_notifier.py`; prompt HUMAN HELP.

### Auth versus anonymous voice

**What.** Production RBAC wants a roster. The hall must work without an account.

**Chosen.** `AUTH_REQUIRED` defaults false. Token route: CSRF + rate limit, no login. Flip only after identity exists (doc 41).

**Trade-off.** Instruments can be open in the demo profile. That is documented, not accidental.

Evidence: `salora_platform/config.py`; `22_PRODUCTION_PLATFORM.md`; `lib/platform/http.ts`.

### Platform sprawl

**What.** Numbered engineering files reached 51. Easy to describe ten runtimes.

**Chosen.** Facades that wrap the worker. Public docs index. Architecture freeze: consume, do not rewrite.

**Trade-off.** Readers must be told Search Platform is not in the audio path. We keep saying it.

Evidence: `docs/README.md`; `41_SALORA_OS_V1_RELEASE.md`; `DAY10_ARCHITECTURE.md`.

### Event bus leak (stabilization)

**What.** `publish()` filtered forbidden **keys** only. A long value could still look like a transcript.

**Chosen.** Match observability: drop long forbidden values. Warn on unknown event names. Tests added.

Evidence: `services/events.py` `_clean_fields`; `test_ai_services.py` `test_event_bus_redacts_forbidden_keys_and_long_values`.

### Compose losing SQLite

**What.** Container recreate wiped `memory.db` / `analytics.db`.

**Chosen.** Volume `salora-data` → `/app/data`. Backend image `WORKDIR /app`.

Evidence: `docker-compose.yml`; `backend/Dockerfile`.

Approaches I did **not** take, because they are not in the repo: a second STT, a speech lake, Kafka, a custom interruption service. I will not narrate debates I cannot point at.

---

## 3. Key architecture decisions

**One Voice Pipeline.** Starter already had Murf. Day 6 telephony is a SIP path beside it, not a replacement. Day 9 guests use the same TTS constructor. Maintenance: one session to test. Scale: more LiveKit workers, not more mouths.

**One SpecialistRouter.** Adaptive Engine advises. A second router would disagree in production. Tests target one `route()` function.

**One pair of databases.** Testing privacy is a schema test, not a paragraph in a README.

**One facade each (orchestrator, runtime, search, automation, registry, bus, shell, fabric).** They exist so Phase 12–40 did not copy `agent.py`. They are thin. Testing them is “does this call the worker module,” not “does this speak.”

**One `can()`.** Python and TypeScript share the permission idea. UI selects are not authority.

**Rejected duplicates.** Second event bus (specialist logger is an allow-list, kwargs dropped). Second search index. Plugin execute. Autonomous loops. Those denials are tests (`may_execute`, `may_autonomous_loop`, HIPAA `ok: False`).

Future development is a new tool or a disabled specialist, or an instrument route like analytics — not a kernel fork. That is the freeze in doc 41.

---

## 4. Lessons learned

**What worked.** Putting every new day behind `AgentSession`. Deterministic scoring. Fail toward the host after one retry. CI that greps for speech columns. Prompt rules that match tests (Forget Me, sanitizer, handback).

**What surprised me.** Gemini’s default thinking after tools. Murf pacing hurting short lines. How fast a “helpful” dashboard asks for a transcript. How many platform names you can add before someone draws them into the voice path.

**What took longer.** Bilingual prompt law (mirror, Devanagari, no tool names). Escalation honesty (do not claim a notify you did not send). Documentation: 51 files needed a public index before a blog.

**What got easier.** After memory was a repository, knowledge and exercises were the same shape: tool in, structure out, speak in the model. After analytics was a second file, enterprise could read ops without touching `User`.

**Practices that paid.** `uv` / `pnpm` only. Ruff and pytest on every worker change. Vitest on engines. Distinguish implemented / architected / planned in the Day 10 briefs so the post cannot lie.

**If I started again.** I would write the two-database law on Day 1, not Day 8. I would take hall screenshots the day the wave worked. I would keep a one-page architecture map from the start so numbered docs did not become the only front door. I would not enable a second TTS “just to compare” in the worker — the commented realtime block is already a temptation.

I would not start with Kafka. I still would not.

---

## 5. Performance and stability

Optimization was knobs on the existing session, not a rewrite.

| Change | Why | Evidence |
| --- | --- | --- |
| Minimal thinking + 120 tokens | Stop post-tool stalls | `agent.py` LLM kwargs |
| `text_pacing=False` | Short tutor lines | TTS comment |
| Endpointing + preemptive generation | Start sooner after silence | `AgentSession` kwargs |
| Session memory cache | One SQLite read per room | `async_lookup.py` |
| Exercise cache + cooldown | Provider blips | `request_cache.py`, `provider_health.py` |
| Failure-isolated analytics | Dashboard must not kill voice | `agent.py` Day 8 comments |
| Voice continues if DB init fails | Mouth is first-class | `agent.py` startup warnings |
| Event value redact | Privacy hole in the bus | `events.py` + test |
| Architecture freeze | Stop forking | doc 41 |
| Contract tests | Facades stay wrappers | `test_os_v1.py`, `test_extensibility.py`, `test_experiences.py` |

I did not add Redis, a job broker, or incremental vector index. Those are listed as future in doc 41 and `infrastructure.py` (`implemented: False`).

---

## 6. Testing and validation

**Backend.** `uv run python -m pytest -q --ignore=tests/test_agent.py` — 434 passed on the last local validation pass. Suites cover memory, knowledge, tools, telephony, escalation, analytics, specialists, enterprise, then platform/OS/experience facades.

**Frontend.** `tsc --noEmit`, `pnpm lint`, `pnpm test` — 25 unit tests on engines (learning, adaptive, fabric, search, rbac, education).

**Lint.** Ruff is the Python gate (not black/mypy). Prettier/ESLint on the web. Stabilization fixed import sort and format drift that would have failed CI.

**Privacy.** CI job greps analytics/memory for speech columns.

**Security.** RBAC tests; event redact test; `AUTH_REQUIRED` left false on purpose.

**Search / automation.** `test_os_v1.py` — one search, one automation alias.

**Voice.** Live LLM judge (`test_agent.py`) needs LiveKit and is skipped in CI. Latency soak and concurrent rooms were **not** run in the validation pass. I will not claim they were.

**Fixed in stabilization (documented).** Event values, DB init logs, compose volume, Dockerfile WORKDIR, dead ternary, ruff/prettier blockers.

**Left out of scope.** Playwright e2e, OTel exporter, live room load, teacher/parent pages, plugin execute.

---

## 7. Future improvements

Only from `41_SALORA_OS_V1_RELEASE.md` and related docs:

1. Identity, then `AUTH_REQUIRED=true`
2. Studio editor / Whiteboard renderer / Graph as instruments (like analytics)
3. Queue behind `JOB_CATALOG`
4. OTel exporter
5. Signed plugin crypto
6. Mobile/desktop **implementations of existing contracts**

Also documented: Redis when rate limits need more than one process; Playwright not present; HIPAA not claimed.

These are future because the hall already talks, and the freeze says consume contracts rather than invent a second kernel. I am not promising dates.

---

## 8. Advice for other developers

Keep one session object. If you need math, hand off inside it.

Reuse a repository. Do not stand up a second “AI memory” when you already have SQLite and JSON.

Name platforms if you must. Do not put them in the audio diagram unless `agent.py` calls them.

Validate integrations with tests that fail closed: sanitizer, Forget Me, one retry, no speech column.

Privacy is a schema. If a column can hold a mouth, do not add it.

Measure latency if you publish a number. I configured knobs; I did not check in a benchmark. Do not copy a marketing millisecond.

Guardrails belong in the prompt **and** in tools (consent, allow-lists). A prompt alone is not a compiler.

Run unit tests on every day you add a tool. Keep the live judge optional so CI stays honest.

Write “implemented / architected / planned” in the README before the blog. It saved this chapter from becoming fiction.

---

## 9. Engineering retrospective

I would still pick LiveKit and Murf. I would still split the two databases. I would still fail toward the host.

I would index docs earlier. I would record the hall the week the wave worked. I would treat “enterprise” as a page that reads ops, not as a reason to grow a second voice stack.

The work I am proud of is mostly refusal: no second TTS, no transcript lake, no silent specialist swap, no fake notify, no plugin execute. The work that talks is still `my_agent`.

---

## 10. Challenge and learning verification

| Item | Backed by |
| --- | --- |
| Day 1–9 sequence | `git log` subjects |
| Latency knobs | `agent.py` comments + kwargs |
| Two databases / no speech columns | schemas + CI privacy job |
| One-retry specialist | `recovery.py` + tests |
| Event value redact | `events.py` + `test_ai_services.py` |
| Compose volume | `docker-compose.yml` |
| Auth default open | config + production doc |
| 434 / 25 tests | last validation run (local) |
| Live voice soak | Not run — do not claim |
| TODO in `backend/src` | None found |
| Future list | doc 41 only |
| “Months of work” as calendar | Not supported — challenge days + local layer |
