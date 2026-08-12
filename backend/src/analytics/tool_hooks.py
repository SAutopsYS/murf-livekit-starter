"""Optional tool wrappers that mark exercise completion for analytics.

Does not modify learning-tool business logic; only observes successful scores.
"""

from __future__ import annotations

import logging
from typing import Any

from livekit.agents import RunContext, function_tool

from tools.score_tool import score_spoken_answer as score_answer_impl

logger = logging.getLogger("analytics.tool_hooks")


@function_tool()
async def score_spoken_answer(
    context: RunContext,
    answer: str,
    level: str,
) -> dict[str, Any]:
    """Score a spoken answer and mark analytics exercise completion on success."""
    logger.info("Scoring tool invoked")
    result = score_answer_impl(answer, level)
    if result.get("error"):
        logger.info("Scoring failed")
        return dict(result)

    logger.info("Answer scored")
    session = getattr(context, "session", None)
    userdata = getattr(session, "userdata", None) if session else None
    if isinstance(userdata, dict):
        userdata["analytics_exercise_completed"] = True
    return dict(result)
