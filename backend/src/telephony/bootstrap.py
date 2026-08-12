"""Outbound conversation bootstrap messages.

No LiveKit/Twilio code. Deterministic structured intros only.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("telephony.bootstrap")

_STOP_EN = "If you do not wish to receive these calls, simply tell me to stop."
_STOP_HI = "अगर आप ये कॉल नहीं चाहती या चाहते, तो बस मुझसे बंद करने के लिए कहें।"


def _is_hindi(language: str) -> bool:
    normalized = language.strip().lower().replace("_", "-")
    return normalized in {"hi", "hi-in", "hindi"} or normalized.startswith("hi-")


def _purpose_label_en(purpose: str) -> str:
    cleaned = purpose.strip().replace("_", " ")
    return cleaned or "English speaking practice"


def _purpose_label_hi(purpose: str) -> str:
    mapping = {
        "daily_practice": "रोजाना अंग्रेज़ी बोलने का अभ्यास",
        "speaking_practice": "अंग्रेज़ी बोलने का अभ्यास",
        "exercise": "अभ्यास गतिविधि",
        "escalation_resolution": "हल हो चुके सहायता अनुरोध",
    }
    key = purpose.strip().lower()
    return mapping.get(key, "अंग्रेज़ी बोलने का अभ्यास")


def _resolution_intro(language: str) -> str:
    """Bootstrap intro for resolved human-help callback calls."""
    if _is_hindi(language):
        return (
            "नमस्ते! मैं VoiceForBharat Tutor बोल रहा हूँ। "
            "यह कॉल आपके हल हो चुके सहायता अनुरोध के बारे में है। "
            "मैं आपको समाधान के बारे में बताने के लिए कॉल कर रहा हूँ। "
            f"{_STOP_HI}"
        )
    return (
        "Hello, this is VoiceForBharat Tutor calling about your resolved "
        "support request. I'm calling to let you know about the resolution. "
        "If you do not wish to receive future calls, please tell me to stop."
    )


class ConversationBootstrap:
    """Build the first outbound-call greeting before tutor conversation continues."""

    def build_intro(
        self,
        learner_name: str | None,
        purpose: str,
        language: str,
    ) -> dict[str, Any]:
        """Return a structured outbound introduction.

        Never raises. Uses Devanagari for Hindi and English script for English.
        """
        if not isinstance(purpose, str) or not purpose.strip():
            purpose = "daily_practice"
        if not isinstance(language, str) or not language.strip():
            language = "en-IN"

        hindi = _is_hindi(language)
        name = learner_name.strip() if isinstance(learner_name, str) else ""
        purpose_key = purpose.strip().lower()

        if purpose_key == "escalation_resolution":
            intro = _resolution_intro(language)
        elif hindi:
            greeting = f"नमस्ते{(' ' + name) if name else ''}!"
            body = (
                f"मैं VoiceForBharat Tutor बोल रहा हूँ। "
                f"यह कॉल आपके {_purpose_label_hi(purpose)} के लिए है। "
                f"{_STOP_HI}"
            )
            intro = f"{greeting} {body}"
        else:
            if purpose_key == "daily_practice":
                reason = "your daily English speaking practice"
            else:
                reason = f"your {_purpose_label_en(purpose)}"
            greeting = f"Hello{(' ' + name) if name else ''}!"
            body = (
                f"This is VoiceForBharat Tutor calling for {reason}. {_STOP_EN}"
            )
            intro = f"{greeting} {body}"

        logger.info("Bootstrap message created")
        return {
            "intro": intro,
            "purpose": purpose.strip(),
            "language": language.strip(),
            "includes_stop_instruction": True,
        }
