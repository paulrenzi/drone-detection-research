# XIAO listener mechanical prototype

Open [REVIEW.html](REVIEW.html) for the current render gallery and [DESIGN.md](DESIGN.md) for sources, dimensions, masses, print settings and assembly. The listener uses the owned Seeed XIAO ESP32S3 + Wio-SX1262 kit, INMP441 breakout, one18650 cell and6 x500 mm fibreglass rod. The mic port is500 mm above soil.

Included: the one-servo four-dart X500 harness, adjustable8–13 mm stake adapter and cell holder, and an inert dummy with four ballast portions matching the model's mass and XYZ balance. Nothing has been printed, dropped or flown. Antenna envelopes, B2B spacing, actual weights and manufacturing fits remain MEASURE.

Run from the repository root using the CAD interpreter:

```powershell
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/fetch_sources.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/fetch_xiao.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/build.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/validate_exports.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/web_export.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/document.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/record_visual_review.py --reviewed
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/validate_package.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/package.py
```

Inspect every newly generated PNG before running `record_visual_review.py --reviewed`; it records your inspection and cannot inspect images itself. All writes stay here. `parameters.py`, `printed.py`, `purchased.py` and `variants.py` are geometry/mass sources. Cache flags are documented in DESIGN.md.

`out/` contains12 printed STEP/STL pairs, current assembly STEP files, bought-part references, print manifest, mass tables, checks, independent export validation and print-kit.zip. STLs are onZ0 in their intended Vyper orientations. Recommended infill is intentionally100%, including the plate; lightening pockets and tower voids are CAD geometry.

`web/` contains dart.glb, harness.glb, aircraft.glb and stake.glb with an8-second `explode` clip, metres andY up. Named nodes and source/mass/uncertainty facts are in [web/manifest.json](web/manifest.json). The stake clip lifts the retained pod from its adapter. These are presentation animations, not physical release simulations. Validators check binary/accessor round trips, trimesh loading, endpoint overlaps and Khronos glTF compliance.
