"""CLI bridge for the Next.js analytics dashboard API.

Usage:
  python -m analytics.cli summary [--preset ...] [--channel ...] [--outcome ...]
  python -m analytics.cli report  [...]
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from analytics.models import AnalyticsReport
from analytics.service import AnalyticsService, get_analytics_service


def _emit(payload: Any) -> int:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.write("\n")
    return 0 if not (isinstance(payload, dict) and payload.get("error")) else 1


def _build_filters(args: argparse.Namespace, service: AnalyticsService):
    return service.build_filter(
        preset=args.preset,
        start_date=args.start_date,
        end_date=args.end_date,
        channel=args.channel,
        outcome=args.outcome,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="analytics.cli")
    parser.add_argument(
        "command",
        choices=("summary", "report", "metrics"),
    )
    parser.add_argument("--preset", default="all")
    parser.add_argument("--start-date", default=None)
    parser.add_argument("--end-date", default=None)
    parser.add_argument("--channel", default="all")
    parser.add_argument("--outcome", default="all")
    args = parser.parse_args(argv)

    service = get_analytics_service()
    filters = _build_filters(args, service)
    if isinstance(filters, dict) and filters.get("error"):
        return _emit(filters)

    if args.command == "metrics":
        metrics = service.get_dashboard_metrics(filters)
        if isinstance(metrics, dict):
            return _emit(metrics)
        return _emit(metrics.to_dict())

    if args.command == "summary":
        summary = service.get_filtered_summary(filters)
        if isinstance(summary, dict):
            return _emit(summary)
        return _emit(summary.to_dict())

    report = service.generate_report(filters)
    if isinstance(report, dict):
        return _emit(report)
    assert isinstance(report, AnalyticsReport)
    return _emit(report.to_dict())


if __name__ == "__main__":
    raise SystemExit(main())
