from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from fluent_common import ASSETS_DIR, DEFAULT_FLUENT, dump_json, ensure_dir, load_json, resolve_path, run_command, split_arguments


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a headless Fluent meshing or solver journal.")
    parser.add_argument(
        "--config",
        default=str(ASSETS_DIR / "fluent_batch_config.example.json"),
        help="Path to the JSON config file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print and record the command without launching Fluent.",
    )
    return parser.parse_args()


def build_command(config: dict, config_dir: Path) -> tuple[list[str], Path]:
    fluent = resolve_path(config.get("ansys", {}).get("fluent", str(DEFAULT_FLUENT)), base_dir=config_dir)
    if not fluent.exists():
        raise FileNotFoundError(f"fluent.exe not found: {fluent}")

    launch = config.get("launch", {})
    files = config.get("files", {})

    dimension = str(launch.get("dimension", "3ddp"))
    mode = str(launch.get("mode", "solver")).lower()
    processors = int(launch.get("processors", 1))
    gui = bool(launch.get("gui", False))
    additional_arguments = str(launch.get("additional_arguments", ""))

    journal = resolve_path(files["journal"], base_dir=config_dir)
    working_dir = resolve_path(files.get("working_dir", str(Path.cwd() / "runs" / f"fluent_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}")), base_dir=config_dir)
    ensure_dir(working_dir)

    if not journal.exists():
        raise FileNotFoundError(f"Journal file not found: {journal}")

    command = [str(fluent), dimension]
    if mode == "meshing":
        command.append("-meshing")
    if not gui:
        command.append("-g")
    if processors > 1:
        command.append(f"-t{processors}")
    command.extend(split_arguments(additional_arguments))
    command.extend(["-i", str(journal)])
    return command, working_dir


def main() -> int:
    args = parse_args()
    config_path = resolve_path(args.config)
    config = load_json(config_path)
    config_dir = config_path.parent

    command, working_dir = build_command(config=config, config_dir=config_dir)
    log_path = working_dir / "fluent_console.log"
    manifest_path = working_dir / "fluent_run_manifest.json"

    dump_json(manifest_path, {"command": command, "working_dir": str(working_dir)})

    if args.dry_run:
        print("Dry run command:")
        print(" ".join(command))
        print(f"Working directory: {working_dir}")
        print(f"Manifest: {manifest_path}")
        return 0

    completed = run_command(command=command, cwd=working_dir, log_path=log_path)
    dump_json(
        manifest_path,
        {
            "command": command,
            "working_dir": str(working_dir),
            "return_code": completed.returncode,
            "log": str(log_path),
        },
    )

    print(f"Working directory: {working_dir}")
    print(f"Console log: {log_path}")
    print(f"Return code: {completed.returncode}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
