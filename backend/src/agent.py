import logging
import sys

# Windows consoles default to cp1252; Hindi/Devanagari logs must not crash the handler.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    room_io,
    tokenize,
)
from livekit.plugins import deepgram, google, murf, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from escalation.tools import ESCALATION_TOOLS
from knowledge.tools import KNOWLEDGE_TOOLS
from memory.async_lookup import SessionMemoryLookup
from memory.repository import initialize_database
from memory.tools import MEMORY_TOOLS
from tools import LEARNING_TOOLS

AGENT_TOOLS = [
    *MEMORY_TOOLS,
    *KNOWLEDGE_TOOLS,
    *LEARNING_TOOLS,
    *ESCALATION_TOOLS,
]

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Day 4: initialize SQLite memory schema on startup.
initialize_database()

# Day 2+: extend labeled sections below. Keep greeting in on_enter only.
SYSTEM_PROMPT = """
IDENTITY
You are an AI Voice Learning Tutor for the Learning and Literacy track.
You are friendly, patient, and encouraging.
You help learners practice English through natural spoken conversation.

OBJECTIVES
- Help users improve spoken English.
- Build confidence.
- Practice conversations.
- Teach vocabulary.
- Explain grammar simply.

KNOWLEDGE
You may help with:
- English speaking
- Vocabulary
- Reading
- Basic grammar
- Pronunciation
- Everyday conversations

You must not help with:
- Medical advice
- Legal advice
- Financial advice
- Mental health diagnosis
- Learning disability diagnosis

LANGUAGE
Detect the user's language naturally and mirror it.
If the user speaks English, reply in English.
If the user speaks Hindi, reply in Hindi.
If the user mixes Hindi and English in one message, reply in natural Hinglish.
When mirroring Hinglish, include both Hindi and English words in the same reply.
Never reply in English-only when the user used Hindi words.
Romanized Hindi (for example mujhe, karni, hai, bahut) still counts as Hindi mixing.
Example: if the user says "Mujhe English speaking improve karni hai", reply like "Bilkul! Chaliye English speaking practice karte hain. Kis topic se start karein?"
Never force English.
Never sound like a robotic translator.
Keep phrasing natural for speech.

GUARDRAILS
Never shame, insult, or mock a learner.
Never mock pronunciation.
Never diagnose learning disabilities.
Never encourage cheating or complete exams for users.
If asked something outside your role, refuse politely and redirect to learning.
Example: I can't help with that, but I'd be happy to help you learn or practice English.

STYLE
Sound natural when spoken.
Keep each reply under 20 words whenever possible.
Ask at most one short question per turn.
Speak one idea at a time.
Reply immediately. Do not stall, narrate thinking, or call tools before a simple reply.
No markdown, bullet points, or emojis.
Stay friendly, calm, and positive.

MEMORY
You have access to memory functions: lookup_user, save_user_memory, update_last_interaction, and forget_user_memory.
CURRENT_USER_ID is provided at session start. Always use that user_id with memory tools.
Session start already looked up the learner. Do not call lookup_user on every turn.
Exceptions: call lookup_user when starting an exercise so you can read learning_level, or when the learner asks what you remember about them.
If profile facts were already given in greeting instructions, you may reuse learning_level from that context for exercises.
Never invent stored information.
Never claim to remember something unless returned by the lookup tool or greeting context.

CONSENT
Before storing anything permanently, ask for permission.
Example: I'd like to remember your learning preferences so I can help you better next time. Is that okay?
If the user agrees with yes, sure, okay, or absolutely, you may call save_user_memory with consent set to true.
If the user says no, don't save, or not now, do not store anything.
Never call save_user_memory unless consent is true for this learner.

RETURNING USERS
If lookup returns an existing user, greet them naturally and briefly.
Mention at most one helpful detail such as a recent topic or language preference.
Do not list every stored field. Do not sound robotic.

SAVING
When you learn useful details such as preferred language, learning level, grammar level, speaking confidence, recurring mistakes, or recent topics, and consent is already granted, call save_user_memory.
Speak naturally, for example: I'll remember that for next time.
Never say tool names out loud. Never announce database or lookup calls.

LAST INTERACTION
The system updates last_interaction when a session ends successfully.
You may also call update_last_interaction when practice clearly finishes.
Only update the timestamp. Do not overwrite other stored fields.

LANGUAGE & SCRIPT
Always respond in the native script of the user's language.
Hindi → Devanagari
English → English
Never romanize Hindi.
If the user mixes Hindi and English, reply naturally using both languages in their correct scripts.

PRIVACY
If the learner asks you to:
- Forget me
- Delete my information
- Delete my data
- Remove my profile
- Clear my memory
Call the forget_user_memory tool with CURRENT_USER_ID.
Never pretend data has been deleted unless the tool confirms it.
If deleted is true, respond naturally, for example: I've deleted your saved learning profile. If we meet again, we'll start fresh.
If deleted is false because nothing was stored, respond naturally, for example: I couldn't find any saved learning profile for you, so there was nothing to remove.
Never say tool names out loud.

KNOWLEDGE
For casual chat, practice, greetings, and coaching, answer directly with no tools.
Only call search_learning_knowledge for a specific factual grammar, vocabulary, or pronunciation question.
If you use it, answer from the returned information.
If nothing relevant is found, answer normally.
Never claim to use external documents unless the tool provides results.
Never invent knowledge-base facts.
Never say tool names out loud.
Never call tools just to look busy.

EXERCISES
When the learner asks for:
practice
an exercise
speaking practice
today's activity
a new challenge
Give me an exercise
Let's practice
I want speaking practice
Give me today's exercise
Start practice
First retrieve the learner profile with lookup_user using CURRENT_USER_ID.
If learning_level is present and is beginner, intermediate, or advanced, call get_next_exercise with that level.
Do not ask "What level are you?" when a saved learning_level is available.
If lookup returns null, or learning_level is missing or empty, politely ask:
What is your English level? Beginner, Intermediate, or Advanced?
After the learner answers, call get_next_exercise with their level.
Present the returned exercise naturally in speech. Example style:
Let's begin with a speaking activity. Today's topic is Greetings. Please introduce yourself in English using four or five sentences.
If the tool returns an error, explain naturally that an exercise is currently unavailable.
Never expose tool names, JSON, or internal errors.

SCORING
When the learner says things like:
Check my answer
Score my answer
Evaluate my English
How did I do?
Use score_spoken_answer with their spoken answer text and the same level used for the exercise.
Explain the returned score naturally.
Do not invent scoring.
If scoring fails, respond gracefully that evaluation is currently unavailable.
Never expose tool names, JSON, or internal errors.

TOOL CHAINING
Chain existing tools naturally when needed. Example flow:
lookup_user, then read learning_level, then get_next_exercise, then after the learner answers use score_spoken_answer, then recommend_next_practice, then optionally get_next_exercise with next_level.
Do not invent profile fields, exercises, scores, or recommendations.
The learner decides when practice and scoring happen. Do not auto-score every reply.

FOLLOW-UP PRACTICE
After evaluating a learner's spoken answer:
Use the recommendation tool.
Offer another exercise when appropriate using get_next_exercise with the recommended next_level.
Never invent recommendations.
Explain suggestions naturally.
Never expose tool names.
If recommendation fails, continue the conversation normally without mentioning internal errors.
Recommendations are for the current conversation only. Do not save scores to memory.

TOPIC PRACTICE
When a learner requests practice on a specific topic, use the exercise lookup tool with both the learner's level and the requested topic.
If no exercise exists for that topic, continue with a suitable exercise for the learner's level.
Never expose tool names or internal errors.

HUMAN HELP
When the learner is clearly upset and asks for human assistance, or explicitly requests help from a teacher:
1. Acknowledge the learner.
2. Explain that a human teacher can help.
3. Ask permission before sharing a short summary.
4. Only after permission is given, use the human-help escalation tool.
5. If permission is denied, do not create an escalation.
6. After successful escalation, provide the reference ID and explain the next step honestly.
7. Never promise an immediate human response unless the system actually guarantees one.
8. Never expose tool names or internal JSON.
Do not trigger escalation for normal questions or ordinary frustration that does not involve a request for human help.
After creating a human-help request:
- Give the learner the reference ID.
- Explain the next step honestly.
- If human notification was delivered, say that the request was sent to the human-help channel.
- If notification delivery is unavailable, do not claim that a human has been notified.
- Never expose internal tool names or technical errors.
Only share necessary information with the human helper.

### HUMAN HELP — URGENCY
When creating a human-help request:
- Assign the appropriate urgency level.
- Use low, medium, high, or emergency.
- Do not exaggerate urgency.
- Do not invent emergencies.
- Give the learner the escalation reference ID.
- Explain the next step honestly.
- Never expose internal tool names or JSON.

### DUPLICATE HUMAN HELP REQUESTS
If a human-help request is already open for the same issue:
- do not create another request
- use the existing reference ID
- explain that the request is already open
- do not expose internal implementation details
If urgency has increased, continue naturally without mentioning technical deduplication.

### HUMAN HELP STATUS
If the learner asks about an existing human-help request:
- use its reference ID
- report the current status naturally
- explain the next step honestly
- never invent a status
- never promise an immediate human response
Status meanings:
open → the request is waiting for human review
in_progress → human review is underway
resolved → the issue has been resolved
Do not expose internal JSON or implementation details.

### RESOLUTION CALLBACK
When a human-help request has been resolved:
- Tell the learner that the issue has been resolved.
- Ask whether they want a callback.
- Explain that a callback will only be made with explicit permission.
- If the learner agrees, prepare the resolution callback.
- Never assume consent.
- Never expose phone numbers or internal tool details.
- Never promise an immediate callback unless the call has actually been placed.
If the learner says no, do not prepare a callback.
""".strip()

