# Day 10 — Phase 1: Research and story foundation

Not the final blog. Evidence from the working tree, 15 Aug 2026.

`origin/main` last commit: Day 9 enterprise. Local tree also has Workspace Shell, `salora_platform`, service facades, and docs 01–51. Those are called out when they are not on `main`.

---

## 1. Repository research summary

| Area | What exists | Evidence |
| --- | --- | --- |
| Voice worker | One `AgentSession` in `backend/src/agent.py` | `deepgram.STT`, `google.LLM`, `murf.TTS`, `agent_name="my-agent"` |
| Hall UI | `/` → `App` → ViewController | `frontend/app/page.tsx`, `components/app/` |
| Instruments | `/analytics`, `/enterprise` | `frontend/app/analytics`, `app/enterprise` |
| Memory | Consented SQLite `users` | `backend/src/memory/`, tests `test_memory*.py` |
| Knowledge | JSON search tool | `knowledge/tools.py` `search_learning_knowledge` |
| Learning tools | Exercise, score, recommend | `tools/livekit_tools.py`, Day 5 tests |
| Specialists | Math live; others disabled | `specialists/router.py`, `test_specialist_*.py` |
| Escalation | Consent + webhook + status | `escalation/tools.py`, `test_escalation_*.py` |
| Analytics | Separate `analytics.db` | `analytics/`, privacy tests |
| OS layer | Shell, RBAC, facades | Local `components/os/`, `src/services/` — mostly uncommitted |
| Studio / Marketplace exec | Providers only | Docs 24, 27. No `/studio` route. `may_execute` false |
| Search / Automation | One facade each | `services/search.py`, `services/automation.py` (local) |
| Config | Example env only | `backend/.env.example`, `frontend/.env.example` |
| Deploy | Compose + Dockerfiles | `docker-compose.yml` (local), `backend/Dockerfile` |
| Tests | 434 backend / 25 frontend (local last run) | CI skips `test_agent.py` |

No live latency numbers in the repository. No session screenshots in `docs/assets/`.

---

## 2. Recommended blog format

**Hybrid.** Not a pure story. Not a pure tutorial.

### Why this repo

The challenge is a 10-day build. Days 1–9 are a real sequence in git. Readers need that story. The interesting engineering is a **constraint**: one Voice Pipeline, two databases, no speech columns. That needs a technical middle.

A story-only post would skip Murf/LiveKit, which the track cares about. A tutorial-only post would read like a starter README and hide why specialists share one mouth.

### How to structure the final blog

| Section | Mode |
| --- | --- |
| Hook, problem, who it is for | Story |
| What the tutor does in a session | Story, then a short workflow list |
| Voice Pipeline (STT / LLM / TTS / LiveKit) | Technical |
| Tools, memory, privacy schema | Technical |
| Math handoff on the same room | Story + one diagram |
| What we refused to build | Story (decisions) |
| Setup | Tutorial (link `docs/guides/installation.md`) |
| Limits and next | Honest, short |

### Recommended outline

1. Title + hook (one learner, one line, one mouth)
2. The problem (speaking practice vs typed chat)
3. Who this is for
4. A session walkthrough (greeting → exercise → score → optional math / help)
5. Architecture: LiveKit in the middle
6. Murf Falcon as the only TTS
7. Memory and analytics as two files
8. Tools without saying tool names out loud
9. Days 1–9 in one table
10. Limits
11. How to run
12. What Day 10 is (audit, not a new engine)

---

## 3. Project story

**Inspiration (docs + git).** The repo began as the Murf LiveKit starter, then became a VoiceForBharat Learning & Literacy tutor (Days 1–9 on `main`). Brand docs name the product SALORA OS: śālā (hall) + ōra (speech). Evidence: `docs/salora/BRAND.md`, `docs/salora/VOICEFORBHARAT.md`, `git log` Day 1–9 subjects.

**Problem.** Learners who want spoken English do not get far by typing a chatbot. They need to hear a reply and answer out loud. Hindi speakers also need the tutor to follow the mix they actually use.

**Why voice.** The prompt and hall are built for speech: short turns, no markdown, one question at a time, wave + status, microphone permission view. Evidence: `SYSTEM_PROMPT` STYLE block in `agent.py`; `welcome-view.tsx` practice suggestions; `view-controller.tsx` session states.

