# Day 10 — Core features and AI capabilities (draft)

Technical middle of the VoiceForBharat post. Not the full article.

**Implemented** = hall or worker does this.  
**Architected** = facade or contract in the tree; not the live audio path.  
**Planned** = written as later work.

---

## 1. Core features overview

The thing a learner can use without reading a diagram is still the hall.

You join a LiveKit room. The worker `my-agent` joins with you. You speak. Deepgram hears. Gemini answers in a short line. Murf Falcon says it. That loop is the product.

Around it I bolted only what the conversation needed: a consented profile, a small knowledge JSON, spoken exercises with a rule-based score, a math guest in the same room, a human-help request after permission, and two instrument pages that never store speech.

A later layer names “Search Platform,” “Automation Platform,” “AI Orchestrator,” “Agent Runtime.” Those are real modules in `backend/src/services/`. They wrap the worker. They do not sit between your microphone and Murf. If I draw them in the voice path, I am lying.

What I would demo on Day 10, in order: start talking, take an exercise, ask a fraction question, ask to forget me, open `/analytics`. Everything else is either a tool behind that, or architecture beside it.

---

## 2. Voice AI capabilities

### Real-time conversation — implemented

A Next.js token route mints a LiveKit JWT. The browser client and the Python `AgentSession` share one room. Audio does not hop through my own socket server. I needed that because a tutor who “uploads a clip and emails you back” is not practice.

### Speech-to-text — implemented

`deepgram.STT(model="nova-3", language="multi")` in `agent.py`. Multi is there for English, Hindi, and mixed turns. I did not train a custom model.

### Murf Falcon TTS — implemented

`murf.TTS(voice="Anisha", style="Conversation", text_pacing=False)`. Sentence tokenizer, minimum two sentences. Pacing was making short tutor lines late, so I turned it off. Only TTS constructor in the worker. Tests in `test_ai_services.py` assert transport/tts/stt labels on the voice facade.

### LiveKit session — implemented

`@server.rtc_session(agent_name="my-agent")`. Silero VAD is prewarmed. `MultilingualModel` turn detector. Endpointing 0.3–1.5s. `preemptive_generation=True` so Gemini can start while the end of the turn is still settling. I do not have a custom barge-in module. If the user talks over the agent, that is the Agents session and VAD, not a SALORA “interruption service.” Evidence for a separate interruption API: not found.

### Greeting and language — implemented

`GREETING_INSTRUCTIONS` plus the LANGUAGE block. Hindi replies use Devanagari. Romanized Hindi still counts as mixing. Chat input is also enabled (`supportsChatInput: true`). Voice is the practice, not the only wire.

### Guardrails — implemented (prompt + tools)

The system prompt refuses medical, legal, financial, and disability diagnosis, and exam cheating. It will not shame pronunciation. Escalation tools add a second gate: consent, allow-listed reasons, sanitizer, dedupe. Prompt text is not a compiler. The tests that bite are the escalation sanitizer and specialist privacy logs.

### Specialist handoff — implemented

Math only. `handoff_to_math_specialist` after the host says it is connecting you. `SpecialistRouter` is the authority. One retry, then back to the host (`specialists/recovery.py`). Shared context is read-only for the guest and strips transcript keys. Handback does not replay the first greeting. Evidence: `test_specialist_handback.py`, `test_specialist_recovery.py`, `test_shared_context.py`.

### Human escalation — implemented (notify is partial)

`create_escalation`, status, optional callback prepare. Webhook is optional. If it is missing, the agent must not claim a human was pinged. Evidence: `test_escalation_notifier.py`.

### Voice UI — implemented

Welcome, connecting, session, ended, mic-permission. Wave visualizer. Status badge. Practice chips send a prompt into the same LiveKit chat path. Local `deriveVoiceSnapshot` maps LiveKit + mute + transfer into phases. That mapper is in the working tree; it does not change the worker.

---

## 3. AI intelligence pipeline

This is the path that actually produces sound:

```text
Microphone
  → LiveKit room
  → Deepgram STT
  → Gemini 3.5 Flash Lite
       ↳ may call AGENT_TOOLS
  → Murf Falcon TTS
  → LiveKit playback
```

Gemini is the only place tools run in a live turn. The tool list is memory, knowledge search, exercise, score, recommend, escalation, math handoff. The prompt says: answer first; do not call tools to look busy; never say tool names out loud.

What is **not** in that path:

