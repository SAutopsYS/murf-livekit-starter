# SALORA OS — Product Architecture

Phase 2.

The Constitution is what never changes.  
The Operating Standards are how teams execute.  
This file is how the product is organized.

Not visually.  
Not technically.  
Structurally.

Every feature, workflow, navigation pattern, learning experience, and future product must fit this architecture.  
If a new object cannot find a place here, it is not built.

---

# Volume I — Product Philosophy

## Why an operating system instead of an app

An app is a destination. A person opens it, uses a feature, leaves.

A learning operating system is the environment in which learning happens. Lessons, memory, teachers, parents, schools, and agents are processes running on one continuity. The person does not start over when they change a surface, a device, or a guest.

SALORA is an OS because the unit of value is not a session. The unit of value is a life of practice that does not require re-introduction.

## Product philosophy

The product exists to keep a learner on the line: the same relationship, the same licensed memory, the same next attempt.

Features are privileges granted to that continuity. They are not destinations that compete with it.

If a capability does not make the next attempt cheaper, clearer, or more honest, it does not belong in the OS.

## Learning as an operating system

Learning is the kernel. Voice, memory, assessment, school, and enterprise are subsystems.

The kernel decides:

- who is speaking
- what the current attempt is
- what may be remembered
- what happens when something fails

Subsystems may not replace the kernel. A dashboard may not become the lesson. A guest may not become the host.

## Continuous learning

Learning is not a streak of opened apps. It is a sequence of attempts with memory between them.

The OS treats yesterday’s miss as today’s first item when the license allows. It does not treat yesterday as a closed file.

Continuous does not mean always-on speech. It means the person can leave and return without being treated as a stranger.

## Sessions vs lifelong learning

A session is a bounded visit: start, work, pause or end.

Lifelong learning is the licensed record of skills, goals, and preferences that survive sessions.

The session may die. The person may not be reset.

A product that optimizes sessions and forgets the life is an app wearing OS language.

## Human-first architecture

A human is the subject. Agents, classrooms, and institutions are around the human.

When a school, a parent, and a tutor disagree, the learner’s safety and dignity are first. Then learning. Then the institution’s report.

No object in the taxonomy outranks the person it describes.

## Calm computing

The OS asks for attention only when the next attempt needs it.

Notifications, guests, and dashboards are quiet by default. Motion is a verb. Sound is the tutor’s voice, not a jingle.

Calm is not emptiness. Calm is the absence of competing primaries.

## Invisible intelligence

Intelligence is judged by the next item, the recovered session, and the honest hedge.

The person should feel taught, not impressed. A visible “thinking” costume is not a product requirement.

If the intelligence must announce itself to be believed, the teaching failed.

## Operating principles of SALORA

1. One host. Guests visit.
2. One attempt at a time.
3. One licensed memory, readable and erasable.
4. One way back that does not restart the person.
5. Fail toward the tutor, never toward a blank stranger.
6. Institutions see outcomes, not tapes.
7. Surfaces are rooms in one house, not separate products that forget each other.

---

# Volume II — Product Taxonomy

Nothing outside this taxonomy should exist as a first-class object.  
A feature may compose these objects. It may not invent a parallel vocabulary.

## People

**User**  
An authenticated or guest account. The legal and technical subject of consent.

**Learner**  
The person practicing. Every user who learns is a learner. A teacher may also be a learner.

**Teacher**  
A human with a professional relationship to one or more learners. Colleague, not spectator.

**Parent**  
A human with a care relationship. Sees time, topics, next step. Never a tape.

**Administrator**  
A human who operates a school or enterprise tenancy. Sees systems and aggregates.

**Researcher**  
A human under a study protocol. Never a silent role on a child’s session.

## Institutions

**Classroom**  
A named group of learners with one or more teachers. Has assignments, pulse, and risk — not utterance feeds.

**School**  
A tenancy of classrooms, teachers, and policy. Owns contract and retention for its members as allowed by law and consent.

**Enterprise**  
A tenancy above or beside schools: district, company, partner. Contracts and control, not learner speech.

## Learning objects

**Domain**  
A broad field (mathematics, language). Stable.

**Subject**  
A taught course-shaped slice of a domain (Class 8 Mathematics).

**Topic**  
A cluster inside a subject (linear equations).

**Concept**  
A single idea a person can be right or wrong about.

**Skill**  
An observable ability composed of concepts (solve a two-step equation aloud).

