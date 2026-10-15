---
title: Central API and military integration
parent: Research Notes
nav_order: 6
---

# Central API and military integration
{: .no_toc }

1. TOC
{:toc}

## What "a centralized API to plot drones" should mean

The military doesn't want a new app. It wants tracks to appear in the tools it already uses. Build the fusion server to **output standard formats**:

| Standard | What it is | Why it matters |
|---|---|---|
| **Cursor-on-Target (CoT)** | Simple XML event format for "something is at this place" | Native to **TAK** (ATAK/WinTAK/iTAK), used widely by US and allied forces and by Ukraine |
| **Anduril Lattice** | Anduril's sensor-fusion and command-and-control software | The US Army's counter-drone backbone; **first integration target** (see below) |
| **SAPIENT** | UK MOD open interface standard for counter-UAS sensors and fusion nodes | Adopted in NATO counter-UAS interoperability work; lets a sensor plug into others' C2 systems |
| GeoJSON / REST / WebSocket | Plain web API | For dashboards, partners, testing |

## Suggested data flow

1. **Node → server:** detection report (time, node position, bearing, elevation, class, confidence). Small enough for LoRa.
2. **Server:** association → triangulation → tracking → threat classification.
3. **Server → users:** CoT to TAK, SAPIENT to C2, GeoJSON to a web map; alerts to fire teams with predicted path.

## Anduril Lattice

Lattice is the integration that matters most. The US Army awarded Anduril an enterprise contract worth up to $20B over 10 years, and JIATF-401 picked Lattice as its counter-UAS command-and-control platform (see [Competitors]({{ site.baseurl }}{% link research/competitors.md %})). A sensor that feeds Lattice reaches the buyer directly.

**What we would send:** each detection as a Lattice track or entity, with position (or bearing from the node), time, class and confidence. Acoustic bearings can cue Anduril's own WISP cameras onto drones they would otherwise miss behind terrain or trees.

**How partners plug in:** Anduril publishes a Lattice SDK for partners, with data model definitions, API bindings, code samples and reference implementations, and runs a Lattice Partner Program. In a CENTCOM exercise, more than 10 sensor teams used it to bring their sensors into one Lattice picture.

{: .warning }
> From press and secondary sources, not Anduril's own docs: live Lattice environments are reportedly partner-gated and subject to US export controls (ITAR/EAR). Confirm the access process, licensing and the exact entity schema directly with Anduril.

**Next step:** a conversation with Anduril about the partner path: what it takes to get SDK and sandbox access, whether a passive acoustic sensor fills a gap they see, and what a pilot looks like.

## Security

- Authenticate nodes (per-device keys) so an adversary can't inject fake drones.
- Encrypt links; assume radios and cell networks are monitored.
- No raw audio leaves nodes — reduces privacy risk and intelligence value if intercepted.
- Keep node radio emissions short and rare so the network stays passive in practice, not just in name.

## Sources

- [OCBJ — Anduril enabling partners to operate on Lattice (Lattice SDK)](https://www.ocbj.com/defense-2/anduril-industries-enabling-partners-to-operate-on-lattice/)
- [The Defense Post — CENTCOM exercise uses Lattice to integrate 10+ sensor teams](https://thedefensepost.com/2024/11/14/us-centcom-exercise-anduril-lattice/amp/)
