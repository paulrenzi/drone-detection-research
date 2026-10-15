---
title: Overview
layout: home
nav_order: 1
---

# Low-Cost Acoustic Drone Detection
{: .fs-8 }

Can a mesh of cheap microphones detect and locate drones well enough to plot them on a shared map — for a fraction of what military counter-UAS sensors cost today?
{: .fs-5 .fw-300 }

---

## The idea

1. Cheap sensor nodes listen for drone sound signatures (engines, propellers).
2. Each node classifies what it hears **on the device** and estimates a **bearing** (direction) to it.
3. Nodes send small detection reports — never raw audio — over a mesh or cellular link.
4. A central service fuses bearings from several nodes into a **position and track**, and publishes it on a map and to military systems (TAK / Cursor-on-Target, SAPIENT).

Software is the comparatively easy part. The hard parts are **range** (how far a node can hear), **direction accuracy**, **false alarms**, and **keeping thousands of nodes alive outdoors** for months.

## Bottom line so far

{: .important }
> The proven model is a dense, fixed network of cheap ground sensors. Ukraine's Sky Fortress runs on ~10,000–14,000 of them at about $400–1,000 each. The most credible way to beat that cost is a **purpose-built mic-array node at roughly $60–120**, mounted high (masts, rooftops, telecom towers), that reports bearings instead of raw detections. Airborne listeners only make sense when they **stop flying to listen** (perch-and-listen) or are lighter-than-air.

## Feasibility matrix

Ratings run **1 (not feasible now) to 5 (proven / build today)**. See [how ratings work](#how-ratings-work).

| # | Model | Overall | Unit cost (est.) | Best against | Status |
|---|---|:-:|---|---|---|
| M1 | [Fixed ground mic-array mesh]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) | **4** | $60–120 | Shahed-class, larger quads | Recommended core |
| M2 | [Phone-based sensor network]({{ site.baseurl }}{% link models/m02-phone-network.md %}) | **5** | $100–500 | Shahed-class | Proven at scale (Ukraine) |
| M3 | [Single-mic nodes + time-difference]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}) | **3** | $30–50 | Shahed-class | Cheapest, harder to make work |
| M4 | [Elevated fixed nodes (towers, masts)]({{ site.baseurl }}{% link models/m04-elevated-nodes.md %}) | **4** | $80–300 + mount | All | Recommended placement for M1 |
| M5 | [Tethered aerostats / balloons]({{ site.baseurl }}{% link models/m05-aerostats.md %}) | **3** | $5k–50k+ | Low-flying targets behind terrain | Niche, gap-filler |
| M6 | [Perch-and-listen drones]({{ site.baseurl }}{% link models/m06-perch-and-listen.md %}) | **2** | $300–1,500 | All, rapid placement | R&D differentiator |
| M7 | [Drone-deployed ground nodes]({{ site.baseurl }}{% link models/m07-drone-deployed-nodes.md %}) | **3** | node + delivery | All | Deployment method for M1 |
| M8 | [Flying microphone drone swarm]({{ site.baseurl }}{% link models/m08-flying-swarm.md %}) | **1** | $200–2,000 | — | Not recommended |
| M9 | [Vehicle / soldier-mounted mobile nodes]({{ site.baseurl }}{% link models/m09-mobile-nodes.md %}) | **3** | $150–1,000 | Convoys, forward positions | Being trialled (Zvook) |
| M10 | [Hybrid: acoustic + passive RF + camera cueing]({{ site.baseurl }}{% link models/m10-hybrid-cueing.md %}) | **4** | $100–2,000 / site | All, incl. confirmation | Phase 2 add-on |
| M11 | [Fiber-optic distributed acoustic sensing]({{ site.baseurl }}{% link models/m11-fiber-das.md %}) | **1–2** | interrogator $50k+ | Near existing fiber | Exploratory |

Reference point: commercial acoustic arrays such as Squarehead **Discovair G2** (Norway) detect small drones at "several hundred metres" and are sold inside full counter-UAS systems at far higher prices. See [Existing systems]({{ site.baseurl }}{% link research/existing-systems.md %}).

## Competitors and positioning

For protecting bases and units in the field: see [Competitor analysis and positioning]({{ site.baseurl }}{% link research/competitors.md %}). Short version: *the passive acoustic layer that catches the drones radio detectors and cameras miss, at the price of a radio detector.*

## How ratings work

Each model is scored 1–5 on four axes, and the overall score is a judgement, not an average:

| Axis | Question |
|---|---|
| **Technical readiness** | Can it be built with parts and methods that exist today? |
| **Cost per km²** | What does it cost to cover an area, not just per unit? |
| **Persistence** | Can it run unattended for weeks or months? |
| **Deployability** | Can non-specialists put it out and keep it running at scale? |

The single most important number is **cost per square kilometre covered = node cost × node density**. Node density is driven by detection range, which differs hugely by target. See [Range and cost-per-km² model]({{ site.baseurl }}{% link research/range-and-cost.md %}).

## How to add to this

- **New research note:** add a Markdown file to `research/` with `parent: Research Notes` in the front matter.
- **New model:** copy `models/_template.md`, number it `mNN-short-name.md`, and add a row to the matrix above.
- **Changed a rating?** Say why in the model page's *Rating history* and in the [Changelog]({{ site.baseurl }}{% link changelog.md %}).
- Mark anything not yet confirmed with an `{: .warning }` callout.
