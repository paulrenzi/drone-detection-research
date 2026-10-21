---
title: "3D models and downloads"
nav_primary: 2
---

# 3D models and downloads
{: .no_toc }

The [tripwire]({{ site.baseurl }}{% link index.md %}) depends on a drone carrying listeners forward and dropping them so they stand up and listen. These are the models of that hardware: one listener (the **dart**), the **harness** that holds and releases four of them, both on a Holybro X500, and a **stake mount** for placing a listener by hand. Each model plays its assembly on its own: press **Pause** to stop it, then rotate, zoom, or drag the slider to take it apart by hand. Point at a part to name it; click it for its mass and what it does. Every printed part is [downloadable](#8-downloads) as STL and STEP.

{: .warning }
> **A computer model, not a tested design.** Nothing here has been printed, assembled, dropped or flown. The bought parts are the manufacturers' own CAD where it exists (the X500 frame, the Seeed XIAO ESP32S3 and Wio-SX1262 boards), and every other dimension comes from a datasheet or is flagged *measure*. Masses are computed from the model's geometry. The open question is whether a dart released sideways from the drone turns nose-down and sticks in soil with the microphone working, and no model answers it. The weighted [dummy](#5-the-drop-test-dummy) dropped from the drone does.

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

A 0.24 × 20 in fibreglass rod is the spike, the spine and the mast. Two printed parts sit on it. The **body**, near the tip, holds the 18650 cell in snap fingers and carries the hanger post the harness grips. The **pod**, on the top end, is a small tray and a screwed lid. It holds the XIAO ESP32S3 with the Wio-SX1262 radio board plugged on top, the microphone behind a side port, and the kit's two flat antennas: the LoRa one on a strip that runs past the pod, the WiFi one inside. Two wires run along the rod from the cell to pads under the XIAO.

The pod has no screen and no status light. The listener reports by radio once a minute that it is alive. A small printed **cap** on the pod's end comes off to reach the USB-C port for flashing, and a pin through the same opening presses BOOT or RESET, so the lid stays shut.

The model lies flat, the way it is carried. Exploded, the body slides off toward the tip and the pod slides off the rod end. The cell and the lid lift away, and the screws, inserts, seals and foam pads separate so each can be seen.

- **Model mass: 5.2 oz,** down from 5.6 oz with the earlier Heltec board. The cell is 1.6 oz (datasheet maximum), the body 1.4 oz, the rod 0.93 oz, the pod tray, lid and cap 0.90 oz, the two boards 0.14 oz, and screws, wire, antennas and seals the rest. Printed masses assume solid PETG at 100% infill. Nothing has been weighed.
- **The hanger is at the model's balance point,** 10.0 in from the tip and offset 0.28 in toward the cell, because the cell sits beside the rod and not on it.
- **Standing in soil,** the tip goes in 2.8 in and the sound port is 19.7 in above the ground. The whole dart is 27 in from tip to antenna. The LoRa antenna's size is a placeholder until the real one is measured, and it is why the dart is longer than before.

## 2. The harness, loaded with four darts

<div class="cad-viewer" data-src="{{ web }}harness.glb" data-manifest="{{ web }}manifest.json" data-model="harness"></div>

One printed plate is zip-tied to the X500's two payload rails at four saddles. An SG90 servo hangs under the plate and turns a printed **rotor** on top of it. Each dart's hanger post comes up through a slot in the plate, and its round head rests on the rotor's rim. The rim has four gaps at different angles. Each 16° servo step lines one gap up with one head, and that dart drops: the inner pair first, then the outer pair.

The darts' weight bears on a ridge on the plate, faced with PTFE tape, not on the servo. A loose keeper washer above the rotor stops it lifting off. Exploded, the keeper lifts first, then the rotor and the servo horn. The servo drops below the plate and the four darts drop below that in two tiers. The harness itself did not change for the new board; its fits were rechecked against the lighter darts.

- **Model mass: 6.5 oz without darts**: plate 4.6 oz, rotor 1.4 oz, servo and horn about 0.32 oz (catalogue), plus fasteners and ties.
- **Four darts plus the harness: 1.7 lb.** That is the payload the X500 has to carry on top of its own battery and avionics. Whether it carries it well is a flight test, not a model result.
- **The rotor's fit and the servo's torque are calculations.** The real breakaway torque has to be measured with the PTFE tape and all four darts loaded. Stall torque is not a torque a servo can hold continuously.

## 3. On the drone

<div class="cad-viewer" data-src="{{ web }}aircraft.glb" data-manifest="{{ web }}manifest.json" data-model="aircraft"></div>

The Holybro X500 V2 is the manufacturer's own STEP model, simplified for the web. The translucent discs are the propellers' swept area, used for the clearance check, not blade models. Exploded, the whole payload lowers 16 in clear of the airframe, then opens as in the harness view.

- **In the carried state nothing overlaps:** darts, frame, rails, clamps, motors, prop discs, landing legs or each other, at the nominal dimensions. The lowest dart is 3.7 in above the ground plane of the stock skids.
- **The model checks a clear path out, not the fall.** It checks each dart sliding 3.5 in straight down through its gap, and a nose-down rotation once a dart is 17 in below the drone. It does not show that a real dart waits that long before it tips, or that it lands upright.

## 4. The stake listener

<div class="cad-viewer" data-src="{{ web }}stake.glb" data-manifest="{{ web }}manifest.json" data-model="stake"></div>

For placing a listener by hand, with no drone. The same pod, board and cell go on a 48 in fibreglass garden stake from a hardware store. A printed **stake adapter** holds the pod: two V-shaped saddles and zip ties grip any stake from 0.31 to 0.51 in across, so the stake's exact size doesn't matter. A 1.6 in offcut of the dart rod plugs the adapter into the pod's usual socket. A separate printed **cell holder**, tied lower on the stake, holds the 18650, wired to the board as in the dart.

Push the stake in by hand, then slide the adapter until the microphone is 19.7 in above the ground; how deep the stake goes doesn't change that. Exploded, the pod pulls off its offcut.

- **Model mass: 10.9 oz** for the whole installation, stake and cell included. Nothing on the stake flies, so this is not drone payload.

## 5. The drop-test dummy

<p><img src="{{ site.baseurl }}/cad/gpt61/renders/dummy_assembled.png" alt="The inert dummy dart standing in soil: the same rod, hanger and pod as a real dart, with a ballast box where the cell would be" width="300"></p>

The first test is a drop, and a dummy is cheaper to break. It uses the same rod, hanger, pod shell, lid, cap and antenna strip as a real dart, with no cell, board or microphone. Steel ballast in four printed pockets, two in the body and two in the pod, brings it to the real dart's mass and balance point.

- **Ballast: 1.3 oz of steel** in all, weighed out into four portions (nuts or washers work), held still with foam. The empty dummy is 3.9 oz; with ballast it matches the real dart's 5.2 oz.
- **Weigh the printed dummy first,** then re-solve the ballast with the real numbers. The model's match is only as good as its estimates.
- **What the drops answer:** whether the dart turns nose-down, when it starts to turn, whether it sticks, and whether the snaps, post and rod survive.

## 6. Every part

Masses are the model's estimates. A dash means no separate figure: the servo and its horn share one 0.32 oz catalogue mass. **Bought** parts are the manufacturer's CAD where one exists and a datasheet build otherwise; **printed** parts are modelled from scratch.

**Per dart**

| Part | Printed or bought | Mass (oz) | Geometry from | What it does |
|---|---|---|---|---|
| Body, with cell snaps and hanger | printed | 1.45 | modelled | Holds the cell and the rod, and carries the dart's weight through its hanger post |
| Pod tray | printed | 0.67 | modelled | Holds the boards, the rod socket and the microphone cavity |
| Pod lid, with the antenna strip | printed | 0.20 | modelled | Closes the pod, holds the boards down through foam pads, and carries the LoRa antenna |
| USB cap | printed | 0.03 | modelled | Covers the end opening for USB-C and the BOOT and RESET buttons |
| Fibreglass rod, 0.24 × 20 in | bought | 0.93 | modelled to spec | Spike, spine and mast |
| Samsung INR18650-25R cell | bought | 1.59 | datasheet | Power |
| Seeed XIAO ESP32S3 | bought | 0.08 | Seeed STEP | Microcontroller, WiFi and battery charger |
| Seeed Wio-SX1262 for XIAO | bought | 0.06 | Seeed STEP; plug-in spacing *measure* | LoRa radio |
| INMP441 microphone breakout | bought | 0.04 | chip from datasheet; breakout board *measure* | Listens through the side port |
| LoRa and WiFi antennas, with leads | bought | 0.04 | *measure*: no dimensioned drawing found | The kit's two flat antennas |
| 3 heat-set inserts and 3 M2 × 6 screws | bought | 0.05 | Ruthex STEP; screws modelled | Hold the lid on |
| Lid seal cord, mic film and mic seal | bought | 0.01 | modelled to the TDK sealing note | Seal the pod; not tested for water or sound |
| 2 power wires, 5 mic wires, 2 cell tabs | bought | 0.05 | modelled | Power from the cell; microphone to the board |
| 3 zip ties | bought | 0.02 | HellermannTyton datasheet | Hold the wires to the rod |
| 4 foam pads | bought | 0.00 | modelled | Cushion the boards |
| **Dart total** | | **5.22** | | |

**Harness**

| Part | Printed or bought | Mass (oz) | Geometry from | What it does |
|---|---|---|---|---|
| Plate with four rail saddles | printed | 4.64 | modelled | Carries the four darts and ties to the payload rails |
| Release rotor | printed | 1.36 | modelled | Holds the dart heads up and uncovers them one at a time |
| TowerPro SG90 servo and stock horn | bought | – | drawing and photo; spline *measure* | Turns the rotor; driven from Pixhawk AUX 1 |
| Keeper screw, spacer and washer | bought | 0.02 | modelled | Stop the rotor lifting off |
| 2 drive pins and 4 nuts | bought | 0.04 | modelled | Couple the servo horn to the rotor |
| 2 servo screws and 2 captive nuts | bought | 0.03 | modelled | Hold the servo under the plate |
| Servo lead and plug | bought | 0.02 | modelled | Servo power and signal |
| 4 rail zip ties | bought | 0.04 | HellermannTyton datasheet | Tie the saddles to the rails |
| PTFE film on the bearing ridge | bought | 0.01 | 3M datasheet | Low-friction face for the rotor |
| **Harness total** (with the servo's 0.32 oz) | | **6.47** | | |

## 7. What the model does and does not show

**What it shows:** every part at a sourced or flagged size, fitting together without overlap in the carried, releasing and standing states, on the stake, and with the dummy's ballast in its pockets. Those are GPT-6.1's 140 generated checks, and they test the model against itself. It also shows the order the parts go together, and a mass for everything.

**What it does not show:**

- **That a dart lands upright.** The darts are carried flat. Nothing here models the fall, the turn nose-down, or 2.8 in of rod going into real soil. This is the first test: print the [dummy](#5-the-drop-test-dummy) and drop it from the drone's release height again and again.
- **That the microphone hears a drone through the pod.** The side port, film and cavity are built from TDK's sealing guidance, but they have never been recorded through.
- **That the pod keeps water out.** It is a printed box with a cord seal and a sealed cap. The seal's squeeze is calculated, not tested.
- **That the X500 flies well with 1.7 lb under it.**
- **About 60 dimensions marked *measure*:** how far apart the two boards sit when plugged together, the antennas, the microphone breakout, the servo's spline and screw thread, and the print fits. They have to be checked with calipers on the bought parts and a printed fit coupon before the real print.
- **The animation is an assembly diagram.** It slides rigid parts apart. It does not show screws turning, ties being cut, inserts being heated in, or the servo's real release sequence.

## 8. Downloads

<p><a class="cad-btn cad-download" href="{{ site.baseurl }}/cad/gpt61/out/print-kit.zip" download>Download the print kit (.zip, 2.4 MB)</a></p>

The print kit holds the STL and STEP for all twelve printed parts, the print settings ([`print_manifest.json`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/out/print_manifest.json)), the design notes, the mass table and the 140 checks. **Print the fit coupon first** and check it against the bought parts with calipers: about 60 dimensions are still marked *measure*. Four darts and the harness take 18 printed pieces; the stake and dummy parts are optional.

| Printed part | Mass (oz) | Print | Edit |
|---|--:|---|---|
| Dart body | 1.45 | <a href="{{ site.baseurl }}/cad/gpt61/out/body.stl" download>body.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/body.step" download>body.step</a> |
| Pod tray | 0.67 | <a href="{{ site.baseurl }}/cad/gpt61/out/pod_shell.stl" download>pod_shell.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/pod_shell.step" download>pod_shell.step</a> |
| Pod lid | 0.20 | <a href="{{ site.baseurl }}/cad/gpt61/out/pod_lid.stl" download>pod_lid.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/pod_lid.step" download>pod_lid.step</a> |
| USB cap | 0.03 | <a href="{{ site.baseurl }}/cad/gpt61/out/usb_cap.stl" download>usb_cap.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/usb_cap.step" download>usb_cap.step</a> |
| Harness plate | 4.64 | <a href="{{ site.baseurl }}/cad/gpt61/out/plate.stl" download>plate.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/plate.step" download>plate.step</a> |
| Release rotor | 1.36 | <a href="{{ site.baseurl }}/cad/gpt61/out/rotor.stl" download>rotor.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/rotor.step" download>rotor.step</a> |
| Fit coupon (print first) | 0.16 | <a href="{{ site.baseurl }}/cad/gpt61/out/fit_coupon.stl" download>fit_coupon.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/fit_coupon.step" download>fit_coupon.step</a> |
| Stake adapter (optional) | 0.47 | <a href="{{ site.baseurl }}/cad/gpt61/out/stake_adapter.stl" download>stake_adapter.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/stake_adapter.step" download>stake_adapter.step</a> |
| Stake cell holder (optional) | 1.08 | <a href="{{ site.baseurl }}/cad/gpt61/out/stake_cell_holder.stl" download>stake_cell_holder.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/stake_cell_holder.step" download>stake_cell_holder.step</a> |
| Dummy body (optional) | 1.78 | <a href="{{ site.baseurl }}/cad/gpt61/out/dummy_body.stl" download>dummy_body.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/dummy_body.step" download>dummy_body.step</a> |
| Dummy lid (optional) | 0.14 | <a href="{{ site.baseurl }}/cad/gpt61/out/dummy_lid.stl" download>dummy_lid.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/dummy_lid.step" download>dummy_lid.step</a> |
| Dummy head insert (optional) | 0.07 | <a href="{{ site.baseurl }}/cad/gpt61/out/dummy_head_insert.stl" download>dummy_head_insert.stl</a> | <a href="{{ site.baseurl }}/cad/gpt61/out/dummy_head_insert.step" download>dummy_head_insert.step</a> |

**Bought parts** as STEP, for checking fits: <a href="{{ site.baseurl }}/cad/gpt61/out/bought_xiao_wio_stack.step" download>XIAO + Wio stack</a> (11 MB), <a href="{{ site.baseurl }}/cad/gpt61/out/bought_SG90.step" download>SG90 servo</a>, <a href="{{ site.baseurl }}/cad/gpt61/out/bought_inmp441.step" download>INMP441</a>, <a href="{{ site.baseurl }}/cad/gpt61/out/bought_18650.step" download>18650 cell</a>, <a href="{{ site.baseurl }}/cad/gpt61/out/bought_rod.step" download>rod</a>. The X500 frame is Holybro's own STEP, too large to host here.

**Assemblies** as STEP: <a href="{{ site.baseurl }}/cad/gpt61/out/dart_stood.step" download>dart standing in soil</a> (24 MB), <a href="{{ site.baseurl }}/cad/gpt61/out/stake_assembled.step" download>stake listener</a> (24 MB), <a href="{{ site.baseurl }}/cad/gpt61/out/dummy_assembled.step" download>dummy</a> (10 MB).

**The 3D models on this page**, as glTF with the explode animation: <a href="{{ site.baseurl }}/cad/gpt61/web/dart.glb" download>dart.glb</a> (3.2 MB), <a href="{{ site.baseurl }}/cad/gpt61/web/harness.glb" download>harness.glb</a> (4.1 MB), <a href="{{ site.baseurl }}/cad/gpt61/web/aircraft.glb" download>aircraft.glb</a> (19 MB), <a href="{{ site.baseurl }}/cad/gpt61/web/stake.glb" download>stake.glb</a> (3.2 MB). Any glTF viewer opens them.

### Sources and provenance

- **Viewer models:** [`dart.glb`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/web/dart.glb), [`harness.glb`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/web/harness.glb), [`aircraft.glb`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/web/aircraft.glb) and [`stake.glb`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/web/stake.glb). Each is one file with an `explode` animation. Every part is a named node, with no errors or warnings from the Khronos glTF validator. The drone and the boards are simplified for the web, so measure from the STEP files, not these.
- **Part data:** [`manifest.json`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/web/manifest.json) lists every node's name, source, mass and what it does, plus the open uncertainties.
- **Still renders:** [dart exploded]({{ site.baseurl }}/cad/gpt61/renders/dart_exploded.png), [pod exploded]({{ site.baseurl }}/cad/gpt61/renders/dart_exploded_pod.png), [USB access]({{ site.baseurl }}/cad/gpt61/renders/pod_usb_access.png), [harness exploded]({{ site.baseurl }}/cad/gpt61/renders/harness_exploded.png), [on the drone]({{ site.baseurl }}/cad/gpt61/renders/aircraft_exploded.png), [stake]({{ site.baseurl }}/cad/gpt61/renders/stake_assembled.png), [dummy ballast]({{ site.baseurl }}/cad/gpt61/renders/dummy_ballast_detail.png), and all 33 in [`REVIEW.html`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/REVIEW.html). GPT-6.1 labelled the renders in millimetres and grams.
- **Print files and design notes:** STL and STEP for every printed part, and the print settings, sources and assembly steps, in [`cad/gpt61/`](https://github.com/paulrenzi/tripwire/tree/main/cad/gpt61). Start with [`DESIGN.md`](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/DESIGN.md), also in millimetres.
- **Who made it:** GPT-6.1, run as an agent through the Codex CLI on 2026-10-15 and 10-16 from a written brief, and again on 2026-10-21 to rebuild it round the XIAO kit ([brief](https://github.com/paulrenzi/tripwire/blob/main/cad/gpt61/BRIEF-xiao.md)). The CAD is CadQuery (Python). Rebuild the viewer models with `cad/gpt61/web_export.py`.
- **The older designs** (v1–v3, hand-built boxes and cylinders) are on [Build: hardware]({{ site.baseurl }}{% link build-hardware.md %}). This model replaces their geometry, not their concept.
