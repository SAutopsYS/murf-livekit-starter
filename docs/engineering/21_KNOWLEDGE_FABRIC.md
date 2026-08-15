# 21 — Knowledge Fabric

The memory layer remembers **understanding**, not chat.

Consumes [19 Learning Intelligence](19_LEARNING_INTELLIGENCE.md) and [20 Adaptive Engine](20_ADAPTIVE_LEARNING_ENGINE.md).  
Does not replace `memory.db` `User` or knowledge JSON search.  
Does not draw a graph.

---

## Decision

`buildKnowledgeFabric(intelligence, adaptive)` projects a node/edge snapshot.  
Long-term persist still requires consent and goes through existing memory tools.  
No utterance fields. Ever.

---

## Architecture

```
LearningIntelligence + AdaptiveSnapshot
        → KnowledgeFabricEngine
        → nodes / edges / retrieved
```

| Module | Path |
|---|---|
| Engine | `frontend/lib/knowledge-fabric/engine.ts` |
| Retrieval | `frontend/lib/knowledge-fabric/retrieval.ts` |
| Lifecycle | `frontend/lib/knowledge-fabric/lifecycle.ts` |
| Policies | `frontend/lib/knowledge-fabric/policies.ts` |
| Provider | `frontend/components/knowledge-fabric/knowledge-fabric-provider.tsx` |

---

## Memory model

Layers: working, short_term, long_term.  
Consented profile → long_term. Adaptive decision → working. Projected topics → short_term.

A node: id, type, title, summary, confidence, importance, layer, source, timestamps, ttl, verification, references.

Never a transcript. Never a spoken_answer.

---

## Objects

concept, entity, relationship, evidence, topic, lesson, rule, observation, correction, question, answer, decision, recommendation, skill, goal, fact, preference, weakness, strength, context.

---

## Relationships

depends_on, related_to, teaches, corrects, improves, contradicts, supports, derived_from, recommended_by, belongs_to.

Architecture only. Memory Graph UI later reads these edges.

---

## Lifecycle

strengthen, weaken, archive, forget, expire.  
Forget is a hard drop (matches memory forget). Archive lowers importance. Expire honors TTL.

---

## Retrieval

Keyword score + importance + layer boost. Same spirit as backend `knowledge/search.py`.  
Query: text, layer, type, limit. Agents consume `retrieved`.

---

## Events / policies

Events: Created, Updated, Merged, Strengthened, Expired, RelationshipCreated/Updated, Retrieved, Verified, Archived.

Policies: no utterances, consent for long-term, min confidence to verify, keep-higher-confidence on conflict, aggregate until consented.

---

## Accessibility / performance

`KnowledgeSummary` announces counts via `sr-only`.  
Memoized snapshot. Incremental lifecycle returns new objects. Do not mount on the hall.

---

## Future plugs

Memory Graph, whiteboard, notebook, flashcards, planner, studio, SDK: read `useKnowledgeFabric()` or `retrieveKnowledge`.  
Parent/teacher dashboards keep their snapshot keys. This fabric does not fork them.
