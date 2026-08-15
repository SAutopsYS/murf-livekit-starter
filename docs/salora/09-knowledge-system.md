# SALORA OS — Knowledge System Constitution

Phase 6.

The Constitution defines why knowledge matters.  
The Product Blueprint defines where knowledge exists.  
The AI System defines how knowledge is used.  
The Learning System defines how knowledge becomes learning.

This file defines what knowledge is, how it is structured, how it evolves, how it is validated, and how every educational object connects.

Not a content repository.  
Not curriculum writing.  
Not documentation.

The permanent Knowledge Architecture and Knowledge Management Constitution.  
Curriculum architects, knowledge engineers, ontology designers, librarians, instructional designers, AI researchers, content strategy, and product follow this file.

Product Architecture named that knowledge and memory do not share a bucket.  
AI System named retrieval and citation seats.  
Learning System named how a mind moves.

This file is the map and the law of the map.

If an object cannot name its type, its edges, its evidence, and its version, it is not knowledge in this OS. It is a file.

---

# Volume I — Knowledge Philosophy

Knowledge in SALORA is a claim that can be taught, checked, cited, versioned, and revised.  
It is not a pile of pages. It is not a model’s prior. It is not a person’s memory.

**Knowledge vs information**  
Information is a signal that arrived. Knowledge is a structured claim with a type, a place in the graph, and a source. A feed of facts is information. A concept with a prerequisite and an example is knowledge.

**Understanding vs facts**  
A fact can be retrieved. Understanding is a model of a concept: definition, near-miss, example, and a skill that uses it. We store both. We do not call a fact-list a curriculum.

**Wisdom vs recall**  
Wisdom is judgment in a life. The OS does not mint wisdom. It may teach a procedure, a principle, and a case. It may not speak as an elder who has lived their years. Recall is a performance. Wisdom is not a badge.

**Connected knowledge**  
An isolated page is a leaf without a branch. A concept without edges cannot be planned, spaced, or transferred. Connection is not a decorative map. It is the infrastructure of the next item.

**Explainable knowledge**  
A teacher can say why this object is here, what it depends on, and where it came from. If only a vector knows why it was retrieved, it is not explainable. We do not teach from a black box.

**Human-centered knowledge**  
The graph exists so a person can try. Density that serves an ontologist and harms a child is vanity. Age, locale, and load change presentation. They do not invent a second truth.

**Living knowledge**  
Claims age. Standards change. A living system revises, versions, and retires. It does not silently rewrite yesterday under a live attempt. Living is disciplined change, not a wiki mood.

**Evidence-first knowledge**  
Every object traces to evidence (Volume VI). Confidence is not evidence. A fluent model is not a source. A popular page is not a validation.

**Knowledge as infrastructure**  
Knowledge is a platform layer. Products, guests, and lessons are views. If the graph is weak, every tutor is weak. If the graph is strong, a simpler mouth can still teach.

**Lifelong knowledge**  
Domains outlive a term, a school, and a model pin. A person may carry competency over decades. The objects they mastered must still be findable, exportable, and honest about decay.

---

# Volume II — Knowledge Architecture

Every first-class knowledge object is one of these types.  
A file format is not a type.  
A team’s folder is not a type.

## Objects

**Domain** — A stable field of human knowledge (mathematics, living systems, language). Outlives a board year.

**Discipline** — A method-community inside or across domains (algebra as practiced; experimental science). Names how claims are warranted.

**Subject** — A taught slice for a context (Class 8 Mathematics; Spoken Hindi). Maps to the graph. Does not replace it.

**Topic** — A cluster of concepts and skills used for navigation and units.

**Concept** — An atomic idea a person can be right or wrong about. The unit of first encoding.

**Principle** — A general claim that governs many cases (conservation; subject-verb agreement). A principle has a scope and known exceptions.

**Rule** — A local, often procedural, constraint (order of operations in this notation). A rule cites a principle or a standard. A rule without a scope is a trap.

**Skill** — An observable performance composed of concepts, principles, and procedures.

