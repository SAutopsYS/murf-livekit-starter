# SALORA OS — Core Platform Blueprint

Stage B.

The Constitution is the law.  
The Product Blueprint is the products.  
The Implementation Foundation is how software is built.

This file is the permanent core platform every present and future SALORA application depends on.

Not an API reference.  
Not a database schema.  
Not a microservice catalog.

Every engineer reads this before implementing a business capability.

Stage A named the tree and the two runtimes.  
This file names the shared capabilities that live in `services/api` (and supporting infra) so `apps/web`, `apps/mobile`, operator surfaces, and `services/voice` do not invent a second identity, a second notifier, or a second search.

Learning execution is Stage C.  
Voice transport remains `services/voice`. This platform does not grow a second mouth.

If a capability is used by more than one product and is not in this file, it is duplication. Extract it or amend this file.

---

# Volume I — Platform Philosophy

**Platform before products**  
A product may not mint a private login, a private file store, or a private event bus. If it needs a shared act, it calls the platform.

**Shared capability over duplication**  
Two implementations of “invite a parent” are a defect. One contract, many callers.

**Learner-first infrastructure**  
The platform exists so a person is not restarted and not exposed. Capacity and queues are judged by host path, forget, and leak absence.

**Services as public contracts**  
Callers depend on contracts in `packages/contracts`, not on a neighbor’s tables.

**Fail safely**  
A down notifier does not take the lesson. A down search does not take Stop. A down guest registry fails toward the host, not a hang.

**Modular evolution**  
A domain may split when it has one purpose and one owner. It may not split to hide a tape.

**Constitutional compliance**  
No utterance field. Guest ≤ host ≤ consent. Tenancy on every learner-shaped row.

**Stable APIs**  
The person is not a breaking change. Version. Dual-run if memory or session is involved.

**Independent deployment**  
API, worker, voice, web, mobile pin and ship on their own clocks. A web deploy does not fork a live voice session.

**Long-term platform stewardship**  
Named owners. Vacancy on identity, forget, or audit is an incident.

---

# Volume II — Platform Architecture

## Layers

1. **Edge** — Gateway, authn, rate limit, tenancy stamp.  
2. **Core services** — Identity, organization, user, session/device.  
3. **Shared services** — Communication, media, search, scheduling, integration, events.  
4. **Domain services** — Learning engine (Stage C), knowledge/content, assessment records, enterprise projections.  
5. **Infrastructure services** — Secrets, observe, backup. Not product logic.

Voice runtime sits beside the edge as transport. It is not a layer that owns users.

## Boundaries

**Public interfaces** — Versioned HTTP/GraphQL for apps and partners. Smallest payload.

**Internal interfaces** — Service-to-service with workload identity. Same forbidden fields.

**Event bus** — Domain and integration events. Names from Data Constitution. No speech payloads.

**Service contracts** — In `packages/contracts`. Errors structured. Idempotency keys on writes that can double.

**Dependency rules**

```
apps → core + shared + domain (via SDK)
voice → core (identity/session) + domain (learning/memory) via API
domain → core + shared
shared → core
core ↛ domain
shared ↛ domain
voice ↛ other services’ databases
```

A domain service that reaches into Identity’s tables is a defect.  
A product that embeds SMTP is a defect.

---

# Volume III — Identity Platform

Identity is the foundation of every interaction. One person, one id, many roles.

**Authentication** — Prove the door. Password, SSO, school IdP. Auth session ≠ lesson visit. MFA for stewards.

**Authorization** — Server RBAC + relationship checks (`teaches`, `cares-for`, `enrolls`). UI is not the control.

**Organizations** — Tenancy root (school, university, enterprise, NGO). Policy and residency live here.

**Schools / teachers / students / parents / enterprises** — Memberships, not separate people. A teacher may also be a learner. Switching workspace does not mint a new id.

**Devices** — Registered. Takeover confirm. Not a new authority over memory.

**Sessions** — `AuthSession` and `LessonVisit` are different objects. Ending auth ends capabilities. Ending a visit does not end the person.

**Permissions** — Capability flags. Guest agent is not a human role. Camera never required to learn.

**Roles** — `learner`, `parent`, `teacher`, `school_admin`, `enterprise_admin`, `researcher`, `operator`.

**Invitations** — Typed edge + expiry. Broken invite re-sends without exposing the child.

**Account recovery** — Recovers the account, not a forgotten memory field.

No shared child logins as culture.  
No face as identity to learn.

---

# Volume IV — Organization Platform

Institutional boundaries. Outcomes, not tapes.

**Organizations** — Legal and policy container.

**Campuses / departments** — Optional hierarchy. Do not become a second tenancy of speech.

