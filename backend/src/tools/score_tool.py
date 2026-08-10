"""Rule-based spoken-answer scoring for Learning & Literacy.

Deterministic heuristics only. No LLM and no external APIs.
LiveKit registration comes in a later phase.
"""

from __future__ import annotations

import logging
import re
from typing import TypedDict

from tools.exercise_tool import normalize_level
from tools.metrics import track_tool_call

logger = logging.getLogger("tools.score")

_SCORE_UNAVAILABLE = {
    "error": True,
    "message": "Unable to score the spoken answer.",
}

# Minimum usable spoken answer length (words).
_MIN_WORD_COUNT = 3

# Level targets used for word-count scoring (inclusive soft ranges).
_WORD_TARGETS: dict[str, tuple[int, int]] = {
    "beginner": (12, 40),
    "intermediate": (25, 70),
    "advanced": (40, 100),
}

_WORD_RE = re.compile(r"[A-Za-z0-9']+")
_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")


class ScoreMetrics(TypedDict):
    """Numeric metrics included in a successful score payload."""

    word_count: int
    unique_words: int
    sentence_count: int


class ScoreResult(TypedDict):
    """Successful spoken-answer score payload."""

    score: int
    level: str
    feedback: list[str]
    metrics: ScoreMetrics
    source: str


class ScoreError(TypedDict):
    """Structured failure payload for the scoring tool."""

    error: bool
    message: str


def count_words(answer: str) -> int:
    """Count alphabetic/numeric tokens in the answer."""
    return len(_WORD_RE.findall(answer))


def count_unique_words(answer: str) -> int:
    """Count unique lowercase word tokens in the answer."""
    words = [token.lower() for token in _WORD_RE.findall(answer)]
    return len(set(words))


def count_sentences(answer: str) -> int:
    """Estimate sentence count from punctuation-delimited segments."""
    parts = [part.strip() for part in _SENTENCE_SPLIT_RE.split(answer) if part.strip()]
    if parts:
        return len(parts)
    # One unfinished thought still counts as a sentence attempt when words exist.
    return 1 if count_words(answer) > 0 else 0


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _word_count_score(word_count: int, level: str) -> float:
    low, high = _WORD_TARGETS[level]
    if word_count <= 0:
        return 0.0
    if word_count < low:
        return _clamp((word_count / low) * 70.0)
    if word_count <= high:
        # Inside target band: scale from 70 to 100.
        span = max(high - low, 1)
        return _clamp(70.0 + ((word_count - low) / span) * 30.0)
    # Slightly past target remains strong; extreme length soft-caps.
    overflow = word_count - high
    return _clamp(100.0 - min(overflow * 0.5, 15.0))


def _vocabulary_score(word_count: int, unique_words: int) -> float:
    if word_count <= 0:
        return 0.0
    diversity = unique_words / word_count
    # Diversity alone can look high on tiny answers; blend with unique volume.
    volume = _clamp((unique_words / 20.0) * 100.0)
    return _clamp((diversity * 70.0) + (volume * 0.30))


def _sentence_completion_score(answer: str, sentence_count: int, word_count: int) -> float:
    if word_count <= 0:
        return 0.0
    ending_punct = 1.0 if answer.rstrip().endswith((".", "!", "?")) else 0.0
    density = _clamp((sentence_count / max(word_count / 12.0, 1.0)) * 100.0)
    return _clamp((density * 0.65) + (ending_punct * 35.0))


def _punctuation_score(answer: str) -> float:
    punct_marks = sum(answer.count(mark) for mark in ".!?,;:")
    if punct_marks <= 0:
        return 35.0
    if punct_marks == 1:
        return 70.0
    if punct_marks <= 4:
        return 90.0
    return 100.0


def compute_score(
    *,
    answer: str,
    level: str,
    word_count: int,
    unique_words: int,
    sentence_count: int,
) -> int:
    """Compute a deterministic 0–100 overall score from lightweight metrics."""
    word_part = _word_count_score(word_count, level)
    vocab_part = _vocabulary_score(word_count, unique_words)
    sentence_part = _sentence_completion_score(answer, sentence_count, word_count)
    punct_part = _punctuation_score(answer)

    overall = (
        (word_part * 0.35)
        + (vocab_part * 0.30)
        + (sentence_part * 0.20)
        + (punct_part * 0.15)
    )
    return int(round(_clamp(overall)))


def generate_feedback(
    *,
    score: int,
    level: str,
    word_count: int,
    unique_words: int,
    sentence_count: int,
    answer: str,
) -> list[str]:
    """Build short, non-conversational feedback strings from metrics."""
    feedback: list[str] = []
    low, high = _WORD_TARGETS[level]

    if word_count < low:
        feedback.append("Try speaking a little longer.")
    elif word_count <= high:
        feedback.append("Good sentence length.")
    else:
        feedback.append("Strong answer length.")

    diversity = (unique_words / word_count) if word_count else 0.0
    if diversity < 0.55:
        feedback.append("Try using more descriptive words.")
    else:
        feedback.append("Nice vocabulary variety.")

    if sentence_count < 2 or not answer.rstrip().endswith((".", "!", "?")):
        feedback.append("Finish thoughts with clear sentence endings.")
    elif score >= 75:
        feedback.append("Speak a little more confidently.")
    else:
        feedback.append("Keep practicing clear full sentences.")

    return feedback[:3]


def _score_spoken_answer_impl(answer: str, level: str) -> ScoreResult | ScoreError:
    if not isinstance(answer, str) or not isinstance(level, str):
        return dict(_SCORE_UNAVAILABLE)  # type: ignore[return-value]

    normalized_level = normalize_level(level)
    if normalized_level is None:
        logger.info("Unable to score answer: unknown level %r", level)
        return dict(_SCORE_UNAVAILABLE)  # type: ignore[return-value]

    cleaned = answer.strip()
    if not cleaned:
        logger.info("Unable to score answer: empty response")
        return dict(_SCORE_UNAVAILABLE)  # type: ignore[return-value]

    word_count = count_words(cleaned)
    if word_count < _MIN_WORD_COUNT:
        logger.info("Unable to score answer: too short (%s words)", word_count)
        return dict(_SCORE_UNAVAILABLE)  # type: ignore[return-value]

    unique_words = count_unique_words(cleaned)
    sentence_count = count_sentences(cleaned)
    score = compute_score(
        answer=cleaned,
        level=normalized_level,
        word_count=word_count,
        unique_words=unique_words,
        sentence_count=sentence_count,
    )
    feedback = generate_feedback(
        score=score,
        level=normalized_level,
        word_count=word_count,
        unique_words=unique_words,
        sentence_count=sentence_count,
        answer=cleaned,
    )

    return {
        "score": score,
        "level": normalized_level,
        "feedback": feedback,
        "metrics": {
            "word_count": word_count,
            "unique_words": unique_words,
            "sentence_count": sentence_count,
        },
        "source": "rule_based",
    }


def score_spoken_answer(answer: str, level: str) -> ScoreResult | ScoreError:
    """Score a learner's spoken answer with deterministic rules.

    Args:
        answer: Transcript text of the spoken response.
        level: Learner level (beginner, intermediate, or advanced).

    Returns:
        Structured score data, or a structured error when scoring is not possible.
    """
    return track_tool_call("score_tool", _score_spoken_answer_impl, answer, level)
