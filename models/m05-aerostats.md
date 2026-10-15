---
title: "M5 — Tethered aerostats / balloons"
parent: Sensor Models
nav_order: 5
---

# M5 — Tethered aerostats and balloons
{: .no_toc }

| Overall | Technical readiness | Cost per km² | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|
| **3/5** | 4/5 | 2/5 | 3/5 | 2/5 |

**Unit cost (est.):** small helium balloon kits from ~$5k; military tethered aerostats $50k to millions
**Best against:** low-flying drones and cruise missiles hidden from ground sensors by terrain
**One-line verdict:** A quiet way to get mics (and radios) very high for days at a time. A gap-filler for valleys and coastlines, not a replacement for the ground mesh.

1. TOC
{:toc}

## How it works

A helium balloon or aerostat on a tether lifts a mic array (and often a radio relay and camera) to 50–500 m. Power and data can run up the tether. It hears over hills and buildings that block ground nodes.

## Real-world evidence

- In Feb 2024, **Gen. Hecker (USAFE)** said the U.S. aimed to field **tethered aerostats** with detection payloads against one-way attack drones "within six months to a year," noting they must be reeled down in strong wind.

{: .warning }
> Some press reports describe "6,000 microphone-laden balloons" in Ukraine. The underlying quote appears to refer to ~6,000 *ground* acoustic sensors plus a separate aerostat plan. Treat the balloon figure as unverified.

## Strengths

- Silent platform — no rotor noise, unlike a hovering drone ([M8]({% link models/m08-flying-swarm.md %})).
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

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 3 | Known platform, US interest; cost and wind limit it to niche use. |

## Sources

- [Interesting Engineering — Hecker on acoustic sensors and tethered aerostats (Feb 2024)](https://interestingengineering.com/military/ukraine-microphone-laden-balloons-awe-us)