**Why real-time.** LiveKit keeps both sides in one room. The worker does not poll a REST chat API for audio. Token route and `AgentSession` are the join path. Evidence: `frontend/app/api/token/route.ts`, `my_agent` in `agent.py`.

**What is different (implemented, not slogan).**

- Same Murf voice after math handoff. No second TTS. Evidence: `handoff.py`, prompt MATH SPECIALIST HANDOFF, tests `test_specialist_handback.py`.
- Memory is opt-in and erasable. Scores do not land on `User`. Evidence: `SYSTEM_PROMPT` CONSENT / FOLLOW-UP; `memory/repository.py` schema.
- Analytics cannot store utterances. Evidence: `analytics/repository.py` columns; CI privacy job; `test_analytics_integration.py` privacy case.

**Vision (docs).** Product Bible: keep the learner on the line; dashboards serve the thread; do not rewrite the kernel. Evidence: `docs/engineering/01_PRODUCT_BIBLE.md`. The live product is still the hall tutor. OS rooms (Studio, Marketplace) are architecture or unmounted providers.

Avoid in the blog: “world’s first” (it appears in `BRAND.md` and `app-config.ts` pageDescription). That is brand copy, not a measurable claim.

---

## 4. Voice agent introduction

| Field | Implemented value | Evidence |
| --- | --- | --- |
| Dispatch name | `my-agent` | `agent.py` `@server.rtc_session(agent_name="my-agent")` |
| Class | `Assistant` | `agent.py` |
| Spoken identity | “AI Voice Learning Tutor” / “AI Learning Tutor” | `SYSTEM_PROMPT` IDENTITY; `GREETING_INSTRUCTIONS` |
| Product chrome | SALORA OS / SALORA AI | `frontend/app-config.ts` |
| Start label | Enter the hall | `app-config.ts` `startButtonText` |

**Primary objective.** Help the user improve spoken English, confidence, vocabulary, and simple grammar through conversation. Evidence: `SYSTEM_PROMPT` OBJECTIVES.

**Audience (implemented).** A person in the browser hall. Language: English, Hindi, or Hinglish. Hindi replies use Devanagari. Evidence: LANGUAGE and LANGUAGE & SCRIPT blocks.

**Workflows that run today**

1. Greet and practice (no tools).
2. Consent, save profile, return later, Forget Me.
3. Knowledge lookup for a factual language question.
4. Exercise → spoken answer → score → recommend → optional next exercise.
5. Math question → announce → `handoff_to_math_specialist` → handback, no new greeting.
6. Upset + ask for a teacher → consent → escalation reference ID.
7. Call ops appear on `/analytics` after a session (anonymous).

**Limitations (implemented constraints)**

- Prompt asks for under 20 words when possible. Not a lecture.
- Chat input is also on (`supportsChatInput: true`). Voice is primary, not exclusive.
- Math is the only live specialist. Router rejects disabled guests. Evidence: `router.py` `validate`, `test_specialist_recovery.py`.
- Telephony is backend-only. Evidence: `telephony/`; no hall dial button found.
- Escalation notify is a no-op without webhook. Evidence: `test_escalation_notifier.py` missing webhook.
- Teacher/parent **pages** are not mounted. Education wrappers exist locally. Evidence: no `app/teacher` route; `services/education.py` wraps enterprise builders.

---

## 5. Target users

Product Bible lists learner, parent, teacher, school admin, operator. Evidence: `01_PRODUCT_BIBLE.md` personas. Map that to **what the code actually offers**.

### Students / learners

**Problem:** Need to speak, not only read.  
**Voice:** Hall session, suggestions (vocabulary, speaking, grammar, daily talk).  
**Support today:** Full Voice Pipeline, memory, exercises, scoring, math guest.  
Evidence: `welcome-view.tsx` `PRACTICE_SUGGESTIONS`; agent tools.

### Teachers

**Problem:** See pulse without listening to a tape.  
**Voice:** Human-help escalation when a learner asks for a teacher.  
**Support today:** Escalation reference IDs + `/enterprise` aggregates (Day 9). `TeacherConsoleService` builds a sanitized student list (consented users only). **No dedicated `/teacher` UI.**  
Evidence: `enterprise/platform.py` `TeacherConsoleService`; `escalation/`; `os-nav.ts` has no teacher route.

### Parents

