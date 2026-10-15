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

**In one line:** don't try to make a microphone hear farther; drop cheap ones 2–4 km forward. A unit then gets about a minute of warning instead of about ten seconds, including against fibre-optic FPVs that emit no radio.

<div class="stats">
  <div class="stat"><p class="stat-num">~1 min</p><p class="stat-label">warning from a line 2 km out, against ~10 s from a ring near the unit (est.)</p></div>
  <div class="stat"><p class="stat-num">$17–50</p><p class="stat-label">per throwaway listener (est.)</p></div>
  <div class="stat"><p class="stat-num">24</p><p class="stat-label">listeners for two lines across a 3 km front</p></div>
  <div class="stat"><p class="stat-num">T9</p><p class="stat-label">the deciding test: can a line report back from under trees?</p></div>
</div>

## The idea in four steps

1. **Lay a line.** A small drone with no pilot drops 3–4 throwaway listeners per flight across the enemy's approach, 2–4 km out. Two lines, a few hundred metres apart.
2. **Listen quietly.** Each listener sleeps until it hears something drone-like, and transmits nothing while it waits.
3. **Report back.** A few-byte alert hops listener to listener to a raised receiver at the unit.
4. **Warn.** Warning time is distance ÷ drone speed, so a line 2 km out gives about 50–65 seconds against an FPV. A ring of microphones 300 m out gives 8–10 (both estimates).

## Where it stands

- **Rated 3 out of 5.** Every part exists, but nobody has shown that a forward line can get its alerts home.
- **The deciding test is radio under trees (T9).** Published measurements say open ground probably works. Under trees, where troops and attacking drones actually go, it is unproven. [Evidence and test plan]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back).
- **Next steps cost little.** The first five tests each cost under $500; see [Parts and first build](#components-and-mvp).

## Front-line problems, in plain terms

From [what the front actually looks like]({{ site.baseurl }}{% link research/field-conditions.md %}). Each fix adds no cost, and each also gathers information the unit can use. These are proposals, not tested yet.

| Problem | What it means day to day | Our fix | What the line learns |
|---|---|---|---|
| **GPS is jammed** | The drone may not put listeners where planned | Short flights from a spot the crew can see; accept drops 20–50 m off. Listeners carry no GPS, which saves money. Troops walking in can also place them by hand | Where GPS fails along the unit's routes |
| **Friendly drones everywhere** | A line that alarms on every drone gets switched off | Alarm only for drones heading **in**, outside the unit's own flight times | Enemy drone habits: when, where and how fast |
| **Tree lines** | Lines follow the tree belts, where radio range is short | Space listeners closer, paid for by dropping GPS | When leaf fall changes radio range |
| **Cold** | Batteries die sooner in winter | Listeners report battery and temperature; re-lay a line when it runs low | Real winter battery life |

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="how-it-works" markdown="block">
<summary><span class="layer-title">How it works</span><span class="layer-sub">Warning time, why lines beat coverage, the listeners, the drone, getting alerts home</span></summary>

### Warning time comes from distance

A microphone hears a small FPV at roughly **100–300 m** ([working estimate]({{ site.baseurl }}{% link research/range-and-cost.md %})). Better hardware barely moves that, so move the listeners forward instead.

| Where the listeners sit | Warning against an FPV at 30–40 m/s |
|---|---|
| Ring placed by hand, ~300 m out | ~8–10 seconds |
| Line laid by drone, 2 km out | ~50–65 seconds |
| Line laid by drone, 4 km out | ~1.5–2 minutes |

{: .warning }
> FPV speeds and detection ranges are planning estimates, not field measurements. The ratio is what matters: ten times the distance is roughly ten times the warning.

Ten seconds is enough to flinch. A minute is enough to take cover, cue a camera and launch an interceptor.

### Lines, not coverage

Covering a whole area against small drones would take thousands of nodes ([the density problem]({{ site.baseurl }}{% link research/range-and-cost.md %}#worked-examples)). Attacking drones mostly come from one side, so a tripwire only covers the approaches.

- **One line**, 2–4 km out, says *something crossed here, at this time*.
- **A second line** a few hundred metres behind adds **direction and speed**, and filters false alarms: a real drone trips both lines in order.
- A listener only has to hear the drone, not locate it, so listeners sit about one detection range apart: every 200–300 m against FPVs, or closer under trees. A 3 km front takes about 12 per line.
- Pinpointing the drone is left to the dense ring near the unit ([M1]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) on [M4]({{ site.baseurl }}{% link models/m04-elevated-nodes.md %}) placements).

### Throwaway listeners

Single-microphone nodes ([M3]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}) class) built to be dropped, not placed:

