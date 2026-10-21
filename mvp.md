---
title: Weekend test and MVP
nav_primary: 4
---

# Weekend test and MVP: $80 to a working line
{: .no_toc }

The [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}) built in five cheap layers. Each answers one question, and its gate decides whether to buy the next. **MVP = layer 5:** six hand-placed listeners hear a real drone and alert a screen in a tree line, while the receiving end transmits nothing.

{: .warning }
> **A plan, not a result: no layer has been run yet.** Gates marked *proposed* are ours; T9's are the site's. Links were loaded 2026-10-15. Items that wouldn't load are search terms.

## Start here: the Saturday test {#weekend-test}

**One day, about $80–90.** How far does a mic half a metre off the ground hear a drone? And how far can its alarm travel by radio?

<div class="stats">
  <div class="stat"><p class="stat-num">$80–90</p><p class="stat-label">with a borrowed drone; ~$360–480 buying everything</p></div>
  <div class="stat"><p class="stat-num">1 day</p><p class="stat-label">2 hours of setup, 3–4 hours in a field</p></div>
  <div class="stat"><p class="stat-num">60 m</p><p class="stat-label">fail: under this, a line needs 3–4× the listeners</p></div>
  <div class="stat"><p class="stat-num">100 m</p><p class="stat-label">pass: heard at 100 m (consumer drone) or 150 m (FPV)</p></div>
</div>

