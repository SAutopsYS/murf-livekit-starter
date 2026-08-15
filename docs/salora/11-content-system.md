# SALORA OS — Content System Constitution

Phase 8.

The Constitution defines why learning exists.  
The Learning System defines how learning works.  
The Knowledge System defines what knowledge is.  
The Assessment System defines how learning is measured.

This file defines how educational content is designed, authored, validated, organized, delivered, maintained, localized, and evolved.

Not curriculum writing.  
Not lesson authoring.  
Not content-management software.

The permanent Content Architecture and Educational Content Constitution.  
Authors, instructional designers, researchers, content strategy, AI content engineering, localization, accessibility, editors, reviewers, teacher partners, and product follow this file.

Knowledge System Volume IV named that content is a presentation of knowledge objects.  
Learning System Volume III named courses, units, modules, and objectives.  
This file is the law of the presentation: how a lesson is built, how a format earns its keep, and who may publish.

If an asset cannot name its knowledge objects, its objective, its lesson stage, and its approval, it is not content in this OS. It is a file.

---

# Volume I — Content Philosophy

Content is a designed encounter with a knowledge object.  
It is not a library of media. It is not a show.

**Content serves learning**  
An asset exists to encode, practice, recall, apply, assess, or reflect. If it does not serve a stage of the Learning Journey, it does not ship. Coverage is not a purpose.

**Content teaches, not entertains**  
Warmth is allowed. A festival is not. Motion, humor, and games are legal only when they carry the try. If removed, and the attempt is not worse, the entertainment was already illegal.

**Understanding before coverage**  
One concept held is worth more than a unit rushed. A course that “finishes the book” and skips practice is a table of contents, not content.

**Quality over quantity**  
A second example that does not teach a near-miss is noise. A third video of the same encode is vanity. We publish fewer, better, bound objects.

**Evergreen knowledge**  
Stable claims stay stable. Living claims version. We do not churn a definition to look fresh. Freshness is a property of the discipline’s clock, not of a content calendar.

**Human-centered content**  
The body in the room is tired, young, old, on a bus, in a second language. Load, script, and stop come first. Our production taste is second.

**Evidence-first content**  
Every teaching claim traces to a knowledge object that traces to evidence. A charming explanation of an uncited claim is a charming fail.

**Accessibility-first content**  
A required asset that cannot be completed in voice-only or type-only, at larger type, without color and without motion, is unfinished. Accessibility is not a variant we add if we have time.

**Global learning**  
A locale is a first-class authoring, not a skin of English. Equivalence is the same class of skill, not the same joke.

**Lifelong education**  
Content outlives a term. A returner meets the same concept id, an honest diagnostic, and no stranger’s origin episode.

---

# Volume II — Content Architecture

Content objects are containers for delivery.  
They point at knowledge objects. They do not replace them.

**Course** — A timed offering of a subject. Has a cohort or a self-pace window. The person’s graph does not end when the course does.

**Unit** — A cluster of objectives inside a course. One theme of work.

**Module** — A sequence inside a unit small enough to finish without a festival.

**Lesson** — One guided encode plus one check, built on the spine in Volume III. Short. Voice-first when the skill is spoken.

**Activity** — A single encounter that is not a full lesson (a warm example, a lab step). Still bound to an object and a stage.

**Exercise** — A prompt to produce. Criterion. Bound to a skill class.

**Practice** — A set of exercises for deliberate or spaced work.

**Reflection** — One metacognitive prompt after a set.

**Assessment** — A disclosed or formative sample (Assessment System). Content here is the item wrapper, not a new scoring law.

**Project** — Multi-session performance. Criteria up front.

**Simulation** — Constrained model of a system. Assumptions labeled.

**Case study** — Situated instance for apply. Not a gossip story.

**Discussion** — Collaborative prompt. Presence visible. Not an anonymous child feed.

**Reference** — Pointer to evidence or a glossary-level definition. Not a lecture in disguise.

**Glossary** — Term table bound to concepts. Locale-aware. Not a second graph.

## Relationships

