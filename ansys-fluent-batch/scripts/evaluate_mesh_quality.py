from __future__ import annotations

import argparse
from pathlib import Path

from fluent_common import dump_json, load_json, resolve_path


def _append_check(checks: list[dict], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": passed, "detail": detail})


def evaluate(summary: dict, gate: dict) -> dict:
    checks: list[dict] = []
    fail_if_missing = bool(gate.get("fail_if_missing_keys", True))

    thresholds = gate.get("thresholds", {})
    required_summary_keys = {
        "max_skewness": "max_skewness",
        "min_orthogonal_quality": "min_orthogonal_quality",
        "max_negative_cell_count": "negative_cell_count",
    }
    for threshold_key, summary_key in required_summary_keys.items():
        if threshold_key in thresholds and summary_key not in summary:
            passed = not fail_if_missing
            _append_check(checks, f"summary_has_{summary_key}", passed, "missing summary key")

    if "max_skewness" in thresholds and "max_skewness" in summary:
        passed = float(summary["max_skewness"]) <= float(thresholds["max_skewness"])
        _append_check(checks, "max_skewness", passed, f"{summary['max_skewness']} <= {thresholds['max_skewness']}")

    if "min_orthogonal_quality" in thresholds and "min_orthogonal_quality" in summary:
        passed = float(summary["min_orthogonal_quality"]) >= float(thresholds["min_orthogonal_quality"])
        _append_check(checks, "min_orthogonal_quality", passed, f"{summary['min_orthogonal_quality']} >= {thresholds['min_orthogonal_quality']}")

    if "max_negative_cell_count" in thresholds and "negative_cell_count" in summary:
        passed = int(summary["negative_cell_count"]) <= int(thresholds["max_negative_cell_count"])
        _append_check(checks, "negative_cell_count", passed, f"{summary['negative_cell_count']} <= {thresholds['max_negative_cell_count']}")

    boundary_zone_names = set(summary.get("boundary_zone_names", []))
    cell_zone_names = set(summary.get("cell_zone_names", []))

    for zone in gate.get("required_boundary_zones", []):
        passed = zone in boundary_zone_names
        _append_check(checks, f"required_boundary_zone:{zone}", passed, "present" if passed else "missing")

    for zone in gate.get("required_cell_zones", []):
        passed = zone in cell_zone_names
        _append_check(checks, f"required_cell_zone:{zone}", passed, "present" if passed else "missing")

    for zone in gate.get("forbidden_boundary_zones", []):
        passed = zone not in boundary_zone_names
        _append_check(checks, f"forbidden_boundary_zone:{zone}", passed, "absent" if passed else "present")

    passed = all(item["passed"] for item in checks)
    return {"passed": passed, "checks": checks}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a Fluent mesh summary against quality gates.")
    parser.add_argument("--gate", required=True, help="Path to the quality gate JSON file.")
    parser.add_argument("--summary", required=True, help="Path to the mesh summary JSON file.")
    parser.add_argument("--output", default="", help="Optional path for the evaluation result JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    gate_path = resolve_path(args.gate)
    summary_path = resolve_path(args.summary)

    gate = load_json(gate_path)
    summary = load_json(summary_path)
    result = evaluate(summary=summary, gate=gate)

    if args.output:
        output_path = resolve_path(args.output)
    else:
        output_path = summary_path.with_name("mesh_quality_result.json")
    dump_json(
        output_path,
        {
            "gate_file": str(gate_path),
            "summary_file": str(summary_path),
            **result,
        },
    )

    print(f"Result file: {output_path}")
    print(f"Passed: {result['passed']}")
    for check in result["checks"]:
        status = "PASS" if check["passed"] else "FAIL"
        print(f"{status}: {check['name']} - {check['detail']}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
