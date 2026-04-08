from __future__ import annotations

import argparse
from pathlib import Path

from fluent_common import ASSETS_DIR, dump_json, ensure_dir, load_json, resolve_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a reusable ANSYS Fluent batch workspace.")
    parser.add_argument("--dest", required=True, help="Destination workspace folder.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing template files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dest = resolve_path(args.dest)

    config_dir = ensure_dir(dest / "config")
    ensure_dir(dest / "geometry")
    ensure_dir(dest / "journals")
    ensure_dir(dest / "reports")
    ensure_dir(dest / "runs")

    batch_config_path = config_dir / "fluent_batch_config.example.json"
    gate_config_path = config_dir / "mesh_quality_gate.example.json"
    summary_path = dest / "reports" / "mesh_summary.example.json"

    if not args.force and (batch_config_path.exists() or gate_config_path.exists() or summary_path.exists()):
        raise FileExistsError(
            "Workspace template files already exist. Use --force to overwrite them."
        )

    batch_config = load_json(ASSETS_DIR / "fluent_batch_config.example.json")
    batch_config["files"]["journal"] = str((dest / "journals" / "mesh_case_001.jou").resolve())
    batch_config["files"]["working_dir"] = str((dest / "runs" / "mesh_case_001").resolve())
    dump_json(batch_config_path, batch_config)

    dump_json(gate_config_path, load_json(ASSETS_DIR / "mesh_quality_gate.example.json"))
    dump_json(summary_path, load_json(ASSETS_DIR / "mesh_summary.example.json"))

    print(f"Workspace initialized at: {dest}")
    print(f"Batch config: {batch_config_path}")
    print(f"Quality gate config: {gate_config_path}")
    print(f"Summary example: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