| Edge | Meaning |
|---|---|
| `contains` | Course → unit → module → lesson → activity |
| `presents` | This asset presents this knowledge object |
| `stage` | This asset serves this lesson stage (Volume III) |
| `variant-of` | Same objective, different presentation (locale, modality, difficulty) |
| `requires` | Prerequisite content or knowledge “enough” |
| `next` | Default successor; Planner may override |
| `assessed-by` | Lesson or module sampled by this assessment |
| `offline-of` | Worksheet or cache view of the same ids |

A lesson with no `presents` edge is a file.  
A `variant-of` that changes the objective is not a variant. It is a different object pretending to be kind.

---

# Volume III — Lesson Architecture

Every lesson follows this educational spine.  
A lesson may skip a stage that the path already completed.  
It may not invent a parallel spine of “hooks” and “payoffs.”

**Learning objective** — One observable class. Named first. If two objectives compete, split the lesson.

**Context** — Why this now: goal, assignment, or last miss. One sentence. Not a biography.

**Introduction** — Where we are and how to stop. Return: no origin story.

**Concept** — The model: definition, scope, near-miss. Ask before a speech when the goal is skill.

**Example** — One worked instance. A second only if the first did not transfer.

**Guided practice** — They produce with a visible scaffold. One hint at a time.

**Independent practice** — Scaffold faded. Isomorphic or near-transfer.

**Reflection** — After the set, one beat. Not during the try.

**Recall** — If this lesson is a return, produce first. Do not re-encode to look helpful.

**Assessment** — Optional check. Formative by default. Disclose if it is of-learning.

**Summary** — What was done. What is due. What is enough. No character sketch.

**Next step** — One next item, a maintain date, or stop. Not a trailer for the rest of the course.

Rules:

- Voice lessons keep working memory to one clause at a time.
- A guest may own guided and independent practice for a subgraph, then leave.
- Media that delays the first produce is a defect.
- If the lesson cannot be finished offline as a smaller twin (read + exercise), say so honestly — do not pretend.

---

# Volume IV — Content Types

Each type has one educational purpose.  
A type that cannot name that purpose is fashion.

**Reading** — Encode or reference in type. Measure the eye can hold. Script-first.

**Audio** — Encode or practice by ear. First-class. Same objective as its reading twin when a twin exists.

**Video** — Show a procedure or a spatial idea that type cannot cheaply show. Captions if it teaches. Never required for Core if audio and type exist.

**Interactive lessons** — Guided produce in a surface. Still the Volume III spine. Not a playground of taps.

**Dialogue** — Spoken turn-taking as the try (language, oral). The host chairs. Not a script of jokes.

**Simulation** — Apply in a constrained model. Assumptions labeled. One idea.

**Laboratory activities** — Procedure in the world or a safe stand-in. Safety first. Not pretend authority.

**Coding exercises** — Produce and check with constrained tools. Do not steal the program they must own when the skill is the program.

**Mathematics practice** — Produce at the edge. Tools verify closed parts. Guests may drill and must leave.

**Writing activities** — They compose. The Writer seat may structure. It does not submit as them when the skill is the writing.

**Speaking activities** — Oral produce. Native script in anything they read. Code-switch allowed.

**Collaborative learning** — Shared try, visible presence. Individual produce still named.

**Projects** — Performance across sessions. Criteria. Not a tape.

**Games for learning** — Allowed only when the mechanic is the try (a timed fluency they were told is timed; a placement of terms that is the classification). If the game can be won without the skill, it is entertainment. Score-as-love is forbidden.

**Field activities** — Observe or collect in the world. Consent and safety. Not surveillance of a home.

A type may combine with a modality (Volume VIII). The purpose does not multiply.

---

# Volume V — Content Quality

A live asset meets these. Knowledge quality (Knowledge System Volume V) still applies to the objects it presents.

**Accuracy** — Matches the pinned knowledge version. A pretty wrong is a fail.

**Educational effectiveness** — After this asset, the next try on the class improves more than after a neighbor, or we revise. Effectiveness is transfer and retention, not watch time.

**Clarity** — One objective. Speakable. Language System applies to every line.

**Accessibility** — Equivalents, keyboard, voice, no color-only, no hover-only, Dynamic Type. Required assets pass or they are not required.

