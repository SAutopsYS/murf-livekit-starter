# Day 10 — Blog and LinkedIn brief

Foundation notes. Final post: [DAY10_BLOG.md](DAY10_BLOG.md). LinkedIn: [DAY10_LINKEDIN.md](DAY10_LINKEDIN.md). Showcase: [SALORA_OS_SHOWCASE.md](SALORA_OS_SHOWCASE.md).

Facts only. Local working tree as of 15 Aug 2026. `origin/main` last commit is Day 9. SALORA OS docs and facades exist locally and are largely uncommitted.

---

## 1. Project summary

**Name:** SALORA OS / SALORA AI  
**Product:** AI Voice Learning Tutor  
**Track:** Murf VoiceForBharat 2026 — Learning & Literacy  
**Kernel:** LiveKit Agents + Murf Falcon TTS + Deepgram Nova-3 + Gemini  

Learners open the hall in the browser, speak, and get a spoken reply. The Python worker joins the same LiveKit room. Frontend and backend do not stream audio to each other.

---

## 2. Voice agent overview

### Primary purpose

Help people practice spoken English through a short, spoken conversation. The agent is a tutor, not a general chatbot.

### Target users

Students and adult learners in India who want to practice English, including people who mix Hindi and English.

### Real-world use case

A learner says they want speaking practice. The tutor greets them, may remember a consented profile, gives a spoken exercise, scores the answer with a rule-based tool, and suggests the next practice. If they ask for math, the same room hands off to a Math Practice Specialist. If they ask for a human teacher, the agent escalates only after consent.

### Why voice is useful

Reading a lesson is not the same as speaking. Voice lets the learner practice turn-taking, pronunciation, and confidence without typing. Hindi and Hinglish stay spoken, with Hindi written in Devanagari when the model replies in Hindi.

### Conversation flow (implemented)

1. Learner clicks Enter the hall, allows the microphone.
2. Next.js mints a LiveKit token (`POST /api/token`).
3. Worker `my-agent` joins the room.
4. `on_enter`: async memory lookup, spoken greeting (Hindi / English / both).
5. Turns: listen → think → speak. Tools only when the prompt requires them.
6. Optional: exercise → score → recommend → another exercise.
7. Optional: math handoff / handback on the same room.
8. Optional: human-help escalation after consent.
9. `on_exit` / shutdown: touch last interaction, complete analytics.

### Voice Pipeline (implemented)

```text
Deepgram STT (nova-3, language=multi)
  → Gemini 3.5 Flash Lite (temp 0.6, max 120 tokens, thinking minimal)
  → Murf Falcon TTS (Anisha, Conversation, text_pacing=False)
LiveKit room + Silero VAD + multilingual turn detector
endpointing 0.3–1.5s, preemptive_generation=True
```

### Agent lifecycle

`disconnected → connecting → ready/idle → listening → thinking → speaking → idle → disconnecting`.  
ViewController owns screens. `deriveVoiceSnapshot` owns in-session meaning (local OS layer).

### Supported features (agent tools)

| Tool group | Functions |
| --- | --- |
| Memory | `lookup_user`, `save_user_memory`, `update_last_interaction`, `forget_user_memory` |
| Knowledge | `search_learning_knowledge` |
| Learning | `get_next_exercise`, `score_spoken_answer`, `recommend_next_practice` |
| Escalation | `create_escalation`, `get_escalation_status`, `prepare_resolution_callback` |
| Handoff | `handoff_to_math_specialist` |

### Current limitations (do not hide)

- Replies are kept short (prompt: under 20 words when possible). Not a long-form teacher.
- Scores are conversation-scoped. They are not written onto `User`.
- Memory needs explicit consent. Anonymous learners stay anonymous.
- Math is the only live specialist. Other guests are registered/disabled.
- Outbound telephony is a backend path. It is not a hall button.
- Escalation notify needs `ESCALATION_WEBHOOK_URL`. Without it, the agent must not claim a human was notified.
- `AUTH_REQUIRED` defaults false. Instruments are open in the demo profile.
- No live latency numbers in-repo. No demo video or session screenshots in `docs/assets/`.
- Studio, Whiteboard, Marketplace execution, and autonomous loops are not product UI.

