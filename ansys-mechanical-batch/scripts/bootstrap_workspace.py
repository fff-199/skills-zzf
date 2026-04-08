from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from wbjn_common import ASSETS_DIR, dump_json, ensure_dir, load_json, resolve_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a reusable ANSYS Mechanical batch workspace.")
    parser.add_argument("--dest", required=True, help="Destination workspace folder.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing template files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dest = resolve_path(args.dest)

    config_dir = ensure_dir(dest / "config")
    ensure_dir(dest / "projects")
    ensure_dir(dest / "runs")
    templates_dir = ensure_dir(dest / "templates")

    config_path = config_dir / "mechanical_config.example.json"
    stub_path = templates_dir / "mechanical_post_stub.py"

    if not args.force and (config_path.exists() or stub_path.exists()):
        raise FileExistsError(
            "Workspace template files already exist. Use --force to overwrite them."
        )

    config_payload = load_json(ASSETS_DIR / "mechanical_config.example.json")
    config_payload["project"]["wbpj_path"] = str((dest / "projects" / "your_model.wbpj").resolve())
    config_payload["project"]["working_dir"] = str((dest / "runs" / "demo_case").resolve())
    dump_json(config_path, config_payload)

    shutil.copy2(ASSETS_DIR / "mechanical_post_stub.py", stub_path)

    print(f"Workspace initialized at: {dest}")
    print(f"Config template: {config_path}")
    print(f"Mechanical stub: {stub_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
