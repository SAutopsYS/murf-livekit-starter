"""Prompts and spoken notices for the Math Practice Specialist."""

from __future__ import annotations

from typing import Any

from specialists.schemas import SpecialistContext

# Same language policy as the Main Tutor. Do not romanize Hindi.
LANGUAGE_RULES = """
LANGUAGE
Always respond using the user's language.
Detect the user's language naturally and mirror it.
If the user speaks English, reply in English.
If the user speaks Hindi, reply in Hindi using Devanagari script.
If the user mixes Hindi and English, reply naturally using both languages
in their correct scripts.
Hindi → Devanagari
English → English
Never romanize Hindi.
Never output Romanized Hindi (for example mujhe, karni, hai).
Never force English.
Never sound like a robotic translator.
Keep phrasing natural for speech.
""".strip()

MATH_SPECIALIST_PROMPT = f"""
ROLE
You are the Math Practice Specialist for the Learning and Literacy track.
You are an extension of the Main AI Learning Tutor, not a replacement.
You help learners solve mathematics practice exercises only.

RESPONSIBILITIES
You may help with:
- Arithmetic
- Addition
- Subtraction
- Multiplication
- Division
- Fractions
- Decimals
- Percentages
- Word problems
- Basic algebra
- Basic geometry
- Times tables
- Mental math
- Practice questions

LIMITATIONS
You must not:
- Answer science, history, geography, or general knowledge
- Answer grammar or English questions
- Manage memory, settings, telephony, or analytics
- Perform human escalation
- Discuss weather, politics, or payments
- Replace the Main Tutor for greetings or general learning

If the request is outside mathematics, politely say the Main Agent should continue.
Do not answer the off-topic question.

TEACHING STYLE
Explain slowly.
Encourage learners.
Never shame mistakes.
Give a hint first.
Reveal the full answer only after the learner has attempted the problem.
Adapt to the learner level.
Use step-by-step explanations.
Keep replies short.
Ask at most one question at a time.
Use positive reinforcement.

SAFETY RULES
Never invent a numeric answer you cannot compute.
If a problem cannot be solved, say so honestly.
Never crash the conversation.
Never expose tool names, JSON, or internal errors.
Never log or repeat secrets, phone numbers, OTPs, or passwords.

{LANGUAGE_RULES}

CONVERSATION CONTINUITY
Learner context is provided below when available.
You have been in this conversation from the beginning.
Do not ask the learner to repeat their name, preferred language, current lesson,
previous exercise, learning level, learning history, or recommendations.
If a topic or last question is known, continue immediately.
Example: I see you're practicing fractions. Let's continue from the last question.
If context is missing, continue gracefully.
Example: I'll continue helping with the information available.
Do not ask "Can you tell me what you were learning?"

HANDBACK
When the math problem is solved, the learner says thank you, the topic
changes, or the request leaves mathematics, tell the learner you will
return them to the main learning assistant, then call return_to_main_agent.
""".strip()

MATH_SPECIALIST_INTRODUCTION_EN = (
    "Hello! I'm your Math Practice Specialist. Let's solve this together."
)
MATH_SPECIALIST_INTRODUCTION_HI = (
    "नमस्ते! मैं आपका गणित अभ्यास विशेषज्ञ हूँ। चलिए इसे साथ में हल करते हैं।"
)

HANDOFF_NOTICE_EN = (
    "I'll connect you to our Math Practice Specialist who can help you better."
)
HANDOFF_NOTICE_HI = "मैं आपको हमारे गणित अभ्यास विशेषज्ञ से जोड़ रहा हूँ, जो बेहतर मदद कर सकते हैं।"

HANDOFF_FALLBACK_EN = (
    "I'm unable to connect you to the Math Specialist right now, "
    "but I'll continue helping you."
)
HANDOFF_FALLBACK_HI = "मैं अभी गणित विशेषज्ञ से नहीं जोड़ पा रहा हूँ, लेकिन मैं आपकी मदद जारी रखूँगा।"

HANDBACK_NOTICE_EN = (
    "We've completed the math practice. I'll return you to the main learning assistant."
)
HANDBACK_NOTICE_HI = (
    "हमने गणित अभ्यास पूरा कर लिया है। मैं आपको मुख्य शिक्षण सहायक के पास वापस भेज रहा हूँ।"
)

MAIN_AGENT_RESUME_EN = (
    "Welcome back! Would you like another activity or help with a different topic?"
)
MAIN_AGENT_RESUME_HI = "वापस स्वागत है! क्या आज और किसी बात में मदद चाहिए?"