**Procedure** — An ordered method (long division; how to cite). Teachable. Fade-able. Not a personality.

**Example** — A worked instance bound to a concept or skill. One idea. Labeled. Localizable.

**Case study** — A longer situated instance. For apply and scenario practice. Not a gossip story about a child.

**Exercise** — A prompt to produce. Bound to a skill class. Has a success criterion.

**Question** — A recall or check item. May be oral. Still an object with a class and a criterion.

**Assessment** — A disclosed sample of a class (Learning System Volume VI). An object that points at items, not a vibe.

**Reflection** — A metacognitive prompt bound to a set or a competency. Not a journal exam.

**Learning outcome** — An observable result a teacher can repeat. Bound to skills or competencies.

**Competency** — A cluster of skills that transfer across items and, later, contexts.

**Credential** — A claim to the world about a competency sample. Human path required. Not a streak.

## Relationships

Every edge is typed. Untyped “related” is a last resort and a smell.

| Edge | Meaning |
|---|---|
| `part-of` | Object belongs to a larger object |
| `prerequisite` | Must be true enough before the target |
| `teaches` | A lesson or asset encodes this concept or skill |
| `assesses` | An item samples this class |
| `example-of` | Instance of a concept, principle, or skill |
| `instance-of-procedure` | This exercise uses that procedure |
| `supports` | A principle or rule governs this skill |
| `exception-to` | Known limit of a rule or principle |
| `transfers-to` | Practice on A helps class B |
| `equivalent-to` | Same claim in another locale or standard |
| `cites` | Evidence link |
| `supersedes` | This version replaces that object |
| `contradicts` | Known conflict; must not be silently merged |

A concept with no `part-of` or `prerequisite` and no `teaches` edge is unfinished.  
A skill with no exercise or question cannot be practiced.  
A credential with no `assesses` path is a lie.

---

# Volume III — Knowledge Graph

The graph is the source of connection.  
The mouth does not recite it.  
The Planner reads the learning projection of it.  
Retrieval reads the semantic projection of it.  
They are views of one graph, not two truths.

**Concepts** — Nodes of encoding. Must have a definition, a near-miss, and at least one example or exercise.

**Dependencies** — `part-of` and `supports`. Structural, not optional flavor.

**Prerequisites** — `prerequisite` with an “enough” rule per target (a threshold on a class, not a mood). The Planner may not skip a hard prerequisite without a teacher override or a diagnostic that already showed enough.

**Related concepts** — Sibling or analog edges. Used for interleaving after encoding, not for first-minute confusion.

**Similar skills** — Same class, different surface. The basis of mixed practice and transfer items.

**Cross-disciplinary links** — Typed (`supports`, `transfers-to`, `equivalent-to`). A decorative “STEAM” cloud is not a link.

**Learning graph** — The subgraph the Planner uses: concept, skill, prerequisite, transfers-to, teaches, assesses. This is the educational spine.

**Competency graph** — Competency → skills → outcomes → credentials. Used for paths and official samples.

**Knowledge maps** — Human-facing views for teachers and architects. Not a poster during speech. Not a learner maze.

**Concept networks** — Neighborhoods for retrieval and for “what else belongs in this unit.” Still typed edges.

**Semantic relationships** — Synonym, translation, notation variant, `equivalent-to`. Semantics serve finding and locale. They do not merge two different claims into one node to make a chart pretty.

Rules of the graph:

- One claim, one node. Variants are edges, not duplicate truths.
- Cycles in `prerequisite` are defects.
- A node without evidence is a draft, not live.
- A node without a version is drift.
- The graph may be incomplete. It may not be invented at retrieval time.

---

# Volume IV — Content Architecture

Content is a presentation of knowledge objects.  
Content is not a second ontology.  
If an asset cannot point at objects in Volume II, it is a file in a drawer.

**Lesson** — Guided encode + one check. Points at concepts and a skill. Short.

**Video** — Optional representation. Captions required if it teaches. Text and voice must still complete the objective (Learning System: UDL, not learning-styles myth).

