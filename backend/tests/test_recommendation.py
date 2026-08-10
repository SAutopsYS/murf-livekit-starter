"""Day 5 Phase 6: adaptive follow-up practice recommendations."""

from __future__ import annotations

import logging

import pytest

from agent import AGENT_TOOLS, SYSTEM_PROMPT
from tools import LEARNING_TOOLS
from tools.livekit_tools import get_next_exercise, recommend_next_practice, score_spoken_answer
from tools.recommendation import recommend_next_practice as build_recommendation


def test_recommendation_tool_registered() -> None:
    learning_names = [
        getattr(tool, "name", getattr(tool, "__name__", "")) for tool in LEARNING_TOOLS
    ]
    assert "recommend_next_practice" in learning_names

    agent_names = [
        getattr(tool, "name", getattr(tool, "__name__", "")) for tool in AGENT_TOOLS
    ]
    assert "recommend_next_practice" in agent_names
    assert "FOLLOW-UP PRACTICE" in SYSTEM_PROMPT
    assert "Use the recommendation tool." in SYSTEM_PROMPT


def test_low_score_repeats_level() -> None:
    result = build_recommendation(42, "beginner")
    assert result.get("error") is not True
    assert result["recommendation"] == "repeat_same_level"
    assert result["next_level"] == "beginner"


def test_medium_score_keeps_level() -> None:
    result = build_recommendation(65, "intermediate")
    assert result.get("error") is not True
    assert result["recommendation"] == "continue_same_level"
    assert result["next_level"] == "intermediate"


def test_high_score_advances_level() -> None:
    result = build_recommendation(88, "beginner")
    assert result.get("error") is not True
    assert result["recommendation"] == "advance_level"
    assert result["next_level"] == "intermediate"

    top = build_recommendation(95, "advanced")
    assert top.get("error") is not True
    assert top["recommendation"] == "continue_same_level"
    assert top["next_level"] == "advanced"


def test_recommendation_invalid_input() -> None:
    assert build_recommendation(-1, "beginner")["error"] is True
    assert build_recommendation(101, "beginner")["error"] is True
    assert build_recommendation(80, "expert")["error"] is True


@pytest.mark.asyncio
async def test_recommendation_chain_with_follow_up(
    caplog: pytest.LogCaptureFixture,
) -> None:
    answer = (
        "Hello, my name is Saloni. I wake up early and drink tea. "
        "I like reading books every morning because stories help me learn new words."
    )

    with caplog.at_level(logging.INFO, logger="tools.livekit"):
        scored = await score_spoken_answer(object(), answer=answer, level="beginner")
        assert scored.get("error") is not True

        recommendation = await recommend_next_practice(
            object(),
            score=scored["score"],
            level="beginner",
        )
        assert recommendation.get("error") is not True
        assert recommendation["next_level"] in {
            "beginner",
            "intermediate",
            "advanced",
        }

        follow_up = await get_next_exercise(
            object(),
            level=recommendation["next_level"],
        )

    assert follow_up.get("error") is not True
    assert follow_up["level"] == recommendation["next_level"]

    messages = [record.getMessage() for record in caplog.records]
    assert "Follow-up exercise selected" in messages

    # Core recommendation logs live on the recommendation logger.
    with caplog.at_level(logging.INFO, logger="tools.recommendation"):
        await recommend_next_practice(object(), score=40, level="beginner")
        await recommend_next_practice(object(), score=90, level="beginner")

    messages = [record.getMessage() for record in caplog.records]
    assert "Recommendation generated" in messages
    assert "Repeating level" in messages
    assert "Advancing learner" in messages
