# 06 — AI Architecture Bible

How intelligence is wired in this repository.  
Law: [../salora/07-ai-system.md](../salora/07-ai-system.md), Master laws III–IV, IX, XI.

---

## AI philosophy

Intelligence is a teacher in a hall. A system that only answers is not in the teacher seat.  
Trust before capability. A model that restarts the person loses the seat.  
Humility is a capability: hedge, one question, offer a human, say I cannot.

## Agent architecture

| Seat | Code | Duty |
|---|---|---|
| Host | `Assistant` in `agent.py` | Relationship, greeting once, tools, refuse, escalation offer |
| Guest | e.g. `math_specialist.py` | Named subgraph, delta, way home |
| Router | `specialists/router.py` | Deterministic, confidence, clarification |
| Registry | `specialists/registry.py` | Enablement. Disabled is not “almost live” |

Same session. Same Murf voice family. `session.update_agent`.  
No guest-of-guest.

## Routing

Explainable. Confidence bands. One clarification. One retry. Fallback to host.  
Uncertainty asks one question. Do not improvise a second router in the LLM.

## Specialists

Math is live. English, Science, Reading, Writing, Grammar, Homework, Teacher (and later Career, Motivation) may register **disabled** until they have a curriculum subgraph and evaluation.  
A guest without a curriculum is a costume.

## Shared memory

`specialists/shared_context.py`, conversation state, read-only projection for the guest.  
Host accepts or rejects deltas. Guest cannot write unbounded memory.

## Context

Prefer structured state (item, last attempt, active guest) over raw history.  
Window full → licensed fields, not a secret diary.

## Tools

LiveKit `@function_tool` via `tools/livekit_tools.py`, registry, manager, validator.  
Closed, schema-checked. Tool failure is spoken as tool failure.  
Tools do not own the relationship.

## Knowledge

`knowledge/` search. Sources or item ids. Empty is empty.  
Do not invent a chapter.

## Reasoning

Gemini is the host LLM. Traces are not personality.  
Closed facts verify with tools (score, calculate). The mouth does not outrank a tool on a closed item.

## Safety

SYSTEM_PROMPT and tools: distress, crime, medical — stop the drill, offer a human.  
No clinician play. Child extra.  
Safety is not a feature flag.

## Fallbacks

Guest fail → host (`recovery.py`).  
Model fail → shorter host path or human offer.  
Voice fail → typed chat if present, else honest stop.  
Reconnect ≠ handoff.

## Escalation

`escalation/`: consent, reference id, webhook, PII sanitization, status.  
Optional resolution callback reuses telephony.  
Do not escalate by leaking a transcript to a dashboard.

## Conversation lifecycle

Start (host) → attempt → optional guest → handback → pause/end.  
Resume: same item, `resume_from_specialist` as designed. No new origin story.  
Outbound telephony: bootstrap EN + Hindi Devanagari, then the same host duty.

## Future multi-agent strategy

More named guests, each with registry, subgraph, eval, way home.  
Never a swarm in the mouth. Never a second pipeline.  
Never unique “soul colors” that change the host identity. A guest may be terser. The climate stays the host.

See [14 Naming Convention](14_NAMING_CONVENTION.md) for agent and tool ids.
