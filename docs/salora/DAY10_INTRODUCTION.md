# Day 10 — Blog introduction (draft)

Opening copy for the VoiceForBharat post. Not the full article.

Status key used in the notes under each section:

- **Implemented** — runs in the hall or worker today
- **Architected** — code and docs exist as a single facade; not a hall feature
- **Planned** — written as future work; do not ship as a claim

---

## 1. Project introduction

I built SALORA OS around a simple loop: a learner opens a browser, speaks, and a tutor speaks back.

That tutor is a LiveKit agent. The page does not stream audio to a custom server of mine. It joins a room. A Python worker named `my-agent` joins the same room. Deepgram turns speech into text. Gemini writes a short reply. Murf Falcon says it. If I added a second text-to-speech path later, I would have two mouths and two personalities. I did not do that.

The product on the home route is an AI Voice Learning Tutor. The chrome says SALORA OS. The spoken identity is still the tutor. You can talk in English, Hindi, or the mix people actually use. Hindi in the reply is written in Devanagari, not default Roman. The first thing the agent does is greet you and ask what you want to practice. It is not a dashboard that happens to have a microphone.

Around that hall I kept two other pages: call analytics, and an enterprise control view. They read operational data. They do not sit in the conversation. They also do not store what you said. Memory, if you allow it, is a small consented profile in one SQLite file. Call stats live in another. Those files are not joined by identity.

I am writing this after ten days on the VoiceForBharat Learning & Literacy track. Days 1–9 are in git. The later “operating system” layer — a workspace shell, service facades, search and automation contracts — exists in the tree as architecture. It does not replace the worker. If you only have time to understand one file, read `backend/src/agent.py`.

---

## 2. Problem statement

Most learning software still asks you to type. You read a prompt, you write an answer, you get a paragraph back. That is fine for grammar drills on a desk. It is a poor substitute for speaking.

In practice, people bounce between a video, a notes app, a translator, and a chatbot. None of those stay with you for a turn of actual speech. None of them are required to answer in the same mix you just used. If you speak Hindi at home and English in class, a product that “supports Hindi” by showing a language dropdown is not the same as a tutor that hears `Mujhe English speaking improve karni hai` and answers in kind.

There is also a trust problem. Voice products like to keep tapes. Dashboards like to show transcripts. I did not want a learner’s mouth in a table. The analytics schema has outcomes and timings. It does not have an utterance column. Tests fail the other way.

Accessibility is not a slogan here. If your hands are busy, or typing in English is the hard part, the session is already a conversation. The hall still has a start button and optional chat — `supportsChatInput` is on — but the practice is spoken. Microphone permission has its own view and a retry. Status is visible while you wait.

AI assistance, in this project, is narrow on purpose. The prompt refuses medical, legal, and financial advice, and it will not sit an exam for you. When a learner is stuck and asks for a person, the agent can open a human-help request, but only after it asks. It will not pretend a teacher was notified if the webhook was never configured.

Fragmented tools are how I would have failed this build: one stack for chat, another for voice, a third for “enterprise.” The constraint I kept was the opposite. One room. One voice. Extra capability arrives as a tool or a guest, then leaves.

---

## 3. Target users

**Students and other learners** are the people the hall is built for. They get the greeting, the practice suggestions (vocabulary, speaking, grammar, daily conversation), exercises, a rule-based score, and a follow-up suggestion that is not written into their profile. If they ask to be forgotten, `forget_user_memory` deletes the row. That path is implemented and tested.

**Teachers** do not get a `/teacher` page. I will not pretend otherwise. What they do get today is the escalation path: a learner can ask for a human, consent to a short summary, and receive a reference ID. The enterprise view can show aggregates. A teacher console builder exists behind the education facade and only lists consented, hashed learner refs. That is a backend shape, not a classroom product.

**Parents** are named in the product docs. A parent dashboard builder exists in the enterprise package. There is no parent route on the site. If you are a parent, the honest story is: the learner practices in the hall; you do not get a tape of them; a dedicated parent surface is still architected, not shipped.

**Professionals** who want spoken English for work can use the same tutor. Daily conversation and speaking-practice chips are in the welcome view. There is no separate “corporate coach” agent in the live worker. Career and interview mentors exist as registered-disabled runtime kinds. They are not live mouths.

**Organizations** can open `/enterprise`. That control center was part of the Day 9 work. Tenant records in the later platform layer are in-memory. Authentication is optional and off by default so an anonymous voice session still works. Do not read that as a hardened multi-tenant SaaS.

**Developers** can run the monorepo with `uv` and `pnpm`, add a LiveKit function tool, or register another specialist behind the existing router. Public API and SDK envelopes are documented. There is no developer portal UI. `portal_ui` is explicitly false.

