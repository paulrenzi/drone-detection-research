---
title: "M7 — Drone-deployed ground nodes"
parent: Sensor Models
nav_order: 7
---

# M7 — Drone-deployed ground nodes
{: .no_toc }

<p class="vz-lede">Use the drone as the <em>installer</em>, not the sensor. Fast mesh build-out in contested or remote ground.</p>

<div class="vz-meters">
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Feasibility</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Payoff</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Technical readiness</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Cost per sq mi</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Persistence</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Deployability</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
</div>

<div class="vz-cards">
  <div class="vz-card"><p class="vz-card-num">Unit cost</p><p>M1 node in a drop-safe case ($80–150) + share of a reusable delivery drone (est.)</p></div>
  <div class="vz-card"><p class="vz-card-num">Best against</p><p>any target, in areas people can't safely reach</p></div>
  <div class="vz-card"><p class="vz-card-num">Payoff</p><p>The delivery method behind the drone-laid tripwire.</p></div>
</div>

## How it works

- A cargo drone carries several hardened M1 nodes and places or drops them at planned points (ridgelines, field edges, rooftops).
- Each node self-orients: it reads its tilt from the accelerometer, its heading from the compass (or by listening to a known sound), and its position from GPS, then joins the mesh.
- Nodes sit on battery + small solar for weeks.
- The delivery drone flies a pre-loaded ArduPilot mission with a drop step at each point and no radio link in flight. See [Delivery drone]({{ site.baseurl }}{% link research/delivery-drone.md %}).

## Strengths

- Builds coverage much faster than ground crews, without exposing people.
- Nodes stay cheap and silent; only the delivery drone is expensive, and it's reused.

## Limits and risks

- Nodes on the ground sit low (less range than [M4]({{ site.baseurl }}{% link models/m04-elevated-nodes.md %})), and may land in grass, mud or at an angle.
- Drop survivability and self-calibration of heading are design problems.
- Nodes can be found and spoofed or destroyed; they need tamper and anti-spoof measures.
- GPS is routinely jammed at the front ([Front-line conditions]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)), so neither the delivery drone nor the nodes can count on it.

## Open questions

- How well can a node estimate its own heading after landing without human calibration?
- Lowest-cost drop-tolerant enclosure that keeps mics clear of mud and water.

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="rating-history" markdown="block">
<summary><span class="layer-title">Rating history</span><span class="layer-sub">Each change to the rating, and why</span></summary>

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | Straightforward extension of M1; self-calibration untested. |

</details>
