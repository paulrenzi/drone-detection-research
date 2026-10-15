# cad/

CadQuery models for the tripwire hardware. Write-up: `build-hardware.md`.

```
python -m venv cad-env && cad-env/Scripts/pip install cadquery
cd cad
python dart.py      # dart parts, mass, stowed size, renders
python harness.py   # X500 harness, dart-clearance check, renders (imports dart)
python quad.py      # TL-1 printed quad, flight-time table, render (imports dart, harness)
```

- `params.py` holds every bought-part dimension with its source; `MEASURE` marks numbers to check with calipers.
- `out/` gets STL (slice these) and STEP (open in any CAD tool).
- Renders go to `../assets/images/build/` via `render.py` (VTK, headless).
- Print in PETG on the Vyper (open frame). Body tip-up, cap deck-down, pod upright, arms flat.
