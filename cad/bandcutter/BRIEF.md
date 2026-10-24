# Brief: the band cutter, as a real 3D model with an animated exploded view

Work in `cad/bandcutter/` only. Do not edit anything else in the repo, and do not commit or push.

## What this is

A countermeasure against fibre-optic FPV drones. These drones pay out a glass fibre (0.25 mm coated,
0.125 mm glass) from a spool they carry, so the fibre drops onto whatever lies under the drone's path.
The band cutter is a hand-built line of posts, about 32 in high, that cuts any fibre lying across it.
The project's cost and speed model is `tools/bandmodel/band_model.py`: read its docstring and
constants first, then `countermeasures/fibre-cutter.md` and `countermeasures/index.md` for context.

## The concept (fixed; solve problems inside it and write down what you changed and why)

- **Posts:** standard 5.5 ft studded steel T-posts with anchor plates, driven 2 ft into the soil with
  a manual post driver, one every 33 ft. Each post carries a **printed head** that slides down over
  the post's top and is locked by one stainless worm-gear hose clamp. The T-post's flanged profile
  stops the head turning under motor torque, and its studs stop it sliding. The two end posts are
  guyed to spiral earth anchors (off the shelf, the dog tie-out kind) against the strap tension.
- **The band:** one closed loop per span of **1/2 in × 0.028 in polyester (PET) pallet strapping**
  (smooth, 800 lb break, sold in 6,500 ft coils), closed with a standard 1/2 in steel crimp seal.
  Each loop runs on one pulley at each of its two posts, in an **upright plane along the line**:
  pulley axles are horizontal and square to the line, the top run is about 32 in above the ground
  and the return run sits under it. Pretension about 5 lb, set by a take-up on the idler.
- **The hooks:** small printed hooks, one every 12 in, each fixed to the strap's outside face with
  one 1/8 in aluminium pop rivet. The hook leans forward, its mouth facing the direction the strap
  moves, so a fibre lying across the top run is caught in the crotch between hook and strap and
  carried along. Because the strap is flat, the hooks always point outward: up on the top run, down
  on the return. Hooks must pass round the pulleys and through the cutter without catching. Design
  the hook shape (how it catches the fibre and how it keeps it) and show it in a detail render.
- **Drive posts and idler posts alternate.** A drive post's head carries one **JGB37-3530 12 V,
  107 rpm** gearmotor (37 mm gearbox, 6 mm D-shaft) turning one horizontal shaft in two 608 bearings,
  with a pulley on each side of the post: one for the span to the left, one for the span to the right.
  The pulleys are about 6 in pitch diameter, crowned for a flat belt, with a rubber tread (e.g. a
  strip of bicycle inner tube) for grip in wet. An idler post's head carries two free pulleys on 608
  bearings, one per span, and the take-up that sets each loop's tension.
- **The cutter:** at the post where each top run arrives, two standard trapezoid utility blades
  stand one either side of the strap's path, edges facing the incoming strap, in a printed holder,
  replaceable without tools. The strap and its hooks pass between them. A fibre carried by a hook
  hangs down over both sides of the strap, so its two sides are drawn onto the blade edges while
  the hook keeps pulling, and it is cut. The gap must let strap and hook through and must not let a
  fibre slip past uncut. Because one shaft drives both spans, one span's top run moves toward its
  drive post and the other's away from it: put each cutter wherever its top run arrives.
- **Power and control, drive posts only:** a 12 V 5 W solar panel on a printed or bent bracket at the
  top of the head, tilted low (matte, to limit glint); a 12 V 1.2 Ah sealed lead-acid battery
  (Yuasa NP1.2-12 size); a small solar charge controller; an ESP32-C3 SuperMini, an Ai-Thinker
  Ra-01H LoRa module and a wire antenna; a MOSFET driver and fuse; all in an off-the-shelf IP65
  junction box about 4 × 3 × 2 in with cable glands, mounted on the head.

Look up the real dimensions of every bought part (T-post profile and studs, hose clamp, PET strap,
crimp seal, pop rivet, utility blade, 608 bearing, JGB37-3530 gearmotor, 5 W panel, NP1.2-12,
junction box, SuperMini, Ra-01H) from datasheets, listings or published CAD, and cite each. Where
something can't be found, mark it MEASURE and make it one parameter.

## What to deliver

1. **Bought parts as real models** at real dimensions, and **printed parts modelled properly**: walls
   for a 0.4 mm nozzle in PETG or ASA (outdoor, UV), fillets, ribs where loads go, FDM clearances,
   bearing seats, the shaft-to-pulley drive, the head-to-T-post fit, the blade holder, the
   take-up, cable routing into the box, drain holes, and a print orientation with minimal supports
   for each printed part. STEP and STL of every printed part to `out/`.
2. **Assemblies:** a drive post, an idler post, and one **span**: a drive post and an idler post with
   the loop, hooks and cutter between them. A real 33 ft span is long against 6 in parts, so show it
   shortened and say so. Check for interference: hooks against pulleys and blades, strap against
   the head, the box and panel against the strap.
3. **Mass properties** of each head and post, printed parts at the infill you recommend.
4. **Exploded views and web models,** exactly as was done for the dart in `cad/gpt61/`: read
   `cad/gpt61/BRIEF-exploded.md`, `cad/gpt61/web_export.py`, `cad/gpt61/web/manifest.json` and
   `assets/js/cad-viewer.js`. Deliver in `web/`:
   - `drive_post.glb`, `idler_post.glb` and `span.glb`, each one file with an 8-second glTF animation
     named `explode` moving every part from assembled (t = 0) to exploded along the direction it is
     actually assembled, in assembly order, with no overlaps in the exploded state;
   - one node per part, named; metres, Y up; PBR colours that tell printed from bought parts;
     each ≤ 8 MB; read back and run through the Khronos glTF validator (`npx gltf-validator`);
   - `web/manifest.json` in the same schema as `cad/gpt61/web/manifest.json`, so the existing
     viewer reads it unchanged: per part, its node name, display name, printed or bought, mass,
     geometry source and one plain sentence on what it does. Unmeasured things stay flagged.
5. **Renders** to `renders/`: each assembly, each exploded view, the hook on the strap catching a
   fibre (draw the fibre), the cutter with a hook passing through, the head on the T-post, and each
   printed part in its print orientation. **Look at every render yourself** and fix anything crude,
   wrong or unclear before you finish.
6. **`DESIGN.md`:** sources, every change to the concept and why, key dimensions and clearances,
   masses, open MEASURE items, print settings, and assembly steps. **US customary units** (in, ft,
   oz, lb, °F) in every caption and document; files and internal geometry may stay metric.
7. **One script that regenerates all of it,** runnable from the repo root with the interpreter below.

## Environment

- Windows 11. Python with CadQuery 2.8, OCP, numpy and trimesh: `C:\Users\paulm\.venvs\cad\Scripts\python.exe`.
  You may `pip install` into it (e.g. `pygltflib`). `cad/gpt61/` has working render and export code you
  may copy into `cad/bandcutter/` and adapt; do not modify `cad/gpt61/`.
- Use the web for datasheets and CAD files, and cite them.
- Take as long as you need: run your scripts, read the numbers, look at the renders, iterate.

## Done means

Three valid `.glb` files with named nodes and the `explode` clip, `web/manifest.json`, the renders
you have looked at, STEP/STL of the printed parts, `DESIGN.md`, the regenerating script, and a final
message listing what you made, file sizes, validator output, and anything you could not do.
