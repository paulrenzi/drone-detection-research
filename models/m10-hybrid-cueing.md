---
title: "M10 — Hybrid: acoustic + passive RF + camera"
parent: Sensor Models
nav_order: 10
---

# M10 — Hybrid: acoustic + passive RF + camera cueing
{: .no_toc }

| Overall | Technical readiness | Cost per km² | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|
| **4/5** | 4/5 | 3/5 | 4/5 | 3/5 |

**Unit cost (est.):** acoustic nodes everywhere ($60–120 each) + RF sensor ($50–500) and PTZ/thermal camera ($300–2,000+) at selected sites
**Best against:** all targets, including confirming what the acoustic layer flags
**One-line verdict:** Acoustic as the cheap wide-area tripwire, other sensors only where they add the most. This is how a credible military system will be judged.

1. TOC
{:toc}

## How it works

| Layer | What it adds | Cheap version |
|---|---|---|
| **Acoustic mesh (M1)** | Wide coverage, works without line of sight, works against **fibre-optic FPVs and pre-programmed drones that emit no radio** | ESP32 + MEMS array |
| **Passive RF** | Detects control/video links (2.4/5.8 GHz, 900 MHz, etc.); can give direction to the drone *and* the pilot | Software-defined radio (RTL-SDR/HackRF-class) + directional antennas |
| **Camera (visible/thermal)** | Confirms the target and gives a precise bearing/elevation | PTZ camera slewed to the acoustic track |
| **Radar data (if available)** | Precise range and speed | Fused from existing military radar feeds |

The acoustic track **cues** the camera or RF sensor where to look; agreement between layers cuts false alarms sharply.

## Strengths

- Each layer covers another's blind spot. Acoustic catches what RF misses (fibre-optic and autonomous drones); RF and cameras catch quiet electric drones that acoustic hears only at short range.
- Sky Fortress already fuses acoustic data with radar feeds.

## Limits and risks

- Integration work: shared timestamps, shared coordinate frames, track fusion.
- Cameras and RF sensors need power and bandwidth; place them sparingly.
- Passive RF raises legal issues in peacetime (intercepting communications).

## Open questions

- What's the false-alarm reduction when acoustic + camera must agree?
- Cheapest camera that can confirm a small quad at 300–500 m.

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 4 | All components exist; integration is engineering, not research. |

## Sources

- [Militarnyi — SkyFortress fuses acoustic and radar data](https://militarnyi.com/en/news/lit-ukr-skyfortress-acoustic-uav-detection/)
- [arXiv 2007.07396 — Real-time drone detection with visible, thermal and acoustic sensors](https://arxiv.org/pdf/2007.07396)
