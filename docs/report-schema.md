# Report Schema

Reports are JSON objects with:

- `tool`: project/tool name.
- `target`: reviewed codebase.
- `authorized`: boolean authorization assertion.
- `mode`: review mode, e.g. `static`.
- `summary`: high-level result.
- `findings`: list of vulnerability findings.

Findings include severity, confidence, category, CWE/OWASP mapping, affected files, evidence, impact, exploitability, remediation, and suggested tests.
