#!/usr/bin/env python3
"""Read-only REDNET Science Coordinator prototype.

The service exposes a tiny status API for the future laboratory coordinator.
It does not execute commands, mutate files, call model providers, or read
private agent memory. It is intentionally boring at runtime.
"""

from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parents[1]
MANIFEST_PATH = BASE_DIR / "manifest.json"
EXAMPLE_LEDGER_PATH = BASE_DIR / "examples" / "task-ledger.example.jsonl"

SAFE_ENV_NAMES = {
    "REDNET_AGENT_MODE",
    "REDNET_MODEL_BASE_URL",
    "REDNET_MODEL_NAME",
    "REDNET_MEMORY_NAMESPACE",
    "REDNET_PORTAL_LABEL",
    "REDNET_LIVE_COMMANDS",
    "REDNET_SECRET_LOGGING",
    "REDNET_ALLOWED_FLOWS",
    "REDNET_REQUIRED_ARTIFACT",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected object in {path}")
    return data


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            item = json.loads(stripped)
            if not isinstance(item, dict):
                raise ValueError(f"Expected object at {path}:{line_number}")
            rows.append(item)
    return rows


def safe_environment(environ: dict[str, str] | None = None) -> dict[str, Any]:
    source = environ or os.environ
    safe: dict[str, Any] = {}
    for name in sorted(SAFE_ENV_NAMES):
        value = source.get(name)
        if value is not None:
            safe[name] = value
    safe["REDNET_MODEL_AUTH_REF_PRESENT"] = bool(source.get("REDNET_MODEL_AUTH_REF"))
    return safe


def normalize_mode(
    manifest: dict[str, Any],
    environ: dict[str, str] | None = None,
) -> tuple[str, str, bool]:
    """Return safe mode, requested mode and invalid-mode flag."""

    source = environ or os.environ
    requested = source.get("REDNET_AGENT_MODE") or str(
        manifest.get("default_mode") or "observe"
    )
    allowed_modes = manifest.get("allowed_modes", [])
    if not isinstance(allowed_modes, list):
        allowed_modes = []
    default_mode = str(manifest.get("default_mode") or "observe")
    fallback = default_mode if default_mode in allowed_modes else "observe"
    if requested in allowed_modes:
        return requested, requested, False
    return fallback, requested, True


def build_status(
    manifest: dict[str, Any],
    tasks: list[dict[str, Any]],
    environ: dict[str, str] | None = None,
) -> dict[str, Any]:
    mode, requested_mode, invalid_mode = normalize_mode(manifest, environ)
    guards = manifest.get("guards", {})
    flows = manifest.get("flows", [])
    required_artifacts = manifest.get("required_artifacts", [])
    return {
        "ok": True,
        "service": manifest.get("id", "rednet-science-coordinator"),
        "version": manifest.get("version"),
        "status": manifest.get("status"),
        "mode": mode,
        "requested_mode": requested_mode,
        "invalid_mode": invalid_mode,
        "allowed_modes": manifest.get("allowed_modes", []),
        "forbidden_modes_by_default": manifest.get("forbidden_modes_by_default", []),
        "live_commands": bool(guards.get("live_commands")),
        "network_changes": bool(guards.get("network_changes")),
        "docker_control": bool(guards.get("docker_control")),
        "artifact_required": bool(guards.get("artifact_required")),
        "flow_count": len(flows) if isinstance(flows, list) else 0,
        "required_artifact_count": len(required_artifacts)
        if isinstance(required_artifacts, list)
        else 0,
        "example_task_count": len(tasks),
        "environment": safe_environment(environ),
    }


def response_for_path(path: str) -> tuple[int, dict[str, Any]]:
    manifest = load_json(MANIFEST_PATH)
    tasks = load_jsonl(EXAMPLE_LEDGER_PATH)
    status = build_status(manifest, tasks)
    if path in {"/", "/health"}:
        return 200, {
            "ok": status["ok"],
            "service": status["service"],
            "mode": status["mode"],
            "live_commands": status["live_commands"],
        }
    if path == "/status":
        return 200, status
    if path == "/flows":
        return 200, {
            "ok": True,
            "flows": manifest.get("flows", []),
            "required_artifacts": manifest.get("required_artifacts", []),
        }
    if path == "/tasks":
        return 200, {"ok": True, "tasks": tasks}
    return 404, {"ok": False, "error": "not_found"}


class Handler(BaseHTTPRequestHandler):
    server_version = "REDNETScienceCoordinator/0.2"

    def do_GET(self) -> None:  # noqa: N802 - stdlib hook name
        parsed = urlparse(self.path)
        code, payload = response_for_path(parsed.path)
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802 - stdlib hook name
        self._deny_mutation()

    def do_PUT(self) -> None:  # noqa: N802 - stdlib hook name
        self._deny_mutation()

    def do_DELETE(self) -> None:  # noqa: N802 - stdlib hook name
        self._deny_mutation()

    def _deny_mutation(self) -> None:
        body = json.dumps(
            {"ok": False, "error": "read_only_service"},
            ensure_ascii=False,
            indent=2,
        ).encode("utf-8")
        self.send_response(405)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Allow", "GET")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="REDNET Science Coordinator")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=18884, type=int)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(
        json.dumps(
            {
                "service": "rednet-science-coordinator",
                "host": args.host,
                "port": args.port,
                "mode": os.environ.get("REDNET_AGENT_MODE", "observe"),
                "read_only": True,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
