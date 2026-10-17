# First-print mechanical package

Start with [REVIEW.html](REVIEW.html) for the render gallery and [DESIGN.md](DESIGN.md) for sources, fits, masses, open measurements, print settings and assembly.

`out/` holds print-oriented STL files, design-datum STEP parts, all three full-aircraft assembly states, bought-part CAD and generated check/mass reports. The generic mic breakout, exact servo/board revisions, antenna and printed fits remain measurement items; this package has not been physically printed, dropped or flown.

Rebuild from the repository root:

```powershell
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/build.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/validate_exports.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/document.py
```

All scripts write only here. `fetch_sources.py` downloads the original reference files and records their hashes. CAD source geometry is preserved in `sources/`; `cache/`, `tmp/` and the optional local PDF-reader dependency are generated working files.

## Exploded views and web models

Run from the repository root with the same CAD interpreter:

```powershell
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/web_export.py
```

[web/manifest.json](web/manifest.json) describes [dart.glb](web/dart.glb), [harness.glb](web/harness.glb) and [aircraft.glb](web/aircraft.glb), including named parts, model mass estimates, geometry sources, colours and unresolved measurements. Each model contains an eight-second `explode` translation animation: time zero is assembled and time eight is exploded. Units are metres, Y up; the dart lies along +X in its carried orientation. The loaded models keep every dart part addressable and share meshes to reduce download size.

The five new `renders/*_exploded*.png` images include whole-model views and pod/harness details. [DESIGN.md](DESIGN.md#exploded-views-and-web-export) explains the service axes and the presentation limits. [web/README.md](web/README.md) describes the files for the website author. Validation reports are in `web/`; the original geometry and everything in `out/` remain unchanged. `--render-only` repeats the PNG renders, and `--no-render` repeats the exports and checks. The script uses local Node/npm to install the Khronos validator under `tmp/` if needed; `--no-install` disables that installation.
