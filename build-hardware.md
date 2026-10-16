---
title: "Build: hardware"
nav_order: 1.6
---

# Build: hardware, the dart, the harness and a printed carrier
{: .no_toc }

Printable designs for the [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}):

- **A listener dart:** sticks in the soil and raises its microphone about 0.8 m.
- **A release harness for the Holybro X500 V2:** carries four darts, one pin each.
- **A fully printed carrier quad (TL-1):** built round the same electronics.

Software: [Build: software]({{ site.baseurl }}{% link build-software.md %}).

{: .warning }
> **Version 0 designs, never printed or flown.** Dimensions from datasheets are sourced; masses, flight times and impact figures are estimates from the models and labelled as such. Parts marked *measure* in [`cad/params.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/params.py) must be checked with calipers before printing.

1. TOC
{:toc}

## Short answer

| | Dart | X500 harness | Printed TL-1 quad |
|---|---|---|---|
| Printed parts | 4 (body, cap, hinge, head pod) | 1 plate | Hull, 4 arms, 4 legs |
| Mass (est.) | ~195 g each, with an 18650 cell | ~100 g with 4 servos | ~380 g frame, against 610 g for the X500 frame ([Holybro](https://holybro.com/products/px4-development-kit-x500-v2)) |
| Hover time with 4 darts (est.) | n/a | 9–10 min | 11.5–12 min |
| Reach with 4 darts (est.) | n/a | **~2.2–2.3 km out** | **~2.8–2.9 km out** |
| Fits the Vyper's 245 × 245 × 260 mm bed | Yes | Yes | Yes, every part |

- **Both carriers reach a line about 2 km out with four darts.** Lines 3–4 km out need two darts per sortie, a bigger pack, or a fixed-wing. That is T13's question, now with numbers to test against.
- **The printed quad wins on mass, not money.** The frame cost saving is small, as [the tripwire says]({{ site.baseurl }}{% link models/tripwire.md %}#why-3d-print-the-drones-and-the-nodes). But an estimated ~230 g lighter frame is worth about 2.5 more minutes of hover with four darts, and the dart bay is built into the hull.
- **Print the dart first.** It is needed for T10 (drop test), T11 (range at 0.5–1 m) and T12 (battery), whichever drone carries it.

## The printer and the CAD

- **Printer: Anycubic Vyper.** Build volume 245 × 245 × 260 mm, nozzle up to 260 °C, bed up to 110 °C. Officially it prints PLA, PETG, TPU, ABS and wood fill ([spec, via 3DSourced](https://www.3dsourced.com/3d-printer-reviews/anycubic-vyper-test-review-specs/)). It has no enclosure, so print in **PETG**: it tolerates sun and heat better than PLA and prints well without an enclosure (inference). Carbon-filled nylon and ASA, the usual next step for arms, warp without an enclosure and need a hardened nozzle. That is a second printer, needed only after the prototype stage.
- **CAD: CadQuery,** text-based and in Python. Every model is a script in [`cad/`](https://github.com/paulrenzi/drone-detection-research/tree/main/cad) that reads its dimensions from one file, `cad/params.py`, so a change shows up as a readable diff. Each run writes STL (for slicing), STEP (for any other CAD tool) and the PNG renders on this page, and prints bed-fit checks, masses and the flight-time table. Install: `python -m venv cad-env` then `cad-env/Scripts/pip install cadquery`. Run `python dart.py`, `harness.py` or `quad.py` from `cad/`.

## 1. The listener dart

<p style="display:flex;gap:1rem;align-items:flex-end;flex-wrap:wrap">
<img src="{{ site.baseurl }}/assets/images/build/dart-deployed.png" alt="Dart deployed: steel spike and cone in the soil, cell body, hinge, mast, head pod with fur and whip at about 0.8 m" width="220">
<img src="{{ site.baseurl }}/assets/images/build/dart-stowed.png" alt="Dart stowed: mast folded flat at the hinge, four pole sections and the head pod alongside the body" width="360">
</p>

*Left: deployed, with the grey block marking soil. Right: stowed for carrying, 100 × 34 × 202 mm.*

**How it works:**

1. It hangs upright, spike down, by the **tongue** on its cap. A steel pin from the harness passes through the tongue.
2. The pin pulls and the dart falls point-first. The **4 mast sections**, shock-corded like a tent pole, snap together, and an elastic band or torsion spring at the **hinge** swings the mast upright.
3. The **6 mm steel spike** and the printed cone go into the soil. The cell sits low, so the dart is nose-heavy. The fur-covered head at the top adds drag, acting like a shuttlecock's feathers to keep it point-down (inference; T10 tests it).
4. The **head pod** holds the board, microphone and antenna together at about 0.8 m. Only two power wires run down the mast to the cell. The mic is out of the grass, and the antenna is at the height T9 assumes.

| Part | Choice | Why |
|---|---|---|
| Spike | 6 mm steel rod, 110 mm, 50 mm exposed, epoxied into the cone | A printed tip blunts in hard soil. The steel puts mass forward |
| Body | Printed cone + 18650 bay, 26 mm across | Thin for penetration; the cell is the heaviest part, so it goes low |
| Cell | One 18650 (~46 g, est.) | About 3,000 mAh in the space of a thumb. Its cost is set by battery life ([T12]({{ site.baseurl }}{% link research/open-questions.md %})) |
| Mast | 4 × 160 mm shock-corded fibreglass tent-pole sections, 8.5 mm | Folds to the body's length and self-assembles when released. Spare sections are cheap |
| Hinge | Printed socket on an M3 bolt between two ears on the cap | Folds flat for carrying, upright when deployed. Spring force to be set by test |
| Head pod | Printed, 34 × 92 mm. Heltec V3 (50.2 × 25.5 × 10.2 mm, [Heltec](https://wiki.heltec.org/docs/devices/open-source-hardware/esp32-series/lora-32/wifi-lora-32-v3/)) standing upright, mic at the top under fur, whip out the top | Mic and antenna both high; a custom board later shrinks the pod |

**Estimated mass:** about 195 g. Printed parts are ~73 g at a 60% fill estimate; steel 24 g, poles 29 g, cell 46 g, board, mic, fur and wire about 23 g. The pod is the easiest saving: a custom board and a 1S pouch cell could bring it to 120–150 g (estimate).

**Not yet known (estimates, to be measured in [T10]({{ site.baseurl }}{% link research/open-questions.md %})):**

| Question | Estimate | How T10 settles it |
|---|---|---|
| Drop height | 5–15 m above ground | Drop from 3, 5, 10 and 15 m onto pasture, ploughed field, packed track and mud |
| Impact speed | Up to ~10 m/s from 5 m and ~17 m/s from 15 m, before drag (free fall, √(2gh)) | Phone slow-motion video beside a marked pole |
| Impact energy | ~10 J from 5 m, ~28 J from 15 m, at 195 g | Count cracked caps and pods per height |
| Spike depth | Steel plus most of the cone in soft soil; little in packed track | Measure each drop; record upright or not |
| Does the mast deploy in a 1–2 s fall? | Unknown | Video; if not, deploy on impact instead (a pin knocked out by the landing) |
| No drop-deployed sensor with published drop figures was found | The Vietnam-era ADSID dart used a steel spike and a drag plate, but its patent gives no drop height ([US3984804A](https://patents.google.com/patent/US3984804A)) | |

## 2. Release harness for the Holybro X500 V2

<img src="{{ site.baseurl }}/assets/images/build/harness-simple.png" alt="One printed plate zip-tied under the X500's two rails, four SG90 servos dropped into pockets, four darts hanging upright; the front-left dart is falling after its servo turned" width="720">

<img src="{{ site.baseurl }}/assets/images/build/harness-simple-latch.png" alt="Close-up: the servo horn arm passes through the side-open notch in the dart's tongue" width="440">

**Why the X500:** it is the site's pick ([delivery drone]({{ site.baseurl }}{% link research/delivery-drone.md %}#recommended-prototype)). It runs ArduPilot, has spare servo outputs, carries a 1–1.5 kg payload (Holybro's two pages disagree, [product](https://holybro.com/products/px4-development-kit-x500-v2), [docs](https://docs.holybro.com/drone-development-kit/px4-development-kit-x500v2.md)), and has **two 10 mm payload rails, 250 mm long**, under the body.

**v1: the servo horn is the latch.** One printed part, four servos, zip ties.

- **One 150 × 120 × 5 mm plate** (~63 g, est.), zip-tied to both rails through long slots, which absorbs the unpublished rail spacing.
- **Four SG90s** (22.2 × 11.8 × 31 mm, 9 g, [datasheet](https://www.friendlywire.com/projects/ne555-servo-safe/SG90-datasheet.pdf)) drop into pockets shaft-down, held by their own tab screws.
- **Each dart's tongue has a side-open notch.** The servo's stock horn arm passes through it, and the dart hangs on the arm.
- **To release, the horn turns 90°** and the arm swings out of the open side. The model checks the latched arm sits in the notch and the sweep clears the tongue at every angle from 0° to 90°, on all four servos.
- **Wired to Pixhawk 6C AUX 1–4,** each with `SERVOx_FUNCTION = 0`, and fired by `DO_SET_SERVO` at its drop point ([ArduPilot](https://ardupilot.org/copter/docs/common-servo.html); mission format on the [software page]({{ site.baseurl }}{% link build-software.md %}#i5-mission-file-mission-tooling--drone)).
- **Darts hang upright with heads outboard,** so each falls point-first.

| | v0 pin-puller | **v1 horn latch** |
|---|---|---|
| Printed parts | 13 (plate, 4 saddles, 4 caps, 4 blocks) | **1** |
| Other hardware | 4 pins, 4 pushrods, 8+ M3 bolts | **zip ties** |
| Failure points per dart | servo, pushrod, pin bore | **servo** |
| Harness mass (est.) | ~150 g | **~100 g** |

**Risk to bench-test:** the horn is held only by the servo's gears. Shake the loaded airframe by hand, then fly once with dummy darts, before trusting it in flight. If it slips, the v0 pin-puller (`cad/harness.py`) is the fallback.

**Load:** 4 × ~195 g darts + ~100 g harness ≈ **0.88 kg** (estimate), inside Holybro's 1–1.5 kg.

**One fix the model found:** the hanging darts reach about **219 mm below the rails**, about 44 mm lower than the X500's stock feet (215 mm gear, [Holybro](https://holybro.com/products/px4-development-kit-x500-v2); rail height below the plate estimated). The drone needs **leg extensions of about 60–80 mm** to take off and land with darts on. Holybro doesn't publish the leg tube size, so those aren't modelled yet. *Measure the legs.*

**Bench checks before flying:** each pin releases under a 200 g load at the servo's commanded PWM; no pin releases while the airframe is shaken by hand; a pin with no dart doesn't jam; SITL fires the same mission ([software page]({{ site.baseurl }}{% link build-software.md %}#6-test-harness)).

## 3. A fully printed carrier: TL-1

<img src="{{ site.baseurl }}/assets/images/build/quad-tl1.png" alt="Printed quad TL-1: orange hull with built-in dart bay, four blue printed arms and tall legs, 10 inch prop discs, four darts hanging under the hull" width="760">

**Design rule: print the frame, buy everything that spins or thinks.** The X500 kit's motors (2216 KV920), 10-inch props, Pixhawk 6C, GPS and 4S pack move across unchanged. Only the frame changes.

| Part | Size | Notes |
|---|---|---|
| Hull | 150 × 130 × 46 mm, 2.4 mm walls | One print. The four release blocks are printed into its floor, the same pattern as the X500 plate. Flight controller and wiring inside; lid not drawn |
| Arms ×4 | 196 × 24 × 20 mm box section | Printed flat, slide into corner sockets. Motor pad drilled for 16 × 16 and 19 × 19 mm patterns (the X500's motor mounts, [Holybro](https://holybro.com/products/px4-development-kit-x500-v2)) |
| Legs ×4 | 12 mm tube, 250 mm, with a foot | Tall enough to clear hanging darts. **Meant to break before an arm does:** a leg is a 30-minute reprint |
| Wheelbase | 450 mm | 10-inch props are about 318 mm apart between neighbouring motors, so they clear |

**Estimated frame mass ~380 g** (CAD volume × PETG density × 0.75 fill), against 610 g for the X500 frame. A printed frame flexes more than carbon. Arm stiffness and vibration at the flight controller are the first things to check, through ArduPilot's vibration logs.

### Payload and flight time (estimates)

Hover power for fixed props grows with mass to the power 1.5, by momentum theory. The anchor is Holybro's **18 minutes' hover with no payload on a 4S 5,000 mAh pack** ([Holybro](https://holybro.com/products/px4-development-kit-x500-v2)). Holybro doesn't publish the X500's all-up weight with that pack, so it is bracketed at **1.6–1.8 kg** (our estimate). Reach assumes 10 m/s, a 20% reserve and an out-and-back flight. Hover is the slower case, since forward flight usually costs a little less.

| Carrier | Darts | All-up (kg) | Hover (min) | Line reachable, km out |
|---|---|---|---|---|
| X500 + harness | 2 | 2.14–2.34 | 11.7–12.2 | 2.8–2.9 |
| X500 + harness | 3 | 2.33–2.53 | 10.2–10.8 | 2.5–2.6 |
| X500 + harness | 4 | 2.52–2.72 | 9.1–9.7 | 2.2–2.3 |
| Printed TL-1 | 2 | 1.76–1.96 | 15.6–15.9 | 3.7–3.8 |
| Printed TL-1 | 3 | 1.95–2.15 | 13.3–13.8 | 3.2–3.3 |
| Printed TL-1 | 4 | 2.15–2.35 | 11.6–12.1 | 2.8–2.9 |

**What this changes:**

- A 2-line, 24-listener kit at 4 per sortie is 6 sorties. At 3 km out with the TL-1 it is 8 sorties of 3. Either way it's one night's work for one crew (estimate).
- Lines 4 km out need the TL-1 with 2 darts, or a fixed-wing carrier. Printed fixed-wing airframes such as Eclipson's take off at 0.5–1.5 kg ([air-rc](https://www.air-rc.com/aircraft/Eclipson-Airplanes_Apex_apex)) but publish no payload or endurance, so a fixed-wing stays unscoped until T13 shows whether 3 km is enough.
- T13 now has a prediction to beat: **X500, 4 darts, about 9–10 minutes' hover.**

## Parts to buy for 4 darts and the harness

Every Amazon listing was opened in a browser on 2026-10-15 and showed Add to Cart at the price given. Electronics already on the [MVP list]({{ site.baseurl }}{% link mvp.md %}#shopping-list) (Heltec boards, INMP441) are not repeated.

| Qty | Part | Buy | Alternative | Price |
|---|---|---|---|---|
| 1 | PETG 1.75 mm, 1 kg (enough for ~8 darts and the harness, est.) | [Overture, Amazon](https://www.amazon.com/dp/B0991YSBDG) | | $17.99 |
| 1 | SG90 servos, 10-pack | [Miuzei, Amazon](https://www.amazon.com/dp/B072V529YD) | [Hosyond 10-pack, Amazon](https://www.amazon.com/dp/B09GFN98X9), $15.99 | $19.99 |
| 1 | 8.5 mm fibreglass shock-cord pole kit: 4 × 25.5 in sections, cord, ferrules. Cut to 160 mm and re-ferrule | [Eureka!, Amazon](https://www.amazon.com/dp/B001DBFA0U) | | $29.95 |
| 1 | 6 mm × 300 mm stainless rod, 2-pack (6 spikes) | [uxcell, Amazon](https://www.amazon.com/dp/B082ZNKJ5B) | | $9.99 |
| 1 | Torsion spring assortment, 45 pcs (hinge) | [Swpeet, Amazon](https://www.amazon.com/dp/B0D94766KX) | | $10.99 |
| 1 | M3 socket bolts and nuts (dart hinge) | [Hilitchi 420 pcs, Amazon](https://www.amazon.com/dp/B014OO5KQG) | [Glarks 510 pcs, Amazon](https://www.amazon.com/dp/B08HHZHXTP), $14.99 | $15.89 |
| 1 | Fur windscreens, 5 + 5 foam | [Cubilux, Amazon](https://www.amazon.com/dp/B0B2D836LY) | [Ruittos 5-pack, Amazon](https://www.amazon.com/dp/B07BQ2LZDX), $8.99 | $9.99 |
| 4 | 18650 cells (not on Amazon) | [Molicel P28A, 18650 Battery Store](https://www.18650batterystore.com/products/molicel-p28a) | as on the MVP page | $5.99 each |
| | **Total** (zip ties assumed owned) | | | **≈ $139** |

## 4. Not yet designed

- **Edge receiver mount:** a pole-top box for a receive-only Heltec, an RS-485 module and a Yagi clamp, from the [edge receiver design]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees). It follows T17's bench version.
- **X500 leg extensions:** once the leg tube is measured.
- **A custom listener board:** it shrinks the head pod and fixes the sleep current (see [wake-on-sound]({{ site.baseurl }}{% link build-software.md %}#1-listener-firmware)).

## Files

| Model | Script | Printable outputs (STL and STEP) | Render |
|---|---|---|---|
| Dart | [`cad/dart.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/dart.py) | `dart_body`, `dart_cap`, `dart_hinge`, `dart_pod` | `dart-deployed.png`, `dart-stowed.png` |
| X500 harness v1 | [`cad/harness_simple.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/harness_simple.py) | `harness_simple_plate`, `dart_cap` (notched) | `harness-simple.png`, `harness-simple-latch.png` |
| X500 harness v0 (fallback) | [`cad/harness.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/harness.py) | `harness_plate`, `harness_saddle`, `harness_release_block` | `harness-x500.png`, `harness-x500-close.png` |
| TL-1 | [`cad/quad.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/quad.py) | `quad_hull`, `quad_arm`, `quad_leg` | `quad-tl1.png` |
| Shared | [`cad/params.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/params.py), [`cad/render.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/render.py) | | |

STL and STEP files are in [`cad/out/`](https://github.com/paulrenzi/drone-detection-research/tree/main/cad/out).
