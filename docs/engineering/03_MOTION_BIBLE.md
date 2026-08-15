# 03 — Motion Bible

Every animation explains state. Never animate for decoration.

Law: Design System Volume VIII, Experience Blueprint.  
Tokens: `--salora-duration-short` (180ms), `--salora-duration-medium` (320ms), `--salora-ease-enter`.

---

## Motion philosophy

Motion is a verb: **arrive, leave, confirm, fail-closed, progress, takeover**.  
If you cannot name the verb, delete the motion.  
One motion at a time on the attempt.

## Timing rules

| Verb | Duration | Notes |
|---|---|---|
| Arrive (primary) | 320ms | Fade + short rise. No bounce |
| Leave | 180–320ms | Get out of the way. Last good state remains |
| Confirm (press) | 180ms | Scale 0.98 on active |
| Progress (determinate) | Linear to true proportion | Never fake |
| Consequence (forget, takeover) | Up to 400ms | Must be noticeable |
| Connecting hold | Copy + existing fade | Not a brand film |

## Durations

- Short: 180ms — press, focus ring, badge  
- Medium: 320ms — panel arrive, welcome stagger  
- Consequence: 400ms max  
- Welcome stagger delays (75–700ms) are allowed once on first paint. Do not restagger on resume.

## Easing

`--salora-ease-enter`: cubic-bezier(0.22, 1, 0.36, 1) — decelerate into rest.  
Linear only for determinate progress.  
No overshoot on errors or on children.  
No spring that bounces a miss.

## Physics

We do not simulate juice. Mass and bounce are not pedagogy.  
Wave visualizer is driven by **real audio energy** (existing LiveKit wave). Do not invent a second liquid engine that ignores the track.

## State transitions

| From → to | Motion |
|---|---|
| Welcome → connecting | Leave welcome, arrive connecting copy |
| Connecting → session | Wave becomes the living core |
| Session → ended | Leave session, arrive ended panel |
| Resume | No new hello animation |
| Guest handoff | Named change of presence — not a reconnect costume |
| Fail-closed | Still, high contrast. **No shake** |

## Voice state animations

Map to existing agent states. Do not add a second state machine in CSS.

| State | Motion meaning |
|---|---|
| Idle | Wave at rest, low amplitude |
| Listening | Energy follows mic input |
| Thinking / processing | Hold, do not theater a brain |
| Speaking | Energy follows agent audio |
| Routing / handoff | Same wave family; copy may name the guest |
| Returning | Same room. No origin burst |
| Offline | Banner, not a spinner personality |

Phase 4/5 enrich these **on the existing visualizer** via `VoiceCore` + `deriveVoiceSnapshot`. They may not replace LiveKit audio. See [17](17_VOICE_ARCHITECTURE.md) and [18](18_LIVING_AI_CORE.md).

## Micro interactions

Hover: 180ms opacity/border. Never the only affordance.  
Press: 0.98 scale on `btn-premium`.  
Focus: ring using pulse.  
Drag: not used on the attempt. If used on instruments, labeled cancel.

## Reusable primitives (Phase 2)

CSS: `.motion-fade`, `.motion-rise`, `.motion-scale`, `.motion-slide` in `globals.css`.  
JS: `Fade`, `Rise`, `Scale`, `Slide`, `Reveal`, `Expand`, `Collapse`, `PageTransition`, `CardTransition`, `DialogTransition`, `ListAnimation` from `@/components/system`.  
All honor `prefers-reduced-motion`.

## Page transitions

Hierarchical (push/pop) matches Back. Crossfades that erase “where I am” are forbidden.

## Performance budget

See [12 Performance Standard](12_PERFORMANCE_STANDARD.md).

- 60fps on the wave on a mid phone, or reduce points — do not add blur stacks  
- `prefers-reduced-motion: reduce` → duration 0, opacity/state only  
- No continuous background animation behind a try  
- No extra WebGL unless it replaces nothing and stays under budget  

A motion that drops first useful audio is a defect.
