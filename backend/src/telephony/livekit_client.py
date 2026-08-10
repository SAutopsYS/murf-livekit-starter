"""LiveKit telephony client for outbound SIP calls.

No prompt, learning, or memory logic.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any, Protocol

from telephony.config import TelephonyConfig

logger = logging.getLogger("telephony.livekit_client")

_CALL_UNAVAILABLE = {
    "error": True,
    "message": "Unable to place outbound call.",
}


class OutboundDialer(Protocol):
    """Injectable dialer used by TelephonyService.place_call."""

    def place_outbound_call(
        self,
        *,
        phone_number: str,
        purpose: str,
        language: str,
        room_name: str | None = None,
    ) -> dict[str, Any]: ...


class LiveKitTelephonyClient:
    """Place outbound calls through the LiveKit SIP API."""

    def __init__(self, config: TelephonyConfig) -> None:
        self._config = config
        logger.info("LiveKit telephony initialized")

    def is_configured(self) -> bool:
        """Return True when LiveKit + outbound SIP trunk are configured."""
        return self._config.outbound_ready

    def _build_room_name(self, purpose: str) -> str:
        safe_purpose = "".join(
            ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in purpose.strip()
        )
        safe_purpose = safe_purpose.strip("-_") or "practice"
        return f"outbound-{safe_purpose}-{uuid.uuid4().hex[:10]}"

    async def _place_outbound_call_async(
        self,
        *,
        phone_number: str,
        purpose: str,
        language: str,
        room_name: str | None = None,
    ) -> dict[str, Any]:
        if not self.is_configured():
            logger.info("Outbound call failed")
            return dict(_CALL_UNAVAILABLE)

        from livekit import api

        room = room_name or self._build_room_name(purpose)
        identity = f"sip-outbound-{uuid.uuid4().hex[:10]}"
        logger.info("Outbound call started")

        lkapi = api.LiveKitAPI(
            url=self._config.livekit_url,
            api_key=self._config.livekit_api_key,
            api_secret=self._config.livekit_api_secret,
        )
        try:
            request = api.CreateSIPParticipantRequest(
                sip_trunk_id=self._config.sip_outbound_trunk_id,
                sip_call_to=phone_number,
                room_name=room,
                participant_identity=identity,
                participant_name=self._config.outbound_caller_name,
                wait_until_answered=False,
            )
            participant = await lkapi.sip.create_sip_participant(request)
        except TimeoutError:
            logger.info("Outbound call failed")
            return dict(_CALL_UNAVAILABLE)
        except Exception:
            logger.info("Outbound call failed")
            return dict(_CALL_UNAVAILABLE)
        finally:
            await lkapi.aclose()

        call_id = getattr(participant, "sip_call_id", None) or getattr(
            participant,
            "participant_id",
            "",
        )
        if not call_id:
            logger.info("Outbound call failed")
            return dict(_CALL_UNAVAILABLE)

        logger.info("Outbound call placed")
        return {
            "status": "calling",
            "provider": "livekit",
            "call_id": str(call_id),
            "purpose": purpose,
            "language": language,
            "room_name": room,
            "participant_identity": identity,
        }

    def place_outbound_call(
        self,
        *,
        phone_number: str,
        purpose: str,
        language: str,
        room_name: str | None = None,
    ) -> dict[str, Any]:
        """Synchronously place an outbound call and return structured data."""
        try:
            return asyncio.run(
                self._place_outbound_call_async(
                    phone_number=phone_number,
                    purpose=purpose,
                    language=language,
                    room_name=room_name,
                )
            )
        except RuntimeError:
            # Nested event loop (e.g. pytest-asyncio) — use a private loop.
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(
                    self._place_outbound_call_async(
                        phone_number=phone_number,
                        purpose=purpose,
                        language=language,
                        room_name=room_name,
                    )
                )
            finally:
                loop.close()
        except Exception:
            logger.info("Outbound call failed")
            return dict(_CALL_UNAVAILABLE)