---

## 3. Architecture summary

```text
Browser (Workspace Shell)
  /                hall — voice
  /analytics       call ops
  /enterprise      control center
        │
        │  token, health, CLI analytics
        ▼
Next.js  +  salora_platform (RBAC, config)     [local OS layer]
        │
        ▼
LiveKit Cloud
        │
        ▼
agent.py Voice Pipeline
  SpecialistRouter (only routing authority)
  memory.db (consented profile)
  analytics.db (anonymous call ops)
  knowledge JSON
  services/* facades                      [local OS layer]
```

| Piece | Actual implementation |
| --- | --- |
| STT | `deepgram.STT(model="nova-3", language="multi")` in `agent.py` |
| LLM | `google.LLM(model="gemini-3.5-flash-lite")` |
| TTS | `murf.TTS(voice="Anisha", style="Conversation")` |
| Transport | LiveKit Agents `AgentSession`, agent name `my-agent` |
| Agent Runtime | Host tutor + registry projection. `may_autonomous_loop` is false |
| Tool calling | LiveKit `@function_tool` list `AGENT_TOOLS` |
| Memory | SQLite `backend/data/memory.db`. No scores, no transcripts |
| Search | JSON `knowledge.search`. Platform search fans out to catalog/agents (local) |
| Automation | One `AutomationService` stub (local). No Kafka |
| Knowledge Fabric | Frontend projection over existing search (local). No second DB |
| Enterprise | `/enterprise` Control Center + specialist graph (Day 9). Tenants in-memory (local) |
| Event bus | In-process `services/events.py` (local). Specialist logger is separate and drops extra kwargs |

One Voice Pipeline. One SpecialistRouter. Do not describe a second mouth.

---

## 4. Feature inventory

### Implemented (learner can use this)

- Live voice conversation in the browser
- Murf Falcon TTS (`Anisha`)
- LiveKit transport and agent dispatch
- Deepgram multilingual STT
- Gemini replies with Hindi / English / Hinglish rules
- Spoken greeting
- Prompt guardrails (no medical/legal/finance diagnosis, no cheating, no shame)
- Consent-first memory and Forget Me
- Knowledge JSON search for grammar/vocab/pronunciation facts
- Exercise lookup (local JSON, optional HTTP with fallback)
- Deterministic spoken-answer scoring
- Follow-up recommendations (conversation only)
- Human-help escalation with reference IDs, urgency, sanitization, dedupe
- Math specialist handoff/handback on the same room
- Analytics dashboard `/analytics` (no speech fields)
- Enterprise Control Center `/enterprise` (Day 9)
- Theme toggle, session states, wave visualizer, chat input
- Backend tests (434 local, CI skips live LLM judge)
- Frontend unit tests (25)

### Partially implemented

- Outbound telephony (code + tests; needs SIP/Twilio env)
- Escalation webhook delivery (code; URL optional)
- Workspace Shell and command palette (local; planned routes toast)
- RBAC / `AUTH_REQUIRED` (exists; default open for anonymous voice)
- Education / mentor / marketplace **providers** (local; not mounted on `/`)
- Search / automation facades (local; consume existing modules)
- Compose + CI + health routes (local working tree)

### Architecture only

- AI Studio editor
- Whiteboard renderer
- Memory Graph UI
- Marketplace plugin execution (`may_execute` is false)
- Public OAuth server / developer portal
- Redis, Kafka, Kubernetes, vector DB
- CRDT collaboration
- Mobile / desktop apps
- Autonomous agent loops
- HIPAA certification

### Future work (documented, not built)

- Identity roster then `AUTH_REQUIRED=true`
- Queue behind `JOB_CATALOG`
- OTel exporter
- Signed plugin crypto
- Instrument UIs for Studio / Whiteboard / Graph
- Real screenshots and a demo recording

