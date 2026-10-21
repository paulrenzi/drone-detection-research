---
title: "3D models and downloads"
nav_primary: 2
---

# 3D models and downloads
{: .no_toc }

The [tripwire]({{ site.baseurl }}{% link index.md %}) depends on a drone carrying listeners forward and dropping them so they stand up and listen. These are the models of that hardware: one listener (the **dart**), the **harness** that holds and releases four of them, and both on a Holybro X500. Each model plays its assembly on its own: press **Pause** to stop it, then rotate, zoom, or drag the slider to take it apart by hand. Point at a part to name it; click it for its mass and what it does. Every printed part is [downloadable](#6-downloads) as STL and STEP.

{: .warning }
> **A computer model, not a tested design.** Nothing here has been printed, assembled, dropped or flown. The bought parts are the manufacturers' own CAD where it exists (the X500 frame, the Heltec board), and every other dimension comes from a datasheet or is flagged *measure*. Masses are computed from the model's geometry. The open question is whether a dart released sideways from the drone turns nose-down and sticks in soil with the microphone working, and no model answers it. A weighted dummy dropped from the drone does.

1. TOC
{:toc}

<script type="importmap">
{ "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
} }
</script>
<script type="module" src="{{ site.baseurl }}/assets/js/cad-viewer.js"></script>

{% assign web = site.baseurl | append: "/cad/gpt61/web/" %}

## 1. One dart

<div class="cad-viewer" data-src="{{ web }}dart.glb" data-manifest="{{ web }}manifest.json" data-model="dart"></div>

A 6 × 500 mm fibreglass rod is the spike, the spine and the mast. Two printed parts sit on it. The **body**, near the tip, holds the 18650 cell in snap fingers and carries the hanger post the harness grips. The **pod**, on the top end, is a tray and a screwed lid. It holds the Heltec board, the microphone behind a side port, and the whip antenna. Two wires run along the rod from the cell to the pod.

The model lies flat, the way it is carried. Exploded, the body slides off toward the tip and the pod slides off the rod end. The cell and the lid lift away, and the screws, inserts, seals and foam pads separate so each can be seen.

- **Model mass: 158.2 g.** The cell is 45 g (datasheet maximum), the body 41.7 g, the rod 26.5 g, the pod tray and lid 29.8 g, the board 9 g, and screws, wire and seals the rest. Printed masses assume solid PETG at 100% infill. Nothing has been weighed.
- **The hanger is at the model's balance point,** 266 mm from the tip and offset 6.5 mm toward the cell, because the cell sits beside the rod and not on it.
- **Standing in soil,** the tip goes in 70 mm and the sound port is 470 mm above the ground. The whole dart is 644 mm from tip to whip.

## 2. The harness, loaded with four darts

<div class="cad-viewer" data-src="{{ web }}harness.glb" data-manifest="{{ web }}manifest.json" data-model="harness"></div>

One printed plate is zip-tied to the X500's two payload rails at four saddles. An SG90 servo hangs under the plate and turns a printed **rotor** on top of it. Each dart's hanger post comes up through a slot in the plate, and its round head rests on the rotor's rim. The rim has four gaps at different angles. Each 16° servo step lines one gap up with one head, and that dart drops: the inner pair first, then the outer pair.

The darts' weight bears on a ridge on the plate, faced with PTFE tape, not on the servo. A loose keeper washer above the rotor stops it lifting off. Exploded, the keeper lifts first, then the rotor and the servo horn. The servo drops below the plate and the four darts drop below that in two tiers.

- **Model mass: 183.5 g without darts**: plate 131.7 g, rotor 38.6 g, servo and horn about 9 g (catalogue), plus fasteners and ties.
- **Four darts plus the harness: 816.1 g.** That is the payload the X500 has to carry on top of its own battery and avionics. Whether it carries it well is a flight test, not a model result.
- **The rotor's fit and the servo's torque are calculations.** With an assumed friction coefficient, the rotor's friction is about a fifth of the SG90's stall torque at rest, and nearly two-thirds of it at 3 g. Stall is not a torque a servo can hold continuously. The real breakaway torque has to be measured with the tape and all four darts loaded.

## 3. On the drone

<div class="cad-viewer" data-src="{{ web }}aircraft.glb" data-manifest="{{ web }}manifest.json" data-model="aircraft"></div>

The Holybro X500 V2 is the manufacturer's own STEP model, simplified for the web. The translucent discs are the propellers' swept area, used for the clearance check, not blade models. Exploded, the whole payload lowers 400 mm clear of the airframe, then opens as in the harness view.

