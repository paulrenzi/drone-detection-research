---
title: "M2 — Phone-based sensor network"
parent: Sensor Models
nav_order: 2
---

# M2 — Phone-based sensor network
{: .no_toc }

<p class="vz-lede">Proven at national scale. The benchmark to beat on cost, not a dead end — and the fastest way to stand up coverage.</p>

<div class="vz-meters">
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Feasibility</span><span class="vz-dots" aria-label="5 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></span><span class="vz-meter-v">5/5</span></div>
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Payoff</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Technical readiness</span><span class="vz-dots" aria-label="5 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></span><span class="vz-meter-v">5/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Cost per sq mi</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Persistence</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Deployability</span><span class="vz-dots" aria-label="5 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></span><span class="vz-meter-v">5/5</span></div>
</div>

<div class="vz-cards">
  <div class="vz-card"><p class="vz-card-num">Unit cost</p><p>$100–500 (used phone + mic + mount + power); Sky Fortress reports $400–1,000 per sensor (est.)</p></div>
  <div class="vz-card"><p class="vz-card-num">Best against</p><p>Shahed-class engine drones and cruise missiles at low altitude</p></div>
  <div class="vz-card"><p class="vz-card-num">Payoff</p><p>Proven and fast, but needs cell coverage and power, which units at the front often lack.</p></div>
</div>

## How it works

- A smartphone (often used/refurbished Android) is connected to an external microphone on a ~6.6 ft pole, with mains or solar power.
- An app detects target sounds and reports detections with the phone's GPS position over the cell network.
- A central system fuses reports from many phones to estimate the drone's path and pushes it to mobile fire teams on tablets.

## Real-world evidence

- **Ukraine — Sky Fortress:** roughly 9,500–10,000 sensors reported in 2024–25, ~14,000 by July 2025; total network cost around $5M; built by two engineers starting in a garage. In one reported raid, 84 drones were detected and 80 engaged.
- **USAFE** (Gen. James Hecker) publicly pushed NATO to copy the approach; testing at Ramstein and in Romania.
- **Lithuania** has contracted a Sky Fortress pilot (2025–26).
- **Lithuania — Drone Rada (Mainline):** a civic, crowd-sourced Android app; volunteers leave a powered phone by a window. Goal of 10,000 participants (June 2026).

## Strengths

- Everything needed — processor, GPS, cellular modem, battery, OS updates — comes in one cheap, mass-produced package.
- Software can be pushed to thousands of devices instantly.
- Crowd-sourced variants can cover cities at almost zero hardware cost to the operator.

## Limits and risks

- Phones have one or two closely spaced mics, so they give **little or no direction information**. Location comes from *which* phones heard it and *when*, which needs high node density.
- Phones aren't built for outdoor, months-long, solar-powered duty: heat, cold, battery swelling, OS updates, app killing.
- Depends on the cellular network, which is a target in wartime.
- Crowd-sourced phones in homes have unknown placement and noise, so data quality varies.

## Where it fits

Use phones **now** to get coverage, and as the comparison baseline for M1. A hybrid — a phone as the "brain" plus a cheap USB mic-array — is a reasonable middle step before a custom board.

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="rating-history" markdown="block">
<summary><span class="layer-title">Rating history</span><span class="layer-sub">Each change to the rating, and why</span></summary>

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 5 | Operational at national scale in Ukraine. |

</details>

<details class="layer" id="sources" markdown="block">
<summary><span class="layer-title">Sources</span><span class="layer-sub">Every source on this page</span></summary>

- [TWZ — Ukraine's acoustic network eyed by U.S.](https://www.twz.com/air/ukraines-acoustic-drone-detection-network-eyed-by-u-s-as-low-cost-air-defense-option)
- [TWZ — Thousands of networked microphones are tracking drones in Ukraine](https://www.twz.com/land/thousands-of-networked-microphones-are-tracking-drones-in-ukraine)
- [NV — Sky Fortress](https://english.nv.ua/russian-war/ukrainian-engineers-develop-sky-fortress-drone-detection-system-to-counter-shaheds-50520480.html)
- [Militarnyi — Lithuania deploys SkyFortress](https://militarnyi.com/en/news/lit-ukr-skyfortress-acoustic-uav-detection/)
- [Euromaidan Press — Lithuania selects Ukrainian tech (14,000 sensors, $400–1,000)](https://euromaidanpress.com/2025/07/29/lithuania-to-deploy-ukrainian-drone-detection-system-by-2026-after-russian-airspace-violations/)
- [LRT — Drone Rada crowd-sourced network (June 2026)](https://www.lrt.lt/en/news-in-english/19/2965205/lithuanian-startup-launches-open-source-network-to-detect-shahed-type-drones)

</details>
