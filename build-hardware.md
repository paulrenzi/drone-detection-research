---
title: "Build: hardware"
nav_order: 1.6
---

# Build: hardware, the dart, the harness and a printed carrier
{: .no_toc }

Printable designs for the [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}):

- **v3, the current design:** each dart is a fibreglass rod, one printed body and a head pod: 3 parts. It hangs from v2's one-servo harness unchanged. A 4-dart kit has 15 parts against v2's 27, and the parts list is about $50 against $63.
- **v2:** the one-rod dart with a separate clip, a zip tie and foam. Its harness is still the current one.
- **v1, superseded:** a folding-mast dart and a four-servo harness, kept below for its drop-test questions and as a fallback.
- **A fully printed carrier quad (TL-1):** built round the X500's electronics.

Software: [Build: software]({{ site.baseurl }}{% link build-software.md %}).

{: .warning }
> **Version 0 designs, never printed or flown.** Dimensions from datasheets are sourced; masses, flight times and impact figures are estimates from the models and labelled as such. Parts marked *measure* in [`cad/params.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/params.py) must be checked with calipers before printing.

1. TOC
{:toc}

## Short answer

| | v3 dart | v2 X500 harness | Printed TL-1 quad |
|---|---|---|---|
| Printed parts | 2 (body, head pod) | 2 (plate, rotor) | Hull, 4 arms, 4 legs |
| Mass (est.) | ~127 g each, with an 18650 cell | ~80 g with its one servo | ~380 g frame, against 610 g for the X500 frame ([Holybro](https://holybro.com/products/px4-development-kit-x500-v2)) |
| Hover time with 4 darts (est.) | n/a | **11.3–11.8 min** (v1: 9–10) | 11.5–12 min with v1 darts |
| Reach with 4 darts (est.) | n/a | **~2.7–2.8 km out** (v1: 2.2–2.3) | ~2.8–2.9 km out with v1 darts |
| Fits the Vyper's 245 × 245 × 260 mm bed | Yes | Yes | Yes, every part |

- **An X500 carries four v3 darts about 2.7 km out,** the same as v2: the dart weighs about the same. Lines 3–4 km out need fewer darts per sortie, a bigger pack, or a fixed-wing. That is T13's question, now with numbers to test against.
- **The printed quad wins on mass, not money.** The frame cost saving is small, as [the tripwire says]({{ site.baseurl }}{% link models/tripwire.md %}#why-3d-print-the-drones-and-the-nodes). But an estimated ~230 g lighter frame is worth about 2.5 more minutes of hover with four darts, and the dart bay is built into the hull.
- **Print the dart first.** It is needed for T10 (drop test), T11 (range at 0.5–1 m) and T12 (battery), whichever drone carries it.

## The printer and the CAD

- **Printer: Anycubic Vyper.** Build volume 245 × 245 × 260 mm, nozzle up to 260 °C, bed up to 110 °C. Officially it prints PLA, PETG, TPU, ABS and wood fill ([spec, via 3DSourced](https://www.3dsourced.com/3d-printer-reviews/anycubic-vyper-test-review-specs/)). It has no enclosure, so print in **PETG**: it tolerates sun and heat better than PLA and prints well without an enclosure (inference). Carbon-filled nylon and ASA, the usual next step for arms, warp without an enclosure and need a hardened nozzle. That is a second printer, needed only after the prototype stage.
- **CAD: CadQuery,** text-based and in Python. Every model is a script in [`cad/`](https://github.com/paulrenzi/drone-detection-research/tree/main/cad) that reads its dimensions from one file, `cad/params.py`, so a change shows up as a readable diff. Each run writes STL (for slicing), STEP (for any other CAD tool) and the PNG renders on this page, and prints bed-fit checks, masses and the flight-time table. Install: `python -m venv cad-env` then `cad-env/Scripts/pip install cadquery`. Run `python v2.py`, `dart.py`, `harness_simple.py` or `quad.py` from `cad/`.

## 1. v3: three parts per dart

<img src="{{ site.baseurl }}/assets/images/build/v3-harness.png" alt="Four v3 darts under the X500's rails on the v2 plate and rotor: each dart is a fibreglass rod with one long orange printed body, holding the cell near the tip and the hanger post at the balance point, and a blue head pod at the back; one dart is falling" width="760">

<p style="display:flex;gap:1rem;align-items:flex-end;flex-wrap:wrap">
<img src="{{ site.baseurl }}/assets/images/build/v3-body.png" alt="The v3 body as printed, lying on its flat underside: an open cell cradle at one end, a sleeve along the rod, and the hanger post with its round head at the other end" width="500">
<img src="{{ site.baseurl }}/assets/images/build/v3-dart.png" alt="v3 dart standing in soil: bare rod tip in the ground, the orange body from the surface up to the hanger post, and the blue head pod with its whip at the top" width="160">
</p>

*Top: four darts on v2's harness, with the first one falling. Left: the body as it prints, cradle open on top. Right: a dart in soil.*

**v3 changes only the dart.** v2's plate, rotor and servo carry it as they are: the hanger head is the same round head on the same radius. The model reruns v2's checks with v3 darts: each dart stays on the rim until its own step, drops at it, and nothing collides at any angle.

**Each dart is a rod, one printed body and the head pod.**

- **The body is one print: nose, cell cradle, sleeve and hanger.** The 18650 presses down into an open cradle whose lips are 15.8 mm apart, narrower than the 18.6 mm cell, so it snaps in and the cradle wraps 251° round it. That replaces v2's zip tie. A sleeve runs back along the rod to the hanger post, which the model places at the balance point, 246 mm from the tip. That replaces v2's separate clip, which had to be glued at a measured spot.
- **No foam.** The mic looks out of a side port under a small printed hood on the pod.
- **It prints lying on its flat underside,** post and cradle opening up, with no supports. It is 186 mm long and weighs about 22 g (estimate).

| | v2 | **v3** |
|---|---|---|
| Parts per dart | 6 (rod, body, clip, pod, foam, zip tie) | **3 (rod, body, pod)** |
| Parts in a 4-dart kit with the harness | 27 | **15** |
| Glue joints set at a measured spot | 1 per dart (clip at the balance point) | **0** |
| Dart mass (est.) | ~126 g | ~127 g |
| Parts to buy for 4 darts and the harness | ≈ $63 | **≈ $50** |

**What it costs in performance:**

- **It still rides flat and must turn point-down as it falls** (T10). The balance point is 44% of the length from the tip, against v2's 45%.
- **No windscreen** means more wind noise. T11 should measure with and without foam. If foam is needed, it's $0.50 a dart and one part back.
- **The balance point is fixed in the print.** If the real board and wiring weigh more or less than the estimates, the dart hangs slightly nose- or tail-low; the plate slot keeps the post upright. The fix is to weigh one assembled dart, put the masses into `v3.py` and reprint the body.
- **The cradle has to hold the cell at landing.** The impact pushes the cell into the solid nose wall, not out through the snap, but T10 should check it.
- **Samsung 25R cells hold 2,500 mAh against the P28A's 2,800,** about 11% less battery, for $1 less each. The Samsung 35E holds 3,500 mAh for $5.99.

**Why the cost fell by a fifth, not by half.** The cells are $20 of the $50, and filament, rods and servos come in packs bigger than one kit needs. Per 4-dart re-lay, the bill is about $26.50: cells $20, rods $4.40 and about $2 of filament (estimates from the model's masses), against about $33 for v2. **The rest of the cost is the cells.** EVE 35V cells (3,500 mAh) were listed at $2.50–2.99 but were sold out on 2026-10-15 at both [18650 Battery Store](https://18650batterystore.com/products/eve-35v-18650-3500mah-10a-battery) and [IMR Batteries](https://imrbatteries.com/products/eve-35v-18650-3500mah-10a-battery). In stock, they would bring a re-lay to about $16.50 (half of v2's) and the parts list to about $40.

**Wiring and mission:** as v2: Pixhawk AUX 1, one `DO_SET_SERVO` step per dart.

*Measure before printing:* as v2, plus the cell's real diameter. The snap needs the lips narrower than the cell, and the 25R measures 18.4 mm, not 18.6.

## 2. v2: one rod, one servo

v3 keeps v2's plate, rotor and servo as they are; only the dart changed. v2's dart is the fallback if the snap cradle or the fixed hanger position fails.

<img src="{{ site.baseurl }}/assets/images/build/v2-harness.png" alt="v2 harness under the X500's two rails: a round printed plate with a dark rotor on top, four darts lying flat beneath it, each a long fibreglass rod with an orange cell body near the tip, a blue clip near the middle and a blue head pod at the back; one dart is falling" width="760">

<p style="display:flex;gap:1rem;align-items:flex-end;flex-wrap:wrap">
<img src="{{ site.baseurl }}/assets/images/build/v2-rotor.png" alt="Top of the plate: the dark rotor with four gaps in its rim; three clip heads rest on the rim, and the fourth slot is empty because its dart has dropped through the gap" width="440">
<img src="{{ site.baseurl }}/assets/images/build/v2-dart.png" alt="v2 dart standing in soil: bare rod tip in the ground, orange cell body at the surface, blue clip halfway up, blue head pod with foam and whip at the top" width="160">
</p>

*Top: four darts under the X500's rails, with the first one falling. Left: the rotor after the first step; that dart's slot is empty. Right: a dart in soil, about 0.5 m to the mic.*

**The dart is one rod with three printed parts on it.** A single 6 × 500 mm solid fibreglass rod is the spike, the spine and the mast.

- **Body:** slides on from the tip and holds the 18650 low, next to the rod, 70 mm back from the point. A zip tie through the back closes the cell bay. Soil stops at the body, so at most 70 mm of rod goes in.
- **Clip:** slides on and is glued where the dart balances, about 253 mm from the tip (model). It is the hanger: a post with a round head.
- **Head pod:** a thin printed shell on the rod's top end, holding the Heltec upright, with the mic under foam and the whip out of the top.

**The harness is one plate, one rotor and one servo.**

- The plate sits on two printed posts zip-tied to the X500's rails. Each dart's clip comes up through a slot in it.
- The clip's round head rests on the rim of a printed rotor, which is screwed to the servo horn. A printed ring on the plate carries the rotor, so the darts' weight goes into the plate, not the servo.
- **The rim has one gap per dart, each at a different angle.** The servo turns 16° per step. Each step brings exactly one gap under its dart's head, and that dart drops through its slot. The model checks every angle from rest to 64°: each dart stays on the rim until its own step and is free at it, and nothing collides at any angle.
- The inner pair drops first, one each side, then the outer pair, so the load stays balanced.
- **To load,** turn the rotor to 64° and fit the last dart, then step back to 48°, 32° and 16° for the third, second and first, then to rest. No gap passes a loaded head on the way down.

**What v2 removed:**

| | v1 | **v2** |
|---|---|---|
| Printed parts per dart | 4 (body, cap, hinge, pod) | **3 (body, clip, pod)** |
| Other parts per dart | steel spike, 4 pole sections, shock cord, spring, bolt, nut, fur | **1 fibreglass rod, foam, zip tie** |
| Joints that must move in flight, per dart | 5 (hinge + 4 pole joints) | **0** |
| Harness | plate + 4 servos | **plate + rotor + 1 servo** |
| Servo outputs on the Pixhawk | 4 | **1** |
| Parts in a 4-dart kit, excluding cells and electronics | 61 | **27** |
| Dart mass (est.) | ~195 g | **~126 g** |
| Darts hang below the rail axis | ~219 mm: needs 60–80 mm leg extensions | **~71 mm: stock legs** |
| Parts to buy for 4 darts and the harness | ≈ $139 | **≈ $63** |

**What it costs in performance:**

- **The mic sits lower,** about 0.49 m above soil if the body reaches the ground, against about 0.8 m for v1. That is still inside the 0.5–1 m T11 tests, at its bottom edge. A 420 mm rod (the cheaper alternative below) gives about 0.42 m.
- **Foam instead of fur** means more wind noise. A fur cover can be added later for about $2 each.
- **The darts ride flat, so each one must turn point-down as it falls.** The cell sits forward and the pod and foam drag at the back. The balance point is 45% of the length from the tip, which should make it fall like a shuttlecock or lawn dart (inference). Whether it turns in 5–15 m of fall is now T10's first question. If it doesn't, hang the clip a little ahead of the balance point so the dart leaves the drone nose-down.
- **One rotor drives all four darts,** so if it jams, the rest of that sortie's darts stay on. With v1, a stuck servo cost one dart. Bench-test it: 50 load-and-release cycles with 130 g dummies, then a shake test.
- **The footprint is longer:** the darts are about 0.77 m long with the whip, so they likely reach past the props fore and aft (estimate; Holybro doesn't publish the overall length). They ride about 70 mm under the rails.

**Wiring and mission:** one output, Pixhawk AUX 1, with `SERVO9_FUNCTION = 0`. Each drop point gets a `DO_SET_SERVO` (183) with p1 = 9 and p2 = that step's PWM. On an SG90's roughly 1,000–2,000 µs span for 180° (typical; calibrate on the bench), 16° is about 180 µs, so steps are about rest + 180, 360, 540 and 720 µs.

*Measure before printing:* how high the SG90's shaft stands above its tabs, which sets the rotor height (sand the ring to match), the rail spacing, and the rod's real diameter.

## 3. v1 dart: folding mast (superseded by v2)

v1 is kept because its drop-test questions still apply to v2, and as a fallback if a flat-carried dart won't turn point-down.

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

## 4. v1 harness: four servos (superseded by v2)

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

## 5. A fully printed carrier: TL-1

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
| **X500 + v2 harness, v2 darts** | 2 | 1.93–2.13 | 13.6–14.0 | 3.3–3.4 |
| **X500 + v2 harness, v2 darts** | 3 | 2.06–2.26 | 12.3–12.8 | 3.0–3.1 |
| **X500 + v2 harness, v2 darts** | 4 | 2.18–2.38 | 11.3–11.8 | 2.7–2.8 |
| X500 + v0 harness, v1 darts | 2 | 2.14–2.34 | 11.7–12.2 | 2.8–2.9 |
| X500 + v0 harness, v1 darts | 3 | 2.33–2.53 | 10.2–10.8 | 2.5–2.6 |
| X500 + v0 harness, v1 darts | 4 | 2.52–2.72 | 9.1–9.7 | 2.2–2.3 |
| Printed TL-1, v1 darts | 2 | 1.76–1.96 | 15.6–15.9 | 3.7–3.8 |
| Printed TL-1, v1 darts | 3 | 1.95–2.15 | 13.3–13.8 | 3.2–3.3 |
| Printed TL-1, v1 darts | 4 | 2.15–2.35 | 11.6–12.1 | 2.8–2.9 |

**What this changes:**

- A 2-line, 24-listener kit at 4 per sortie is 6 sorties. At 3 km out with the TL-1 it is 8 sorties of 3. Either way it's one night's work for one crew (estimate).
- Lines 4 km out need the TL-1 with 2 darts, or a fixed-wing carrier. Printed fixed-wing airframes such as Eclipson's take off at 0.5–1.5 kg ([air-rc](https://www.air-rc.com/aircraft/Eclipson-Airplanes_Apex_apex)) but publish no payload or endurance, so a fixed-wing stays unscoped until T13 shows whether 3 km is enough.
- T13 now has a prediction to beat: **X500, 4 v2 darts, about 11–12 minutes' hover.** The v2 rows use the model's masses: 126 g per dart, 80 g for the harness.

## 6. Parts to buy: v3, 4 darts and the harness

Every Amazon listing was opened in a browser on 2026-10-15 and showed Add to Cart at the price given. Electronics already on the [MVP list]({{ site.baseurl }}{% link mvp.md %}#shopping-list) (Heltec boards, INMP441) are not repeated.

| Qty | Part | Buy | Alternative | Price |
|---|---|---|---|---|
| 1 | PETG 1.75 mm, 1 kg (plate, rotor and 4 darts use about 0.25 kg, est.) | [SUNLU, Amazon](https://www.amazon.com/dp/B0DJS3PJVX) | [Overture, Amazon](https://www.amazon.com/dp/B0991YSBDG), $17.99 | $13.99 |
| 1 | Solid fibreglass rod, 6 mm × 500 mm, 10-pack (one rod per dart) | [LLZZQQF, Amazon](https://www.amazon.com/dp/B0FNZQLH1P) | [6 × 420 mm 10-pack, Amazon](https://www.amazon.com/dp/B0CGLMZSTG), $9.99; mic about 0.42 m | $11.00 |
| 1 | SG90 servo, 2-pack (one fitted, one spare) | [Amazon](https://www.amazon.com/dp/B0DFKPVRC2) | [Beffkkip 3-pack, Amazon](https://www.amazon.com/dp/B0G6R7ZZXH), $6.99 | $4.99 |
| 4 | 18650 cells (not on Amazon) | [Samsung 25R, 2,500 mAh, 18650 Battery Store](https://www.18650batterystore.com/products/samsung-25r-18650) | [Samsung 35E, 3,500 mAh](https://www.18650batterystore.com/collections/18650-batteries), $5.99; [Molicel P28A](https://www.18650batterystore.com/products/molicel-p28a), $5.99 | $4.99 each |
| | **Total** (CA glue assumed owned) | | | **≈ $50** |

**Where v2's $13 went:** the foam ($4.99), a cheaper spool of the same PETG ($4.00 less), and cheaper cells ($4.00 less for four). If T11 shows foam is needed: [Phinus 10-pack, Amazon](https://www.amazon.com/dp/B07X4VKKQ7), $4.99.

**Where v1's $76 went (v1 to v2):** the folding mast (pole kit $29.95, springs $10.99, M3 hardware $15.89), the steel spike ($9.99), three of four servos (a 2-pack replaces a 10-pack), and fur (foam instead). v1's list was PETG, a 10-pack of SG90s, the pole kit, stainless rod, springs, M3 hardware, fur and cells, ≈ $139.

## 7. Not yet designed

- **Edge receiver mount:** a pole-top box for a receive-only Heltec, an RS-485 module and a Yagi clamp, from the [edge receiver design]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees). It follows T17's bench version.
- **X500 leg extensions:** only for v1 darts; v2 darts ride high enough for stock legs.
- **TL-1 with the v2 plate:** the hull still carries v1's release blocks and tall legs.
- **A custom listener board:** it shrinks the head pod and fixes the sleep current (see [wake-on-sound]({{ site.baseurl }}{% link build-software.md %}#1-listener-firmware)).

## Files

| Model | Script | Printable outputs (STL and STEP) | Render |
|---|---|---|---|
| Dart | [`cad/dart.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/dart.py) | `dart_body`, `dart_cap`, `dart_hinge`, `dart_pod` | `dart-deployed.png`, `dart-stowed.png` |
| **v3 dart** | [`cad/v3.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/v3.py) | `v3_dart_body`, `v3_dart_pod` (harness: v2's `v2_plate`, `v2_rotor`) | `v3-harness.png`, `v3-body.png`, `v3-dart.png` |
| v2 dart and harness | [`cad/v2.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/v2.py) | `v2_dart_body`, `v2_dart_clip`, `v2_dart_pod`, `v2_plate`, `v2_rotor` | `v2-harness.png`, `v2-rotor.png`, `v2-dart.png` |
| X500 harness v1 | [`cad/harness_simple.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/harness_simple.py) | `harness_simple_plate`, `dart_cap` (notched) | `harness-simple.png`, `harness-simple-latch.png` |
| X500 harness v0 (fallback) | [`cad/harness.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/harness.py) | `harness_plate`, `harness_saddle`, `harness_release_block` | `harness-x500.png`, `harness-x500-close.png` |
| TL-1 | [`cad/quad.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/quad.py) | `quad_hull`, `quad_arm`, `quad_leg` | `quad-tl1.png` |
| Shared | [`cad/params.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/params.py), [`cad/render.py`](https://github.com/paulrenzi/drone-detection-research/blob/main/cad/render.py) | | |

STL and STEP files are in [`cad/out/`](https://github.com/paulrenzi/drone-detection-research/tree/main/cad/out).
