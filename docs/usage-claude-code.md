# Usage with Claude Code

Prepare a prompt:

```bash
python scripts/run_review.py ./my-repo --agent claude --authorized > /tmp/asr-claude-prompt.md
claude -p "$(cat /tmp/asr-claude-prompt.md)" --allowedTools 'Read,Bash' --max-turns 10
```

Use `Read` and limited `Bash` for local inspection. Do not grant broad network or destructive permissions for default reviews.