**Neutrality** — No hidden advocacy. Controversy is named and cited.

**Inclusiveness** — Examples do not assume one city, family, body, or board as the world. A named locale is honest, not a disguised universal.

**Readability** — Load-appropriate. Devanagari and other scripts unclipped. No third display font as a teaching face.

**Scientific validity** — Empirical claims follow the discipline. No “brain-based” decoration.

**Citation quality** — Showable sources. No “the model said.”

**Cultural appropriateness** — No mockery, no untranslatable hand-sign as the only cue, no child-as-anecdote.

**Age appropriateness** — Scope, example, and safety fit the band.

An asset that is loved and does not move the class is a failed asset.  
An asset that is plain and moves the class is enough.

---

# Volume VI — Authoring Architecture

**Human authors** — Named. They own the draft’s meaning. Prestige does not skip review.

**AI drafting** — Allowed for outline, variants, hints, alt text, locale drafts. The draft is a draft. It has no `cites` of its own until a human binds evidence.

**Editorial review** — Clarity, structure, Language System, house spine (Volume III). Can refuse.

**Expert review** — Discipline warrant against the knowledge object. Can refuse.

**Accessibility review** — Equivalents, script, motor, cognitive load of the surface. Can refuse.

**Educational review** — Objective, practice, dignity, journey stage. Can refuse.

**Legal review** — License, copyright, child safety of topic, attribution. When the asset uses a work we do not own, this review is required.

**Version control** — Every asset. Diffable. Pinned in live lessons. Mid-try swap forbidden without a written rule.

**Approval workflow** — Two humans for child-facing teaching assets (educational + expert, or educational + editor when the object is already expert-signed). AI cannot be one of the two.

**Publishing** — Pins version, locale, graph bindings, and modality twins. Unpublished is not retrievable as live.

AI drafts. Humans approve.  
A “publish to production” from a model is an incident.

---

# Volume VII — Adaptive Content

Presentation adapts. Learning objectives remain stable.

**Reading levels** — Shorter clauses, not a different science. The concept id does not change.

**Difficulty levels** — Smaller isomorphic items or faded scaffolds. Variants, not easier truth.

**Language adaptation** — Locale and script. `variant-of` plus Knowledge `equivalent-to`.

**Examples** — Skins they chose or that the locale authored. The definition remains.

**Practice variants** — Mixed surfaces of the same class. The class remains.

**Learning paths** — Sequence of lessons. Planner may reorder within prerequisite law. Teacher may override.

**Accessibility variants** — Audio twin, typed twin, larger type, reduced motion. Same objective. Not a lesser course.

**Goal-based content** — Emphasis and due dates from goals they set. Not an invented life.

**Revision content** — Recall-first twins of lessons they have already encoded. Do not re-introduce as new.

**Human override** — Teacher assigns or skips. The OS does not sulk. The objective of the assigned object stays the object’s objective.

Adaptation that needs a second objective “for them” is not adaptation. It is a fork of the curriculum.

---

# Volume VIII — Multimodal Content

Every modality teaches the same concept.  
A modality is a doorway, not a new truth.

**Text** — Default for reference, rubrics, and anything that must be checked later.

**Speech** — Default for the attempt in this OS. Same objective. Speakable lines.

**Images** — When the idea is spatial or iconic. Labeled. Not a hero that delays the try. Text not burned into the image.

**Diagrams** — One idea, high contrast, localizable labels as type.

**Animation** — A verb: show a procedure. Reduced motion: still frames that still teach. No bounce as pedagogy.

**Interactive media** — Produce, not tap-to-advance a comic.

**Video** — Procedure or space. Captions. Not required if twins exist.

**Whiteboards** — Shared or personal working surface. Resource, not a surveillance feed. Retention follows the resource rule.

**AR / VR** — Scenario or spatial apply. Optional. Core remains without a headset. Gaze is not a quiz by default.

**Future interfaces** — Inherit the same concept id, objective, and stop. New sensors optional.

Rules:

- If a concept has a required modality, it must have a twin or an honest “cannot teach this class without X.”
- Switching modality mid-lesson is not a new hello and not a new objective.
- A flashy modality that cannot name the Volume III stage it serves is decoration.

