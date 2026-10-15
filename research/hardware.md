---
title: Hardware notes and cost levers
parent: Research Notes
nav_order: 4
---

# Hardware notes and cost levers
{: .no_toc }

1. TOC
{:toc}

## Reference node (M1)

| Function | Options | Est. cost | Notes |
|---|---|---|---|
| Processor | ESP32-S3 (vector instructions, Wi-Fi/BLE), RP2350, STM32H7 | $4–10 | ESP32-S3 can run small audio classifiers; heavier beamforming may want an H7 or a Pi Zero 2 W-class board |
| Microphones | INMP441, ICS-43434 (I²S digital MEMS) | $1–3 each | Digital I²S avoids analog noise; matched sensitivity across mics helps |
| GPS | u-blox M8/M10-class with PPS | $8–15 | Position + sub-microsecond time |
| Heading | Magnetometer + accelerometer (e.g. LIS3MDL + LSM6) | $2–6 | Calibrate at install |
| Comms | LoRa SX1262 (Meshtastic-style mesh) **or** LTE Cat-M/NB-IoT | $6–25 | LoRa: no carrier needed, low data rate. Cellular: simpler, depends on network |
| Power | 5–10 W solar + LiFePO₄ 6–12 Ah | $20–40 | Size for winter days at your latitude |
| Enclosure | IP65 box + acoustic membrane + foam/fur windscreen | $8–20 | Windscreen quality strongly affects range |

## Ways to cut cost

1. **Report bearings, not audio.** On-device classification keeps radios and backhaul cheap.
2. **Use mass-market parts** (ESP32, MEMS mics, LoRa modules) — no defence-specific components.
3. **Mount on existing structures** to avoid mast costs and gain range.
4. **Design for one-person, 10-minute installation**, with self-calibration where possible — labour and maintenance dominate fielded cost.
5. **Duty-cycle smartly:** low-power wake on sound energy, full classification only when something is heard.
6. **Open hardware and software** lets allies and volunteers build nodes locally.
7. **Mix densities:** sparse nodes for Shahed-class coverage, dense clusters only around high-value points.

## Phone as an interim node (M2 bridge)

A used Android phone + USB multi-channel mic (e.g. a small USB array) can test the array approach before a custom board exists.