**Enterprises** in the brochure sense — SSO, HIPAA, plugin execution — are not claimed. HIPAA checks return not-ok. Marketplace `may_execute` is false. Those are intentional locks, not missing checkboxes I forgot to tick.

---

## 4. Why Voice AI

I type all day. I still would not practice spoken English by typing it.

Speech is the skill. A UI that collects text and then “reads it out” is a detour. In the hall, the learner talks, the agent talks, and the wave and status exist so you can see listening versus speaking. That is faster than submitting a form, and it matches how people already switch languages mid-sentence.

Hands-free matters in small ways: you can take a turn while you hold a notebook. You can try a sentence again without finding a cursor. The session is a LiveKit room, so the back-and-forth is not a file upload.

For India, the multilingual part is not an extra locale pack. Deepgram is set to `language="multi"`. The prompt treats romanized Hindi as Hindi mixing and answers in natural Hinglish when that is what you used. It also insists on Devanagari when the reply is Hindi. I have broken that rule in logs on Windows consoles; the worker forces UTF-8 so Hindi in the terminal does not die as `?`. The product rule is still: do not romanize Hindi in the mouth of the tutor.

Voice is also how a specialist can visit without becoming a new app. Math hands off inside the same room. The host tells you it is connecting you. When you come back, it does not greet you like a stranger. Reconnect and handoff are different on purpose.

I am not going to quote a speedup against typing. I did not publish that measurement. What I did tune, in code, is the spoken turn: short max tokens, minimal Gemini thinking, endpointing between 0.3 and 1.5 seconds, preemptive generation on.

---

## 5. Why Murf Falcon

Murf Falcon is the text-to-speech engine. It is wired through the LiveKit Murf plugin as `murf.TTS`. The voice is `Anisha`, style `Conversation`. That is the only TTS constructor in the worker.

I kept Falcon when I added memory, tools, telephony, escalation, and a math specialist. A second provider would have been a second personality. The specialist is a guest. It does not bring its own mouth.

A few choices were about how the tutor sounds in a short turn, not about a leaderboard. Sentence tokenization starts at two sentences. `text_pacing` is off. The comment in `agent.py` is plain: pacing added delay on short tutor replies. I wanted the line to start. I do not have a checked-in benchmark of Falcon against another TTS in this repository, so I will not invent one.

Falcon is also why Hindi and English can stay on one voice family while the text script changes. The model writes; Murf speaks. The pipeline around it — Deepgram, Gemini, LiveKit — is there so that speech in and speech out stay in the same room.

If Murf is down, the session does not grow a backup TTS. Readiness checks look for the Murf key. That is a product choice: fail honestly, do not swap the voice mid-hall.

---

## 6. Architecture philosophy

The voice path is one `AgentSession`. Everything I added later had to consume that, or stay off the hall.

That habit turned into a platform rule. In the later layer there is one provider registry, one in-process event bus, one search facade, one automation facade, one agent runtime host, one workspace shell, and an orchestrator that picks a capability and then gets out of the way. The orchestrator does not route specialists. `SpecialistRouter` does. I say that because “one AI orchestrator” is easy to oversell. It is a service facade. The live mouth is still `agent.py`.

Search in the hall is the knowledge JSON tool. The “Search Platform” fans out to that knowledge, a marketplace catalog, and agent manifests. It is one query contract. It is not a second memory database. Automation is one workflow service. It is not a second queue product. Knowledge Fabric projects the same knowledge search. Memory Graph is not allowed to write `memory.db`. Marketplace can list plugins. It cannot execute them.

I did this because I have watched teams “scale” by cloning the stack. Two routers disagree. Two search indexes drift. Two voice paths mean two bugs at 11 p.m. One pipeline is easier to test. It is also the only way a math guest can return you to the same tutor without a reconnect.

Scalability, for this repo, is not a Kubernetes essay. Frontend can replica. Workers scale by LiveKit jobs. SQLite stays until a single writer saturates, with the same schema laws. Redis is written down as a future rate-limit store. It is not running in compose. Compose persists `/app/data` so a recreate does not eat the local databases. That is the honest ceiling.

---

## 7. Future vision

I want a learner to leave, come back tomorrow, and not be a stranger — if they said that was all right. I want a teacher to see pulse without a tape. I want a parent surface that shows time and next step, not a transcript. Those last two are drawn in the docs and partly shaped in services. They are not the home page.

What I will not do to get there is fork the voice path. Identity can turn `AUTH_REQUIRED` on once a roster exists. Studio and the whiteboard can become instruments, the way analytics already did. A queue can sit behind the job catalog. None of that needs a second Murf, a second router, or a speech lake.

SALORA OS, if it grows up, is still a hall. Guests visit. Dashboards stand to the side. The line stays open.
