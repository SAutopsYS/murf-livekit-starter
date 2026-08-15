# SALORA OS — Platform Architecture

How SALORA is architected as a platform.

Not source code.  
Not API documentation.  
Not implementation.

Permanent boundaries and philosophy. Engineering teams follow this file after the Constitution and Operating Standards.

If a system cannot name its layer, its data class, and its owner, it is not a system. It is drift.

---

# Volume I — Platform Philosophy

**Reliability before complexity**  
A simple host that stays in the room beats a clever graph that drops the person. Complexity is spent only to protect continuity, privacy, or a named guest with a way home.

**Privacy by architecture**  
Absence of a field is stronger than a policy over a field. Transcripts are not a column waiting for a better dashboard. Speech is not a byproduct we store “in case.”

**Composable systems**  
Layers and services compose through small, honest contracts. A guest composes with the host. It does not fork the voice path.

**Loose coupling**  
A model swap, a school tenancy, or a device client may change without rewriting identity, consent, or session continuity. Coupling is allowed around the kernel: host, license, fail-closed.

**Clear ownership**  
Every service has a human owner for the 3 a.m. failure. Shared ownership of a leak is no ownership.

**Graceful degradation**  
Lose a guest, keep the host. Lose a model, keep a shorter honest path or a human offer. Lose the network, tell the truth. Do not hang. Do not pretend.

**Offline resilience**  
The platform assumes absence. Cached licensed memory and last lesson may be readable. Sync is idempotent. Offline is a mode, not an error costume.

**Human-centered infrastructure**  
Infrastructure exists so a person is not restarted and not exposed. Capacity, traces, and queues are judged by fail-closed rate, first useful audio, and leak absence — not by vanity throughput.

These principles outrank framework fashion.

---

# Volume II — Core Platform Layers

A layer has a purpose and a boundary. It may not own a neighbor’s data class.

**Identity Layer**  
Stable ids for users, agents, tenancies. The host id survives model change. Does not store speech.

**Authentication Layer**  
Proves who is at the door. Sessions of proof are not lessons. Does not infer a child from a device without a written rule.

**Authorization Layer**  
What a role may do. Guest ≤ host ≤ consent. School cannot mint a tape right.

**Profile Layer**  
Chosen attributes and preferences. Not inferred biography.

**Memory Layer**  
Licensed fields, projections, forget, promotion rules. Boundary: no raw conversation lake.

**Learning Layer**  
Graphs, items, states, spacing, next item. Boundary: does not speak; does not store utterances.

**AI Layer**  
Host and guest seats, planner, tools, prompt hierarchy, evaluation hooks. Boundary: does not own voice transport; does not own consent.

**Voice Layer**  
One pipeline into the room. Transport, turn, reconnect-as-same-room. Boundary: not a second brain; not an archive.

**Media Layer**  
Requested images, optional captures. Boundary: no silent camera; no face as a requirement.

**Storage Layer**  
Holds the data classes in Volume IV. Boundary: encryption and retention as assigned; no “scratch” that becomes a profile.

**Sync Layer**  
One live attempt; device takeover; idempotent writes. Boundary: does not merge two tutors.

**Notification Layer**  
Quiet delivery. Boundary: not a tutor; not marketing.

**Analytics Layer**  
Structured events without content of speech. Boundary: not Memory; not Assessment records of a child’s words.

**Security Layer**  
Keys, threats, supply chain, session hardness. Cross-cuts. Does not relax for a demo.

**Monitoring Layer**  
Health of host, guest, voice, memory, tools. Traces of route, not of mouth.

**Configuration Layer**  
Flags, curricula versions, guest registration. Safety and forget are not optional flags in production.

---

# Volume III — Service Architecture

Logical services. One purpose. One owner.

