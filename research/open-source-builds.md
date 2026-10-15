---
title: Open-source projects to build on
parent: Research Notes
nav_order: 1.5
---

# Open-source projects to build on
{: .no_toc }

Three public projects already cover parts of what this site proposes. Two are working low-cost detectors on the same chip family we picked; one is academic code for telling drones apart. None of them does bearings, fusion, military map output or forward placement, which is where this project would add something. The last section turns them into a [weekend test kit](#weekend-test-kit-start-training-the-detector) for collecting training audio.

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
| **Best use for us** | Starting firmware for a tripwire node | Real range data and a tested low-cost unit design | Method ideas and labelled data |

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
- Its **four-mic board** as a sensitivity trick: summing four mics gives about 6 dB for free. It is **not** a bearing board. The author tried beamforming and found that at 79 mm across it buys nothing, because the array is a tenth of a wavelength at rotor frequencies. Bearings need mics spread much wider, as in [M1]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}).
- Its printed enclosure and local alarm ideas for hand-placed rings.

**Cautions:** the author's own disclaimer says it is not a life-safety product, has had no certification, and that the firmware, written in a month, is the least mature part, with false alarms indoors on some music and fan-like noise. The hardware licence (CERN-OHL-W) asks that changes to the board design be shared under the same licence, which matters if we sell a modified board. The author also says VolAnti was never made for or with any military and will never include countermeasures; the licences still allow reuse, but any military use of a derived design should credit it and keep its name off.

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

## Weekend test kit: start training the detector

The aim of a first weekend is not a finished node. It is **labelled recordings** of a drone at known distances, plus plenty of recordings of everything that isn't a drone, a first classifier trained on them, and a free baseline detector (Batear) to beat. Training data is the real bottleneck ([Training data]({{ site.baseurl }}{% link research/datasets.md %})), so the first test should start producing it.

{: .warning }
> Prices are rough US figures checked in October 2026 and change often. Check the listing before buying. Where a part has to ship from China, it won't arrive by this weekend; those parts are marked.

### What training needs, and what each part is for

| Training needs… | Because… | Covered by |
|---|---|---|
| **A drone to record** | No recordings, no model. Distance has to be known to label each clip | The drone, with its app's distance readout |
| **Recordings of everything else** | Most false alarms come from cars, mowers, wind, birds and generators. A model only learns to ignore what it has heard | The same recorders, left running when no drone is up |
| **A microphone at node height, out of the wind** | A mic in the grass hears much less, and wind noise is the biggest range-killer in VolAnti's tests | Tripod or light stand, fur windscreen |
| **A baseline detector to beat** | If a trained model doesn't beat a simple harmonic detector, it isn't worth the power it costs | Batear on two LoRa boards, plus mics |
| **Audio through the same cheap mic the nodes will use** | Phones filter and compress audio differently. A model trained only on phone audio may do worse on a MEMS mic | Step 2: a Batear recorder board (ships from China) |
| **Field power** | Nothing out there has a wall socket | Power banks |

### The parts

<div class="kit-grid">

<figure class="kit-card">
<img src="{{ site.baseurl }}/assets/images/kit/lora-board.jpg" alt="An ESP32 LoRa development board with a small screen and antenna" loading="lazy">
<figcaption>
<p class="kit-name">LoRa board, ×2</p>
<p class="kit-price">~$25–30 each</p>
<p>Heltec WiFi LoRa 32 V3 (US 915 MHz). One runs Batear's detector, one its gateway. Batear has a web flasher, so no toolchain. Doubles as a first LoRa range test.</p>
<p class="kit-credit">Similar LILYGO T-Beam shown. Photo: Chiffre01, CC0</p>
</figcaption>
</figure>

<figure class="kit-card">
<img src="{{ site.baseurl }}/assets/images/kit/mics-breadboard.jpg" alt="Four I2S microphone breakouts wired to an ESP32-S3 board on a breadboard" loading="lazy">
<figcaption>
<p class="kit-name">I2S MEMS mics + breadboard</p>
<p class="kit-price">~$11 for 3 mics, ~$10 for breadboard and jumpers</p>
<p>INMP441 breakouts: cheap and on Amazon. The ICS-43434 that Batear prefers is discontinued. Five wires per mic. Headers need soldering.</p>
<p class="kit-credit">VolAnti breadboard build. Photo: Agam Rossen, CC BY-SA 4.0</p>
</figcaption>
</figure>

<figure class="kit-card">
<img src="{{ site.baseurl }}/assets/images/kit/windscreen.jpg" alt="A furry microphone windscreen" loading="lazy">
<figcaption>
<p class="kit-name">Fur windscreens</p>
<p class="kit-price">~$10 for a pack</p>
<p>Small clip-on "dead cat" fur covers, sized for lapel mics and phones. Cheapest range gain there is in wind.</p>
<p class="kit-credit">Larger shotgun-mic version shown. Photo: Nicolai Equipment, CC BY-SA 3.0</p>
</figcaption>
</figure>

