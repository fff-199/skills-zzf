---
name: ansys-mechanical-batch
description: Use when the user wants to automate ANSYS Workbench Mechanical on this Windows machine, especially for parameterized `.wbpj` projects, batch solves, Workbench journal (`.wbjn`) generation, input/output parameter inspection, parameter sweeps, or AI closed-loop optimization around Mechanical. Prefer this skill when the task fits the pattern "inspect Workbench parameters, set parameter expressions on a design point, run an update, and collect output parameters or results" and avoid direct GUI-only workflows unless batch mode is insufficient.
---

# ANSYS Mechanical Batch

Use this skill to drive ANSYS Mechanical through Workbench batch mode first. Keep the first version conservative:

1. Start from an existing parameterized `.wbpj`
2. Inspect Workbench parameter IDs
3. Update a design point through parameter expressions
4. Run `UpdateAllDesignPoints`
5. Read back Workbench output parameters from JSON

Prefer this over direct GUI scripting because it is more stable for repeatable runs and AI optimization loops.

## Environment

Use these machine-local defaults unless the user points to a different install:

- Workbench batch: `D:\ANSYS\ANSYS Inc\v251\Framework\bin\Win64\RunWB2.exe`
- Mechanical UI: `D:\ANSYS\ANSYS Inc\v251\aisol\bin\winx64\AnsysWBU.exe`
- License server: `1055@localhost`

If batch launch fails, inspect `workbench_console.log` first and confirm the project still opens interactively in Workbench.

## Quick Start

If the user needs a new automation workspace, scaffold one with:

```powershell
python "C:\Users\fff\.codex\skills\ansys-mechanical-batch\scripts\bootstrap_workspace.py" `
  --dest "F:\pyANSYS-AI"
```

Inspect a project before changing anything:

```powershell
python "C:\Users\fff\.codex\skills\ansys-mechanical-batch\scripts\inspect_mechanical_project.py" `
  --project "F:\pyANSYS-AI\projects\your_model.wbpj" `
  --output-dir "F:\pyANSYS-AI\runs\inspect_case"
```

Run a parameterized batch solve after editing the config:

```powershell
python "C:\Users\fff\.codex\skills\ansys-mechanical-batch\scripts\run_mechanical_batch.py" `
  --config "F:\pyANSYS-AI\config\mechanical_config.example.json"
```

## Workflow

### 1. Stabilize the model

- Require an existing `.wbpj` rather than drawing complex geometry from scratch.
- Promote every optimization variable to a Workbench input parameter.
- Promote every acceptance metric needed by automation to a Workbench output parameter.
- Prefer numeric outputs; do not use screenshots or contour images as data sources.

### 2. Inspect the parameter map

Run `scripts/inspect_mechanical_project.py` and read the generated JSON to find:

- input parameter IDs such as `P1`, `P2`
- output parameter IDs such as `P3`, `P4`
- available design-point names

Use explicit units in expressions like `"10 [mm]"` or `"1000 [N]"`.

### 3. Solve in batch

Use `scripts/run_mechanical_batch.py` with a config JSON. The script:

- opens the source project
- saves a working copy into the run folder
- sets parameter expressions on the chosen design point
- updates the design point
- writes `results.json`

Keep each solve in its own working directory so runs are reproducible.

### 4. Build the closed loop

Once one batch solve is stable, wrap the config edits in a Python loop:

1. choose the next candidate parameter set
2. run `run_mechanical_batch.py`
3. read `results.json`
4. compare outputs to numeric acceptance criteria
5. stop on success or generate the next candidate

Use this loop for sweeps, bisection, heuristic search, or an AI-selected next design point.

### 5. Escalate only when Workbench parameters are not enough

If the user needs result objects or exports that are not already promoted to Workbench outputs:

- start from `assets/mechanical_post_stub.py`
- add in-Mechanical scripting for result creation or tabular export
- keep the outer orchestration in Workbench batch mode

If the task is pure structural or thermal solving without a strong Workbench dependency, consider `MAPDL` or `PyMAPDL` instead of forcing everything through Mechanical.

## Constraints

- Prefer batch mode over GUI control.
- Prefer Workbench parameters over clicking tree objects.
- Write explicit units in parameter expressions.
- Export structured numeric data to JSON, CSV, or text.
- Save a copied working project for each run instead of mutating the original project in place.
- Read `workbench_console.log` whenever `results.json` is missing.

## Resources

- `scripts/bootstrap_workspace.py`: create a reusable workspace skeleton with config, templates, `projects/`, and `runs/`
- `scripts/inspect_mechanical_project.py`: dump Workbench parameter and design-point metadata to JSON
- `scripts/run_mechanical_batch.py`: apply parameter expressions, solve, and export output parameters
- `assets/mechanical_config.example.json`: config template for one batch run
- `assets/mechanical_post_stub.py`: starting point for future in-Mechanical scripting
