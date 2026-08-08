"""Data-access methods for learner memory. No business logic."""

from __future__ import annotations

import logging
import sqlite3
from datetime import datetime, timezone

from memory.database import get_connection, get_database_path
from memory.models import User

logger = logging.getLogger("memory.repository")

_USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL DEFAULT '',
    language_preference TEXT NOT NULL DEFAULT '',
    learning_level TEXT NOT NULL DEFAULT '',
    grammar_level TEXT NOT NULL DEFAULT '',
    speaking_confidence TEXT NOT NULL DEFAULT '',
    common_mistakes TEXT NOT NULL DEFAULT '[]',
    last_topics TEXT NOT NULL DEFAULT '[]',
    consent INTEGER NOT NULL DEFAULT 0,
    last_interaction TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
"""

_USERS_USER_ID_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_users_user_id ON users (user_id)
"""

_USER_COLUMNS = (
    "id",
    "user_id",
    "name",
    "language_preference",
    "learning_level",
    "grammar_level",
    "speaking_confidence",
    "common_mistakes",
    "last_topics",
    "consent",
    "last_interaction",
    "created_at",
    "updated_at",
)

_SELECT_USER_COLUMNS_SQL = f"SELECT {', '.join(_USER_COLUMNS)} FROM users"

_SELECT_USER_BY_USER_ID_SQL = f"""
{_SELECT_USER_COLUMNS_SQL}
WHERE user_id = ?
"""

_SELECT_USER_EXISTS_SQL = "SELECT 1 FROM users WHERE user_id = ? LIMIT 1"

_SELECT_ALL_USERS_SQL = f"""
{_SELECT_USER_COLUMNS_SQL}
ORDER BY id ASC
"""

_COUNT_USERS_SQL = "SELECT COUNT(*) AS user_count FROM users"

_INSERT_USER_SQL = """
INSERT INTO users (
    user_id,
    name,
    language_preference,
    learning_level,
    grammar_level,
    speaking_confidence,
    common_mistakes,
    last_topics,
    consent,
    last_interaction,
    created_at,
    updated_at
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_UPDATE_USER_SQL = """
UPDATE users
SET
    name = ?,
    language_preference = ?,
    learning_level = ?,
    grammar_level = ?,
    speaking_confidence = ?,
    common_mistakes = ?,
    last_topics = ?,
    consent = ?,
    last_interaction = ?,
    updated_at = ?
WHERE user_id = ?
"""

_DELETE_USER_SQL = "DELETE FROM users WHERE user_id = ?"

_UPDATE_LAST_INTERACTION_SQL = """
UPDATE users
SET last_interaction = ?, updated_at = ?
WHERE user_id = ?
"""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def initialize_database() -> bool:
    """Create the data directory, database file, and tables if needed.

    Returns True on success. Logs and returns False on database errors.
    """
    try:
        with get_connection() as connection:
            connection.execute(_USERS_TABLE_SQL)
            connection.execute(_USERS_USER_ID_INDEX_SQL)
            connection.commit()
        logger.info("Memory database ready at %s", get_database_path())
        return True
    except sqlite3.Error:
        logger.exception("Failed to initialize memory database")
        return False


def create_user(user: User) -> User | None:
    """Insert a new learner profile and return the stored User.

    Returns None when user_id already exists or a database error occurs.
    """
    now = _utc_now_iso()
    created_at = user.created_at or now
    updated_at = user.updated_at or now

    try:
        with get_connection() as connection:
            connection.execute(
                _INSERT_USER_SQL,
                user.insert_params(created_at=created_at, updated_at=updated_at),
            )
            connection.commit()
    except sqlite3.IntegrityError:
        logger.warning("Duplicate user_id, create skipped: %s", user.user_id)
        return None
    except sqlite3.Error:
        logger.exception("Failed to create user %s", user.user_id)
        return None

    return get_user_by_id(user.user_id)


def get_user_by_id(user_id: str) -> User | None:
    """Fetch a learner by external user_id. Returns None if missing."""
    try:
        with get_connection() as connection:
            row = connection.execute(_SELECT_USER_BY_USER_ID_SQL, (user_id,)).fetchone()
    except sqlite3.Error:
        logger.exception("Failed to fetch user %s", user_id)
        return None

    if row is None:
        return None
    return User.from_row(row)


def update_user(user: User) -> User | None:
    """Update mutable learner fields for an existing user_id.

    Returns None when the user is missing or a database error occurs.
    """
    if not user_exists(user.user_id):
        logger.info("update_user skipped; user not found: %s", user.user_id)
        return None

    updated_at = _utc_now_iso()
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                _UPDATE_USER_SQL,
                user.update_params(updated_at=updated_at),
            )
            connection.commit()
            if cursor.rowcount == 0:
                return None
    except sqlite3.Error:
        logger.exception("Failed to update user %s", user.user_id)
        return None

    return get_user_by_id(user.user_id)


def delete_user(user_id: str) -> bool:
    """Delete a learner profile. Returns True when a row was removed."""
    try:
        with get_connection() as connection:
            cursor = connection.execute(_DELETE_USER_SQL, (user_id,))
            connection.commit()
            return cursor.rowcount > 0
    except sqlite3.Error:
        logger.exception("Failed to delete user %s", user_id)
        return False


def update_last_interaction(user_id: str, timestamp: str | None = None) -> User | None:
    """Set last_interaction (and updated_at) for an existing learner.

    Returns None when the user is missing or a database error occurs.
    """
    if not user_exists(user_id):
        logger.info("update_last_interaction skipped; user not found: %s", user_id)
        return None

    interaction_at = timestamp or _utc_now_iso()
    updated_at = _utc_now_iso()

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                _UPDATE_LAST_INTERACTION_SQL,
                (interaction_at, updated_at, user_id),
            )
            connection.commit()
            if cursor.rowcount == 0:
                return None
    except sqlite3.Error:
        logger.exception("Failed to update last_interaction for %s", user_id)
        return None

    return get_user_by_id(user_id)


def user_exists(user_id: str) -> bool:
    """Return True when a learner with the given user_id exists."""
    try:
        with get_connection() as connection:
            row = connection.execute(_SELECT_USER_EXISTS_SQL, (user_id,)).fetchone()
    except sqlite3.Error:
        logger.exception("Failed to check existence for user %s", user_id)
        return False
    return row is not None


def list_users() -> list[User]:
    """Return all learner profiles as User objects. Empty list on error."""
    try:
        with get_connection() as connection:
            rows = connection.execute(_SELECT_ALL_USERS_SQL).fetchall()
    except sqlite3.Error:
        logger.exception("Failed to list users")
        return []
    return [User.from_row(row) for row in rows]


def count_users() -> int:
    """Return the number of stored learner profiles. Returns 0 on error."""
    try:
        with get_connection() as connection:
            row = connection.execute(_COUNT_USERS_SQL).fetchone()
    except sqlite3.Error:
        logger.exception("Failed to count users")
        return 0
    if row is None:
        return 0
    return int(row["user_count"])
