---
title: MVP path
nav_order: 1.5
---

# The MVP path: from an $80 radio test to a working line
{: .no_toc }

This page lays out how to build the [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}) in cheap layers, from parts you can order today. Each layer answers one question, and its result decides whether the next layer is worth buying. The **MVP** is layer 5: a short line of hand-placed listeners that hears a real drone crossing and gets an alert to a screen inside a tree line, without the receiving end transmitting. Reviewed 2026-10-15.

{: .warning }
> **A plan, not a result.** No layer has been run yet.
> - Pass marks marked *proposed* are ours. Where the site already sets one ([T9]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back)), it is used unchanged.
> - Every purchase link below was loaded in a browser on 2026-10-15 and showed the product and a price. Prices and stock change; items we could not load are named as search terms, not links.

1. TOC
{:toc}

## The layers at a glance

| Layer | Question | Test | New spend | Running total | Gate before the next layer |
|---|---|---|---|---|---|
| **0** (alongside all of them) | Would a minute's warning change what troops do? | [T18]({{ site.baseurl }}{% link research/problem-check.md %}#the-next-step-ask-before-building-t18) interviews | $0 | $0 | If most say no, stop building |
| **1** | Can a listener near the ground report back over km, in the open and through trees? | [T9]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back) | ~$65–80 | ~$80 | T9's pass marks, or a margin that predicts them |
| **2** | How far does a mic at 0.5–1 m hear a drone? | T11 + the [weekend kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector) | ~$40–60 (drone borrowed) | ~$130 | Range sets listener spacing and so the cost per km |
| **3** | Can the unit hear its line from inside a tree line, without transmitting? | T17 + an SDR check (T8) | ~$90–130 | ~$250 | Edge receiver gets layer 1's links and emits nothing |
| **4** | Does a listener last weeks on a small battery, and in the cold? | T12 | ~$35–135 | ~$300–400 | Weeks at room temperature, a measured cold penalty |
| **5: MVP** | Does the whole chain work end to end? | Six-listener line, drone crossings, a week left running (T5) | ~$250–350 | ~$600–750 | Below |
| After the MVP | Mass raids, drone laying, friend or foe, jamming | T7, T13, T14, T15, T19 | — | — | Not needed to prove the idea |

Things you probably already own cover the rest: a laptop, phones, USB power banks, a tripod, a soldering iron.

## Layer 0: ask first (T18, $0)

