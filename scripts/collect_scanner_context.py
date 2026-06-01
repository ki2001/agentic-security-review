#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

TOOLS = [
    ("semgrep", "semgrep", "Semgrep static analysis"),
    ("bandit", "bandit", "Bandit Python security checks"),
    ("npm-audit", "npm", "npm audit for Node dependencies"),
    ("pip-audit", "pip-audit", "Python dependency audit"),
    ("codeql", "codeql", "CodeQL database analysis"),
]


def detect_tools() -> list[dict]:
    detected = []
    for name, command, description in TOOLS:
        path = shutil.which(command)
        detected.append({
            "name": name,
            "command": command,
            "available": path is not None,
            "path": path,
            "description": description,
        })
    return detected


def build_context(target: str) -> dict:
    path = Path(target).expanduser().resolve()
    manifests = []
    for pattern in ("requirements.txt", "pyproject.toml", "package.json", "package-lock.json", "go.mod"):
        manifests.extend(str(p.relative_to(path)) for p in path.rglob(pattern) if p.is_file()) if path.exists() and path.is_dir() else None
    return {
        "target": str(path),
        "note": "Scanner integrations are optional context only. Run tools locally/with authorization; do not scan third-party services.",
        "tools": detect_tools(),
        "manifests": sorted(set(manifests)),
        "suggested_commands": [
            "semgrep scan --config auto <target>",
            "bandit -r <target>",
            "pip-audit -r requirements.txt",
            "npm audit --json",
            "codeql database analyze <database> --format=sarif-latest",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect optional local scanner context for an authorized security review")
    parser.add_argument("target", help="Local repository path")
    args = parser.parse_args()
    print(json.dumps(build_context(args.target), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
