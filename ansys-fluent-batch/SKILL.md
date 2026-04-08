---
name: ansys-fluent-batch
description: Use when the user wants to automate ANSYS Fluent on this Windows machine, especially for headless meshing, mesh quality gating, batch solver runs, existing `.msh`, `.cas`, or `.cas.h5` workflows, Fluent journal (`.jou`) orchestration, or AI closed-loop optimization around Fluent. Prefer this skill when meshing reliability, named zone stability, Watertight Geometry, fault-tolerant meshing, or mesh QA are material risks and avoid treating Fluent as a single-step solver launch.
---

# ANSYS Fluent Batch

Use this skill to treat Fluent as a meshing-plus-solver pipeline, not a one-line solver launch. Split the work into:

1. workspace setup
2. headless meshing or solver launch
3. mesh quality gate
4. optimization loop

Prefer this over ad hoc GUI operation when the user wants repeatable meshing, stable zones, batch journals, or closed-loop iteration.

## Environment

Use these machine-local defaults unless the user points elsewhere:

- Fluent launcher: `D:\ANSYS\ANSYS Inc\v251\fluent\ntbin\win64\fluent.exe`
- Embedded PyFluent Python: `D:\ANSYS\ANSYS Inc\v251\commonfiles\CPython\3_10\winx64\Release\python\python.exe`
- Local Workbench meshing journals:
  - `D:\ANSYS\ANSYS Inc\v251\aisol\CommonFiles\Utilities\Meshing\CutCellMeshingWithFluentTemplate.jou`
  - `D:\ANSYS\ANSYS Inc\v251\aisol\CommonFiles\Utilities\Meshing\TGAutoMeshingWithFluentTemplate.jou`

Keep `-g` in batch runs unless the user explicitly needs UI interaction.

## Quick Start

Scaffold a Fluent workspace first:

```powershell
python "C:\Users\fff\.codex\skills\ansys-fluent-batch\scripts\bootstrap_workspace.py" `
  --dest "F:\pyANSYS-AI\fluent"
```

Run a headless journal through `fluent.exe`:

```powershell
python "C:\Users\fff\.codex\skills\ansys-fluent-batch\scripts\run_fluent_journal.py" `
  --config "F:\pyANSYS-AI\fluent\config\fluent_batch_config.example.json"
```

Evaluate a mesh summary against numeric gates:

```powershell
python "C:\Users\fff\.codex\skills\ansys-fluent-batch\scripts\evaluate_mesh_quality.py" `
  --gate "F:\pyANSYS-AI\fluent\config\mesh_quality_gate.example.json" `
  --summary "F:\pyANSYS-AI\fluent\reports\mesh_summary.json"
```

## Workflow

### 1. Choose the route before automating

- If the user already has a valid `.msh` or `.cas.h5`, prefer solver-only automation first.
- If the CAD is clean and parameterized, use batch meshing.
- If the CAD is dirty, leaky, or topology changes often, do manual cleanup first and automate only after the meshing path is stable.

Read [references/workflow-map.md](references/workflow-map.md) before deciding how much of the geometry and mesh pipeline to automate.

### 2. Separate meshing from solving

- Run meshing and solver in different journals or clearly separated phases.
- Do not change geometry, remesh, and solve in one opaque step unless the process is already proven stable.
- Preserve zone naming because the solver stage depends on stable boundary and cell zone IDs.

### 3. Gate the mesh numerically

Do not accept a mesh because it "looks fine". Export and check:

- negative cell count
- max skewness
- min orthogonal quality
- required boundary zones
- required cell zones
- unexpected or missing zones

Use `scripts/evaluate_mesh_quality.py` with [references/mesh-quality-gates.md](references/mesh-quality-gates.md).

### 4. Freeze the mesh before optimization when possible

- First optimize with a fixed mesh and varying BCs, models, or material values.
- Only allow geometry changes after the remeshing path passes quality gates repeatedly.
- For geometry-driven loops, keep a per-run mesh summary and a per-run solver summary.

### 5. Escalate carefully

If journal-only control is insufficient:

- use embedded PyFluent from the installed ANSYS Python
- keep the same quality gates and headless workflow
- do not let AI improvise freeform meshing on fragile CAD

## Constraints

- Prefer `-g` headless mode.
- Prefer journal or API orchestration over GUI clicks.
- Treat meshing as a separate failure surface.
- Enforce numeric mesh QA before solving.
- Do not parse contour screenshots as data.
- Keep one run directory per case for reproducibility.
- Release sessions and licenses cleanly after each run.

## Resources

- `scripts/bootstrap_workspace.py`: create a reusable Fluent workspace with config, journals, reports, and runs folders
- `scripts/run_fluent_journal.py`: launch headless Fluent meshing or solver runs from a config JSON
- `scripts/evaluate_mesh_quality.py`: enforce numeric mesh-quality gates from JSON summaries
- `assets/fluent_batch_config.example.json`: example batch-launch config
- `assets/mesh_quality_gate.example.json`: example thresholds and required zones
- `assets/mesh_summary.example.json`: example input format for the quality-gate script
- `references/workflow-map.md`: route selection for existing mesh, batch meshing, and dirty CAD
- `references/mesh-quality-gates.md`: practical QA gates for meshing-first automation
