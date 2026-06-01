#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def validate_report(path: Path) -> list[str]:
    schema = json.loads((ROOT / "schemas" / "report.schema.json").read_text())
    report = json.loads(path.read_text())
    validator = Draft202012Validator(schema)
    return [f"{list(error.path)}: {error.message}" for error in sorted(validator.iter_errors(report), key=lambda e: e.path)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Agentic Security Review JSON report")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    errors = validate_report(args.report)
    if errors:
        print(f"invalid: {args.report}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"valid: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