**Audio** — First-class in a voice OS. Same objects as a lesson. Not a podcast of the brand.

**Reading** — A text resource with a measure the eye can hold. Script-first. Cites.

**Interactive activity** — A try in a surface. Still an exercise underneath.

**Simulation** — A model of a system for apply. Labeled assumptions. Not a game that hides the objective.

**Experiment** — A procedure in the world or a constrained lab-like task. Safety first. Not pretend authority.

**Practice** — A set of exercises bound to a skill class.

**Flashcards** — Active recall objects. Prompt and criterion. If they reveal first, they are content, not practice.

**Projects** — Multi-session performance tasks. Criteria. Not a tape.

**Worksheets** — Printable or offline views of exercises. Same ids. Sync must not duplicate the attempt.

**Discussion** — A prompt for collaboration. Presence visible. Not an anonymous feed of children.

**Reflection** — The metacognitive object, as a short prompt.

**Assessments** — Disclosed samples. Item ids. Human path if official.

**References** — The evidence objects themselves, or pointers to them.

## Organization

Assets live in packages: locale, version, license, subject binding, graph bindings.  
A package that is only a zip of videos is not organized.  
Search finds objects first, assets second.  
The same concept may have many assets. Truth does not multiply with assets.

---

# Volume V — Knowledge Quality

A live object meets these. A draft may not.

**Accuracy** — The claim matches the cited evidence and the pinned standard. A pretty wrong is a fail.

**Completeness** — Enough to teach the object’s type: a concept has definition, near-miss, example; a skill has a procedure or a criterion and an exercise.

**Neutrality** — No hidden advocacy. Where a live controversy exists, the object says so and cites. Neutrality is not false balance between a fact and a fiction.

**Educational value** — The object earns a place on a path: it is used to encode, practice, recall, or assess. Orphan trivia does not ship.

**Scientific validity** — Empirical claims follow the discipline’s warrant. “Brain-based” decoration is not validity (Learning System Volume XIII).

**Citation quality** — Stable, showable to a teacher, versioned. A broken link, a nameless PDF, or “the model said” is not a citation.

**Readability** — Language System: speakable, script-correct, load-appropriate.

**Accessibility** — Text equivalent for media. Diagrams labeled. Not color-only meaning.

**Age appropriateness** — Scope and example fit the band. Safety of topic is a gate, not an afterthought.

**Cultural neutrality** — Default examples do not assume one city, one class, one family shape. Locality is a locale layer, not a disguised universal.

**Bias detection** — Review for mockery of regional forms, gendered skills, single-board-as-world, and child-as-anecdote. A hit blocks live.

Quality is a ship gate. Popularity is not a quality score.

---

# Volume VI — Evidence Architecture

Every knowledge object traces to evidence.  
No evidence, no live node.

**Primary sources** — The originating warrant where the discipline requires it (a standard’s text; a dataset; a historical document). Used when we claim the thing itself.

**Secondary sources** — Reviews, textbooks, trusted syntheses. Allowed when they are the normal warrant of the subject. Still cited.

**Research papers** — For methods, learning claims, and contested science. We do not launder a blog as a paper.

**Books** — Allowed when they are the standard carrier. Edition and page or section, not a vibe.

**Educational standards** — Board and framework bindings (`equivalent-to`). A subject may follow a board. The graph still exists above the board.

**Expert review** — A named human in the discipline signs a version. Anonymous “team” is not expert review.

**Peer review** — A second human who can refuse. For credentials, contested claims, and child-facing science.

**Citations** — `cites` edges. Visible to teachers. Retrievable. Versioned with the object.

**Knowledge verification** — Closed claims can be checked by a tool or a rubric. Open claims hedge and cite. Verification is recorded on the version.

**Continuous validation** — After live: error reports, teacher flags, retrieval misses, failed items that are item-fault not learner-fault. Validation can send a node back to revision.

A model’s confidence is not a source.  
A vector neighbor is not a source.  
A child’s session is not a source.

---

