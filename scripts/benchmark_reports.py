#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def score_benchmark(benchmark: dict, report: dict) -> dict:
    expected = benchmark.get("expected_findings", [])
    findings = report.get("findings", [])
    finding_text = "\n".join(
        " ".join([
            finding.get("id", ""),
            finding.get("title", ""),
            finding.get("category", ""),
            " ".join(finding.get("cwe", [])),
            " ".join(finding.get("owasp", [])),
        ]).lower()
        for finding in findings
    )
    matches = []
    misses = []
    for item in expected:
        terms = [term.lower() for term in item.get("match_terms", [])]
        if terms and any(term in finding_text for term in terms):
            matches.append(item["id"])
        else:
            misses.append(item["id"])
    total = len(expected)
    return {
        "benchmark": benchmark["name"],
        "total_expected": total,
        "matched": len(matches),
        "missed": len(misses),
        "score": (len(matches) / total) if total else 0,
        "matched_ids": matches,
        "missed_ids": misses,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a report against a deliberately vulnerable demo benchmark manifest")
    parser.add_argument("benchmark", help="Benchmark manifest JSON")
    parser.add_argument("report", help="Agentic Security Review JSON report")
    args = parser.parse_args()
    benchmark = json.loads(Path(args.benchmark).read_text())
    report = json.loads(Path(args.report).read_text())
    print(json.dumps(score_benchmark(benchmark, report), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
