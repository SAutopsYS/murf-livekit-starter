"""Specialist agents for the Learning and Literacy track.

The Main Tutor remains the primary conversational agent. Specialists are
extensions, not replacements. Only the Math Practice Specialist is active.
"""

from specialists.context import (
    build_specialist_context,
    merge_handback_context,
    read_context_from_userdata,
)
from specialists.handoff import (
    HANDBACK_TOOLS,
    HANDOFF_TOOLS,
    execute_handback,
    execute_handoff,
    handoff_to_math_specialist,
    return_to_main_agent,
)
from specialists.intent import (
    detect_intent,
    should_handoff_to_math,
    should_return_to_main,
)
from specialists.math_specialist import (
    MathPracticeSpecialist,
    get_inherited_language_policy,
    get_math_specialist_prompt,
    is_in_scope,
    refuse_out_of_scope,
)
from specialists.prompts import MATH_SPECIALIST_PROMPT, build_math_specialist_prompt
from specialists.registry import (
    MATH_SPECIALIST_ID,
    disable_specialist,
    discover_capabilities,
    enable_specialist,
    get_specialist,
    list_active_specialists,
    list_disabled_specialists,
    list_specialists,
    register_specialist,
    reset_specialist_registry,
    unregister_specialist,
)
from specialists.router import SpecialistRouter, get_specialist_router
from specialists.schemas import RouteTarget, SpecialistContext
from specialists.shared_context import (
    SharedContextManager,
    continuity_opening,
    get_shared_context_manager,
)

__all__ = [
    "HANDBACK_TOOLS",
    "HANDOFF_TOOLS",
    "MATH_SPECIALIST_ID",
    "MATH_SPECIALIST_PROMPT",
    "MathPracticeSpecialist",
    "RouteTarget",
    "SharedContextManager",
    "SpecialistContext",
    "SpecialistRouter",
    "build_math_specialist_prompt",
    "build_specialist_context",
    "continuity_opening",
    "detect_intent",
    "disable_specialist",
    "discover_capabilities",
    "enable_specialist",
    "execute_handback",
    "execute_handoff",
    "get_inherited_language_policy",
    "get_math_specialist_prompt",
    "get_shared_context_manager",
    "get_specialist",
    "get_specialist_router",
    "handoff_to_math_specialist",
    "is_in_scope",
    "list_active_specialists",
    "list_disabled_specialists",
    "list_specialists",
    "merge_handback_context",
    "read_context_from_userdata",
    "refuse_out_of_scope",
    "register_specialist",
    "reset_specialist_registry",
    "return_to_main_agent",
    "should_handoff_to_math",
    "should_return_to_main",
    "unregister_specialist",
]
