---
title: MVP path
nav_order: 1.5
---

# The MVP path: $80 radio test to a working line
{: .no_toc }

The [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}) built in five cheap layers. Each answers one question, and its gate decides whether to buy the next. **MVP = layer 5:** six hand-placed listeners hear a real drone and alert a screen in a tree line, while the receiving end transmits nothing.

{: .warning }
> **A plan, not a result: no layer has been run yet.** Gates marked *proposed* are ours; T9's are the site's. Links were loaded 2026-10-15. Items that wouldn't load are search terms.

| Layer | Question | Spend | Total | Gate |
|---|---|---|---|---|
| [0](#layer-0) T18 | Would a minute's warning change what troops do? | $0 | $0 | Most say yes, else stop |
| [1](#layer-1-the-radio-test-t9) T9 | Can a board at 0.5–1 m report back over 2–3 km, through trees? | ~$65–80 | ~$80 | T9's marks, or margins that predict them |
| [2](#layer-2-hear-a-drone-from-near-the-ground-t11) T11 | How far does a mic at 0.5–1 m hear a drone? | ~$50 | ~$130 | ≥100 m (sets spacing, so cost per km) |
| [3](#layer-3-the-edge-receiver-t17) T17 | Can the edge receiver hear the line without transmitting? | ~$90–130 | ~$250 | Layer 1's delivery, SDR sees nothing |
| [4](#layer-4-battery-and-cold-t12) T12 | Does a listener last weeks, and in the cold? | ~$35–135 | ~$300–400 | ≥3 weeks, cold loss measured |
| [5](#layer-5-the-mvp-a-six-listener-line) MVP | Does the whole chain work? | ~$250–350 | ~$600–750 | 18/20 crossings in 10 s, <1 false alarm/day, silent |

Assumed owned: laptop, phone, USB power banks, soldering iron.

## Layer 0: ask first (T18, $0) {#layer-0}

Run alongside everything. 5–10 interviews with recent front-line users ([questions]({{ site.baseurl }}{% link research/problem-check.md %}#the-next-step-ask-before-building-t18)). The [lives estimate]({{ site.baseurl }}{% link research/lives-model.md %}) depends on whether troops act on warning. No hardware test answers that.

<details class="layer" id="layer-1-the-radio-test-t9" markdown="block">
<summary><span class="layer-title">Layer 1: radio test (T9), ~$80</span><span class="layer-sub">Board at 0.5–1 m to a raised receiver, 2–3 km, across open ground, forest and hedgerows</span></summary>

**Why first:** it is the [deciding question]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-home), it needs no drone, and every later layer reuses the boards.

| Item | Buy | Alternatives |
|---|---|---|
| **2 × LoRa board**, 915 MHz | Heltec WiFi LoRa 32 V3, [Rokland, $29.97](https://store.rokland.com/products/heltec-wifi-lora-32v3) | [Heltec direct, $17.90–19.90](https://heltec.org/project/wifi-lora-32-v3/) + China shipping; [RAK WisBlock kit, $34.97](https://store.rokland.com/products/rak-wireless-wisblock-meshtastic-starter-kit); [LILYGO T3S3, $72.99](https://www.tindie.com/products/yihang/915mhz-meshtastic-kit-t3s3-s3-sx1262/) |
| **u.FL→SMA cable** (V3 has no SMA) | [Adafruit 851, $3.95](https://www.adafruit.com/product/851) | Any u.FL to SMA-female pigtail |
| **10 dB attenuator** (margin method) | [Inmet AHC-10, RF Parts, $15.91](https://www.rfparts.com/ahc-10.html) | [L-com 20 dB, $92.09](https://www.l-com.com/coaxial-2w-20db-rf-fixed-attenuator-sma-male-to-sma-female-passivated-stainless-steel-body-up-to-6-ghz) |
| **Mast**, 6–10 m | **Free:** upstairs window, roof edge, tree | [Spiderbeam 12 m HD, $109.99](https://moonrakeronline.com/us/spiderpole-12hd-telescopic-pole-12m-heavy-duty-fibreglass); 7 m ~$55, same store |
| **Antenna** (run D) | [8 dBi omni, Newegg Business, $16.99](https://www.neweggbusiness.com/p/9B-2VT-04FG-00029) | [Rokland 5.8 dBi kit, $49.97](https://store.rokland.com/products/meshtastic-compatible-6-dbi-n-female-omni-outdoor-915-mhz-antenna-kit-with-6-10-or-15-cable-choice) |

**Minimum:** 2 boards + cable, $64. With the attenuator, $80.

**Firmware**
- **Quick walk:** Meshtastic [Range Test](https://meshtastic.org/docs/configuration/module/range-test/), region US. Logs `rangetest.csv` with GPS. It sends one packet every 15–60 s, so it finds where the link dies but can't count delivery.
- **Counted points:** a [RadioLib](https://github.com/jgromes/RadioLib) ping sketch sending one packet every 1–2 s, 100 per point. It sets output power directly, which the margin method needs.

**Margin method:** lets a woodlot stand in for 2 km of forest.
1. At each point, step power down 22 → 17 → 12 → 7 → 2 dBm, then add the attenuator, until delivery drops below 80%. The power you cut is the margin. Each spreading-factor step (SF12 → SF7) adds about 2.5 dB.
2. Repeat 150, 300 and 600 m into forest. Margin lost per 100 m predicts where the link dies.
3. This is an extrapolation ([Weissberger](https://en.wikipedia.org/wiki/Weissberger%27s_model)), so one real 2 km forest point is still needed.

| Run | Place | Node | Receiver |
|---|---|---|---|
| A | Field or farm road | 0.5 m and 1 m | 6–10 m and 2 m |
| B | Woodlot, node inside | 1 m | Edge, raised |
| C | Same woods, node to node | 1 m, 100–300 m apart | — |
| E | Hedgerows (US stand-in for [windbreak belts]({{ site.baseurl }}{% link models/tripwire.md %}#a-windbreak-belt-is-not-a-forest)) | Across 1, 2, 3 belts | Raised, last belt |

Run with leaves on now and leaves off in December.

**Gate:** [T9's marks]({{ site.baseurl }}{% link research/open-questions.md %}#the-test-t9), e.g. 90% at 3 km open from a 1 m node, or 80% node to node at 200 m in forest. If open ground passes but forest fails, carry on with denser lines under trees or another way home.
**Not testable at home:** jamming (T19), which is illegal in the US. 915 MHz at legal power is licence-free.

</details>

<details class="layer" id="layer-2-hear-a-drone-from-near-the-ground-t11" markdown="block">
<summary><span class="layer-title">Layer 2: hear a drone from the ground (T11), ~$50</span><span class="layer-sub">Mic range at 0.5–1 m sets spacing, and so the cost of a line</span></summary>

**Why:** the site assumes listeners every 200–300 m against FPVs, but the [only measured range]({{ site.baseurl }}{% link models/tripwire.md %}#warning-time-comes-from-distance) for cheap mics is 50–60 m. Kit: the [weekend kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector) with the mic lowered, running Batear on layer 1's boards.

| Item | Buy | Alternatives |
|---|---|---|
| **3 × I2S mic** | [Adafruit SPH0645, $6.95](https://www.adafruit.com/product/3421) (Adafruit's replacement for the ICS-43434) | INMP441 (Batear's wiring): [Vetco, $4.95](https://vetco.net/products/omnidirectional-microphone-module-inmp441-high-precision-i2s); [Amazon 5-pack, ~$13](https://www.amazon.com/dp/B09G4RNT3G) |
| **Fur windscreens** | [Movo WS10n 5-pack, $14.95](https://www.movophoto.com/products/ws10n-universal-furry-outdoor-microphone-windscreen-lavalier) | [Movo WS-RD 2-pack, $9.95](https://www.movophoto.com/products/ws-rd-furry-lav-mic-windscreen-2x) |
| **Breadboard + jumpers** | [Adafruit 3314, $9.95](https://www.adafruit.com/products/3314) | [SparkFun 140 pcs, $8.95](https://www.sparkfun.com/jumper-wire-kit-140pcs.html) |
| **Recorder** | [XIAO ESP32S3 Sense, $13.99](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html) | Phone in a windscreen (free); [SparkFun Thing Plus S3, $24.95](https://www.sparkfun.com/sparkfun-thing-plus-esp32-s3.html) |
| **Stake** | Search "fiberglass driveway marker" 48 in, ~$3–5 | Garden stake |
| **Drone** | **Borrow a 5–7 in FPV:** [AMA clubs](https://www.modelaircraft.org/club-finder), [MultiGP](https://www.multigp.com/chapters/) | [Potensic ATOM SE, $249.99](https://store.potensic.com/products/atom-se); DJI Mini 4K ~$299 (search); [DJI Neo, $169](https://store.dji.com/product/dji-neo), out of stock |
| **Wind** | Phone weather app | Handheld anemometer, ~$15–35 (search) |

**Run** ([weekend plan]({{ site.baseurl }}{% link research/open-source-builds.md %}#a-weekend-plan), mic at 0.5 and 1 m)
- Hover 60 s at 25, 50, 100, 150, 200 and 300 m, at two altitudes. Then fly straight passes.
- Log wind on every run.
- Record 30+ min with no drone: traffic, mowers, birds.
- Repeat along a [tree line]({{ site.baseurl }}{% link research/field-conditions.md %}#where-infantry-actually-sit-tree-lines).
- Fly under FAA TRUST or Part 107.

**Gate (proposed):**
- **Pass:** 9 of 10 passes heard at ≥100 m with a consumer drone, or ≥150 m with an FPV, in light wind. 200 m spacing holds.
- **Fail, under 60 m:** a line needs 3–4× the listeners per km. Redo the [cost]({{ site.baseurl }}{% link models/tripwire.md %}#what-it-costs-estimates) first.

</details>

<details class="layer" id="layer-3-the-edge-receiver-t17" markdown="block">
<summary><span class="layer-title">Layer 3: silent edge receiver (T17), ~$90–130</span><span class="layer-sub">Receive-only board at the tree-line edge, wired to the dugout, proven silent with an SDR</span></summary>

**Why:** a unit that transmits gets found. This proves it can [hear the line silently]({{ site.baseurl }}{% link models/tripwire.md %}#the-design-a-listen-only-receiver-at-the-tree-line-edge-wired-home).

| Item | Buy | Alternatives |
|---|---|---|
| **3rd LoRa board** | Heltec V3, [Rokland, $29.97](https://store.rokland.com/products/heltec-wifi-lora-32v3) | As layer 1 |
| **RS-485, edge** | [SparkFun breakout (3.3 V), $12.50](https://www.sparkfun.com/sparkfun-transceiver-breakout-rs-485.html) | MAX3485 module (not the 5 V MAX485) |
| **USB→RS-485, laptop** | [Waveshare (B), ~$7.99](https://www.waveshare.com/product/iot-communication/wired-comm-converter/usb-to-rs485-b.htm) | Any FTDI/CH340 adapter |
| **Wire** | Old Ethernet cable (one pair) | 300 m run: [burial Cat5e 1000 ft, $243](https://www.cctvcameraworld.com/products/direct-burial-cat5e-cable-1000ft.html) |
| **Directional antenna** | **DIY** wire Yagi on a wooden boom, a few dollars | [Pasternack 9 dBi, $254.99](https://www.pasternack.com/single-antenna-880-960-mhz-9-dbi-gain-n-pe51ya1018-p.aspx) (N, needs N→SMA); layer 1's omni |
| **Into the canopy** | Tennis ball + paracord | [WesSpur throw line kit](https://wesspur.com/arborist-throw-line-kit), ~$50+ |
| **SDR** | [Nooelec NESDR SMArt v5, $54.95](https://www.nooelec.com/store/sdr/sdr-receivers/nesdr-smart.html) | [RTL-SDR Blog V3, ~$35–40](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/) (V4 discontinued) |

**Run**
1. Raise the receive-only board 5–10 m at a woodlot edge and cable it in to a laptop.
2. Send from layer 1's passing points and log delivery.
3. Watch 902–928 MHz on the SDR for 1 h, at the edge and at the laptop.
4. Once the short run works, prove 300 m of cable. RS-485 is rated to ~1,200 m at low data rates.

**Gate (proposed):** delivery matches layer 1, the SDR sees **no transmission**, and alerts reach the laptop within 2 s. If the board emits anything in receive mode, fix the firmware first.

</details>

<details class="layer" id="layer-4-battery-and-cold-t12" markdown="block">
<summary><span class="layer-title">Layer 4: battery and cold (T12), ~$35–135</span><span class="layer-sub">Weeks on one cell? The kitchen freezer is the cold chamber</span></summary>

**Why:** listeners are disposable, so battery life sets the [running cost]({{ site.baseurl }}{% link models/tripwire.md %}#the-running-cost-lines-are-ammunition). It needs the classifier trained on layer 2's audio.

| Item | Buy | Alternatives |
|---|---|---|
| **Current meter** | [Nordic PPK2, Adafruit, $99.95](https://www.adafruit.com/product/5048) (reads µA sleep current) | USB meter, e.g. FNIRSI FNB58, ~$40–50 (search). Average current only |
| **Cells** | [Molicel P28A, $5.99](https://www.18650batterystore.com/products/molicel-p28a) | [Samsung 30Q, $6.99](https://www.18650batterystore.com/products/samsung-30q); [Battery Junction P28A, ~$6.70](https://batteryjunction.com/molicel-inr18650-p28a) |
| **Holder** | [SparkFun 1×18650, $1.25](https://www.sparkfun.com/battery-holder-1x18650-wire-leads.html) (backordered) | Any 18650 holder with leads |
| **Plug** | Solder the V3's included SH1.25 lead to the holder | LiPo with "Micro JST 1.25" ([Rokland V3 page](https://store.rokland.com/products/heltec-wifi-lora-32v3)). Adafruit LiPos (JST-PH) don't fit |
| **Freezer logger** | [Inkbird IBS-TH2 Plus, $24.99](https://inkbird.com/products/ibs-th2-plus) (only the probe goes in; the body is rated to −10 °C) | [GoveeLife R1, $39.99](https://us.govee.com/products/goveelife-smart-thermometer-r1) |

**Run**
1. Measure the current asleep, listening and sending, then work out days per cell.
2. Run one listener on a cell at room temperature until it dies, with a speaker playing a drone clip on a timer.
3. Repeat in the freezer (−18 °C), with the board reporting its voltage and temperature as in the [cold fix]({{ site.baseurl }}{% link models/tripwire.md %}#solving-the-field-limits-at-no-extra-cost).

**Gate (proposed):** at least **3 weeks** at room temperature, with the cold loss measured. If it fails, recompute the running cost; a one-week listener may still pay.

</details>

<details class="layer" id="layer-5-the-mvp-a-six-listener-line" markdown="block">
<summary><span class="layer-title">Layer 5: the MVP, six listeners, ~$250–350</span><span class="layer-sub">Hand-placed line 1–2 km out, the silent edge receiver, real drone crossings</span></summary>

**Proves:** drone crosses → listener hears → alert hops home → edge hears → screen in the trees shows it, in time.

| Per listener | Source | Cost |
|---|---|---|
| Heltec V3 | [Rokland](https://store.rokland.com/products/heltec-wifi-lora-32v3) or [Heltec](https://heltec.org/project/wifi-lora-32-v3/) | $18–30 |
| Mic + windscreen | Layer 2 | $7–10 |
| Cell + holder | Layer 4 | $7–8 |
| Box | [IP65 ABS 100×68×50 mm, Newegg Business, $10.99](https://www.neweggbusiness.com/p/9B-072-001K-007A7) | $11 |
| Stake | Driveway marker | $3–5 |
| **Total** | | **$45–65** |

Six listeners cost $270–390. Add four if layer 1's forest hops need tighter spacing.

**Run**
1. [Place by hand]({{ site.baseurl }}{% link models/tripwire.md %}#why-not-have-people-place-the-listeners) across a hedgerow gap, at layer 2's spacing, 1–2 km from the edge.
2. Fly 20 crossings, varying height, time of day and wind, and GPS-log each one.
3. Leave the line running a week (T5) to count false alarms.

**Measure:**
- detections;
- time from crossing to screen;
- delivery per link;
- false alarms per day;
- battery left at the end.

**Gate (proposed):**
- **18 of 20** crossings on screen, each within **10 s**.
- **Under 1** false alarm per line per day.
- **No transmission** from the receiving end, checked on the SDR.

A pass shows the idea works at small scale on US ground. It does not show it against jamming, Ukrainian terrain, mass raids or air-dropped placement.

</details>

## After the MVP

| Test | Adds | Why later |
|---|---|---|
| T7 | 20+ listeners, losses in a mass raid | ~$1,000; only matters once a line works |
| T10, T13, T14 | Drone-laid listeners, with and without GPS | Hand placement proves the rest first |
| T15 | Friend or foe | Needs recordings of friendly drones |
| T19 | Jamming | Illegal in the US; needs a licensed range or Ukraine |
| T6 | Shahed-class engines | Needs a partner |

All tests: [open questions]({{ site.baseurl }}{% link research/open-questions.md %}).
