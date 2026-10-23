---
title: "M4 — Elevated fixed nodes"
parent: Sensor Models
nav_order: 4
---

# M4 — Elevated fixed nodes (towers, masts, rooftops)
{: .no_toc }

<p class="vz-lede">Not a separate sensor so much as <em>where to put M1</em>. Getting mics 33–98 ft up is probably the cheapest range gain available.</p>

<div class="vz-meters">
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Feasibility</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Payoff</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Technical readiness</span><span class="vz-dots" aria-label="5 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></span><span class="vz-meter-v">5/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Cost per sq mi</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Persistence</span><span class="vz-dots" aria-label="5 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></span><span class="vz-meter-v">5/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Deployability</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
</div>

<div class="vz-cards">
  <div class="vz-card"><p class="vz-card-num">Unit cost</p><p>M1 node ($80–150) + mount ($0 on existing structures, $100–300 for a dedicated mast) (est.)</p></div>
  <div class="vz-card"><p class="vz-card-num">Best against</p><p>everything — height helps for all targets</p></div>
  <div class="vz-card"><p class="vz-card-num">Payoff</p><p>Height is the cheapest range gain available, and range is the biggest weakness.</p></div>
</div>

## How it works

Mount nodes on telecom towers, power poles, water towers, grain silos, church steeples, tall rooftops or telescoping masts instead of 6.6 ft poles.

## Why height helps

- **Less ground noise:** traffic, people and machinery are at ground level; height puts distance between them and the mic.
- **Fewer obstacles:** buildings, trees and hills block and scatter sound. A low-flying drone behind a ridge may be inaudible at 6.6 ft but audible at 66 ft.
- **Less ground absorption:** sound travelling close over soft ground and vegetation loses energy faster.
- **Better radio range** for LoRa/mesh links at the same time.

{: .warning }
> Wind usually gets *stronger* with height, which raises wind noise at the mic. Good windscreens matter even more up high. The net gain needs field measurement.

## Real-world evidence

- **Zvook** (Ukraine, Lviv) mounts microcomputer-based acoustic sensors on **radio towers**.
- Sky Fortress mounts on ~6.6 ft (six-foot) poles — cheaper to install, but presumably a range trade-off.

## Limits and risks

- Access agreements with tower owners (telecom operators, utilities) — slow, but they have power and backhaul on site.
- Installation needs climbers or lifts; maintenance visits cost more.
- High structures are known, visible targets.

## Open questions

- Range gain at 6.6 ft vs. 33 ft vs. 98 ft for the same target and wind — the single most useful field test after basic detection works.
- Can telecom operators host nodes at scale (as Drone Rada is discussing with Lithuanian operators)?

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="rating-history" markdown="block">
<summary><span class="layer-title">Rating history</span><span class="layer-sub">Each change to the rating, and why</span></summary>

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 4 | Proven placement (Zvook); deployability limited by access/installation. |

</details>

<details class="layer" id="sources" markdown="block">
<summary><span class="layer-title">Sources</span><span class="layer-sub">Every source on this page</span></summary>

- [Startup Estonia — Zvook tests vehicle-mounted detector at NATO BATT26 (mentions tower-mounted origins)](https://ecosystem.startupestonia.ee/news/note/zvook-tests-vehicle-mounted-acoustic-drone-detector-at-nato-s-batt26)
- [TWZ — Thousands of networked microphones are tracking drones in Ukraine](https://www.twz.com/land/thousands-of-networked-microphones-are-tracking-drones-in-ukraine)

</details>
