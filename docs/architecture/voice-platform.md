# Voice Pipeline

One path. LiveKit carries audio. Murf Falcon speaks. Deepgram listens. Gemini thinks.

Canonical spec: [17 Voice Architecture](../engineering/17_VOICE_ARCHITECTURE.md). Visual host: [18 Living AI Core](../engineering/18_LIVING_AI_CORE.md).

## Pipeline

```text
User speaks → Deepgram STT → Gemini → Murf Falcon TTS → LiveKit → User hears
```

Default voice: Murf `Anisha`. Hindi replies use Devanagari. Do not add a second STT or TTS.

## Session meaning

`deriveVoiceSnapshot` is the only mapper from LiveKit + network + mute + transfer to `VoicePhase`. UI reads `useVoice()`. ViewController owns screens (welcome, connecting, session, ended). The machine owns in-session meaning. Do not merge those jobs.

```text
disconnected → connecting → ready / idle
                           → listening → thinking → speaking → idle
                           → muted | paused | routing | returning
                           → disconnecting → disconnected
```

## Privacy

No transcript or utterance column in `memory.db` or `analytics.db`. Logs use fixed event names. Scores stay conversation-scoped.

## Specialist handoff

Math is the live guest. Other specialists may be registered and disabled. Handoff stays on the same LiveKit room and the same Murf mouth. SpecialistRouter is the only routing authority.

## Related

- [Backend](backend.md)
- [06 AI Architecture Bible](../engineering/06_AI_ARCHITECTURE_BIBLE.md)
- [guides/troubleshooting.md](../guides/troubleshooting.md)
