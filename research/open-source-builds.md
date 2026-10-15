---
title: Open-source projects to build on
parent: Research Notes
nav_order: 1.5
---

# Open-source projects to build on
{: .no_toc }

Three public projects already cover parts of what this site proposes. Two are working low-cost detectors on the same chip family we picked; one is academic code for telling drones apart. None of them does bearings, fusion, military map output or forward placement, which is where this project would add something.

1. TOC
{:toc}

## At a glance

| | Batear | VolAnti | AcousticPrint |
|---|---|---|---|
| **What it is** | Single-mic detector node + LoRa gateway | Four-mic detector unit with local alarm | Machine-learning code for drone identification |
| **Hardware** | ESP32-S3 + one MEMS mic (ICS-43434 or INMP441) | ESP32-S3, four digital mics, own 4-layer PCB, printed case | Shotgun mic (RØDE NTG4) for recordings; runs on a PC |
| **Detection** | FFT harmonic ladder | Propeller harmonic pattern | ML classifier that rejects unknown sounds |
| **Range published** | None | **104.2 m** (one test, hovering quad) | n/a |
| **Bearing / position** | No | No (mics are summed for gain) | No |
| **Links** | LoRa star to gateway, or Ethernet/PoE; MQTT, Home Assistant | LoRa alerts between units | None |
| **Licence** | **MIT** | Apache-2.0 firmware, CERN-OHL-W-2.0 hardware, CC BY-SA docs | **None stated** |
| **Activity** | Active (last push 2026-10-06), ~425 stars | Active (last push 2026-09-20), ~416 stars | Dormant since May 2020, 5 stars |
| **Best use for us** | Starting firmware for a tripwire node | Real range data and a 4-mic board to turn into a bearing board | Method ideas and labelled data |

## Batear

