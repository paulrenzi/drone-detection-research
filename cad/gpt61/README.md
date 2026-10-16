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
