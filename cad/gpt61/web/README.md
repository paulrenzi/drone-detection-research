# Models for the website author

`dart.glb`, `harness.glb` and `aircraft.glb` each contain both states in the single animation clip **explode**, duration **8 seconds**. Clamp and scrub it: 0 is assembled, 8 is exploded. Units are **metres**, **Y up**. The dart long axis is **+X**, horizontal in carried orientation. There are no textures, external resources, compression extensions or separate state files. PBR materials are embedded.

`manifest.json` is the reference for page text and hover labels. `models.<name>.parts[]` records each node's `node_name`, canonical `part_name`, `display_name`, printed/bought classification, source, one-sentence function, PBR colours, estimated `mass_g`, its basis, and uncertainties. Loaded models prefix dart nodes with `dart1_` through `dart4_`; meshes are shared but each part is independently named. A node can have several material primitives, especially a populated board. Pick the mesh node's name rather than assuming one primitive is one part. `triangle_count` includes all mesh instances; `unique_mesh_triangle_count` counts stored meshes once.

All masses are CAD estimates or catalog figures. A `null` mass means **unmeasured/unavailable**, never zero. Servo and supplied horn have a shared catalog mass of 9 g, with no separately defensible split. The aircraft has no established mass breakdown. The manifest's payload estimate excludes the existing aircraft, flight battery and avionics. Treat the listed totals as approximate model results, not a measured flight payload.

The physical prototype has not been printed, dropped, flown or acoustically/waterproof qualified. The antenna envelope, generic mic breakout, servo variant, OLED stack, print fits and other `MEASURE` items require verification. Prop swept slabs are clearance proxies, not blade models. The clip is a staged assembly diagram: unscrewing, flexible cable routing, snap deformation, cutting closed ties and heating inserts are not simulated. Factory-welded tabs and heat-set inserts are shown apart for identification, not as routine service-removable pieces. The real servo release sequence is described in `../DESIGN.md` and is different from this presentation clip.

The independent exploded endpoint solids are checked in `exploded_checks.json`; original assembled checks are in `../out/checks.json`. `validation-readback.json` checks binary structure, every named node, normals, triangle counts, and animation samples against the source transforms; trimesh also reads each file. `validation-khronos.json` contains full validator messages, including informational messages. `provenance.json` confirms the protected geometry and full-resolution outputs were not modified. `visual_review.json` records the inspection of all five final PNGs by their hashes, plus manifest mass-total checks; it is an inspection receipt, not an automatically renewed physical qualification.

Regenerate from the repository root:

```powershell
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/web_export.py
```

The script writes only in `cad/gpt61/`. It requires the existing B-rep cache and mass report; generate those with the original package workflow if absent. It uses CadQuery, numpy, trimesh and VTK already present in the CAD venv. Node/npm supplies the optional Khronos validator, locally installed and cached under `../tmp/`. `--no-install` skips installing it; `--no-render` skips PNG generation, and `--render-only` repeats only the PNGs. Neither option modifies full-resolution CAD.
