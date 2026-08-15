# 01 — Product Bible

SALORA AI builds **SALORA OS**: the world's first AI Learning Operating System.

This file is product law for engineers and designers.  
Strategy handbooks: [../salora/02-product-blueprint.md](../salora/02-product-blueprint.md), [../salora/00-master-constitution.md](../salora/00-master-constitution.md).

---

## Vision

A person can practice by voice, leave, and return without being treated as a stranger. The OS keeps the host, the licensed memory, and the next attempt. Dashboards and guests serve that thread. They do not replace it.

## Mission

Keep the learner on the line. Ship a voice-first hall that teaches, fails toward the tutor, and forgets what it was not given.

## Product philosophy

We are not a chatbot with a waveform.  
We are not a dashboard that happens to have a mic.  
We are an operating system for learning: session, memory, specialists, school, parent, and enterprise are rooms in one house.

Code that does not make the next attempt cheaper, clearer, or more honest waits.

## Core principles

1. One host. Guests visit and leave.
2. One voice path (LiveKit + Murf Falcon). No second pipeline.
3. Resume is not a new hello. Reconnect is not handoff.
4. Memory is licensed, listed, and erasable.
5. No default tape. Analytics never store utterances.
6. Fail toward the tutor. One retry. No loops.
7. Hindi is Devanagari, never default Roman.
8. Teacher override stands. The learner may stop.
9. Trust and Learning cannot score zero on a ship.
10. Reuse the working system. Evolve. Do not rewrite the kernel.

## User personas

| Persona | Job in the hall | Must never see |
|---|---|---|
| Learner | Attempt, stop, return | A stranger greeting, a rank, a tape of themselves |
| Parent | Time, topic, next step | Utterances, a warden UI |
| Teacher | Assign, pulse, override | Gossip view, silent observe |
| School / enterprise admin | Health, policy, aggregates | Learner speech as a toy |
| Operator | Route, fail-closed, forget | Prompt bodies in logs |

## Long-term vision

More subjects as named guests with curricula. More rooms (teacher, parent, school) on one identity. More devices that inherit the host. Never a marketplace of souls. Never a second kernel.

## Product pillars

| Pillar | In this repo today |
|---|---|
| Voice hall | `frontend` session + `backend/src/agent.py` |
| Memory | `backend/src/memory/` consent + Forget Me |
| Knowledge & tools | `backend/src/knowledge/`, `backend/src/tools/` |
| Specialists | `backend/src/specialists/` — Math live |
| Continuity beyond the browser | Telephony, escalation |
| Instruments | `/analytics`, `/enterprise` |

Instruments never outrank the attempt.

## Success metrics

Measure: first useful audio, fail-closed rate, forget completion, resume without new hello, transfer/retention when the learning engine lands, privacy-safe event volume.

Do not measure: time trapped, streak fear, watch-through as mastery, public rank.

## Roadmap philosophy

[IMPLEMENTATION.md](../salora/IMPLEMENTATION.md): one milestone, app still talks, tests still run.  
Phase 2 is the design system on existing components. Not a new product.

## Decision framework

Before a change:

1. Which Master law applies?
2. Does this reuse a working module?
3. What is the fail-toward-host path?
4. Is a new field licensed? Could a mouth hide in it?
5. If removed, is the attempt worse?
6. Who owns 3 a.m.?

“We’ll fix trust later” is a failed decision.

See also: [09 Git Workflow](09_GIT_WORKFLOW.md) PR checklist.
