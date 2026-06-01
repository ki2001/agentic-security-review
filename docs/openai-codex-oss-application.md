# OpenAI Codex for OSS Application Draft

## Project

`agentic-security-review`

## Short description

Agentic Security Review is an open-source defensive security-review workflow for Codex. It helps maintainers perform authorized adversarial code review on repositories and receive structured vulnerability reports with evidence, severity, exploitability reasoning, CWE/OWASP mapping, remediation guidance, and suggested tests.

## Longer description

I am building `agentic-security-review`, an open-source project that packages reusable Codex and Claude Code skills for authorized static security review of local and GitHub repositories.

The project demonstrates a high-value Codex workflow: multi-file code understanding, threat modeling, business-logic vulnerability discovery, and secure remediation guidance. It focuses on vulnerabilities that traditional static scanners often miss, such as broken access control, tenant isolation issues, auth/session mistakes, unsafe data flows, webhook bypasses, and risky agent/tool permissions.

The project is safety-conscious by design. It is static/local review by default, does not perform live exploitation, and clearly requires authorization. Outputs are maintainer-friendly and structured as Markdown and JSON, with severity, confidence, evidence, exploitability reasoning, CWE/OWASP mapping, recommended fixes, and tests to add.

The MVP includes reusable skills, report schemas, a deliberately vulnerable demo app, sample reports, a small CLI for prompt generation/report validation, and tests.

## How Codex will be used

I plan to use Codex Pro to:

- improve the Codex security-review skill;
- dogfood the review workflow on open-source repositories;
- build SARIF export and GitHub Action integration;
- create more deliberately vulnerable demo apps and benchmark reports;
- improve remediation guidance and security-test generation;
- support maintainers who want defensive reviews of their own OSS repos.

## Why this is useful to OSS

Many open-source maintainers lack dedicated AppSec support. This project gives maintainers a repeatable AI-assisted workflow for finding and explaining security issues in a way that is actionable, safe, and structured.

It complements existing scanners rather than replacing them, with emphasis on cross-file reasoning and business-logic vulnerabilities.

## Safety framing

The project explicitly avoids live exploitation and offensive automation. It is intended for code owners, maintainers, and authorized reviewers. Default behavior is static/local review only, with safe reproduction notes and remediation guidance.

## Repository

https://github.com/ki2001/agentic-security-review