- **AI Orchestrator** — `AIOrchestrator.run(intent)` is a facade for voice/learning/adaptive/knowledge/agents. Architected. Not invoked from `my_agent`.
- **Learning Engine / Adaptive Engine (frontend)** — project analytics and advise. They do not generate the spoken line.
- **Search Platform** — `SearchService.search` fans out in-process. The hall tool is still `search_learning_knowledge`.
- **Knowledge Fabric** — projection over the same knowledge search. No extra retrieve step in `agent.py`.

If I published the stacked diagram from a platform slide as “how a sentence is made,” I would be describing architecture, not the worker.

Context in a session: LiveKit conversation plus `SessionMemoryLookup` (one background SQLite read, cached). Specialist visits get a sanitized `SpecialistContext` in userdata, not a pasted transcript. After handback, resume instructions tell the host not to greet again.

Recovery: specialist start retries once, then structured fallback to the host. Analytics start/complete is failure-isolated so a dashboard bug does not kill the room. Memory init failure logs and the worker still talks. I did not write a generic “reconnect the whole OS” engine.

---

## 4. Learning and knowledge features

### Consented memory — implemented

`lookup_user`, `save_user_memory`, `update_last_interaction`, `forget_user_memory`. SQLite `users` in `memory.db`. Consent must be true before save. Scores are not columns. Evidence: `memory/repository.py`, `test_forget_user_memory.py`, `test_memory.py`.

Why: a returning learner should not be a stranger, and a “Forget me” should not be theater.

### Knowledge search — implemented

`search_learning_knowledge` reads JSON (`english_basics.json`) through `knowledge.search`. Used for a factual grammar or pronunciation question, not for small talk. Empty list means “answer normally.” Evidence: `knowledge/tools.py`, `test_knowledge.py`.

### Exercises, scoring, recommendations — implemented

`get_next_exercise` (level, optional topic). Local JSON, optional HTTP with fallback and cooldown. `score_spoken_answer` is deterministic — no LLM judge. `recommend_next_practice` stays in the conversation. The prompt forbids saving scores to memory. Evidence: `tools/score_tool.py`, `test_recommendation.py`, `test_exercise_provider.py`.

### Learning Engine — architected (projection)

`buildLearningIntelligence` and `LearningService.snapshot` read analytics + memory. They do not teach. They do not write XP onto the user. Docs: `19_LEARNING_INTELLIGENCE.md`.

### Adaptive Engine — architected (advice)

Frontend adaptive **advises**. `AdaptiveService.decide` calls `SpecialistRouter`. The router still decides math versus host. Docs: `20_ADAPTIVE_LEARNING_ENGINE.md`. Tests: `test_ai_services.py` adaptive wrap.

### Knowledge Fabric / Memory Graph — architected

Fabric is a semantic view of the same search. Graph explores fabric. It must not write `memory.db`. No graph UI on `/`.

---

## 5. Search and automation features

### Search Platform — architected

`SearchService` / `DiscoveryService` (alias) hybrid-search knowledge, marketplace catalog, and agent manifests. One `SearchHit` contract. No vector database in compose. Hall learners do not open a search box on `/`. Evidence: `services/search.py`, `test_os_v1.py`.

### Automation Platform — architected

`AutomationService` is the only workflow engine. `WorkflowAutomationService` is the same class. Jobs are a catalog, not Kafka. Evidence: `services/automation.py`, `33_WORKFLOW_AUTOMATION_PLATFORM.md`.

### Marketplace / plugins — architected (catalog only)

Seed catalog. `may_execute()` is `False`. Verified is not runnable. Evidence: `services/marketplace.py`, `test_extensibility.py`.

### AI Studio / Whiteboard — architected

Commands and canvas models. No editor. No renderer. Not mounted on the hall.

### SDK / public API — architected

`ApiEnvelope` v1. Tokens via existing service. Portal UI false.

### Collaboration — architected

Presence contract. `crdt` false. Voice stays on LiveKit.

---

## 6. Enterprise and security features

### Analytics dashboard — implemented

`/analytics`. Separate `analytics.db`. Outcomes, rates, filters, export. No transcript field. Evidence: `analytics/repository.py`, `test_analytics_bonuses.py`, CI privacy job.

### Enterprise control center — implemented (Day 9)

`/enterprise`. Orchestrator metadata, graphs, parent/teacher *builders*, health. Speech still forbidden. Later org records are in-memory. Evidence: `frontend/app/enterprise`, `enterprise/`.

### RBAC — implemented as a library, auth optional

