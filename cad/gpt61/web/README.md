# Models for the website author

`dart.glb`, `harness.glb`, `aircraft.glb` and `stake.glb` use metres, Y up and an eight-second animation named `explode`. Scrub from 0 (assembled) to 8 (exploded). Dart lies along +X; the stake model stands upright. All materials are embedded PBR colours, with no textures or external resources.

These models use the Seeed XIAO ESP32S3 + Wio-SX1262 kit. The kit FPC antenna envelopes, board mating spacing and actual masses remain MEASURE. Nothing has been printed, dropped or flown.

Human dimensions and masses are displayed in inches and ounces or pounds. The GLB format remains in metres. Machine-readable manifest field names and values remain unchanged: `mass_g` still records grams, and fields with metric unit suffixes retain those units. STEP/STL manufacturing exports stay in millimetres. Do not rescale model files to match display labels.

`manifest.json` contains file sizes, stored and instanced triangle counts, node names, display names, physical part functions, source references, material colours and model mass estimates. Loaded darts keep separately named nodes and share meshes. Servo and stock horn share a 0.32 oz catalog mass; their individual mass fields and all aircraft-part mass fields are null. Null means unavailable, never zero. Auxiliary stake parts are included in the stake model, not flight payload.

The animations illustrate service/explosion order. They do not simulate servo release, falls, flexures, threads, wires or continuous collision-free disassembly. Cut disposable ties and disconnect wires before moving the real pod. The stake clip withdraws its retained pod subassembly 3.94 in from the adapter. Source-detail parts remain grouped as physical purchased assemblies.

`validation-readback.json` checks named nodes, binary/accessor structure, normals, counts and every animation sample against source transforms; trimesh loads every file. `validation-khronos.json` contains full Khronos results. `exploded_checks.json` checks endpoint separation using CAD solids. Current assembled and variant checks are in `../out/checks.json`. `../out/visual_review.json` records inspection hashes for every final render.

Rebuild after the CAD build and independent export validator:

```powershell
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/web_export.py
```

Use `--render-only` to repeat exploded PNGs and `--no-render` for GLBs and validators only. All writes, including any npm validator installation/cache, stay under `cad/gpt 61/`.
