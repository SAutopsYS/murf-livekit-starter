"""SQLite helpers for the analytics database (separate from memory.db)."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = BACKEND_ROOT / "data"
DEFAULT_DATABASE_PATH = DATA_DIR / "analytics.db"

_database_path_override: Path | None = None


def get_database_path() -> Path:
    return _database_path_override or DEFAULT_DATABASE_PATH


def set_database_path(path: Path | None) -> None:
    global _database_path_override
    _database_path_override = path


@contextmanager
def temporary_database(path: Path) -> Iterator[Path]:
    previous = _database_path_override
    set_database_path(path)
    try:
        yield path
    finally:
        set_database_path(previous)


def ensure_data_dir(db_path: Path | None = None) -> Path:
    path = db_path or get_database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path.parent


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or get_database_path()
    ensure_data_dir(path)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection
