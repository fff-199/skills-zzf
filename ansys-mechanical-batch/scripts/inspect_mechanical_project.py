from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from wbjn_common import DEFAULT_RUNWB2, ensure_dir, resolve_path, run_workbench, wb_path, write_text


def build_journal(project_file: Path, result_file: Path) -> str:
    project_wb = wb_path(project_file)
    result_wb = wb_path(result_file)

    return f"""# encoding: utf-8
SetScriptVersion(Version="25.1.0")
import json

project_file = r"{project_wb}"
result_file = r"{result_wb}"

Open(FilePath=project_file)

parameter_payload = []
for parameter in Parameters.GetAllParameters():
    raw_value = parameter.Value
    value = ""
    unit = ""
    try:
        value = raw_value.Value
        unit = raw_value.Unit
    except:
        if raw_value is None:
            value = ""
        else:
            value = str(raw_value)

    parameter_payload.append({{
        "name": parameter.Name,
        "display_text": str(parameter.DisplayText),
        "usage": str(parameter.Usage),
        "expression": str(parameter.Expression),
        "expression_type": str(parameter.ExpressionType),
        "quantity_name": str(parameter.ValueQuantityName),
        "value": value,
        "unit": unit,
        "error_message": str(parameter.ErrorMessage),
    }})

design_point_payload = []
for design_point in Parameters.GetAllDesignPoints():
    design_point_payload.append({{
        "name": design_point.Name,
        "display_text": str(design_point.DisplayText),
        "retained": bool(design_point.Retained),
        "note": str(design_point.Note),
    }})

payload = {{
    "project_file": project_file,
    "parameter_count": len(parameter_payload),
    "design_point_count": len(design_point_payload),
    "parameters": parameter_payload,
    "design_points": design_point_payload,
}}

with open(result_file, "w") as stream:
    stream.write(json.dumps(payload, indent=2))
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect Workbench Mechanical parameters and design points.")
    parser.add_argument("--project", required=True, help="Path to the source .wbpj file.")
    parser.add_argument(
        "--runwb2",
        default=str(DEFAULT_RUNWB2),
        help="Path to RunWB2.exe. Defaults to the detected ANSYS 2025 R1 installation.",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Optional output directory. Defaults to runs/inspect_<timestamp> under the current working directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only write the journal, do not launch Workbench.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    project_file = resolve_path(args.project)
    runwb2 = resolve_path(args.runwb2)

    if not project_file.exists():
        raise FileNotFoundError(f"Project file not found: {project_file}")
    if not runwb2.exists():
        raise FileNotFoundError(f"RunWB2.exe not found: {runwb2}")

    if args.output_dir:
        output_dir = resolve_path(args.output_dir)
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path.cwd() / "runs" / f"inspect_{stamp}"
    ensure_dir(output_dir)

    result_file = output_dir / "project_snapshot.json"
    journal_file = output_dir / "inspect_project.wbjn"
    log_file = output_dir / "workbench_console.log"

    write_text(journal_file, build_journal(project_file=project_file, result_file=result_file))

    if args.dry_run:
        print(f"Journal written to: {journal_file}")
        return 0

    completed = run_workbench(runwb2=runwb2, journal=journal_file, log_path=log_file)

    if not result_file.exists():
        raise RuntimeError(
            "Workbench finished without producing the snapshot JSON. "
            f"Check the log: {log_file}"
        )

    snapshot = json.loads(result_file.read_text(encoding="utf-8"))
    print(f"Snapshot written to: {result_file}")
    print(f"Workbench log: {log_file}")
    print(f"Return code: {completed.returncode}")
    print(f"Parameters found: {snapshot['parameter_count']}")
    print(f"Design points found: {snapshot['design_point_count']}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