- A **dart body** that sticks upright in soil, with a **spring mast** that lifts the microphone 0.5–1 m. A microphone lying in grass hears much worse.
- **Wake on sound:** the processor and radio wake only when something drone-like is heard. Target: **weeks on a small battery**.
- **No recovery.** Lost or dead listeners are replaced by the next flight, like ammunition.

Open-source starting points exist: [Batear]({{ site.baseurl }}{% link research/open-source-builds.md %}#batear) (MIT licence) already runs a single-mic detector with encrypted LoRa alerts on an ESP32-S3, and [VolAnti]({{ site.baseurl }}{% link research/open-source-builds.md %}#volanti) has published a 104 m range test.

### The delivery drone

- **Flies itself.** A pre-planned mission on open-source autopilot software (ArduPilot), with a drop at each point and every radio link off, so nothing broadcasts while the line is laid. Six flights lay two lines across a 3 km front.
- **Reusable**, but cheap enough to lose. At the end of its life it can be left on high ground as a relay.
- Airframes, software and GPS jamming: [Delivery drone]({{ site.baseurl }}{% link research/delivery-drone.md %}).

### Getting alerts home

A listener sends a few bytes only when it hears something: time, its ID, what it heard, how sure it is, a short description of the sound and its battery level. Alerts hop down the line to a raised receiver at the unit, on a mast or [aerostat]({{ site.baseurl }}{% link models/m05-aerostats.md %}), which feeds the shared map, TAK and [Lattice]({{ site.baseurl }}{% link research/integration.md %}#anduril-lattice).

As more units lay lines that report to the same map, they add up to a wider network that nobody had to plan or fund centrally.

</details>

<details class="layer" id="solving-the-field-limits-at-no-extra-cost" markdown="block">
<summary><span class="layer-title">Front-line problems: the full fixes</span><span class="layer-sub">GPS jamming, friendly drones, tree lines and cold, solved at no extra cost while gathering information</span></summary>

{: .warning }
> A design proposal, not a tested system. The tests that would check it are at the end of this section.

### The fixes

| Problem | Fix | What the line learns | Extra cost |
|---|---|---|---|
| **GPS is jammed** ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)) | No GPS on the listener. Its position is the planned drop point, corrected by where the drone's flight log says it released. Its clock is set when it is loaded and kept in step with neighbours whenever they relay. Its own GPS would be jammed in the same places as the drone's anyway. The drone flies short legs from a point the crew can confirm by eye; drops 20–50 m off still make a line (T14). Troops walking in at night can also place listeners by hand (an inference) | ArduPilot's flight log records GPS fix quality on every flight, so each sortie maps where GPS failed or jumped along the unit's routes | **Saves $8–15 per listener** |
| **Friendly drones** ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#what-infantry-use-to-hear-drones-today)) | A drone heading in trips the outer line first; one heading out trips the inner line first. The unit enters its own flight times on the receiving tablet. An inbound drone outside those times is an alarm; everything else is logged quietly | Each alert carries a few bytes describing the sound (main tone, loudness, duration). Alerts during friendly flights label themselves, so the line builds training examples for the next batch's classifier | None: a few more bytes per alert |
| **Tree lines** ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#where-infantry-actually-sit-tree-lines)) | Lay lines across the tree belts and the gaps between them, spaced closer under canopy. The money that bought 12 listeners with GPS buys about 15–17 without | Every received packet comes with its signal strength. Logged per link, it shows when leaf fall or growth changes range and which links are about to fail | None |
| **Cold** ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#seasons)) | No pricier cold-rated cells up front. Listeners add battery voltage and chip temperature to packets they already send, plus a rare stand-alone check-in | Measured winter battery life, which no source we found has published, and a forecast of when each line needs re-laying | None on boards that already read their battery, such as the Heltec V3 (Meshtastic reports its level); two resistors, a few cents, on a custom board. The ESP32-S3 has a [built-in temperature sensor](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/temp_sensor.html), which reads close to air temperature only while the listener sleeps |

### What the unit gets

Over weeks, a line becomes a record of drone traffic on the unit's approach:

