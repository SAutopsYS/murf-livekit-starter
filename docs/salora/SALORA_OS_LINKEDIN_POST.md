# SALORA OS — LinkedIn post

Copy-ready after you replace `BLOG_URL_HERE` with the published Medium URL. Do not invent a millisecond number. Tag **Murf AI** in the LinkedIn UI.

Do not publish this post until the blog URL is real.

---

I built SALORA OS around a simple loop: open a browser, speak, get a spoken reply.

It is a voice learning hall on LiveKit. Deepgram hears. Gemini writes a short line. **Murf Falcon – the fastest TTS API** says it (`Anisha`). One Voice Pipeline. No second mouth.

What is actually live: a Hindi / English / Hinglish tutor, consent-first memory and Forget Me, rule-based scoring, math handoff in the same room, and dashboards that do not store what you said.

What I learned the hard way:

Gemini 3.x wants to “think” after tools. That kills a spoken turn. I turned thinking down and turned Murf pacing off for short replies.

A useful dashboard will ask for a transcript. I used two SQLite files instead. CI fails if a speech column appears.

A second TTS looks like scale. It is two bugs at 11 p.m.

The later OS layer (search, automation, orchestrator) wraps that worker. It does not sit between the microphone and Murf.

Latency was not benchmarked in this validation run. I will not invent one.

Built during **10 Days of Voice Agents – VoiceForBharat Edition**.

Blog: BLOG_URL_HERE
Repo: https://github.com/SAutopsYS/SALORA-OS.git

Thank you Murf AI for Falcon and for VoiceForBharat.

#VoiceForBharat #VoiceAI #LiveKit #MurfFalcon #SALORAOS