<figure class="kit-card">
<img src="{{ site.baseurl }}/assets/images/kit/tripod.jpg" alt="A tripod" loading="lazy">
<figcaption>
<p class="kit-name">Tripod or light stand, ×2</p>
<p class="kit-price">~$20–30 each, or use what you have</p>
<p>Holds a node and a phone 1–2 m up, matching the tripwire's spring mast.</p>
<p class="kit-credit">Photo: David Adam Kess, CC BY-SA 4.0</p>
</figcaption>
</figure>

<figure class="kit-card">
<img src="{{ site.baseurl }}/assets/images/kit/power-bank.jpg" alt="A USB power bank" loading="lazy">
<figcaption>
<p class="kit-name">USB power banks, ×2</p>
<p class="kit-price">~$15 each, or use what you have</p>
<p>Runs each board all day in the field. Small 1S LiPo packs also plug straight into the Heltec.</p>
<p class="kit-credit">Photo: Ronggy, public domain</p>
</figcaption>
</figure>

<figure class="kit-card">
<img src="{{ site.baseurl }}/assets/images/kit/camera-drone.jpg" alt="A small folding camera drone" loading="lazy">
<figcaption>
<p class="kit-name">Drone to record</p>
<p class="kit-price">$0 if borrowed; ~$210–300 new</p>
<p>A sub-250 g camera drone such as a DJI Mini 4K is the easy buy: GPS hover and a live distance readout make labelling simple. It is quieter than an attack FPV, so its ranges are conservative.</p>
<p class="kit-credit">DJI Mini 2 shown. Photo: Florian Fuchs, CC BY-SA 4.0</p>
</figcaption>
</figure>

<figure class="kit-card">
<img src="{{ site.baseurl }}/assets/images/kit/fpv-drone.jpg" alt="A 5-inch-class racing quadcopter" loading="lazy">
<figcaption>
<p class="kit-name">A real FPV, if you can get one</p>
<p class="kit-price">$0 at a local FPV club</p>
<p>A 5–7 inch FPV is the actual target and sounds different from a camera drone. Ask a local club pilot to fly passes past your mics. Best recordings per dollar.</p>
<p class="kit-credit">Photo: Commanderbryce, CC BY-SA 4.0</p>
</figcaption>
</figure>

<figure class="kit-card">
<img src="{{ site.baseurl }}/assets/images/kit/esp32-s3.jpg" alt="An ESP32-S3 development board" loading="lazy">
<figcaption>
<p class="kit-name">Step 2: recorder board</p>
<p class="kit-price">~$15–25, ships from China</p>
<p>LILYGO T-ETH-Lite S3. Batear's wired build saves 16 kHz WAV to microSD at the press of a button, through the same MEMS mic. Not on Amazon, and may need a USB-serial adapter to flash.</p>
<p class="kit-credit">Generic ESP32-S3 board shown. Photo: VectorVoyager, CC BY-SA 4.0</p>
</figcaption>
</figure>

<figure class="kit-card">
<img src="{{ site.baseurl }}/assets/images/kit/microsd.jpg" alt="A microSD card next to an SD card and a dime" loading="lazy">
<figcaption>
<p class="kit-name">microSD card, 32 GB</p>
<p class="kit-price">~$8</p>
<p>For the step 2 recorder. Must be FAT32 and 32 GB or smaller. 16 kHz audio is about 115 MB an hour.</p>
<p class="kit-credit">Photo: Nashucks, CC0</p>
</figcaption>
</figure>

</div>

**Free:** the phones you already have (one per recording spot), a laptop, Audacity for cutting and labelling clips, and Python (librosa plus scikit-learn or PyTorch) or Edge Impulse's free tier, which can export a model to run on an ESP32-S3.

### The recommendation

| Kit | What you buy | Cost |
|---|---|---|
| **Cheapest MVP (you have tripods, power banks and a drone to borrow)** | 2 Heltec V3, 3 INMP441 mics, breadboard and jumpers, windscreens | **~$80–90** |
| **Full MVP (buy everything, including a drone)** | The above, plus 2 stands, 2 power banks and a DJI Mini 4K | **~$360–480** |
| Step 2, ordered now for later | T-ETH-Lite S3 and a microSD card | ~$25–35 |

Buy the Heltec boards, mics and windscreens from Amazon on Thursday so they arrive by the weekend. Order the T-ETH-Lite at the same time; it will take a week or two.

**Record with phones this weekend.** It is the honest shortcut. Use a recorder app that saves uncompressed WAV and lets you turn off noise reduction, and put a fur windscreen on each phone. When the T-ETH-Lite arrives, repeat a short session through the MEMS mic and check whether the model still works on it.

### A weekend plan

**Friday evening, about 2 hours**

