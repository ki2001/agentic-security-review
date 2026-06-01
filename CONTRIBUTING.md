# Contributing

Contributions are welcome if they improve defensive, authorized security review.

## Good contributions

- Better review prompts and guardrails.
- Report schema improvements.
- Demo vulnerable apps.
- SARIF/GitHub Action support.
- Safe scanner integrations.
- Tests and documentation.

## Not accepted

- Weaponized exploit automation.
- Live target scanning features by default.
- Credential theft, persistence, malware, or stealth features.
- Content encouraging unauthorized access.

## Development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest -q
```