`can(role, permission)` in `salora_platform.auth` and `lib/platform/rbac.ts`. Token route is rate-limited and CSRF-checked; it does not require a logged-in roster. `AUTH_REQUIRED` defaults false. That is a demo choice, not a locked campus.

### Privacy rules — implemented

No utterance columns. Event bus drops forbidden keys and long forbidden values. Observability redacts the same. Specialist logger discards extra kwargs (even if someone passes `transcript=`). Evidence: `services/events.py`, `salora_platform/observability.py`, `specialists/events.py`.

### Plugin and capability locks — implemented as denials

`may_execute` false. `may_autonomous_loop` false. HIPAA `ok: False`. Those are tests, not TODOs.

### Workspace Shell — architected / local UI

`OsShell` wraps routes. Command palette lists planned rooms and toasts. Hall stays voice. Feature flags exist; they are not all wired into nav.

---

## 7. Engineering design decisions

**One Voice Pipeline.** I already had Murf in the starter. Every extra mouth is a second personality and a second outage. Math is a guest. Telephony is a separate SIP path that does not replace the browser session.

**One SpecialistRouter.** Intent is deterministic. The Adaptive Engine may suggest. It does not get a second vote in production audio.

**One pair of databases.** Profile facts versus anonymous call ops. Joining them by learner id would rebuild the tape I refused.

**Facades, not forks.** Orchestrator, search, automation, runtime, registry — all consume `agent.py`, `knowledge.search`, or the specialist registry. I rejected a second event bus. The platform bus is in-process and capped. Specialist events are a small allow-list logger, not a competing bus.

**Provider registry as a list, not a swap.** Live adapters match env names already used by the worker. Future names register disabled. `agent.py` still constructs Deepgram, Gemini, and Murf. The registry does not hot-swap TTS mid-call.

**Events for modules, not for speech.** Publish names like `AssignmentSubmitted`. Field keys that look like `transcript` never land. I did not put the LiveKit audio path on that bus.

**Reuse.** Day 6 telephony, Day 7 escalation, Day 8 analytics, Day 9 specialists all leave `AgentSession` construction in one function. That is the maintainability argument. It is also why a blog should not describe ten platforms as ten runtimes.

---

## 8. Feature verification summary

| Capability | State | Evidence |
| --- | --- | --- |
| Live voice + LiveKit room | Implemented | `agent.py` `my_agent`; `app/api/token/route.ts` |
| Deepgram STT | Implemented | `deepgram.STT` nova-3 multi |
| Murf Falcon TTS | Implemented | `murf.TTS` Anisha; `test_ai_services.py` |
| Gemini + tools | Implemented | `AGENT_TOOLS`; `SYSTEM_PROMPT` |
| Memory + Forget Me | Implemented | `memory/`; `test_forget_user_memory.py` |
| Knowledge JSON | Implemented | `knowledge/tools.py`; `test_knowledge.py` |
| Exercise / score / recommend | Implemented | `tools/`; Day 5 tests |
| Math handoff | Implemented | `specialists/`; recovery/handback tests |
| Escalation | Implemented; notify partial | `escalation/`; notifier tests |
| Analytics + `/analytics` | Implemented | `analytics/`; bonus tests |
| `/enterprise` | Implemented | Day 9 enterprise package |
| Guardrails | Implemented (prompt + sanitizer) | `SYSTEM_PROMPT`; `test_escalation_sanitizer.py` |
| Multilingual | Implemented | prompt + Deepgram `multi` |
| RBAC | Implemented library; auth off by default | `salora_platform.auth`; `rbac.ts` |
| Workspace Shell | Local UI | `components/os/` |
| AI Orchestrator | Architected | `services/orchestrator.py` — not in `my_agent` |
| Agent Runtime | Architected host | `services/agent_runtime.py`; `may_autonomous_loop` false |
| Learning / Adaptive engines | Architected projections | `lib/learning`, `lib/adaptive`; router stays authority |
| Knowledge Fabric / Graph | Architected | docs 21, 26; no `/graph` |
| Search Platform | Architected | `services/search.py`; `test_os_v1.py` |
| Automation | Architected | `services/automation.py` |
| Marketplace execute | Denied | `may_execute` false |
| Studio / Whiteboard UI | Architected | no editor, no renderer |
| Custom interruption API | Not found | VAD + turn detector only |
| Published TTS benchmark | Not found | — |

Latency: I configured endpointing, preemptive generation, token cap, and `text_pacing=False`. I did not check in a millisecond number. Do not invent one.