**Goal**  
A learner- or teacher-set aim with a time horizon (board exam; speak a paragraph).

**Lesson**  
A guided sequence toward a concept or skill. May be spoken.

**Practice**  
Repeated attempts at the edge of ability. Not a lecture.

**Assessment**  
A scored or judged sample of a skill class. Permanent records require a human path.

**Revision**  
Return to a forgotten or weak item after a gap.

**Reflection**  
A short metacognitive act after a set. Not during the try.

## Interaction objects

**Conversation**  
A bounded spoken or typed exchange inside a session. Not a stored tape by default.

**Session**  
A visit with start, pause, resume, end. See Volume X.

**Workspace**  
A room for one role’s job. See Volume VII.

**Resource**  
A licensed artifact: passage, problem, image, worksheet. Has a source.

**Notification**  
One fact, one optional action. Never a second tutor.

## Memory and knowledge

**Memory**  
A licensed structured record about a learner. Listed. Erasable. Not a transcript lake.

**Knowledge**  
Curriculum and resources the OS can retrieve. Cited. Not invented biography.

**Learning graph**  
Directed relations among concepts and skills (prerequisite, part-of, transfers-to).

## Agents

**Agent**  
A named intelligence with a role. Host or guest. Has identity, permissions, and a way home.

**Host**  
The tutor. Owns the relationship.

**Guest**  
A specialist. Named, tasked, returned.

**Tool**  
A closed capability an agent may call (score, retrieve, calculate). Not a person.

## Product containers

**Profile**  
The person’s visible and licensed self: language, accessibility, goals they chose to show.

**Settings**  
Controls for consent, devices, notifications, and preferences. Not a second product.

**Search index**  
A memory prosthetic over objects in this taxonomy. Not a new curriculum.

If a proposal needs a new noun, first prove an existing noun cannot hold it.

---

# Volume III — Information Architecture

## Product hierarchy

SALORA OS  
→ Home (orientation)  
→ Learning (attempt)  
→ Memory (licensed record)  
→ People rooms (Parent, Teacher, Classroom, School, Enterprise)  
→ System rooms (Search, Settings, Profile, Notifications)

Home orients. Learning attempts. Memory remembers. People rooms report. System rooms govern.

No fifth kind of top-level room.

## Navigation hierarchy

1. Where am I (workspace + mode)
2. What is the one primary
3. How do I go back without restart
4. How do I search if I forgot the map
5. How do I stop

Depth is allowed. Lostness is not.

## Learning hierarchy

Goal → Subject → Topic → Skill → Concept → Item (lesson / practice / assessment)

The person sees the current item and the reason it is next. They do not need the whole graph in their mouth.

## Knowledge hierarchy

Domain → Subject → Topic → Concept ↔ Skill  
Edges: prerequisite, part-of, related, transfers-to.

Knowledge is retrieved into an item. It is not dumped as a chapter during speech.

## Memory hierarchy

User consent  
→ Long-term licensed fields  
→ Shared projections (parent/teacher/school as allowed)  
→ Session state (dies unless promoted)  
→ Temporary working set (item, last attempt, active guest)

Lower layers cannot outlive higher consent.

## Search hierarchy

1. Continue current attempt
2. People and rooms the user may enter
3. Goals, subjects, topics
4. Resources
5. Settings and help

Search never outranks an open session without confirm.

## Settings hierarchy

1. Safety and consent
2. Memory and forget
3. Language and accessibility
4. Voice and devices
5. Notifications
6. People links (parent, teacher, school)
7. Account

Fashion and experiments sit last or not at all.

## Profile hierarchy

Who I am (name they chose, language, age band as required)  
What I am working on (goals)  
What I allow (memory, sharing)  
What I can leave (export, delete)

A profile is not a social page.

## Workspace hierarchy

Each workspace (Volume VII) contains:

- Orientation (where / who)
- Primary job surface
- Secondary instruments
- Settings slice for that role
- A path to the learner’s attempt when the role is allowed

Instruments never replace the attempt for the learner.

---

# Volume IV — User Journey Architecture

Every major journey has five acts: Entry, Progression, Completion, Exit, Recovery.

## First-time learner

**Entry** — Language, one permission that is needed now, a name they choose. No biography interview.  
**Progression** — One short attempt that produces something. Host, not a tour.  
**Completion** — They know what “next” means tomorrow.  
**Exit** — Leave without punishment. Memory only if licensed.  
**Recovery** — Return is “we can continue,” not “welcome, stranger.”

