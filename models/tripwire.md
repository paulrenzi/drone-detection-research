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

## Why it matters

- **Drones cause about 80% of casualties** at the front, by analysts' estimates ([NPR, Oct 2026](https://www.tpr.org/news/2026-10-05/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)).
- **Units cope by not moving:** underground, under nets, taking hours to cover a kilometre. Every trip out is exposure (same source).
- **Fibre-optic FPVs, the fastest-growing threat, emit no radio**, so the detectors units carry miss them. A microphone hears them.
- **Nothing cheap fills the gap yet.** Camera systems like WISP aren't at the front and can't see through tree lines; Zvook's acoustic FPV sensor, the NW0, sits at the unit, not forward: it needs 15–18 W of power and a link. It's on sale at about $834–950 per sensor, but its range and fibre-optic claims are the maker's only ([details]({{ site.baseurl }}{% link research/competitors.md %}#zvook-nw0--direct-competitor-claims-only)). Denmark's Komodo already sells a sensor variant that drones can drop, built for Shaheds rather than FPV lines ([details]({{ site.baseurl }}{% link research/competitors.md %}#komodo--the-drone-dropped-sensor-already-exists)).

Full evidence: [Is the problem worth solving?]({{ site.baseurl }}{% link research/problem-check.md %})

## Where it stands

- **Rated 3 out of 5.** Every part exists, but nobody has shown that a forward line can get its alerts home.
- **The deciding test is radio under trees (T9).** Published measurements say open ground probably works. Under trees, where troops and attacking drones actually go, it is unproven. [Evidence and test plan]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back).
- **The proposed answer: hear the lines from the edge of the unit's tree line.** A listen-only receiver, placed by hand and raised at the belt edge, wired back to the dugout so the unit's position emits nothing. [Design](#getting-alerts-out-of-the-trees).
- **The one unproven link is whether warning changes what troops do.** No source measures it. Ask front-line users before building more ([T18]({{ site.baseurl }}{% link research/problem-check.md %}#the-next-step-ask-before-building-t18)).
- **Next steps cost little.** The first five tests each cost under $500; see [Parts and first build](#components-and-mvp).

## Front-line problems, in plain terms

From [what the front actually looks like]({{ site.baseurl }}{% link research/field-conditions.md %}). Each fix adds no cost, and each also gathers information the unit can use. These are proposals, not tested yet.

| Problem | What it means day to day | Our fix | What the line learns |
|---|---|---|---|
| **GPS is jammed** | The drone may not put listeners where planned | Short flights from a spot the crew can see; accept drops 20–50 m off. Listeners carry no GPS, which saves money. Troops walking in can also place them by hand | Where GPS fails along the unit's routes |
| **Friendly drones everywhere** | A line that alarms on every drone gets switched off | Alarm only for drones heading **in**, outside the unit's own flight times | Enemy drone habits: when, where and how fast |
| **Tree lines** | Lines follow the tree belts, where radio range is short | Drop listeners at belt edges, not inside. Hear them with a listen-only receiver raised at the edge of the unit's own tree line, wired back to the dugout. Space them closer, paid for by dropping GPS | When leaf fall changes radio range |
| **Cold** | Batteries die sooner in winter | Listeners report battery and temperature; re-lay a line when it runs low | Real winter battery life |

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="how-it-works" markdown="block">
<summary><span class="layer-title">How it works</span><span class="layer-sub">Warning time, why lines beat coverage, the listeners, the drone, getting alerts home</span></summary>

### Warning time comes from distance

A microphone hears a small FPV at roughly **100–300 m** ([working estimate]({{ site.baseurl }}{% link research/range-and-cost.md %})). Better hardware barely moves that, so move the listeners forward instead.

{: .warning }
> **The only measured range for cheap microphones is lower: about 50–60 m** against a consumer drone in a windy field ([what's measured]({{ site.baseurl }}{% link research/competitors.md %}#what-is-actually-measured)). FPVs are probably louder, but no study has flown one at distance. If 50–60 m holds, listeners sit about 100 m apart and a 3 km line needs about 30, not 12. T11 decides it.

| Where the listeners sit | Warning against an FPV at 30–40 m/s |
|---|---|
| Ring placed by hand, ~300 m out | ~8–10 seconds |
| Line laid by drone, 2 km out | ~50–65 seconds |
| Line laid by drone, 4 km out | ~1.5–2 minutes |

{: .warning }
> FPV speeds and detection ranges are planning estimates, not field measurements. The ratio is what matters: ten times the distance is roughly ten times the warning.

Ten seconds is enough to flinch. A minute is enough to get people under cover, hold a resupply run or evacuation, ready shooters, and cue a camera or turret. Interceptor drones are built mostly for other targets so far. [What a minute buys]({{ site.baseurl }}{% link research/problem-check.md %}#what-a-minute-buys).

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

A listener sends a few bytes only when it hears something: time, its ID, what it heard, how sure it is, a short description of the sound and its battery level. Alerts hop down the line to a raised receiver at the unit ([getting alerts out of the trees](#getting-alerts-out-of-the-trees)), on a mast or [aerostat]({{ site.baseurl }}{% link models/m05-aerostats.md %}), which feeds the shared map, TAK and [Lattice]({{ site.baseurl }}{% link research/integration.md %}#anduril-lattice).

As more units lay lines that report to the same map, they add up to a wider network that nobody had to plan or fund centrally.

</details>

<details class="layer" id="getting-alerts-out-of-the-trees" markdown="block">
<summary><span class="layer-title">Getting alerts out of the trees</span><span class="layer-sub">The radio problem as an engineering problem: a listen-only receiver at the edge of the unit's tree line, wired back</span></summary>

{: .warning }
> A design proposal, not a tested system. Loss figures are model estimates; the measurements are in [T9]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back).

Getting alerts home is the tripwire's deciding question. Rather than wait for a test to say yes or no, treat it as something to engineer.

### A windbreak belt is not a forest

Most published forest tests put both radios deep under canopy, and found hops of 50–250 m. But much of the front is open farmland cut by planted windbreaks only **3–15 m wide**, and that is where units sit ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#where-infantry-actually-sit-tree-lines)). A signal crossing a belt passes through metres of trees, not hundreds.

| Trees the signal crosses | 433 MHz | 915 MHz | 2.4 GHz |
|---|:-:|:-:|:-:|
| One 10 m windbreak belt | ~3.5 dB | ~4.4 dB | ~5.8 dB |
| 200 m of forest | ~24 dB | ~29 dB | ~38 dB |

{: .note }
> Estimates from [Weissberger's model](https://en.wikipedia.org/wiki/Weissberger%27s_model) for dense, leafy trees, not measurements. A belt crossed at an angle is deeper than its width. The low-antenna forest tests in T9 lost more than this model predicts.

On paper there is room for it. An SX1262 at full power and SF12 has roughly 159 dB to spend. A listener at 1 m reaching a receiver at 10 m, 3 km away over open ground, uses roughly 119 dB of that (free space plus the ground loss worked out in T9). That leaves about 40 dB for belts, fading and margin, so four belts at about 4–5 dB each fit (all estimates). **Deep forest does not fit** and needs the fallbacks below.

### The design: a listen-only receiver at the tree-line edge, wired home

- **Placed by hand where the unit already is.** One receiver at the edge of the unit's own tree line, facing the lines, raised 5–10 m: on a pole, or hoisted into the canopy with a throw line so the leaves hide it (heights are estimates). The unit's radio then sits out of the trees instead of under them.
- **It never transmits.** A wire carries alerts to the dugout, so nothing at the unit's position emits. Put the receiver 100–300 m along the belt from the dugout, and the listeners' bursts point at a box on a pole, not at the people.
- **A small directional antenna** (a Yagi) aimed at the lines adds gain on the receiving end only, roughly 6–9 dB (estimate), and hears less from other directions. Listeners keep their simple antennas, since nobody knows which way a dropped one faces.
- **Two or three receivers on the same wire**, spread along the belt. A listener only has to reach one of them, which gets round fading and a single blocked path.
- **The wire.** Alerts are a few bytes, so a slow serial link is plenty. RS-485 over ordinary twisted pair is rated to about **1.2 km** ([TI](https://www.ti.com/document-viewer/SN65HVD72/datasheet/typical-application-sllse118349)), and several receivers can share one pair. A second pair can carry power, so nothing at the edge needs a battery. The alternative is fibre from spent FPV spools: light, unjammable, and already lying across the battlefield in such quantity that one more run is hard to trace ([Business Insider](https://www.yahoo.com/news/articles/unjammable-drones-leaving-wires-everywhere-114504509.html)). Fibre needs optical converters at each end, which draw far more power than an RS-485 chip.
- **Listeners at belt edges, not inside them.** Drop listeners on the home-facing edge of forward belts, or in the gaps. The microphone still hears drones flying along the belt, and the radio path crosses fewer trees.
- **A lower band if needed.** 433 MHz loses about 1 dB less per belt than 915 MHz, and about 5 dB less through 200 m of forest (model estimates), at the cost of longer antennas.

### Is the hop point safe to place by hand? (inference)

Safer than anything forward of the unit. It goes where the troops already are, it emits nothing, and it can be installed at night. What can give it away is visual: a pole, a cable run, or a hoisted box seen by a drone overhead. So hoist it into the canopy rather than on a pole where possible, run the wire along the belt, and, if it is found, it points to a box, not to the dugout.

### When it isn't enough

- **Deep forest.** Hops of 50–250 m are what has been measured. Options: listeners only at forest edges and clearings, denser hops, a relay drone left on high ground, or an [aerostat]({{ site.baseurl }}{% link models/m05-aerostats.md %}) at the unit.
- **A wired forward hop (an idea, untested).** The delivery drone could unspool fibre to a forward hop point as it flies out, the way fibre-optic FPVs do.

### What it costs (estimates)

| Part | Est. cost |
|---|---|
| LoRa board, receive only (e.g. Heltec V3) | $20–30 |
| Small 915 MHz Yagi | $20–40 |
| RS-485 transceiver modules, one per end | $2–5 |
| Twisted pair or field cable, 300–1,000 m | $30–100 |
| USB-to-RS-485 adapter at the dugout, feeding the tablet | $5–15 |
| Pole, or throw line and pulley for the canopy | $20–60 |
| **One edge receiver and its wire** | **≈ $100–250** |

The wire works in every terrain case: a few metres to an edge in a windbreak, hundreds of metres in real forest, a short run to a roof or pole in ruins (inference; no source gives the distance, see [field conditions]({{ site.baseurl }}{% link research/field-conditions.md %}#where-infantry-actually-sit-tree-lines)). The open risk is the radio leg from listeners to the edge receiver, which is T9 run E.

This is test T17. It also adds a windbreak run to [T9]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back).

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
| **Tree lines** ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#where-infantry-actually-sit-tree-lines)) | Lay lines across the tree belts and the gaps between them, spaced closer under canopy. The money that bought 12 listeners with GPS buys about 15–17 without. Hear them with a listen-only receiver at the edge of the unit's own tree line ([design](#getting-alerts-out-of-the-trees)) | Every received packet comes with its signal strength. Logged per link, it shows when leaf fall or growth changes range and which links are about to fail | None |
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

### Considered: anchoring to a central node

A reader suggested one central node with a known position, and listeners that measure their distance to it, instead of GPS on every node.

- **The tripwire already works this way.** Listeners carry no GPS; the delivery drone's release point is the reference. The anchor wouldn't need GPS either, since it would be jammed at the unit too: make it a point fixed from a map or a one-off survey.
- **A central time beacon** is simpler than neighbours syncing with each other, and is now one of the options in T15. The catch is that a regular transmission marks the unit (T8), so it would have to be rare or sent from somewhere else.
- **Dead reckoning** is for things that move. A dropped listener doesn't; the drone already dead-reckons (T14).
- **Radio ranging doesn't pay here.** With listeners 100–300 m apart, 20–50 m of position error doesn't change "a drone crossed near listener 7". The current radio (SX1262) can't measure distance; the SX1280 can, but on 2.4 GHz, which reaches less far. A published outdoor test reached 1.4 km over open farmland with an average error of 46 m, worst where a forest shadowed the link ([Müller et al., 2021](https://digitalcollection.zhaw.ch/bitstream/11475/22769/3/2021_Mueller-etal_Outdoor-ranging-and-positioning-based-on-LoRa-modulation.pdf)). A listener 2–4 km out under trees would probably not reach an anchor at all, and every ranging exchange is another emission.
- **Where it could pay:** [M1]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) and [M3]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}), which locate a drone from several nodes and need positions and clocks to a few metres and milliseconds. That is [T16]({{ site.baseurl }}{% link research/open-questions.md %}#t16-positions-and-clocks-without-gps).

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

### The running cost: lines are ammunition

The kit price is only the start. Listeners aren't recovered, so every line is re-laid when its batteries run out. All figures below are estimates, built on the part prices above and the unproven "weeks" battery target (T12):

- **One re-lay** of two 12-listener lines: 24 × $17–50 ≈ **$400–1,200** in listeners, plus 6–8 drone sorties at 3–4 listeners each.
- **At four weeks per battery:** about 13 re-lays a year, so **≈ $5–16k a year** per 3 km front. That doubles at two weeks.
- **Plus** listeners lost to shelling, and the occasional delivery drone.

So the tripwire is a consumable, not a one-off purchase. It costs less than a radar but more than a radio detector bought once. Two things shrink the bill: battery life measured in months, not weeks, and a cheaper listener. Test T12 decides which bill is real.

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
| **Drone-laid tripwire** | ✅ | ✅ | **~1–2 min** | ❌ | **~$1.5–2.5k kit, then ≈ $5–16k a year in re-lays** ([est.](#the-running-cost-lines-are-ammunition)) | ✅ |
| Hand-placed acoustic ring | ✅ | ✅ | ~10 s | ❌ | similar | ✅ |
| Radio detector (e.g. Chuyka) | ❌ | partly | long, if it emits | ❌ | ~$584–701 | ✅ |
| Camera (e.g. WISP) | ✅ if in sight | ❌ | depends on sight lines | ❌ | far higher | ❌ |
| Radar | ✅ if in sight | ❌ | long, if in sight | **✅** | $40k–160k | ❌ |
| Phone network (Sky Fortress) | ✅ | ✅ | ~10 s for FPVs near the unit | **✅** (cellular) | $400–1,000 per sensor | ❌ |

**The same assumptions on every row.** The warning times are our estimates from where each sensor sits, not measurements. Every acoustic row, ours included, assumes the sensor actually hears an FPV, which nobody has measured ([what's measured]({{ site.baseurl }}{% link research/competitors.md %}#what-is-actually-measured)). The tripwire's minute comes from distance, not from a better microphone; if T11 finds short range, it needs more listeners, not less warning.

**Trees hurt every option, in different ways.** A windbreak belt weakens a radio link by a few dB ([estimate](#getting-alerts-out-of-the-trees)), and sound gets through too, but a belt blocks a camera's or radar's view outright. A radio detector at the unit isn't stopped by trees, but can't hear fibre-optic FPVs. Phones need cell coverage. Any sensor pushed forward, of any kind, has to get its report home through the same trees: the tripwire's radio problem is shared, not unique to it.

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

<details class="layer" id="questions-weve-weighed" markdown="block">
<summary><span class="layer-title">Questions we've weighed</span><span class="layer-sub">Hands or a drone, whether it's worth it, getting listeners back, a central anchor, predicting radio range</span></summary>

### Why not have people place the listeners?

**For the first builds, they should.** Placing listeners by hand tests what decides everything (radio range, detection range and battery: T9, T11, T12) without also depending on the drop and no-GPS flights (T13, T14). People also place them better: upright, hidden, and at belt edges where the radio carries.

The drone earns its place later. A line 2–4 km out sits inside the drone kill zone, which units describe as 5–7 km deep or more ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#the-drone-kill-zone)). Every walk out risks people and takes hours, and lines need re-laying as listeners die. A drone sortie takes minutes and risks a drone. Placing by hand stays the right tool near the unit: the inner ring, the [edge receiver](#getting-alerts-out-of-the-trees), and nights when the drone can't fly.

### Is it worth it if it works exactly as specified?

For warning time, probably: about a minute instead of about ten seconds, including against fibre-optic FPVs that radio detectors miss. Even working perfectly, it has limits:

- It only catches drones that cross a line. Launches from inside it, or routes round its ends, are missed.
- It says *something crossed here*, not where it will strike.
- A minute is only worth what the unit can do with it. Against fibre-optic FPVs that is mostly avoidance (get under cover, hold movement), plus readying shooters and cueing turrets ([what a minute buys]({{ site.baseurl }}{% link research/problem-check.md %}#what-a-minute-buys)).
- The enemy adapts, by flying round the ends or hunting listeners.

Whether a minute changes outcomes is for front-line users to say, not a test bench, and nothing published answers it. So that comes first: [Is the problem worth solving?]({{ site.baseurl }}{% link research/problem-check.md %}) sets out the evidence and the questions to ask (T18).

### Should listeners be retrievable, for example by a magnet on the drone?

**Not in the field (an inference).** A listener costs $17–50. Picking one up means the drone hovering low over each listener, inside the kill zone, exposed just as it was when it dropped it. Finding a listener would also need better than the 20–50 m the drop plan gives, so it would need a homing signal: another emission. A magnetic pickup is buildable; it just doesn't pay.

**Yes on test ranges,** where boards are reused across dozens of trials. A buzzer or light that turns on when commanded, and a person walking out, is enough.

### A central anchor instead of GPS on every node?

A reader's suggestion; considered [here](#solving-the-field-limits-at-no-extra-cost). The tripwire already works that way. It matters more for M1 and M3 ([T16]({{ site.baseurl }}{% link research/open-questions.md %}#t16-positions-and-clocks-without-gps)).

### Can the radio question be answered before the field test?

Partly, by simulation calibrated to the published measurements. Nothing published settles it. [Method and nearest research]({{ site.baseurl }}{% link research/open-questions.md %}#predicting-it-before-the-field-test).

</details>

<details class="layer" id="limits-and-risks" markdown="block">
<summary><span class="layer-title">Other risks</span><span class="layer-sub">Radio range, tracing, noisy laying, gaps, false alarms, litter, export rules</span></summary>

- **Getting alerts home is the hardest part.** Published measurements with antennas near the ground show over 4 km in open country, but only 50–250 m in most forest tests and about 1 km at best. In woods a line would relay hop by hop at perhaps 100–200 m. Nobody has measured a 0.5–1 m listener reaching a raised receiver 2–4 km away. A listen-only receiver at the edge of the unit's tree line is the [proposed answer](#getting-alerts-out-of-the-trees). [Evidence and test plan]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back).
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
<summary><span class="layer-title">Tests</span><span class="layer-sub">Eight cheap tests, from radio range to friendly drones</span></summary>

| Test | What it answers | Rough cost |
|---|---|---|
| **T9** Radio range at 2–3 km, open ground and trees, raised receiver at the unit ([test plan]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back)) | Can a forward line report back at all? Probably yes in the open; trees unproven | < $300 |
| **T10** Drop-test printed dart bodies onto soil, sand, mud and grass | Do listeners land upright with the mic clear? | < $200 |
| **T11** FPV detection range for one mic on a 0.5–1 m spring mast | How far apart listeners can be | < $300 |
| **T12** Wake-on-sound battery life with a small classifier, including in cold | Is "weeks" real, and how much shorter in winter? | < $200 |
| **T13** Drop flight: 4 listeners on planned points from a printed quad | Placement accuracy and payload | < $500 |
| **T14** The same flight with GPS unavailable | Can a line be laid under jamming? | < $300 |
| **T15** Record friendly drones; test whether sound, which line trips first and flight times can sort friend from foe, with clocks kept in step without GPS | Will the line cry wolf? | < $200 |
| **T17** Build a [listen-only edge receiver](#getting-alerts-out-of-the-trees) raised at a tree-belt edge, wired 300–1,000 m to the dugout | Can a unit hear its lines from inside a tree line without transmitting from its position? | < $300 |

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
| 2026-10-15 | 3 (unchanged); payoff 5 confirmed | [Front-line evidence]({{ site.baseurl }}{% link research/problem-check.md %}) supports the payoff: drones cause about 80% of casualties, fibre-optic FPVs beat the radio detectors units carry, and no cheap system fills the gap. Feasibility is unchanged: radio out of the trees (T9, T17) and whether warning changes behaviour (T18) are still unproven. |
| 2026-10-15 | 3 (unchanged) | Proposed an engineering answer to the radio question: a listen-only receiver at the edge of the unit's tree line, wired back. Windbreak belts are 3–15 m wide, not forests, and cost a few dB each on paper. Untested (T9, T17). |
</details>
