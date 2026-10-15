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
| **SAPIENT** | UK MOD open interface standard for counter-UAS sensors and fusion nodes | Adopted in NATO counter-UAS interoperability work; lets a sensor plug into others' C2 systems |
| GeoJSON / REST / WebSocket | Plain web API | For dashboards, partners, testing |

## Suggested data flow

1. **Node → server:** detection report (time, node position, bearing, elevation, class, confidence). Small enough for LoRa.
2. **Server:** association → triangulation → tracking → threat classification.
3. **Server → users:** CoT to TAK, SAPIENT to C2, GeoJSON to a web map; alerts to fire teams with predicted path.

## Security

- Authenticate nodes (per-device keys) so an adversary can't inject fake drones.
- Encrypt links; assume radios and cell networks are monitored.
- No raw audio leaves nodes — reduces privacy risk and intelligence value if intercepted.
