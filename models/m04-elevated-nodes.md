---
title: "M4 — Elevated fixed nodes"
parent: Sensor Models
nav_order: 4
---

# M4 — Elevated fixed nodes (towers, masts, rooftops)
{: .no_toc }

| Feasibility | Payoff | Technical readiness | Cost per sq mi | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|:-:|
| **4/5** | **4/5** | 5/5 | 4/5 | 5/5 | 3/5 |

**Unit cost (est.):** M1 node ($80–150) + mount ($0 on existing structures, $100–300 for a dedicated mast)

**Best against:** everything — height helps for all targets

**One-line verdict:** Not a separate sensor so much as *where to put M1*. Getting mics 33–98 ft up is probably the cheapest range gain available.

**Payoff:** Height is the cheapest range gain available, and range is the biggest weakness.

1. TOC
{:toc}

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

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 4 | Proven placement (Zvook); deployability limited by access/installation. |

## Sources

- [Startup Estonia — Zvook tests vehicle-mounted detector at NATO BATT26 (mentions tower-mounted origins)](https://ecosystem.startupestonia.ee/news/note/zvook-tests-vehicle-mounted-acoustic-drone-detector-at-nato-s-batt26)
- [TWZ — Thousands of networked microphones are tracking drones in Ukraine](https://www.twz.com/land/thousands-of-networked-microphones-are-tracking-drones-in-ukraine)
