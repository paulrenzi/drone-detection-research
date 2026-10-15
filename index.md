---
title: Overview
layout: home
nav_order: 1
---

<div class="hero" markdown="1">
<span class="hero-tag">RESEARCH NOTEBOOK · REVIEWED 2026-10-15</span>

# Low-cost acoustic drone detection

Can a mesh of cheap microphones detect and locate drones well enough to plot them on a shared map, for a fraction of what military counter-UAS sensors cost today?
</div>

<div class="stats">
  <div class="stat"><p class="stat-num">8</p><p class="stat-label">sensor models rated 3 or higher</p></div>
  <div class="stat"><p class="stat-num">$60</p><p class="stat-label">low end of a purpose-built node</p></div>
  <div class="stat"><p class="stat-num">14k</p><p class="stat-label">nodes in Sky Fortress (upper est.)</p></div>
  <div class="stat"><p class="stat-num">M1</p><p class="stat-label">recommended core</p></div>
</div>

<p class="kicker">01 · The idea</p>

## Listen, classify, report, fuse.

1. Cheap sensor nodes listen for drone sound signatures (engines, propellers).
2. Each node classifies what it hears **on the device** and estimates a **bearing** (direction) to it.
3. Nodes send small detection reports — never raw audio — over a mesh or cellular link.
4. A central service fuses bearings from several nodes into a **position and track**, and publishes it on a map and to military systems (TAK / Cursor-on-Target, SAPIENT).

Software is the comparatively easy part. The hard parts are **range** (how far a node can hear), **direction accuracy**, **false alarms**, and **keeping thousands of nodes alive outdoors** for months.

{: .important }
> The proven model is a dense, fixed network of cheap ground sensors. Ukraine's Sky Fortress runs on ~10,000–14,000 of them at about $400–1,000 each. The most credible way to beat that cost is a **purpose-built mic-array node at roughly $60–120**, mounted high (masts, rooftops, telecom towers), that reports bearings instead of raw detections. The only airborne option still on the list is lighter-than-air: a tethered aerostat.

<p class="kicker">02 · The landscape</p>

## What's out there, what works, what failed.

Counter-drone sensing has split into a few camps. Each one is good at something, and each has a blind spot.

**What works.** Ukraine settled the main question: cheap acoustic networks work in war. Sky Fortress runs about 14,000 phone-and-microphone sensors on poles at $400–1,000 each, roughly $5M for the whole network, and tracks Shaheds and cruise missiles with them. Zvook puts microcomputers on radio towers and is trialling a vehicle version with NATO. At the top end, Squarehead's Discovair and Microflown's AVISA show what premium acoustic arrays can do without line of sight: a few hundred metres against small drones. Soldiers already buy cheap radio detectors in numbers; BlueBird's Chuyka costs about $750–850 and picks up analog FPV video at up to 4 km. Anduril's WISP cameras and Lattice software sit at the expensive end and are becoming the US Army's backbone.

**What falls short, and why.** The blind spots are exactly where drones are moving.

- **Radio detectors** hear radio, not drones. Fibre-optic FPVs and pre-programmed drones are invisible to them, and they rarely give a position to put on a map.
- **Radar** is accurate, but it transmits all the time, so it can be found and targeted. It also needs line of sight and costs $40k–160k a unit.
- **Cameras**, even WISP, can't see a low drone behind trees, buildings or a ridge.
- **Premium acoustic arrays** work, but they are single expensive sensors sold through prime contractors. Even they top out at a few hundred metres, so better hardware alone doesn't buy more range.
- **Sky Fortress** is built for national coverage of loud engine drones over cellular networks, not for portable kits that units can carry against FPVs.

**What the front tells us.** The evidence makes a strong case that the gap is real, and that it is where units are dying ([full review]({{ site.baseurl }}{% link research/problem-check.md %})):