- **Enemy drone habits:** time of day, which tree lines and gaps they use, and speed from the time between the two lines. That says when to stay under cover and where to point a camera or interceptor. On the shared map, many units' lines show the pattern across a sector.
- **Friendly traffic:** a count of the unit's own flights, useful for checking against neighbouring units' drones.
- **A jamming map**, updated every sortie.
- **A radio and season map**, showing where lines need closer spacing and when.
- **Winter battery data**, measured where it matters.
- **Lost listeners as a signal (an inference):** one that goes quiet while its battery was healthy was probably destroyed or found. Where and when that happens is itself a sign of activity.

### Rules that keep it cheap and quiet

- **No new transmissions to gather data.** Summaries ride on alerts and relays already being sent. A stand-alone check-in goes out at most once or twice a day, and the unit can switch it off. Keep the extra summary to roughly 10–15 bytes (an estimate), since every byte adds air time.
- **No audio leaves a listener.** LoRa is far too slow. Training recordings come from the [weekend test kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector) and test ranges.
- **Classifier updates ship in the next batch of listeners**, not over the air.
- **The record lives at the unit's receiver and on the shared map**, not in the listeners.

### What has to be proven

- **Clocks without GPS.** Telling direction from which line trips first needs neighbouring clocks to agree within about 1–2 seconds for weeks. A drone at 30–40 m/s crosses lines a few hundred metres apart roughly 5–15 seconds apart, and ordinary microcontroller clocks drift a few seconds a day (both estimates). Neighbour syncing has to keep up (T15).
- **Direction alone doesn't sort friend from foe.** Friendly drones fly home inbound, and enemy scouts leave outbound. Until T15 shows whether sound can tell them apart, the unit's flight times do most of the work.
- **Positions from the drop plan** are only as good as the drone's navigation (T14).
- **Battery life in cold**, with the extra bytes counted (T12).

</details>

<details class="layer" id="components-and-mvp" markdown="block">
<summary><span class="layer-title">Parts and first build</span><span class="layer-sub">What goes in one listener, five cheap build steps, and photos of the starter parts</span></summary>

### What goes in one listener

