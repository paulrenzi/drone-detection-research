---
title: "M11 — Fiber-optic distributed acoustic sensing"
parent: Sensor Models
nav_order: 11
---

# M11 — Fiber-optic distributed acoustic sensing (DAS)
{: .no_toc }

| Overall | Technical readiness | Cost per km² | Persistence | Deployability |
|:-:|:-:|:-:|:-:|:-:|
| **1–2/5** | 1/5 | 3/5 | 5/5 | 3/5 |

**Unit cost (est.):** DAS interrogator box typically tens of thousands of dollars and up; fiber itself is cheap or already in the ground
**Best against:** unknown — possibly low-flying drones directly over existing fiber routes
**One-line verdict:** Exploratory. Turns an ordinary fiber cable into thousands of vibration sensors. Proven for people, vehicles and digging near pipelines; airborne drones are only starting to be studied.

1. TOC
{:toc}

## How it works

A laser box (interrogator) sends pulses down a standard fiber and measures tiny reflections. Sound and vibration hitting the fiber change those reflections, so every few metres of cable becomes a sensor — over tens of kilometres from one box.

## Evidence so far

- DLR (German Aerospace Center) published 2026 work *towards unmanned vehicle detection using DAS*, showing detection of underwater and airborne vehicles **when close to the cable**.
- DAS is widely used for pipeline and perimeter security; one proposed use is launching a drone *to* a DAS alert, the reverse of what we want.

## Limits and risks

- Buried fiber is poorly coupled to airborne sound; sensitivity to a drone at altitude is likely low.
- The interrogator is expensive, and one cable gives a line of coverage, not an area.

## Why keep it on the list

Borders, pipelines, rail lines and highways often already have fiber. If DAS can hear low-flying drones even at short range, it adds a "free" tripwire along those routes.

## Rating history

| Date | Rating | Why |
|---|---|---|
| 2026-10-15 | 1–2 | Early research only for airborne targets. |

## Sources

- [DLR — Anhaus et al. 2026, towards unmanned vehicle detection using DAS](https://elib.dlr.de/225388/)
- [Pipeline Journal — integrated DAS and UAV solution](https://www.pipeline-journal.net/articles/integrated-solution-distributed-acoustic-sensing-fibre-optic-technology-unmanned-aerial)