**User Service** — Accounts, roles, guest/anonymous.  
**Learning Service** — Items, states, graphs, next.  
**Assessment Service** — Samples, tool scores, human-review flags.  
**Memory Service** — License, list, project, forget.  
**Voice Service** — The one pipeline; reconnect semantics.  
**AI Router** — Host vs named guest; confidence; one retry; fail to host.  
**Model Gateway** — Seats models behind host/guest; evaluation gate.  
**Search Service** — Index of allowed taxonomy objects.  
**Content Service** — Resources with sources and versions.  
**Teacher Service** — Classes, assignments, override.  
**Parent Service** — Projections and rare alerts.  
**Enterprise Service** — Tenancy, policy, aggregates, health.  
**Billing Service** — Entitlements. Cannot lock dignity behind improvisation; policy is written.  
**Audit Service** — Who accessed what class of data. Not a transcript archive.  
**Permissions Service** — Capability decisions used by all others.  
**Notification Service** — Quiet facts.

A new service must declare which layer it sits in and which data class it may touch. Two services may not both believe they are the router.

---

# Volume IV — Data Architecture

**Operational Data** — Sessions as visits, device takeover, live flags. Short-lived where possible.

**Learning Data** — States, due times, item ids, scores of a class. No utterances.

**Memory Data** — Licensed fields, consent receipts, projection grants, deletion records.

**Analytics Data** — Event names, timings, route ids, fail-closed, latency. No content.

**Audit Data** — Access, export, forget, admin acts. Retention by law and contract.

**Content Data** — Curriculum, items, sources, versions.

**Media Data** — Explicit artifacts. Retention short unless the resource is the curriculum.

**Configuration Data** — Flags, guest versions, prompt hierarchy pointers.

**Offline Data** — Device cache of last lesson and licensed snapshot. Encrypted. Expiring.

**Synchronization Data** — Cursors, idempotency keys, conflict rule: one live session.

**Retention** — Speech not retained by default. Learning and memory retained as licensed and contracted. Analytics aggregated and aged.

**Deletion** — Forget and account delete complete in product paths. Backups age out. Teaching systems may not resurrect a forgotten field.

**Ownership** — The person owns memory about them. The school owns roster and contract data as law allows. The company owns product configuration and models. Nobody owns a child’s mouth.

---

# Volume V — AI Infrastructure

Permanent seats. Models are replaceable.

**Host AI** — Relationship, refusal, escalation offer, accept/reject guest deltas.  
**Guest AI** — Named specialist, subgraph, time-boxed by task, no guest-of-guest.  
**Planner** — Next pedagogical move. Deterministic when declared deterministic.  
**Reasoner** — On demand for a class of task. Not a personality stream.  
**Memory Manager** — Reads license; writes deltas; never promotes without consent.  
**Model Gateway** — Maps seat → model version after evaluation.  
**Tool Runtime** — Closed, validated tools. Failures spoken as tool failures.  
**Context Manager** — Prefers structured state. Window full → licensed summary, not a secret diary.  
**Safety Layer** — In front of every mouth. Distress, crime, medical, child harm: stop drill, offer human.  
**Evaluation Layer** — Volume VII of Operating Standards as a gate, not a poster.  
**Fallback Layer** — Guest → host; model → shorter host or human; voice → typed or honest stop.  
**Routing Engine** — Explainable; confidence bands; one clarification; one retry; no loops.  
**Prompt Layer** — Hierarchy: Safety → Constitution/behavior → role → licensed memory → task → style. Lower cannot cancel higher.  
**Knowledge Retrieval** — Sources required. No invented citation.  
**Model Registry** — Versions, scores, seat history. A model without Recovery and Honesty seats does not enter production.

There is one voice path. A second path is an architectural incident.

---

# Volume VI — Platform Reliability

**Availability** — The host path is the SLO that matters. A green guest and a dead host is an outage.

**Scalability** — Scale the pipeline and learning reads. Do not scale a transcript store we refused to have.

**Fault tolerance** — Isolate guest failure. Isolate tenancy. Isolate a bad model version behind the gateway.

**Graceful failure** — Speak the failure. Keep state. Do not crash the room.

**Disaster recovery** — Restore identity, license, learning state, content. Do not restore a speech lake that must not exist.

**Backups** — Encrypted. Retention aligned with deletion. Tested restores.

**Observability** — Route, latency, fail-closed, error class. No mouth in the trace.

**Incident response** — Speech leak is Sev-1. Restart-the-person is Sev-1. Growth waits.

