import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def test_sample_report_matches_report_schema():
    schema = json.loads((ROOT / "schemas" / "report.schema.json").read_text())
    report = json.loads((ROOT / "examples" / "sample-reports" / "vulnerable-python-api-report.json").read_text())

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(report), key=lambda e: e.path)

    assert errors == []


def test_finding_schema_rejects_missing_required_fields():
    schema = json.loads((ROOT / "schemas" / "finding.schema.json").read_text())
    validator = Draft202012Validator(schema)

    errors = list(validator.iter_errors({"title": "Missing most fields"}))

    assert errors
    assert any("severity" in str(error.message) or "required" in str(error.message) for error in errors)
