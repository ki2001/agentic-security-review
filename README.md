# Agentic Security Review

**Authorized adversarial code review workflows for open-source maintainers using Codex and Claude Code.**

Agentic Security Review helps maintainers run static, defensive AI security reviews over local or GitHub codebases and produce structured vulnerability reports with evidence, severity, confidence, exploitability analysis, CWE/OWASP mapping, remediation guidance, and suggested tests.

It is designed to complement static scanners by focusing on cross-file reasoning, business-logic flaws, authorization boundaries, unsafe data flows, and LLM/agent tooling risks.

## Why this exists

Static scanners are excellent at known patterns. They are weaker at questions like:

- Can a low-privileged user reach another tenant's data by changing an identifier?
- Is authorization enforced server-side or only in the frontend?
- Does a webhook, background job, or retry path bypass normal checks?
- Can user input cross a trust boundary into a file, shell, template, SSRF, or deserialization sink?
- Are AI agents/tools configured with broader filesystem or command permissions than intended?

This project packages a repeatable agent workflow so reviews are safer, more consistent, and more useful to maintainers than one-off prompts.

## What it does

- Reviews local repos or GitHub repos in an authorized static-review mode.
- Provides reusable Codex and Claude Code security-review skills.
- Generates maintainer-friendly reports with evidence and remediation guidance.
- Defines JSON schemas for normalized findings and reports.
- Includes a deliberately vulnerable demo app and sample reports.
- Provides CLIs for prompt generation, schema validation, SARIF export, optional scanner context, and benchmark scoring.
- Supports single-agent, multi-agent, and patch-review modes.
- Includes a GitHub Actions workflow that prepares PR/diff review prompts and exports sample SARIF artifacts.

## What it is not

- Not a live-target scanner.
- Not an exploit framework.
- Not a malware, persistence, or credential-theft tool.
- Not a guarantee that code is secure.
- Not a replacement for professional security review.

By default, the workflow is static/local only and instructs agents: **Do not perform live exploitation.**

## Quickstart

```bash
git clone https://github.com/ki2001/agentic-security-review.git
cd agentic-security-review
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest -q
```

Prepare a Codex review prompt:

```bash
python scripts/run_review.py examples/vulnerable-python-api --agent codex --authorized > /tmp/asr-codex-prompt.md
codex exec "$(cat /tmp/asr-codex-prompt.md)"
```

Prepare a Claude Code review prompt:

```bash
python scripts/run_review.py examples/vulnerable-python-api --agent claude --authorized > /tmp/asr-claude-prompt.md
claude -p "$(cat /tmp/asr-claude-prompt.md)" --allowedTools 'Read,Bash' --max-turns 10
```

Validate a JSON report:

```bash
python scripts/validate_report.py examples/sample-reports/vulnerable-python-api-report.json
```

Export SARIF for GitHub code scanning or downstream tooling:

```bash
python scripts/export_sarif.py examples/sample-reports/vulnerable-python-api-report.json --output /tmp/asr.sarif
```

Run multi-agent or patch-review prompt preparation:

```bash
python scripts/run_review.py examples/vulnerable-python-api --agent codex --authorized --mode multi-agent
python scripts/run_review.py . --agent codex --authorized --mode patch-review --patch patch.diff
```

Collect optional local scanner context without requiring scanner installs:

```bash
python scripts/collect_scanner_context.py . > /tmp/asr-scanner-context.json
```

Score a report against the demo benchmark manifest:

```bash
python scripts/benchmark_reports.py benchmarks/vulnerable-python-api.json examples/sample-reports/vulnerable-python-api-report.json
```

## Example finding

```text
ASR-001: User-controlled org_id allows cross-tenant invoice access
Severity: high
Confidence: high
Category: broken_access_control
CWE: CWE-639
OWASP: A01:2021-Broken Access Control

The /invoices/<invoice_id> route reads org_id from the query string instead of deriving organization scope from the authenticated user/session. A user who can guess an invoice ID can request it with another organization's ID.

Recommended fix: derive organization scope from trusted session/user claims and enforce it server-side in the invoice lookup.
```

Full examples:

- `examples/vulnerable-python-api/`
- `examples/sample-reports/vulnerable-python-api-report.md`
- `examples/sample-reports/vulnerable-python-api-report.json`

## Skills

- `skills/codex/security-reviewer.md` — Codex-oriented authorized adversarial review workflow.
- `skills/claude/security-reviewer.md` — Claude Code-oriented authorized adversarial review workflow.

Both skills include:

1. scope confirmation;
2. safety boundary;
3. repository reconnaissance;
4. attack-surface mapping;
5. evidence validation;
6. Markdown + JSON report format;
7. remediation and suggested tests.

## Report schema

Reports are normalized around:

- `tool`
- `target`
- `authorized`
- `mode`
- `summary`
- `findings[]`

Each finding includes:

- `id`, `title`, `severity`, `confidence`, `category`
- `cwe`, `owasp`
- `affected_files`
- `summary`, `impact`
- `exploitability`
- `evidence`
- `recommended_fix`
- `suggested_tests`

See `schemas/` and `docs/report-schema.md`.

## Safety policy

Use only on code you own or are authorized to review. Default mode is static/local review. Do not use this project to attack deployed third-party systems. See `docs/safety-policy.md` and `SECURITY.md`.

## Roadmap status

Completed roadmap items:

- SARIF export for GitHub code scanning: `scripts/export_sarif.py`.
- GitHub Action for PR/diff reviews: `.github/workflows/agentic-security-review.yml`.
- Multi-agent review mode: `--mode multi-agent` with recon mapper, vulnerability analyst, and remediation reviewer roles.
- Optional scanner integrations: `scripts/collect_scanner_context.py` detects Semgrep, Bandit, npm audit, pip-audit, and CodeQL availability for authorized local use.
- Benchmarks over deliberately vulnerable demo apps: `benchmarks/vulnerable-python-api.json` plus `scripts/benchmark_reports.py`.
- Patch-review mode for verifying remediations and PR diffs: `--mode patch-review --patch <diff>`.

## License

MIT
