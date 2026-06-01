import json
import subprocess
import sys
from pathlib import Path

from scripts.run_review import ReviewOptions, build_review_prompt, resolve_target

ROOT = Path(__file__).resolve().parents[1]


def test_multi_agent_prompt_names_all_review_roles():
    target = resolve_target(str(ROOT / "examples" / "vulnerable-python-api"))
    prompt = build_review_prompt(
        target=target,
        agent="codex",
        authorized=True,
        options=ReviewOptions(mode="multi-agent"),
    )

    assert "Multi-agent review mode" in prompt
    assert "Recon mapper" in prompt
    assert "Vulnerability analyst" in prompt
    assert "Remediation reviewer" in prompt


def test_patch_review_prompt_is_diff_focused_and_safe(tmp_path):
    diff = tmp_path / "change.diff"
    diff.write_text("diff --git a/app.py b/app.py\n+subprocess.run(user_input, shell=True)\n")
    target = resolve_target(str(ROOT / "examples" / "vulnerable-python-api"))

    prompt = build_review_prompt(
        target=target,
        agent="claude",
        authorized=True,
        options=ReviewOptions(mode="patch-review", patch=str(diff)),
    )

    assert "Patch-review mode" in prompt
    assert "changed lines" in prompt
    assert "Do not perform live exploitation" in prompt
    assert "subprocess.run" in prompt


def test_scanner_context_cli_reports_missing_tools_without_failing():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "collect_scanner_context.py"), str(ROOT)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["target"]
    assert {tool["name"] for tool in payload["tools"]} >= {"semgrep", "bandit", "npm-audit", "pip-audit", "codeql"}
    assert all("available" in tool for tool in payload["tools"])


def test_benchmark_cli_scores_sample_report():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "benchmark_reports.py"),
            str(ROOT / "benchmarks" / "vulnerable-python-api.json"),
            str(ROOT / "examples" / "sample-reports" / "vulnerable-python-api-report.json"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["benchmark"] == "vulnerable-python-api"
    assert payload["total_expected"] >= 1
    assert payload["matched"] >= 1
    assert payload["score"] > 0


def test_github_action_workflow_exists_for_pr_reviews():
    workflow = (ROOT / ".github" / "workflows" / "agentic-security-review.yml").read_text()

    assert "pull_request" in workflow
    assert "scripts/run_review.py" in workflow
    assert "actions/upload-artifact" in workflow
