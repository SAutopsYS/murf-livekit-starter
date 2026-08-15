# 18 — Living AI Core

Phase 5: visual intelligence layer.  
It consumes [17 Voice Architecture](17_VOICE_ARCHITECTURE.md).  
It does not replace the LiveKit wave.

---

## Decision

The core is a **host**, not a second audio engine.  
`VoiceCore` wraps the existing `AudioVisualizer` (wave).  
Glow, ring, breathe, expand are CSS transforms driven by `data-phase` and `data-motion`.  
If you cannot name the verb, delete the motion.

---

## Architecture

| Module | Job |
|---|---|
| Core state | `useVoice()` snapshot |
| Core theme | `visual.colorToken` → `--voice-core-color` |
| Core motion | `visual.motionToken` → CSS |
| Core renderer | `VoiceCore` |
| Core events | `useVoiceEvent` |
| Core a11y | `VoiceLiveRegion` + overlay text |
| Core metrics | `VoiceFeedback` (mic / net / AI label) |

A future renderer (Orb, rings) implements the same host contract: wrap children, read snapshot, do not own LiveKit.

---

## Visual language

| Verb | Phase | Meaning |
|---|---|---|
| rest | idle / connected | Present, waiting |
| hold | connecting | Honest wait |
| breathe | thinking | Hold. No brain theater |
| glow / expand | speaking | Voice energy (wave still owns amplitude) |
| ripple | listening | Mic is live |
| compress | paused | Held, not reset |
| split | routing | Named guest |
| merge | returning | Host back, same room |
| still | muted / offline / error | Fail-closed |

Tokens live in `frontend/lib/voice/visual-language.ts`.  
CSS: `.voice-core*` in `frontend/styles/globals.css`.

---

## State mapping

Every phase exposes: color token, motion token, priority, label, meaning, hint.  
Badge, connecting view, stage title, overlay, and core all read the same object.

---

## Waveform

Unchanged processing: `useAgentAudioVisualizerWave` + `useTrackVolume` + shader.  
Improvements: type prop is wired again; stage no longer hardcodes sky chrome; core glow uses pulse tokens.  
Do not add a second FFT.

---

## Agent transitions

`reportAgentTransfer` sets phase `routing` and overlay `source → destination`.  
No transfer animation yet. Future transfer visuals subscribe to `AgentTransferred`.

Registered guests (math, coding, career, interview) stay on the backend. The core only names them when told.

---

## Accessibility

`prefers-reduced-motion` disables breathe/scale.  
Overlays are text. Color is not the only signal.  
Live region announces label + meaning.

---

## Performance

Glow/ring are composited transforms. No layout thrash.  
Target: 60fps on the wave. If a phone drops, reduce glow — do not add particles.  
Context updates only when derived snapshot inputs change.

---

## Future integrations

| Feature | Plug-in |
|---|---|
| Neural pulse / voice rings | New renderer inside `VoiceCore` |
| Memory graph | Subscribe to events; do not drive the wave |
| Multi-agent viz | `AgentTransferred` + overlay |
| AI Studio / learning | OS modules; they consume the same machine |