- **Drones cause about 80% of casualties**, by analysts' estimates ([NPR, Oct 2026](https://www.tpr.org/news/2026-10-05/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)).
- **Troops survive mainly by not moving:** underground, under nets, hiding when they hear a drone, taking hours to cover a kilometre and going months without rotation (same source). That is coping, not protection.
- **The fastest-growing threat beats the detectors units carry.** Fibre-optic FPVs send no radio, so radio detectors miss them ([Kyiv Independent](https://kyivindependent.com/as-russias-fiber-optic-drones-flood-the-battlefield-ukraine-is-racing-to-catch-up/)); they are 30–50% or more of FPVs in some sectors.
- **The expensive answer isn't there.** We found no reporting of Anduril's WISP at Ukraine's front ([its published use](https://dronexl.co/2026/08/06/anduril-wisp-washington-national-guard-drones-birds/) is US domestic security), and cameras can't see through tree lines anyway.
- **Ukrainian builders are moving the same way.** Zvook announced an acoustic FPV sensor for front-line positions in January 2026 ([Militarnyi](https://militarnyi.com/en/news/ukraine-develops-acoustic-detector-for-fpv-drones/)): validation of the approach, and a competitor.

What is not yet shown is that **earlier warning changes what troops do**. No source measures it. That is the next thing to check, and it costs nothing: ask front-line users (T18).

**What failed outright.** Microphones on flying drones don't work: the listener's own rotors sit centimetres from the mic, and published measurements put the target 10–30 times quieter than the drone's own noise. Perching drones (land, stop the motors, listen) fix that, but landing reliably and keeping them powered is still research. Fibre-optic acoustic sensing turns a cable into a long line of microphones, but buried fibre hears airborne sound poorly and has only detected vehicles close to the cable. All three rated below 3 and are no longer on this site.

## The routes still open.

The gap nobody fills cheaply is **passive detection of drones that don't transmit and can't be seen, at a price every unit can carry.** Four practical routes lead there:

1. **Purpose-built mic-array nodes at $60–120, mounted high** ([M1]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) on [M4]({{ site.baseurl }}{% link models/m04-elevated-nodes.md %}) placements). Many cheap nodes rather than one better sensor, each reporting a bearing rather than a bare alarm. This is the core.
2. **Phones as a fast start** ([M2]({{ site.baseurl }}{% link models/m02-phone-network.md %})). Proven at scale by Sky Fortress. Trade unit quality for speed when coverage is needed this month.
3. **Portable unit kits, and a [drone-laid tripwire]({{ site.baseurl }}{% link models/tripwire.md %}).** 8–12 nodes around a ~500 m perimeter for about $1,500–2,500, placed by hand or dropped by drone ([M7]({{ site.baseurl }}{% link models/m07-drone-deployed-nodes.md %})), with vehicle-mounted nodes ([M9]({{ site.baseurl }}{% link models/m09-mobile-nodes.md %})) for units on the move. This is the form factor Sky Fortress wasn't built for. Dropping cheap listeners 2–4 km forward turns ~10 seconds of warning into a minute or more.
4. **Be the sensor, not the platform** ([M10]({{ site.baseurl }}{% link models/m10-hybrid-cueing.md %})). Feed tracks into Lattice, TAK and SAPIENT, and use acoustic bearings to point cameras and RF sensors at drones they would otherwise miss.

The lasting advantage isn't the hardware, which anyone can copy. It's **training data** (real combat recordings and local false-alarm sounds) and integrations that are already in the field. Details and sources are in [Existing systems]({{ site.baseurl }}{% link research/existing-systems.md %}) and the [competitor analysis]({{ site.baseurl }}{% link research/competitors.md %}).

<p class="kicker">03 · The constraint</p>

## Passive by design.

Many of the counter-drone SBIR topics we are targeting ask for **passive** detection, and for a hard reason: a radar transmits all the time, and an adversary can locate that transmission and send a drone or munition down it. A microphone transmits nothing while it listens.

So every model on this site has to work without an active emitter:

- **Listening is silent.** Nodes detect, classify and take a bearing on the device and emit nothing while they do it.
- **Reports are short and rare.** A node sends a few-byte detection report only when it hears something, at low power, never a continuous signal. Where that is still too much, a node can be wired, use fibre, or store reports and burst them later.
- **No radar in our kit.** We add no emitter of our own. If a site already runs a radar, its track can be fused in, but nothing we field depends on it.
- **Other sensors must be passive too.** Passive RF (receive only) and cameras (visible or thermal) qualify; anything that illuminates the target does not.

<p class="kicker">04 · Feasibility matrix</p>

## Eight ways to build the network.

Each model gets two scores. **Feasible** runs from 1 (not feasible now) to 5 (proven, build today). **Payoff** runs from 1 to 5 for how much it would matter to units in the field, against small drones including fibre-optic FPVs, if it works. Models rated below 3 (perch-and-listen drones, flying microphone swarms, and fibre-optic distributed acoustic sensing) have been dropped. See [how ratings work](#how-ratings-work).

| # | Model | Feasible | Payoff | Unit cost | Status |
|---|---|:-:|:-:|---|---|
| UC | [Drone-laid tripwire (use case: M3 nodes laid by M7)]({{ site.baseurl }}{% link models/tripwire.md %}) | <span class="score score-mid">3</span> | <span class="score score-hi">5</span> | ~$1.5–2.5k kit | Highest payoff; one radio test away |
| M1 | [Fixed ground mic-array mesh]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) | <span class="score score-hi">4</span> | <span class="score score-hi">4</span> | $60–120 | Recommended core |
| M2 | [Phone-based sensor network]({{ site.baseurl }}{% link models/m02-phone-network.md %}) | <span class="score score-hi">5</span> | <span class="score score-mid">3</span> | $100–500 | Proven at scale (Ukraine) |
| M3 | [Single-mic nodes + time-difference]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}) | <span class="score score-mid">3</span> | <span class="score score-mid">3</span> | $30–50 | Cheapest, harder to make work |
| M4 | [Elevated fixed nodes (towers, masts)]({{ site.baseurl }}{% link models/m04-elevated-nodes.md %}) | <span class="score score-hi">4</span> | <span class="score score-hi">4</span> | $80–300 + mount | Recommended placement for M1 |
| M5 | [Tethered aerostats / balloons]({{ site.baseurl }}{% link models/m05-aerostats.md %}) | <span class="score score-mid">3</span> | <span class="score score-lo">2</span> | $5k–50k+ | Niche, gap-filler |
| M7 | [Drone-deployed ground nodes]({{ site.baseurl }}{% link models/m07-drone-deployed-nodes.md %}) | <span class="score score-mid">3</span> | <span class="score score-hi">4</span> | node + delivery | Deployment method for M1 |
| M9 | [Vehicle / soldier-mounted mobile nodes]({{ site.baseurl }}{% link models/m09-mobile-nodes.md %}) | <span class="score score-mid">3</span> | <span class="score score-mid">3</span> | $150–1,000 | Being trialled (Zvook) |
| M10 | [Hybrid: acoustic + passive RF + camera cueing]({{ site.baseurl }}{% link models/m10-hybrid-cueing.md %}) | <span class="score score-hi">4</span> | <span class="score score-hi">4</span> | $100–2,000 / site | Phase 2 add-on |
{: .matrix }

Each model's page says what it works best against. Reference point: commercial acoustic arrays such as Squarehead **Discovair G2** (Norway) detect small drones at "several hundred metres" and are sold inside full counter-UAS systems at far higher prices. See [Existing systems]({{ site.baseurl }}{% link research/existing-systems.md %}).

<p class="kicker">05 · Positioning</p>

## The layer the others miss.

For protecting bases and units in the field: *the acoustic layer that hears the drones radio detectors and cameras miss, at the price of a radio detector.*

Being passive sets us apart from radar, not from everyone: cameras such as Anduril's WISP are passive too. What sets us apart is **hearing what they can't see**: a small drone flying low behind trees, buildings or a ridge, including fibre-optic FPVs that give off no radio signal for a detector to catch. Sky Fortress hears drones too, but it is a fixed national network tuned for larger, louder targets, not a kit a unit can carry.

Be honest about range. Against small quadcopters even premium arrays reach only a few hundred metres, so this is an **early-warning perimeter that cues cameras and other sensors**, giving seconds to tens of seconds of warning. It is not wide-area coverage.

The first integration target is **Anduril Lattice**, which the US Army has picked as its counter-drone backbone. A cheap passive sensor that feeds Lattice makes the expensive systems better instead of competing with them. See [Lattice integration]({{ site.baseurl }}{% link research/integration.md %}#anduril-lattice).

[Read the competitor analysis →]({{ site.baseurl }}{% link research/competitors.md %}){: .btn .btn-primary }

<p class="kicker">06 · Ratings</p>

## How ratings work
{: #how-ratings-work }

**Feasibility** is scored 1–5 on four axes, and the feasibility score is a judgement, not an average:

| Axis | Question |
|---|---|
| **Technical readiness** | Can it be built with parts and methods that exist today? |
| **Cost per km²** | What does it cost to cover an area, not just per unit? |
| **Persistence** | Can it run unattended for weeks or months? |
| **Deployability** | Can non-specialists put it out and keep it running at scale? |

**Payoff** is scored separately, 1–5: how much the model would matter for protecting units in the field against small drones, including fibre-optic FPVs, if it works. A model can be easy and unimportant (phones in a rear area) or hard and decisive (the drone-laid tripwire). Read the two together.

The single most important number is **cost per square kilometre covered = node cost × node density**. Node density is driven by detection range, which differs hugely by target. See [Range and cost-per-km² model]({{ site.baseurl }}{% link research/range-and-cost.md %}).

<p class="kicker">07 · Contributing</p>

## How to add to this

- **New research note:** add a Markdown file to `research/` with `parent: Research Notes` in the front matter.
- **New model:** copy `models/_template.md`, number it `mNN-short-name.md`, and add a row to the matrix above. It must work without an active emitter, it is only listed if its feasibility rates 3 or higher, and it needs both a feasibility and a payoff score.
- **Changed a rating?** Say why in the model page's *Rating history* and in the [Changelog]({{ site.baseurl }}{% link changelog.md %}).
- Mark anything not yet confirmed with an `{: .warning }` callout.
