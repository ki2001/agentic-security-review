#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

SEVERITY_LEVEL = {
    "critical": "error",
    "high": "error",
    "medium": "warning",
    "low": "note",
    "informational": "note",
}


def finding_to_rule(finding: dict) -> dict:
    tags = []
    tags.extend(finding.get("cwe", []))
    tags.extend(finding.get("owasp", []))
    return {
        "id": finding["id"],
        "name": finding.get("category", finding["id"]),
        "shortDescription": {"text": finding["title"]},
        "fullDescription": {"text": finding.get("summary", "")},
        "help": {"text": finding.get("recommended_fix", "")},
        "properties": {
            "problem.severity": finding.get("severity"),
            "confidence": finding.get("confidence"),
            "tags": tags,
        },
    }


def finding_to_result(finding: dict) -> dict:
    affected = finding.get("affected_files", [{}])[0]
    path = affected.get("path", "unknown")
    lines = affected.get("lines") or [1]
    return {
        "ruleId": finding["id"],
        "level": SEVERITY_LEVEL.get(finding.get("severity"), "warning"),
        "message": {"text": f"{finding['title']}: {finding.get('summary', '')}"},
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {"uri": path},
                    "region": {"startLine": int(lines[0])},
                }
            }
        ],
        "properties": {
            "confidence": finding.get("confidence"),
            "impact": finding.get("impact"),
            "safe_reproduction": finding.get("exploitability", {}).get("safe_reproduction"),
        },
    }


def convert_report(report: dict) -> dict:
    findings = report.get("findings", [])
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "agentic-security-review",
                        "informationUri": "https://github.com/ki2001/agentic-security-review",
                        "rules": [finding_to_rule(finding) for finding in findings],
                    }
                },
                "results": [finding_to_result(finding) for finding in findings],
                "properties": {
                    "target": report.get("target"),
                    "mode": report.get("mode"),
                    "authorized": report.get("authorized"),
                    "summary": report.get("summary"),
                },
            }
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export an Agentic Security Review JSON report as SARIF 2.1.0")
    parser.add_argument("report", help="Path to Agentic Security Review JSON report")
    parser.add_argument("--output", "-o", help="Output SARIF path. Defaults to stdout")
    args = parser.parse_args()

    report = json.loads(Path(args.report).read_text())
    sarif = convert_report(report)
    text = json.dumps(sarif, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text)
        print(f"wrote: {args.output}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
