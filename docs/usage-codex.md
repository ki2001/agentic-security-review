# Usage with Codex

From a target repository, run Codex with the contents of `skills/codex/security-reviewer.md` plus your target scope.

Example prompt preparation:

```bash
python scripts/run_review.py ./my-repo --agent codex --authorized > /tmp/asr-codex-prompt.md
codex exec "$(cat /tmp/asr-codex-prompt.md)"
```

Keep the review static/local unless you have explicit authorization for more.