Run alongside everything below. Five to ten interviews with people who have recent front-line experience ([questions]({{ site.baseurl }}{% link research/problem-check.md %}#the-next-step-ask-before-building-t18)). The [lives estimate]({{ site.baseurl }}{% link research/lives-model.md %}) rests on whether troops act on warning, and no hardware test can answer that.

<details class="layer" id="layer-1-the-radio-test-t9" markdown="block">
<summary><span class="layer-title">Layer 1: the radio test (T9), about $80</span><span class="layer-sub">Can a board at 0.5–1 m get a few bytes back over 2–3 km, in the open, through trees and across hedgerows?</span></summary>

**Why first:** it is the [deciding question]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-home), it needs no drone, and the boards carry on into every later layer.

### Buy

| Item | Buy | Alternatives |
|---|---|---|
| **2 × LoRa board**, 915 MHz | Heltec WiFi LoRa 32 V3, [Rokland, $29.97](https://store.rokland.com/products/heltec-wifi-lora-32v3) | [Heltec's own store, $17.90–19.90](https://heltec.org/project/wifi-lora-32-v3/) plus shipping from China; [RAK WisBlock Meshtastic starter kit, Rokland, $34.97](https://store.rokland.com/products/rak-wireless-wisblock-meshtastic-starter-kit) (different chip, same radio); [LILYGO T3S3 kit, Tindie, $72.99](https://www.tindie.com/products/yihang/915mhz-meshtastic-kit-t3s3-s3-sx1262/) |
| **Adapter cable** (the V3's antenna socket is a tiny IPEX/u.FL, not SMA) | [Adafruit 851, $3.95](https://www.adafruit.com/product/851) | Any "u.FL to SMA female pigtail" |
| **10 dB attenuator** (optional, for the margin method) | [Inmet AHC-10 at RF Parts, $15.91](https://www.rfparts.com/ahc-10.html) | [L-com 20 dB, $92.09](https://www.l-com.com/coaxial-2w-20db-rf-fixed-attenuator-sma-male-to-sma-female-passivated-stainless-steel-body-up-to-6-ghz) (only if 10 dB isn't enough) |
| **Mast**, 6–10 m | **Free:** a second-floor window, a roof edge, or a tree branch | [Spiderbeam 12 m HD fibreglass pole, Moon Raker, $109.99](https://moonrakeronline.com/us/spiderpole-12hd-telescopic-pole-12m-heavy-duty-fibreglass); a 7 m Spiderbeam is listed on the same store at about $55 |
| **Better antenna** (run D only) | [915 MHz 8 dBi omni with u.FL cable, Newegg Business, $16.99](https://www.neweggbusiness.com/p/9B-2VT-04FG-00029) | [Rokland 5.8 dBi outdoor kit, $49.97](https://store.rokland.com/products/meshtastic-compatible-6-dbi-n-female-omni-outdoor-915-mhz-antenna-kit-with-6-10-or-15-cable-choice) |
| Power, stake, zip ties | What you own: two USB power banks, a broom handle or garden stake | — |

**Minimum spend:** two Rokland boards and the adapter, about $64. With the attenuator, about $80.

### Two ways to run it

- **Quick walk, no code: Meshtastic's [Range Test module](https://meshtastic.org/docs/configuration/module/range-test/).** Flash both boards with Meshtastic, set region US, turn the module on. One node sends numbered packets and the other saves `rangetest.csv` with positions to its own flash, downloadable over Wi-Fi. It sends only one packet every 15–60 s, so use it to find roughly where the link dies, not to count delivery.
- **Counted points: a ping sketch.** For 100 packets per point in a few minutes, flash a short transmit/receive sketch built on [RadioLib](https://github.com/jgromes/RadioLib), which ships SX126x examples. It sends a numbered packet every second or two. It also sets the radio's output power directly, which the margin method needs.

### The margin method: let a small woodlot stand in for 2 km of forest

A yes/no at each point says little. **How much signal is spare** says more:

1. At each point, step the transmit power down (22, 17, 12, 7, 2 dBm, then lower), and note where delivery falls under 80%. The 10 dB attenuator adds another step if needed.
2. What you could cut is the **margin in dB**. Each step down in spreading factor, SF12 to SF7, costs roughly another 2.5 dB.
3. Do it at a few forest distances (150, 300, 600 m). The fall in margin with depth gives the trees' loss per 100 m, and so a rough prediction of where the link dies.

This is an **extrapolation**: forest loss does not grow evenly with depth ([Weissberger's model](https://en.wikipedia.org/wiki/Weissberger%27s_model)). At least one real 2 km forest point is still needed for the pass.

### Where

| Run | Place | Node | Receiver |
|---|---|---|---|
| A: open | A farm road or long field | Staked at 0.5 m and 1 m | Raised 6–10 m, and at 2 m |
| B: under canopy | A woodlot, node inside | 1 m | At the edge, raised |
| C: forest hops | The same woods | Both at 1 m, 100–300 m apart | — |
| E: hedgerows | Farmland with hedgerows, the nearest US match for [windbreak belts]({{ site.baseurl }}{% link models/tripwire.md %}#a-windbreak-belt-is-not-a-forest) | Across 1, 2 and 3 belts | Raised, at the last belt |

Run it now, with leaves on, and again in December, with leaves off.

### Gate

Use [T9's pass marks]({{ site.baseurl }}{% link research/open-questions.md %}#the-test-t9) unchanged: for example, 90% delivered at 3 km in the open from a 1 m node, and 80% node to node at 200 m in forest.

- **Pass, or margins that predict a pass:** go to layer 2.
- **Fails in forest, passes in the open:** carry on, but plan denser lines under trees or a different way home ([what a fail means]({{ site.baseurl }}{% link research/open-questions.md %}#the-test-t9)).

**Cannot be tested at home:** jamming (T19). Running a jammer is illegal in the US outside licensed ranges. Everything above runs licence-free at legal power on 915 MHz.

</details>

<details class="layer" id="layer-2-hear-a-drone-from-near-the-ground-t11" markdown="block">
<summary><span class="layer-title">Layer 2: hear a drone from near the ground (T11), about $50</span><span class="layer-sub">How far does a cheap mic on a 0.5–1 m stake hear a drone? That sets spacing, and so the cost of a line</span></summary>

**Why second:** spacing drives everything the line costs. The site assumes listeners every 200–300 m against FPVs, but the [only measured range]({{ site.baseurl }}{% link models/tripwire.md %}#warning-time-comes-from-distance) for cheap mics is 50–60 m against a consumer drone in wind.

This is the [weekend test kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector) with the mic lowered to listener height. The layer 1 boards run Batear's detector and gateway.

### Buy

| Item | Buy | Alternatives |
|---|---|---|
| **I2S MEMS mics**, 3 | [Adafruit SPH0645 breakout, $6.95 each](https://www.adafruit.com/product/3421) (Adafruit calls it the drop-in replacement for the discontinued ICS-43434 that Batear prefers) | INMP441 (the one in Batear's wiring guide): [Vetco, $4.95](https://vetco.net/products/omnidirectional-microphone-module-inmp441-high-precision-i2s), or a [5-pack on Amazon, about $13](https://www.amazon.com/dp/B09G4RNT3G) |
| **Fur windscreens** | [Movo WS10n 5-pack, $14.95](https://www.movophoto.com/products/ws10n-universal-furry-outdoor-microphone-windscreen-lavalier) | [Movo WS-RD 2-pack, $9.95](https://www.movophoto.com/products/ws-rd-furry-lav-mic-windscreen-2x) |
| **Breadboard and jumpers** | [Adafruit half-size breadboard + 78 jumpers, $9.95](https://www.adafruit.com/products/3314) | [SparkFun 140-piece jumper kit, $8.95](https://www.sparkfun.com/jumper-wire-kit-140pcs.html) |
| **Recorder** (labelled training audio) | [Seeed XIAO ESP32S3 Sense, from $13.99](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html): built-in mic and microSD; pick the Sense variant | A phone in a windscreen, free. [SparkFun Thing Plus ESP32-S3, $24.95](https://www.sparkfun.com/sparkfun-thing-plus-esp32-s3.html) |
| **Stake**, 0.5–1 m, slightly springy | Fibreglass driveway markers, 48 in, a few dollars each at any hardware store (search "fiberglass driveway marker"; no store page loaded for us) | A garden stake |
| **Drone** | **Borrow.** A real 5–7 inch FPV is the target: find a pilot through the [AMA club finder](https://www.modelaircraft.org/club-finder) or [MultiGP chapters](https://www.multigp.com/chapters/) | [Potensic ATOM SE, $249.99](https://store.potensic.com/products/atom-se). DJI Mini 4K is the usual buy, about $299, but its store page did not load for us. [DJI Neo, $169](https://store.dji.com/product/dji-neo) was out of stock |
| Wind speed | A phone weather app, free | Any handheld anemometer, about $15–35 (no single page verified) |

**Spend:** about $50 with a borrowed drone.

### Run it

As in the [weekend plan]({{ site.baseurl }}{% link research/open-source-builds.md %}#a-weekend-plan), with the mic on a stake at **0.5 m and 1 m**, not 1–2 m:

- Hover 60 s at 25, 50, 100, 150, 200 and 300 m, at two altitudes, then fly straight passes.
- Log wind for every run.
- Record 30+ minutes of no drone: traffic, mowers, wind, birds.
- Repeat at a tree line, with the drone flying along it, since that is the [approach route]({{ site.baseurl }}{% link research/field-conditions.md %}#where-infantry-actually-sit-tree-lines).

Fly under FAA recreational rules (with the free TRUST certificate) or Part 107, at a legal site.

### Gate (proposed)

- **Pass:** 9 of 10 passes detected at **100 m or more** in light wind with a consumer drone, or 150 m with an FPV. Lines at about 200 m spacing then hold.
- **Fail (under 60 m):** a line needs three to four times the listeners per km. Rework the [cost]({{ site.baseurl }}{% link models/tripwire.md %}#what-it-costs-estimates) before layer 3, since this may kill the economics, not the physics.

</details>

<details class="layer" id="layer-3-the-edge-receiver-t17" markdown="block">
<summary><span class="layer-title">Layer 3: the silent edge receiver (T17), about $90–130</span><span class="layer-sub">A receive-only board raised at the tree-line edge, wired back to the "dugout", proven with an SDR to emit nothing</span></summary>

**Why now:** the unit cannot transmit from its position without being found. This layer proves it can [hear the line silently]({{ site.baseurl }}{% link models/tripwire.md %}#the-design-a-listen-only-receiver-at-the-tree-line-edge-wired-home), on the links layer 1 measured.

### Buy

| Item | Buy | Alternatives |
|---|---|---|
| **Third LoRa board**, receive only | Heltec V3, [Rokland, $29.97](https://store.rokland.com/products/heltec-wifi-lora-32v3) | As layer 1 |
| **RS-485 transceiver** at the edge | [SparkFun RS-485 breakout (3.3 V), $12.50](https://www.sparkfun.com/sparkfun-transceiver-breakout-rs-485.html) | Generic "MAX3485 module", a few dollars (3.3 V part; the common MAX485 is 5 V) |
| **USB to RS-485** at the dugout laptop | [Waveshare USB to RS485 (B), about $7.99](https://www.waveshare.com/product/iot-communication/wired-comm-converter/usb-to-rs485-b.htm) | Any FTDI or CH340-based RS-485 adapter |
| **Wire** | **At home:** any old Ethernet cable; one twisted pair carries the data | Full 300 m run later: [direct-burial Cat5e, 1000 ft, CCTV Camera World, $243](https://www.cctvcameraworld.com/products/direct-burial-cat5e-cable-1000ft.html) |
| **Directional antenna** | **DIY:** a 915 MHz wire Yagi on a wooden boom, a few dollars of copper and an hour; many free calculators | [Pasternack 9 dBi Yagi, $254.99](https://www.pasternack.com/single-antenna-880-960-mhz-9-dbi-gain-n-pe51ya1018-p.aspx) (N connector, needs an N-to-SMA cable), or start with layer 1's omni |
| **Getting it into the canopy** | A tennis ball and paracord, free | [WesSpur arborist throw line kit](https://wesspur.com/arborist-throw-line-kit) (about $50 and up) |
| **SDR** to prove silence | [Nooelec NESDR SMArt v5 bundle, $54.95](https://www.nooelec.com/store/sdr/sdr-receivers/nesdr-smart.html) | [RTL-SDR Blog V3, about $35–40](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/) (the V4 is no longer sold) |

### Run it

1. Set the edge board to receive only, raise it 5–10 m at a woodlot or hedgerow edge, and run the cable into the trees to a laptop.
2. Place layer 1's sender at the distances that passed, and log delivery at the laptop.
3. Run the SDR beside the edge board and at the laptop for an hour. Look for any burst on 902–928 MHz from our end.
4. RS-485 is specified for about 1,200 m at low data rates. Prove it on 300 m only once the short run works.

### Gate (proposed)

- **Pass:** the edge receiver matches layer 1's delivery from the same points, the SDR shows **no transmission** from the edge or the dugout, and alerts reach the laptop within 2 s of arriving at the edge.
- **Fail:** if the board emits anything in receive mode, fix the firmware before going on. Range worse than layer 1 points at the antenna or its height.

</details>

<details class="layer" id="layer-4-battery-and-cold-t12" markdown="block">
<summary><span class="layer-title">Layer 4: battery and cold (T12), about $35–135</span><span class="layer-sub">Does a listener that sleeps until it hears something last weeks, and how much less in winter? The kitchen freezer is the cold chamber</span></summary>

**Why now:** listeners are thrown away, so battery life sets the [running cost]({{ site.baseurl }}{% link models/tripwire.md %}#the-running-cost-lines-are-ammunition). It needs the classifier trained on layer 2's recordings.

### Buy

| Item | Buy | Alternatives |
|---|---|---|
| **Current meter** | [Nordic Power Profiler Kit II, Adafruit, $99.95](https://www.adafruit.com/product/5048): measures the sleep current properly | A USB power meter such as the FNIRSI FNB58, about $40–50 (no US page verified). It reads the average, not microamp sleep |
| **Cells** | [Molicel P28A 18650, $5.99](https://www.18650batterystore.com/products/molicel-p28a) | [Samsung 30Q, $6.99](https://www.18650batterystore.com/products/samsung-30q); [Battery Junction P28A, about $6.70](https://batteryjunction.com/molicel-inr18650-p28a) |
| **Cell holder** | [SparkFun 1×18650 holder with leads, $1.25](https://www.sparkfun.com/battery-holder-1x18650-wire-leads.html) (on backorder when checked) | Any single 18650 holder with wire leads |
| **Battery plug** | The V3 comes with an SH1.25 two-pin battery lead: solder it to the holder | A LiPo with a "Micro JST 1.25" plug, listed on [Rokland's V3 page](https://store.rokland.com/products/heltec-wifi-lora-32v3). Adafruit's LiPos **do not fit** (JST-PH) |
| **Freezer logger** | [Inkbird IBS-TH2 Plus, $24.99](https://inkbird.com/products/ibs-th2-plus): put only its probe in the freezer, the body is rated to −10 °C | [GoveeLife Thermometer R1, $39.99](https://us.govee.com/products/goveelife-smart-thermometer-r1) |

### Run it

1. Measure sleep current, listen-and-classify current and send current. Multiply out to days on one cell.
2. Run one listener on a cell at room temperature, with a speaker playing a drone clip on a timer, until it dies.
3. Repeat in the kitchen freezer (about −18 °C) with the board sending its battery voltage and temperature, as the [cold fix]({{ site.baseurl }}{% link models/tripwire.md %}#solving-the-field-limits-at-no-extra-cost) designs it.

### Gate (proposed)

- **Pass:** at least **3 weeks** at room temperature, with the cold penalty measured.
- **Fail:** recompute the [running cost]({{ site.baseurl }}{% link models/tripwire.md %}#the-running-cost-lines-are-ammunition). A one-week listener may still pay, but the tripwire page's figures change.

</details>

<details class="layer" id="layer-5-the-mvp-a-six-listener-line" markdown="block">
<summary><span class="layer-title">Layer 5: the MVP, a six-listener line, about $250–350</span><span class="layer-sub">Six hand-placed listeners across a hedgerow gap 1–2 km out, the silent edge receiver, and real drone crossings</span></summary>

**What it proves:** that the parts proven one at a time work as one system. A drone crosses, a listener hears it, the alert hops home, the edge receiver hears it, and a screen in the trees shows it, fast enough to matter.

### Buy

Six listeners, using the parts proven above:

| Per listener | Buy | Cost |
|---|---|---|
| LoRa board | Heltec V3, [Rokland](https://store.rokland.com/products/heltec-wifi-lora-32v3) or [Heltec](https://heltec.org/project/wifi-lora-32-v3/) | $18–30 |
| Mic and windscreen | From layer 2 | $7–10 |
| Cell and holder | From layer 4 | $7–8 |
| Box | [IP65 ABS box 100×68×50 mm, Newegg Business, $10.99](https://www.neweggbusiness.com/p/9B-072-001K-007A7) | $11 |
| Stake | Fibreglass driveway marker | $3–5 |
| **Per listener** | | **≈ $45–65** |

Six listeners come to about $270–390. Add four if layer 1 showed forest hops need closer spacing.

### Run it

1. **Lay it by hand**, as the tripwire page [recommends for first builds]({{ site.baseurl }}{% link models/tripwire.md %}#why-not-have-people-place-the-listeners): six listeners across a gap between hedgerows or along a woodlot edge, at layer 2's spacing, 1–2 km from the edge receiver.
2. **Fly 20 crossings** at different heights, times and wind, with a GPS log for each.
3. **Leave it a week** (T5) to count false alarms from traffic, tractors, birds and aircraft.

Measure:
- crossings detected;
- time from the drone crossing the line to the alert on screen;
- delivery per link;
- false alarms per day;
- battery left at the end.

### Gate for the MVP (proposed)

- **18 of 20 crossings** reach the screen, each within **10 seconds** of the drone crossing.
- **Under one false alarm per line per day** over the week.
- **No transmission** from the receiving end, confirmed with the SDR.

If it passes, the idea is shown to work at small scale on US ground. It is still not shown against jamming, Ukrainian terrain, mass raids or air-dropped placement.

</details>

## After the MVP

Not needed to prove the idea, and mostly costlier or not testable at home:

| Test | What it adds | Why later |
|---|---|---|
| T7, 20+ listeners | Loss during a mass raid | ~$1,000, and only matters once a line works |
| T10, T13, T14 | Dropping listeners from a drone, with and without GPS | Hand placement proves everything else first |
| T15 | Telling friendly drones from enemy | Needs recordings of real friendly types |
| T19 | Does the link survive a jammer? | Illegal to run in the US; needs a partner with a licensed range or a test in Ukraine |
| T6 | Shahed-class engines | Needs a partner |

Full list: [open questions and field tests]({{ site.baseurl }}{% link research/open-questions.md %}).
