# Agentic Security Review

Authorized adversarial code review workflows for open-source maintainers using Codex and Claude Code.

## What it does

Agentic Security Review helps you run a static, defensive security review of a local or GitHub codebase and produce maintainer-friendly vulnerability reports with:

- evidence and affected files;
- severity and confidence;
- CWE/OWASP mapping;
- exploitability reasoning;
- remediation guidance;
- suggested tests.

It is designed to complement static scanners by focusing on cross-file reasoning, business logic flaws, auth boundaries, and unsafe data flows.

## What it is not

- Not a live-target scanner.
- Not an exploitation framework.
- Not a guarantee that code is secure.
- Not a replacement for professional security review.

By default, the workflow is static/local only and instructs agents: **Do not perform live exploitation.**

## Quickstart

```bash
git clone https://github.com/YOUR_USER/agentic-security-review.git
cd agentic-security-review
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest -q
```

Prepare a Codex review prompt:

```bash
python scripts/run_review.py examples/vulnerable-python-api --agent codex --authorized
```

Prepare a Claude Code review prompt:

```bash
python scripts/run_review.py examples/vulnerable-python-api --agent claude --authorized
```

## Skills

- `skills/codex/security-reviewer.md` — Codex-oriented security review prompt.
- `skills/claude/security-reviewer.md` — Claude Code-oriented security review prompt.

## Example

See:

- `examples/vulnerable-python-api/` for a deliberately vulnerable local demo app.
- `examples/sample-reports/vulnerable-python-api-report.md` for expected report style.
- `examples/sample-reports/vulnerable-python-api-report.json` for structured output.

## Safety

Use only on code you own or are authorized to review. See `docs/safety-policy.md` and `SECURITY.md`.

## Roadmap

- SARIF export.
- GitHub Action.
- PR/diff review mode.
- Multi-agent review mode.
- Optional scanner integrations: Semgrep, Bandit, npm audit, pip-audit, CodeQL.
