"""Math Practice Specialist. One responsibility: mathematics practice."""

from __future__ import annotations

from typing import Any

from livekit.agents import Agent, RunContext, function_tool

from specialists.intent import has_math_signal, is_main_agent_topic
from specialists.prompts import (
    MATH_SPECIALIST_PROMPT,
    build_math_specialist_prompt,
    build_specialist_enter_instructions,
    specialist_introduction,
)
from specialists.schemas import SpecialistContext
from specialists.solver import solve_math
from specialists.utils import (
    inherit_language_policy,
    language_script_is_valid,
    normalize_language,
    reuse_exercise_lookup,
    reuse_knowledge_search,
)

SPECIALIST_ROLE = "math_practice_specialist"
SPECIALIST_TRACK = "learning_and_literacy"

OUT_OF_SCOPE_TOPICS = (
    "grammar",
    "science",
    "history",
    "geography",
    "weather",
    "politics",
    "payments",
    "telephony",
    "escalation",
    "analytics",
    "memory",
    "settings",
)

_LESSON_EN = {
    "addition": (
        "Let's add slowly. Line the numbers up. Add ones, then tens. "
        "Try the first step, then I will check."
    ),
    "subtraction": (
        "Let's subtract step by step. Start from the ones place. "
        "What do you get after the first step?"
    ),
    "multiplication": (
        "Let's multiply in small steps. Break the number into tens and ones. "
        "What is your first partial product?"
    ),
    "division": (
        "Let's divide slowly. Ask how many groups fit. What is your first estimate?"
    ),
    "fractions": (
        "Let's look at the fraction parts. Same bottom number first. "
        "What do you think the next step is?"
    ),
    "decimals": (
        "Let's line up the decimal points. Then add or subtract as usual. "
        "Where does the decimal sit in your answer?"
    ),
    "percentages": (
        "Percent means out of one hundred. Write it as a fraction over 100. "
        "What is your first step?"
    ),
    "word_problems": (
        "Let's read the story once. Circle the numbers and the action word. "
        "Do we add, subtract, multiply, or divide?"
    ),
    "algebra": (
        "Let's keep both sides balanced. Do the same step on each side. "
        "What should we do first?"
    ),
    "geometry": (
        "Let's name the shape and the formula. Write the known sides. "
        "Which measurement are we finding?"
    ),
    "tables": (
        "Let's say the table slowly. I will start, then you continue. "
        "What comes after the first two facts?"
    ),
}

_LESSON_HI = {
    "addition": ("चलिए जोड़ को धीरे-धीरे करते हैं। पहले इकाई, फिर दहाई। पहला चरण आप आज़माएँ।"),
    "subtraction": (
        "चलिए घटाना चरणबद्ध करते हैं। इकाई से शुरू करें। पहले चरण के बाद क्या मिलता है?"
    ),
    "multiplication": (
        "चलिए गुणा छोटे चरणों में करते हैं। संख्या को तोड़ें। पहला आंशिक गुणनफल क्या है?"
    ),
    "division": ("चलिए भाग धीरे-धीरे करते हैं। कितने समूह बैठते हैं? आपका पहला अनुमान क्या है?"),
    "fractions": ("चलिए भिन्न के भाग देखते हैं। पहले हर समान करें। अगला चरण क्या होगा?"),
    "decimals": (
        "चलिए दशमलव बिंदु एक रेखा में रखें। फिर सामान्य जोड़ या घटाना करें। उत्तर में दशमलव कहाँ है?"
    ),
    "percentages": ("प्रतिशत का अर्थ है सौ में से। इसे 100 पर भिन्न लिखें। पहला चरण क्या है?"),
    "word_problems": (
        "चलिए कहानी एक बार पढ़ते हैं। संख्याएँ और क्रिया शब्द चुनें। "
        "जोड़ना है, घटाना है, गुणा है, या भाग?"
    ),
    "algebra": ("दोनों पक्ष संतुलित रखें। एक ही चरण दोनों ओर करें। पहले क्या करें?"),
    "geometry": ("आकृति और सूत्र याद करें। ज्ञात भुजाएँ लिखें। हम कौन सी माप निकाल रहे हैं?"),
    "tables": (
        "पहाड़ा धीरे-धीरे बोलें। मैं शुरू करता हूँ, फिर आप जारी रखें। पहली दो संख्याओं के बाद क्या आता है?"
    ),
}

_REFUSE_EN = (
    "That's outside math practice. The main learning assistant can continue from here."
)
_REFUSE_HI = "यह गणित अभ्यास के बाहर है। मुख्य शिक्षण सहायक इसमें आगे मदद कर सकते हैं।"