## Returning learner

**Entry** — Same host. Last licensed state. No new origin story.  
**Progression** — Next item from weakness or goal.  
**Completion** — A set ends with one reflection or one next time.  
**Exit** — Pause or end keeps the thread.  
**Recovery** — After crash or drop, same room, same item.

## Daily learner

**Entry** — Today’s one primary.  
**Progression** — Practice at the edge.  
**Completion** — Enough. Not a trap.  
**Exit** — Quiet.  
**Recovery** — Missed days do not become shame or a reset.

## Parent onboarding

**Entry** — Invite, relationship, what they will see and will not.  
**Progression** — First report they can repeat to another parent.  
**Completion** — They can find time, topic, next step.  
**Exit** — They can leave the console without leaving the child’s learning.  
**Recovery** — Broken invite is re-sent without exposing the child.

## Teacher onboarding

**Entry** — School or self, class, subjects.  
**Progression** — One class pulse, one assignment, one override.  
**Completion** — They can explain a student line in one breath.  
**Exit** — Class remains.  
**Recovery** — They can reclaim a guest the OS started.

## School onboarding

**Entry** — Contract, DPA, admin identity, retention.  
**Progression** — Roster, policy, first classroom.  
**Completion** — A teacher can teach without a second product.  
**Exit** — Export of what they are owed.  
**Recovery** — Failed roster import does not create ghost learners.

## Enterprise onboarding

**Entry** — Tenancy, roles, regions, data processing.  
**Progression** — Control plane: health, policy, aggregates.  
**Completion** — They can operate without learner speech.  
**Exit** — Offboarding deletes or returns as contracted.  
**Recovery** — Mis-scoped admin is revoked without touching lessons.

## Guest user

**Entry** — Learn now. Minimal identity.  
**Progression** — Session only. No silent long-term memory.  
**Completion** — Offer to keep a license, not a trap.  
**Exit** — Session dies.  
**Recovery** — If they later claim the session, only with proof and consent.

## Anonymous learning

**Entry** — Allowed where law allows.  
**Progression** — No profile, no share, no institution.  
**Completion** — Skill in the hour, not a dossier.  
**Exit** — Nothing to forget because nothing was kept.  
**Recovery** — Device change starts fresh unless they choose identity.

## Premium journey

**Entry** — A capability they already understand (more guests, more subjects, school tools).  
**Progression** — Continuity stays. Payment is not a new personality.  
**Completion** — The attempt is better, not louder.  
**Exit** — Downgrade keeps memory they licensed. Features leave; the person does not.  
**Recovery** — Failed payment does not lock a child out of a host that already knew them without a cruel wall. Policy is written, not improvised.

---

# Volume V — Learning Flow Architecture

Every learning feature must support this spine. A feature may start mid-spine. It may not invent a parallel spine.

Discover → Choose → Learn → Practice → Recall → Assess → Reflect → Improve → Master → Teach Others

**Discover** — What exists that matches a goal or a gap. Search and teacher assignment live here. Not a marketplace costume.

**Choose** — One next commitment. If two compete, neither is chosen.

**Learn** — First encoding. Short. Host or lesson. Ask before a speech when the goal is skill.

**Practice** — Attempts at the edge. Guests may enter for a skill and must leave.

**Recall** — Produce from memory after a gap. The OS does not re-lecture to look helpful.

**Assess** — Sample the class of skill. Score the attempt.

**Reflect** — What was hard. One beat.

**Improve** — Next item from the miss. Difficulty visible.

**Master** — Stable success across spaced items. A state, not a badge party.

**Teach Others** — Explanation to a peer, a younger learner, or a written proof. Optional. Never required to keep dignity.

A feature that only discovers and never practices is content, not the OS.  
A feature that only assesses and never improves is a test vendor.

---

# Volume VI — Navigation Architecture

## Primary navigation

The few rooms of the current workspace. Always: where I am, the attempt or the job, a way to Stop for learners.

Primary is not a junk drawer. If it needs nineteen siblings, the architecture failed.

## Secondary navigation

Instruments inside a room: timeline, memory list, class list. They do not steal the primary.

## Context navigation

Up one level. Back one step. Both must exist. Back does not mean restart.

## Deep links

A link may open a lesson, a class, a memory item, a setting.  
If a session is already live, the link asks before it replaces the attempt.

## Universal search

