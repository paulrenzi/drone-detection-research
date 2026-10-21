---
title: "M9 — Vehicle / soldier-mounted mobile nodes"
parent: Sensor Models
nav_order: 9
---

# M9 — Vehicle and soldier-mounted mobile nodes
{: .no_toc }

| Feasibility | Payoff | Technical readiness | Cost per sq mi | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|:-:|
| **3/5** | **3/5** | 3/5 | 3/5 | 4/5 | 4/5 |

**Unit cost (est.):** $150–1,000 (ruggedized M1 array + vehicle power)

**Best against:** threats to convoys, checkpoints and forward positions

**One-line verdict:** Brings the network to where troops actually are. Vehicle noise is the main problem; works best while stopped.

**Payoff:** Covers units on the move, but range drops while moving.

1. TOC
{:toc}

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

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | In NATO trials; self-noise limits it on the move. |

## Sources

- [Startup Estonia — Zvook vehicle-mounted detector at NATO BATT26](https://ecosystem.startupestonia.ee/news/note/zvook-tests-vehicle-mounted-acoustic-drone-detector-at-nato-s-batt26)
- [University of Salford — Experimental evaluation of acoustic drone tracking using mobile microphone arrays](https://salford.figshare.com/articles/conference_contribution/Experimental_Evaluation_of_Acoustic_Drone_Tracking_using_Mobile_Microphone_Arrays/27697134/1)
