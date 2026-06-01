# Safety Policy

## Allowed by default

- Static review of local code.
- Static review of public GitHub repositories.
- Review of private code when the user is authorized.
- Safe local reproduction notes for toy/demo targets.
- Remediation guidance and suggested tests.

## Restricted by default

- Live external probing or scanning.
- Exploit delivery against third-party systems.
- Credential harvesting.
- Malware, persistence, stealth, or destructive operations.
- Weaponized payload generation.

## Agent instruction

Every review prompt must include: **Do not perform live exploitation.**
