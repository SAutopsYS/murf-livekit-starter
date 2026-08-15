"""API contract helpers for a future SDK. Does not redesign existing routes."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T")

API_VERSION = "v1"


@dataclass(frozen=True)
class ApiError:
    code: str
    message: str
    status: int


@dataclass(frozen=True)
class CursorPage(Generic[T]):
    items: tuple[T, ...]
    next_cursor: str | None
    limit: int


@dataclass(frozen=True)
class ApiEnvelope(Generic[T]):
    version: str
    ok: bool
    data: T | None
    error: ApiError | None


def ok(data: T, version: str = API_VERSION) -> ApiEnvelope[T]:
    return ApiEnvelope(version=version, ok=True, data=data, error=None)


def fail(
    code: str, message: str, status: int, version: str = API_VERSION
) -> ApiEnvelope[None]:
    return ApiEnvelope(
        version=version,
        ok=False,
        data=None,
        error=ApiError(code=code, message=message, status=status),
    )


def envelope_dict(envelope: ApiEnvelope[Any]) -> dict[str, Any]:
    return asdict(envelope)


def paginate(items: list[T], *, cursor: int = 0, limit: int = 20) -> CursorPage[T]:
    window = items[cursor : cursor + limit]
    nxt = cursor + limit if cursor + limit < len(items) else None
    return CursorPage(
        items=tuple(window),
        next_cursor=str(nxt) if nxt is not None else None,
        limit=limit,
    )