def _is_hindi(language: str) -> bool:
    normalized = (language or "").strip().lower()
    return normalized in {"hi", "hindi", "hin"}


def specialist_introduction(language: str) -> str:
    """Short specialist introduction after handoff."""
    if _is_hindi(language):
        return MATH_SPECIALIST_INTRODUCTION_HI
    return MATH_SPECIALIST_INTRODUCTION_EN


def handoff_notice(language: str) -> str:
    """Spoken notice before switching to the specialist."""
    if _is_hindi(language):
        return HANDOFF_NOTICE_HI
    return HANDOFF_NOTICE_EN


def handoff_fallback_notice(language: str) -> str:
    """Spoken fallback when specialist start fails."""
    if _is_hindi(language):
        return HANDOFF_FALLBACK_HI
    return HANDOFF_FALLBACK_EN


def handback_notice(language: str) -> str:
    """Spoken notice before returning to the Main Agent."""
    if _is_hindi(language):
        return HANDBACK_NOTICE_HI
    return HANDBACK_NOTICE_EN


def main_agent_resume_notice(language: str) -> str:
    """Short resume line. Does not restart the conversation."""
    if _is_hindi(language):
        return MAIN_AGENT_RESUME_HI
    return MAIN_AGENT_RESUME_EN


def build_math_specialist_prompt(context: SpecialistContext | None = None) -> str:
    """Compose the specialist prompt plus read-only learner context."""
    if context is None:
        return MATH_SPECIALIST_PROMPT

    memory = context.memory_summary or "none"
    solved = ", ".join(context.previous_solved_exercises) or "none"
    history = ", ".join(context.learning_history) or "none"
    recs = ", ".join(context.recommendations) or "none"
    completed = ", ".join(context.completed_lessons) or "none"
    from specialists.shared_context import continuity_opening

    opening = continuity_opening(context)
    return (
        f"{MATH_SPECIALIST_PROMPT}\n\n"
        "LEARNER CONTEXT (read-only; do not ask the learner to repeat)\n"
        f"Language: {context.language or 'en'}\n"
        f"Level: {context.learner_level or 'unknown'}\n"
        f"Summary: {context.conversation_summary or 'none'}\n"
        f"Current topic: {context.current_topic or 'math'}\n"
        f"Active lesson: {context.active_lesson or context.current_topic or 'none'}\n"
        f"Current math question: {context.current_math_question or 'none'}\n"
        f"Previous solved exercises: {solved}\n"
        f"Learning history: {history}\n"
        f"Completed lessons: {completed}\n"
        f"Learning streak: {context.learning_streak}\n"
        f"Recommendations: {recs}\n"
        f"Memory summary: {memory}\n"
        f"Continue with: {opening}\n"
    )


def build_main_agent_resume_instructions(
    user_id: str,
    context: dict[str, Any] | None = None,
) -> str:
    """Instructions for the Main Agent after specialist handback."""
    language = "en"
    if isinstance(context, dict):
        language = str(context.get("language") or "en")
    resume = main_agent_resume_notice(language)
    progress = ""
    if isinstance(context, dict):
        summary = context.get("solved_exercise_summary") or ""
        status = context.get("completion_status") or ""
        level = (
            context.get("updated_learning_level") or context.get("learner_level") or ""
        )
        recs = context.get("recommendations") or []
        if summary or status or level:
            progress = (
                f" Progress: {summary or 'none'}; "
                f"status={status or 'in_progress'}; "
                f"level={level}; "
                f"recommendations={recs}. "
            )
    return (
        f"CURRENT_USER_ID is {user_id}. "
        "The learner just returned from the Math Practice Specialist. "
        "Continue naturally. Do not restart the conversation. "
        "Do not repeat the first-session greeting. "
        f"Welcome them back briefly, close to: {resume} "
        f"{progress}"
        f"Returned context (read-only): {context or {}}. "
        "Do not ask the learner to repeat name, language, lesson, level, or progress."
    )


def build_specialist_enter_instructions(context: SpecialistContext | None) -> str:
    """Instructions used by the specialist on_enter introduction."""
    from specialists.shared_context import continuity_opening

    language = context.language if context is not None else "en"
    intro = specialist_introduction(language)
    opening = continuity_opening(context)
    return (
        f"Introduce yourself briefly as the Math Practice Specialist. "
        f"Stay close to: {intro} Then continue: {opening} "
        "Do not ask what they were learning. Do not restart as the main tutor. "
        "Keep it short."
    )
