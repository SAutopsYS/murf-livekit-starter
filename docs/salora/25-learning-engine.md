# SALORA OS — Learning Engine Blueprint

Stage C.

The Constitution is why learning exists.  
The Product Blueprint is where it happens.  
The AI System is who teaches.  
The Knowledge System is what is learned.  
The Assessment System is how mastery is measured.  
The Content System is how resources are authored.

This file is how learning executes in software.

Not curriculum writing.  
Not lesson planning.  
Not educational theory.

The permanent Learning Engine Implementation Blueprint.  
Every engineer and learning scientist reads this before implementing a learning function.

Stage B is the shared platform (identity, org, comms, search).  
This engine is a **domain** on that platform. It does not mint a second user, a second notifier, or a second file store.

Voice (`services/voice`) is a client of this engine: it asks for the next move, reports an attempt outcome (class + result, not the spoken words), and fails toward the host. It does not become a second curriculum database.

If a learning feature cannot name the service, the graph object, the state transition, and the evidence it writes, it is not implemented.

---

# Volume I — Learning Engine Philosophy

**Learning-first engineering**  
The unit of work is an attempt on a class of skill. Pages, videos, and guests are delivery.

**Mastery before completion**  
A `completed` flag without transfer and retention is a lie we do not persist as mastery.

**Practice over passive consumption**  
A watch-through without produce is not a completion we count as learning (Content analytics).

**Progress through evidence**  
Writes are item ids, results, levels, dues. Not vibes. Not “engagement.”

**Educational integrity**  
When the goal is their skill, we do not submit as them. Official records need a human path.

**Adaptive without manipulation**  
Next item and schedule change. Truth and identity do not. No streak as love.

**Human-centered learning systems**  
Teacher override stands. Learner may stop. Enough is valid.

**Explainable learning decisions**  
An operator or teacher can see why this id was next (prerequisite, due, last miss, assignment). “The embedding liked it” is not an explanation we ship.

**Long-term maintainability**  
States and edges are the API. A new practice type is a strategy behind the Practice service, not a new soul.

**Learning as infrastructure**  
Other products call this engine. They do not reimplement spacing in a feature flag.

---

# Volume II — Curriculum Engine

Implements Learning System Volume III and Knowledge bindings.

**Objects** — Domain, subject, course, unit, module, lesson, objective, competency, path. Each has an id, version, locale, `presents` targets.

**Relationships** — `contains`, `presents`, `requires`, `next` (default only), `assessed-by`. Planner may override `next` within prerequisite law.

**Versioning** — Pin in live paths. Mid-try text swap forbidden without a written rule. `supersedes` keeps history for credentials.

**API shape** — Read a path, resolve a lesson for a locale and twin (voice/type). No “generate a course” endpoint that publishes.

AI may draft offline. Publish remains human (Content governance).

---

# Volume III — Lesson Engine

Every lesson follows one execution pipeline. Content Volume III is the spine. This is the runtime.

**Lesson runtime** — A `LessonVisit` (platform session pointer + engine state): objective id, stage, item id, scaffolds, guest id if any.

**Lesson flow**

```
objective → context → introduction → concept → example
→ guided_practice → independent_practice → reflection
→ recall? → check? → summary → next
```

A path may skip a stage already satisfied (diagnostic “enough”). It may not invent a hook/payoff spine.

**Learning states** — Product Architecture states on the skill/item: Not Started → … → Mastered / Archived. The visit has a stage. The class has a state. Do not mix them.

**Checkpoints** — Stage boundaries. Resume returns to the stage, not to a new hello.

**Examples / guided / independent** — Item ids. Guided allows one hint. Independent fades.

**Reflection / recall / summary / next** — Reflection Engine and Recommendation Service. Summary is facts, not a character sketch.

Voice maps stages to spoken turns. The engine still owns the stage machine. The worker does not invent a parallel flow.

---

# Volume IV — Practice Engine

Practice is the kernel. Scheduling is a function, not a mood.

**Active recall / retrieval** — Prompt before reveal. If reveal-first, it is content, not practice.

**Spaced repetition** — Due from Forgotten and Needs Revision (Cepeda). Streaks do not drive the scheduler.

**Interleaving** — After encoding, mix related classes. Not on minute one of a new idea.

**Adaptive / mixed / scenario** — Smaller isomorphic on miss; transfer when stable; scenarios for soft apply. One primary.

**Coding / mathematics / writing** — Same engine, different tools. Tools verify closed parts. They do not steal the try when the skill is the produce.

**Reflection practice** — After the set. Stored only if licensed.

