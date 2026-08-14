"""Day 9 Phases 1-2: Math Practice Specialist foundation."""

from __future__ import annotations

from pathlib import Path

from agent import AGENT_TOOLS, SYSTEM_PROMPT, Assistant
from specialists.math_specialist import (
    MathPracticeSpecialist,
    build_teaching_response,
    get_inherited_language_policy,
    get_math_specialist_prompt,
    is_in_scope,
    refuse_out_of_scope,
)
from specialists.prompts import MATH_SPECIALIST_PROMPT, build_math_specialist_prompt
from specialists.schemas import SpecialistContext
from specialists.solver import solve_math
from specialists.utils import contains_devanagari, contains_romanized_hindi


def _tool_names(tools: list[object]) -> set[str]:
    return {getattr(tool, "name", getattr(tool, "__name__", "")) for tool in tools}


def test_specialist_initializes() -> None:
    specialist = MathPracticeSpecialist()
    assert specialist.role == "math_practice_specialist"
    assert specialist.track == "learning_and_literacy"
    assert specialist.specialist_context.language == "en"


def test_specialist_prompt_loads() -> None:
    prompt = get_math_specialist_prompt()
    assert prompt == MATH_SPECIALIST_PROMPT
    assert "ROLE" in prompt
    assert "RESPONSIBILITIES" in prompt
    assert "LIMITATIONS" in prompt
    assert "TEACHING STYLE" in prompt
    assert "SAFETY RULES" in prompt
    assert "LANGUAGE" in prompt
    assert "Math Practice Specialist" in prompt
    assert "Give a hint first" in prompt


def test_responsibility_boundaries() -> None:
    assert is_in_scope("Let's practice multiplication") is True
    assert is_in_scope("Help me with fractions") is True
    assert is_in_scope("What is photosynthesis?") is False
    assert is_in_scope("Help me with grammar") is False
    assert is_in_scope("Call me later") is False
    specialist = MathPracticeSpecialist()
    refused = specialist.handle_turn("Who won the election?")
    assert refused["in_scope"] is False
    assert refused["return_to_main"] is True
    assert "main learning assistant" in refused["text"].lower()


def test_multilingual_configuration_inherited() -> None:
    policy = get_inherited_language_policy()
    assert "Devanagari" in policy
    assert "Never romanize Hindi" in policy
    assert "Never output Romanized Hindi" in policy
    assert "Devanagari" in SYSTEM_PROMPT
    assert "Never romanize Hindi" in SYSTEM_PROMPT


def test_existing_tutor_unchanged() -> None:
    assert "AI Voice Learning Tutor" in SYSTEM_PROMPT
    assert "IDENTITY" in SYSTEM_PROMPT
    tutor = Assistant()
    assert tutor._resume_from_specialist is False
    names = _tool_names(AGENT_TOOLS)
    assert "lookup_user" in names
    assert "search_learning_knowledge" in names
    assert "get_next_exercise" in names
    assert "create_escalation" in names
    source = Path(__file__).resolve().parents[1] / "src" / "agent.py"
    text = source.read_text(encoding="utf-8")
    assert 'voice="Anisha"' in text
    assert 'style="Conversation"' in text
    assert "session = AgentSession(" in text
    assert 'stt=deepgram.STT(model="nova-3", language="multi")' in text


def test_addition() -> None:
    solved = solve_math("12 + 5")
    assert solved.get("error") is not True
    assert solved["answer"] == "17"
    lesson = build_teaching_response("addition", "en", "12 + 5")
    assert lesson["in_scope"] is True
    assert lesson["hint_first"] is True
    assert lesson["answer"] is None
    assert "add" in lesson["text"].lower()


def test_multiplication() -> None:
    solved = solve_math("6 x 7")
    assert solved.get("error") is not True
    assert solved["answer"] == "42"
    lesson = build_teaching_response("multiplication", "en", "6 x 7")
    assert lesson["hint_first"] is True
    assert "multiply" in lesson["text"].lower()


def test_word_problems() -> None:
    solved = solve_math(
        "Word problem: Riya has 8 pencils and gets 4 more. How many does she have?"
    )
    assert solved.get("error") is not True
    assert solved["topic"] == "word_problems"
    assert solved["answer"] == "12"
    lesson = build_teaching_response("word_problems", "en")
    assert "add, subtract, multiply, or divide" in lesson["text"].lower()


def test_fractions() -> None:
    solved = solve_math("1/2 + 1/4")
    assert solved.get("error") is not True
    assert solved["answer"] == "3/4"
    lesson = build_teaching_response("fractions", "en", "1/2 + 1/4")
    assert lesson["topic"] == "fractions"
    assert lesson["hint_first"] is True


def test_hindi_responses() -> None:
    lesson = build_teaching_response("addition", "hi")
    assert contains_devanagari(lesson["text"]) is True
    assert contains_romanized_hindi(lesson["text"]) is False
    refused = refuse_out_of_scope("hi")
    assert contains_devanagari(refused) is True
    specialist = MathPracticeSpecialist(
        specialist_context=SpecialistContext(language="hi")
    )
    result = specialist.handle_turn("मौसम कैसा है?")
    assert contains_devanagari(result["text"]) is True
    assert contains_romanized_hindi(result["text"]) is False


def test_english_responses() -> None:
    lesson = build_teaching_response("percentages", "en", "20% of 50")
    assert lesson["language"] == "en"
    assert "percent" in lesson["text"].lower()
    specialist = MathPracticeSpecialist()
    result = specialist.handle_turn("Help me with percentages")
    assert result["in_scope"] is True
    assert result["language"] == "en"


def test_out_of_scope_rejection() -> None:
    specialist = MathPracticeSpecialist()
    for question in (
        "Explain photosynthesis",
        "Help me with English grammar",
        "What is the weather today?",
        "Please escalate to a teacher",
    ):
        result = specialist.handle_turn(question)
        assert result["in_scope"] is False
        assert result["return_to_main"] is True


def test_context_is_injected_and_not_redemanded() -> None:
    context = SpecialistContext(
        language="hi",
        learner_level="beginner",
        conversation_summary="Learner asked for times tables",
        current_math_question="7 times 8",
        previous_solved_exercises=["2+2"],
        memory_summary="level=beginner; language=hindi; topics=math",
    )
    prompt = build_math_specialist_prompt(context)
    assert "LEARNER CONTEXT" in prompt
    assert "beginner" in prompt
    assert "7 times 8" in prompt
    assert "Do not ask the learner to repeat" in prompt
    specialist = MathPracticeSpecialist(specialist_context=context)
    assert specialist.specialist_context.learner_level == "beginner"
    assert "7 times 8" in specialist.prompt


def test_unsolvable_math_returns_structured_error() -> None:
    result = solve_math("draw a circle that proves politics")
    assert result.get("error") is True
    assert result.get("message")
    lesson = build_teaching_response(
        "geometry", "en", "draw a circle that proves politics"
    )
    assert lesson["error"] is True


def test_specialist_reuses_learning_system() -> None:
    specialist = MathPracticeSpecialist(
        specialist_context=SpecialistContext(learner_level="beginner")
    )
    exercise = specialist.lookup_practice("greetings")
    assert isinstance(exercise, dict)
    knowledge = specialist.lookup_knowledge("noun")
    assert isinstance(knowledge, list)


def test_specialist_does_not_own_ops_tools() -> None:
    specialist = MathPracticeSpecialist()
    names = _tool_names(list(specialist.tools))
    assert "return_to_main_agent" in names
    assert "create_escalation" not in names
    assert "lookup_user" not in names
    assert "handoff_to_math_specialist" not in names
