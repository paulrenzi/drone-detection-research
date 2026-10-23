---
title: "M3 — Single-mic nodes + time-difference"
parent: Sensor Models
nav_order: 3
---

# M3 — Single-mic nodes + time-difference of arrival
{: .no_toc }

<p class="vz-lede">Cheapest hardware, but shifts all the difficulty into timing and computation. Better as a cross-check inside M1 than as the whole system.</p>

<div class="vz-meters">
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Feasibility</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter vz-meter-key"><span class="vz-meter-name">Payoff</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Technical readiness</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Cost per sq mi</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Persistence</span><span class="vz-dots" aria-label="4 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i></span><span class="vz-meter-v">4/5</span></div>
  <div class="vz-meter"><span class="vz-meter-name">Deployability</span><span class="vz-dots" aria-label="3 of 5"><i class="on"></i><i class="on"></i><i class="on"></i><i class=""></i><i class=""></i></span><span class="vz-meter-v">3/5</span></div>
</div>

<div class="vz-cards">
  <div class="vz-card"><p class="vz-card-num">Unit cost</p><p>$30–50 (est.)</p></div>
  <div class="vz-card"><p class="vz-card-num">Best against</p><p>loud, continuous sources (Shahed-class) in areas with dense nodes</p></div>
  <div class="vz-card"><p class="vz-card-num">Payoff</p><p>Too sparse to locate drones on its own, but its low cost is what makes throwaway tripwire nodes possible.</p></div>
</div>

## How it works

- Each node has **one microphone**, GPS, and a radio. No direction finding on the node.
- Nodes timestamp sound features very precisely using the **GPS timing pulse (PPS)**.
- The server compares *when* each node heard the same sound. The time differences define hyperbolas; where they cross is the source (multilateration, like how gunshot-detection systems work).
- Sound travels ~13 in per millisecond, so ~1 ms timing error ≈ 12 in of path difference — GPS timing (≪1 ms) is good enough.

## Strengths

- Cheapest possible node — no array, simpler board.
- Accuracy can be good *if* the nodes are spread widely around the target (wide baseline).

## Limits and risks

- Needs the **same sound** matched across nodes miles apart. A drone's sound is continuous, not a sharp bang like a gunshot, so the match must use cross-correlation of streamed features — **more data to send** and more server work.
- Nodes far apart hear the drone through different wind, echoes and Doppler, which smears the timing.
- Needs at least 3–4 nodes hearing simultaneously; with weak targets that's rare.
- Bandwidth: LoRa can't carry correlation snippets from many nodes during a mass raid.
- **GPS jamming removes the timing pulse** this model depends on, and front-line jamming reaches 12–16 mi ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)). Positions can be surveyed once, but clocks drift without it. Radio ranging to a central anchor, suggested by a reader, is too coarse for positions here: the best published outdoor figure we found is an average error under 33 ft after correction ([Müller et al., 2021](https://digitalcollection.zhaw.ch/bitstream/11475/22769/3/2021_Mueller-etal_Outdoor-ranging-and-positioning-based-on-LoRa-modulation.pdf)), and 33 ft is about 30 ms of sound travel. A time beacon from a surveyed anchor is the more promising half; its accuracy is unmeasured. See [T16]({{ site.baseurl }}{% link research/open-questions.md %}#t16-positions-and-clocks-without-gps).

## Open questions

- Can a compact feature (e.g. engine harmonic phase over 1–2 s) be correlated across nodes reliably enough to send over LoRa?
- What's the accuracy versus M1 bearings for the same node count?
- Without GPS, how closely can a time beacon from a surveyed anchor keep node clocks in step? ([T16]({{ site.baseurl }}{% link research/open-questions.md %}#t16-positions-and-clocks-without-gps))

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="rating-history" markdown="block">
<summary><span class="layer-title">Rating history</span><span class="layer-sub">Each change to the rating, and why</span></summary>

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | Physics is sound; matching continuous sound across distant nodes is unproven at low bandwidth. |

</details>

<details class="layer" id="sources" markdown="block">
<summary><span class="layer-title">Sources</span><span class="layer-sub">Every source on this page</span></summary>

- See [Localization methods]({{ site.baseurl }}{% link research/localization.md %}).

</details>
