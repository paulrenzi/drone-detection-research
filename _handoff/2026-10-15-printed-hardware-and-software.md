# Handoff: 3D-printed hardware and software, the missing half

Written at `HEAD: 93b634d` (2026-10-15). It supersedes nothing: the three earlier 2026-10-15
handoffs are done. `_handoff/` is not published by Jekyll.

## Repo rules (unchanged)

- All work in this repo (`C:\Users\paulm\drone-detection-research`), never umbrella-arcades.
- Before starting, run `git pull --ff-only`.
- Add files by explicit path, never `git add -A`.
- Commit with `git commit -F -` and a quoted heredoc.
- Edit with Write/Edit, never `open(p,"w")`.
- Every factual claim is sourced, or labelled as an inference or estimate.
- Write in plain, dense prose with no filler. Paul asked for this repeatedly.
- Add a newest-first row to `changelog.md` for each change.
- Verify by rendering the live page with `?cb=<sha>` once the Pages build finishes, never by an HTTP 200.
  - Build check: `gh api repos/paulrenzi/drone-detection-research/pages/builds/latest`.
  - Render checker: `%TEMP%\rc_mvp.py <sha>`. It holds a needle list per page and reports broken internal anchors.
- Subagents run on sonnet or haiku, never opus.

## What this session did (all pushed, all render-verified)

| Commit | Change |
|---|---|
| `17f97f4` | MVP page cut to tables and steps |
| `7caab76` | Amazon first in every layer. Every link was opened and checked for Add to Cart and the price on 10-15. Cells and the PPK2 stay off Amazon. |
| `4fd2265`, `b4108d1` | **T18 is no longer a gate.** See the ruling below. |
| `93b634d` | The all-layers shopping list is collapsed at the bottom. Layer 1 is open by default. |

## Ruling from Paul: no demand gates

> "If you got the same timing at lower price, you use that. If you get more time to react at
> lower price, you stop even asking questions."

Never make "would troops value this?" a gate or a reason to scrap.

- **What gates are:** delivery (radio range, detection range, battery, placement) and hidden costs that aren't price (false alarms, risk to whoever places the kit, maintenance).
- **What interviews (T18) are for:** sizing the lives estimate and shaping how a line is placed. Nothing more.

## Hardware Paul now owns

**Two Seeed ReSpeaker XVF3800 USB 4-mic arrays.** They are good for layer 2 (the T11 range test) as a reference recorder alongside an INMP441, and as a test of whether they can give a bearing.

- **Caveat:** their speech processing (noise suppression, automatic gain, beamforming) treats a steady drone hum as noise to remove.
- **Before using one:** confirm all of it can be switched off ([XMOS guide](https://www.xmos.com/documentation/XM-014888-PC/pdf/xvf3800_user_guide_v3.2.1.pdf)).
- **Spacing rule:** set listener spacing from the INMP441's range, not the array's.
- **Not on the site yet.** Paul said he may want a line in layer 2. Ask first.

## The next session: hardware design and software layout

Paul's words: "start visualizing the harness for an existing drone, or modeling the 3D printed
drone, and spacing out the software." The site argues for all of this but **has no design for any of it**.

### What exists today (text only)

| Topic | Where | Says |
|---|---|---|
| Listener body | `models/tripwire.md` "Throwaway listeners", "What goes in one listener" | Dart body sticks upright in soil. A spring mast lifts the mic 0.5–1 m. Printed housing, $1–2 in filament. Fur windscreen. |
| Why print | `tripwire.md` `#why-3d-print-the-drones-and-the-nodes` | A printed frame saves only $15–35 per drone, because electronics are 85–90% of its cost. Printing pays on listeners, release clips and cargo racks, field repair, and fast iteration. A printed fixed-wing carrier is worth testing. |
| Delivery drone | `research/delivery-drone.md` "Recommended prototype" | X500-class quad, Pixhawk 6C, ArduPilot. **One servo pin per node, fired by `DO_SET_SERVO` at each drop waypoint.** No radio links in flight. Missions loaded with pymavlink. Plain GPS first, then optical flow. |
| Drop test | T13 in `research/open-questions.md`, tripwire step 5 | A printed quad lays 4 listeners on planned points, under $500. Flight time with 3–4 nodes is **unknown**; T13 measures it. |
| Firmware base | `research/open-source-builds.md` | Batear (MIT): one mic, ESP32-S3, encrypted LoRa. VolAnti: 104 m range test. |

### Hardware still missing

1. **Release harness for an existing drone.** Decide the host first:
   - **X500 + Pixhawk** is the site's pick. The servo release is native.
   - **A DJI Mini or Mavic** has no servo output. It would need a light-triggered or self-timed release, and the site already says DJI suits prototypes only.
   - **An FPV quad** may be what Ukraine actually has.

   Ask Paul which drone he has or would buy. Then design a printed mount that holds 3–4 listeners, with one servo pin per listener.
2. **Listener dart.** A printed body with a soil spike, a spring or folding mast reaching 0.5–1 m, and a cavity for the board and cell. It must fit the Heltec V3 now and a custom board later.
   - Decide the fin or drag layout so it lands point-down.
   - Unsourced: drop height, impact speed, and whether the mast deploys after landing. Estimate these and label them.
3. **Printed drone.** Lowest priority, because the site says printing barely saves money on the airframe. Still unscoped: a printed quad or fixed-wing for T13. Estimate payload and flight time first; they are unknown.
4. **Edge receiver mount.** A pole-top housing for the receive-only board and a Yagi mount. Lower priority.

### Software still missing (nothing is architected)

Lay these out as components, interfaces and owners, then mark what Batear already covers:

- **Listener firmware:**
  - wake-on-sound, then a drone/no-drone classifier on the ESP32-S3;
  - LoRa alert packet format, relay and hop rules, deduplication;
  - battery and temperature reports;
  - no GPS: position comes from the drop plan;
  - classifier updates ship in the next batch, not over the air (`tripwire.md`).
- **Edge receiver firmware:** receive only, never transmit (proved with an SDR in T17), then RS-485 to the dugout.
- **Dugout display:** shows which listener tripped, where it is on the map, the time since crossing and a confidence. It needs a false-alarm policy and some way to show the line's health.
- **Mission tooling:** turn a planned line into an ArduPilot mission with `DO_SET_SERVO` at each drop point, and log drop positions so they feed the listener map.
- **Training data and classifier pipeline:** datasets are in `research/datasets.md`; the layer 2 recordings add field audio.
- **Test harness:** SITL for the drop missions, and a bench replay of recorded audio into a listener.

### Visualising it

**No CAD tool is installed on the PC.** Checked 10-15: no OpenSCAD, CadQuery, Blender, FreeCAD, trimesh or slicer.

- **Proposed:** text-based CAD so files diff in git and are reviewable. Either OpenSCAD (`winget install OpenSCAD.OpenSCAD`) or CadQuery (pip). Render PNGs headless for the site; STLs go in the repo, for example `cad/`.
- **Ask Paul first:**
  1. Does he own a 3D printer, and which one? That sets the bed size and material.
  2. Which drone, if any, does he own?
  3. Should the hardware and software get one new site page or two?

### Suggested order

1. Ask the questions above.
2. Software layout page: no tools needed, and it can start at once.
3. Listener dart in CAD, with a rendered image on the site.
4. Release harness for the chosen drone.
5. Printed drone, only once payload and flight time are estimated.
