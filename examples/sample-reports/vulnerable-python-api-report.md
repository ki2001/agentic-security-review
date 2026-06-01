# Agentic Security Review Report: Vulnerable Python API

## Scope

- Target: `examples/vulnerable-python-api`
- Mode: authorized static review
- Live testing: not performed
- App status: deliberately vulnerable local demo app; do not deploy

## Executive summary

The demo Flask API contains several intentionally vulnerable patterns. The highest-impact issue is broken access control in invoice retrieval: the API trusts a request parameter for organization scope rather than deriving scope from authenticated server-side context.

Additional intentionally vulnerable patterns include path traversal in file download, hardcoded secret material, debug mode enabled, and unsafe shell command construction.

## Findings

### ASR-001: User-controlled org_id allows cross-tenant invoice access

- Severity: high
- Confidence: high
- Category: broken access control
- CWE: CWE-639
- OWASP: A01:2021-Broken Access Control
- Affected file: `examples/vulnerable-python-api/app.py`

#### Summary

The `/invoices/<invoice_id>` route reads `org_id` from the query string instead of deriving organization scope from the authenticated user/session. A user who can guess an invoice ID can request it with another organization's ID.

#### Evidence

```python
org_id = request.args.get("org_id")
invoice = INVOICES.get(invoice_id)
if not invoice or invoice["org_id"] != org_id:
    return jsonify({"error": "not found"}), 404
return jsonify(invoice)
```

The code compares invoice ownership to user-controlled input, not to trusted session data such as `current_user()["org_id"]`.

#### Impact

An authenticated user may retrieve invoices belonging to another organization if they know or guess invoice identifiers and organization IDs.

#### Safe local reproduction

Run only against the deliberately vulnerable local demo app:

```text
GET /invoices/inv_2?org_id=org_b
```

This demonstrates the issue using toy seeded data. Do not run against systems you are not authorized to test.

#### Recommended fix

Derive organization scope from trusted server-side user/session claims and enforce it in the lookup:

```python
user = current_user()
invoice = INVOICES.get(invoice_id)
if not invoice or invoice["org_id"] != user["org_id"]:
    return jsonify({"error": "not found"}), 404
```

#### Suggested tests

- User from `org_a` cannot access `inv_2`.
- Supplying `org_id` in the query string is ignored.
- Invoice lookup uses server-side session organization only.

## Other intentionally vulnerable patterns to review

- Path traversal in `/download` via unsanitized filename.
- Command injection risk in `/resize` via unsafe `os.system` string interpolation.
- Hardcoded Flask `SECRET_KEY`.
- `debug=True` in app startup.
