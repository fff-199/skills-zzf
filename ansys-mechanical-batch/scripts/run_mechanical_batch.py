from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from wbjn_common import ASSETS_DIR, DEFAULT_RUNWB2, ensure_dir, load_json, resolve_path, run_workbench, wb_path, write_text


def build_journal(
    source_project: Path,
    working_project: Path,
    result_file: Path,
    design_point_name: str,
    inputs: dict[str, str],
    outputs: list[str],
) -> str:
    source_project_wb = wb_path(source_project)
    working_project_wb = wb_path(working_project)
    result_file_wb = wb_path(result_file)
    inputs_json = json.dumps(inputs, ensure_ascii=True, indent=2)
    outputs_json = json.dumps(outputs, ensure_ascii=True, indent=2)

    return f"""# encoding: utf-8
SetScriptVersion(Version="25.1.0")
import json

source_project = r"{source_project_wb}"
working_project = r"{working_project_wb}"
result_file = r"{result_file_wb}"
target_design_point = "{design_point_name}"
input_updates = json.loads(r'''{inputs_json}''')
requested_outputs = json.loads(r'''{outputs_json}''')


def serialize_parameter(parameter, design_point):
    raw_value = Parameters.GetParameterValueForDesignPoint(
        DesignPoint=design_point,
        Parameter=parameter
    )
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

    return {{
        "name": parameter.Name,
        "display_text": str(parameter.DisplayText),
        "usage": str(parameter.Usage),
        "expression": str(parameter.Expression),
        "value": value,
        "unit": unit,
        "quantity_name": str(parameter.ValueQuantityName),
        "error_message": str(parameter.ErrorMessage),
    }}


Open(FilePath=source_project)
Save(FilePath=working_project, Overwrite=True)

all_parameters = {{}}
for parameter in Parameters.GetAllParameters():
    all_parameters[parameter.Name] = parameter

design_point = None
for candidate in Parameters.GetAllDesignPoints():
    if candidate.Name == target_design_point or str(candidate.DisplayText) == target_design_point:
        design_point = candidate
        break

if design_point is None:
    raise Exception("Design point not found: " + target_design_point)

for parameter_name, expression in input_updates.items():
    if parameter_name not in all_parameters:
        raise Exception("Input parameter not found: " + parameter_name)
    design_point.SetParameterExpression(all_parameters[parameter_name], expression)

UpdateAllDesignPoints(DesignPoints=[design_point])

input_payload = []
for parameter_name in sorted(input_updates.keys()):
    input_payload.append(serialize_parameter(all_parameters[parameter_name], design_point))

output_payload = []
for parameter_name in requested_outputs:
    if parameter_name not in all_parameters:
        raise Exception("Output parameter not found: " + parameter_name)
    output_payload.append(serialize_parameter(all_parameters[parameter_name], design_point))

payload = {{
    "source_project": source_project,
    "working_project": working_project,
    "design_point": {{
        "name": design_point.Name,
        "display_text": str(design_point.DisplayText),
        "retained": bool(design_point.Retained),
        "note": str(design_point.Note),
    }},
    "inputs": input_payload,
    "outputs": output_payload,
}}

with open(result_file, "w") as stream:
    stream.write(json.dumps(payload, indent=2))

Save()
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a parameterized Mechanical Workbench project in batch mode.")
    parser.add_argument(
        "--config",
        default=str(ASSETS_DIR / "mechanical_config.example.json"),
        help="Path to the JSON config file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only generate the journal and run folder, do not launch Workbench.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = resolve_path(args.config)
    config = load_json(config_path)
    config_dir = config_path.parent

    runwb2 = resolve_path(config.get("ansys", {}).get("runwb2", str(DEFAULT_RUNWB2)), base_dir=config_dir)
    source_project = resolve_path(config["project"]["wbpj_path"], base_dir=config_dir)
    outputs = list(config.get("outputs", []))
    inputs = dict(config.get("inputs", {}))
    design_point_name = str(config.get("design_point", {}).get("name", "0"))

    if not runwb2.exists():
        raise FileNotFoundError(f"RunWB2.exe not found: {runwb2}")
    if not source_project.exists():
        raise FileNotFoundError(f"Workbench project not found: {source_project}")
    if not inputs:
        raise ValueError("No input parameters were provided in the config.")
    if not outputs:
        raise ValueError("No output parameters were provided in the config.")

    configured_working_dir = config.get("project", {}).get("working_dir", "")
    if configured_working_dir:
        run_dir = resolve_path(configured_working_dir, base_dir=config_dir)
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = Path.cwd() / "runs" / f"mechanical_run_{stamp}"
    ensure_dir(run_dir)

    working_project = run_dir / f"{source_project.stem}_run.wbpj"
    journal_file = run_dir / "solve_mechanical.wbjn"
    result_file = run_dir / "results.json"
    log_file = run_dir / "workbench_console.log"

    journal_text = build_journal(
        source_project=source_project,
        working_project=working_project,
        result_file=result_file,
        design_point_name=design_point_name,
        inputs=inputs,
        outputs=outputs,
    )
    write_text(journal_file, journal_text)

    if args.dry_run:
        print(f"Journal written to: {journal_file}")
        print(f"Run directory: {run_dir}")
        return 0

    completed = run_workbench(runwb2=runwb2, journal=journal_file, log_path=log_file)

    if not result_file.exists():
        raise RuntimeError(
            "Workbench finished without producing results.json. "
            f"Check the log: {log_file}"
        )

    result_payload = json.loads(result_file.read_text(encoding="utf-8"))
    print(f"Run directory: {run_dir}")
    print(f"Results JSON: {result_file}")
    print(f"Workbench log: {log_file}")
    print(f"Return code: {completed.returncode}")
    print("Output summary:")
    for item in result_payload["outputs"]:
        value = item["value"]
        unit = item["unit"]
        suffix = f" {unit}" if unit else ""
        print(f"  {item['name']} ({item['display_text']}): {value}{suffix}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