**Classrooms** — Roster, assignments, pulse. Presence visible. No silent observers.

**Groups / cohorts** — Time-boxed or standing. Exit is first-class for voluntary groups.

**Membership** — Typed, dated, revocable.

**Ownership** — Who may assign, override a guest, export, offboard.

**Hierarchies** — Org → campus → department → classroom. Queries do not walk into a mouth.

**Invitations** — Same as Identity, scoped to an org object.

**Governance** — Retention, who can see projections, who can start a guest in a child’s path (through the host, never around it).

When an org leaves: export what they are owed. No shadow graph from speech.

---

# Volume V — User Platform

Every learner owns one identity. Profile is not a social page.

**Profiles** — Chosen name, age band as required, nothing inferred they did not grant.

**Preferences** — Pace, session length, voice or type. Not a “visual learner” doctrine.

**Languages** — Locale and script. Hindi → Devanagari. Switch confirms if an item is live.

**Accessibility** — Type size, reduced motion, captions, input mode. First-class, not a lesser flag.

**Goals** — Pointers to Goal Engine (Stage C). User platform stores that they exist, not a secret life plan.

**Time zones** — Scheduling truth. Not a tracking toy.

**Notification preferences** — Quiet default. Marketing never.

**Learning identity** — The same person on the graph. Not a second dossier.

**Privacy settings** — License, projections, export, delete. Forget completes here.

**Device management** — List, revoke, takeover history without content of lessons.

---

# Volume VI — Communication Platform

Communication supports learning. It is not a second tutor.

**Notifications** — One fact, one optional action. Life-safety may break quiet.

**Email / push / SMS** — Same template law. SMS only when needed (invite, recovery). No lesson body in SMS.

**In-app messaging** — Teacher-to-class and support. Not a child feed. Not a tape.

**Announcements / broadcasts** — Org-scoped. Dismissible unless safety.

**Preferences** — Honored. Quiet is valid.

**Delivery status** — For operators. Not a read-receipt of a child’s fear.

**Templates** — Language System. Speakable. No urgency costume. No child anecdote.

A down comms service does not block Stop or resume.

---

# Volume VII — Media Platform

Media remains independent from learning logic.  
A file is not a lesson until Content binds it (`presents`).

**File storage** — Object store. Encrypted. Tenancy prefixed.

**Images / videos / audio / documents** — Typed. Captions required if video teaches. Audio may be a lesson twin, not a recording of the room by default.

**Upload pipeline** — Virus, type, size, license check. No silent camera upload.

**CDN** — Public twins only. Private memory edits do not go to a shared TV CDN.

**Metadata** — License, version, locale, accessibility twin pointer. Not “what they said about it.”

**Versioning** — `supersedes`. Mid-try swap forbidden without a written rule.

**Licensing** — No stolen book. Attribution stored.

Lesson tapes are not a media type we offer.

---

# Volume VIII — Search Platform

Search discovers. It never owns curriculum or identity.

**Global search** — Taxonomy objects the role may see. Confirm before leaving a live attempt.

**Content / knowledge / curriculum** — Ids from those graphs. Graph constraints forbid retired, wrong age, no evidence.

**User search** — Roster-scoped. Not a people browser across tenancies.

**Semantic search** — Index over objects we have. A neighbor is a candidate, not a citation.

**Filtering / ranking** — Educational fit, locale, pin, quality. Popularity last or absent.

**Suggestions** — Command palette twin. Same confirm rule.

**Indexing** — From live objects. Forget and retirement drop the id. We do not index mouths.

Empty is a first-class result.

---

# Volume IX — Scheduling Platform

Time supports continuity. It does not threaten a streak.

**Calendar** — Due revisions, assigned sessions, meetings they set.

**Sessions** — Pointers to lesson visits and live rooms. Not a second session object that forgets the host.

**Events / reminders / deadlines** — Quiet. One fact.

**Learning schedule** — Written by Goal and Practice engines (Stage C). This platform stores time and timezone.

**Teacher availability / parent meetings** — Optional. Presence visible.

**Time zones / recurrence** — Honest. Exam dates they gave may tighten a path. They may still stop.

A reminder is not a warden.

---

# Volume X — Integration Platform

Integrations extend. They do not redefine the host, the license, or fail-closed.

**OAuth / SSO** — Identity door. Not a biography harvest.

**LMS / SIS** — Roster, enroll, assignment and outcome pass-back. Least fields. No lesson pipe.

**Video platforms** — Content twins. Not a proctor camera. Not required for Core.

**Payment providers** — Entitlements. Written failed-payment policy. No child humiliation SKU.

**Cloud storage** — Licensed resources they meant to keep.

**Calendar systems** — Due and meetings. Not streak threats.

