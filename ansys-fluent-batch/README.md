# ansys-fluent-batch

Use when the user wants to automate ANSYS Fluent on this Windows machine, especially for headless meshing, mesh quality gating, batch solver runs, existing `.msh`, `.cas`, or `.cas.h5` workflows, Fluent journal (`.jou`) orchestration, or AI closed-loop optimization around Fluent. Prefer this skill when meshing reliability, named zone stability, Watertight Geometry, fault-tolerant meshing, or mesh QA are material risks and avoid treating Fluent as a single-step solver launch.

## Portable Entry Point

- Start here if you are using this repository from a non-Codex agent.
- The original Codex-oriented source remains in `SKILL.md` for reference.
- Run bundled scripts relative to this folder, for example `./ansys-fluent-batch/scripts/...` from the repo root.

## Adapted Instructions

# ANSYS Fluent Batch

Use this skill to treat Fluent as a meshing-plus-solver pipeline, not a one-line solver launch. Split the work into:

1. workspace setup
2. headless meshing or solver launch
3. mesh quality gate
4. optimization loop

Prefer this over ad hoc GUI operation when the user wants repeatable meshing, stable zones, batch journals, or closed-loop iteration.

## Environment

Prefer `FLUENT_EXE` or `ANSYS_ROOT` when available. Example machine-local locations on Windows often look like:

- Fluent launcher: `%ANSYS_ROOT%\fluent\ntbin\win64\fluent.exe`
- Embedded PyFluent Python: `%ANSYS_ROOT%\commonfiles\CPython\3_10\winx64\Release\python\python.exe`
- Local Workbench meshing journals:
  - `%ANSYS_ROOT%\aisol\CommonFiles\Utilities\Meshing\CutCellMeshingWithFluentTemplate.jou`
  - `%ANSYS_ROOT%\aisol\CommonFiles\Utilities\Meshing\TGAutoMeshingWithFluentTemplate.jou`

Keep `-g` in batch runs unless the user explicitly needs UI interaction.

## Quick Start

Scaffold a Fluent workspace first:

```powershell
python "<repo-root>\ansys-fluent-batch\scripts\bootstrap_workspace.py" `
  --dest "<workspace-root>\fluent"
```

Run a headless journal through `fluent.exe`:

```powershell
python "<repo-root>\ansys-fluent-batch\scripts\run_fluent_journal.py" `
  --config "<workspace-root>\fluent\config\fluent_batch_config.example.json"
```

Evaluate a mesh summary against numeric gates:

```powershell
python "<repo-root>\ansys-fluent-batch\scripts\evaluate_mesh_quality.py" `
  --gate "<workspace-root>\fluent\config\mesh_quality_gate.example.json" `
  --summary "<workspace-root>\fluent\reports\mesh_summary.json"
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

## Resource Map

### Scripts
- `scripts/bootstrap_workspace.py`
- `scripts/evaluate_mesh_quality.py`
- `scripts/fluent_common.py`
- `scripts/run_fluent_journal.py`

### References
- `references/mesh-quality-gates.md`
- `references/workflow-map.md`

### Assets
- `assets/fluent_batch_config.example.json`
- `assets/mesh_quality_gate.example.json`
- `assets/mesh_summary.example.json`

## Portability Notes

- Use repository-relative paths or set SKILLS_ROOT instead of relying on a Codex-specific install path.
- Review Windows absolute paths before running. Replace them with local paths or environment variables.
- This skill assumes Windows-native tools. Validate tool availability before use on other systems.

## Source

- Original skill definition: `SKILL.md`
