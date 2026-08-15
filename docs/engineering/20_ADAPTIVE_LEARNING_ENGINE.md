# 20 — Adaptive Learning Engine

The decision layer. It does not teach. It chooses the next lawful move.

Consumes [19 Learning Intelligence](19_LEARNING_INTELLIGENCE.md).  
Does not replace the backend specialist router.  
Does not mount on the hall.

---

## Decision

`buildAdaptiveSnapshot(intelligence)` is the only decider on the frontend.  
Live routing still happens in `SpecialistRouter`. This engine **advises**.

---

## Architecture

```
LearningIntelligence → AdaptiveEngine → AdaptiveSnapshot
                         ├ decision + alternatives
                         ├ mastery[]
                         ├ revision[]
                         ├ specialist advice
                         └ predictions
```

| Module | Path |
|---|---|
| Engine | `frontend/lib/adaptive/engine.ts` |
| Policies | `frontend/lib/adaptive/policies.ts` |
| Mastery | `frontend/lib/adaptive/mastery.ts` |
| Revision | `frontend/lib/adaptive/revision.ts` |
| Prediction | `frontend/lib/adaptive/prediction.ts` |
| Routing advice | `frontend/lib/adaptive/routing.ts` |
| Provider | `frontend/components/adaptive/adaptive-provider.tsx` |

`AdaptiveProvider` takes `intelligence` as a prop. No fetch. No voice wrap.

---

## Decision flow

Actions: continue, pause, repeat, revise, challenge, advance, escalate, simplify, practice, assess, review, recommend_specialist, recommend_human.

Each decision: reason, confidence, priority, explanation, timestamp, relatedSkillIds.

Policy inputs: confidence, consistency, latency, response quality, recent failures/successes, attention, velocity, weaknesses, phase.

Default: **continue / stay with tutor**. Fail toward the host.

---

## Mastery model

unknown → learning → emerging → practicing → confident → mastered  
plus forgotten, regression, needs_review.

Derived from skill practiceCount / mastery / trend. Null mastery stays unknown. No fake 87%.

---

## Revision engine

Queue kinds: spaced, weak, missed, queue, recommended.  
Built from weaknesses, mastery needs_review, and revision recs.  
Flashcards later consume this list. No UI here.

---

## Prediction engine

completionProbability, masteryForecast, dropOffRisk, reviewNeed, recommendedPracticeMinutes, expectedImprovement, learningVelocity.

All projected. Thin data stays low-confidence. Not a promise.

---

## Specialist advice

tutor (live), math (live), coding/career/interview/writing/language (registered, disabled).

Returns reason, confidence, urgency, expectedOutcome, `live` flag.  
Disabled guests never become a second mouth.

---

## Accessibility / performance

`AdaptiveDecisionSummary` exposes explanation to `sr-only`.  
Snapshot memoized from intelligence identity. No hall polling.

---

## Future plugs

Missions, flashcards, study planner, coaches, studio: call `buildAdaptiveSnapshot` or `useAdaptive()`.  
Do not write a second policy file.
