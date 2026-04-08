---
name: comsol-electrochem-fluid
description: Use when the user wants to build, adapt, troubleshoot, benchmark, or automate COMSOL models involving electrochemistry, batteries, corrosion, electrodeposition, electrolyzers, fuel cells, fluid flow, microfluidics, porous flow, pipe flow, nonisothermal flow, or electrochemistry-flow couplings on this Windows machine. This skill navigates the local COMSOL Application Library under F:\comsol\COMSOL63\Multiphysics\applications, shortlists relevant .mph examples, maps the problem to the right interface/coupling family, and points to automation through COMSOL Java export and the local toolkit at D:\VScode file\comsol.
---

# COMSOL Electrochem Fluid

## Quick Start

1. Classify the user's problem on four axes:
   - electrochemistry fidelity: current distribution only, species transport, double layer, porous electrode, battery/fuel cell
   - flow regime: none, laminar, turbulent, microfluidic, porous, pipe, multiphase
   - coupling: heat, species, deformation, two-phase, porous transport
   - geometry scale: 1D, 2D, axisymmetric, 3D
2. Use `scripts/find_examples.py` to shortlist local `.mph` examples from the COMSOL Application Library.
3. Read [references/case-map.md](references/case-map.md) for curated example families and [references/modeling-patterns.md](references/modeling-patterns.md) for interface and coupling choices.
4. Prefer adapting the closest existing `.mph` example before rebuilding from scratch.
5. If the user wants automation, export the chosen model to Java from COMSOL Desktop and integrate it with the local toolkit in `D:\VScode file\comsol`.

## Workflow

### 1. Shortlist examples

Run the bundled search script first.

Common commands:

```powershell
python "C:\Users\fff\.codex\skills\comsol-electrochem-fluid\scripts\find_examples.py"
python "C:\Users\fff\.codex\skills\comsol-electrochem-fluid\scripts\find_examples.py" --keyword electrolyzer --keyword pem
python "C:\Users\fff\.codex\skills\comsol-electrochem-fluid\scripts\find_examples.py" --module Electrochemistry_Module --module CFD_Module --keyword bubbly
python "C:\Users\fff\.codex\skills\comsol-electrochem-fluid\scripts\find_examples.py" --module Corrosion_Module --keyword localized
```

Default search scope already includes the most relevant modules:

- `Electrochemistry_Module`
- `Fuel_Cell_and_Electrolyzer_Module`
- `Electrodeposition_Module`
- `Corrosion_Module`
- `Battery_Design_Module`
- `CFD_Module`
- `Microfluidics_Module`
- `Porous_Media_Flow_Module`
- `Pipe_Flow_Module`
- `COMSOL_Multiphysics`

By default the script skips `*_geom_sequence.mph` because those are geometry-helper models, not the main study model.

### 2. Choose the closest modeling family

Use these families as the first-pass decision tree:

- electroanalysis and basic electrochemistry:
  use `cyclic_voltammetry`, `microdisk_voltammetry`, `impedance_spectroscopy`, `diffuse_double_layer`
- electrochemistry plus transport or separation:
  use `electrodialysis`, `capacitive_deionization`, `chlor_alkali`, `isoelectric_focusing`, `zone_electrophoresis`
- electrolyzers and fuel cells:
  use `alkaline_electrolyzer`, `pem_electrolyzer`, `soec`, `nonisothermal_pem_fuel_cell`, `two_phase_pemfc`, `pemfc_serpentine_flow_field`
- electrodeposition and plating:
  use `decorative_plating`, `electroplating_rack`, `pcb_designer`, `cu_electrowinning_bubbly_flow`, `cu_deposition_trench`
- corrosion:
  use `atmospheric_corrosion`, `galvanic_corrosion_mg_alloy`, `pitting_corrosion`, `localized_corrosion`, `pipeline_corrosion_protection_iccp`
- pure or supporting flow:
  use `backstep`, `turbulent_mixing`, `heat_sink`, `electrokinetic_valve`, `electroosmotic_mixer`, `convection_porous_medium`, `heat_exchanger_plate`

### 3. Reuse examples deliberately

- Keep the example if the user's geometry and physics are close; only swap geometry, parameters, materials, and BCs.
- Combine a domain example and a coupling example when one example is too narrow.
- Prefer lower-dimensional examples first when the user is still deciding on governing physics.
- Move to 3D only after the 1D or 2D physics closes and converges.

### 4. Move to automation when needed

For automation tasks, use the installed COMSOL docs plus the local toolkit:

- COMSOL root: `F:\comsol\COMSOL63\Multiphysics`
- Java API guide: `F:\comsol\COMSOL63\Multiphysics\doc\pdf\COMSOL_Multiphysics\ApplicationProgrammingGuide.pdf`
- Programming reference: `F:\comsol\COMSOL63\Multiphysics\doc\pdf\COMSOL_Multiphysics\COMSOL_ProgrammingReferenceManual.pdf`
- Java API HTML: `F:\comsol\COMSOL63\Multiphysics\doc\help\wtpwebapps\ROOT\doc\com.comsol.help.comsol\api\com\comsol\model\util\ModelUtil.html`
- Local automation toolkit: `D:\VScode file\comsol`

Recommended automation path:

1. Open the closest `.mph` example in COMSOL Desktop.
2. Verify interfaces, couplings, study steps, materials, and solver settings.
3. Export the model to Java.
4. Fold the generated Java into the local automation pipeline instead of hand-writing the full API from scratch.
5. For existing `.mph` sweeps, prefer batch mode on the `.mph` directly.

## References

- Read [references/case-map.md](references/case-map.md) for curated examples and where each family is useful.
- Read [references/modeling-patterns.md](references/modeling-patterns.md) for interface selection and coupling heuristics.

