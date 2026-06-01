#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Target:
    kind: str
    value: str
    path: Path | None = None


def resolve_target(value: str) -> Target:
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return Target(kind="github" if "github.com" in parsed.netloc else "url", value=value)

    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Target path does not exist: {path}")
    return Target(kind="local", value=str(path), path=path)


def load_skill(agent: str) -> str:
    if agent not in {"codex", "claude"}:
        raise ValueError("agent must be 'codex' or 'claude'")
    return (ROOT / "skills" / agent / "security-reviewer.md").read_text()


def build_review_prompt(*, target: Target, agent: str, authorized: bool, threat_model: str | None = None) -> str:
    skill = load_skill(agent)
    authorization = "authorized" if authorized else "NOT explicitly authorized"
    threat = (
        f"\nThreat model file/content: {threat_model}\n"
        if threat_model
        else "\nNo separate threat model supplied. Infer a basic threat model from the code.\n"
    )
    return f"""{skill}

---

## Review request

Perform an authorized static security review of this target.

Target kind: {target.kind}
Target: {target.value}
Authorization assertion: {authorization}

Do not perform live exploitation. Do not scan external services. Keep any reproduction guidance local and safe.

Return both Markdown and JSON using the Agentic Security Review schema. Mention Markdown and JSON clearly in the final output.
{threat}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare an Agentic Security Review prompt")
    parser.add_argument("target", help="Local path or GitHub URL to review")
    parser.add_argument("--agent", choices=["codex", "claude"], default="codex")
    parser.add_argument("--authorized", action="store_true", help="Assert you are authorized to review the target")
    parser.add_argument("--threat-model", help="Optional threat model path or short text")
    args = parser.parse_args()

    target = resolve_target(args.target)
    print(build_review_prompt(target=target, agent=args.agent, authorized=args.authorized, threat_model=args.threat_model))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
