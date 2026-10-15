---
title: "M3 — Single-mic nodes + time-difference"
parent: Sensor Models
nav_order: 3
---

# M3 — Single-mic nodes + time-difference of arrival
{: .no_toc }

| Feasibility | Payoff | Technical readiness | Cost per km² | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|:-:|
| **3/5** | **3/5** | 3/5 | 4/5 | 4/5 | 3/5 |

**Unit cost (est.):** $30–50

**Best against:** loud, continuous sources (Shahed-class) in areas with dense nodes

**One-line verdict:** Cheapest hardware, but shifts all the difficulty into timing and computation. Better as a cross-check inside M1 than as the whole system.

**Payoff:** Too sparse to locate drones on its own, but its low cost is what makes throwaway tripwire nodes possible.

1. TOC
{:toc}

## How it works

- Each node has **one microphone**, GPS, and a radio. No direction finding on the node.
- Nodes timestamp sound features very precisely using the **GPS timing pulse (PPS)**.
- The server compares *when* each node heard the same sound. The time differences define hyperbolas; where they cross is the source (multilateration, like how gunshot-detection systems work).
- Sound travels ~34 cm per millisecond, so ~1 ms timing error ≈ 0.3 m of path difference — GPS timing (≪1 ms) is good enough.

## Strengths

- Cheapest possible node — no array, simpler board.
- Accuracy can be good *if* the nodes are spread widely around the target (wide baseline).

## Limits and risks

- Needs the **same sound** matched across nodes kilometres apart. A drone's sound is continuous, not a sharp bang like a gunshot, so the match must use cross-correlation of streamed features — **more data to send** and more server work.
- Nodes far apart hear the drone through different wind, echoes and Doppler, which smears the timing.
- Needs at least 3–4 nodes hearing simultaneously; with weak targets that's rare.
- Bandwidth: LoRa can't carry correlation snippets from many nodes during a mass raid.

## Open questions

- Can a compact feature (e.g. engine harmonic phase over 1–2 s) be correlated across nodes reliably enough to send over LoRa?
- What's the accuracy versus M1 bearings for the same node count?

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | Physics is sound; matching continuous sound across distant nodes is unproven at low bandwidth. |

## Sources

- See [Localization methods]({{ site.baseurl }}{% link research/localization.md %}).