# Volume VII — Retrieval Architecture

Retrieval finds existing objects.  
It does not mint objects.

**Semantic search** — Meaning over exact string, still returning typed objects. A semantic hit without an id is a miss.

**Vector retrieval** — Allowed as an index over objects we already have. Vectors do not become a parallel curriculum. A neighbor is a candidate, not a citation.

**Hybrid search** — Graph constraints + lexical + vector. The graph can forbid a hit (wrong age, wrong locale, retired, no evidence). Forbid outranks similarity.

**Knowledge ranking** — Educational fit first: prerequisite enough, locale, version pin, quality gate, then similarity. Popularity is last and usually absent.

**Context retrieval** — Session and task may filter. They may not expand into unlicensed memory. Context is a filter, not a biography.

**Curriculum retrieval** — Guest and path retrieve inside their subgraph. A math guest does not retrieve a random inspiring quote.

**Memory retrieval** — Licensed fields about the person. Different bucket. Never mixed into a knowledge citation.

**Citation retrieval** — When a claim needs a source, retrieve the `cites` target. If empty, say empty.

**Recommendation retrieval** — The Planner’s next object. One next. Not a store row.

**Explainable retrieval** — An operator or teacher can see: why this id (edge, locale, pin, query). “The embedding liked it” is not an explanation we ship to a teacher.

Empty retrieval is a first-class result: teach smaller from what we have, or offer a human. Do not fill from a prior.

---

# Volume VIII — Knowledge Personalization

Knowledge changes presentation, never truth.

**Difficulty** — Harder items and faded examples. The principle does not change.

**Context** — Classroom, home, exam, offline. The asset may change. The concept id does not.

**Language** — Locale and script. `equivalent-to` bindings. Not a new science.

**Age** — Example and load. Not a different law of arithmetic.

**Goals** — Which path is emphasized. Not which facts are true.

**Background** — Diagnostic “enough” on prerequisites. Not an invented life story.

**Prior knowledge** — Skip or descend. The skipped node still exists.

**Weaknesses** — More exercises on the class. Not a scarlet letter on the node.

**Interests** — Optional example skins they licensed or chose. A football wrapper does not replace the definition. Interests are not harvested from a tape.

**Human override** — Teacher picks the object. The graph yields. Truth does not.

A personalization that needs a second graph of “their truth” is forbidden.  
A personal knowledge space (Volume XIV) is a licensed view, not a private physics.

---

# Volume IX — Content Lifecycle

Research → Draft → Expert Review → Educational Review → AI Review → Accessibility Review → Pilot → Publication → Monitoring → Revision → Archival → Retirement

**Research** — Evidence gathered. Type chosen. Edges sketched. Harm analysis if the topic can harm.

**Draft** — Object exists. Not retrievable as live.

**Expert review** — Discipline warrant. Can refuse.

**Educational review** — Learning System: objective, practice, load, dignity. Can refuse.

**AI review** — Seats may flag missing edges, uncited claims, unspeakable lines, hallucination risk. AI cannot approve. AI cannot publish.

**Accessibility review** — Script, equivalents, age, contrast in diagrams. Can refuse.

**Pilot** — Small, consented, teacher-partnered when schools are involved.

**Publication** — Pinned version. Live retrieval. Guest subgraphs may pin this version.

**Monitoring** — Item-fault vs learner-fault, teacher flags, citation rot, locale breakage.

**Revision** — New version. `supersedes`. Live sessions do not swap text mid-try without a written rule.

**Archival** — Off paths. Still citable as history. Not recommended.

**Retirement** — No retrieval for teaching. Export and records that depended on it keep a frozen citation. We do not pretend it never existed if a credential pointed at it — we mark superseded.

Skipping Expert or Educational review for child-facing science is not allowed.  
Skipping Accessibility review for a required asset is not allowed.

---

# Volume X — Knowledge Governance

**Editorial review** — A named editor owns the live set for a domain or subject. Vacancy is an incident.

