---
title: "M1 — Fixed ground mic-array mesh"
parent: Sensor Models
nav_order: 1
---

# M1 — Fixed ground mic-array mesh
{: .no_toc }

| Feasibility | Payoff | Technical readiness | Cost per km² | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|:-:|
| **4/5** | **4/5** | 4/5 | 4/5 | 4/5 | 4/5 |

**Unit cost (est.):** $60–120 per node at volume

**Best against:** engine-driven one-way attack drones (Shahed/Geran class), larger multirotors

**One-line verdict:** The recommended core. A purpose-built board that reports *bearing + class + confidence* is cheaper than a phone and gives better direction data.

**Payoff:** The layer that locates drones near a unit; any position fix needs it.

1. TOC
{:toc}

## How it works

- A small board carries **4–8 MEMS microphones** in a ring or cross, roughly **10–20 cm across**.
- Because sound reaches each mic at slightly different times, the board can compute the **direction of arrival** (bearing and, with a 3-D layout, elevation). Standard methods: GCC-PHAT time differences, SRP-PHAT or MUSIC beamforming.
- A small neural classifier on the board decides *what* it hears (Shahed engine, quadcopter, motorbike, generator, aircraft…).
- The node sends a tiny report: `time, node position, bearing, elevation, class, confidence`. No raw audio leaves the node, which keeps bandwidth low and avoids recording people.
- The server intersects bearings from **three or more nodes** to get a position, and a tracking filter (Kalman / multi-target tracker) turns positions into tracks.

See [Localization methods]({{ site.baseurl }}{% link research/localization.md %}) for detail.

## Bill of materials (estimate, volume pricing)

| Part | Example | Cost |
|---|---|---|
| Processor | ESP32-S3 (or RP2350 / small Cortex-M7 for more DSP) | $4–10 |
| Microphones ×4–8 | INMP441 / ICS-43434 I²S MEMS | $4–20 |
| GPS with timing pulse (PPS) | u-blox M10-class module | $8–15 |
| Compass / IMU (for absolute bearing) | magnetometer + accelerometer | $2–6 |
| Radio | LoRa SX1262 module **or** LTE Cat-M/NB-IoT modem | $6–25 |
| Solar panel + LiFePO₄ battery + charger | 5–10 W panel, 6–12 Ah | $20–40 |
| Weatherproof enclosure + **wind protection** (foam + fur) | IP65 box, acoustic mesh | $8–20 |
| PCB, assembly, mounting | | $8–15 |
| **Total** | | **≈ $60–150** |

Full detail and alternatives: [Hardware notes]({{ site.baseurl }}{% link research/hardware.md %}).

## Strengths

- Roughly **4–8× cheaper** than the current $400–1,000 per-sensor benchmark.
- Produces **bearings**, which triangulate far better than "detected / not detected" from a single mic.
- Low power: on-device processing plus small reports means solar operation for months.
- No phone OS, app store, SIM churn or screen to break; easier to harden and to certify.

## Limits and risks

- **Small electric quadcopters are quiet.** Expect hundreds of metres, not kilometres, so coverage against them needs much denser nodes.
- **Wind noise** is the biggest real-world degrader of range. Needs good windscreens and wind-aware detection thresholds.
- **Compass error** directly becomes bearing error. Needs calibration at install (e.g. point at a known landmark or use two GPS fixes).
- **GPS jamming.** GPS gives each node its position and clock, and front-line jamming reaches 20–25 km ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)). A node that never moves needs its position only once, from a survey at install. Keeping clocks in step is the harder part. A reader suggested an alternative: nodes measure their distance to one surveyed central node by radio time of flight (SX1280-class radio, 2.4 GHz). One published outdoor test measured an average error of 46 m at up to 1.4 km, cut below 10 m by a correction fitted to that same route ([Müller et al., 2021](https://digitalcollection.zhaw.ch/bitstream/11475/22769/3/2021_Mueller-etal_Outdoor-ranging-and-positioning-based-on-LoRa-modulation.pdf)). That is coarse for this model and unmeasured under trees, and each exchange is another emission. A time beacon from the same anchor, or calibrating nodes against the delivery drone's logged track as it flies over, may do better. See [T16]({{ site.baseurl }}{% link research/open-questions.md %}#t16-positions-and-clocks-without-gps).
- **False alarms** from mopeds, chainsaws, generators, aircraft. Needs lots of local negative training data.
- **Multiple simultaneous drones:** matching the right bearings to the right target is a real algorithm problem ("data association").
- A custom board means a hardware design cycle, certification (radio), and a supply chain.

## Open questions (what would change the rating)

- Measured detection range for a real Shahed-class engine and for common FPV/quads, per wind condition.
- Measured bearing accuracy from a 15 cm 4-mic array vs. an 8-mic array — is the extra cost worth it?
- How many false alarms per node per day in a farm, a town, and near a highway?
- LoRa mesh vs. cellular: latency and reliability with hundreds of nodes reporting during a raid.
- Under GPS jamming, can a surveyed anchor (ranging, a time beacon) or a calibration flyby keep node positions and clocks good enough? ([T16]({{ site.baseurl }}{% link research/open-questions.md %}#t16-positions-and-clocks-without-gps))

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 4 | Initial assessment. All parts exist; not yet field-tested by us. |

## Sources

- [TWZ — Ukraine's acoustic network eyed by U.S. as low-cost air defense](https://www.twz.com/air/ukraines-acoustic-drone-detection-network-eyed-by-u-s-as-low-cost-air-defense-option)
- [Robin Radar — acoustic sensors for drone detection (overview of strengths/limits)](https://www.robinradar.com/blog/acoustic-sensors-drone-detection)
