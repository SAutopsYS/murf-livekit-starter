# SALORA OS — Engineering Constitution

Phase 12.

Not coding guidelines.  
Not a style guide.  
Not a framework catechism.

The permanent Engineering Constitution for every repository that touches SALORA.

Platform Architecture named layers.  
Infrastructure named metal.  
This file names how software is made, reviewed, tested, and released so the person is not restarted and not exposed.

If a change cannot name the layer, the data class, the test that proves fail-closed or forget, and the owner of the night, it does not merge.

---

# Volume I — Engineering Philosophy

**Continuity is the feature** — Resume without a new hello is not polish. It is the product.

**Honesty in names** — `handoff` is not `reconnect`. `memory` is not `transcript`.

**Smallest honest change** — Reversible. Except privacy and safety, which are not experiments.

**One pipeline** — A second voice path is not an experiment. It is an incident.

**Tests before trust** — Fail-closed, handback, forget, privacy logs, no-restart. If it touches them, the tests exist in the same change.

**Refuse cleverness that hides** — A smart abstraction that smuggles speech is not smart.

**Human-readable failure** — Structured errors. No stack in the lesson.

**Docs for the 3 a.m.** — How to fail, forget, add a guest. Not a Day-N graveyard.

---

# Volume II — Software Architecture

**Kernel** — Host, session continuity, license, stop, fail-closed.

**Guests** — Registered, versioned, subgraph, way home. No guest-of-guest.

**Clients** — Views of the OS. They do not mint a second tutor. They do not store a tape.

**Contracts** — Small payloads. Versioned. No utterance fields.

**Flags** — Real for risk. Safety and forget are not flag-optional in production.

**Modularity** — Compose. Do not fork the kernel for a demo.

A new repo that speaks to a learner obeys this file or it is not ours.

---

# Volume III — Backend Engineering

**Services** — One purpose. One owner. One data class primary.

**APIs** — Least fields. Authz on the server. Structured errors.

**State** — Session state dies unless promoted. Learning state is not a mouth.

**Jobs** — Idempotent. No speech summary into the graph.

**Compatibility** — The person is not a breaking change. APIs may version.

**Local** — A developer can run the host path without a child’s data.

---

# Volume IV — Frontend Engineering

**One OS** — Web is the OS, not a brochure.

**Tokens** — Design tokens only. Magic numbers are drift.

**No hover-only** — Keyboard path in the same change.

**Confirm** — Deep link and search do not steal a live attempt.

**No transcript UI** — If the field does not exist, the screen cannot invent it.

**Performance** — First useful interaction. Polling single-flight. Pause when hidden.

**Accessibility** — Labels, focus, contrast, reduced motion. Same PR.

---

# Volume V — Mobile Engineering

**Core on a small phone** — Attempt, stop, voice, back.

**Takeover** — Second device asks. Does not fork.

**Cache** — Licensed snapshot and last lesson. Encrypted. Expiring.

**Sensors** — Optional. Camera never required to learn. No silent capture.

**Stores** — Official stores do not excuse a second pipeline.

**Background** — Audio only if they chose it and can still Stop.

---

# Volume VI — AI Engineering

**Seats** — Host and guests. Pins. Prompt hierarchy. Lower cannot cancel higher.

**Tools** — Schema in, schema out. Fail spoken as tool fail.

**Eval in CI** — Safety, honesty, recovery gates where we can automate. Live listen still required for voice seats.

**No prompt in logs** — Event names. Route ids.

**No invented curriculum** — Drafts are drafts. Publish is human.

**Model files** — Supply chain. No surprise weights in a client.

---

# Volume VII — Infrastructure Engineering

Obeys Phase 11.  
As code: reproducible, reviewed, least privilege.  
A terraform surprise that opens a public bucket is an incident, not a shortcut.

---

# Volume VIII — Testing Architecture

Required when the change can touch them:

- No new hello on resume
- Reconnect ≠ handoff
- Guest fail → host, one retry, no loop
- Forget completes; teaching cannot resurrect
- Logs have no utterance, phone, OTP, secret
- Offline honest
- Authz cannot be bypassed in the client
- Tokens and labels for new controls

LLM-as-judge tests may exist for teaching quality. They do not replace the above.

A red privacy test does not merge.

---

# Volume IX — Code Review

Reviewers answer, not vibe:

- What law does this obey?
- What data class is new?
- What is the fail path?
- Is a transcript-shaped field present?
- Are tests in the same change?
- Is the name honest?

Approval is not a like.  
“We’ll add tests later” on kernel paths is a refuse.

---

# Volume X — Release Engineering

**Pin** — Model, prompt, guest, content, client.

**Progressive** — Sandbox, internal, pilot, prod. Child-facing guests do not skip pilot.

**Rollback** — First-class. A launch that skipped review rolls back.

**Migrations** — Move state, not speech we do not keep. Prove return-without-restart on a real account shape before done.

**Hotfix** — Still no utterance field. A hotfix that bypasses AI evaluation for a speaking model is an incident.

---

# Volume XI — Documentation

**In repo** — How to run, fail, forget, add a guest, export.

**Decisions** — ADR. Dissent recorded.

**No graveyard** — Dead Day-N docs are archived.

**No child examples** — Synthetic only.

---

# Volume XII — Performance Engineering

**p95 first useful audio** — A product number.

**Budgets** — Cheap phone, low bandwidth. Beauty that costs the try is not beauty.

**N+1 and polls** — Single-flight. Hidden tab pauses.

**Load** — School-day shape. Do not load-test with real child data.

---

# Volume XIII — Secure Engineering

Obeys Phase 13.  
In every change: least privilege, no secrets in repo, server-side authz, threat model when children, memory, voice, or export move.

---

# Volume XIV — Future Engineering

New languages and runtimes are allowed.  
They inherit kernel, tests, and the ban on a second pipeline.  
A future that generates all code still cannot generate a tape or a publish of curriculum.

---

# Volume XV — Engineering Manifesto

We write so a person can continue.

Cleverness that restarts them is incompetence. Speed that leaks them is harm. A clean abstraction that lies about memory is a lie.

The repository is not a playground. It is the floor of a hall where a child may speak. We will merge less, name honestly, test the refuse, and leave the next engineer able to find the way home.

What must never change: one pipeline, tests for forget and fail-closed, no utterance fields, pins in production, review that can refuse, docs for 3 a.m.

Stay on the line. Merge the duty. Not the demo.