---

## 5. Development journey

### Milestones (git `main`)

| Commit theme | What shipped |
| --- | --- |
| Starter | Murf + LiveKit template |
| Day 1 | Working voice agent |
| Day 2 | Tutor prompt, guardrails, Hinglish, greeting |
| Day 3 | Hall UX: states, wave, suggestions, mic errors |
| Day 4 | `memory.db`, consent, Forget Me, knowledge tools |
| Day 5 | Exercises, scoring, recommendations, failover |
| Day 6 | Outbound telephony path (browser pipeline unchanged) |
| Day 7 | Human-help escalation |
| Day 8 | `analytics.db` + `/analytics` |
| Day 9 | SpecialistRouter, Math guest, `/enterprise` |

Local (uncommitted) work after Day 9: Workspace Shell, `salora_platform`, service facades, docs 01–51, Day 10 docs cleanup.

### Architectural decisions that stuck

- One LiveKit room, one Murf voice. Specialists are guests, not a second TTS.
- Two SQLite files. Never join identity to anonymous call ops.
- Scores stay in the conversation. Memory holds profile facts only after consent.
- Hindi replies use Devanagari. Romanized Hindi in the learner’s speech still counts as mixing.
- SpecialistRouter is deterministic. The Adaptive Engine may advise. It does not route.
- Gemini thinking is forced minimal and output is capped so spoken turns stay short.

### Problems and how they were solved

| Problem | Solution that shipped |
| --- | --- |
| Second-agent temptation | Same session, handoff tools, disabled placeholders never route |
| Transcripts on dashboards | Separate analytics schema; privacy CI forbids speech columns |
| Slow spoken turns | `thinking_level=minimal`, `max_output_tokens=120`, `text_pacing=False`, short endpointing |
| Hindi in Windows logs | UTF-8 stdout reconfigure; no second TTS |
| Tool chatter | Prompt: answer first, tools only when needed, never say tool names |
| Provider outage on exercises | Local JSON fallback + cooldown |
| Escalation over-trigger | Consent + reason allow-list + dedupe |
| Auth vs anonymous voice | `AUTH_REQUIRED` default false. Do not flip without a roster |

### Lessons

- Voice products fail when the prompt is long and the model thinks out loud. Cap tokens. Speak one idea.
- Privacy is a schema law, not a UI promise.
- “Enterprise” can sit on the same mouth. A second pipeline is the expensive mistake.
- Docs can outgrow the hall. Architecture-only modules must stay unmounted.

---

## 6. Challenges and lessons (blog-ready)

**Challenge:** Keep Murf Falcon as the only voice while adding memory, tools, telephony, escalation, and a math specialist.  
**Lesson:** Add tools and guests. Do not add a second STT/TTS.

**Challenge:** Learners speak Hindi, English, and Hinglish.  
**Lesson:** Mirror the mix. Write Hindi in Devanagari. Do not force English.

**Challenge:** Dashboards want “what was said.”  
**Lesson:** Store outcomes and latency. Do not store utterances.

**Challenge:** Gemini 3.x thinks after tools.  
**Lesson:** Minimal thinking + short max tokens. Tutor replies stay speakable.

---

## 7. Repository review (recommendations only)

Do not treat these as work done in this pass.

- Commit or stash the local OS layer before the public Day 10 tag, or the GitHub repo will not match the blog.
- `scripts/node_modules` should stay untracked (currently 0 tracked files).
- LICENSE still says Copyright Murf Inc. (starter). Call that out if you publish as SALORA.
- Root README is cleaned. Numbered engineering files remain an archive — point blogs at `docs/README.md`.
- `app-config.ts` pageDescription still says “world’s first.” Optional copy tweak later. Not required for Day 10 facts.

---

## 8. Documentation review

