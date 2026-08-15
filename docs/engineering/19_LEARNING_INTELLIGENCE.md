# 19 — Learning Intelligence

The permanent learning engine for SALORA OS.  
UI consumes it. Voice does not own it. Analytics is not rewritten.

Voice: [17 Voice Architecture](17_VOICE_ARCHITECTURE.md).  
OS: [16 Workspace Architecture](16_WORKSPACE_ARCHITECTURE.md).  
Memory law: consent, no utterance column, scores stay conversation-scoped.

---

## Decision

Learning intelligence is a **projection**.

| Store | Job |
|---|---|
| `memory.db` `User` | Consented profile. Tutor writes. Specialists read. |
| `analytics.db` `CallAnalyticsRecord` | Anonymous call ops. No `user_id`. |
| Session `SpecialistContext` / `ConversationState` | In-RAM. No transcripts. |
| `buildLearningIntelligence` | Frontend engine. Derives profile, skills, insights, recs, goals, timeline. |

Do not join memory and analytics by identity.  
Do not persist scores into `User`.  
Do not mount `LearningProvider` on the hall.

---

## Architecture

```
Existing APIs          Engine                         Consumers
/api/analytics    →    adaptInstruments()        →    useLearning()
/api/enterprise   →    buildLearningIntelligence →    LearningInsightList
memory User       →    mergeMemoryUser()         →    future /learning
recommend_next_*  →    RecommendationKind reuse  →    future missions
```

| Module | Path |
|---|---|
| Types | `frontend/lib/learning/types.ts` |
| Engine | `frontend/lib/learning/engine.ts` |
| Adapters | `frontend/lib/learning/adapters.ts` |
| Skills | `frontend/lib/learning/skills.ts` |
| States | `frontend/lib/learning/states.ts` |
| Events | `frontend/lib/learning/events.ts` |
| Provider | `frontend/components/learning/learning-provider.tsx` |

`LearningProvider` `autoload` defaults **false**. Instruments may pass snapshots. The hall must not poll this.

---

## Learner profile

Extends the meaning of `User` without a second table.

`preferredLanguage`, `currentLevel`, `grammarLevel`, `confidence`, `interests` ← memory / enterprise.  
`strengths` / `weaknesses` ← parent + heatmap + memory graph nodes.  
`streak`, `progressScore`, skill slots ← projected metrics.  
`learnerRef` is `aggregate` until a consented memory adapter is passed. Never a raw user id in analytics.

---

## Skill model

Catalog: speaking, listening, reading, writing, vocabulary, grammar, reasoning, problem solving, math (+ topic children), coding, career, interview.

Each skill: id, title, description, category, difficulty, mastery, confidence, practiceCount, lastPracticed, trend, related, dependencies.

Mastery is **null** unless enterprise heatmap supplies a number. Do not invent 87%.

---

## Knowledge model

Kinds: concept, topic, lesson, exercise, question, answer, correction, insight, recommendation, weakness, strength, mistake, achievement, revision.

These are structured objects, not chat logs. Achievement exists as a kind. There is no achievement UI.

---

## Learning state

`new | active | practicing | reviewing | paused | completed | needs_review | recommended | archived`

Each exposes label, meaning, priority, color token, icon token.  
`getLearningVisual(phase)`.

---

## Insights

Kinds: strength, weakness, recommendation, prediction, improvement, reminder, risk, celebration, trend.

Projected today from weak/strong topics, analytics summary sentence, streak, empty-hall reminder.  
`InsightCard` already exists. `LearningInsightList` consumes it.

---

## Recommendations

Kinds include conversation, practice, revision, plus backend `repeat_same_level | continue_same_level | advance_level`.

Reason and confidence are required. Recs are conversation-law: they do not write memory.

---

## Goals

Horizon + status + progress + deadline + priority.  
Today: topic counts become open weekly goals. Not XP. Not missions.

---

## Timeline

Events from `recent_calls` and `journey.steps`. Architecture only. No fancy viz.

---

## Metrics

Learning time, speaking time, completion, retention (null), confidence (null), consistency, response quality (null), latency, participation, practice frequency.

Reuse analytics duration / success and enterprise voice / parent. Do not redesign `/analytics`.

---

## Events

`useLearningActions().subscribe`.  
LessonStarted/Completed, GoalCreated/Updated, RecommendationGenerated, InsightCreated, SkillImproved, ReviewRequested, TimelineUpdated, ConversationFinished, ProfileUpdated.

Bus is a ref Set. No extra renders.

---

## Accessibility

`LearningStateLabel` and insight list expose `aria-label` / `sr-only` meaning.  
Tokens follow pulse / warning / success. Color is not the only signal.  
Reduced motion: no new animation in this layer.

---

## Performance

Engine is a pure function. Snapshot memoized.  
Do not put this provider in `App`. Voice FFT and LiveKit stay untouched.

---

## Future plugs (do not build here)

| Feature | How it plugs |
|---|---|
| Missions / XP / achievements UI | New consumers. Same goals/insights. No shame. |
| Memory graph viz | Reads knowledge + skills. Does not store utterances. |
| Study planner / flashcards | Recommendations + skills. |
| AI Studio / coaches | Same profile. Guests stay read-only on memory. |
| Parent / teacher dashboards | Already have snapshot keys. Engine projects; do not fork those pages. |

`/learning` stays planned in `os-nav` until a page consumes `LearningProvider`.
