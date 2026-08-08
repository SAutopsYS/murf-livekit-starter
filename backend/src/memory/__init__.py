"""Persistent memory foundation for the Learning & Literacy tutor.

Phase 3 exposes LiveKit function tools that call the repository.
"""

from memory.async_lookup import SessionMemoryLookup
from memory.models import User
from memory.repository import (
    count_users,
    create_user,
    delete_user,
    get_user_by_id,
    initialize_database,
    list_users,
    update_last_interaction,
    update_user,
    user_exists,
)
from memory.tools import MEMORY_TOOLS

__all__ = [
    "MEMORY_TOOLS",
    "SessionMemoryLookup",
    "User",
    "count_users",
    "create_user",
    "delete_user",
    "get_user_by_id",
    "initialize_database",
    "list_users",
    "update_last_interaction",
    "update_user",
    "user_exists",
]
