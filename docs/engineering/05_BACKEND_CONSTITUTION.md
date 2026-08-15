# 05 — Backend Constitution

Law for `backend/`.  
Stack: Python 3.10+, `uv`, LiveKit Agents, Murf Falcon, Deepgram, Gemini.

Entry: `backend/src/agent.py`.  
Do not replace the worker with a second voice server.

---

## Architecture principles

- One pipeline: STT → host/guest → TTS.  
- Modules own a data class. Memory is not analytics. Analytics is not a transcript store.  
- Deterministic routing for specialists (`specialists/router.py`).  
- Fail-closed: guest fail → host, one retry (`specialists/recovery.py`).  
- Privacy-safe logs: no transcripts, OTPs, phones, secrets.

## Module structure (current)

```
backend/src/
  agent.py              # host Assistant, session, Murf voice
  memory/               # consent, SQLite, Forget Me
  knowledge/            # searchable tips
  tools/                # exercises, scoring, registry, manager
  specialists/          # router, registry, math, handoff
  analytics/            # call outcomes, CLI
  enterprise/           # control-plane snapshot, CLI
  telephony/            # outbound SIP
  escalation/           # human help
```

New capability: new package under `src/` with `__init__.py`, tests under `backend/tests/`.  
Do not dump logic into `agent.py` beyond wiring.

## Services

A service is a class with one job (e.g. `TelephonyService`, analytics service).  
The worker calls services. Services do not import frontend.

## Repositories

SQLite repositories stay schema-stable unless a migration is written and privacy-reviewed.  
No `transcript` column. Ever.

## Agents

Host: `Assistant` in `agent.py`.  
Guests: registered in `specialists/registry.py`. Only enabled guests route.  
Same `AgentSession`. Same `murf.TTS(voice="Anisha")`. `session.update_agent`.  
Resume: `resume_from_specialist=True`.

## Memory

Licensed structured fields. Consent first. Forget completes in product tools.  
Specialists get a projection, not a diary.  
See [06 AI Architecture Bible](06_AI_ARCHITECTURE_BIBLE.md).

## Knowledge

JSON repository + `search_learning_knowledge`. Retrieval does not invent a citation.  
New packs follow [14 Naming Convention](14_NAMING_CONVENTION.md).

## Caching

Tool request cache, session exercise rotation, provider health cooldown.  
Never cache a transcript. Licensed memory cache dies with permission.

## Streaming

Audio streaming is LiveKit’s job. Do not add a parallel WebSocket of PCM.

## Feature flags

`telephony/features.py` pattern: explicit, default-safe.  
Safety, forget, and fail-closed are not optional in production.

## Logging

Event names, ids, error class, latency.  
`print` of user speech is an incident.

## Monitoring

Analytics and enterprise CLIs / Next `execFile` bridges.  
Health: host start, fail-closed, forget, guest retry. Not “engagement.”

## Security

[13 Security Standard](13_SECURITY_STANDARD.md).  
`.env` never committed. `.env.example` placeholders only.

## Testing

`uv run python -m pytest` from `backend/`.  
New tools and prompts: tests first, LLM-judge pattern where the suite already uses it.  
Required: fail-closed, handback, forget, privacy logs, no-restart when those paths change.

## Scalability

Worker concurrency is LiveKit’s. Do not scale a speech lake.  
School-day peaks: host fleet first.

## API design

Frontend talks to Next routes; Next may `execFile` Python CLIs.  
Payloads: smallest, no utterance fields, structured errors.  
Future Nest control plane (`services/api`) consumes the same contracts — it does not embed STT/TTS.

## Versioning

Guests, prompts, and content pin. “Latest” is not a pin.  
Python package: `pyproject.toml`. Ruff: 88 columns, double quotes.

See [08 Coding Standards](08_CODING_STANDARDS.md), [11 Testing Standard](11_TESTING_STANDARD.md).
