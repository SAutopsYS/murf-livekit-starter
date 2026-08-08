import logging

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    inference,
    tokenize,
    room_io,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from knowledge.tools import KNOWLEDGE_TOOLS
from memory.async_lookup import SessionMemoryLookup
from memory.repository import initialize_database
from memory.tools import MEMORY_TOOLS

AGENT_TOOLS = [*MEMORY_TOOLS, *KNOWLEDGE_TOOLS]

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
No markdown, bullet points, or emojis.
Stay friendly, calm, and positive.

MEMORY
You have access to memory functions: lookup_user, save_user_memory, update_last_interaction, and forget_user_memory.
CURRENT_USER_ID is provided at session start. Always use that user_id with memory tools.
Whenever appropriate:
Look up the current user using the lookup tool.
If the user exists, use their stored learning profile naturally.
If they do not exist, continue normally.
Never invent stored information.
Never claim to remember something unless returned by the lookup tool.

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
When the learner asks factual questions about English learning, grammar, pronunciation, vocabulary, or speaking tips:
Use the knowledge search tool first.
Answer using the returned information.
If no relevant information is found, answer normally.
Never claim to use external documents unless the tool provides results.
Never invent knowledge-base facts.
Never say tool names out loud.
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
        # Day 4: memory + knowledge access via LiveKit function tools only.
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
        llm=google.LLM(
            model="gemini-3.5-flash-lite",
        ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # Recommended Murf Falcon voices: Anisha, Samar, Pooja.
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
            voice="Anisha",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True,
        ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
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