**Scheduler inputs** — Last result, state, due, assignment, teacher override, “enough.”  
**Scheduler output** — One next item id and why (explainable).

No random “keep them busy” queue.

---

# Volume V — Assessment Engine

Implements Assessment System in software.

**Diagnostics / placement** — Short. Placement reversible. Teacher may override.

**Formative** — Default. Writes evidence for the Planner. Does not enter official record unless `promotes-to` and a human rule.

**Summative / competency / projects** — Disclosed. `samples` + `contains`. Rubric before open items.

**Rubrics** — Published. AI may draft application. Human owns official.

**AI-supported evaluation** — Closed items by tools. Open items draft only for children and official records.

**Human review / certification / appeals** — Required flags on the record. Examiner seat may run the session. It does not own the record.

**Writes** — Sample id, class, item ids, outcome, context (language, drop). Not the oral blob.

---

# Volume VI — Mastery Engine

Mastery is continuously updated. It can decay.

**Competency / skill levels** — Beginner → Developing → Proficient → Advanced → Expert, plus Maintenance, Regression, Recovery (Assessment Volume IV).

**Confidence** — Optional stated confidence vs accuracy. Calibration is the measure.

**Retention / transfer** — First-class inputs. Expert cannot be minted without them.

**Regression / recovery** — Failed spaced transfer → Regression → Recovering (same thread, smaller demand).

**Long-term maintenance** — Scheduled return while Mastered.

**Thresholds** — Written “enough” per class. Teachers and experts set. AI may simulate; it does not set.

**Recommendation** — Consumes levels and dues. Does not write vanity.

A score may inform a transition. A score may not skip transfer and retention.

---

# Volume VII — Progress Engine

Progress measures learning, never vanity.

**Learning timeline** — Visits and samples as events (ids, stages, outcomes). No utterances.

**Progress graph** — View of states and levels. Empty is drawn.

**Milestones** — Optional, local, tied to a real sample. Absence does not shame.

**Goals** — From Goal Engine.

**Practice history** — Item ids, results, hints used, transfer flag.

**Competency growth / velocity** — Change across spaced samples, not items per minute.

**Retention history** — Recall after gaps.

**Streak logic** — If it exists, it serves spacing (“you have a due”). It does not threaten. It is not a learning state.

**Completion quality** — Produce happened. Watch-through alone is not quality.

No leaderboard table. No “engagement score” column.

---

# Volume VIII — Personalization Engine

Personalization changes delivery, never truth.

**Difficulty / pace** — Edge of ability. Enough is valid. Visible.

**Weakness / strength** — From attempts. Named as a class. Shown to them and, if granted, to a teacher.

**Revision scheduling** — Practice Engine dues.

**Recommendation pipeline**

```
assignments + dues + last miss + prerequisite enough + override
→ one item id + reason code
```

**Preferences** — From User Platform (language, accessibility, voice/type).

**Human override** — Teacher assign/skip/lock/pull guest. OS does not sulk. Parent does not silently rewrite a teacher’s assignment.

**AI collaboration** — Planner seat may propose. Engine validates against graph and override. A model cannot publish a new objective.

No second graph of “their physics.”

---

# Volume IX — Learning Graph Engine

Neo4j (or equivalent) holds typed edges. Postgres holds states and evidence. They do not share a mouth.

**Knowledge dependencies / skill / competency graphs** — Knowledge System edges.

**Learning paths** — Sequences of lesson/objective ids.

**Cross-domain links** — Typed only.

**Mastery / recommendation / goal / progress / evidence graphs** — Projections for traversal, not posters in the lesson.

**Traversal**

- Next practice: due ∪ assigned ∪ prerequisite-satisfied neighbors.  
- Skip: diagnostic enough or teacher override.  
- Forbid: retired, no evidence, wrong age, cycle in `prerequisite`.

Cycles in `prerequisite` are defects (CI check).  
Retrieval/search (Stage B) may suggest candidates. This engine forbids illegal ones.

---

# Volume X — Reflection Engine

Reflection closes a meaningful cycle. During the try, no journal.

**Prompts** — One beat. Bound to the set. Language System.

**Self-assessment / confidence** — Optional. Used for calibration, not shame.

**Learning journals** — Only if they chose and licensed. Erasable. Not a required essay in the mouth.

**AI Reflection Coach** — One question. Stops. No invented biography.

**Human reflection** — Teacher conference notes are outcomes, not quotes.

**Error review** — Last misses of a class. Produce again or smaller item.

**Goal updates / metacognition / insights** — Short. Stored as structured fields if licensed (“hard step = fraction add”), not as a paragraph we mine.

