#!/usr/bin/env python3
"""Validate that the REDNET portal stays a static read-only surface."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTAL = ROOT / "portal"
APP = PORTAL / "app.js"
DATA = PORTAL / "data.js"
INDEX = PORTAL / "index.html"
MANIFEST = PORTAL / "manifest.webmanifest"
SERVICE_WORKER = PORTAL / "sw.js"
README = PORTAL / "README.md"
GITIGNORE = ROOT / ".gitignore"


class PortalValidationError(Exception):
    pass


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise PortalValidationError(detail)


def validate_static_surface(app: str, index: str) -> None:
    forbidden_runtime_markers = [
        "fetch(",
        "XMLHttpRequest",
        "WebSocket",
        "navigator.sendBeacon",
        "localStorage",
        "sessionStorage",
        "<form",
        "type=\"submit\"",
        "type='submit'",
    ]
    combined = app + "\n" + index
    for marker in forbidden_runtime_markers:
        require(marker not in combined, f"portal contains live/browser mutation marker: {marker}")


def validate_state(data: str) -> None:
    require('mode: "только чтение"' in data, "portal state must stay read-only")
    require("scienceCoordinator:" in data, "science coordinator card is missing")
    require("metaSkills:" in data, "meta-skill toolkit card is missing")
    require("actionAllowed: true" not in data, "portal must not allow direct actions")
    require("actionAllowed: false" in data, "portal must mark actions as disabled")
    require("REDNET_MODEL_AUTH_REF" not in data, "portal must not mention auth refs")
    require("REDNET_MODEL_AUTH_REF" not in read(APP), "portal app must not mention auth refs")
    sample_runtime = read(PORTAL / "runtime" / "docker-status.sample.js")
    require("127.0.0.1:18883" not in data + sample_runtime, "portal must not expose local service ports")

    raw_allowed = re.search(r"allowed:\s*\"[^\"]*сырая нить", data, flags=re.IGNORECASE)
    require(raw_allowed is None, "raw thread must not be listed as allowed in portal modes")

    guarded_actions = ["Перезапуск агента", "Смена маршрута"]
    for title in guarded_actions:
        pattern = rf"title:\s*\"{re.escape(title)}\"[\s\S]*?state:\s*\"disabled\""
        require(re.search(pattern, data), f"dangerous action is not disabled: {title}")


def validate_runtime_boundary(app: str, readme: str, gitignore: str) -> None:
    require(
        "runtime/docker-status.local.js" in app or "runtime/docker-status.local.js" in readme,
        "portal should document optional local runtime status file explicitly",
    )
    require(
        "?runtime=local" in app or "?runtime=local" in readme,
        "local runtime status should be opt-in, not loaded by default",
    )
    require(
        'params.get("runtime") !== "local"' in app,
        "runtime loader must require exact ?runtime=local value",
    )
    require(
        "portal/runtime/docker-status.local.js" in gitignore,
        "local runtime status file must stay ignored",
    )


def validate_pwa(index: str, manifest_text: str, service_worker: str) -> None:
    require('rel="manifest"' in index, "index.html must link the PWA manifest")
    require("serviceWorker" in index + service_worker + read(APP), "portal must register a service worker")

    manifest = json.loads(manifest_text)
    require(manifest.get("display") == "standalone", "PWA manifest must use standalone display")
    require(manifest.get("start_url", "").startswith("./"), "PWA start_url must stay local")
    require(manifest.get("scope") == "./", "PWA scope must stay local to portal/")
    require(manifest.get("theme_color") == "#08111f", "PWA theme_color changed unexpectedly")
    icons = manifest.get("icons", [])
    require(any(icon.get("sizes") == "192x192" for icon in icons), "PWA manifest missing 192x192 icon")
    require(any(icon.get("sizes") == "512x512" and icon.get("purpose") == "maskable" for icon in icons), "PWA manifest missing maskable 512 icon")

    forbidden_remote = ["http://", "https://", "ws://", "wss://"]
    combined = manifest_text + "\n" + service_worker
    for marker in forbidden_remote:
        require(marker not in combined, f"PWA should not depend on remote URL: {marker}")
    require("CACHE_NAME" in service_worker and "APP_SHELL" in service_worker, "service worker should define app-shell cache")
    require("url.origin !== self.location.origin" in service_worker, "service worker must ignore cross-origin requests")
    require("shellRequest" in service_worker and "!isNavigation && !shellRequest" in service_worker, "service worker must avoid caching non-shell runtime files")
    require('caches.match("./index.html")' in service_worker, "service worker must have local offline fallback")


def main() -> int:
    try:
        app = read(APP)
        data = read(DATA)
        index = read(INDEX)
        manifest = read(MANIFEST)
        service_worker = read(SERVICE_WORKER)
        readme = read(README)
        gitignore = read(GITIGNORE)
        validate_static_surface(app, index)
        validate_state(data)
        validate_runtime_boundary(app, readme, gitignore)
        validate_pwa(index, manifest, service_worker)
    except Exception as exc:
        print(f"portal read-only validation failed: {exc}", file=sys.stderr)
        return 1
    print("OK portal read-only validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