| Part | Example | Est. cost | Why it's there |
|---|---|---|---|
| Microcontroller | ESP32-S3 | $4–10 | Runs the drone / no-drone classifier on the device, so only a few bytes are sent |
| Microphone | INMP441 or ICS-43434 (I²S digital MEMS) | $1–3 | One mic is enough: a line listener only has to hear, not take a bearing |
| LoRa radio | SX1262, 915 MHz in the US | $6–25 | Sends alerts and relays neighbours' alerts toward the unit |
| GPS | none | $0 (was $8–15) | Dropped: it would be jammed where it matters most ([why](#solving-the-field-limits-at-no-extra-cost)) |
| Battery | small LiPo cell | ~$3–8 (estimate) | Weeks, not days, only if the listener sleeps until it hears something |
| Body, spring mast, battery housing | 3D-printed | $1–2 in filament | Sticks upright and holds the mic 0.5–1 m up |
| Windscreen | fur or foam cover | ~$1–3 (estimate) | Wind is the biggest range-killer in [VolAnti's tests]({{ site.baseurl }}{% link research/open-source-builds.md %}#volanti) |
| **Total** | | **~$17–50** | Against a **$30–60 target** (~$25–65 with GPS) |

{: .warning }
> Part prices come from [Hardware]({{ site.baseurl }}{% link research/hardware.md %}); the battery and windscreen figures are estimates. All are hobby-grade, small-volume prices. A board that already combines the ESP32-S3 and LoRa radio, such as the Heltec WiFi LoRa 32 V3, costs about $25–30 and is the easiest way to build the first ones. A full kit of 24 listeners and one delivery drone is estimated at **$1,500–2,500**.

### Five build steps

Each step answers one question before money goes into the next. They match the [tests](#open-questions).

| Step | What you build | What it proves | Rough cost |
|---|---|---|---|
| **1. Weekend test kit** | 2 Heltec V3 boards running [Batear]({{ site.baseurl }}{% link research/open-source-builds.md %}#batear), 3 INMP441 mics, windscreens, phones as recorders | A cheap mic hears a drone at known distances; first labelled training audio; a first radio range figure | **~$80–90** with a borrowed drone, tripods and power banks; ~$360–480 buying everything |
| **2. Radio range test (T9)** | The same two boards, one carried away from a raised receiver | Whether a line 2–4 km out can report back at all. **The deciding question** | < $300 |
| **3. Listener on a mast (T10, T11)** | One listener on a 0.5–1 m spring mast, plus a drop-tested printed dart body | Detection range at listener height (sets spacing), and whether listeners land upright | < $500 |
| **4. Battery test (T12)** | One listener with wake-on-sound and a small classifier | Whether "weeks on a small battery" is real | < $200 |
| **5. Drop flight (T13)** | A printed quad that lays 4 listeners on planned points | Placement accuracy and payload | < $500 |

### Parts for step 1

{: .warning }
> Prices are rough US figures checked in October 2026 and change often. Parts marked "ships from China" won't arrive in days. The "step 2" recorder board below is the kit's own later upgrade, not build step 2.

{% include kit-parts.html %}

Buying advice and a full weekend plan: [weekend test kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector).

</details>

<details class="layer" id="compared-with-the-alternatives" markdown="block">
<summary><span class="layer-title">Compared with the alternatives</span><span class="layer-sub">Radio detectors, cameras, radar, phone networks, and why not just drop phones</span></summary>

The claim is narrow: **for early warning of low drones approaching a unit, including drones that emit no radio.** It works best alongside the others: a radio detector still catches radio-controlled FPVs at long range, and the tripwire tells a camera where to look.

| | Fibre-optic FPV | Behind trees or a ridge | Warning time vs FPV | Emits while watching | Rough cost | A unit can carry it |
|---|:-:|:-:|---|:-:|---|:-:|
| **Drone-laid tripwire** | ✅ | ✅ | **~1–2 min** | ❌ | **~$1.5–2.5k kit** | ✅ |
| Hand-placed acoustic ring | ✅ | ✅ | ~10 s | ❌ | similar | ✅ |
| Radio detector (e.g. Chuyka) | ❌ | partly | long, if it emits | ❌ | ~$750–850 | ✅ |
| Camera (e.g. WISP) | ✅ if in sight | ❌ | depends on sight lines | ❌ | far higher | ❌ |
| Radar | ✅ if in sight | ❌ | long, if in sight | **✅** | $40k–160k | ❌ |
| Phone network (Sky Fortress) | ✅ | ✅ | ~10 s for FPVs near the unit | **✅** (cellular) | $400–1,000 per sensor | ❌ |

### Why not just drop phones?

Phones are the [best-proven acoustic sensor there is]({{ site.baseurl }}{% link models/m02-phone-network.md %}) and still win for fixed networks with power and cell coverage, and as the display at the unit. For a line dropped 2–4 km forward, purpose-built listeners win:

| | Purpose-built listener | Phone |
|---|---|---|
| **Emissions** | Silent until it hears something, then one short burst | Keeps checking in with the cell network, so it can be located; with radios off it can't report |
| **Network** | Its own mesh; no cell towers | Needs cell coverage, which near the front is jammed, destroyed or watched |
| **Battery** | Wake-on-sound: weeks (target) | Running a mic and classifier non-stop: about a day (estimate) |
| **Weight** | Target well under 100 g, so a small drone carries 3–4 | ~150–200 g plus a mast |
| **Cost** | $17–50 (estimate) | ~$50–100 for the cheapest phone, plus mount and protection |
| **Survives a drop** | Designed for it | Isn't |
| **Brains** | Only needs "drone-like sound: yes or no" | Can run much bigger classifiers |

The phone's one real advantage is computing power. A listener only has to answer *was that a drone?*, a small-classifier job of the kind that already runs on microcontrollers. That still has to be proven on real recordings.

</details>

<details class="layer" id="limits-and-risks" markdown="block">
<summary><span class="layer-title">Other risks</span><span class="layer-sub">Radio range, tracing, noisy laying, gaps, false alarms, litter, export rules</span></summary>

- **Getting alerts home is the hardest part.** Published measurements with antennas near the ground show over 4 km in open country, but only 50–250 m in most forest tests and about 1 km at best. In woods a line would relay hop by hop at perhaps 100–200 m. Nobody has measured a 0.5–1 m listener reaching a raised receiver 2–4 km away. [Evidence and test plan]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back).
- **The relay chain can point home.** A chain of bursts leading back to the unit could be traced. Keep bursts short and rare, bend the chain instead of running it straight, and treat listeners as disposable.
- **Laying the line is noisy.** The drone can be heard and seen, so the enemy may learn roughly where the line is. Lay lines at night or under other noise, and expect losses.
- **Only drones that cross the line are caught.** A drone launched from inside the line, or routed around its ends, is missed. The inner ring is still needed.
- **False alarms with nobody to check.** Wind, vehicles and birds can trip a single listener. Requiring both lines, or two neighbours, to agree is the main filter.
- **Litter.** Throwaway listeners are electronic waste. Consider biodegradable printed bodies and batteries that can't leak.
- **Export controls.** A counter-drone sensor kit may fall under ITAR/EAR once built for military use.

GPS jamming, friendly drones, tree lines and cold are covered [above](#solving-the-field-limits-at-no-extra-cost).

</details>

<details class="layer" id="why-3d-print-the-drones-and-the-nodes" markdown="block">
<summary><span class="layer-title">Why 3D-print the drone and listeners</span><span class="layer-sub">It barely cheapens the drone, but it makes the system easier to field</span></summary>

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
> Rough estimates for hobby-grade parts at small volume. Parts for military use may face supply-chain and country-of-origin rules.

Electronics are about 85–90% of the drone's cost, so a printed frame saves only about $15–35 per drone. Printing pays off elsewhere:

- **The listeners.** Each needs a dart body, mast mount and battery housing: a dollar or two printed, no tooling, and they are used by the hundred.
- **The drop mechanism.** Release clips and cargo racks are small custom parts, exactly what printers are good at.
- **Making and fixing kits near the front** from a file, without waiting on a supply chain. Ukraine already prints drone parts at scale.
- **Fast design changes.** When a dart breaks in drop tests, the fix ships as a new file that day.

A **printed fixed-wing** carrier is worth testing too: it flies much farther on the same battery and doesn't need to hover.

</details>

<details class="layer" id="open-questions" markdown="block">
<summary><span class="layer-title">Tests</span><span class="layer-sub">Seven cheap tests, from radio range to friendly drones</span></summary>

| Test | What it answers | Rough cost |
|---|---|---|
| **T9** Radio range at 2–3 km, open ground and trees, raised receiver at the unit ([test plan]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back)) | Can a forward line report back at all? Probably yes in the open; trees unproven | < $300 |
| **T10** Drop-test printed dart bodies onto soil, sand, mud and grass | Do listeners land upright with the mic clear? | < $200 |
| **T11** FPV detection range for one mic on a 0.5–1 m spring mast | How far apart listeners can be | < $300 |
| **T12** Wake-on-sound battery life with a small classifier, including in cold | Is "weeks" real, and how much shorter in winter? | < $200 |
| **T13** Drop flight: 4 listeners on planned points from a printed quad | Placement accuracy and payload | < $500 |
| **T14** The same flight with GPS unavailable | Can a line be laid under jamming? | < $300 |
| **T15** Record friendly drones; test whether sound, which line trips first and flight times can sort friend from foe, with clocks kept in step without GPS | Will the line cry wolf? | < $200 |

All are tracked in [Open questions]({{ site.baseurl }}{% link research/open-questions.md %}).

</details>

<details class="layer" id="rating-history" markdown="block">
<summary><span class="layer-title">Background and rating history</span><span class="layer-sub">The Vietnam-era precedent, and why the rating is where it is</span></summary>

### Precedent

In the Vietnam War, **Operation Igloo White** air-dropped acoustic and seismic sensors (including the ACOUBUOY and SPIKEBUOY) along the Ho Chi Minh Trail and relayed their detections back by aircraft. What's new is that the sensor, the delivery drone and the classifier are now cheap enough to throw away.

### Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | Each part exists (cheap nodes, autonomous drop drones, LoRa mesh), but nobody has proven forward lines can report back over 2–4 km. Rises to 4 if the radio range test passes. |
| 2026-10-15 | 3 (unchanged) | Reviewed published LoRa range measurements: over 4 km in the open with antennas at 1.5 m, but 1 km or less in forest. The open-ground case looks likely; the forest case needs the [T9 field test]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back), which now has pass/fail criteria. |
| 2026-10-15 | 3 (unchanged) | Reviewed front-line conditions. Fibre-optic FPVs, which radio detectors can't see, and predictable approach routes along tree lines support the payoff. GPS jamming, friendly drones and the forest radio case add work; they are now tests T14, T15 and T9. |
| 2026-10-15 | 3 (unchanged) | Proposed [no-extra-cost fixes](#solving-the-field-limits-at-no-extra-cost) for those limits: drop the node's GPS, sort friend from foe by line order and flight windows, and report battery and temperature. The fixes also turn the line into a record of drone traffic. All untested; rating moves only on test results. |
| 2026-10-15 | 3 (unchanged) | Page reorganised into layers: summary, front-line problems in plain terms, then fold-out detail. No change to the evidence. |
</details>