**[github.com/batear-io/batear](https://github.com/batear-io/batear)**: an open-source, edge-only acoustic drone detector built on the ESP32-S3. No cloud and no subscription.

**How it detects:** it samples one microphone at 16 kHz, runs a 1024-point FFT (15.6 Hz per bin) and looks for a fundamental between 180 and 2,400 Hz with matching peaks at 2× and 3× that frequency, the harmonic "ladder" that spinning rotors make. A 0–1 confidence score combines signal-to-noise and harmonic ratios with smoothing. An alarm needs 2 positive frames in a row and clears after 8 negative ones. The whole scan takes well under 10 ms per frame.

**How it reports:** each detector sends an AES-128-GCM-encrypted, 36-byte packet over 915 MHz LoRa to one gateway, which forwards it to MQTT and Home Assistant. A wired version uses Ethernet or PoE, with a REST API and over-the-air updates. It can also record the audio around each alarm to an SD card, and reports battery voltage in every packet.

**What we'd take:**

- It is close to a **[tripwire]({{ site.baseurl }}{% link models/tripwire.md %}) node already**: one cheap mic, an ESP32-S3, LoRa, encryption and tiny packets. The MIT licence means we can build on it commercially with almost no conditions.
- The alarm recordings are a ready-made way to **collect labelled field audio**, which is our real bottleneck ([Training data]({{ site.baseurl }}{% link research/datasets.md %})).
- Its harmonic detector is a sensible first stage before a learned classifier.

**What it lacks for our use:** no direction or position; a star network, not a mesh, so no hop-by-hop relay back from a forward line; no GPS; the ESP32-S3 runs the FFT continuously, which is not a weeks-on-a-battery design; output goes to Home Assistant, not TAK or Lattice; and no published range. Field testing in Ukraine is described as planned, not done.

## VolAnti

**[volantitech.com](https://volantitech.com/)** · [github.com/agamrossen/VolAnti](https://github.com/agamrossen/VolAnti): an open-hardware acoustic detector designed and tested by Agam Rossen, an engineering student at the University of York. It is one person's project, not a company.

**The unit:** a 91 mm square, four-layer board with four digital microphones sampled at 16 kHz, in a printed case, with a beeper, light, vibration motor and an e-paper screen that keeps the alert showing with the power off. Units send 18-byte LoRa alerts to each other. The full unit is listed at **£50–80**, a breadboard version at **£35–45**. It looks for the evenly spaced harmonics of propellers, so it works on fibre-optic drones.

**Why it matters to us: it publishes real range numbers.** One unit detected a hovering four-motor airframe at **104.2 m** on a street with traffic, without alarming on the cars. Its expected range by wind:

| Wind | Expected range |
|---|---|
| Still air, under 2 m/s | 100–200 m |
| Light breeze | 50–120 m |
| Breezy | 15–50 m |
| Strong, upwind, over 8 m/s | 5–25 m |

That backs the low end of our [100–300 m working estimate]({{ site.baseurl }}{% link research/range-and-cost.md %}) for small quads and shows how hard wind cuts it. For the tripwire it means node spacing may need to be **closer than 200–300 m** in windy country, or nodes need better windscreens and height.

Nine units were built and sent to an unnamed site in September 2026.

**What we'd take:**

- Its **range-versus-wind table** as a starting point for our own measurements.
- Its **four-mic board**. It sums the mics for about 6 dB of gain; the same four mics could estimate a **bearing** instead, turning it into an M1-style node.
- Its printed enclosure and local alarm ideas for hand-placed rings.

**Cautions:** the author's own disclaimer says it is not a life-safety product, has had no certification, and that the firmware, written in a month, is the least mature part, with false alarms indoors on some music and fan-like noise. The hardware licence (CERN-OHL-W) asks that changes to the board design be shared under the same licence, which matters if we sell a modified board.

## AcousticPrint

**[github.com/AcousticPrint/AcousticPrint](https://github.com/AcousticPrint/AcousticPrint)**: research code from an academic team (Kolamunna, Li, Dahanayake, Seneviratne, Thilakaratne, Zomaya, Seneviratne) that builds acoustic "signatures" for drone classes and flags sounds that match **no known class** as outliers.

**Data:** recordings of five commercial drones (Parrot Bebop 2, DJI Mavic Pro, Phantom 4, Spark, Matrice 100) flown about 20 m up, plus clips of four more from YouTube, and non-drone sounds (road vehicles, bees, speech, quiet background), with amplitude and time-stretch augmentation.

**What we'd take:** the **open-set idea**. In the field most sounds are neither a known drone nor silence, and a classifier that can say "I don't know this sound" is the right shape for keeping false alarms down. The non-drone recordings are also useful negatives.

**Cautions:** no licence is published, which by default means **we may not reuse the code**; reading it for ideas is fine, and we'd need the authors' permission to copy it. The repository has been dormant since 2020, states no accuracy figures, and covers consumer camera drones, not FPVs or Shaheds.

## What this means for the project

- **The single detector node is largely solved in the open.** Two independent projects detect drones on an ESP32-S3 for well under $100. Hardware is not the moat, as the [overview]({{ site.baseurl }}{% link index.md %}) already argues.
- **What nobody has published** is what this site is about: bearings from cheap nodes, fusing many nodes into a track, relaying from forward lines, output to TAK and Lattice, and real combat recordings.
- **Fastest path to a prototype:** start tripwire nodes from Batear's MIT firmware, measure range against VolAnti's published numbers, and add open-set rejection along AcousticPrint's lines on our own data.
- These projects are also **free alternatives** a buyer could find. Anything we sell has to do clearly more than they do.

## Sources

- [Batear — GitHub](https://github.com/batear-io/batear) and its [detection algorithm notes](https://github.com/batear-io/batear/blob/main/docs/how-it-works.md)
- [VolAnti — project site](https://volantitech.com/), [GitHub](https://github.com/agamrossen/VolAnti) and [licence and disclaimer](https://github.com/agamrossen/VolAnti/blob/main/LICENSE.md)
- [AcousticPrint — GitHub](https://github.com/AcousticPrint/AcousticPrint)
