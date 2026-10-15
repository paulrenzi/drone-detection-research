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
  <div class="stat"><p class="stat-num">11</p><p class="stat-label">sensor models rated</p></div>
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
> The proven model is a dense, fixed network of cheap ground sensors. Ukraine's Sky Fortress runs on ~10,000–14,000 of them at about $400–1,000 each. The most credible way to beat that cost is a **purpose-built mic-array node at roughly $60–120**, mounted high (masts, rooftops, telecom towers), that reports bearings instead of raw detections. Airborne listeners only make sense when they **stop flying to listen** (perch-and-listen) or are lighter-than-air.

<p class="kicker">02 · Feasibility matrix</p>

## Eleven ways to build the network.

Rated **1 (not feasible now) to 5 (proven, build today)**. See [how ratings work](#how-ratings-work).

| # | Model | Overall | Unit cost | Status |
|---|---|:-:|---|---|
| M1 | [Fixed ground mic-array mesh]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) | <span class="score score-hi">4</span> | $60–120 | Recommended core |
| M2 | [Phone-based sensor network]({{ site.baseurl }}{% link models/m02-phone-network.md %}) | <span class="score score-hi">5</span> | $100–500 | Proven at scale (Ukraine) |
| M3 | [Single-mic nodes + time-difference]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}) | <span class="score score-mid">3</span> | $30–50 | Cheapest, harder to make work |
| M4 | [Elevated fixed nodes (towers, masts)]({{ site.baseurl }}{% link models/m04-elevated-nodes.md %}) | <span class="score score-hi">4</span> | $80–300 + mount | Recommended placement for M1 |
| M5 | [Tethered aerostats / balloons]({{ site.baseurl }}{% link models/m05-aerostats.md %}) | <span class="score score-mid">3</span> | $5k–50k+ | Niche, gap-filler |
| M6 | [Perch-and-listen drones]({{ site.baseurl }}{% link models/m06-perch-and-listen.md %}) | <span class="score score-lo">2</span> | $300–1,500 | R&D differentiator |
| M7 | [Drone-deployed ground nodes]({{ site.baseurl }}{% link models/m07-drone-deployed-nodes.md %}) | <span class="score score-mid">3</span> | node + delivery | Deployment method for M1 |
| M8 | [Flying microphone drone swarm]({{ site.baseurl }}{% link models/m08-flying-swarm.md %}) | <span class="score score-lo">1</span> | $200–2,000 | Not recommended |
| M9 | [Vehicle / soldier-mounted mobile nodes]({{ site.baseurl }}{% link models/m09-mobile-nodes.md %}) | <span class="score score-mid">3</span> | $150–1,000 | Being trialled (Zvook) |
| M10 | [Hybrid: acoustic + passive RF + camera cueing]({{ site.baseurl }}{% link models/m10-hybrid-cueing.md %}) | <span class="score score-hi">4</span> | $100–2,000 / site | Phase 2 add-on |
| M11 | [Fiber-optic distributed acoustic sensing]({{ site.baseurl }}{% link models/m11-fiber-das.md %}) | <span class="score score-lo">1–2</span> | interrogator $50k+ | Exploratory |
{: .matrix }

Each model's page says what it works best against. Reference point: commercial acoustic arrays such as Squarehead **Discovair G2** (Norway) detect small drones at "several hundred metres" and are sold inside full counter-UAS systems at far higher prices. See [Existing systems]({{ site.baseurl }}{% link research/existing-systems.md %}).

<p class="kicker">03 · Positioning</p>

## The layer the others miss.

For protecting bases and units in the field: *the passive acoustic layer that catches the drones radio detectors and cameras miss, at the price of a radio detector.*

[Read the competitor analysis →]({{ site.baseurl }}{% link research/competitors.md %}){: .btn .btn-primary }

<p class="kicker">04 · Ratings</p>

## How ratings work
{: #how-ratings-work }

Each model is scored 1–5 on four axes, and the overall score is a judgement, not an average:

| Axis | Question |
|---|---|
| **Technical readiness** | Can it be built with parts and methods that exist today? |
| **Cost per km²** | What does it cost to cover an area, not just per unit? |
| **Persistence** | Can it run unattended for weeks or months? |
| **Deployability** | Can non-specialists put it out and keep it running at scale? |

The single most important number is **cost per square kilometre covered = node cost × node density**. Node density is driven by detection range, which differs hugely by target. See [Range and cost-per-km² model]({{ site.baseurl }}{% link research/range-and-cost.md %}).

<p class="kicker">05 · Contributing</p>

## How to add to this

- **New research note:** add a Markdown file to `research/` with `parent: Research Notes` in the front matter.
- **New model:** copy `models/_template.md`, number it `mNN-short-name.md`, and add a row to the matrix above.
- **Changed a rating?** Say why in the model page's *Rating history* and in the [Changelog]({{ site.baseurl }}{% link changelog.md %}).
- Mark anything not yet confirmed with an `{: .warning }` callout.
