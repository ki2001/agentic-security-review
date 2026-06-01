from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_codex_skill_contains_required_safety_and_report_sections():
    text = (ROOT / "skills" / "codex" / "security-reviewer.md").read_text()

    required_phrases = [
        "authorized defensive security reviewer",
        "Do not perform live exploitation",
        "Scope confirmation",
        "Repository reconnaissance",
        "Vulnerability report format",
        "CWE",
        "OWASP",
        "Remediation",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_claude_skill_contains_required_safety_and_workflow_sections():
    text = (ROOT / "skills" / "claude" / "security-reviewer.md").read_text()

    required_phrases = [
        "authorized defensive security reviewer",
        "Do not perform live exploitation",
        "Attack surface mapping",
        "Evidence validation",
        "Vulnerability report format",
        "Suggested tests",
    ]

    for phrase in required_phrases:
        assert phrase in text
