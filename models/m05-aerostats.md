---
title: "M5 — Tethered aerostats / balloons"
parent: Sensor Models
nav_order: 5
---

# M5 — Tethered aerostats and balloons
{: .no_toc }

<p class="vz-lede">A quiet way to get mics (and radios) very high for days at a time. A gap-filler for valleys and coastlines, not a replacement for the ground mesh.</p>

<div class="vz-meters">
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Feasibility</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Payoff</span><span class="vz-dots" aria-label="2 of 5"><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">2/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Technical readiness</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Cost per sq mi</span><span class="vz-dots" aria-label="2 of 5"><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">2/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Persistence</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Deployability</span><span class="vz-dots" aria-label="2 of 5"><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">2/5</span></div>
</div>

<div class="vz-cards">
  <div class="vz-card"><p class="vz-card-num">Unit cost</p><p>small helium balloon kits from ~$5k; military tethered aerostats $50k to millions (est.)</p></div>
  <div class="vz-card"><p class="vz-card-num">Best against</p><p>low-flying drones and cruise missiles hidden from ground sensors by terrain</p></div>
  <div class="vz-card"><p class="vz-card-num">Payoff</p><p>A useful gap-filler at fixed sites; too costly and visible for most units.</p></div>
</div>

## How it works

A helium balloon or aerostat on a tether lifts a mic array (and often a radio relay and camera) to 160–1,600 ft. Power and data can run up the tether. It hears over hills and buildings that block ground nodes.

## Real-world evidence

- In Feb 2024, **Gen. Hecker (USAFE)** said the U.S. aimed to field **tethered aerostats** with detection payloads against one-way attack drones "within six months to a year," noting they must be reeled down in strong wind.

{: .warning }
> Some press reports describe "6,000 microphone-laden balloons" in Ukraine. The underlying quote appears to refer to ~6,000 *ground* acoustic sensors plus a separate aerostat plan. Treat the balloon figure as unverified.

## Strengths

- Silent platform — no rotor noise, unlike a hovering drone.
- Stays up for days; tethered power removes battery limits.
- One high node can cover the gap that would need many ground nodes in rough terrain.

## Limits and risks

- **Wind:** must come down in high wind; tether hum and balloon motion add noise and bearing error.
- Highly visible and easy to shoot down; helium logistics.
- Airspace coordination with friendly aircraft.
- Costs far more per unit than M1; worth it only where terrain makes ground coverage expensive.

## Open questions

- Bearing stability on a moving, swaying platform (needs an IMU-corrected array).
- Cheapest viable kit: weather balloon + small tether vs. purpose-built aerostat.

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="rating-history" markdown="block">
<summary><span class="layer-title">Rating history</span><span class="layer-sub">Each change to the rating, and why</span></summary>

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | Known platform, US interest; cost and wind limit it to niche use. |

</details>

<details class="layer" id="sources" markdown="block">
<summary><span class="layer-title">Sources</span><span class="layer-sub">Every source on this page</span></summary>

- [Interesting Engineering — Hecker on acoustic sensors and tethered aerostats (Feb 2024)](https://interestingengineering.com/military/ukraine-microphone-laden-balloons-awe-us)

</details>
