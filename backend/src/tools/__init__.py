"""External Learning & Literacy tools (Day 5)."""

from tools.chaining import (
    LEVEL_FALLBACK_QUESTION,
    resolve_exercise_level,
    should_ask_for_level,
)
from tools.dataset import (
    EXERCISES_FILENAME,
    ExerciseDataset,
    ExerciseItem,
    clear_dataset_cache,
    list_dataset_files,
    load_dataset,
    load_exercise_dataset,
    resolve_dataset_path,
)
from tools.exercise_tool import (
    ExerciseError,
    ExerciseResult,
    filter_items_by_topic,
    get_local_exercise,
    normalize_level,
    normalize_topic,
)
from tools.exercise_tool import (
    get_next_exercise as lookup_next_exercise,
)
from tools.livekit_tools import (
    LEARNING_TOOLS,
    get_next_exercise,
    recommend_next_practice,
    score_spoken_answer,
)
from tools.manager import ToolManager, get_tool_manager
from tools.metrics import get_tool_metrics, reset_tool_metrics
from tools.provider import (
    ExerciseConfig,
    ExerciseProvider,
    build_exercise_provider,
    clear_exercise_config_cache,
    get_exercise_config,
    validate_exercise_payload,
)
from tools.provider_health import (
    ProviderHealth,
    clear_provider_health_config_cache,
    get_provider_health,
    get_provider_health_config,
    reset_provider_health,
)
from tools.recommendation import (
    RecommendationError,
    RecommendationResult,
)
from tools.recommendation import (
    recommend_next_practice as build_recommendation,
)
from tools.registry import (
    ToolMetadata,
    ToolRegistry,
    get_tool,
    get_tool_registry,
    list_capabilities,
    list_categories,
    list_tools,
)
from tools.request_cache import (
    RequestCache,
    clear_request_cache_config_cache,
    get_request_cache,
    get_request_cache_config,
    reset_request_cache,
)
from tools.score_tool import (
    ScoreError,
    ScoreMetrics,
    ScoreResult,
    compute_score,
    count_sentences,
    count_unique_words,
    count_words,
    generate_feedback,
)
from tools.score_tool import (
    score_spoken_answer as score_answer,
)
from tools.session_cache import (
    SessionExerciseCache,
    get_session_exercise_cache,
    reset_session_exercise_cache,
)
from tools.validator import ExerciseValidator, get_exercise_validator

TOOLS = LEARNING_TOOLS

__all__ = [
    "EXERCISES_FILENAME",
    "LEARNING_TOOLS",
    "LEVEL_FALLBACK_QUESTION",
    "TOOLS",
    "ExerciseConfig",
    "ExerciseDataset",
    "ExerciseError",
    "ExerciseItem",
    "ExerciseProvider",
    "ExerciseResult",
    "ExerciseValidator",
    "ProviderHealth",
    "RecommendationError",
    "RecommendationResult",
    "RequestCache",
    "ScoreError",
    "ScoreMetrics",
    "ScoreResult",
    "SessionExerciseCache",
    "ToolManager",
    "ToolMetadata",
    "ToolRegistry",
    "build_exercise_provider",
    "build_recommendation",
    "clear_dataset_cache",
    "clear_exercise_config_cache",
    "clear_provider_health_config_cache",
    "clear_request_cache_config_cache",
    "compute_score",
    "count_sentences",
    "count_unique_words",
    "count_words",
    "filter_items_by_topic",
    "generate_feedback",
    "get_exercise_config",
    "get_exercise_validator",
    "get_local_exercise",
    "get_next_exercise",
    "get_provider_health",
    "get_provider_health_config",
    "get_request_cache",
    "get_request_cache_config",
    "get_session_exercise_cache",
    "get_tool",
    "get_tool_manager",
    "get_tool_metrics",
    "get_tool_registry",
    "list_capabilities",
    "list_categories",
    "list_dataset_files",
    "list_tools",
    "load_dataset",
    "load_exercise_dataset",
    "lookup_next_exercise",
    "normalize_level",
    "normalize_topic",
    "recommend_next_practice",
    "reset_provider_health",
    "reset_request_cache",
    "reset_session_exercise_cache",
    "reset_tool_metrics",
    "resolve_dataset_path",
    "resolve_exercise_level",
    "score_answer",
    "score_spoken_answer",
    "should_ask_for_level",
    "validate_exercise_payload",
]
