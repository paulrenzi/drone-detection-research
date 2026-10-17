# Brief 2: exploded views and web-viewable 3D models

Work in `cad/gpt61/` only. Do not edit anything else in the repo, and do not commit or push.

## Context

You built this package in the previous run: read `DESIGN.md`, `README.md`, `build.py`, `printed.py`, `purchased.py` and `parameters.py` first. The geometry is settled for now. **Do not change any part's geometry, dimensions or the concept.** This run adds two things on top of it.

The project owner wants a page on the project's website (GitHub Pages, Jekyll) with a 3D viewer where a visitor can rotate each model and switch between it assembled and exploded. Someone else will write the page. Your job is the models and the facts the page's text will be written from.

## What to deliver

1. **Exploded views** of:
   - **one dart:** every part, printed and bought: rod, body, pod shell, pod lid, Heltec V3, INMP441, 18650 cell, antenna, and any fasteners, snaps or wiring you modelled;
   - **the harness:** plate, rotor, SG90 and its horn, zip ties if modelled, with the four darts' hanger heads in place or the darts drawn as single grouped bodies;
   - **the whole carried assembly** under the X500: drone, harness and four darts, with the harness and darts exploded downward away from the airframe.

   Explode each part along the direction it is actually assembled or removed, in assembly order, far enough apart that every part is clearly visible and nothing overlaps in the exploded state, but close enough that you can still see where each one goes. Check the exploded states for overlap the same way you checked the assembled ones.

2. **PNG renders of each exploded view,** in `renders/`, alongside the existing ones. Look at every one yourself and fix the explode distances until each reads clearly.

3. **glTF binary (`.glb`) files for the web,** in a new folder `web/`:
   - `dart` — one dart, carried (lying) orientation or upright, your call; say which;
   - `harness` — the harness with four darts loaded;
   - `aircraft` — the X500 with the harness and four darts (carried state).

   For each of the three, deliver **one `.glb` with both states**, preferably as a single glTF animation clip named `explode` that moves every part from its assembled position (t = 0) to its exploded position (end of clip) using node translations, so a viewer can scrub between them. If you can't produce a valid animation, deliver a separate `<name>-assembled.glb` and `<name>-exploded.glb` instead and say why.

   Requirements:
   - one glTF node per part, named with the part's name from `DESIGN.md` (e.g. `pod_shell`, `heltec_v3`), so the page can name parts on hover;
   - units in **metres**, **Y up** (glTF convention), origin at a sensible centre;
   - colours that tell printed parts from bought parts, matching the existing renders where possible; PBR materials (`baseColorFactor`, `metallicFactor`, `roughnessFactor`), no textures needed;
   - **size budget: `dart` and `harness` ≤ 8 MB each, `aircraft` ≤ 20 MB.** The X500 and Heltec source models are huge; decimate or re-tessellate them for the web copy (coarser tessellation of the STEP is fine) and drop internal detail nobody can see. The printed parts should keep enough detail that snaps, ribs and channels are visible. Keep the full-resolution STEP/STL in `out/` untouched;
   - each `.glb` must load cleanly: validate it by reading it back (e.g. with `trimesh` or `pygltflib`), and if the Khronos `gltf-validator` is available or installable via npm, run it and report errors and warnings.

4. **`web/manifest.json`**: for each model, the file name, file size, triangle count, whether it carries the `explode` animation and its duration, and per part: node name, display name, printed or bought, material/colour, mass in grams (from your mass properties), the source of its geometry (manufacturer STEP, datasheet, or modelled by you), and one plain sentence on what the part does. This is what the page's reference text will be written from, so it must be accurate and must not overstate anything. Anything unmeasured stays flagged as unmeasured.

5. **A script that regenerates all of it** (e.g. `web_export.py`, plus whatever exploded-view code you add), runnable from the repo root with the same interpreter, and a short new section in `DESIGN.md` and `README.md` describing the exploded views and the `web/` files.

## Environment

- Python with CadQuery 2.8, OCP 7.9, numpy and trimesh: `C:\Users\paulm\.venvs\cad\Scripts\python.exe`. You may `pip install` into that venv (e.g. `pygltflib`) if you need to.
- The full-resolution assembly STEPs are in `out/` (244 MB each); regenerate anything you need with `build.py`.
- Write only inside `cad/gpt61/`.

## Done means

- three `.glb` files in `web/` within budget, each loads, each has named part nodes, and each either animates assembled→exploded or has its assembled/exploded pair;
- exploded renders in `renders/` that you have looked at;
- `web/manifest.json` complete;
- a final message listing what you made, file sizes, any validator output, and anything you could not do.
