# Mesh Quality Gates

Treat these as practical default gates, not universal truth. Tighten or relax them based on the model and numerics.

## Hard fail checks

Fail the run immediately if any of these are true:

- `negative_cell_count > 0`
- a required boundary zone is missing
- a required cell zone is missing
- the meshing workflow reports an unrecoverable failure

## Default numeric gates

Use these as first-pass defaults:

- `max_skewness <= 0.95`
- `min_orthogonal_quality >= 0.10`
- `negative_cell_count == 0`

Prefer stronger gates when the model is sensitive:

- `max_skewness <= 0.90`
- `min_orthogonal_quality >= 0.15`

## Structural checks

Check these before solving:

- boundary and cell zone names are exactly what the solver workflow expects
- no unexpected merged zones broke the setup mapping
- cell count is within an expected band for the case
- inflation or boundary-layer expectations were met if the case depends on them

## Automation rule

Never advance to solver automation until the mesh summary passes all required checks.

Recommended pattern:

1. export a JSON mesh summary from the meshing workflow
2. run `evaluate_mesh_quality.py`
3. stop on failure with a machine-readable report
4. only launch the solver when the gate passes