**Problem:** Time, topic, next step — not a recording.  
**Voice:** Child (or adult learner) practices in the hall.  
**Support today:** `ParentDashboardService` exists as a backend builder. Education `ParentService` wraps it locally. **No dedicated parent page on the hall.** Do not claim a shipped parent app.  
Evidence: `enterprise/intelligence.py`; `services/education.py`; no `app/parent`.

### Developers

**Problem:** Run and extend without forking the pipeline.  
**Voice:** Same worker; add `@function_tool` or a specialist behind the router.  
**Support today:** README, `docs/guides/`, `AGENTS.md`, tests. SDK / public API are envelopes and architecture. **No developer portal UI.**  
Evidence: `docs/api/sdk.md`; `45_PUBLIC_API_PLATFORM.md` `portal_ui: False`.

### Organizations / enterprise users

**Problem:** Health and policy without speech as a toy.  
**Voice:** Same tutor; Control Center reads aggregates.  
**Support today:** `/enterprise` (Day 9). Local tenant models are in-memory. `AUTH_REQUIRED` defaults false.  
Evidence: `frontend/app/enterprise`; `services/tenants.py`; `salora_platform` config.

---

## 6. Why voice instead of a traditional UI

The hall still has a start button, practice chips, and optional chat. Voice is the **practice medium**, not the only input. Evidence: `supportsChatInput: true`; `PRACTICE_SUGGESTIONS` send a prompt into the LiveKit session.

| Reason | How this repo supports it | Evidence |
| --- | --- | --- |
| Accessibility | Mic permission view and retry; status badges; spoken greeting | `microphone-permission-view.tsx`, `session-status-badge.tsx` |
| Faster loop | Short replies, preemptive generation, 0.3–1.5s endpointing | `agent.py` session kwargs |
| Hands-free | Once in session, speech is the turn | LiveKit `AgentSession`; wave panel |
| Learning | Exercises and scoring are spoken | `get_next_exercise`, `score_spoken_answer` |
| Natural mix | Mirror Hindi / English / Hinglish | `SYSTEM_PROMPT` LANGUAGE |
| Real-time | Shared LiveKit room, not request/response audio files | token route + worker |

Do not claim a measured “X ms faster than typing.” Evidence not found in the current repository.

---

## 7. Murf Falcon and LiveKit

### LiveKit

**Role:** Real-time room. Browser participant + worker participant. Token minted in Next.js.  
**Why it is in the repo:** Starter and Days 1–9 are LiveKit Agents. Frontend uses `livekit-client` / Agents UI.  
**Implementation:** `POST /api/token` (`livekit-server-sdk`); worker `@server.rtc_session`; optional SIP in `telephony/` (partial).  
Evidence: `frontend/app/api/token/route.ts`; `agent.py`; `backend/.env.example` `LIVEKIT_*`.

### Murf Falcon

**Role:** Only TTS. Voice `Anisha`, style `Conversation`, `text_pacing=False`.  
**Why:** Challenge TTS. Prompt and comments name Anisha / Samar / Pooja as recommended.  
**Implementation:** `from livekit.plugins import murf` then `murf.TTS(...)`. Same mouth after specialist handoff (no second `TTS()`).  
Evidence: `agent.py` lines 486–492; `MURF_API_KEY` in `.env.example`.  
Do not claim a latency benchmark. Evidence not found (no checked-in Falcon vs other TTS numbers in this tree’s current docs). An older commit message says “Added benchmark comparison”; that content is not in the current README.

### Voice Pipeline

STT Deepgram nova-3 `language="multi"` → Gemini `gemini-3.5-flash-lite` → Murf. VAD Silero prewarm. `MultilingualModel` turn detector.  
Evidence: `agent.py` `my_agent`. Tests: `test_ai_services.py` `VoiceService.status()` reports livekit / murf / deepgram (local services package).

---

## 8. Development journey

Commit history **is** available on `main` (Days 1–9). Local OS work is mostly uncommitted.

| Milestone | Decision |
| --- | --- |
| Day 1 | Ship a talking agent before features |
| Day 2 | Tutor prompt, guardrails, greeting — still one pipeline |
| Day 3 | Hall states and wave; session ≠ machine later split in local voice lib |
| Day 4 | Consent memory; Forget Me; knowledge as a tool |
| Day 5 | Tools + local fallback; scores not saved to memory |
| Day 6 | Telephony as a **separate** path; browser pipeline unchanged |
| Day 7 | Escalation only after consent; sanitize before webhook |
| Day 8 | Second SQLite file; no utterance columns |
| Day 9 | SpecialistRouter; Math guest; fail toward host after one retry |
| Local after 9 | Facades and docs. Hall still voice-only |

