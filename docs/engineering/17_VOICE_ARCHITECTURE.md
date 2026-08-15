# 17 — Voice Architecture

Phase 4: one voice state machine on the existing LiveKit session.  
The wave, Murf, and transport are not replaced.

Living Core visuals: [18 Living AI Core](18_LIVING_AI_CORE.md).  
Motion law: [03 Motion Bible](03_MOTION_BIBLE.md).

---

## Decision

LiveKit remains the transport.  
`deriveVoiceSnapshot` is the only mapper from LiveKit + network + mute + transfer → `VoicePhase`.  
UI reads `useVoice()`. It does not re-switch on `agent.state`.

---

## Lifecycle

```
disconnected → connecting → ready/idle
                           → listening → thinking → speaking → idle
                           → muted | paused | routing | returning
                           → disconnecting → disconnected
offline and error can interrupt any connected phase
```

| Lifecycle | When |
|---|---|
| disconnected | Not in a room |
| connecting | LiveKit `Connecting` or agent initializing |
| ready | Connected + idle |
| listening / thinking / speaking | Agent states |
| idle | Connected, waiting |
| offline | `navigator.onLine === false` |

ViewController still owns **screens** (welcome / connecting / session / ended / mic-error).  
The machine owns **in-session meaning**. Do not merge those two jobs.

---

## State machine

`VoicePhase`: idle, connecting, connected, listening, thinking, speaking, paused, routing, returning, muted, disconnected, offline, error.

Priority (highest wins): error → offline → connecting → paused → routing → muted → agent activity → idle → disconnected.

Source: `frontend/lib/voice/derive.ts`.  
Table: `frontend/lib/voice/visual-language.ts`.

---

## Event flow

`useVoiceActions().subscribe(fn)`.

| Event | Cause |
|---|---|
| PhaseChanged | Any phase change |
| SessionStarted / SessionEnded | Enter/leave a live line |
| ListeningStarted / Stopped | Phase listening |
| ThinkingStarted / Finished | Phase thinking |
| SpeakingStarted / Finished | Phase speaking |
| MuteChanged | Enter/leave muted |
| AgentTransferred | `reportAgentTransfer` |
| ReconnectStarted / Finished | Connecting transitions |
| NetworkChanged | Online/offline |

Listeners are a ref Set. They do not rerender the provider.

---

## Session architecture

```
App
  AgentSessionProvider     LiveKit kernel
    VoiceProvider          one snapshot + event bus
      ViewController       screens
        AgentSessionView   badge + stage + transcript + controls
```

`reportAgentTransfer({ source, destination, reason, confidence, durationMs, timestamp })`  
`clearAgentTransfer()`  
Specialist router on the backend stays. This is the frontend socket for a named guest.

---

## Component hierarchy

| Module | Job |
|---|---|
| `VoiceProvider` | Subscribe once. Derive. Emit. |
| `useVoice` | Snapshot |
| `useVoiceActions` | Bus + transfer + pause |
| `VoiceLiveRegion` | Screen reader |
| `VoiceCore` | Visual host (Phase 5) |
| `VoiceOverlay` / `VoiceFeedback` / `VoiceIndicators` | Shared chrome |

Do not add a second provider that remaps `useAgent()`.

---

## Accessibility

- `aria-live="polite"` on badge and live region
- Labels come from `visual.label` / `visual.meaning`
- Reduced motion zeros core CSS
- Fail-closed: still, no shake
- Keyboard: existing control bar. Do not steal focus for animation

---

## Performance

- Snapshot memoized. Actions context is stable.
- Events fire only on phase change.
- Wave still uses `useTrackVolume` inside the existing hook. Do not put FFT in React context.
- Audio latency is LiveKit’s. This layer is CSS + derived strings.

---

## Future Orb / multi-agent

Orb, rings, neural pulse: **renderers** that read `visual.colorToken`, `visual.motionToken`, `phase`.  
They replace `VoiceCore` internals, not `deriveVoiceSnapshot`.  
Handoff visualization: subscribe to `AgentTransferred`. Do not invent a second router.