**Subject experts** — Sign versions. Their name is on the object. Prestige is not a substitute for a second reviewer on contested claims.

**Curriculum teams** — Bind subjects, units, paths. They do not mint shadow graphs.

**AI contributions** — Draft, cluster, flag, suggest edges. Never the publisher. Never the source.

**Human approval** — Two humans for live child-facing claims (expert + educational, or expert + peer). One human may draft. One may not ship alone.

**Version control** — Every object. Diffable. Rollback. Pin in production seats.

**Audit history** — Who approved, who changed, what evidence was added or removed. Not a transcript of learners.

**Licensing** — Every asset and source has a license we can honor. We do not teach from a stolen book.

**Copyright** — We do not paste a work we do not have the right to paste. Short citation is not a chapter.

**Attribution** — Authors, translators, standards bodies, and source works are named. The OS does not wear their labor as its personality.

A guest, a partner, or a school may contribute packages. They pass this governance or they do not enter retrieval.

---

# Volume XI — Multilingual Knowledge

**Translation** — Meaning and type first. A translator may refuse an unteachable line. Machine translation is a draft.

**Localization** — Examples, units, names, and boards. Not a skin of English thought.

**Native scripts** — First-class. Hindi → Devanagari, never default Roman. A node that clips matras is not live in that locale.

**Cultural adaptation** — Local examples via `equivalent-to` or locale assets. The concept id remains. Adaptation is not erasure of a standard the exam will use — we say when the exam form differs.

**Regional curriculum** — Board bindings as edges, not as a fork of truth. A regional path can require a local procedure.

**Terminology** — A term table per locale, bound to the concept. Do not let two translations become two concepts without an edge.

**Examples** — Re-authored when a joke, food, or street does not travel. Still `example-of` the same concept.

**Pronunciation** — Stored where speech teaches. Ask once on a name. Do not Anglicize.

**Cross-language mapping** — `equivalent-to` and term tables. Code-switch is allowed in the room; the objects stay mapped.

**Educational equivalence** — A locale is not “easier.” Equivalence is the same class of skill, not the same English sentence.

A language we cannot govern, cite, and review does not get a fake graph. It waits.

---

# Volume XII — AI & Knowledge

AI illuminates the graph. It does not replace the graph.

**Knowledge retrieval** — Seats call retrieval. They receive ids and allowed fields. They do not browse a secret web of children.

**Citation** — If the mouth makes a claim that needs a source, it emits the source we retrieved. No source, no claim — hedge or smaller teach.

**Hallucination prevention** — Closed facts verify against the object or a tool. Empty retrieval is empty. A prior is not a curriculum. Invented ids are a safety event.

**Knowledge updates** — Models do not update the graph. Humans do, through the lifecycle. A model that “noticed” an error may file a flag. That is all.

**Source attribution** — The person and the teacher can be shown the source. Hidden training residue is not attribution.

**Knowledge validation** — AI review is a linter. Human approval is the gate.

**Fact checking** — Tools and objects outrank the mouth on closed facts. The mouth outranks neither safety nor the person on Stop.

**Reasoning with knowledge** — The Reasoner may use retrieved objects as premises. Premises are ids. A step that needs a missing premise stops.

**Teaching from knowledge** — Teacher and Host seats teach the bound example and exercise. They do not invent a parallel lesson and call it the same concept.

**Memory separation** — Licensed memory is not a citation. A child’s miss is not written back as a knowledge example. Their attempt does not become our textbook.

**AI never invents curriculum.**  
It may draft a node. A human must type it, edge it, cite it, and approve it. A generated path that is not a subgraph of live objects is a hallucination of a course.

---

# Volume XIII — Knowledge Analytics

Analytics improve knowledge. They do not measure popularity.

**Knowledge coverage** — Live objects vs the competency map we claim to teach. Holes are first-class.

**Concept mastery** — Learning states on the concept and its skills (Learning System). Used to find object-fault (many fail the item, few fail neighbors).

**Content usage** — Which assets are actually used in attempts. Orphans are revision or retirement candidates. Usage is not a quality trophy.

