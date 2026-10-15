---
title: "Use case — Drone-laid tripwire"
parent: Sensor Models
nav_order: 0
---

# Use case — Drone-laid tripwire
{: .no_toc }

| Feasibility | Payoff | Technical readiness | Cost per km² | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|:-:|
| **3/5** | **5/5** | 3/5 | 4/5 | 4/5 | 4/5 |

**Kit cost (est.):** about $1,500–2,500 for 24 throwaway listeners plus one reusable, 3D-printed delivery drone

**Best against:** low FPVs and small quads heading for a unit, including fibre-optic FPVs that emit no radio

**One-line verdict:** Don't try to make a microphone hear farther. Put cheap ones farther out. A unit gets about a minute of warning instead of about ten seconds, without transmitting anything while it listens.

**Payoff:** The only option here that gives about a minute of warning against fibre-optic FPVs at a price units can afford.

1. TOC
{:toc}

## The problem it solves

A microphone hears a small FPV at roughly **100–300 m** ([working estimate]({{ site.baseurl }}{% link research/range-and-cost.md %})). Better hardware barely moves that: even premium arrays top out at a few hundred metres. A sensor ring placed by hand around a position therefore gives only seconds of warning.

Warning time is **distance from the unit ÷ drone speed**, not detection range. So move the listeners forward.

| Where the listeners sit | Warning against an FPV at 30–40 m/s |
|---|---|
| Ring placed by hand, ~300 m out | ~8–10 seconds |
| Line laid by drone, 2 km out | ~50–65 seconds |
| Line laid by drone, 4 km out | ~1.5–2 minutes |

{: .warning }
> FPV speeds and detection ranges are planning estimates, not field measurements. The ratio is what matters: ten times the distance is roughly ten times the warning.

Ten seconds is enough to flinch. A minute is enough to take cover, cue a camera and launch an interceptor.

## How it works

### 1. Lines, not coverage

Drones attacking a unit mostly come from one direction: the enemy side. Covering the whole area against small drones would take thousands of nodes ([the density problem]({{ site.baseurl }}{% link research/range-and-cost.md %}#worked-examples)). A tripwire only has to cover the **approach corridors**.

- **One line** across the approach, 2–4 km out, says *something crossed here, at this time*.
- **A second line** a few hundred metres behind it adds **heading and speed**, and filters false alarms: a real drone trips both lines in order.
- Locating the drone precisely is left to the dense ring near the unit ([M1]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) on [M4]({{ site.baseurl }}{% link models/m04-elevated-nodes.md %}) placements). The far line only has to raise the alarm and say which way to look.

A node in a line only has to hear the drone, not fix its position, so nodes can be spaced at roughly their detection range: about every 200–300 m against FPVs. A 3 km front then takes about 12 nodes per line, or 24 for two lines.

### 2. Throwaway listeners

{: .note }
> Open-source starting points exist: [Batear]({{ site.baseurl }}{% link research/open-source-builds.md %}#batear) (MIT licence) already runs a single-mic harmonic detector with encrypted LoRa alerts on an ESP32-S3, and [VolAnti]({{ site.baseurl }}{% link research/open-source-builds.md %}#volanti) has published a 104 m range test. See [Open-source projects to build on]({{ site.baseurl }}{% link research/open-source-builds.md %}).

Each listener is a single-microphone node ([M3]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}) class) built to be dropped, not placed:

