from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_ROOT / "assets"


def discover_runwb2() -> Path:
    env_path = os.environ.get("RUNWB2_EXE")
    if env_path:
        return Path(env_path).expanduser()

    ansys_root = os.environ.get("ANSYS_ROOT")
    if ansys_root:
        candidate = Path(ansys_root).expanduser() / "Framework" / "bin" / "Win64" / "RunWB2.exe"
        if candidate.exists():
            return candidate

    for candidate in common_runwb2_candidates():
        if candidate.exists():
            return candidate

    return Path("RunWB2.exe")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def dump_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(path_str: str, base_dir: Path | None = None) -> Path:
    path = Path(path_str).expanduser()
    if not path.is_absolute() and base_dir is not None:
        path = base_dir / path
    return path.resolve()


def wb_path(path: Path) -> str:
    return path.resolve().as_posix()


def common_runwb2_candidates() -> list[Path]:
    candidates: list[Path] = []
    for root in _common_ansys_roots():
        try:
            versions = sorted((path for path in root.iterdir() if path.is_dir()), reverse=True)
        except OSError:
            continue
        for version_dir in versions:
            candidates.append(version_dir / "Framework" / "bin" / "Win64" / "RunWB2.exe")
    return candidates


def _common_ansys_roots() -> list[Path]:
    roots: list[Path] = []
    for drive in ("C", "D", "E", "F", "G"):
        drive_root = Path(f"{drive}:\\")
        if not drive_root.exists():
            continue
        for candidate in (
            drive_root / "Program Files" / "ANSYS Inc",
            drive_root / "ANSYS" / "ANSYS Inc",
        ):
            if candidate.exists():
                roots.append(candidate)
    return roots


DEFAULT_RUNWB2 = discover_runwb2()


def run_workbench(runwb2: Path, journal: Path, log_path: Path, timeout_s: int | None = None) -> subprocess.CompletedProcess[str]:
    command = [str(runwb2), "-B", "-R", str(journal)]
    completed = subprocess.run(
        command,
        cwd=str(journal.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_s,
    )

    log_text = []
    log_text.append("COMMAND:")
    log_text.append(" ".join(command))
    log_text.append("")
    log_text.append("RETURN CODE:")
    log_text.append(str(completed.returncode))
    log_text.append("")
    log_text.append("STDOUT:")
    log_text.append(completed.stdout)
    log_text.append("")
    log_text.append("STDERR:")
    log_text.append(completed.stderr)
    write_text(log_path, "\n".join(log_text))
    return completed
