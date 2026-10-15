---
title: "M6 — Perch-and-listen drones"
parent: Sensor Models
nav_order: 6
---

# M6 — Perch-and-listen drones
{: .no_toc }

| Overall | Technical readiness | Cost per km² | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|
| **2/5** | 2/5 | 2/5 | 3/5 | 4/5 |

**Unit cost (est.):** $300–1,500 (small airframe + M1 sensor board)
**Best against:** any target, where sensors must be placed fast or re-positioned
**One-line verdict:** The version of "drones with mics" that solves the self-noise problem: fly to a high spot, land, **shut the motors off**, listen for hours. A genuine differentiator, but R&D, not off-the-shelf.

1. TOC
{:toc}

## How it works

1. A small drone carries an M1-style mic array, GPS, compass and radio.
2. It flies to a chosen perch — rooftop, ridge, pole top, tree — and lands.
3. Motors stop. It now works exactly like a fixed elevated node ([M4]({% link models/m04-elevated-nodes.md %})), on battery or a small solar panel.
4. When needed (battery low, coverage gap moves, threat to the node) it flies to a new perch or home.

## Strengths

- Avoids the fatal flaw of flying listeners: with motors off, there's **no ego-noise**.
- Coverage can be **reshaped in minutes** — e.g. follow a unit, cover a new approach route.
- Reaches high perches without climbers or tower agreements.

## Limits and risks

- Reliable autonomous landing on rough perches is hard; wind can tip a perched drone.
- Battery for listening is small; solar on a small airframe is marginal. Expect hours to a day or two, not months.
- Much higher unit cost and maintenance than a fixed node, and they get lost.
- Heading after landing must be re-measured (compass near motors/metal is unreliable).

## Open questions

- Endurance of a perched node with motors off and a 1–2 W listening load.
- Can a cheap FPV-class frame land reliably on a flat roof or pole cap with simple vision?

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 2 | Solves the physics problem; engineering and cost unproven. |

## Sources

- See [M8 — Flying microphone swarm]({% link models/m08-flying-swarm.md %}) for the ego-noise evidence that motivates this model.
