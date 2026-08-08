"""SQLite connection helpers for the memory database.

Schema SQL lives in repository.py. This module only manages paths and connections.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

# backend/data/memory.db (backend/ is two levels above this file: memory/ -> src/ -> backend/)
BACKEND_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = BACKEND_ROOT / "data"
DEFAULT_DATABASE_PATH = DATA_DIR / "memory.db"

_database_path_override: Path | None = None


def get_database_path() -> Path:
    """Return the active database path (override used by tests)."""
    return _database_path_override or DEFAULT_DATABASE_PATH


def set_database_path(path: Path | None) -> None:
    """Override the database path. Pass None to restore the default."""
    global _database_path_override
    _database_path_override = path


@contextmanager
def temporary_database(path: Path) -> Iterator[Path]:
    """Use a temporary database path within a context (for tests)."""
    previous = _database_path_override
    set_database_path(path)
    try:
        yield path
    finally:
        set_database_path(previous)


def ensure_data_dir(db_path: Path | None = None) -> Path:
    """Create the parent directory for the active database if needed."""
    path = db_path or get_database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path.parent


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Open a SQLite connection with Row factory enabled."""
    path = db_path or get_database_path()
    ensure_data_dir(path)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
