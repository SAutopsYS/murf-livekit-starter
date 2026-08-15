# VoiceForBharat history

This repository started as a Murf VoiceForBharat 2026 Learning & Literacy submission. The Voice Pipeline from that work is the kernel. SALORA OS grew on top of it. This page keeps the day history so the root README can stay short.

Track: Learning & Literacy. TTS: Murf Falcon. Transport: LiveKit.

## Days 1–9

| Day | What landed |
| --- | --- |
| 1 | Starter voice agent end-to-end |
| 2 | Learning Tutor personality, greeting, bilingual guardrails |
| 3 | Session states, transcript, wave, practice suggestions, a11y |
| 4 | Consented SQLite memory, Forget Me, knowledge JSON tools |
| 5 | Exercise tools, scoring, recommendations, provider failover |
| 6 | Outbound telephony on a separate path. Browser pipeline unchanged |
| 7 | Consent-first human-help escalation |
| 8 | Privacy-safe analytics dashboard (`analytics.db`) |
| 9 | SpecialistRouter + Math guest on the same room and mouth |

Enterprise Control Center (`/enterprise`) sits on the Day 9 specialists. No second Voice Pipeline.

## Demo checklists

Day-by-day demo steps that used to live in the root README:

**Learning tools.** New learner consent. Returning greeting. “Give me an exercise.” Spoken score → recommendation. Knowledge tip. Forget Me. API failure falls back to local JSON.

**Telephony.** Health ready. Prepare → dial. Bootstrap EN / Hindi Devanagari. Daily practice. Outcomes. Structured failure, no stack traces.

**Escalation.** No escalate on normal talk. Request help → consent → reference ID → webhook. Duplicates handled. Optional callback consent.

**Analytics.** Open `/analytics`. Complete a real call. Counts and recent row update. Export has no speech.

**Specialist.** General question stays on the host. Math hands off and hands back. No greeting restart.

## What did not change

Browser Voice Pipeline. Murf Falcon as the only mouth. No utterance column.
