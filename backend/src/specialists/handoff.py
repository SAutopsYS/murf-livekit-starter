"""Main Agent to Math Practice Specialist handoff and handback."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from livekit.agents import RunContext, function_tool

from specialists.closing import build_handback_summary
from specialists.context import read_context_from_userdata
from specialists.conversation_state import (
    append_specialist_history,
    apply_state_to_userdata,
    conversation_state_from_context,
    read_state_from_userdata,
)
from specialists.events import log_specialist_event
from specialists.intent import infer_math_topic, should_return_to_main
from specialists.metrics import record_handback, record_handoff
from specialists.prompts import (
    handback_notice,
    handoff_fallback_notice,
    handoff_notice,
)
from specialists.recovery import start_specialist_with_retry
from specialists.registry import MATH_SPECIALIST_ID
from specialists.router import SpecialistRouter, get_specialist_router
from specialists.schemas import (
    HandbackResult,
    HandoffResult,
    RouteTarget,
    SpecialistContext,
)
from specialists.shared_context import SharedContextManager, get_shared_context_manager

SpecialistFactory = Callable[..., Any]
MainAgentFactory = Callable[..., Any]


def _session_userdata(context: Any) -> dict[str, Any]:
    session = getattr(context, "session", None)
    userdata = getattr(session, "userdata", None)
    if isinstance(userdata, dict):
        return userdata
    return {}


def _session_user_id(context: Any, userdata: dict[str, Any]) -> str | None:
    stored = userdata.get("user_id")
    if stored:
        return str(stored)
    return None


async def _switch_agent(context: Any, agent: Any) -> bool:
    session = getattr(context, "session", None)
    if session is None or not hasattr(session, "update_agent"):
        if isinstance(getattr(session, "userdata", None), dict):
            session.userdata["pending_agent"] = agent
        return True
    try:
        await session.update_agent(agent)
        return True
    except Exception:
        return False


def execute_handoff(
    *,
    user_text: str = "",
    language: str = "",
    learner_level: str = "",
    conversation_summary: str = "",
    current_math_question: str = "",
    previous_solved_exercises: list[str] | None = None,
    learning_history: list[str] | None = None,
    recommendations: list[str] | None = None,
    user_id: str | None = None,
    memory_profile: dict[str, Any] | None = None,
    userdata: dict[str, Any] | None = None,
    router: SpecialistRouter | None = None,
    specialist_factory: SpecialistFactory | None = None,
    context_manager: SharedContextManager | None = None,
) -> HandoffResult:
    """Deterministic handoff. Never raises. Never logs transcripts."""
    log_specialist_event("handoff_requested", transcript=user_text)
    log_specialist_event("handoff_started", transcript=user_text)
    active_router = router or get_specialist_router()
    manager = context_manager or get_shared_context_manager()
    question = current_math_question or user_text
    decision = active_router.route(
        question or user_text, read_context_from_userdata(userdata)
    )

    if decision["target"] != RouteTarget.MATH_SPECIALIST.value:
        code = (
            "clarification_needed"
            if decision.get("reason") == "clarification_needed"
            else "handoff_not_applicable"
        )
        log_specialist_event("handoff_failed", secret="ignored")
        return {
            "error": True,
            "handed_off": False,
            "specialist_id": MATH_SPECIALIST_ID,
            "message": str(
                decision.get("message") or handoff_fallback_notice(language or "en")
            ),
            "code": code,
        }

    try:
        topic_hint = infer_math_topic(user_text) or infer_math_topic(question) or "math"
        context = manager.build(
            language=language,
            learner_level=learner_level,
            conversation_summary=conversation_summary,
            current_topic=topic_hint,
            current_math_question=question,
            previous_solved_exercises=previous_solved_exercises,
            learning_history=learning_history,
            recommendations=recommendations,
            user_id=user_id,
            memory_profile=memory_profile,
            existing=read_context_from_userdata(userdata),
        )
    except Exception:
        context = manager.recover(language or "en")

    factory = specialist_factory or active_router.get_factory(MATH_SPECIALIST_ID)
    agent, start_info = start_specialist_with_retry(factory, context)
    if start_info.get("error") is True or agent is None:
        manager.transfer(userdata, context, active_agent="main")
        record_handoff(success=False, recovered=True)
        log_specialist_event("handoff_failed")
        log_specialist_event("recovery_completed")
        return {
            "error": True,
            "handed_off": False,
            "specialist_id": MATH_SPECIALIST_ID,
            "message": str(
                start_info.get("message") or handoff_fallback_notice(context.language)
            ),
            "code": str(start_info.get("code") or "specialist_start_failed"),
            "context": context.as_public_dict(),
        }

    manager.transfer(userdata, context, active_agent="math_specialist")
    state = conversation_state_from_context(
        context,
        session_id=str((userdata or {}).get("analytics_call_id") or ""),
        active_agent="math_specialist",
        previous_agent="main",
        existing=read_state_from_userdata(userdata),
    )
    append_specialist_history(
        state,
        specialist_id=MATH_SPECIALIST_ID,
        outcome="started",
        reason_for_handoff=str(decision.get("reason") or "math_request"),
    )
    apply_state_to_userdata(userdata, state)
    record_handoff(success=True)
    log_specialist_event("handoff_completed")
    result: HandoffResult = {
        "error": False,
        "handed_off": True,
        "specialist_id": MATH_SPECIALIST_ID,
        "message": handoff_notice(context.language),
        "context": context.as_public_dict(),
    }
    result["agent"] = agent  # type: ignore[typeddict-unknown-key]
    return result


def execute_handback(
    *,
    user_text: str = "",
    reason: str = "",
    solved_exercise_summary: str = "",
    conversation_summary: str = "",
    recommendations: list[str] | None = None,
    userdata: dict[str, Any] | None = None,
    current_context: SpecialistContext | None = None,
    problem_solved: bool = False,
    practice_completed: bool = False,
    main_agent_factory: MainAgentFactory | None = None,
    completion_status: str = "",
    updated_learning_level: str = "",
    context_manager: SharedContextManager | None = None,
) -> HandbackResult:
    """Deterministic handback. On failure the specialist continues."""
    log_specialist_event("handback_requested", transcript=user_text)
    manager = context_manager or get_shared_context_manager()
    try:
        context = current_context or manager.load_or_recover(userdata)[0]
    except Exception:
        context = manager.recover()
    merged = manager.merge_handback(
        context,
        solved_exercise_summary=solved_exercise_summary,
        conversation_summary=conversation_summary,
        recommendations=recommendations,
        completion_status=completion_status
        or ("completed" if problem_solved or practice_completed else ""),
        updated_learning_level=updated_learning_level,
    )

    if (
        user_text
        and not problem_solved
        and not practice_completed
        and reason not in {"solved", "thank_you", "topic_change", "completed"}
        and not should_return_to_main(user_text)
    ):
        log_specialist_event("handback_failed")
        return {
            "error": True,
            "returned": False,
            "fallback": "specialist_continues",
            "message": "Handback not applicable.",
            "code": "handback_not_applicable",
            "context": merged.as_public_dict(),
        }

    factory = main_agent_factory
    if factory is None:

        def factory(**_kwargs: Any) -> Any:
            from agent import Assistant

            return Assistant(resume_from_specialist=True)

    try:
        agent = factory(resume_from_specialist=True)
    except Exception:
        log_specialist_event("handback_failed")
        record_handback(success=False)
        return {
            "error": True,
            "returned": False,
            "fallback": "specialist_continues",
            "message": "Unable to resume the main learning assistant.",
            "code": "main_agent_resume_failed",
            "context": merged.as_public_dict(),
        }

    manager.transfer(userdata, merged, active_agent="main", resume=True)
    state = conversation_state_from_context(
        merged,
        session_id=str((userdata or {}).get("analytics_call_id") or ""),
        active_agent="main",
        previous_agent="math_specialist",
        existing=read_state_from_userdata(userdata),
    )
    append_specialist_history(
        state,
        specialist_id=MATH_SPECIALIST_ID,
        outcome="completed"
        if problem_solved or practice_completed
        else reason or "returned",
        reason_for_handoff="handback",
    )
    apply_state_to_userdata(userdata, state)
    record_handback(
        success=True,
        exercises=len(merged.previous_solved_exercises),
    )
    log_specialist_event("handback_completed")
    closing = build_handback_summary(merged, merged.language)
    result: HandbackResult = {
        "error": False,
        "returned": True,
        "fallback": "",
        "message": closing,
        "context": merged.as_public_dict(),
    }
    result["agent"] = agent  # type: ignore[typeddict-unknown-key]
    return result


@function_tool()
async def handoff_to_math_specialist(
    context: RunContext,
    current_math_question: str = "",
    conversation_summary: str = "",
    learner_level: str = "",
    language: str = "",
) -> dict[str, Any]:
    """Hand the learner to the Math Practice Specialist.

    Call ONLY when the learner asks to solve or practice mathematics:
    arithmetic, addition, subtraction, multiplication, division, fractions,
    decimals, percentages, algebra, geometry, times tables, mental math,
    or word problems.

    Examples that SHOULD trigger this tool:
    - I need help solving 24 x 18
    - Can you teach fractions?
    - Let's practice multiplication
    - Help me with percentages

    Do NOT call for greetings, science, English, memory, escalation,
    telephony, or analytics.

    Before calling, tell the learner you are connecting them to the
    Math Practice Specialist. Do not switch silently.

    Args:
        current_math_question: The math question or topic to transfer.
        conversation_summary: Short summary of the conversation so far.
        learner_level: Saved or stated learner level when known.
        language: Learner language (en or hi).
    """
    userdata = _session_userdata(context)
    result = execute_handoff(
        user_text=current_math_question,
        language=language,
        learner_level=learner_level,
        conversation_summary=conversation_summary,
        current_math_question=current_math_question,
        user_id=_session_user_id(context, userdata),
        userdata=userdata,
    )
    if result.get("error") is True:
        return {
            "error": True,
            "handed_off": False,
            "message": result.get("message") or handoff_fallback_notice(language),
            "code": result.get("code") or "handoff_failed",
        }

    agent = result.pop("agent", None)
    switched = await _switch_agent(context, agent)
    if not switched:
        log_specialist_event("handoff_failed")
        return {
            "error": True,
            "handed_off": False,
            "message": handoff_fallback_notice(language or "en"),
            "code": "handoff_switch_failed",
        }
    return {
        "error": False,
        "handed_off": True,
        "specialist_id": MATH_SPECIALIST_ID,
        "message": result.get("message") or handoff_notice(language or "en"),
        "context": result.get("context") or {},
    }


@function_tool()
async def return_to_main_agent(
    context: RunContext,
    reason: str = "",
    solved_exercise_summary: str = "",
    conversation_summary: str = "",
) -> dict[str, Any]:
    """Return the learner to the main learning assistant.

    Call when:
    - the math problem is solved
    - the learner says thank you
    - the learner asks a non-math question
    - the topic changes
    - the practice session is complete

    Before calling, tell the learner you are returning them to the
    main learning assistant. Do not switch silently.

    Args:
        reason: solved, thank_you, topic_change, or completed.
        solved_exercise_summary: Short summary of what was practiced.
        conversation_summary: Updated conversation summary.
    """
    userdata = _session_userdata(context)
    current = read_context_from_userdata(userdata)
    result = execute_handback(
        reason=reason,
        solved_exercise_summary=solved_exercise_summary,
        conversation_summary=conversation_summary,
        userdata=userdata,
        current_context=current,
        problem_solved=reason == "solved",
        practice_completed=reason == "completed",
    )
    if result.get("error") is True:
        return {
            "error": True,
            "returned": False,
            "fallback": result.get("fallback") or "specialist_continues",
            "message": result.get("message")
            or "Unable to resume the main learning assistant.",
            "code": result.get("code") or "handback_failed",
        }

    agent = result.pop("agent", None)
    switched = await _switch_agent(context, agent)
    if not switched:
        log_specialist_event("handback_failed")
        return {
            "error": True,
            "returned": False,
            "fallback": "specialist_continues",
            "message": "Unable to resume the main learning assistant.",
            "code": "handback_switch_failed",
        }
    return {
        "error": False,
        "returned": True,
        "message": result.get("message") or handback_notice(current.language),
        "context": result.get("context") or {},
    }


HANDOFF_TOOLS = [handoff_to_math_specialist]
HANDBACK_TOOLS = [return_to_main_agent]

__all__ = [
    "HANDBACK_TOOLS",
    "HANDOFF_TOOLS",
    "execute_handback",
    "execute_handoff",
    "handoff_to_math_specialist",
    "return_to_main_agent",
    "should_return_to_main",
]