**Learning effectiveness** — Transfer and retention after this object, vs a neighbor. Item-fault analysis.

**Knowledge gaps** — Missing prerequisites, missing exercises, missing locale equivalents.

**Retrieval quality** — Precision of ids, empty-when-empty, explainability samples, forbidden-hit rate (graph constraints obeyed).

**Citation quality** — Rot, unshowable sources, objects live without `cites`.

**Content freshness** — Age vs the discipline’s clock (a math definition ages slowly; a policy ages fast). Freshness is not a reason to churn a stable concept.

**Update frequency** — Too rare on living standards is a risk. Too often on a stable concept is thrash.

**Educational impact** — Did the next try improve after this object entered a path? If not, the object is decoration.

No ranking of children.  
No ranking of teachers as content.  
No “most engaging video” as a knowledge KPI.  
A viral asset that does not move transfer is a failed asset.

---

# Volume XIV — Future Knowledge

Information will become infinite. The graph will not become a dump.

**Living knowledge graphs** — More edges, faster revision, same types, same evidence gate. Living is not automated publish.

**AI-generated curriculum** — Draft only. Lifecycle and two humans remain. A future that publishes a model’s course to a child has left this constitution.

**Dynamic knowledge maps** — Views that re-layout for a teacher or a path. The nodes do not move their meaning.

**Personal knowledge spaces** — Licensed views: their goals, their states, their notes if they wrote them. Not a shadow physics. Exportable. Erasable.

**Global educational networks** — Shared packages across schools and locales with `equivalent-to`. A network is not a marketplace of souls or a scrape of children.

**Scientific discovery integration** — New claims enter as drafts with primary evidence. They do not appear in a child’s path because a headline was loud.

**Real-time knowledge updates** — Allowed for operators and for living standards after review. Not mid-try text swap. Not a breaking news tutor.

**Lifelong knowledge models** — The person’s competency graph over decades, in their export. Our models of the world remain the shared graph, not a private fork per child.

**Human–AI knowledge collaboration** — AI flags and drafts. Humans warrant. Teachers override paths. Librarians own the catalog.

**Future educational standards** — New boards bind as edges. We do not rebuild the OS per board. We do not pretend one board is the world.

The future may add media we do not have names for.  
It may not add a bucket where speech becomes a textbook, or a truth that changes by subscriber tier.

---

# Volume XV — Knowledge Manifesto

Knowledge is humanity’s shared inheritance. It does not belong to a model, a board, or this company. We are stewards of a map: we hold claims so a person can try them, check them, and leave them better than a rumor.

Education depends on trustworthy knowledge because a fluent lie is worse than a silence. A child will remember a wrong rule with the same body they use for a true one. If we teach from confidence, we teach weather. If we teach from evidence, we teach a world that can be checked when we are gone.

AI must illuminate knowledge rather than replace it. A light that invents the furniture is a fire. The mouth may point, hint, and retrieve. It may not mint a curriculum in the dark and call the glow a school.

Every concept deserves context: a definition, a near-miss, an example, a prerequisite, a source, a version. A concept without context is a word. Words are cheap. Context is how a mind can use a word tomorrow.

Evidence matters more than confidence. Confidence is a tone. Evidence is a trail. When the two disagree, we keep the trail and humble the tone. When we have no trail, we say we do not know, and we do not fill the hole with a neighbor in vector space.

What must never change, even when information grows past any library:

Knowledge and memory do not share a bucket.  
Every live object has a type, edges, evidence, and a version.  
Retrieval finds; it does not invent.  
Presentation may change; truth may not.  
AI may draft; humans publish.  
A child’s attempt does not become our source.  
Empty is empty.  
A credential samples a class.  
A language is a first-class map, not a skin.  
The graph can be incomplete. It cannot be a lie.

The operating system is a hall with a catalog.

If the catalog is honest, a quiet tutor is enough.  
If the catalog is a dump, no voice can save it.

Stay on the line.  
Cite.  
Connect.  
Do not invent the world.