- **In the carried state nothing overlaps:** darts, frame, rails, clamps, motors, prop discs, landing legs or each other, at the nominal dimensions. The lowest dart is 90 mm above the ground plane of the stock skids.
- **The model checks a clear path out, not the fall.** It checks each dart sliding 90 mm straight down through its gap, and a nose-down rotation once a dart is 430 mm below the drone. It does not show that a real dart waits that long before it tips, or that it lands upright.

## 4. Every part

Masses are the model's estimates. A dash means no separate figure: the servo and its horn share one 9 g catalogue mass. **Bought** parts are the manufacturer's CAD where one exists and a datasheet build otherwise; **printed** parts are modelled from scratch.

**Per dart**

| Part | Printed or bought | Mass (g) | Geometry from | What it does |
|---|---|---|---|---|
| Body, with cell snaps and hanger | printed | 41.7 | modelled | Holds the cell and the rod, and carries the dart's weight through its hanger post |
| Pod tray | printed | 21.8 | modelled | Holds the electronics, the rod socket and the microphone cavity |
| Pod lid | printed | 8.1 | modelled | Closes the pod and holds the boards down through foam pads |
| Fibreglass rod, 6 × 500 mm | bought | 26.5 | modelled to spec | Spike, spine and mast |
| Samsung INR18650-25R cell | bought | 45.0 | datasheet | Power |
| Heltec WiFi LoRa 32 V3 | bought | 9.0 | manufacturer STEP, OLED added from the datasheet | Microcontroller and LoRa radio |
| INMP441 microphone breakout | bought | 1.0 | chip from datasheet; breakout board *measure* | Listens through the side port |
| Whip, boot and U.FL lead | bought | 1.2 | *measure*: no identified part | Antenna |
| 4 heat-set inserts and 4 M2 × 6 screws | bought | 2.0 | Ruthex STEP; screws modelled | Hold the lid on |
| Lid seal cord, mic film and mic seal | bought | 0.3 | modelled to the TDK sealing note | Seal the pod; not tested for water or sound |
| 2 power wires, 2 cell tabs | bought | 1.2 | modelled | Run power from the cell to the pod |
| 3 zip ties | bought | 0.6 | HellermannTyton datasheet | Hold the wires to the rod |
| 4 foam pads | bought | 0.0 | modelled | Cushion the board |
| **Dart total** | | **158.2** | | |

**Harness**

