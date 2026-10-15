---
title: "M8 — Flying microphone drone swarm"
parent: Sensor Models
nav_order: 8
---

# M8 — Flying microphone drone swarm
{: .no_toc }

| Overall | Technical readiness | Cost per km² | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|
| **1/5** | 2/5 | 1/5 | 1/5 | 2/5 |

**Unit cost (est.):** $200–2,000 per airframe, plus spares, chargers and operators
**Best against:** —
**One-line verdict:** Not recommended as a detection layer. A flying drone's own propellers drown out the target it's listening for. See [M6]({{ site.baseurl }}{% link models/m06-perch-and-listen.md %}) for the variant that works.

1. TOC
{:toc}

## How it works (as proposed)

A swarm of very small drones, each carrying a microphone, flies in a pattern over the area and listens for other drones.

## Why it fails

- **Ego-noise:** the listener's own rotors are centimetres from its microphone. Published research measures signal-to-noise ratios around **−10 to −15 dB** for sounds captured from a flying micro air vehicle — the target is 10–30× quieter than the drone's own noise. DroneAudioset recordings go as low as **−57 dB**. Smaller drones put the rotors even closer to the mic.
- **Endurance:** micro drones fly ~5–20 minutes. Continuous coverage needs several airframes rotating per point, plus charging.
- **Cost per km²:** many times the cost of a fixed node, with ongoing losses.
- **Signature:** a swarm is noisy, emits RF, is easy to spot and jam, and may be mistaken for the threat by friendly air defence.

## What research does exist

Ego-noise reduction (beamforming, spatial filtering, blind source separation) is an active topic, mainly for search-and-rescue — detecting a shouting person, not a distant drone. It improves things, but not enough to beat a silent ground node.

## What would change the rating

A step-change in quiet propulsion, or very effective ego-noise cancellation that recovers a distant drone at useful range in field tests.

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 1 | Ego-noise, endurance and cost each independently rule it out for persistent detection. |

## Sources

- [DroneAudioset (arXiv 2510.15383)](https://arxiv.org/html/2510.15383v1)
- [QMUL — microphone-array ego-noise reduction for micro aerial vehicles](https://webspace.eecs.qmul.ac.uk/lin.wang/demo/auditory-mav.html)
- [SAGE — UAV detection from an onboard microphone array](https://journals.sagepub.com/doi/abs/10.1177/1756829320925748)
