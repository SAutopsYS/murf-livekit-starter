# 12 — Performance Standard

Performance before visual effects. A pretty jank is a defect.

---

## Frontend budget

| Item | Target |
|---|---|
| First useful interaction on welcome | < 2s on a mid phone, mid network |
| JS shipped to `/` | Avoid new heavy libs on the hall route |
| Wave | 60fps; drop points before adding blur |
| Theme / navigation | 180–320ms, no layout thrash |
| Analytics/enterprise poll | Single-flight; pause when `document.hidden` |

## Backend budget

| Item | Target |
|---|---|
| Tool local path (score, local exercise) | p95 < 200ms in-process |
| Memory lookup | Async as today; do not block greeting |
| Fail-closed handback | Immediate; no retry storm |
| CLI snapshot for enterprise | Seconds, not a hang; no speech scan |

## Bundle size

Do not add Three.js, extra font families, or a second animation runtime to `/`.  
Route-split `/analytics` and `/enterprise` (already separate pages).  
A third typeface is a defect ([07](07_DESIGN_SYSTEM_BIBLE.md)).

## FPS

Wave and CSS transitions: 60fps.  
If a device cannot hold it, reduce visualizer complexity — do not add a GPU toy.

## Animation rules

[03 Motion Bible](03_MOTION_BIBLE.md).  
`prefers-reduced-motion: reduce` → no duration, state only.  
No continuous aurora behind the try.

## API response targets

Next `/api/token`: fast path; do not add extra LLM calls.  
`/api/analytics` and `/api/enterprise`: existing execFile pattern; do not widen payloads with content fields.

## Streaming targets

First useful audio: a human pause, not a lecture.  
This is the SLO that outranks dashboard TTI.  
Reconnect restores the same room; do not pay a second full handshake costume in UI.

## Lazy loading rules

Lazy-load instruments, not the session kernel.  
No suspense flash that looks like a new hello.

## Caching rules

HTTP cache: not for tokens as if they were public pages.  
Redis (future): live flags only.  
Never cache transcripts.  
Tool request cache stays bounded (existing).

## Optimization checklist

- [ ] No new dependency on the hall route without a budget note  
- [ ] Images: SVG marks, no 4K hero  
- [ ] Polling pauses when hidden  
- [ ] Motion tokens, not unbounded springs  
- [ ] Backend change does not block greeting on a sync disk hit  
- [ ] Measured or reasoned — not “it feels fine on my laptop”  

See [04 Frontend](04_FRONTEND_CONSTITUTION.md), [05 Backend](05_BACKEND_CONSTITUTION.md).