Recall without a map. Same hierarchy as Volume III. Confirm before leaving a live session.

## Command palette

Keyboard and power-user twin of search. Same objects. Same confirm rule.

## Voice navigation

Spoken commands that the host already understands: stop, help, repeat, slower, go back, I need a human.  
Voice navigation is not a second product. It is the host listening.

## Gesture navigation

Back, pause, skip only when the same actions exist as labeled controls. Gesture never becomes the only path.

## Keyboard navigation

Every primary and every commitment is reachable without a pointer. Order follows meaning, not visual fashion.

## Future navigation

New sensors (gaze, spatial) may point. They may not become required to learn. The host and the labeled path remain.

---

# Volume VII — Workspace Architecture

Each workspace exists for one purpose. If a workspace grows a second purpose, split it.

**Learner Workspace**  
Do the attempt. See the next item. Pause. Remember what was licensed.

**Teacher Workspace**  
Assign, see pulse and risk, override a guest, explain a line to a parent.

**Parent Workspace**  
See time, topics, completion, next step. Never a tape.

**School Workspace**  
Roster, policy, classrooms, retention, export.

**Enterprise Workspace**  
Tenancy, health, contracts, aggregates, control. No learner speech as a toy.

**Admin Workspace**  
Operate the OS: flags that are allowed, incidents, access. Not a secret lesson view.

**Research Workspace**  
Protocol, consent, de-identified or licensed study data. Separate from product analytics vanity.

**AI Workspace**  
Operators inspect routing, guest health, evaluation scores. Traces without tapes. Not a learner room.

A person may hold several roles. They switch workspaces. The learner’s session does not become a dashboard because the same human is also a teacher.

---

# Volume VIII — Knowledge Architecture

Knowledge is what can be taught. Memory is what was licensed about a person. They do not share a bucket.

**Subjects** — Taught containers with a syllabus shape.  
**Domains** — Stable fields above subjects.  
**Topics** — Clusters.  
**Concepts** — Atomic ideas.  
**Skills** — Observable performances.  
**Dependencies** — Prerequisite and part-of edges.  
**Learning graphs** — The map used by the planner. Not shown as a poster during speech.  
**Prerequisites** — Must be true enough before a new skill. “Enough” is defined per skill, not by mood.  
**Mastery paths** — Spaced sequences from first encoding to stable transfer. Paths can be assigned. They cannot shame.

A guest without a curriculum subgraph is not a guest. It is a costume.

---

# Volume IX — Learning State Architecture

A skill or item for a learner is in exactly one primary state. Secondary flags (offline, guest-active) are not substitutes.

| State | Meaning |
|---|---|
| Not Started | No licensed attempt |
| Started | Opened, not yet a real try |
| Learning | First encoding in progress |
| Practicing | Repeated attempts at the edge |
| Needs Revision | Weak or due for spacing |
| Forgotten | Once held, now failed recall |
| Recovering | After miss, drop, or fail-closed; same thread |
| Mastered | Stable across spaced transfer items |
| Teaching | Learner explaining to another |
| Archived | Removed from the active path; not deleted from history they own |

Forgotten is not shame. It is a scheduling fact.  
Mastered is not a forever trophy. It can return to Needs Revision.

The OS may not invent states like “engaged” or “delighted” as learning states.

---

# Volume X — Session Architecture

A session is a visit. It is not the person.

**Start** — Host present. Last licensed thread offered. Permissions only as needed.  
**Pause** — State kept. No new hello on resume.  
**Resume** — Same item, same guest rule, same voice family.  
**Switch** — Change of skill or guest goes through the host. Confirm if the current attempt is live.  
**Continue** — After a planned gap (next day). Lifelong memory, new session object.  
**Interruptions** — Barge-in for Stop, Help, safety. Not for our eagerness.  
**Recovery** — Drop, crash, failed guest: last good state, host, no restart.  
**Multi-device continuation** — The attempt is the person’s, not the device’s. One live session. A second device asks to take over; it does not fork two tutors.  
**Background mode** — Audio may continue only if the person chose it and can still Stop. A hidden session is not a spy.

Reconnect is not handoff. Handoff is a named guest. Reconnect is the same room after a break in the pipe.

---

# Volume XI — Memory Architecture

Product memory is licensed structure. Not a diary we refuse to show.

