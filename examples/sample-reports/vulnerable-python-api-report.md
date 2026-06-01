# Agentic Security Review Report: Vulnerable Python API

## Summary

The demo app contains multiple intentionally vulnerable patterns. The highest-impact issue is broken access control in invoice retrieval, where the API trusts a request parameter for organization scope.

## Findings

### ASR-001: User-controlled org_id allows cross-tenant invoice access

- Severity: high
- Confidence: high
- Category: broken_access_control
- CWE: CWE-639
- OWASP: A01:2021-Broken Access Control
- Affected file: `examples/vulnerable-python-api/app.py`

The `/invoices/<invoice_id>` route reads `org_id` from the query string instead of deriving organization scope from the authenticated user/session. A user who can guess an invoice ID can request it with the victim organization's ID.

Remediation: derive organization scope from `current_user()` and enforce it server-side.
