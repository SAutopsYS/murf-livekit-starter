"""SQLite repository for call analytics (separate analytics.db)."""

from __future__ import annotations

import logging
from datetime import datetime, time, timezone
from typing import Any

from analytics.database import get_connection
from analytics.models import (
    AnalyticsFilter,
    CallAnalyticsRecord,
    DashboardMetrics,
    RecentCall,
    isoformat,
    parse_datetime,
)

logger = logging.getLogger("analytics.repository")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS call_analytics (
    call_id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    channel TEXT NOT NULL,
    language TEXT NOT NULL,
    outcome TEXT,
    failure_type TEXT,
    first_response_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_call_analytics_started
    ON call_analytics(started_at DESC);
"""


class AnalyticsRepository:
    """Persist and query privacy-safe call analytics records."""

    def __init__(self) -> None:
        self.initialize()

    def initialize(self) -> bool:
        try:
            with get_connection() as conn:
                conn.executescript(SCHEMA_SQL)
                conn.commit()
            return True
        except Exception:
            logger.exception("Failed to initialize analytics database")
            return False

    def create_call(self, record: CallAnalyticsRecord) -> CallAnalyticsRecord | None:
        try:
            with get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO call_analytics (
                        call_id, started_at, ended_at, channel, language,
                        outcome, failure_type, first_response_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.call_id,
                        isoformat(record.started_at),
                        isoformat(record.ended_at),
                        record.channel,
                        record.language,
                        record.outcome,
                        record.failure_type,
                        isoformat(record.first_response_at),
                    ),
                )
                conn.commit()
            return self.get_call(record.call_id)
        except Exception:
            return None

    def get_call(self, call_id: str) -> CallAnalyticsRecord | None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM call_analytics WHERE call_id = ?",
                (call_id,),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_record(row)

    def update_outcome(
        self,
        call_id: str,
        outcome: str,
        *,
        ended_at: datetime | None = None,
        failure_type: str | None = None,
    ) -> CallAnalyticsRecord | None:
        current = self.get_call(call_id)
        if current is None:
            return None
        end = ended_at or datetime.now(timezone.utc)
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE call_analytics
                SET outcome = ?, ended_at = ?, failure_type = ?
                WHERE call_id = ?
                """,
                (outcome, isoformat(end), failure_type, call_id),
            )
            conn.commit()
        return self.get_call(call_id)

    def update_first_response(
        self,
        call_id: str,
        first_response_at: datetime,
    ) -> CallAnalyticsRecord | None:
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE call_analytics
                SET first_response_at = ?
                WHERE call_id = ? AND first_response_at IS NULL
                """,
                (isoformat(first_response_at), call_id),
            )
            conn.commit()
        return self.get_call(call_id)

    def get_total_calls(self, filters: AnalyticsFilter | None = None) -> int:
        return self._count("1=1", filters)

    def get_successful_calls(self, filters: AnalyticsFilter | None = None) -> int:
        return self._count("outcome = 'success'", filters)

    def get_failed_calls(self, filters: AnalyticsFilter | None = None) -> int:
        return self._count("outcome = 'failed'", filters)

    def get_dashboard_metrics(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> DashboardMetrics:
        return DashboardMetrics(
            total_calls=self.get_total_calls(filters),
            successful_calls=self.get_successful_calls(filters),
            failed_calls=self.get_failed_calls(filters),
        )

    def get_failure_categories(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> dict[str, int]:
        where, params = self._filter_clause(filters)
        sql = f"""
            SELECT COALESCE(failure_type, 'unknown') AS category, COUNT(*) AS cnt
            FROM call_analytics
            WHERE outcome = 'failed' AND {where}
            GROUP BY category
            ORDER BY cnt DESC, category ASC
        """
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return {str(row["category"]): int(row["cnt"]) for row in rows}

    def get_recent_calls(
        self,
        limit: int = 10,
        filters: AnalyticsFilter | None = None,
    ) -> list[RecentCall]:
        capped = max(1, min(int(limit), 50))
        where, params = self._filter_clause(filters)
        sql = f"""
            SELECT * FROM call_analytics
            WHERE {where}
            ORDER BY started_at DESC
            LIMIT ?
        """
        with get_connection() as conn:
            rows = conn.execute(sql, [*params, capped]).fetchall()
        return [self._row_to_recent(row) for row in rows]

    def get_language_breakdown(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> dict[str, int]:
        where, params = self._filter_clause(filters)
        sql = f"""
            SELECT COALESCE(NULLIF(TRIM(language), ''), 'unknown') AS lang,
                   COUNT(*) AS cnt
            FROM call_analytics
            WHERE {where}
            GROUP BY lang
            ORDER BY cnt DESC, lang ASC
        """
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return {str(row["lang"]): int(row["cnt"]) for row in rows}

    def get_channel_breakdown(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> dict[str, int]:
        where, params = self._filter_clause(filters)
        sql = f"""
            SELECT COALESCE(NULLIF(TRIM(channel), ''), 'unknown') AS ch,
                   COUNT(*) AS cnt
            FROM call_analytics
            WHERE {where}
            GROUP BY ch
            ORDER BY cnt DESC, ch ASC
        """
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return {str(row["ch"]): int(row["cnt"]) for row in rows}

    def list_records_for_performance(
        self,
        filters: AnalyticsFilter | None = None,
    ) -> list[CallAnalyticsRecord]:
        where, params = self._filter_clause(filters)
        sql = f"SELECT * FROM call_analytics WHERE {where}"
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [self._row_to_record(row) for row in rows]

    def clear_all(self) -> None:
        with get_connection() as conn:
            conn.execute("DELETE FROM call_analytics")
            conn.commit()

    def _count(self, base: str, filters: AnalyticsFilter | None) -> int:
        where, params = self._filter_clause(filters)
        sql = f"SELECT COUNT(*) AS cnt FROM call_analytics WHERE ({base}) AND ({where})"
        with get_connection() as conn:
            row = conn.execute(sql, params).fetchone()
        return int(row["cnt"]) if row else 0

    def _filter_clause(
        self,
        filters: AnalyticsFilter | None,
    ) -> tuple[str, list[Any]]:
        clauses = ["1=1"]
        params: list[Any] = []
        if filters is None:
            return " AND ".join(clauses), params

        if filters.start_date is not None:
            start = datetime.combine(filters.start_date, time.min, tzinfo=timezone.utc)
            clauses.append("started_at >= ?")
            params.append(isoformat(start))
        if filters.end_date is not None:
            end = datetime.combine(filters.end_date, time.max, tzinfo=timezone.utc)
            clauses.append("started_at <= ?")
            params.append(isoformat(end))
        if filters.channel:
            clauses.append("channel = ?")
            params.append(filters.channel)
        if filters.outcome == "success":
            clauses.append("outcome = 'success'")
        elif filters.outcome == "failed":
            clauses.append("outcome = 'failed'")
        elif filters.outcome == "incomplete":
            clauses.append("outcome IS NULL")
        return " AND ".join(clauses), params

    @staticmethod
    def _row_to_record(row: Any) -> CallAnalyticsRecord:
        return CallAnalyticsRecord(
            call_id=str(row["call_id"]),
            started_at=parse_datetime(row["started_at"]) or datetime.now(timezone.utc),
            ended_at=parse_datetime(row["ended_at"]),
            channel=str(row["channel"] or "browser"),
            language=str(row["language"] or "en-IN"),
            outcome=row["outcome"],
            failure_type=row["failure_type"],
            first_response_at=parse_datetime(row["first_response_at"]),
        )

    @staticmethod
    def _row_to_recent(row: Any) -> RecentCall:
        started = parse_datetime(row["started_at"])
        ended = parse_datetime(row["ended_at"])
        duration: int | None = None
        if started and ended and ended >= started:
            duration = int((ended - started).total_seconds())
        return RecentCall(
            call_id=str(row["call_id"]),
            started_at=isoformat(started),
            ended_at=isoformat(ended),
            duration_seconds=duration,
            channel=str(row["channel"] or "unknown"),
            outcome=row["outcome"],
            failure_type=row["failure_type"],
        )


_default_repository: AnalyticsRepository | None = None


def get_analytics_repository() -> AnalyticsRepository:
    global _default_repository
    if _default_repository is None:
        _default_repository = AnalyticsRepository()
    return _default_repository


def reset_analytics_repository() -> AnalyticsRepository:
    global _default_repository
    _default_repository = AnalyticsRepository()
    return _default_repository
