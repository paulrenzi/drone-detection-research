---
title: Range and cost-per-km² model
parent: Research Notes
nav_order: 2
nav_tripwire: 4
---

# Range and cost-per-km² model
{: .no_toc }

1. TOC
{:toc}

## The metric that matters

**Cost per km² = node cost × nodes per km².**
Node density is set by how far a node can hear the target, and by the need for **at least three nodes** to hear it at once (for a position fix from bearings).

A simple layout rule: on a triangular grid with spacing equal to the detection range *r*, most points are heard by ≥3 nodes. That grid needs about **1.15 / r² nodes per km²** (r in km).

## Detection range by target (working estimates)

{: .warning }
> These ranges are planning guesses from public reporting and the general acoustics of each target. They must be replaced with field measurements. Wind, terrain, time of day and background noise can halve or double them.

| Target | Sound source | Working range estimate |
|---|---|---|
| Shahed/Geran-class one-way attack drone | Piston engine, propeller — loud, tonal | 1–5 km |
| Cruise missile at low altitude | Jet/turbofan | 1–5 km |
| Large multirotor / Mavic-class | Electric motors, props | 200–500 m |
| Small FPV quad | Electric, small props, high-pitched | 100–300 m |
| Fibre-optic FPV | Same as FPV — no RF, so acoustic is one of few options | 100–300 m |

Squarehead's commercial array claims small-drone detection out to "several hundred metres", consistent with the middle rows.

The first published field number for a cheap node comes from the open-source [VolAnti]({{ site.baseurl }}{% link research/open-source-builds.md %}#volanti) unit: a hovering quad detected at **104.2 m** on a street with traffic, with expected range falling from 100–200 m in still air to 5–25 m in strong wind. That supports the low end of the small-quad rows and shows how much wind matters.

**Published measurements point lower still** ([full table]({{ site.baseurl }}{% link research/competitors.md %}#what-is-actually-measured)):
- **Cheap MEMS array:** eight cheap MEMS microphones on an ESP32-S3 detected a DJI Phantom to about 50 m, with an effective range of about 60 m and 5–8% false positives (Ghouli, *Acta Acustica* 2026).
- **Speaker tone:** studio and shotgun microphones heard a speaker tone set to a hovering drone's level at 69–94 m in low wind and 36–46 m in high wind (*Sensors* 2025).
- **None of these used an FPV.** Treat 100–300 m for FPVs as unproven until T11.

## Worked examples

| Range *r* | Nodes / km² | At $100 / node | At $450 / node (phone benchmark) |
|---|---|---|---|
| 3 km | 0.13 | **$13 / km²** | $58 / km² |
| 1 km | 1.15 | **$115 / km²** | $518 / km² |
| 300 m | 12.8 | **$1,280 / km²** | $5,750 / km² |
| 150 m | 51 | **$5,100 / km²** | $23,000 / km² |

Takeaways:

- Against Shahed-class targets, area coverage is **cheap** at any node price — national-scale coverage is realistic (Ukraine shows this).
- Against small electric drones, density explodes. Wide-area coverage is unrealistic; protect **points** (bases, positions, critical infrastructure) instead.
- Halving node cost and **doubling range** are worth the same: doubling range cuts density by 4×. Range improvements (height, windscreens, better arrays and classifiers) may be the bigger lever.

## What drives range

- **Source loudness and frequency:** low-frequency engine tones travel further; high-pitched small props fade faster.
- **Spreading loss:** ~6 dB lost per doubling of distance, plus air absorption that grows with frequency.
- **Background noise:** a quiet rural night vs. a city day can be 30 dB apart.
- **Wind:** turbulence at the mic adds low-frequency noise; wind direction also bends sound.
- **Terrain and height:** obstacles block; ground absorbs; height helps (see [M4]({{ site.baseurl }}{% link models/m04-elevated-nodes.md %})).
- **Array gain:** combining N mics adds up to ~10·log₁₀(N) dB against diffuse noise — about 6 dB for 4 mics, 9 dB for 8.
