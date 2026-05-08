# wjc9011 COMSOL MCP Server

Reference for the most complete from-scratch automation path.

Upstream: https://github.com/wjc9011/COMSOL_Multiphysics_MCP

## When to prefer it

- end-to-end build from natural language
- boolean geometry, multiple physics, or coupled physics
- MPh's high-level API would force frequent drops to `model.java`

Skip when the model is validated and only needs sweeps/exports, or when the probe reports `recommendation` is NOT `mcp_server_ready`.

## Install (once per machine)

```bash
git clone --depth 1 --single-branch --branch main \
  https://github.com/wjc9011/COMSOL_Multiphysics_MCP.git
cd COMSOL_Multiphysics_MCP
python -m pip install -e .
```

Repo is ~491 MB (PDF knowledge base committed). Always shallow-clone.

Register in host MCP config (`~/.claude.json` or equivalent) under `mcpServers`:

```json
"comsol": {
  "type": "stdio",
  "command": "<absolute path to comsol-mcp executable>",
  "args": [],
  "env": {
    "JAVA_HOME": "<COMSOL_ROOT>/java/win64/jre",
    "HF_ENDPOINT": "https://hf-mirror.com",
    "HF_HOME": "D:\\huggingface_cache"
  }
}
```

Restart the host agent after editing. The probe script (`probe_comsol_env.py`) reports `recommendation: mcp_server_ready` when the setup is complete.

## Canonical call sequence

```
comsol_start
  -> model_create
  -> [geometry_add_*  ... -> geometry_boolean_*  -> geometry_build]
  -> [physics_add_* | multiphysics_add]
  -> physics_configure_boundary  (per-BC)
  -> physics_set_material
  -> mesh_create
  -> study_solve  |  study_solve_async + study_get_progress + study_wait
  -> results_evaluate  |  results_export_data  |  results_export_image
  -> model_save  |  model_save_version
```

## Tool catalogue summary

See `comsol-mcp-server-setup/references/tool-catalogue.md` for the full 80+ tool listing. Quick reference:

| Group | Count | Key tools |
|-------|-------|-----------|
| Session | 4 | `comsol_start`, `_connect`, `_disconnect`, `_status` |
| Model | 9 | `model_load`, `_create`, `_save`/`_save_version`, `_inspect` |
| Geometry | 14 | `geometry_add_block`/`_cylinder`/`_sphere`, `_boolean_union`/`_difference`, `_build` |
| Physics | 16 | `physics_add_heat_transfer`/`_laminar_flow`/`_electrostatics`/`_solid_mechanics`, `multiphysics_add` |
| Mesh | 3 | `mesh_create`, `_list`, `_info` (shallow — no size/distribution/swept-layers) |
| Study | 8 | `study_solve` (sync), `_solve_async` + `_get_progress` + `_wait` |
| Results | 9 | `results_evaluate`, `_global_evaluate`, `_export_data`/`_image` |
| Knowledge | 8 | `docs_get`/`_list`, `pdf_search`, `troubleshoot`, `modeling_best_practices` |

## Known limitations

- **One COMSOL client per Python process** (singleton). If a session goes bad, restart the MCP server process.
- **Mesh control is shallow** (3 tools, auto-mesh oriented). For mesh sequences with size, distribution, swept layers, or boundary-layer meshes, fall back to Java export (§3 in `runtime-modes.md`).
- **First pdf_search is slow**: sentence-transformers model download (~200 MB). Use `HF_HOME` pointing to a non-C-drive location and `HF_ENDPOINT` for mirrors.
