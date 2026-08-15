# SALORA OS — Platform & Infrastructure Constitution

Phase 11.

Platform Architecture (04) named layers and service boundaries.  
This file names the metal and the weather: how compute, storage, network, and recovery keep the hall standing.

Not cloud documentation.  
Not a vendor runbook.  
Not DevOps fashion.

The permanent Platform and Infrastructure Constitution.  
Infrastructure, platform engineering, SRE, security, and operations follow this file.

A cloud may be replaced. A region may be added. The duties in this file may not.

If a cluster, bucket, or queue cannot name the data class it holds, the service it serves, and the failure that keeps the host, it is not infrastructure. It is drift.

---

# Volume I — Platform Philosophy

Infrastructure exists so a person is not restarted and not exposed.

**Continuity over cleverness** — A boring host path that stays up beats a clever mesh that drops the room.

**Absence over policy** — Do not provision a speech lake “in case.” What does not exist cannot leak.

**Vendor humility** — Clouds are guests. We do not marry a brand. Contracts and IAM are ours.

**Region as duty** — Residency is architecture, not a slide. A demo does not waive it.

**Degrade, do not lie** — Offline is a mode. A dead guest is a host sentence. A hang is a defect.

**Human-centered capacity** — We scale first useful audio and school-day peaks, not vanity throughput.

**One pipeline** — Voice transport is one path into the room. A second path is an incident.

**Owned secrets** — Keys are not in the tree, not in the image, not in the trace.

---

# Volume II — Infrastructure Architecture

Permanent kinds of infrastructure. Implementations change. Kinds do not.

**Edge** — Clients and caches. Licensed snapshot and last lesson. Encrypted. Expiring. No second tutor.

**Transport** — The one voice path. Reconnect is the same room. Not an archive.

**Compute** — Stateless workers for request and session work. Sticky only where the live attempt requires it — and then takeover is still one session.

**Data plane** — Operational, learning, memory, content, audit stores. Separate classes. No mixed bucket.

**Control plane** — Tenancy, flags, pins, guest registry. Safety and forget are not optional flags.

**Identity plane** — Users, agents, services. Host id stable across deploys.

**Observe plane** — Metrics, traces of route, logs without content. Not Memory.

**Recover plane** — Backups, restore drills, region fail. Restore identity, license, learning state, content. Do not restore a lake we refused to have.

A new kind requires an amendment. A new vendor does not.

---

# Volume III — Cloud Architecture

A cloud is a landlord. We are the tenant with a law.

**Multi-region capable** — Architecture allows residency. Where contracted, data stays.

**Blast radius** — Tenancy isolation. A bad guest version does not take the host fleet. A bad tenant does not read another.

**No shared scrap** — Scratch that becomes a profile is forbidden.

**Exit** — We can leave a cloud with identity, license, learning state, and content. If we cannot, we are not tenants. We are captives.

**Managed services** — Allowed when they do not require a transcript field or a hidden replica we cannot forget.

**Accounts** — Prod, sandbox, research. No real child roster in sandbox. No production memory in research.

---

# Volume IV — Compute Architecture

**Session compute** — Serves the live attempt. Fail toward host. Scale on school-day. Preempt a guest before the host.

**Batch compute** — Evaluation, index, spacing. Never writes unlicensed memory. Never reads a mouth.

**Edge compute** — Optional for latency. Must still forget. An offline edge host that cannot forget does not ship.

**Jobs** — Idempotent. Named owner. No job that “summarizes speech into the graph.”

**Isolation** — Guest inference isolated from host. Tool runtime constrained. Unbounded code as a child’s identity is forbidden.

**Pins** — Model, prompt, guest, content versions pin on the compute that serves them. “Latest” is not a pin.

---

# Volume V — Storage Architecture

Storage is where privacy is won or lost.

| Store | Holds | Must not |
|---|---|---|
| Operational | Live session flags, takeover, idempotency | Utterances |
| Learning | States, due, item ids, class scores | Mouths |
| Memory | Licensed fields, receipts, deletions | Inferences they did not grant |
| Content | Packages, versions, media they meant to keep | Ambient home capture |
| Audit | Access, export, forget, admin | Transcripts |
| Analytics | Event names, timings, route ids | Content of speech |
| Backup | Encrypted copies of the above | A secret fourth copy of speech |

**Encryption** — In transit and at rest for every class that exists.

**Deletion** — Forget and account delete complete in product paths. Backups age out. Teaching systems may not resurrect a forgotten field.

**Object names** — Honest. A bucket called `tmp` that holds profiles is an incident.

---

# Volume VI — Networking

