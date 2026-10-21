# Brief: tail fins, and renders that show why the dart falls point-down

Work in `cad/gpt61/` only. Do not edit anything else in the repo, and do not commit or push. This revises your XIAO package (`BRIEF-xiao.md`, `BRIEF-us-units.md`, `DESIGN.md`), so read those first. Every caption, label and document you write follows the unit rules in `BRIEF-us-units.md`: US units, trade names as sold, STEP/STL in mm, GLB in metres, json/csv keys unchanged.

## What is wrong now

Paul looked at the dart renders and could not tell how the dart is bottom-weighted, with what looks like a battery at the top, or what steers it so it comes down straight in wind. He is right on both counts:

- **Nothing shows the weight.** The 18650 sits in the body near the tip, and the balance point is 10.0 in from the tip of a 27 in dart. But no render marks the balance point, and the cell is hidden inside the body. The pod at the top looks like the heavy part.
- **Nothing steers it.** The dart is carried flat, hung at its balance point, so it leaves the drone level and must turn nose-down on its own. It has no fins. Its only tail drag is the small XIAO pod and the antenna strip, which is less than the old Heltec pod gave it. `build-3d.md` already admits the model "checks a clear path out, not the fall".

## What to do

1. **Add tail fins** at the top end of the dart, so the centre of pressure sits well behind the centre of mass, as on a lawn dart or a shuttlecock. Choose the count, planform, span and position yourself (on the pod, or a separate printed collar on the rod just below it), and say why.
   - Estimate the centre of pressure with a stated, simple method (projected side area, or Barrowman-style, for the rod, body, pod, antenna strip and fins). Report the static margin as the distance from the centre of mass to the centre of pressure, in inches and in body widths, before and after the fins. Say what margin you aimed for and why.
   - The fins must stay clear in every existing check: carried, mid-release and released, against the frame, rails, prop sweeps, skids, the harness, the ground and the other three darts. They must pass the release gaps, must not cover the mic port, the USB cap or the antenna strip, and must print flat in PETG without supports. If they cannot fit at full size, say what you gave up.
   - Re-solve the mass and balance with the fins on: the hanger post moves to the new balance point, and the dummy's ballast is recomputed to match the new dart. Report the new dart mass, balance point and four-dart payload.
2. **Say whether flat carriage is still right.** Compare hanging at the balance point, as now, with hanging slightly ahead of it so the dart leaves already tilted nose-down. Give the trade-off (clearance under the drone, release friction, how soon it turns). Change the carriage only if every check still passes, and say what you chose.
3. **Wind.** A finned dart points along the air it falls through, not straight down, so it lands tilted into the wind. Tabulate the landing tilt for drops of 16, 33 and 49 ft in winds of 5, 10 and 15 mph, ignoring drag (tilt ≈ atan(wind / impact speed)), and say how drag would change it. State plainly that this is an estimate, not a test.
4. **New renders**, all labelled in US units, added to `REVIEW.html` and inspected like the rest:
   - `dart_balance.png`: a side view with the balance point, the centre of pressure before and after the fins, and the cell highlighted inside a cut-away body, each labelled with its distance from the tip.
   - `dart_fins_detail.png`: a close view of the fins and how they attach.
   - `dart_fall_sequence.png`: the dart drawn at four moments of a fall, leaving flat, turning, nose-down in still air, and tilted into a 10 mph wind. A schematic is fine, as long as it is labelled as one and not as a simulation.
   - Re-render every existing view the fins appear in.
5. **Update everything else that depends on the dart:** `DESIGN.md` (a new section on the fins, the balance, the margin and the wind table, with every caveat), `README.md`, the print table and print kit (new or changed STLs), the STEP assemblies, `web/dart.glb`, `web/harness.glb`, `web/aircraft.glb` and `web/manifest.json` (keep every key, including `mass_g`; new part nodes get names), and the checks. Rerun the validators, `record_visual_review.py --reviewed` after you have looked at every new PNG, and the packaging.

## Do not claim

Nothing here has been printed, dropped or flown. Do not write that the dart lands upright, self-rights or survives a drop. Write what the estimate says and that the dummy drop test is what will tell.

## Done when

The fins are modelled and clear every check, mass and balance are re-solved with the dummy matched, the three new renders and the updated ones are inspected, the documents and web models are current, and every check passes. Finish with a short report: the fin design, the margin before and after, the new masses and balance point, the carriage decision, the wind table, the check count, and anything you could not do.
