import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sarif_export_cli_converts_sample_report(tmp_path):
    output = tmp_path / "report.sarif"

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "export_sarif.py"),
            str(ROOT / "examples" / "sample-reports" / "vulnerable-python-api-report.json"),
            "--output",
            str(output),
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    sarif = json.loads(output.read_text())
    assert sarif["version"] == "2.1.0"
    run = sarif["runs"][0]
    assert run["tool"]["driver"]["name"] == "agentic-security-review"
    assert run["results"]
    assert all(result["locations"] for result in run["results"])