**Session memory** — Current item, last attempt, active guest, short working set. Dies with the session unless promoted.  
**Learning memory** — States from Volume IX, last scores of a class, due dates for spacing.  
**AI memory** — Projection the host or guest may read. Cannot exceed license. Guest writes a delta the host accepts.  
**User preferences** — Language, pace, accessibility, notification quiet. Not inferences they did not grant.  
**Long-term memory** — Listed fields. Human-readable. Erasable.  
**Temporary memory** — Caches and device drafts. Expire. Never a secret second profile.  
**Shared memory** — Projections to parent, teacher, school. Outcomes, not utterances. Revocable.  
**Deleted memory** — Forget completes in the product they use. Tombstones may exist for audit, not for teaching.

The product may not remember a fact it was not given.

---

# Volume XII — Feature Architecture

Features are organized by duty, not by team slogan.

**Core Features** — Host, session continuity, licensed memory, stop, language, forget.  
**Learning Features** — Lesson, practice, recall, spacing, goals, graphs as used by the planner.  
**Communication Features** — Voice, typed path, teacher messages that are not tapes, translation as a tool.  
**Assessment Features** — Items, scoring tools, human review path, reports without feeds.  
**Productivity Features** — Search, command palette, planning, calendar of due revisions. Never a second OS.  
**AI Features** — Host, guests, planner, tools, evaluation scores for operators.  
**School Features** — Classroom, assignment, pulse, override.  
**Parent Features** — Time, topic, next step, rare safety alert.  
**Admin Features** — Tenancy, policy, access, incidents.  
**Developer Features** — Documented extension points that cannot break host, consent, or fail-closed.  
**Experimental Features** — Flagged, reversible, never on safety, forget, or child records.

A feature names its category or it is not scheduled.

---

# Volume XIII — Cross-Platform Architecture

One identity. One memory license. One host.

| Environment | What it must keep | What it may drop |
|---|---|---|
| Mobile | Attempt, stop, voice, back | Dense instruments |
| Tablet | Attempt plus light teacher/parent | Enterprise density |
| Desktop | Full instruments for the role | Nothing that mobile needed to learn |
| Web | Same OS, not a marketing site wearing lessons | Native sensors |
| Watch | Pause, next, stop, glance of due | Teaching |
| Vision | Spatial pointing as optional | Required face or gaze |
| Voice-only | Full host path | Visual hierarchy |
| Automotive | Safety first; short; stop | Deep practice |
| TV | Shared room; large type; no secrets on screen | Personal memory edit |
| Future | Labeled path + host | Any required new sensor |

If a platform cannot fail toward the host, it does not offer guests.

---

# Volume XIV — Feature Lifecycle

Idea → Research → Prototype → Validation → Pilot → Internal Release → Beta → Public Release → Improvement → Mature → Deprecated → Retired

**Idea** — Names the taxonomy object and the learning-flow step.  
**Research** — Operating Standards Volume V. Harm analysis first.  
**Prototype** — Tests continuity and fail-closed, not costume.  
**Validation** — Observation plus numbers. A restart-shame story can kill it.  
**Pilot** — Contract, consent, teacher partner.  
**Internal Release** — Employees as learners, not as marketers.  
**Beta** — Limits, known absences spoken.  
**Public Release** — Scorecard and reviews passed.  
**Improvement** — Spaced return of the feature’s own defects.  
**Mature** — Ownership, docs, evaluation.  
**Deprecated** — Replacement named. Continuity preserved.  
**Retired** — Data path closed. Memory they own is exported or deleted as promised.

Skipping Pilot for a child-facing guest is not allowed.

---

# Volume XV — Product Evolution

**Adding features** — They occupy a taxonomy noun, a workspace, a flow step, and a lifecycle stage. They do not add a second host.

**Removing features** — Ask: if removed, is the attempt worse? If no, remove. Memory and stop cannot be removed.

**Merging products** — One host, one license, one identity. A merged product that restarts the person has failed the merge.

**Splitting products** — Allowed when a workspace’s purpose split. Identity and memory remain one OS.

**Platform evolution** — New devices inherit Volume XIII. They do not fork the kernel.

**AI evolution** — New models sit in host or guest seats after evaluation. They do not rewrite the relationship.

**Education evolution** — New subjects are graphs and items. They are not a new personality.

**Long-term compatibility** — A learner from a decade ago can return: same dignity, licensed memory they still allow, no stranger greeting. File formats and models may change. The person may not be discarded.

If the OS grows and the attempt gets more expensive, the evolution is wrong.
