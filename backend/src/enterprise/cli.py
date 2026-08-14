"""CLI bridge for the Next.js enterprise control center."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from typing import Any

from enterprise.intelligence import LearningReportService, build_simple_pdf
from enterprise.orchestrator import get_orchestrator
from enterprise.platform import ControlCenterService, TeacherConsoleService
from enterprise.privacy import sanitize_payload


def _emit(payload: Any) -> int:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.write("\n")
    return 0 if not (isinstance(payload, dict) and payload.get("error")) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="enterprise.cli")
    parser.add_argument(
        "command",
        choices=("snapshot", "decide", "export", "search"),
    )
    parser.add_argument("--text", default="")
    parser.add_argument("--format", default="json", choices=("json", "pdf"))
    parser.add_argument(
        "--kind",
        default="report",
        choices=("report", "teacher", "health", "control"),
    )
    parser.add_argument("--query", default="")
    args = parser.parse_args(argv)

    if args.command == "decide":
        decision = get_orchestrator().decide(args.text)
        return _emit(sanitize_payload(decision))

    if args.command == "search":
        snapshot = ControlCenterService().snapshot()
        query = args.query.lower().strip()
        hits: list[dict[str, str]] = []
        if query:
            for agent in snapshot["agents"]:
                name = str(agent.get("display_name") or "")
                if query in name.lower() or query in str(agent.get("id")):
                    hits.append({"group": "agents", "label": name})
            for cell in snapshot["heatmap"]["cells"]:
                if query in cell["topic"]:
                    hits.append({"group": "topics", "label": cell["topic"]})
        return _emit({"results": hits, "query_len": len(query)})

    if args.command == "export":
        if args.kind == "teacher":
            payload = TeacherConsoleService().build()
        elif args.kind == "health":
            payload = ControlCenterService().snapshot()["ops"]
        elif args.kind == "control":
            payload = ControlCenterService().snapshot()
        else:
            payload = LearningReportService().export_json()
        if args.format == "pdf":
            lines = [f"{key}: {payload.get(key)}" for key in list(payload)[:12]]
            pdf = build_simple_pdf("Enterprise Export", [str(line) for line in lines])
            return _emit(
                {
                    "format": "pdf",
                    "filename": f"{args.kind}.pdf",
                    "content_base64": base64.b64encode(pdf).decode("ascii"),
                }
            )
        return _emit({"format": "json", "payload": payload})

    return _emit(ControlCenterService().snapshot())


if __name__ == "__main__":
    raise SystemExit(main())