| Doc | Role for the blog |
| --- | --- |
| [README.md](../../README.md) | Setup and stack |
| [docs/architecture/overview.md](../architecture/overview.md) | Layer diagram |
| [docs/architecture/voice-platform.md](../architecture/voice-platform.md) | Pipeline |
| [VOICEFORBHARAT.md](VOICEFORBHARAT.md) | Days 1–9 |
| [guides/installation.md](../guides/installation.md) | Setup block |
| [guides/configuration.md](../guides/configuration.md) | Env table |

Missing for the blog: screenshots, a 30–60s demo clip, a measured latency line.

---

## 9. Public release checklist

| Check | Status |
| --- | --- |
| `.env.local` gitignored | Yes (backend + frontend) |
| Tracked env files | `.env.example` placeholders only |
| Live API keys in git | None found |
| Real webhook URLs | None found |
| Phone numbers in tests | Fake `+919876543210` only |
| Speech columns in DBs | Forbidden; CI scan exists |
| SQLite DBs tracked | No (`data/*.db` ignored) |
| Personal learner data | Not in git |
| Uncommitted OS surface | Large. Decide what GitHub should show |

Recommend: before push, `git status` and confirm no `.env.local`. Do not commit `backend/data/*.db`.

---

## 10. Blog content outline (do not write the post yet)

1. **Intro** — I built a spoken English tutor for VoiceForBharat Learning & Literacy.
2. **Problem** — Learners need to *speak*, not only read. Typing a chatbot is the wrong loop.
3. **Audience** — Students and adults in India; Hindi / English / Hinglish.
4. **Why voice** — Turn-taking, confidence, native-script replies.
5. **What it does** — Greet, remember with consent, exercise, score, recommend, math handoff, human help, analytics.
6. **Architecture** — One pipeline diagram. LiveKit in the middle. Two SQLite files.
7. **Murf Falcon** — `Anisha`, conversational, pacing off, same mouth for the specialist.
8. **Hard parts** — Privacy schema, bilingual speech, short turns, one-room handoff.
9. **What I refused** — Second TTS, transcript lake, score persistence, silent specialist swap.
10. **Setup** — Link README / installation guide. Two terminals or `start_app.*`.
11. **What’s next** — Identity, instrument UIs, a recorded demo. Not a new voice stack.
12. **Close** — Repo link. Hall URL locally. Days 1–9 table.

### LinkedIn outline (short)

- One sentence: spoken English tutor on LiveKit + Murf Falcon.
- Three facts: bilingual, consent memory, math guest on the same voice.
- One constraint: no second pipeline, no transcripts stored.
- Link + ask: try saying “Give me an exercise” or a fraction problem.

---

## 11. Assets

### Available

- `frontend/public/salora-mark.svg` and `salora-mark-dark.svg`
- ASCII / Mermaid-style diagrams in docs
- Code: `backend/src/agent.py` pipeline block (lines ~470–505)
- Test signal: 434 backend / 25 frontend (local)
- Open Graph image route (`app/opengraph-image.tsx`)

### Missing (needed for a strong Day 10 post)

- Hall ready screenshot
- Live session screenshot (wave + status; no real learner transcript)
- `/analytics` screenshot
- `/enterprise` screenshot
- 30–60s silent or consented demo video / GIF
- Measured first-response time from a real call (analytics already records `first_response_at`)

---

## 12. Setup instructions (copy for the blog)

```bash
cp backend/.env.example backend/.env.local
cp frontend/.env.example frontend/.env.local
# LIVEKIT_*, MURF_API_KEY, DEEPGRAM_API_KEY, GOOGLE_API_KEY
```

```bash
cd backend && uv sync && uv run python src/agent.py download-files && uv run python src/agent.py dev
cd frontend && pnpm install && pnpm dev
```

Open http://localhost:3000.

---

## 13. Scores (this brief)

| Score | Value | Why |
| --- | --- | --- |
| Repository readiness | 78 | Env hygiene is good. Large uncommitted tree. No screenshots. LICENSE is starter copyright. |
| Day 10 blog readiness | 80 | Facts and outline are enough to write. Demo media and a commit decision are the gaps. |
