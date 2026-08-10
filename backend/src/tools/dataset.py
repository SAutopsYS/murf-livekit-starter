"""Lightweight dataset loader for Learning & Literacy tool data.

Responsibilities:
- locate JSON dataset files under tools/resources
- load JSON datasets from disk
- cache loaded datasets in memory
- expose the exercise dataset loader

No search, scoring, or exercise selection logic lives here.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, TypedDict

logger = logging.getLogger("tools.dataset")

RESOURCES_DIR = Path(__file__).resolve().parent / "resources"
EXERCISES_FILENAME = "exercises.json"

_dataset_cache: dict[Path, Any] = {}


class ExerciseItem(TypedDict):
    """One speaking exercise from the local dataset."""

    id: str
    topic: str
    title: str
    exercise: str


ExerciseDataset = dict[str, list[ExerciseItem]]


def resolve_dataset_path(filename: str) -> Path:
    """Return the absolute path for a dataset file under tools/resources."""
    name = filename.strip()
    if not name:
        raise ValueError("dataset filename must be non-empty")
    if Path(name).name != name:
        raise ValueError("dataset filename must not include directories")
    return RESOURCES_DIR / name


def load_dataset(filename: str, *, force_reload: bool = False) -> Any:
    """Load a JSON dataset by filename, using an in-memory cache.

    Args:
        filename: JSON file name inside tools/resources (for example exercises.json).
        force_reload: When True, bypass and refresh the cache for this file.

    Returns:
        Parsed JSON payload (dict or list, depending on the file).
    """
    path = resolve_dataset_path(filename)

    if not force_reload and path in _dataset_cache:
        logger.info("Dataset cache hit: %s", filename)
        return _dataset_cache[path]

    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")

    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    _dataset_cache[path] = payload
    logger.info("Dataset loaded: %s", filename)
    return payload


def _normalize_exercise_item(raw: object) -> ExerciseItem | None:
    if not isinstance(raw, dict):
        return None

    item_id = str(raw.get("id", "")).strip()
    topic = str(raw.get("topic", "")).strip()
    title = str(raw.get("title", "")).strip()
    exercise = str(raw.get("exercise", "")).strip()
    if not item_id or not topic or not title or not exercise:
        return None

    return {
        "id": item_id,
        "topic": topic,
        "title": title,
        "exercise": exercise,
    }


def _normalize_exercise_dataset(payload: object) -> ExerciseDataset:
    if not isinstance(payload, dict):
        raise ValueError("Exercise dataset must be a JSON object")

    dataset: ExerciseDataset = {}
    for level, items in payload.items():
        level_key = str(level).strip().lower()
        if not level_key or not isinstance(items, list):
            continue
        normalized_items: list[ExerciseItem] = []
        for item in items:
            normalized = _normalize_exercise_item(item)
            if normalized is not None:
                normalized_items.append(normalized)
        dataset[level_key] = normalized_items
    return dataset


def load_exercise_dataset(*, force_reload: bool = False) -> ExerciseDataset:
    """Load and cache the local speaking-exercise dataset.

    Returns:
        Mapping of level name -> list of exercise items.
    """
    payload = load_dataset(EXERCISES_FILENAME, force_reload=force_reload)
    # Re-normalize on every call so callers always get a typed shape.
    # Raw JSON remains cached by load_dataset.
    return _normalize_exercise_dataset(payload)


def clear_dataset_cache(filename: str | None = None) -> None:
    """Clear one cached dataset, or the entire cache when filename is None."""
    if filename is None:
        _dataset_cache.clear()
        logger.info("Dataset cache cleared")
        return

    path = resolve_dataset_path(filename)
    removed = _dataset_cache.pop(path, None)
    if removed is not None:
        logger.info("Dataset cache entry cleared: %s", filename)


def list_dataset_files() -> list[str]:
    """List JSON filenames currently present under tools/resources."""
    if not RESOURCES_DIR.is_dir():
        return []
    return sorted(path.name for path in RESOURCES_DIR.glob("*.json") if path.is_file())
