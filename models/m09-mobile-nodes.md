---
title: "M9 — Vehicle / soldier-mounted mobile nodes"
parent: Sensor Models
nav_order: 9
---

# M9 — Vehicle and soldier-mounted mobile nodes
{: .no_toc }

<p class="vz-lede">Brings the network to where troops actually are. Vehicle noise is the main problem; works best while stopped.</p>

<div class="vz-meters">
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Feasibility</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Payoff</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Technical readiness</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Cost per sq mi</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Persistence</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Deployability</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
</div>

<div class="vz-cards">
  <div class="vz-card"><p class="vz-card-num">Unit cost</p><p>$150–1,000 (ruggedized M1 array + vehicle power) (est.)</p></div>
  <div class="vz-card"><p class="vz-card-num">Best against</p><p>threats to convoys, checkpoints and forward positions</p></div>
  <div class="vz-card"><p class="vz-card-num">Payoff</p><p>Covers units on the move, but range drops while moving.</p></div>
</div>

## How it works

- A mic array on a vehicle roof or mast (or a small one on a soldier's kit) listens for drones and reports bearings, with GPS and IMU giving the platform's position and heading.
- A stationary vehicle acts as a temporary fixed node; several vehicles form an instant local mesh.
- Detections feed the same central picture as fixed nodes, and also alert the crew directly.

## Real-world evidence

- **Zvook** tested a vehicle-mounted version of its tower-based system with the Latvian armed forces during **NATO exercise BATT26**.
- University of Salford published an experimental evaluation of acoustic drone tracking with **mobile microphone arrays**.

## Limits and risks

- Engine, tyre and wind noise while moving sharply reduce range; expect "useful when parked or slow."
- Platform motion must be removed from bearings (IMU-corrected).
- Wearable versions are tiny arrays → coarse bearings.

## Open questions

- Detection range while moving at 19–37 mph vs. stationary.
- Can engine noise be cancelled using a reference mic near the engine?

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="rating-history" markdown="block">
<summary><span class="layer-title">Rating history</span><span class="layer-sub">Each change to the rating, and why</span></summary>

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | In NATO trials; self-noise limits it on the move. |

</details>

<details class="layer" id="sources" markdown="block">
<summary><span class="layer-title">Sources</span><span class="layer-sub">Every source on this page</span></summary>

- [Startup Estonia — Zvook vehicle-mounted detector at NATO BATT26](https://ecosystem.startupestonia.ee/news/note/zvook-tests-vehicle-mounted-acoustic-drone-detector-at-nato-s-batt26)
- [University of Salford — Experimental evaluation of acoustic drone tracking using mobile microphone arrays](https://salford.figshare.com/articles/conference_contribution/Experimental_Evaluation_of_Acoustic_Drone_Tracking_using_Mobile_Microphone_Arrays/27697134/1)

</details>
