# Agentic Security Review Spec

## Goal

Build an open-source Codex/Claude workflow for authorized adversarial code review that produces structured vulnerability findings with evidence, exploitability analysis, severity, and remediation guidance.

## Positioning

The project is a maintainer-first defensive security assistant. It helps reviewers reason across files and workflows where static scanners may miss business logic flaws.

## MVP scope

- Codex security-review skill.
- Claude Code security-review skill.
- JSON schemas for reports/findings.
- Deliberately vulnerable Python demo app.
- Sample Markdown and JSON reports.
- Minimal CLI that prepares review prompts.
- Tests validating schema and prompt contracts.

## Non-goals

- Live target scanning.
- Offensive exploit automation.
- Malware, persistence, credential theft, stealth, or destructive payloads.
- Claims of complete vulnerability coverage.

## Success criteria

- `pytest -q` passes.
- Sample JSON report validates against schema.
- README explains safety boundaries and quickstart.
- Skills include scope confirmation, reconnaissance, attack-surface mapping, evidence validation, and remediation guidance.
