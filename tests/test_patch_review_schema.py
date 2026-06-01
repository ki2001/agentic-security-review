import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def test_report_schema_accepts_patch_review_mode():
    schema = json.loads((ROOT / "schemas" / "report.schema.json").read_text())
    report = json.loads((ROOT / "examples" / "sample-reports" / "vulnerable-python-api-report.json").read_text())
    report["mode"] = "patch-review"

    errors = sorted(Draft202012Validator(schema).iter_errors(report), key=lambda e: e.path)

    assert errors == []