---

# Volume IX — Content Lifecycle

Research → Draft → Review → Validation → Pilot → Publication → Monitoring → Improvement → Localization → Versioning → Archival → Retirement

**Research** — Objective, knowledge bindings, evidence, harm analysis.

**Draft** — Human or AI-assisted. Not live.

**Review** — Editorial, expert, educational, accessibility, legal as required.

**Validation** — Item-fault vs learner-fault on a small set; speak-aloud; script check.

**Pilot** — Consented. Teacher-partnered when schools are involved.

**Publication** — Pin. Retrieve. Guest subgraphs may pin this version.

**Monitoring** — Drops, misses that are item-fault, locale breakage, citation rot, accessibility defects.

**Improvement** — New version. `supersedes`. Do not rewrite under a live try.

**Localization** — Not an afterthought at the end of English. A locale may be the first author. English is not the source of truth by default; the knowledge object is.

**Versioning** — Asset, package, and lesson spine version. Rollback is first-class.

**Archival** — Off paths. Citable as history.

**Retirement** — No live retrieve. Frozen citations remain for records that pointed here.

Skipping Educational or Accessibility review for a required child-facing lesson is not allowed.

---

# Volume X — Localization System

Knowledge remains consistent across languages.  
Content presents that knowledge in a locale.

**Translation** — Meaning and objective first. A translator may refuse an unteachable line. Machine translation is a draft.

**Regional standards** — Board bindings as edges. A local exam form is named when it differs.

**Cultural adaptation** — Re-authored examples. Same `presents` target.

**Native examples** — Written in the locale, not translated jokes.

**Local curriculum** — Paths and units that follow a board. Still map to the graph.

**Terminology** — Glossary bound to concepts. Two translations do not become two sciences.

**Pronunciation** — Stored where speech teaches. Ask once on a name. Do not Anglicize.

**Script support** — Native script first-class. Hindi → Devanagari, never default Roman. Unclipped matras are a ship gate.

**Educational equivalence** — Same class of skill. A locale is not “easier.”

**Inclusive language** — Formal/informal per Language System. No mockery of a regional form.

A language we cannot review, bind, and approve does not get a fake course. It waits.

---

# Volume XI — AI & Content

**Draft generation** — Outlines, variants, alt text, first-pass locale. Labeled as draft.

**Content review** — Linter: missing stage, missing binding, unspeakable line, uncited claim. Not an approval.

**Exercise generation** — Candidates bound to a class. Human selects and binds criterion. Unbound generated drills do not go live.

**Hint generation** — One-hint candidates. A hint that is the answer must be labeled solution.

**Example generation** — Must include a near-miss or it is a restatement. Human keeps or kills.

**Difficulty adjustment** — Propose a smaller isomorphic or a transfer variant. Human or Planner law accepts. The objective stays.

**Content validation** — Check against the pinned knowledge object and tools. Flag conflicts. Do not silently “fix” truth.

**Fact checking** — Objects and tools outrank the draft. Empty evidence is empty.

**Citation support** — Retrieve `cites` targets. Do not invent a source.

**Human approval** — Still two humans for child-facing teaching assets.

AI never publishes independently.  
AI never invents a lesson that is not a presentation of live knowledge objects.  
A generated path of unbound media is a hallucination of a course.

---

# Volume XII — Content Analytics

Analytics improve teaching. They do not measure entertainment.

**Completion quality** — Finished the produce, not the play-through. A video watched to the end with no try is a failed completion.

**Practice success** — Accuracy and faded scaffolds on the class.

**Learning outcomes** — Transfer and retention after this asset.

**Misconception detection** — Recurring near-misses that are item-fault or missing near-miss in the encode. Feeds revision, not a child’s label.

**Content effectiveness** — Next-try improvement vs a neighbor asset of the same object.

**Revision frequency** — Thrash on a stable concept is a smell. Silence on a living standard is a risk.

**Accessibility metrics** — Twin coverage, caption coverage, fail rates when type is large or motion is off. Gaps are defects.

**Localization quality** — Refusal rate by translators, script defects, equivalence reviews.

**Engagement for learning** — Means “completed a real attempt.” Not time trapped, not taps, not smile time, not watch hours.