**Least path** — A service speaks only to what it must.

**Voice path** — One. Documented. Not branched into an analytics tap.

**No quiet mirror** — Packet capture of lessons is forbidden except a time-boxed incident with a named human and no retained payload.

**Public surface** — Small. Authz on the server. Tokens are not lessons.

**School networks** — Low bandwidth and intercepting proxies are expected. TLS stays. We do not require exotic ports to learn.

**Split horizon** — Research and prod do not share a flat network of data.

---

# Volume VII — Identity Infrastructure

**Human identity** — Stable. School SSO where contracted. No shared child logins as a workaround.

**Agent identity** — Host id does not change when a model changes. Guests have ids.

**Service identity** — Workloads authenticate. No long-lived god keys in a script.

**Device identity** — A new device is not a new authority over memory. Takeover is confirmed.

**Workload vs lesson** — Auth session ≠ lesson session. Ending auth ends capabilities. Ending a lesson does not have to end the person.

---

# Volume VIII — Observability

We see the route, not the mouth.

**Metrics** — Host start, fail-closed, first useful audio, forget completion, guest retry, error class, saturation.

**Traces** — Route ids, seat, tool name, latency. No prompt body. No utterance. No OTP.

**Logs** — Event names. Structured. No secrets.

**Alerts** — Truth: host down, leak class, forget fail, region fail. Not “engagement dip.”

**Dashboards** — Operators and Enterprise. No child as a row of speech.

**Access** — Observe plane is privileged. Admin is not a lesson viewer.

---

# Volume IX — Reliability Engineering

**Host SLO** — The SLO that matters. A green guest and a dead host is an outage.

**Error budget** — Spent on continuity and safety, not on costume launches.

**Degrade map** — Guest → host. Model → shorter host or human. Voice → type or honest stop. Network → offline truth.

**Chaos** — We may kill a guest in sandbox. We do not chaos a child’s official record.

**Toil** — Automate the repeat. Do not automate a policy change.

---

# Volume X — Scalability

**Scale the attempt** — Concurrent rooms, first audio, learning reads.

**Do not scale a lake** — We refused the lake.

**School-day shape** — Peaks are expected. Capacity plans name them.

**Tenancy** — Noisy neighbor contained.

**Indexes** — Retrieval scales over objects we have. Vectors are an index, not a second curriculum.

**Cost** — Cost per minute of real learning. A 10× bill for a 1% demo is refused.

---

# Volume XI — Disaster Recovery

**Restore what we keep** — Identity, license, learning state, content, audit.

**Do not restore what we refused** — A speech lake in a backup is a leak we scheduled.

**RPO/RTO** — Written per class. Host path recovers before instruments.

**Drills** — Restores are tested. A backup never restored is a story.

**Region fail** — Fail toward a host that still knows the license, or tell the truth.

**Ransomware / integrity** — Immutable backups where required. Forget still ages them.

---

# Volume XII — Security Infrastructure

Deep law lives in Phase 13. Here the metal:

**Segmentation** — Planes and tenancies.

**Secrets** — KMS, rotation, no tree.

**Supply chain** — Images signed. Dependencies owned. No surprise model in the client.

**Admin paths** — Break-glass named, logged, time-boxed. Break-glass is not a lesson view.

**Hardening** — Defaults closed. Public buckets are incidents.

---

# Volume XIII — Infrastructure Operations

**Change** — RFC for kernel (host, voice, memory, forget). Pins in prod.

**On-call** — Named humans for host, voice, memory, forget, leak.

**Access** — Least privilege. Time-boxed.

**Vendors** — Exit clause. Data class named. Forget honored or disconnected.

**Cost ops** — Visible. Costume spend is a product decision, not a surprise bill.

**Docs** — How to fail, restore, forget, isolate a guest.

---

# Volume XIV — Future Infrastructure

Clouds will change names. Devices will change senses.

What remains: one voice path, separate stores, residency capable, restore without a lake, edge that can forget, observe without a mouth.

A future fabric (edge mesh, orbital, on-school) inherits these duties or it does not carry a child.

---

# Volume XV — Platform Manifesto

The platform is the floor of the hall, not the show.

If the floor is quiet and strong, a tired tutor can still teach. If the floor is a maze of lakes and mirrors, no SRE can make it honest.

We will be boring where boring keeps a person. We will be strict where a bucket wants a name it does not deserve. We will leave every cloud able to be left.

What must never change: no speech store by default, one pipeline, forget that completes, host SLO first, keys out of the tree, a restore that does not resurrect a sin.

Stay on the line. Provision less. Keep the room.