def _lesson_bank(language: str) -> dict[str, str]:
    if normalize_language(language) == "hi":
        return _LESSON_HI
    return _LESSON_EN


def refuse_out_of_scope(language: str = "en") -> str:
    """Polite refusal that returns control to the Main Agent."""
    if normalize_language(language) == "hi":
        return _REFUSE_HI
    return _REFUSE_EN


def is_in_scope(text: str) -> bool:
    """Return True only for mathematics requests."""
    if not isinstance(text, str) or not text.strip():
        return False
    if is_main_agent_topic(text) and not has_math_signal(text):
        return False
    return has_math_signal(text)


def build_teaching_response(
    topic: str,
    language: str = "en",
    expression: str | None = None,
    *,
    reveal_answer: bool = False,
) -> dict[str, Any]:
    """Build a short, hint-first teaching payload. Never crashes."""
    lang = normalize_language(language)
    key = (topic or "arithmetic").strip().lower()
    bank = _lesson_bank(lang)
    text = bank.get(key) or bank.get("addition", "")
    payload: dict[str, Any] = {
        "in_scope": True,
        "language": lang,
        "topic": key,
        "text": text,
        "hint_first": True,
        "answer": None,
        "error": False,
    }
    if expression:
        solved = solve_math(expression)
        if solved.get("error") is True:
            payload["error"] = True
            payload["message"] = (
                solved.get("message") or "Unable to solve this math problem."
            )
            return payload
        payload["steps"] = list(solved.get("steps") or [])
        payload["expression"] = solved.get("expression")
        if reveal_answer:
            payload["answer"] = solved.get("answer")
        else:
            payload["hint"] = (solved.get("steps") or [text])[0]
    if lang == "hi" and not language_script_is_valid(payload["text"], "hi"):
        payload["text"] = _REFUSE_HI
    return payload


class MathPracticeSpecialist(Agent):
    """LiveKit agent for mathematics practice only. No second voice pipeline."""

    role = SPECIALIST_ROLE
    track = SPECIALIST_TRACK

    def __init__(self, specialist_context: SpecialistContext | None = None) -> None:
        self.specialist_context = specialist_context or SpecialistContext()
        from specialists.handoff import HANDBACK_TOOLS

        super().__init__(
            instructions=build_math_specialist_prompt(self.specialist_context),
            tools=[*HANDBACK_TOOLS, solve_math_problem],
        )

    @property
    def prompt(self) -> str:
        return build_math_specialist_prompt(self.specialist_context)

    def introduction(self) -> str:
        return specialist_introduction(self.specialist_context.language)

    def continuity_opening(self) -> str:
        from specialists.shared_context import continuity_opening

        return continuity_opening(self.specialist_context)

    def handle_turn(self, user_text: str) -> dict[str, Any]:
        """Deterministic turn helper for tests and structured errors."""
        language = self.specialist_context.language
        if not is_in_scope(user_text):
            return {
                "in_scope": False,
                "language": language,
                "text": refuse_out_of_scope(language),
                "return_to_main": True,
                "error": False,
            }
        solved = solve_math(user_text)
        topic = str(solved.get("topic") or "arithmetic")
        return build_teaching_response(
            topic,
            language,
            user_text,
            reveal_answer=False,
        )

    def lookup_practice(self, topic: str | None = None) -> dict[str, Any]:
        """Reuse the existing exercise repository. Does not generate items."""
        level = self.specialist_context.learner_level or "beginner"
        return reuse_exercise_lookup(level, topic)

    def lookup_knowledge(self, query: str) -> list[dict[str, Any]]:
        """Reuse the existing knowledge repository. Read-only."""
        return reuse_knowledge_search(query)

    async def on_enter(self) -> None:
        session = getattr(self, "session", None)
        if session is None or not hasattr(session, "generate_reply"):
            return
        await session.generate_reply(
            instructions=build_specialist_enter_instructions(self.specialist_context)
        )


@function_tool()
async def solve_math_problem(
    context: RunContext,
    expression: str,
) -> dict[str, Any]:
    """Solve a basic math expression with deterministic steps.

    Use for arithmetic, fractions, percentages, and simple word problems.
    Returns structured steps and an answer, or a structured error.
    Never guess. Does not generate spoken text.

    Args:
        expression: The math problem or expression to solve.
    """
    del context
    return dict(solve_math(expression))


def get_math_specialist_prompt() -> str:
    """Return the base specialist prompt."""
    return MATH_SPECIALIST_PROMPT


def get_inherited_language_policy() -> str:
    """Return the multilingual policy shared with the Main Tutor."""
    return inherit_language_policy()