| Part | Printed or bought | Mass (g) | Geometry from | What it does |
|---|---|---|---|---|
| Plate with four rail saddles | printed | 131.7 | modelled | Carries the four darts and ties to the payload rails |
| Release rotor | printed | 38.6 | modelled | Holds the dart heads up and uncovers them one at a time |
| TowerPro SG90 servo and stock horn | bought | – | drawing and photo; spline *measure* | Turns the rotor; driven from Pixhawk AUX 1 |
| Keeper screw, spacer and washer | bought | 0.6 | modelled | Stop the rotor lifting off |
| 2 drive pins and 4 nuts | bought | 1.1 | modelled | Couple the servo horn to the rotor |
| 2 servo screws and 2 captive nuts | bought | 0.9 | modelled | Hold the servo under the plate |
| Servo lead and plug | bought | 0.5 | modelled | Servo power and signal |
| 4 rail zip ties | bought | 1.0 | HellermannTyton datasheet | Tie the saddles to the rails |
| PTFE film on the bearing ridge | bought | 0.2 | 3M datasheet | Low-friction face for the rotor |
| **Harness total** (with the servo's 9 g) | | **183.5** | | |

## 5. What the model does and does not show

**What it shows:** every part at a sourced or flagged size, fitting together without overlap in the carried, releasing and standing states. Those are GPT-6.1's 74 generated checks, and they test the model against itself. It also shows the order the parts go together, and a mass for everything.

**What it does not show:**

- **That a dart lands upright.** The darts are carried flat. Nothing here models the fall, the turn nose-down, or 70 mm of rod going into real soil. This is the first test: print a dummy, weight it to 158 g, and drop it from the drone's release height again and again.
- **That the microphone hears a drone through the pod.** The side port, film and cavity are built from TDK's sealing guidance, but they have never been recorded through.
- **That the pod keeps water out.** It is a printed box with a cord seal. The seal's squeeze is calculated, not tested.
- **That the X500 flies well with 816 g under it.**
- **About 60 dimensions marked *measure*:** the microphone breakout, the antenna, the servo's spline and screw thread, and the print fits. They have to be checked with calipers on the bought parts and a printed fit coupon before the real print.
- **The animation is an assembly diagram.** It slides rigid parts apart. It does not show screws turning, ties being cut, inserts being heated in, or the servo's real release sequence.

## 6. Downloads

<p><a class="cad-btn cad-download" href="{{ site.baseurl }}/cad/gpt61/out/print-kit.zip" download>Download the print kit (.zip, 0.7 MB)</a></p>

The print kit holds all six STL files, the print settings ([`print_manifest.json`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/out/print_manifest.json)), the design notes, the mass table and the 74 checks. **Print the fit coupon first** and check it against the bought parts with calipers: about 60 dimensions are still marked *measure*.

| Printed part | Mass (g) | Print | Edit |
|---|--:|---|---|
| Dart body | 41.7 | <a href="{{ site.baseurl }}/cad/gpt61/out/body.stl" download>body.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/body.step" download>body.step</a> |
| Pod tray | 21.8 | <a href="{{ site.baseurl }}/cad/gpt61/out/pod_shell.stl" download>pod_shell.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/pod_shell.step" download>pod_shell.step</a> |
| Pod lid | 8.1 | <a href="{{ site.baseurl }}/cad/gpt61/out/pod_lid.stl" download>pod_lid.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/pod_lid.step" download>pod_lid.step</a> |
| Harness plate | 131.7 | <a href="{{ site.baseurl }}/cad/gpt61/out/plate.stl" download>plate.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/plate.step" download>plate.step</a> |
| Release rotor | 38.6 | <a href="{{ site.baseurl }}/cad/gpt61/out/rotor.stl" download>rotor.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/rotor.step" download>rotor.step</a> |
| Fit coupon (print first) | – | <a href="{{ site.baseurl }}/cad/gpt61/out/fit_coupon.stl" download>fit_coupon.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/fit_coupon.step" download>fit_coupon.step</a> |

**Bought parts** as STEP, for checking fits: <a href="{{ site.baseurl }}/cad/gpt61/out/bought_heltec_v3.step" download>Heltec V3</a> (35 MB), <a href="{{ site.baseurl }}/cad/gpt61/out/bought_SG90.step" download>SG90 servo</a>, <a href="{{ site.baseurl }}/cad/gpt61/out/bought_inmp441.step" download>INMP441</a>, <a href="{{ site.baseurl }}/cad/gpt61/out/bought_18650.step" download>18650 cell</a>, <a href="{{ site.baseurl }}/cad/gpt61/out/bought_rod.step" download>rod</a>. The X500 frame is Holybro's own STEP, too large to host here.

**The 3D models on this page**, as glTF with the explode animation: <a href="{{ site.baseurl }}/cad/gpt61/web/dart.glb" download>dart.glb</a> (3.6 MB), <a href="{{ site.baseurl }}/cad/gpt61/web/harness.glb" download>harness.glb</a> (4.5 MB), <a href="{{ site.baseurl }}/cad/gpt61/web/aircraft.glb" download>aircraft.glb</a> (19 MB). Any glTF viewer opens them.

### Sources and provenance

- **Viewer models:** [`dart.glb`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/web/dart.glb) (3.6 MB), [`harness.glb`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/web/harness.glb) (4.5 MB) and [`aircraft.glb`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/web/aircraft.glb) (19 MB). Each is one file with an `explode` animation. Every part is a named node, with no errors or warnings from the Khronos glTF validator. The drone and the board are simplified for the web, so measure from the STEP files, not these.
- **Part data:** [`manifest.json`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/web/manifest.json) lists every node's name, source, mass and what it does, plus the open uncertainties.
- **Still renders:** [dart exploded]({{ site.baseurl }}/cad/gpt61/renders/dart_exploded.png), [pod exploded]({{ site.baseurl }}/cad/gpt61/renders/dart_exploded_pod.png), [harness exploded]({{ site.baseurl }}/cad/gpt61/renders/harness_exploded.png), [harness detail]({{ site.baseurl }}/cad/gpt61/renders/harness_exploded_detail.png), [on the drone]({{ site.baseurl }}/cad/gpt61/renders/aircraft_exploded.png), and the full gallery in [`REVIEW.html`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/REVIEW.html).
- **Print files and design notes:** STL and STEP for every printed part, and the print settings, sources and assembly steps, in [`cad/gpt61/`](https://github.com/paulrenzi/tripwire/tree/main/cad/gpt61). Start with [`DESIGN.md`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/DESIGN.md).
- **Who made it:** GPT-6.1, run as an agent through the Codex CLI on 2026-10-15 and 10-16, from a written brief. The CAD is CadQuery (Python). Rebuild the viewer models with `cad/gpt61/web_export.py`.
- **The older designs** (v1–v3, hand-built boxes and cylinders) are on [Build: hardware]({{ site.baseurl }}{% link build-hardware.md %}). This model replaces their geometry, not their concept.
