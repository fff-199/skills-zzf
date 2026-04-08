---
name: aspen-plus-local-automation
description: Automate local Aspen Plus models on this Windows machine through Python COM using the existing AspenPlus-Python-Interface workspace. Use when a user wants to connect to a local Aspen Plus `.bkp` or `.apw` model, control blocks or streams from code, run closed-loop simulations, perform sensitivity or optimization studies, export Aspen artifacts such as `.rep`, `.sum`, and `.cpm`, or postprocess Aspen outputs into CSV, JSON, or plots.
---

# Aspen Plus Local Automation

Use the existing local workspace instead of rebuilding the integration from scratch.

## Use This Workspace

Work from:

- `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main`

Prefer the scaffold in:

- `D:\VScode file\ASPEN\aspenpy\AspenPlus-Python-Interface-main\starter_project`

Read [references/repo-map.md](references/repo-map.md) when you need the exact local file map.

## Follow This Workflow

1. Confirm Aspen Plus can open the target `.bkp` or `.apw` model manually before touching code.
2. Edit `starter_project/project_config.json` to point at the target model, default stream probe, mutation case, and sensitivity case.
3. Run `python scripts/env_check.py` from `starter_project` to verify COM, model loading, one `Run()`, and one stream read.
4. Run `python scripts/single_run.py` to validate the minimal closed loop: set parameter, run, read outputs, restore, and export `.rep/.sum/.cpm`.
5. Run `python scripts/sensitivity_radfrac.py` only after the single-run loop is stable.
6. Extend wrappers only when needed. First check whether `CodeLibrary.py` already exposes the Aspen variable. If not, use Aspen Variable Explorer to find the path and add a thin helper to the starter project.

## Reuse These Files

- `starter_project/project_config.json`: central model and case configuration
- `starter_project/app/config.py`: config loader
- `starter_project/app/codelibrary_loader.py`: imports `示例脚本/CodeLibrary.py`
- `starter_project/app/aspen_runner.py`: Aspen session wrapper
- `starter_project/app/postprocess.py`: CSV, JSON, and plot helpers
- `starter_project/scripts/env_check.py`: smoke test
- `starter_project/scripts/single_run.py`: minimal closed loop
- `starter_project/scripts/sensitivity_radfrac.py`: batch scan template

## Respect These Constraints

- Run Aspen in serial. Do not start multiple parallel Aspen COM sessions unless you first redesign the wrapper.
- Expect `CodeLibrary.py` to change the Python process working directory during session startup.
- Expect `CodeLibrary.py` to hold Aspen COM state at class level. Reuse a single session per script.
- Expect Aspen text exports to land in the Aspen model directory rather than the `starter_project/outputs` folder.
- Enable dialog suppression for unattended runs.
- Treat Aspen run messages as first-class diagnostics. If a case fails, inspect the exported `.cpm` before changing the optimizer or loop logic.

## Extend Safely

When a user asks for new automation around a specific model:

1. Identify the exact Aspen object names: blocks, streams, feeds, and KPIs.
2. Start with one controlled mutation and one output probe.
3. Add failure logging and restore logic before adding optimization.
4. Save structured results to `starter_project/outputs` as JSON or CSV.
5. Export Aspen text artifacts for traceability when the run matters.

## Validate Before Calling It Done

After edits to the scaffold or a model mapping:

1. Run `python scripts/env_check.py`.
2. Run `python scripts/single_run.py`.
3. Run the relevant batch script only after the first two are green.

If a user asks to build a new Aspen automation flow from scratch, start by adapting `starter_project` rather than modifying the original `示例脚本` files.