**Webhooks** — Event names, not content. Retry-safe.

**Public APIs** — Partner contracts. Same forbidden fields. Sandbox first.

Vendor outage fails toward the host. Dual-write of one attempt is a defect.

---

# Volume XI — Platform Events

Every service communicates through defined contracts.

**Event bus** — Internal. Not a place to park audio.

**Domain events** — `IdentityInvited`, `ForgetCompleted`, `VisitResumed`, `GuestFailedClosed`. Past tense. Ids, not bodies.

**Integration events** — Outbound to LMS/SIS. Outcomes, not utterances.

**Contracts / versioning** — In `packages/contracts`. Additive first. Break = new version.

**Idempotency** — Keys on producers and consumers. Sync must not duplicate an attempt.

**Retry / DLQ** — Bounded. Poison to humans. No retry storm into a child’s phone.

**Event auditing** — That an event was emitted and consumed. Not a replay of a mouth.

Voice runtime may emit `VisitResumed`, `GuestEntered`, `FailClosed`. It may not emit `UtteranceHeard`.

---

# Volume XII — Platform Security

Obeys Security & Privacy Constitution. Platform-shaped:

**Identity security** — Workload identity between services. No god keys in scripts.

**Secrets** — Manager. Rotation. Not in git.

**Service authentication** — mTLS or signed service tokens. Apps do not call internal ports.

**API security** — Authz on server. Least payload. Versioned errors.

**Rate limiting** — At edge. Learner attempt is not starved by an enterprise poller.

**Audit logs** — Access, export, forget, admin. Not transcripts.

**Encryption** — In transit and at rest.

**Tenant isolation** — Every query stamped. Cross-tenant is an incident.

**Zero trust** — Internal is not trusted because it is internal.

**Security monitoring** — Route anomalies, public buckets, failed forget. Not “interesting lessons.”

---

# Volume XIII — Platform Operations

**Service discovery** — Internal. Clients use the gateway.

**Health checks** — Can auth work? Can forget complete? Can we emit events without a mouth?

**Scaling** — School-day peaks. Host/voice fleet preempts costume jobs.

**Failover** — Degrade map: comms down ≠ lesson down. Search down ≠ Stop down.

**Monitoring** — Host SLO still the SLO. Platform SLIs: auth success, invite success, forget completion, event lag.

**Backups** — Restore identity, orgs, licenses. Not a lake.

**Maintenance** — Announced. Live visits do not become stranger greetings.

**Incident recovery** — Sev-1 law.

**Service lifecycle / deprecation** — Replacement named. Dual-run if identity or session involved. Memory and Stop cannot be deprecated.

---

# Volume XIV — Platform Evolution

**New services** — One purpose, one owner, one data class, a contract, a fail path. Amendment if they are shared.

**New domains** — Stage C and later stages plug in. They do not fork Identity.

**Service splitting** — Allowed when a context is a real boundary. Forbidden as a way to hide fields.

**Platform migration** — Move state, not speech we do not keep. Prove return-without-restart.

**API evolution** — Version. The person is not the breaking change.

**Multi-region** — Residency capable. Forget completes where they live.

**Edge services** — Cache and auth near the person. Must still forget. No edge tape.

**AI-native platform** — Seats call this platform. The platform is not a model. A model is not an admin.

**Future integrations** — Same refuse: no transcript capability that does not exist.

**Backward compatibility** — A learner from a decade ago can sign in and not be a stranger.

Evolution never breaks Volume II of the Master Constitution.

---

# Volume XV — Platform Manifesto

Platforms exist to enable products, not to compete with them.

A platform that grows a Home feed to justify itself has become a product in costume. This platform has no personality. It has doors, stamps, clocks, and a refuse. Products bring the lesson. The platform keeps the person one person.

Shared capabilities create stronger systems than isolated applications because a forget that works in one app and fails in another is not forget. It is a lie with two codepaths. We will have one forget, one invite, one search confirm, one quiet notifier.

Service contracts matter more than implementations. Nest may leave. Postgres may leave. The contract “forget completes and teaching cannot resurrect” does not leave.

Infrastructure should disappear behind learning. The learner should not know the bus. They should know the next item and Stop. When they must know the bus, we have leaked our architecture into their working memory.

Platform stability is a promise to every learner: the id they had, the license they gave, the visit they paused, will still mean the same tomorrow.

What must never change:

One identity.  
Auth session ≠ lesson visit.  
No utterance on the bus.  
Search does not own truth.  
Media is not a tape.  
Integrations do not redefine the host.  
A down shared service does not take the attempt.  
Forget is a platform act, not a product plugin.

Stay on the line.  
Share the door.  
Do not share the mouth.
