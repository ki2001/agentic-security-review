import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_validate_report_cli_accepts_sample_report():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_report.py"), str(ROOT / "examples" / "sample-reports" / "vulnerable-python-api-report.json")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "valid" in result.stdout.lower()