---

# Volume XI — Goal Engine

Goals guide. They do not pressure.

**Types** — Learning, weekly, long-term, competency, career (older, requested), revision.

**Tracking / completion / adaptation** — They may change or abandon without shame.

**Human override** — Learner and teacher. Parent may suggest if sharing granted.

Exam dates they gave may tighten dues. Stop remains.  
The engine does not invent a life plan.  
Career goals do not write a child dossier.

---

# Volume XII — Learning Analytics Engine

Analytics improve learning. They never rank learners.

**Measures** — Mastery growth (including decay), knowledge gaps, retention, practice quality, calibration, velocity, goal progress, competency distribution (class-scoped for a teacher), transfer, effectiveness of an asset.

**Writes** — Aggregates and teacher-scoped distributions. No public histogram of named children.

**Reads** — Planner, teacher dashboard, research plane (protocol).

**Forbidden** — Engagement-as-moral, leaderboards, utterance features, “hardest working student.”

A metric that rises while dignity falls is retired.

---

# Volume XIII — Learning Services

Bounded contexts inside the domain (Nest modules or equivalent). One purpose. One owner. One primary store.

| Service | Owns | Must not |
|---|---|---|
| Curriculum | Paths, versions, bindings | Publish without human; live mid-try swap |
| Lesson | Visit stage machine | A second voice pipeline |
| Practice | Items in play, scheduler | Streak threats; random busywork |
| Assessment | Samples, official flags | Oral blobs; tool-only child records |
| Mastery | Levels, decay, thresholds | Mint Expert without transfer/retention |
| Progress | Timeline, quality | Vanity scores |
| Recommendation | One next id + reason | Own truth; ignore override |
| Reflection | Prompts, licensed notes | Journals as required exams |
| Goal | Goals they set | Invented life plans |
| Analytics | Aggregates, gaps | Rankings; mouths |

Voice worker is a caller, not a member of this table.  
Shared platform (Stage B) is not reimplemented here.

---

# Volume XIV — Learning APIs

Contracts in `packages/contracts`. Versioned. No utterance fields.

**Curriculum** — `GET` path/lesson/twins. `POST` only for governed authoring tools.

**Lesson** — `start`, `resume`, `advance_stage`, `end`. Resume does not greet.

**Practice** — `next` (returns item + reason), `submit_result` (class, result, hint_used, transfer_flag).

**Assessment** — `start_sample` (discloses type), `submit`, `appeal`. Official requires reviewer id.

**Progress / mastery** — Read states and levels. Writes only through practice/assessment.

**Reflection / goals** — Create/update licensed shorts. Delete honors forget.

**Recommendation** — `next` is the only write-adjacent call; it writes an explanation id, not a new curriculum node.

**Analytics** — Teacher/operator reads. No child-export of raw attempts as speech.

**Events** — `VisitResumed`, `StageAdvanced`, `ResultRecorded`, `LevelChanged`, `DueScheduled`, `OverrideApplied`, `SampleDisclosed`. Ids and enums. No text of answers.

Idempotency on `submit_result` so sync does not double the attempt.

---

# Volume XV — Learning Engine Manifesto

Software exists to enable learning, not to deliver content.

A CMS can ship a video. An engine must ship a try, a miss, a smaller try, a gap, and a later item of the same class. If we only deliver content, we have built a store and taught the voice to be a waiter.

Practice is more valuable than passive consumption because the mind changes when it produces. We will count produce. We will not count a finished progress bar as mastery.

Mastery matters more than completion because the world will not present the identical screen. Completion is a courtesy to a calendar. Mastery is a promise about a later hour. The engine stores the promise only when transfer and retention have spoken.

Reflection is part of every educational journey and a thief if it happens during the try. We will ask one question after the set. We will not turn a tired mouth into a journal product.

Learning systems must remain transparent and explainable. A next item without a reason code is a mood. A teacher who cannot see why is not a colleague. We will keep the reason next to the id.

What must never change, even when models, graphs, and runtimes change:

One lesson pipeline.  
One next item, with a reason.  
States on the class, stages on the visit.  
Mastery that can decay.  
Teacher override.  
Stop and enough.  
Results without mouths.  
Search and embeddings may suggest; the graph may forbid.  
Voice is a client of this engine, not a second curriculum.

The hall has a clock, a graph, and a try.

If the engine is honest, a quiet tutor is enough.  
If the engine is a casino of streaks, no tutor can make it school.

Stay on the line.  
Advance the stage.  
Record the evidence.  
Recommend one thing.
