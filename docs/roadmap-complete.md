# Completed Roadmap Features

The initial public roadmap has been implemented as safe, local-first functionality.

## SARIF export

`scripts/export_sarif.py` converts Agentic Security Review JSON reports into SARIF 2.1.0 for GitHub code scanning and other SARIF consumers.

```bash
python scripts/export_sarif.py examples/sample-reports/vulnerable-python-api-report.json --output sample.sarif
```

## GitHub Action for PR/diff reviews

`.github/workflows/agentic-security-review.yml` runs on pull requests and workflow dispatch. It prepares a patch-aware review prompt artifact and validates/exports the sample report as SARIF.

The workflow is intentionally safe by default: it prepares review context and artifacts; it does not run live exploitation or scan external services.

## Multi-agent review mode

`--mode multi-agent` adds three review roles to the generated prompt:

1. Recon mapper — frameworks, entry points, trust boundaries, assets, and attack surface.
2. Vulnerability analyst — likely flaws, evidence validation, severity, and confidence.
3. Remediation reviewer — safe fixes, regression tests, and false-positive challenge.

```bash
python scripts/run_review.py examples/vulnerable-python-api --authorized --mode multi-agent
```

## Optional scanner integrations

`scripts/collect_scanner_context.py` detects local availability of Semgrep, Bandit, npm audit, pip-audit, and CodeQL. The output can be attached to a Codex/Claude review prompt as optional context.

```bash
python scripts/collect_scanner_context.py . > scanner-context.json
python scripts/run_review.py . --authorized --scanner-context scanner-context.json
```

## Benchmarks over demo apps

`benchmarks/vulnerable-python-api.json` declares expected vulnerability classes for the deliberately vulnerable Flask app. `scripts/benchmark_reports.py` scores report coverage against that manifest.

```bash
python scripts/benchmark_reports.py benchmarks/vulnerable-python-api.json examples/sample-reports/vulnerable-python-api-report.json
```

## Patch-review mode

`--mode patch-review --patch <diff>` focuses the generated prompt on changed lines, directly relevant surrounding code, incomplete remediations, and regression tests.

```bash
git diff --unified=40 main...HEAD > patch.diff
python scripts/run_review.py . --authorized --mode patch-review --patch patch.diff
```
