# 51 — SALORA OS v2 Vision

No implementation. Roadmap only. Phases 1–39 stay the kernel.

---

## Long-term architecture

v2 adds **clients and loops**, not a second OS. Search, automation, RBAC, voice, and router remain singular.

Vision themes (conceptual): autonomous AI teams, distributed agent networks, robotics, IoT, cross-device intelligence, ambient computing, multi-modal workspace, quantum-ready *as a thought experiment*.

None of these may introduce a second STT/TTS or an utterance column.

---

## Evolution strategy

1. Consume contracts (`ApiEnvelope`, `can()`, `SearchService`, `AutomationService`).
2. Flip sandbox flags only with an explicit product decision (`may_execute`, `may_autonomous_loop`).
3. Add providers through `ProviderRegistry`, not forks of `agent.py`.

---

## Backward compatibility

`API_VERSION=v1` is frozen. Breaking changes are `v2` envelopes. SQLite schema laws do not relax.

---

## Platform stability rules

- one voice path
- one router
- one search
- one automation
- one RBAC
- no utterance column
- consume, do not rewrite

---

## Future expansion guidelines

A new mentor is a specialist + runtime manifest. A new industry is a `IndustryProfile`. A new client is Mobile/Desktop contracts. A new region is a compose profile.

---

## Five-year roadmap

| Year | Focus |
|---|---|
| 1 | Identity, queue, Studio/Whiteboard/Graph instruments |
| 2 | Public API + signed plugins + Redis rate limits |
| 3 | Multi-region + compliance certifications (not HIPAA by default) |
| 4 | Mobile/desktop implementations of existing contracts |
| 5 | Optional autonomous teams **behind** the sandbox, still one mouth |

---

## Final roadmap (Phase 1–40)

| Band | What |
|---|---|
| 1–10 | Brand, design, OS shell, voice, living core, learning, adaptive, fabric, production |
| 11–20 | Backend platform, Studio, Whiteboard, Graph, Marketplace, Enterprise, SDK, Collab, Agent runtime |
| 21–30 | Search, automation, productivity, clients, governance, cloud, v1 freeze |
| 31–40 | Education UX, mentors, industry solutions, public API, infra, deploy, compliance, optimization, ecosystem, **v2 vision** |
