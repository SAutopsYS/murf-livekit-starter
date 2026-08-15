# Day 10 — LinkedIn post

Copy-ready. Do not claim a checked-in latency benchmark. Murf Falcon’s product line is quoted as Murf states it; this repo does not publish a millisecond bake-off.

---

I spent 10 days on **10 Days of Voice Agents – VoiceForBharat Edition** building a tutor that stays on the line.

SALORA OS is a voice-first learning hall. You open a browser, speak in English, Hindi, or Hinglish, and a LiveKit worker answers with **Murf Falcon – the fastest TTS API**. Deepgram hears. Gemini writes a short reply. Murf Falcon (`Anisha`) speaks it. One Voice Pipeline. No second mouth.

What I actually shipped in the hall:

- A Learning Tutor that greets you and practices with you
- Consent-first memory and a real Forget Me
- Spoken exercises with a rule-based score (not an LLM judge)
- Math specialist handoff in the **same** room
- Human-help escalation only after consent
- Analytics and an enterprise view that never store what you said

Biggest lessons:

1. Voice dies if the model “thinks out loud” after tools. I turned Gemini thinking down and turned Murf pacing off for short tutor lines.
2. A useful dashboard will ask for a transcript. I used two SQLite files instead — profile vs anonymous ops — and CI fails if a speech column appears.
3. A second TTS or a second router looks like scale. It is two bugs at 11 p.m. Math is a guest. It does not bring its own mouth.

The later “OS” layer (search, automation, orchestrator facades) wraps that worker. It does not sit between your microphone and Murf. I wrote that down so the blog cannot lie.

If you are building a voice agent: keep one session, protect the schema, and label implemented vs planned before you post.

Repo: https://github.com/SAutopsYS/SALORA-OS

Thank you [Murf AI](https://www.linkedin.com/company/murf-ai/) for Falcon and for VoiceForBharat.

#VoiceForBharat #VoiceAI #LiveKit #MurfFalcon #LearningTech

---

## Notes for posting

- Attach hall / analytics screenshots only after you capture them (none are in `docs/assets/` yet).
- Tag **Murf AI** in the LinkedIn UI (the markdown company link above is a fallback).
- Do not add a fake “X ms latency” line.
- Publish the repo (or a public fork) before you paste the GitHub URL.