**Priorities that show up in code:** fail closed, privacy schema, short spoken turns, reuse `agent.py`.

**Lessons:** Add tools and guests. Do not add a second STT/TTS. Privacy is columns, not a disclaimer.

---

## 9. Project highlights

| Highlight | Why it matters | Evidence |
| --- | --- | --- |
| One Voice Pipeline | Specialists do not fork Murf | `agent.py` single `AgentSession`; handoff tests |
| Privacy split | Memory ≠ analytics | Two DB paths; CI speech-column job |
| Consent + Forget Me | Licensed memory | `memory/tools.py`; `test_forget_user_memory.py` |
| Deterministic scoring | No LLM judge for practice scores | `tools/score_tool.py` |
| SpecialistRouter | Math only when confident | `router.py`; recovery tests |
| Hall + instruments | Voice stays first | `/` vs `/analytics` `/enterprise` |
| Docs after Day 9 | Map for a blog | `docs/README.md` |

Search, Automation, Agent Runtime facades, Marketplace catalog: important as **architecture discipline** (one of each). They are not hall features. Say that in the blog.

---

## 10. Blog foundation

### Title ideas

1. One mouth: building a spoken English tutor on LiveKit and Murf Falcon
2. Learning that stays on the line — a VoiceForBharat tutor
3. Days 1–10: a voice tutor that refuses a second pipeline
4. Hindi, English, and a single Murf voice
5. What we stored — and what we refused to store

### Subtitle ideas

- A Learning & Literacy agent with consent memory, exercises, and a math guest in the same room
- VoiceForBharat Day 10 notes from a working LiveKit + Murf Falcon tutor
- Architecture constraints from a real hall, not a rewrite

### Opening hook (draft, not the full post)

I did not need another chatbot. I needed something that would wait while I spoke, answer in the mix I used, and forget me if I asked. The hall still uses one LiveKit room and one Murf voice. Everything else had to fit that.

### Executive summary (for the top of the post)

SALORA OS is a browser hall for spoken English practice. A Python LiveKit worker hears with Deepgram, thinks with Gemini, and speaks with Murf Falcon (Anisha). Learners can save a profile only after consent, take a spoken exercise, get a rule-based score, ask for math on the same voice, or escalate to a human after permission. Analytics keep call outcomes, not transcripts. Day 10 is the write-up, not a new engine.

### Table of contents (for the final post)

1. The problem
2. A session in the hall
3. Why voice
4. LiveKit and Murf Falcon
5. Memory and analytics
6. Tools and the math guest
7. Ten days, one pipeline
8. Limits
9. Run it yourself

### Key messages

1. Voice is the practice, not a decoration on a form.
2. One TTS. Guests visit and leave.
3. Consent before memory. Forget Me is real.
4. No utterance column.
5. Hindi is Devanagari.
6. Day 10 does not add a second architecture.

---

## 11. Evidence summary

Cited above: `agent.py`, `app-config.ts`, `welcome-view.tsx`, `token/route.ts`, `memory/`, `knowledge/`, `tools/`, `specialists/`, `escalation/`, `analytics/`, `01_PRODUCT_BIBLE.md`, `BRAND.md`, `VOICEFORBHARAT.md`, Day 4–9 tests, `git log` on `main`.

---

## 12. Missing information

| Item | Status |
| --- | --- |
| Live first-response latency | Evidence not found in the current repository (field exists in analytics; no published number) |
| Demo screenshots / video | Evidence not found under `docs/assets/` |
| Falcon vs other TTS benchmark in current docs | Evidence not found (old commit message only) |
| Teacher / parent dedicated routes | Evidence not found |
| Studio / Marketplace product UI | Evidence not found (providers + docs only) |
| Whether local OS layer will be in the public Day 10 tag | Not decided in-repo |

---

## 13. Phase 1 readiness score

**86 / 100**

Research is enough to write the opening and the architecture middle. Gaps are media, a commit/push decision, and any latency figure you measure yourself later — do not invent one.
