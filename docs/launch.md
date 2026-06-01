# Launch Plan

## Positioning

Agentic Security Review is a defensive Codex/Claude workflow for authorized adversarial code review. It helps maintainers catch high-impact bugs that require cross-file reasoning: broken access control, auth/session mistakes, unsafe data flows, business-logic flaws, and risky agent/tool permissions.

Avoid saying: bad actor, exploit any repo, autonomous hacking, weaponized exploit generation.

Use: authorized adversarial review, defensive security, maintainer-first reports, static/local review, structured vulnerability findings.

## X launch thread

### Post 1

I'm open-sourcing `agentic-security-review`: a defensive Codex/Claude workflow for authorized adversarial code review.

It reviews a repo like a security engineer would and outputs maintainer-friendly vulnerability reports:

- evidence
- severity + confidence
- exploitability reasoning
- CWE/OWASP mapping
- remediation steps
- tests to add

Built for OSS maintainers. Static/local review by default. No live exploitation.

Repo: https://github.com/ki2001/agentic-security-review

### Post 2

Why build this?

Static scanners catch lots of known patterns. They often miss business-logic bugs that require cross-file reasoning:

- frontend-only auth checks
- IDOR / tenant isolation mistakes
- webhook paths that bypass normal checks
- unsafe file/shell/template/data-flow paths
- agent tools with excessive permissions

### Post 3

The repo includes:

- Codex security-review skill
- Claude Code security-review skill
- JSON report schema
- deliberately vulnerable Python demo app
- sample Markdown + JSON reports
- tiny CLI for prompt generation and report validation

### Post 4

Example finding from the demo app:

`/invoices/<invoice_id>` trusts `org_id` from the query string instead of deriving org scope from the authenticated session.

That turns into a maintainer-friendly report with impact, evidence, CWE-639, remediation, and tests to add.

### Post 5

Looking for OSS maintainers who want to try this on their own repos and give feedback.

Goal: make AI-assisted security review safer, more repeatable, and more useful — not replace professional AppSec.

## Short single-post version

I’m open-sourcing `agentic-security-review`, a defensive Codex/Claude workflow for authorized adversarial code review.

It turns repo review into structured maintainer-friendly findings: evidence, severity, exploitability, CWE/OWASP mapping, remediation, and tests to add.

Static/local by default. No live exploitation.

https://github.com/ki2001/agentic-security-review
