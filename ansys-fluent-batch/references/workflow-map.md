# Fluent Workflow Map

Use this decision map before writing automation.

## 1. Existing mesh or case already available

Choose this route when the user already has one of:

- `.msh`
- `.cas`
- `.cas.h5`
- a validated Workbench-to-Fluent pipeline

Preferred action:

- automate the solver first
- leave meshing unchanged
- export numeric reports, residuals, and monitors

## 2. Clean, parameterized geometry and stable topology

Choose this route when:

- the geometry is already cleaned
- boundary names are stable
- topology does not change unpredictably
- the user expects repeated remeshing

Preferred action:

- automate meshing in batch mode
- write mesh summary files
- run a quality gate before solving

Useful template references when ANSYS is installed locally:

- `%ANSYS_ROOT%\aisol\CommonFiles\Utilities\Meshing\CutCellMeshingWithFluentTemplate.jou`
- `%ANSYS_ROOT%\aisol\CommonFiles\Utilities\Meshing\TGAutoMeshingWithFluentTemplate.jou`

## 3. Dirty CAD, leaking geometry, or unstable topology

Choose this route when:

- imported CAD is not watertight
- zone names or face groups change between runs
- topology changes enough to invalidate downstream assumptions

Preferred action:

- do not start with full automation
- repair and baseline the geometry interactively first
- confirm one clean batch meshing pass
- only then wrap it in journals or API calls

## 4. Closed-loop optimization

Use this order:

1. fixed mesh, vary solver-side parameters
2. fixed meshing workflow, vary geometry parameters cautiously
3. full geometry-plus-mesh loop only after repeated stable passes

Do not unlock geometry changes on day one unless the user already has a robust remeshing baseline.