**Long-term retention** — Recall after a gap that used this encode or this practice set.

No “most entertaining lesson.”  
No ranking of authors as a product wall.  
A viral asset that does not move transfer is retired or rewritten.

---

# Volume XIII — Content Governance

**Editorial boards** — Own the live set for a domain or subject. Named. Vacancy is an incident.

**Subject experts** — Sign the knowledge binding. A lesson cannot outrun an unsigned object.

**Curriculum teams** — Bind courses, units, paths. No shadow graph.

**Accessibility teams** — Can block a required asset. Their refuse stands.

**Localization teams** — Can refuse a line. Their refuse stands.

**AI contributions** — Draft and flag only. Named as machine in the audit. Never as author of record.

**Human approval** — Two humans for child-facing teaching assets. Recorded.

**Licensing** — Every asset. We do not teach from a stolen book. Short citation is not a chapter.

**Copyright** — Legal review when we use another’s work. Attribution is visible.

**Audit history** — Who drafted, who approved, which knowledge version, which locale. Not a transcript of learners.

A school or partner package passes this governance or it does not enter live retrieval.

---

# Volume XIV — Future Content

Media will change. The spine will not.

**Living lessons** — Faster revision of living claims. Same Volume III. No mid-try swap. No automated publish.

**AI-assisted authoring** — Stronger drafts, same two-human gate, same ban on invented curriculum.

**Dynamic curriculum** — Paths that reorder within prerequisite law. Dynamics that change truth by subscriber tier are forbidden.

**Personalized content** — Variants of presentation. Personal knowledge spaces remain licensed views, not private physics.

**Immersive learning** — Scenario and spatial apply. Optional. Core without a headset.

**Spatial education** — Diagrams in space. Labels as type. Gaze not a quiz by default.

**Collaborative content** — Co-authored lessons by teachers, still governed. Children are not unpaid authors of our catalog unless a program they joined says so and they can erase.

**Community contributions** — Draft packages. Same reviews. No marketplace of personalities.

**Lifelong libraries** — Exportable, versioned, decaying mastery against stable concept ids.

**Future educational media** — New formats inherit `presents`, objective, stage, twins, and stop.

The future may add a medium we cannot name.  
It may not add a required spectacle, a lesson without an object, or a publish button for a model.

---

# Volume XV — Content Manifesto

Content exists to enable understanding, not consumption.

A lesson is a table, a concept, an example, and a try. It is not a feed. When we count hours watched and call it learning, we have built a theater and asked a child to sit still in it. This hall does not sell seats. It asks for a produce.

Clarity is more valuable than volume. One sentence they can use tomorrow beats a unit they survived. Volume is how a store looks full. Clarity is how a mind gets a next step. If we must cut, we cut the extra example, the extra motion, the extra hello — never the objective, the check, or the way to stop.

Educational quality outweighs production speed. A fast wrong lesson is a wound that spaces itself into memory. A slow right lesson is a kindness. AI will make drafts cheap. That does not make publish cheap. The cost we refuse to pay is a child’s wrong rule, fluently taught.

Every lesson deserves evidence. Not a vibe, not a brand film, not a model’s prior. A bound object, a source, a version. If we cannot show a teacher why this line is here, the line is not here.

Teachers remain essential, regardless of technology. They assign, override, refuse a guest, explain a line to a parent, and sign a sample. Content that tries to replace that judgment is not advanced. It is rude. The OS is a colleague’s tool. The colleague stays.

What must never change, even when the medium is air:

Every asset presents a knowledge object.  
Every lesson has one objective and a produce.  
Entertainment that does not carry the try does not ship.  
Presentation may adapt; the objective may not.  
Every required asset has a twin or an honest limit.  
AI drafts. Humans publish.  
A locale is a first-class author, not a skin.  
A child’s attempt does not become our next example without license and governance.  
Completion without a try is not completion.  
The next step is one step.

The operating system is a hall with a lesson on the table.

If the lesson is clear, a quiet voice is enough.  
If the lesson is a show, no voice can make it true.

Stay on the line.  
Bind the object.  
Ask them to try.  
Publish less.
