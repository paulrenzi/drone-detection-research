# Brief: US units in every render and in the design notes

Work in `cad/gpt61/` only. Do not edit anything else in the repo, and do not commit or push. This revises your own XIAO package from earlier today (`BRIEF-xiao.md`, `DESIGN.md`, `LAST_MESSAGE-xiao.md`), so read those first.

## What is wrong now

The site this package feeds (trip/wire) now uses US customary units everywhere: inches, feet, yards and miles for length; ounces and pounds for mass; mph for speed; °F for temperature. Every page and the field app were converted. Your package is the last place still in metric. The render titles, subtitles and callout labels say things like "686 mm overall | mic 500 mm above soil", "36.82 g total steel ballast" and "16.8 mm throat", and `DESIGN.md` is written entirely in mm and g.

There are also typography faults to fix while you are in there: missing spaces between numbers and words, such as "46 x32 mm", "to500 mm", "nominal10 mm OD, clamp8-13 mm", "mic500 mm", "same18650", "PETG,0.4 mm nozzle,0.2 mm layers,100% infill".

## What to do

1. **Re-render every PNG in `renders/`** (all 33) with every caption, title, subtitle and callout in US units. Do not change any geometry, camera or colour; only the text changes.
2. **Rewrite `DESIGN.md`, `README.md`, `web/README.md` and the human-readable text of `REVIEW.html` and `out/checks.md`** in US units. Keep the content and every caveat; change the units and fix the typography.
3. **Unit rules:**
   - Length in decimal inches. Use 0.01 in for most dimensions, and 0.001 in for clearances, tolerances, film and wall thicknesses under 0.1 in, so no fit information is lost. Use feet for lengths over about 3 ft only where it reads better (the 48 in stake stays 48 in).
   - Mass in ounces to 0.01 oz; pounds for totals over 1 lb (for example, 1.71 lb).
   - Density in lb/in³ for PETG and steel, with the g/cm³ value it came from in parentheses, since filament makers quote g/cm³.
   - Torque in oz·in; force in lbf; temperature in °F; volume in in³.
   - Angles stay in degrees.
   - **Trade names and part numbers stay exactly as sold**: M2, M2x6, M2x8, M3, RX-M2x4, 18650, INR18650-25R, SG90, T18R, DIN934. Metric screw and insert sizes are names, not measurements. Nozzle size and layer height are sold and set in mm, so give those as "0.4 mm nozzle (0.016 in)" and "0.20 mm layers (0.008 in)".
   - When a source quotes a metric value, give the inch value, with the source's metric figure in parentheses the first time it appears in the source register only, so a reader can check it against the datasheet. Nowhere else.
4. **Do not change these, and say so in `DESIGN.md`:**
   - STEP and STL files stay in millimetres. Slicers read STL as mm, so rescaling would break printing.
   - GLB files stay in metres (the glTF standard).
   - Machine-readable data (`*.json`, `*.csv`) keep their field names and values, because the website reads them. In particular, do not rename `mass_g` or any other key in `web/manifest.json`. You may convert free-text description strings in it to US units.
   - `parameters.py` and the build code stay in mm internally. Add a conversion helper for the captions rather than changing the model's units.
5. **Inspect every regenerated PNG** at full size before running `record_visual_review.py --reviewed`. Check that every label is in US units, nothing is cropped or overlapping, and the numbers match the model.
6. Re-run the validators and packaging so `checks.json`, `export_validation.json`, `visual_review.json`, `receipt.json` and `print-kit.zip` are current, and confirm all checks still pass. The geometry has not changed, so every check result should be the same as this morning's.

## Done when

All 33 renders and the four documents above are in US units with the typography fixed, every check passes, and the print kit is rebuilt. Finish with a short report: what changed, the check count, and anything you could not convert.
