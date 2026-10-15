---
title: "M7 — Drone-deployed ground nodes"
parent: Sensor Models
nav_order: 7
---

# M7 — Drone-deployed ground nodes
{: .no_toc }

| Overall | Technical readiness | Cost per km² | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|
| **3/5** | 3/5 | 3/5 | 4/5 | 4/5 |

**Unit cost (est.):** M1 node in a drop-safe case ($80–150) + share of a reusable delivery drone
**Best against:** any target, in areas people can't safely reach
**One-line verdict:** Use the drone as the *installer*, not the sensor. Fast mesh build-out in contested or remote ground.

1. TOC
{:toc}

## How it works

- A cargo drone carries several hardened M1 nodes and places or drops them at planned points (ridgelines, field edges, rooftops).
- Each node self-orients: it reads its tilt from the accelerometer, its heading from the compass (or by listening to a known sound), and its position from GPS, then joins the mesh.
- Nodes sit on battery + small solar for weeks.

## Strengths

- Builds coverage much faster than ground crews, without exposing people.
- Nodes stay cheap and silent; only the delivery drone is expensive, and it's reused.

## Limits and risks

- Nodes on the ground sit low (less range than [M4]({{ site.baseurl }}{% link models/m04-elevated-nodes.md %})), and may land in grass, mud or at an angle.
- Drop survivability and self-calibration of heading are design problems.
- Nodes can be found and spoofed or destroyed; they need tamper and anti-spoof measures.

## Open questions

- How well can a node estimate its own heading after landing without human calibration?
- Lowest-cost drop-tolerant enclosure that keeps mics clear of mud and water.

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | Straightforward extension of M1; self-calibration untested. |