**Monitoring** — Host, guest, voice, memory, tools. Alert on truth, not on “engagement.”

**Health checks** — Can the host start? Can forget complete? Can a guest fail closed?

**Capacity planning** — First useful audio and school-day peaks. Not demo-week theater.

**Service ownership** — Named humans. Runbooks for fail-closed, forget, leak.

---

# Volume VII — Security Architecture

**Identity** — Stable, unique, no shared child logins as a workaround.  
**Authentication** — Proven session. School SSO where contracted.  
**Authorization** — Server-side roles. UI is not the control.  
**Encryption** — In transit and at rest for every data class that exists.  
**Secrets** — Out of the tree. Rotated. Never in traces.  
**Key management** — Owned. Separated from application fashion.  
**Access control** — Least privilege. Admin is not a lesson viewer.  
**Device trust** — Takeover is confirmed. A new device is not a new authority over memory.  
**Session management** — Lesson session ≠ auth session, but both can end. Ending auth ends capabilities.  
**API security** — Smallest payload. No utterance fields. Versioned errors.  
**Supply chain** — Dependencies we own. No surprise models in the client.  
**Infrastructure security** — Tenancy isolation. No shared scrap that becomes data.  
**Threat modeling** — Required when a change touches children, memory, voice, or export.  
**Audit trails** — Access and forget and export. Not speech.

---

# Volume VIII — Privacy Architecture

**Consent** — Separate capabilities. Needful time. Revocable. Receipts stored.  
**Memory** — Listed. Projected. Never raw mouth as memory.  
**Data minimization** — If a feature can run on an id and a state, it does not get a paragraph.  
**Deletion** — Product-complete. Backup-aged. No teaching on deleted fields.  
**Retention** — Default short for media and operational live flags. Learning retained as licensed. Speech not retained by default.  
**Export** — What they are owed. Privacy-safe. No secret dossier.  
**Regional compliance** — Data residency as contracted. Architecture allows region; demos do not waive it.  
**Child privacy** — Extra review. No A/B on safety or forget. No study without protocol.  
**School privacy** — DPA before roster. Teachers are not a loophole for tapes.  
**Enterprise privacy** — Aggregates. Control plane without speech toys.  
**Research data** — Isolated workspace. Consent distinct from product consent. No vanity join.

Privacy is a shape of storage, not a banner.

---

# Volume IX — Platform Governance

**Architecture reviews** — A change that touches host, voice path, memory, routing, or forget requires a review against this file.

**RFC process** — Written. Named layer, data class, owner, failure mode, privacy shape. No RFC, no kernel change.

**Breaking changes** — Continuity of the person is not breakable. APIs may version. The host id may not reset as a migration trick.

**Deprecation** — Replacement named. Dual run if memory or session is involved. Then retire.

**Ownership** — Service owners and layer owners. Vacancy is an incident.

**Documentation** — How to fail, forget, add a guest, export. Not a graveyard of sprints.

**Technical decisions** — Recorded. Dissent recorded. Constitution wins conflicts.

**Versioning** — Guests, prompts, content, APIs. A guest without a curriculum version is not deployable.

**Platform standards** — Logging without content. Tests for fail-closed and forget. Flags not on safety.

**Migration strategy** — Move state, not speech we do not keep. Prove return-without-restart on a real account before declaring done.

---

# Volume X — Future Platform

2050. Clouds have other names. Models have other shapes. Devices have other senses.

What remains:

There is a person with a stable identity.  
There is a host that does not get replaced by a guest.  
There is a license on memory, visible and erasable.  
There is one path for the living voice in the room.  
There is a planner that picks one next move.  
There is a safety mouth in front of every mouth.  
There is a way to fail that keeps the room.  
There is no lake of children speaking.

The metal will change. The vendors will change. The size of context windows will change.

If we store what we swore we would not store, the platform has already died, even if the uptime graph is green.  
If we can swap every model and the person is still not a stranger, the platform has lived.

Architecture is the promise that the hall can be rebuilt without evicting the people inside it.

That promise is the only future-proofing that matters.