1. **Flash two Heltec boards** from the [Batear web flasher](https://docs.batear.io/flasher/): one *detector*, one *gateway*. Give the gateway your phone's hotspot ([how](#phone-setup)).
2. **Wire a mic** to the detector ([pins]({{ site.baseurl }}{% link research/open-source-builds.md %}#the-saturday-test)).
3. **Open the logger** on your phone and connect. Play a drone clip at the mic. You should see an alarm.
4. **In the field,** put the detector and a recording phone side by side, 0.5 m up, in windscreens. Clap and press **Sync clap**.
5. **Speaker sweep.** Play the speaker files from 5 m. Log each as a *Speaker* run ([how](#speaker-test)). Skip this without a laptop and sound meter.
6. **Fly.** Take off beside the mic. Hover 60 s at 50, 100 and 150 m. Log each as a *Hover* run.
7. **Record 30 minutes with no drone.** Log it as *No drone*.
8. **Walk the gateway away** until packets stop, with a phone looping the drone clip at the detector. Log each stop as a *Radio walk*.
9. **Export** both CSVs before you leave.

**The result** is the logger's *Range so far* table: heard at 100 m passes, under 60 m fails.

Kit and buying advice: [weekend test kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector). In the US, pass the free TRUST test and check the airspace before flying.

### The logger {#weekend-logger}

Below it is running on **made-up demo data**.

<iframe class="logger-demo" src="{{ site.baseurl }}/tools/weekend/logger.html?embed=1" title="Weekend logger, running on demo data" loading="lazy"></iframe>

<p><a class="btn btn-primary" href="{{ site.baseurl }}/tools/weekend/logger.html">Open the logger on your phone</a> <a class="btn" href="{{ site.baseurl }}/tools/weekend/logger.html?demo=1">Try it with demo data</a></p>

<details class="layer" id="phone-setup" markdown="block">
<summary><span class="layer-title">Set up the phone (WiFi)</span><span class="layer-sub">Any phone. The gateway joins your hotspot and the page reads it through a public MQTT broker</span></summary>

1. Turn on your phone's hotspot. On an iPhone, switch on **Maximize Compatibility**: the board only sees 2.4 GHz.
2. Open the logger on the phone. Under **Connect** it shows a gateway ID such as `tw-k3f9x2`.
3. When you flash the gateway, fill in the Batear flasher's gateway settings:
   - Wi-Fi SSID and password: your hotspot's
   - MQTT broker URL: `mqtt://broker.hivemq.com:1883`
   - Gateway Device ID: the logger's ID
4. Tap **Connect over WiFi**. The chip turns to *gateway online* when the board checks in.

This needs mobile data, so you need a cell signal in the field. Readings pass through a free public broker, so anyone who guessed the ID could read them: fine for a backyard test, not for anything sensitive. Keep the screen on. The page asks the phone to stay awake, and readings that arrive while it's locked are lost.

Phones can't read a USB board from a web page: iPhones never could, and Chrome on Android is only starting to. With a laptop and a cable, use **Connect USB** instead. Plugging in the detector as well adds its confidence score.

The gateway only hears from the detector when it alarms, clears, or sends its 30-minute heartbeat. That's why the radio walk needs a drone clip looping at the detector. Leave **Beep on alarm** off while recording.
</details>

<details class="layer" id="weekend-downloads" markdown="block">
<summary><span class="layer-title">Downloads</span><span class="layer-sub">Firmware, the logger, the speaker files and the clip cutter</span></summary>

| File | What it's for | Get it |
|---|---|---|
| Batear firmware | Detector and gateway, unchanged. Our own firmware isn't needed until layer 3 | [Web flasher](https://docs.batear.io/flasher/) |
| Logger | The page above, as one file that works offline over USB | <a href="{{ site.baseurl }}/tools/weekend/logger.html" download>logger.html</a> |
| Speaker files | `make_playback.py`: turns one drone recording and one meter reading into a 60 s file per distance for the [speaker test](#speaker-test) | <a href="{{ site.baseurl }}/tools/weekend/make_playback.py" download>make_playback.py</a> · <a href="{{ site.baseurl }}/tools/weekend/test_make_playback.py" download>tests</a> |
| Clip cutter | Lines a recording up on the clap and cuts each run into labelled 1 s clips: `drone_100m`, `drone_pass`, `background`. The manifest records whether Batear was alarming during each clip: the baseline a model has to beat | <a href="{{ site.baseurl }}/tools/weekend/cut_clips.py" download>cut_clips.py</a> · <a href="{{ site.baseurl }}/tools/weekend/test_cut_clips.py" download>tests</a> |

Afterwards, to make training clips from each recording (Python 3.11+, and [ffmpeg](https://ffmpeg.org/) for a phone's `.m4a`):

```bash
python cut_clips.py --runs S20261025-1003_runs.csv --events S20261025-1003_events.csv --recording phone-0.5m.m4a --sync --tag mic05 --rate 16000 --out clips
```

Hold out whole runs for testing, never clips from a run you trained on.
</details>

{: .note }
> The tools are tested on demo data and synthetic audio, not yet on a real board.

### Could a speaker stand in for the drone? {#speaker-test}

**For most distances, yes.** A speaker finds the detector's threshold cheaply and precisely. It can't copy what 100 m of real ground does to the sound, so step 6 still flies the drone at three distances to check it.

<details class="layer" markdown="block">
<summary><span class="layer-title">The reasoning, and how to run it</span><span class="layer-sub">Source level, spreading, what a speaker gets wrong</span></summary>

**The arithmetic.** EASA lists the DJI Mini 4 Pro and Mini 5 Pro at a sound power of **81 dB(A)** ([EASA](https://www.easa.europa.eu/en/node/143951)). Spreading over a sphere, that is about 70 dB(A) at 1 m, 36 at 50 m, **30 at 100 m**, 24 at 200 m and 20 at 300 m (6 dB less each time the distance doubles). A quiet field is often 30–40 dB(A). So at 100 m a consumer drone is about as loud overall as the background, and detection depends on its rotor tones standing out in narrow bands. That fits the only measured cheap-mic range, 50–60 m. Air absorption hardly matters at these distances: under about 1 dB at 300 m below 1 kHz (ISO 9613-1, 20 °C, 70% humidity), rising to several dB above 2 kHz.

**Two ways to use a speaker:**

| | A. Speaker near the mic, turned down | B. Speaker at the real distance, on a pole |
|---|---|---|
| Set-up | Speaker 5 m from the mic. Play the drone clip quieter by 20·log₁₀(distance ÷ 5) dB: 26 dB for 100 m, 32 dB for 200 m | Speaker 3–10 m up at the real distance, playing at the drone's own level (about 70 dB(A) at 1 m for a Mini-class drone) |
| Captures | The detector's threshold against your real background noise, in 1 dB steps, as often as you like | Also the real ground, wind and trees along the path |
| Misses | Everything along the path: ground interference near a 0.5 m mic, wind bending the sound (upwind can lose 10 dB or more), turbulence | The drone's height and motion, and its own directivity |
| Needs | Any Bluetooth speaker, a basic sound level meter | A speaker that plays loud without distorting; FPV levels are unknown and probably much louder |

**What makes it work:**
- **Calibrate loud, then attenuate exactly.** Cheap sound meters can't read 20–30 dB(A). Measure the clip at the mic at a comfortable level, then make the quieter versions by digital gain, not by guessing with the volume knob.
- **Know the source level.** Recordings online aren't level-calibrated. For a Mini-class drone, use EASA's 81 dB(A). For an FPV, borrow one for ten minutes and measure it at 5 m: no published measurement turned up.
- **Watch for distortion.** A speaker driven hard adds harmonics, and harmonics are what Batear's detector listens for, so distortion would flatter the result. Keep the speaker well below full volume, and compare the h2 and h3 values in the detector's log for the speaker and the real drone at the same level.
- **Check the low end.** Small speakers lose output in the low hundreds of hertz, where consumer-drone rotor tones sit. Look at the clip's spectrum before trusting a small speaker.
- **Log it as a speaker.** Use the logger's *Speaker* run type. Its results get their own line in the range table, and the clip cutter labels them `speaker_100m`, never mixed with real flights.

**What it buys.** Each 6 dB of detector sensitivity doubles the range. A speaker can measure that threshold in an afternoon, without a pilot, airspace rules or an FPV. It can also run at night, in wind, and next to a road, and it builds training data at known levels. One real flight at 50, 100 and 150 m then shows whether the threshold-plus-spreading estimate holds over real ground. If it does, later tests can lean on the speaker. If not, the gap is the near-ground effect T11 exists to measure.

These are standard acoustics estimates, not measurements of our kit.
</details>

<details class="layer" markdown="block">
<summary><span class="layer-title">Run the speaker test</span><span class="layer-sub">make_playback.py writes one file per distance, level-matched to a single meter reading</span></summary>

You need a steady recording of the drone hovering, a Bluetooth speaker 5 m from the mic, and a sound level meter. Set the meter to A-weighting, slow, and read it at the mic.

1. **Make the calibration file**, play it, and measure it. Then turn the speaker off and measure the background too. Don't touch the volume from here on.

   ```bash
   python make_playback.py --clip mini-hover.wav --out playback --cal-only
   ```

2. **Write the distance files** from those two readings. `--source-lwa 81` is the Mini 4 Pro's EASA figure; for a drone you measured yourself, use your reading at 5 m, e.g. `--source-spl 56 --source-distance 5`.

   ```bash
   python make_playback.py --clip mini-hover.wav --out playback --cal-spl 66 --cal-background 38 --source-lwa 81 --distances 25,50,75,100,150,200,300
   ```

   Each file is 60 s of the clip, looped, turned down by the exact amount for its distance: 36 dB below the calibration for 100 m in this example. `playlist.csv` lists file, distance, level and gain. For a threshold sweep, use `--levels 40,38,36,34,32,30,28,26` instead: one file per level at the mic, each named with the distance it stands for.

3. **Play each file** and log it in the logger as a *Speaker* run at that distance. Three runs per distance give the range table enough to call it.

If a distance needs the speaker louder than the calibration, the script refuses: turn up, move closer, and measure again. Levels below the background are expected at range; that's the regime being tested.
</details>

## The five layers to the MVP

| Layer | Question | Spend | Total | Gate |
|---|---|---|---|---|
| [0](#layer-0) T18 | Where does a minute help most, and how would troops place a line? | $0 | $0 | None: sizes the payoff, shapes placement |
| [1](#layer-1-the-radio-test-t9) T9 | Can a board at 0.5–1 m report back over 2–3 km, through trees? | ~$65–80 | ~$80 | T9's marks, or margins that predict them |
| [2](#layer-2-hear-a-drone-from-near-the-ground-t11) T11 | How far does a mic at 0.5–1 m hear a drone? | ~$50 | ~$130 | ≥100 m (sets spacing, so cost per km) |
| [3](#layer-3-the-edge-receiver-t17) T17 | Can the edge receiver hear the line without transmitting? | ~$90–130 | ~$250 | Layer 1's delivery, SDR sees nothing |
| [4](#layer-4-battery-and-cold-t12) T12 | Does a listener last weeks, and in the cold? | ~$35–135 | ~$300–400 | ≥3 weeks, cold loss measured |
| [5](#layer-5-the-mvp-a-six-listener-line) MVP | Does the whole chain work? | ~$250–350 | ~$600–750 | 18/20 crossings in 10 s, <1 false alarm/day, silent |

Assumed owned: laptop, phone, USB power banks, soldering iron.

## Layer 0: ask alongside (T18, $0, not a gate) {#layer-0}

Earlier warning against a threat nothing else detects (fibre-optic FPVs), at lower cost, is worth having; that is not tested here. 5–10 interviews ([questions]({{ site.baseurl }}{% link research/problem-check.md %}#the-next-step-ask-before-building-t18)) only tune the build: which moments matter most (sizes the [lives estimate]({{ site.baseurl }}{% link research/lives-model.md %})), and how troops would place listeners and a receiver.

<details class="layer" id="layer-1-the-radio-test-t9" markdown="block" open>
<summary><span class="layer-title">Layer 1: radio test (T9), ~$80</span><span class="layer-sub">Board at 0.5–1 m to a raised receiver, 2–3 km, across open ground, forest and hedgerows</span></summary>

**Why first:** it is the [deciding question]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-home), it needs no drone, and every later layer reuses the boards.

| Item | Buy | Alternatives |
|---|---|---|
| **2 × LoRa board**, 915 MHz | Heltec V3 2-pack, [Amazon, $44.98](https://www.amazon.com/dp/B0CW6151WJ) | [Rokland, $29.97 each](https://store.rokland.com/products/heltec-wifi-lora-32v3); [Heltec direct, $17.90–19.90](https://heltec.org/project/wifi-lora-32-v3/) + China shipping; [RAK WisBlock kit, $34.97](https://store.rokland.com/products/rak-wireless-wisblock-meshtastic-starter-kit); [LILYGO T3S3, $72.99](https://www.tindie.com/products/yihang/915mhz-meshtastic-kit-t3s3-s3-sx1262/) |
| **u.FL→SMA cable** (V3 has no SMA) | Proxicast, [Amazon, $7.94](https://www.amazon.com/dp/B09GJGNPQX) | [Adafruit 851, $3.95](https://www.adafruit.com/product/851) |
| **10 dB attenuator** (margin method) | MWRF, [Amazon, $12.49](https://www.amazon.com/dp/B07MRG9RDV) | [Inmet AHC-10, RF Parts, $15.91](https://www.rfparts.com/ahc-10.html); [L-com 20 dB, $92.09](https://www.l-com.com/coaxial-2w-20db-rf-fixed-attenuator-sma-male-to-sma-female-passivated-stainless-steel-body-up-to-6-ghz) |
| **Mast**, 6–10 m | **Free:** upstairs window, roof edge, tree | Mifoci 23 ft, [Amazon, $59.99](https://www.amazon.com/dp/B0GYYL3S6C) (16 ft [$39.99](https://www.amazon.com/dp/B0GYXPXCNY)); [Spiderbeam 12 m HD, $109.99](https://moonrakeronline.com/us/spiderpole-12hd-telescopic-pole-12m-heavy-duty-fibreglass) |
| **Antenna** (run D) | 915 MHz omni with u.FL lead, [Amazon, $16.95](https://www.amazon.com/dp/B0GSB5XKLF) | [8 dBi omni, Newegg Business, $16.99](https://www.neweggbusiness.com/p/9B-2VT-04FG-00029); [Rokland 5.8 dBi kit, $49.97](https://store.rokland.com/products/meshtastic-compatible-6-dbi-n-female-omni-outdoor-915-mhz-antenna-kit-with-6-10-or-15-cable-choice) |

**Minimum:** 2 boards + cable, $53. With the attenuator, $65.

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
| **3 × I2S mic** | INMP441 5-pack (Batear's wiring), [Amazon, $12.51](https://www.amazon.com/dp/B09G4RNT3G) | Adafruit SPH0645: [Amazon, $12.62](https://www.amazon.com/dp/B06XNL2GBW), [Adafruit, $6.95](https://www.adafruit.com/product/3421); INMP441 at [Vetco, $4.95](https://vetco.net/products/omnidirectional-microphone-module-inmp441-high-precision-i2s) |
| **Fur windscreens** | eBoot 5-pack, [Amazon, $8.99](https://www.amazon.com/dp/B01E4ZMTEG) | [Movo WS10n 5-pack, $14.95](https://www.movophoto.com/products/ws10n-universal-furry-outdoor-microphone-windscreen-lavalier) |
| **Breadboard + jumpers** | BOJACK kit, [Amazon, $9.99](https://www.amazon.com/dp/B08Y59P6D1) | [Adafruit 3314, $9.95](https://www.adafruit.com/products/3314); [SparkFun 140 pcs, $8.95](https://www.sparkfun.com/jumper-wire-kit-140pcs.html) |
| **Recorder** | XIAO ESP32S3 Sense, [Amazon, $23.99](https://www.amazon.com/dp/B0C69FFVHH) | Phone in a windscreen (free); [Seeed direct, $13.99](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html) |
| **Stake** | 48 in fiberglass, 20-pack, [Amazon, $23.99](https://www.amazon.com/dp/B0DF58T198) | Garden stake |
| **Drone** | **Borrow a 5–7 in FPV:** [AMA clubs](https://www.modelaircraft.org/club-finder), [MultiGP](https://www.multigp.com/chapters/) | [Potensic ATOM SE, $249.99](https://store.potensic.com/products/atom-se); DJI Mini 4K ~$299 (search); [DJI Neo, $169](https://store.dji.com/product/dji-neo), out of stock |
| **Wind** | Phone weather app | Anemometer, [Amazon, $12.99](https://www.amazon.com/dp/B0D7Z43M9S) |

**Run** ([weekend plan]({{ site.baseurl }}{% link research/open-source-builds.md %}#the-saturday-test), mic at 0.5 and 1 m)
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
| **3rd LoRa board** | Heltec V3, [Amazon, $34.99](https://www.amazon.com/dp/B0D1H1FN9Y) | [Rokland, $29.97](https://store.rokland.com/products/heltec-wifi-lora-32v3); as layer 1 |
| **RS-485, edge** | MAX3485 (3.3 V) 5-pack, [Amazon, $8.99](https://www.amazon.com/dp/B0FTFXT876) | [SparkFun breakout, $12.50](https://www.sparkfun.com/sparkfun-transceiver-breakout-rs-485.html). Not the 5 V MAX485 |
| **USB→RS-485, laptop** | FT232RL adapter, [Amazon, $16.31](https://www.amazon.com/dp/B081MB6PN2) | [Waveshare (B), ~$7.99](https://www.waveshare.com/product/iot-communication/wired-comm-converter/usb-to-rs485-b.htm) |
| **Wire** | Old Ethernet cable (one pair) | 300 m run: burial Cat5e 1000 ft, [Amazon VIVO, $89.99](https://www.amazon.com/dp/B0092TJ4K2) or [TRUE CABLE, $228.99](https://www.amazon.com/dp/B01JAVNWOK) |
| **Directional antenna** | **DIY** wire Yagi on a wooden boom, a few dollars | 7 dBi Yagi, N-female, [Amazon, $24.99](https://www.amazon.com/dp/B0CPFT1V9L) (needs N→SMA); [Pasternack 9 dBi, $254.99](https://www.pasternack.com/single-antenna-880-960-mhz-9-dbi-gain-n-pe51ya1018-p.aspx) |
| **Into the canopy** | Tennis ball + paracord | Throw line kit, [Amazon, $21.68](https://www.amazon.com/dp/B0DH2SV5XK) |
| **SDR** | RTL-SDR Blog V3 + dipoles, [Amazon, $47.95](https://www.amazon.com/dp/B0BMKB3L47) | Dongle only, [Amazon, $37.95](https://www.amazon.com/dp/B0BMKZCKTF); Nooelec SMArt v5, [Amazon, $44.95](https://www.amazon.com/dp/B01HA642SW) |

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
| **Current meter** | [Nordic PPK2, Adafruit, $99.95](https://www.adafruit.com/product/5048) (reads µA sleep current; Amazon $189.99) | FNIRSI FNB58, [Amazon, $49.99](https://www.amazon.com/dp/B0BJ253W31). Average current only |
| **Cells** (not on Amazon) | [Molicel P28A, $5.99](https://www.18650batterystore.com/products/molicel-p28a) | [Samsung 30Q, $6.99](https://www.18650batterystore.com/products/samsung-30q); [Battery Junction P28A, ~$6.70](https://batteryjunction.com/molicel-inr18650-p28a) |
| **Holder** | 2-pack with leads, [Amazon, $5.99](https://www.amazon.com/dp/B092TGQ7PB) | [SparkFun 1×18650, $1.25](https://www.sparkfun.com/battery-holder-1x18650-wire-leads.html) (backordered) |
| **Plug** | Solder the V3's included SH1.25 lead to the holder | LiPo with "Micro JST 1.25" ([Rokland V3 page](https://store.rokland.com/products/heltec-wifi-lora-32v3)). Adafruit LiPos (JST-PH) don't fit |
| **Freezer logger** | Inkbird IBS-TH2 Plus, [Amazon, $24.99](https://www.amazon.com/dp/B08TM67HJH) (only the probe goes in; the body is rated to −10 °C) | [GoveeLife R1, $39.99](https://us.govee.com/products/goveelife-smart-thermometer-r1) |

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
| Heltec V3 | [Amazon 2-pack](https://www.amazon.com/dp/B0CW6151WJ), or [Heltec direct](https://heltec.org/project/wifi-lora-32-v3/) | $18–23 |
| Mic + windscreen | Layer 2 packs | $4–5 |
| Cell + holder | Layer 4 | $9 |
| Box | uxcell IP65 100×68×50 mm, [Amazon, $15.69](https://www.amazon.com/dp/B07FKN8SZG); [Newegg Business, $10.99](https://www.neweggbusiness.com/p/9B-072-001K-007A7) | $11–16 |
| Stake | Layer 2's 20-pack | $1–2 |
| **Total** | | **$45–55** |

Six listeners cost $270–330. Add four if layer 1's forest hops need tighter spacing.

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

<details class="layer" id="shopping-list" markdown="block">
<summary><span class="layer-title">Full shopping list, all layers</span><span class="layer-sub">Amazon where it sells the part, prices checked 2026-10-15. Alternatives are in each layer</span></summary>

| Layer | Item | Buy | Price |
|---|---|---|---|
| 1 | Heltec LoRa 32 V3, 915 MHz, 2-pack | [Amazon](https://www.amazon.com/dp/B0CW6151WJ) | $44.98 |
| 1 | u.FL→SMA pigtail, Proxicast | [Amazon](https://www.amazon.com/dp/B09GJGNPQX) | $7.94 |
| 1 | 10 dB SMA attenuator, MWRF | [Amazon](https://www.amazon.com/dp/B07MRG9RDV) | $12.49 |
| 1 | 915 MHz omni, N, with u.FL lead (run D) | [Amazon](https://www.amazon.com/dp/B0GSB5XKLF) | $16.95 |
| 1 | Mast, 23 ft fiberglass (optional; a window or tree is free) | [Amazon](https://www.amazon.com/dp/B0GYYL3S6C) | $59.99 |
| 2 | INMP441 I2S mic, 5-pack | [Amazon](https://www.amazon.com/dp/B09G4RNT3G) | $12.51 |
| 2 | Fur windscreens, 5-pack | [Amazon](https://www.amazon.com/dp/B01E4ZMTEG) | $8.99 |
| 2 | Breadboards + jumpers | [Amazon](https://www.amazon.com/dp/B08Y59P6D1) | $9.99 |
| 2 | Seeed XIAO ESP32S3 Sense (recorder) | [Amazon](https://www.amazon.com/dp/B0C69FFVHH) | $23.99 |
| 2 | 48 in fiberglass stakes, 20-pack | [Amazon](https://www.amazon.com/dp/B0DF58T198) | $23.99 |
| 2 | Anemometer (optional) | [Amazon](https://www.amazon.com/dp/B0D7Z43M9S) | $12.99 |
| 3 | Heltec V3, single | [Amazon](https://www.amazon.com/dp/B0D1H1FN9Y) | $34.99 |
| 3 | MAX3485 RS-485 modules (3.3 V), 5-pack | [Amazon](https://www.amazon.com/dp/B0FTFXT876) | $8.99 |
| 3 | USB→RS-485, FT232RL | [Amazon](https://www.amazon.com/dp/B081MB6PN2) | $16.31 |
| 3 | RTL-SDR Blog V3 + dipole kit | [Amazon](https://www.amazon.com/dp/B0BMKB3L47) | $47.95 |
| 3 | 915 MHz Yagi, 7 dBi (optional; DIY is a few dollars) | [Amazon](https://www.amazon.com/dp/B0CPFT1V9L) | $24.99 |
| 3 | Throw line kit (optional; a tennis ball works) | [Amazon](https://www.amazon.com/dp/B0DH2SV5XK) | $21.68 |
| 3 | Burial Cat5e, 1000 ft (300 m run only) | [Amazon](https://www.amazon.com/dp/B0092TJ4K2) | $89.99 |
| 4 | Nordic PPK2 current meter | [Adafruit](https://www.adafruit.com/product/5048) (Amazon $189.99) | $99.95 |
| 4 | 18650 cells, Molicel P28A (not on Amazon) | [18650 Battery Store](https://www.18650batterystore.com/products/molicel-p28a) | $5.99 each |
| 4 | 18650 holders with leads, 2-pack | [Amazon](https://www.amazon.com/dp/B092TGQ7PB) | $5.99 |
| 4 | Inkbird IBS-TH2 Plus freezer logger | [Amazon](https://www.amazon.com/dp/B08TM67HJH) | $24.99 |
| 5 | 2 more Heltec 2-packs (6 listeners in all) | [Amazon](https://www.amazon.com/dp/B0CW6151WJ) | $89.96 |
| 5 | IP65 box 100×68×50 mm, uxcell | [Amazon](https://www.amazon.com/dp/B07FKN8SZG) | $15.69 each |

</details>

## After the MVP

| Test | Adds | Why later |
|---|---|---|
| T7 | 20+ listeners, losses in a mass raid | ~$1,000; only matters once a line works |
| T10, T13, T14 | Drone-laid listeners, with and without GPS. Dart, X500 harness and printed carrier: [Build: hardware]({{ site.baseurl }}{% link build-hardware.md %}) | Hand placement proves the rest first |
| T15 | Friend or foe | Needs recordings of friendly drones |
| T19 | Jamming | Illegal in the US; needs a licensed range or Ukraine |
| T6 | Shahed-class engines | Needs a partner |

All tests: [open questions]({{ site.baseurl }}{% link research/open-questions.md %}).