1. Solder headers onto the Heltec boards. Wire one INMP441 to the detector board: VDD to 3.3V, GND to GND, SCK to GPIO4, WS to GPIO5, SD to GPIO6, L/R to GND ([Batear hardware](https://github.com/batear-io/batear/blob/main/docs/hardware.md)).
2. Flash one board as detector and one as gateway with Batear's [web flasher](https://docs.batear.io/flasher/) in Chrome or Edge.
3. Play a drone clip from a phone half a metre away and watch the alarm reach the gateway.
4. Download a public dataset from the [Training data]({{ site.baseurl }}{% link research/datasets.md %}) page and train a first drone / no-drone model, so the pipeline works before Saturday's data arrives.

**Saturday, in the field, 3–4 hours**

1. Find open ground where flying is legal. Put the Batear detector and a phone on stands at 1–2 m, side by side, both in windscreens. Take off right next to them, so the app's distance from home is the distance from the mic.
2. Hover for 60 seconds each at **25, 50, 100, 150 and 200 m**, at two altitudes, then fly straight passes. At each step, write down whether Batear alarmed, plus wind speed (a weather app is fine). This is your first range-versus-wind data point to set beside [VolAnti's]({{ site.baseurl }}{% link research/open-source-builds.md %}#volanti).
3. Record **at least 30 minutes with no drone up:** traffic, a mower, wind, birds, people talking, a generator, any aircraft. Negatives are as valuable as drone clips.
4. Walk the gateway away from the detector until alerts stop. That is a first taste of the tripwire's deciding question, [T9]({{ site.baseurl }}{% link research/open-questions.md %}).

**Sunday, at the laptop**

1. Cut recordings into 1-second clips and label them by distance from the flight notes.
2. Split train and test **by session or flight, not by clip.** Clips cut from the same minute of audio nearly match, and mixing them across the split makes any model look far better than it is.
3. Train a small model and measure it on the held-out flight and the held-out negatives: detection rate at each distance, and false alarms per hour of negatives.
4. Compare it with Batear's alarms from Saturday at the same distances.

**What counts as success:** a classifier that beats Batear's harmonic detector at 100 m or more with fewer false alarms per hour; a first range figure at a known wind speed; and a first LoRa range figure in your terrain.

{: .note }
> **Fly legally.** In the US, recreational pilots must pass the free online TRUST test and fly in permitted airspace (check B4UFLY or a similar app), under 400 ft and within sight. Drones under 250 g flown for fun don't need registering; heavier ones do. Recording drone sound in a field needs no permit, but keep cameras off neighbours' property.

## Sources

- [Batear — GitHub](https://github.com/batear-io/batear) and its [detection algorithm notes](https://github.com/batear-io/batear/blob/main/docs/how-it-works.md)
- [VolAnti — project site](https://volantitech.com/), [GitHub](https://github.com/agamrossen/VolAnti) and [licence and disclaimer](https://github.com/agamrossen/VolAnti/blob/main/LICENSE.md)
- [AcousticPrint — GitHub](https://github.com/AcousticPrint/AcousticPrint)
- Test kit: [Batear hardware and wiring](https://github.com/batear-io/batear/blob/main/docs/hardware.md), [Batear TF-card recording](https://github.com/batear-io/batear/blob/main/docs/configuration.md), [VolAnti breadboard build](https://github.com/agamrossen/VolAnti/blob/main/docs/breadboard-build.md), [Adafruit ICS-43434 (discontinued notice)](https://www.adafruit.com/product/6049), [Rokland — Heltec V3 US915](https://store.rokland.com/products/heltec-wifi-lora-32v3), [CNX Software — T-ETH-Lite S3](https://www.cnx-software.com/2023/09/27/lilygo-t-eth-lite-esp32-s3-board-ethernet-poe/), [The Drive — DJI Mini 4K pricing](https://www.thedrive.com/news/dji-drones-amazon-spring-sale-2026), [FAA — recreational flyers](https://www.faa.gov/uas/recreational_flyers)
- Kit photos, cropped and resized, from Wikimedia Commons: [LILYGO T-Beam](https://commons.wikimedia.org/wiki/File:Meshtastic_T-Beam.jpg) (Chiffre01, CC0), [windshield](https://commons.wikimedia.org/wiki/File:Nicolai_Equipment_Windshield_for_Shotgun_Microphone.jpg) (Nicolai Equipment, [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)), [tripod](https://commons.wikimedia.org/wiki/File:(Photography_equipment_Tripod_Photo_Camera_Tripod_photograph_in_a_studio).jpg) (David Adam Kess, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)), [power bank](https://commons.wikimedia.org/wiki/File:USB_power_bank.jpg) (Ronggy, public domain), [DJI Mini 2](https://commons.wikimedia.org/wiki/File:DJI_Mini_2.jpg) (Florian Fuchs, CC BY-SA 4.0), [racing quad](https://commons.wikimedia.org/wiki/File:Racing_Drone.jpg) (Commanderbryce, CC BY-SA 4.0), [ESP32-S3](https://commons.wikimedia.org/wiki/File:ESP32-S3_on_paper.jpg) (VectorVoyager, CC BY-SA 4.0), [microSD](https://commons.wikimedia.org/wiki/File:Size_comparison_of_SD_card,_microSD_card,_and_dime.jpg) (Nashucks, CC0). Breadboard photo from [VolAnti](https://github.com/agamrossen/VolAnti) (Agam Rossen, CC BY-SA 4.0).