- **Dart body** that sticks upright in soil, with a **spring mast** that lifts the microphone 0.5–1 m off the ground. A microphone lying in grass hears much worse.
- **Wake on sound.** A low-power trigger listens all the time; the microcontroller, classifier and radio wake only when something drone-like is heard. The target is **weeks on a small battery**.
- **No recovery.** Nodes are consumables, like ammunition. Lost, found or dead nodes are simply replaced by the next sortie.
- **Target bill of materials: $30–60** (microcontroller, MEMS microphone, LoRa radio, battery, printed body). No GPS: see [Solving the field limits](#solving-the-field-limits-at-no-extra-cost). See [Hardware]({{ site.baseurl }}{% link research/hardware.md %}).

### 3. A cheap delivery drone

A small quadcopter carries **3–4 nodes**, flies a pre-planned GPS route, drops each node on its point and returns. Six sorties lay two lines across a 3 km front.

- **Autonomous, not piloted.** It runs a pre-planned mission on open-source autopilot firmware such as ArduPilot, with no video feed. Each drop is a step in the mission, and ArduPilot can be set to finish the mission with every radio link off. That means no operator skill is needed, and nothing is broadcasting while the line is laid. Airframes, software and how it handles GPS jamming: [Delivery drone]({{ site.baseurl }}{% link research/delivery-drone.md %}).
- **Reusable**, but cheap enough to lose.
- At the end of its life, a delivery drone can be landed on high ground and left as a relay (see below).

### 4. Reports find their way back

Nodes send a few-byte detection report (time, node ID, class, confidence, plus a short description of the sound and the node's battery level) only when they hear something. Reports hop node to node down the line and back toward the unit, where a raised receiver on a mast or [aerostat]({{ site.baseurl }}{% link models/m05-aerostats.md %}) collects them and feeds the shared map, TAK and [Lattice]({{ site.baseurl }}{% link research/integration.md %}#anduril-lattice).

### 5. The network grows from the bottom up

Every unit's lines report to the same shared map. As units lay their own tripwires, the lines add up to a broader network that nobody had to plan or fund centrally: Sky Fortress-style coverage, grown out of kits that units carry.

## Components and MVP

### What goes in one node

| Part | Example | Est. cost | Why it's there |
|---|---|---|---|
| Microcontroller | ESP32-S3 | $4–10 | Runs the drone / no-drone classifier on the device, so only a few bytes are sent |
| Microphone | INMP441 or ICS-43434 (I²S digital MEMS) | $1–3 | One mic is enough: a line node only has to hear, not take a bearing |
| LoRa radio | SX1262, 915 MHz in the US | $6–25 | Sends the report and relays neighbours' reports back toward the unit |
| GPS | none | $0 (was $8–15) | Dropped: it would be jammed where it matters most. Position comes from the drop plan and the delivery drone's log, time from neighbouring nodes ([why](#solving-the-field-limits-at-no-extra-cost)) |
| Battery | small LiPo cell | ~$3–8 (estimate) | Weeks, not days, only if the node sleeps until it hears something |
| Body, spring mast, battery housing | 3D-printed | $1–2 in filament | Sticks upright and holds the mic 0.5–1 m up |
| Windscreen | fur or foam cover | ~$1–3 (estimate) | Wind is the biggest range-killer in [VolAnti's tests]({{ site.baseurl }}{% link research/open-source-builds.md %}#volanti) |
| **Total** | | **~$17–50** | Against the **$30–60 target** above (~$25–65 with GPS) |

{: .warning }
> Part prices come from [Hardware]({{ site.baseurl }}{% link research/hardware.md %}); the battery and windscreen figures are estimates. All are hobby-grade, small-volume prices. A board that already combines the ESP32-S3 and LoRa radio, such as the Heltec WiFi LoRa 32 V3, costs about $25–30 and is the easiest way to build the first nodes.

### The MVP, step by step

Each step answers one question before money goes into the next. The steps match the tests in [Open questions](#open-questions).

| Step | What you build | What it proves | Rough cost |
|---|---|---|---|
| **1. Weekend test kit** | 2 Heltec V3 boards running [Batear]({{ site.baseurl }}{% link research/open-source-builds.md %}#batear), 3 INMP441 mics, windscreens, phones as recorders | A cheap mic hears a drone at known distances; first labelled training audio; a first LoRa range figure in your terrain | **~$80–90** with a borrowed drone, tripods and power banks; ~$360–480 buying everything |
| **2. Radio range test (T9)** | The same two boards, one carried away from a raised receiver | Whether a line 2–4 km out can report back at all. **The deciding question** | < $300 |
| **3. Node on a mast (T10, T11)** | One node on a 0.5–1 m spring mast, plus a drop-tested printed dart body | Detection range at node height (sets node spacing), and whether nodes land upright | < $500 |
| **4. Battery test (T12)** | One node with wake-on-sound and a small classifier | Whether "weeks on a small battery" is real | < $200 |
| **5. Drop sortie (T13)** | A printed quad that lays 4 nodes on GPS points | Placement accuracy and payload | < $500 |

### Parts for step 1

{: .warning }
> Prices are rough US figures checked in October 2026 and change often. Parts marked "ships from China" won't arrive in days. The "step 2" recorder board below is the kit's own later upgrade, not MVP step 2.

{% include kit-parts.html %}

Buying advice and a full weekend plan for step 1 are in the [weekend test kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector).

## Why 3D-print the drones (and the nodes)

The honest answer: **printing doesn't make the drone much cheaper, but it makes the whole system easier to field.**

| Part of a small delivery quad | Estimated cost |
|---|---|
| Motors (4) | $40–80 |
| Electronic speed controllers | $25–40 |
| Flight controller | $20–40 |
| GPS / compass | $10–20 |
| Control receiver | $10–20 |
| Battery | $20–40 |
| Frame: carbon fibre | $20–40 |
| Frame: 3D-printed | **$3–8** in filament |

{: .warning }
> Rough estimates for hobby-grade parts at small volume. Real prices depend on volume and sourcing, and parts for military use may face supply-chain and country-of-origin rules.

The electronics are about 85–90% of the drone's cost, so a printed frame saves around $15–35 per drone. Where printing really pays off:

- **The nodes, not the drone.** Every node needs a dart body, a spring mast mount and a battery housing. Printed, each costs a dollar or two and needs no tooling. Nodes are consumed by the hundred, so this is where the savings add up.
- **The drop mechanism.** The release clips and cargo racks are small custom parts, which is exactly what printers are good at.
- **Making and fixing kits near the front.** A unit or depot with a printer can rebuild frames and print node bodies from a file, without waiting on a supply chain. Ukraine already prints drone parts at scale.
- **Fast design changes.** When drop tests show a dart breaks or tips over, the fix ships as a new file that day.

A further option worth testing is a **printed fixed-wing** carrier. Fixed-wing aircraft fly much farther on the same battery and don't need to hover, which suits simply dropping nodes along a line.

## Why this beats the alternatives, for this job

The claim is narrow: **for early warning of low drones approaching a unit, including drones that emit no radio.** It does not beat everything at everything.

| | Fibre-optic FPV | Behind trees or a ridge | Warning time vs FPV | Emits while watching | Rough cost | A unit can carry it |
|---|:-:|:-:|---|:-:|---|:-:|
| **Drone-laid tripwire** | ✅ | ✅ | **~1–2 min** | ❌ | **~$1.5–2.5k kit** | ✅ |
| Hand-placed acoustic ring | ✅ | ✅ | ~10 s | ❌ | similar | ✅ |
| Radio detector (e.g. Chuyka) | ❌ | partly | long, if it emits | ❌ | ~$750–850 | ✅ |
| Camera (e.g. WISP) | ✅ if in sight | ❌ | depends on sight lines | ❌ | far higher | ❌ |
| Radar | ✅ if in sight | ❌ | long, if in sight | **✅** | $40k–160k | ❌ |
| Phone network (Sky Fortress) | ✅ | ✅ | ~10 s for FPVs near the unit | **✅** (cellular) | $400–1,000 per sensor | ❌ |

It works best **alongside** the others, not instead of them. A radio detector still catches radio-controlled FPVs at long range, and the tripwire tells the camera where to look.

### Why not just drop phones?

Phones are the [best-proven acoustic sensor there is]({{ site.baseurl }}{% link models/m02-phone-network.md %}), and for a fixed network in an area with power and cell coverage they still win. For a line dropped 2–4 km forward, purpose-built nodes win on every point that matters:

| | Purpose-built node | Phone |
|---|---|---|
| **Emissions** | Silent until it hears something, then one short burst | A phone keeps checking in with the cell network even when idle, so it can be located. With its radios off, it can't report |
| **Network** | Its own mesh; needs no cell towers | Needs cell coverage, which near the front is jammed, destroyed or watched |
| **Battery** | Wake-on-sound: weeks (target) | Running a microphone and classifier non-stop: about a day on its own battery (estimate) |
| **Weight** | Target well under 100 g, so a small drone carries 3–4 | ~150–200 g plus a mast, so fewer per sortie |
| **Cost per node** | $30–60 (target) | ~$50–100 for even the cheapest phone, plus mount and protection |
| **Survives a drop** | Designed for it | Isn't |
| **Brains** | Only needs "drone-like sound: yes or no" | Can run much bigger classifiers |

The phone's one real advantage is computing power. A tripwire node only has to answer one question, *was that a drone?*, which is a small-classifier job of the kind that already runs on microcontrollers. That still has to be proven on real recordings (see open questions).

Where phones still win: **today**, in rear areas with power and coverage, and as the receiver and display at the unit itself.

## Limits and risks

- **Getting reports back is the hardest part.** Published measurements with antennas near the ground show over 4 km in open country, but only 50–250 m in most forest tests and about 1 km at best. In woods the line would have to relay hop by hop at perhaps 100–200 m, more densely than the spacing assumed above. Nobody has measured a 0.5–1 m node reaching a raised receiver 2–4 km away. See [the evidence and test plan]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back).
- **The relay chain can point home.** A chain of bursts leading back to the unit could be traced. Keep bursts short and rare, bend the chain instead of running it straight, and treat nodes as disposable.
- **Laying the line is noisy.** The delivery drone can be heard and seen, so the enemy may learn roughly where the line is. Lay lines at night or under other noise, and expect to lose some nodes.
- **GPS is jammed at the front.** The delivery drone can't count on GPS to reach its drop points, and nodes can't count on it to report where they landed ([Front-line conditions]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)). A line doesn't need metre accuracy, and a node's position can be taken from the drop point in the mission, but flying the route without GPS is untested (T14).
- **The sky is full of friendly drones.** Ukrainian observation, bomber and resupply drones fly over the same tree lines. A line that alarms on every drone is useless, so it needs a way to tell friend from foe, such as friendly flight schedules or known friendly sound signatures (T15).
- **Tree lines decide the layout.** Infantry, their footpaths and fibre-optic FPVs all follow the windbreak tree lines ([Front-line conditions]({{ site.baseurl }}{% link research/field-conditions.md %}#where-infantry-actually-sit-tree-lines)). That is good for hearing drones, since their routes are predictable, but it makes the forest radio case in T9 the one that matters. Cover and radio paths change when leaves fall.
- **Cold.** Hobby-grade parts are often rated only to about −10 °C. Winter battery life must be measured, not assumed (T12).
- The GPS, friendly-drone, tree-line and cold limits each have a fix that adds no cost and gathers information: see [Solving the field limits](#solving-the-field-limits-at-no-extra-cost).
- **Only drones that cross the line are caught.** A drone launched from inside the line, or one routed around its ends, is missed. The inner ring is still needed.
- **False alarms with nobody to check.** Wind, vehicles and birds can trip a single node. Requiring both lines, or two neighbouring nodes, to agree is the main filter.
- **Litter.** Throwaway nodes are electronic waste left in the field. Consider biodegradable printed bodies and a battery that can't leak.
- **Export controls.** A counter-drone sensor kit may fall under ITAR/EAR once it is built for military use.

## Solving the field limits at no extra cost

The four limits from [front-line conditions]({{ site.baseurl }}{% link research/field-conditions.md %}) (GPS jamming, friendly drones, tree lines and cold) can each be handled with parts the node already has. Each fix also makes the line collect something the unit can use. The node gets cheaper, not dearer, because the GPS comes out.

{: .warning }
> This is a design proposal, not a tested system. The tests that would check it are listed at the end of this section.

### The fixes

| Limit | Fix | What the line learns from it | Extra cost |
|---|---|---|---|
| **GPS is jammed** | Take the GPS off the node. Its position is the planned drop point, corrected by where the delivery drone's flight log says it released. Its clock is set when it is loaded on the drone and kept in step with its neighbours whenever they relay a message. A node's own GPS would be jammed in the same places as the drone's, so it adds little where it matters most | ArduPilot's flight log records GPS fix quality on every flight. Each sortie becomes a survey of where GPS failed or the position jumped along the unit's own routes | **Saves $8–15 per node** |
| **Friendly drones** | Use the two lines the design already has. A drone heading in trips the outer line first; one heading out trips the inner line first. The unit enters its own flight windows on the receiving tablet. An inbound drone outside a friendly window is an alarm; everything else is logged quietly | Each alert carries a few bytes describing the sound: main tone, loudness and how long it lasted. Alerts inside a friendly window are labelled friendly automatically, so the line builds its own labelled examples for training the next batch's classifier | None: a few more bytes per alert |
| **Tree lines** | Lay lines across the tree belts and the gaps between them, spaced closer under canopy. The GPS saving pays for it: the money that bought 12 nodes with GPS buys about 15–17 without | Every received packet already comes with its signal strength and noise level. Logging them for each link shows when leaf fall or new growth changes range, and which links are about to fail | None |
| **Cold** | Don't pay for cold-rated cells up front. Each node adds its battery voltage and chip temperature to packets it already sends, plus a rare stand-alone check-in | Measured winter battery life from the field, which no source we found has published, and a forecast of when each line needs re-laying | None on boards that already read their battery, such as the Heltec V3 (Meshtastic reports its battery level). A custom node needs two resistors, a few cents. The ESP32-S3 has a [built-in temperature sensor](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/temp_sensor.html); it reads the chip, which is close to the air temperature only while the node sleeps |

Cost per node, from the parts table above: **about $17–50 without GPS**, against $25–65 with it.

### What the unit gets

Over weeks, a line turns into a record of drone traffic on the unit's approach:

- **When and where enemy drones come:** time of day, which tree lines and gaps they use, and their speed from the time between the two lines. That tells the unit when to keep under cover and where to point a camera or interceptor. On the shared map, many units' lines show the pattern across a sector.
- **Friendly traffic:** a count of the unit's own flights through the line, useful for checking against neighbouring units' drones.
- **A jamming map** from the delivery drone's logs, updated every sortie.
- **A radio and season map** from link strength, showing where lines need closer spacing and when.
- **Cold-weather battery data**, measured where it matters.
- **Lost nodes as a signal (an inference):** a node that goes quiet while its last battery reading was healthy didn't run flat. It was probably destroyed or found. Where and when that happens is itself a sign of activity.

### Rules that keep it cheap and quiet

- **No new transmissions to gather data.** Sound summaries, battery and temperature ride on alerts and relays the node sends anyway. A stand-alone check-in goes out at most once or twice a day, and the unit can switch it off. Every extra byte adds air time, so keep the extra summary to roughly 10–15 bytes (an estimate).
- **No audio leaves the node.** LoRa is far too slow for it. Raw recordings for training come from the [weekend test kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector) and test ranges, not from the front.
- **Classifier updates go into the next batch of nodes**, not over the air. Nodes are consumables, so each new batch carries what the last one learned.
- **The record lives at the unit's receiver and on the shared map**, not in the nodes.

### What has to be proven

- **Clocks without GPS.** Telling direction from which line trips first needs neighbouring nodes' clocks to agree within about 1–2 seconds for weeks. A drone at 30–40 m/s crosses lines a few hundred metres apart roughly 5–15 seconds apart, and ordinary microcontroller clocks drift by a few seconds a day (both estimates). Syncing with neighbours has to keep up (T15).
- **Direction alone doesn't sort friend from foe.** Friendly drones fly home inbound, and enemy scouts leave outbound. Until T15 shows whether sound can tell them apart, the flight windows carry most of the weight.
- **Positions from the drop plan** are only as good as the drone's navigation (T14).
- **Battery life in cold**, with the extra bytes counted (T12).

## Precedent

The idea is older than it looks. In the Vietnam War, **Operation Igloo White** air-dropped acoustic and seismic sensors (including the ACOUBUOY and SPIKEBUOY) along the Ho Chi Minh Trail and relayed their detections back by aircraft. What's new is that the sensor, the delivery drone and the classifier are now cheap enough to throw away.

## Open questions

| Test | What it answers | Rough cost |
|---|---|---|
| Ground-to-ground LoRa range at 2–3 km, in open ground and in trees, with a raised receiver at the unit ([test plan]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back)) | Can a forward line report back at all? The deciding question. Published data says probably yes in the open; the forest case is unproven | < $300 |
| Drop-test printed dart bodies onto soil, sand, mud and grass | Do nodes land upright and keep the microphone clear? | < $200 |
| FPV detection range for a single microphone on a 0.5–1 m spring mast | How far apart nodes can be | < $300 |
| Wake-on-sound battery life with a small drone classifier on a microcontroller | Is "weeks" real? | < $200 |
| Autonomous drop sortie: 4 nodes on GPS points from a printed quad | Placement accuracy and payload | < $500 |
| The same sortie with GPS unavailable (optical flow, compass and barometer from a known start point) | Can the line be laid under jamming? | < $300 |
| Record friendly drones and test whether the classifier, which line trips first, and friendly flight times can sort friend from foe, with node clocks kept in step without GPS | Will the line cry wolf? | < $200 |

These are tracked in [Open questions]({{ site.baseurl }}{% link research/open-questions.md %}) as T9–T15. What the ground looks like for the units it serves is in [Front-line conditions]({{ site.baseurl }}{% link research/field-conditions.md %}).

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | Each part exists (cheap nodes, autonomous drop drones, LoRa mesh), but nobody has proven forward lines can report back over 2–4 km. Rises to 4 if the radio range test passes. |
| 2026-10-15 | 3 (unchanged) | Reviewed published LoRa range measurements: over 4 km in the open with antennas at 1.5 m, but 1 km or less in forest. The open-ground case looks likely; the forest case needs the [T9 field test]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back), which now has pass/fail criteria. |
| 2026-10-15 | 3 (unchanged) | Reviewed front-line conditions. Fibre-optic FPVs, which radio detectors can't see, and predictable approach routes along tree lines support the payoff. GPS jamming, friendly drones and the forest radio case add work; they are now tests T14, T15 and T9. |
| 2026-10-15 | 3 (unchanged) | Proposed [no-extra-cost fixes](#solving-the-field-limits-at-no-extra-cost) for those limits: drop the node's GPS, sort friend from foe by line order and flight windows, and report battery and temperature. The fixes also turn the line into a record of drone traffic. All untested; rating moves only on test results. |
