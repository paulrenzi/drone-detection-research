---
title: "M2 — Phone-based sensor network"
parent: Sensor Models
nav_order: 2
---

# M2 — Phone-based sensor network
{: .no_toc }

| Feasibility | Payoff | Technical readiness | Cost per sq mi | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|:-:|
| **5/5** | **3/5** | 5/5 | 3/5 | 3/5 | 5/5 |

**Unit cost (est.):** $100–500 (used phone + mic + mount + power); Sky Fortress reports $400–1,000 per sensor

**Best against:** Shahed-class engine drones and cruise missiles at low altitude

**One-line verdict:** Proven at national scale. The benchmark to beat on cost, not a dead end — and the fastest way to stand up coverage.

**Payoff:** Proven and fast, but needs cell coverage and power, which units at the front often lack.

1. TOC
{:toc}

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

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 5 | Operational at national scale in Ukraine. |

## Sources

- [TWZ — Ukraine's acoustic network eyed by U.S.](https://www.twz.com/air/ukraines-acoustic-drone-detection-network-eyed-by-u-s-as-low-cost-air-defense-option)
- [TWZ — Thousands of networked microphones are tracking drones in Ukraine](https://www.twz.com/land/thousands-of-networked-microphones-are-tracking-drones-in-ukraine)
- [NV — Sky Fortress](https://english.nv.ua/russian-war/ukrainian-engineers-develop-sky-fortress-drone-detection-system-to-counter-shaheds-50520480.html)
- [Militarnyi — Lithuania deploys SkyFortress](https://militarnyi.com/en/news/lit-ukr-skyfortress-acoustic-uav-detection/)
- [Euromaidan Press — Lithuania selects Ukrainian tech (14,000 sensors, $400–1,000)](https://euromaidanpress.com/2025/07/29/lithuania-to-deploy-ukrainian-drone-detection-system-by-2026-after-russian-airspace-violations/)
- [LRT — Drone Rada crowd-sourced network (June 2026)](https://www.lrt.lt/en/news-in-english/19/2965205/lithuanian-startup-launches-open-source-network-to-detect-shahed-type-drones)
