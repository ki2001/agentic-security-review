# Vulnerable Python API

This is a deliberately vulnerable local demo app for Agentic Security Review. Do not deploy it.

Intentional issues include:

- IDOR / broken access control on invoice lookup.
- Path traversal in file download.
- Hardcoded secret key.
- Debug mode enabled.
- Unsafe shell command construction.
