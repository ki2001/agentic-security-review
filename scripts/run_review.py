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


@dataclass(frozen=True)
class ReviewOptions:
    mode: str = "single-agent"
    patch: str | None = None
    scanner_context: str | None = None


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


def _read_inline_or_file(value: str | None) -> str | None:
    if not value:
        return None
    candidate = Path(value).expanduser()
    if candidate.exists():
        return candidate.read_text()
    return value


def _mode_instructions(options: ReviewOptions) -> str:
    if options.mode == "single-agent":
        return "Single-agent review mode: perform the full review workflow yourself."

    if options.mode == "multi-agent":
        return """Multi-agent review mode:
1. Recon mapper: inventory frameworks, entry points, trust boundaries, sensitive assets, and attack surface.
2. Vulnerability analyst: reason from the recon map to likely flaws, validate evidence, and assign severity/confidence.
3. Remediation reviewer: propose safe fixes and regression tests, then challenge each finding for false positives.
Return one consolidated maintainer-friendly report; do not invent separate agents or claim parallel execution unless actually performed."""

    if options.mode == "patch-review":
        patch_text = _read_inline_or_file(options.patch)
        patch_section = patch_text or "No patch diff supplied. Use repository diff context if available."
        return f"""Patch-review mode:
Focus on changed lines and changed data/control flow. Identify newly introduced vulnerabilities, incomplete fixes, and regression tests that should accompany the patch. Keep review bounded to the diff plus directly relevant surrounding code.

Patch/diff context:
```diff
{patch_section}
```"""

    raise ValueError("mode must be 'single-agent', 'multi-agent', or 'patch-review'")


def build_review_prompt(
    *,
    target: Target,
    agent: str,
    authorized: bool,
    threat_model: str | None = None,
    options: ReviewOptions | None = None,
) -> str:
    skill = load_skill(agent)
    options = options or ReviewOptions()
    authorization = "authorized" if authorized else "NOT explicitly authorized"
    threat = (
        f"\nThreat model file/content: {_read_inline_or_file(threat_model)}\n"
        if threat_model
        else "\nNo separate threat model supplied. Infer a basic threat model from the code.\n"
    )
    scanner_context = (
        f"\nScanner context:\n```json\n{_read_inline_or_file(options.scanner_context)}\n```\n"
        if options.scanner_context
        else ""
    )
    mode = _mode_instructions(options)
    return f"""{skill}

---

## Review request

Perform an authorized static security review of this target.

Target kind: {target.kind}
Target: {target.value}
Authorization assertion: {authorization}
Review mode: {options.mode}

Do not perform live exploitation. Do not scan external services. Keep any reproduction guidance local and safe.

Return both Markdown and JSON using the Agentic Security Review schema. Mention Markdown and JSON clearly in the final output.
{threat}
{scanner_context}
## Mode-specific instructions

{mode}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare an Agentic Security Review prompt")
    parser.add_argument("target", help="Local path or GitHub URL to review")
    parser.add_argument("--agent", choices=["codex", "claude"], default="codex")
    parser.add_argument("--authorized", action="store_true", help="Assert you are authorized to review the target")
    parser.add_argument("--threat-model", help="Optional threat model path or short text")
    parser.add_argument("--mode", choices=["single-agent", "multi-agent", "patch-review"], default="single-agent")
    parser.add_argument("--patch", help="Patch/diff file path or inline diff text for patch-review mode")
    parser.add_argument("--scanner-context", help="Optional scanner context JSON path or inline JSON from collect_scanner_context.py")
    args = parser.parse_args()

    target = resolve_target(args.target)
    options = ReviewOptions(mode=args.mode, patch=args.patch, scanner_context=args.scanner_context)
    print(build_review_prompt(target=target, agent=args.agent, authorized=args.authorized, threat_model=args.threat_model, options=options))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