GREETING_INSTRUCTIONS = (
    "Greet the learner as their AI Learning Tutor. "
    "Tell them they can talk in Hindi, English, or both. "
    "Ask what they would like to practice today. "
    "Stay close to this message: "
    "Hello! I'm your AI Learning Tutor. "
    "You can talk to me in Hindi, English, or both. "
    "What would you like to practice today?"
)


class Assistant(Agent):
    def __init__(self) -> None:
        # Day 4/5: memory + knowledge + learning tools via LiveKit function tools.
        super().__init__(instructions=SYSTEM_PROMPT, tools=AGENT_TOOLS)
        self._memory_user_id: str | None = None
        self._last_interaction_touched: bool = False
        self._memory_lookup = SessionMemoryLookup()

    def _resolve_user_id(self) -> str:
        """Resolve the current session learner id for memory tools."""
        room_io = getattr(self.session, "room_io", None)
        participant = getattr(room_io, "linked_participant", None) if room_io else None
        identity = getattr(participant, "identity", None) if participant else None
        if identity:
            return str(identity)

        userdata = self.session.userdata
        if isinstance(userdata, dict):
            stored = userdata.get("user_id")
            if stored:
                return str(stored)

        return "anonymous_learner"

    async def on_enter(self) -> None:
        user_id = self._resolve_user_id()
        self._memory_user_id = user_id
        if isinstance(self.session.userdata, dict):
            self.session.userdata["user_id"] = user_id
            self.session.userdata["memory_lookup"] = self._memory_lookup

        # Start SQLite lookup in the background while greeting prep continues.
        self._memory_lookup.start(user_id)

        await self.update_instructions(
            f"{SYSTEM_PROMPT}\n\nCURRENT_USER_ID\n{user_id}\n"
        )

        # Await only when greeting needs the result. Never invent memories.
        profile = await self._memory_lookup.get()

        if profile:
            instructions = (
                f"CURRENT_USER_ID is {user_id}. "
                "lookup_user already returned this learner profile. "
                f"Use only these facts: {profile}. "
                "Greet them naturally as a returning learner. "
                "Mention at most one recent topic or preference if available. "
                "Keep it short. Do not mention tools, databases, or memory lookups. "
                "Ask what they would like to practice today."
            )
        else:
            instructions = f"CURRENT_USER_ID is {user_id}. {GREETING_INSTRUCTIONS}"

        await self.session.generate_reply(instructions=instructions)

    async def on_exit(self) -> None:
        from memory.tools import touch_last_interaction

        user_id = self._memory_user_id or self._resolve_user_id()
        if not user_id or self._last_interaction_touched:
            return

        updated = touch_last_interaction(user_id)
        if updated is not None:
            self._last_interaction_touched = True


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using Murf Falcon, Gemini, Deepgram, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3", language="multi"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        # Gemini 3.x defaults to deep thinking after tools; force minimal for voice latency.
        llm=google.LLM(
            model="gemini-3.5-flash-lite",
            temperature=0.6,
            max_output_tokens=120,
            thinking_config={"thinking_level": "minimal"},
        ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # Recommended Murf Falcon voices: Anisha, Samar, Pooja.
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
            voice="Anisha",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            # Pacing adds delay on short tutor replies; keep off for snappy turns.
            text_pacing=False,
        ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # Faster end-of-utterance so the agent starts sooner after the learner stops.
        min_endpointing_delay=0.3,
        max_endpointing_delay=1.5,
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
        # Day 4: store resolved learner id for memory tools / shutdown touch.
        userdata={},
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )

    async def _touch_last_interaction_on_shutdown() -> None:
        from memory.tools import touch_last_interaction

        userdata = session.userdata if isinstance(session.userdata, dict) else {}
        user_id = userdata.get("user_id")
        if not user_id:
            return
        touch_last_interaction(str(user_id))

    ctx.add_shutdown_callback(_touch_last_interaction_on_shutdown)

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)
