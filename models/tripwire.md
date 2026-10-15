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
- **Target bill of materials: $30–60** (microcontroller, MEMS microphone, GPS, LoRa radio, battery, printed body). See [Hardware]({{ site.baseurl }}{% link research/hardware.md %}).

### 3. A cheap delivery drone

A small quadcopter carries **3–4 nodes**, flies a pre-planned GPS route, drops each node on its point and returns. Six sorties lay two lines across a 3 km front.

- **Autonomous, not piloted.** It runs a pre-planned mission on open-source autopilot firmware such as ArduPilot or INAV, with no video feed. That means no operator skill is needed, and no video transmitter is broadcasting while the line is laid.
- **Reusable**, but cheap enough to lose.
- At the end of its life, a delivery drone can be landed on high ground and left as a relay (see below).

### 4. Reports find their way back

Nodes send a few-byte detection report (time, node ID, class, confidence) only when they hear something. Reports hop node to node down the line and back toward the unit, where a raised receiver on a mast or [aerostat]({{ site.baseurl }}{% link models/m05-aerostats.md %}) collects them and feeds the shared map, TAK and [Lattice]({{ site.baseurl }}{% link research/integration.md %}#anduril-lattice).

### 5. The network grows from the bottom up

Every unit's lines report to the same shared map. As units lay their own tripwires, the lines add up to a broader network that nobody had to plan or fund centrally: Sky Fortress-style coverage, grown out of kits that units carry.

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

- **Getting reports back is the hardest part.** Ground-to-ground radio range in trees or rough terrain can fall well under a kilometre. The line has to relay hop by hop, and the raised receiver at the unit matters a lot. This is the most likely point of failure, so it is the first thing to test.
- **The relay chain can point home.** A chain of bursts leading back to the unit could be traced. Keep bursts short and rare, bend the chain instead of running it straight, and treat nodes as disposable.
- **Laying the line is noisy.** The delivery drone can be heard and seen, so the enemy may learn roughly where the line is. Lay lines at night or under other noise, and expect to lose some nodes.
- **Only drones that cross the line are caught.** A drone launched from inside the line, or one routed around its ends, is missed. The inner ring is still needed.
- **False alarms with nobody to check.** Wind, vehicles and birds can trip a single node. Requiring both lines, or two neighbouring nodes, to agree is the main filter.
- **Litter.** Throwaway nodes are electronic waste left in the field. Consider biodegradable printed bodies and a battery that can't leak.
- **Export controls.** A counter-drone sensor kit may fall under ITAR/EAR once it is built for military use.

## Precedent

The idea is older than it looks. In the Vietnam War, **Operation Igloo White** air-dropped acoustic and seismic sensors (including the ACOUBUOY and SPIKEBUOY) along the Ho Chi Minh Trail and relayed their detections back by aircraft. What's new is that the sensor, the delivery drone and the classifier are now cheap enough to throw away.

## Open questions

| Test | What it answers | Rough cost |
|---|---|---|
| Ground-to-ground LoRa range at 2–3 km, in open ground and in trees, with a raised receiver at the unit | Can a forward line report back at all? The deciding question | < $300 |
| Drop-test printed dart bodies onto soil, sand, mud and grass | Do nodes land upright and keep the microphone clear? | < $200 |
| FPV detection range for a single microphone on a 0.5–1 m spring mast | How far apart nodes can be | < $300 |
| Wake-on-sound battery life with a small drone classifier on a microcontroller | Is "weeks" real? | < $200 |
| Autonomous drop sortie: 4 nodes on GPS points from a printed quad | Placement accuracy and payload | < $500 |

These are tracked in [Open questions]({{ site.baseurl }}{% link research/open-questions.md %}) as T9–T13.

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | Each part exists (cheap nodes, autonomous drop drones, LoRa mesh), but nobody has proven forward lines can report back over 2–4 km. Rises to 4 if the radio range test passes. |
