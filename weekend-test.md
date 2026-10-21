---
title: Saturday test
nav_primary: 4
---

# The Saturday test
{: .no_toc }

**One day, about $80–90, and no drone.** How far does a mic 20 in off the ground hear a drone, and how far can its alarm travel by radio? A Bluetooth speaker plays a recorded drone at the level it would reach the mic from 80 to 1,000 ft.

**Pass:** heard at 330 ft. **Fail:** under 200 ft.

**You need:** the two XIAO ESP32S3 + Wio-SX1262 kits with their antennas, a USB-C data cable, a laptop with Chrome, an INMP441 mic with jumper wires (its pins need soldering), two fur windscreens, a Bluetooth speaker, one phone with a free sound meter app (NIOSH SLM on an iPhone), two power banks and a tape measure ([kit and prices]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector)).

## The steps

Do steps 1–3 at home the day before.

1. **Flash both boards** from [our flasher]({{ site.baseurl }}/tools/flasher/), antennas on: the *detector*, then the *gateway* with your phone's hotspot ([how](#phone-setup)). This replaces the Meshtastic firmware they came with. Then scan the flasher's QR code with the phone. It opens the logger, which runs the whole test.
2. **Wire the mic** to the detector: SCK to D3, WS to D4, SD to D5, L/R to GND, VDD to 3V3, GND to GND.
3. **Check it works.** Turn on the hotspot and power both boards. The logger should show *gateway online*, and *last packet* should reset about once a minute as the detector checks in. In the logger's *Sound at the mic*, tap **Start this phone's mic** and set its meter once ([how](#phone-meter)). Pair the speaker, then in *Speaker test* tap **Play calibration** next to the mic. You should see an alarm, and the speaker should sound full, not thin like a phone call ([why](#phone-meter)).
4. **Lay out the field** ([where everything goes](#field-layout)). Put the detector 20 in up in its windscreen, with the phone right beside it at the same height. Put the speaker on a chair 16 ft away, facing the mic, with the gateway and its power bank on the chair too. On the phone, turn on Do Not Disturb and set Auto-Lock to Never.
5. **Calibrate the speaker** from the logger: set the volume until *Sound at the mic* reads 60–65 dB(A), then tap **Measure at the mic** ([how](#speaker-test)).
6. **Start the sweep.** Tap **Start sequence**, then walk 65 ft behind the speaker and stay quiet for about an hour. The phone records at the mic, plays every distance (about 28 minutes), records 30 minutes of background with the speaker off, and stops the recording. Then tap **Save recording**.
7. **Walk the gateway away** with the phone, stopping at 330, 660 and 1,300 ft and on. At each stop, set *Type* to *Radio walk*, enter the distance, tap **Start run**, and stop it once a packet arrives, about a minute. Turn back when none comes in two minutes.

**The result** is the logger's *Range so far* table: for each distance, whether the detector heard it, the level the phone measured at the mic, and the detector's own level. There's nothing to export: the logger saves every run online as it goes, so you can ask Claude to read the latest session from anywhere. The recording is for [training clips](#weekend-downloads).

<p><a class="btn btn-primary" href="{{ site.baseurl }}/tools/weekend/logger.html">Open the logger</a></p>

A speaker can't copy what 330 ft of real ground and wind does to the sound. A real flight checks that later, in [layer 2]({{ site.baseurl }}{% link mvp.md %}#layer-2-hear-a-drone-from-near-the-ground-t11).

## Details

<details class="layer" id="field-layout" markdown="block">
<summary><span class="layer-title">Where everything goes</span><span class="layer-sub">One phone at the mic; no house WiFi needed: the gateway joins the phone's hotspot</span></summary>

<figure class="field-layout" style="margin:12px 0 16px;max-width:420px">
<svg viewBox="0 0 360 496" width="100%" role="img" aria-labelledby="flTitle flDesc" style="color:inherit;font-family:inherit">
<title id="flTitle">Field layout for the Saturday test</title>
<desc id="flDesc">Seen from above: the detector and mic 20 inches up in a windscreen, with the phone beside it; a chair 16 feet away holding the Bluetooth speaker facing the mic, plus the gateway and its power bank; you standing quiet 65 feet or more behind the speaker. Not to scale.</desc>
<defs><marker id="flArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#c2562c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<rect x="6" y="6" width="348" height="440" rx="12" fill="#6a9a3a" fill-opacity="0.08" stroke="currentColor" stroke-opacity="0.3" stroke-dasharray="4 4"/>
<text x="20" y="32" font-size="13" fill="currentColor" fill-opacity="0.7">Grass, 16 ft or more from walls and cars</text>
<circle cx="80" cy="92" r="25" fill="#1d9e75" fill-opacity="0.18" stroke="#1d9e75"/>
<text x="80" y="97" font-size="14" font-weight="600" text-anchor="middle" fill="currentColor">Mic</text>
<rect x="118" y="68" width="30" height="48" rx="6" fill="#534ab7" fill-opacity="0.15" stroke="#534ab7"/>
<circle cx="133" cy="108" r="2.5" fill="#534ab7"/>
<text x="162" y="76" font-size="13" font-weight="600" fill="currentColor">Detector + mic</text>
<text x="162" y="93" font-size="13" fill="currentColor">20 in up, windscreen</text>
<text x="162" y="110" font-size="13" fill="currentColor">Phone beside it: the</text>
<text x="162" y="127" font-size="13" fill="currentColor">logger, meter, recorder</text>
<line x1="80" y1="222" x2="80" y2="122" stroke="#c2562c" stroke-width="1.5" marker-end="url(#flArrow)"/>
<text x="70" y="168" font-size="13" text-anchor="end" fill="currentColor">16 ft,</text>
<text x="70" y="185" font-size="13" text-anchor="end" fill="currentColor">taped</text>
<path d="M140 120 Q 190 172 132 226" fill="none" stroke="#534ab7" stroke-width="1.2" stroke-dasharray="3 3"/>
<text x="186" y="168" font-size="12" fill="currentColor" fill-opacity="0.8">Bluetooth +</text>
<text x="186" y="184" font-size="12" fill="currentColor" fill-opacity="0.8">hotspot, 16 ft</text>
<rect x="30" y="226" width="100" height="56" rx="8" fill="#c2562c" fill-opacity="0.15" stroke="#c2562c"/>
<text x="80" y="249" font-size="14" font-weight="600" text-anchor="middle" fill="currentColor">Chair</text>
<text x="80" y="268" font-size="13" text-anchor="middle" fill="currentColor">Speaker</text>
<text x="146" y="248" font-size="13" fill="currentColor">Speaker faces the mic</text>
<text x="146" y="265" font-size="13" fill="currentColor">Gateway + power bank</text>
<text x="146" y="282" font-size="13" fill="currentColor">on the chair too</text>
<line x1="80" y1="286" x2="80" y2="372" stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="2 4"/>
<text x="94" y="334" font-size="13" fill="currentColor">65 ft or more</text>
<circle cx="80" cy="390" r="9" fill="none" stroke="currentColor" stroke-width="1.4"/>
<path d="M66 428 Q80 398 94 428" fill="none" stroke="currentColor" stroke-width="1.4"/>
<text x="112" y="398" font-size="13" font-weight="600" fill="currentColor">You, quiet,</text>
<text x="112" y="415" font-size="13" fill="currentColor">behind the speaker</text>
<text x="8" y="468" font-size="12" fill="currentColor" fill-opacity="0.7">Not to scale. For the radio walk afterwards,</text>
<text x="8" y="485" font-size="12" fill="currentColor" fill-opacity="0.7">carry the gateway and the phone away together.</text>
</svg>
</figure>

- **The phone sits at the mic,** at the same height, so what it measures and records is what the detector hears. It plays to the speaker by Bluetooth from there. Bluetooth reaches about 33 ft, less through a body or a bag, so nobody stands between them.
- **Each board gets its own power bank,** since they sit 16 ft apart. If *last packet* stops resetting, the detector's power bank may have switched itself off: some do when a board draws too little. Use another one.
- **Keep the gateway within about 30 ft of the phone** all day. It reaches the logger through the phone's hotspot. The detector reaches the gateway by LoRa, which goes hundreds of yards.
- **Stay 16 ft or more from walls, cars and fences,** on grass. A hard surface behind the mic adds up to 3 dB and flatters the result.
- **Check for a cell signal** where you set up. The hotspot needs mobile data. Without it, use a laptop and the USB cable.
- **Do Not Disturb matters.** A notification plays through the speaker at test volume and gets logged as drone sound, and a call stops the audio. Airplane mode won't work, because the hotspot needs data.
- **Flash the gateway with the hotspot, not your home WiFi.** Otherwise it works in the garden and goes silent in the field. On an iPhone, switch on **Maximize Compatibility**: the board only sees 2.4 GHz.
</details>

<details class="layer" id="phone-setup" markdown="block">
<summary><span class="layer-title">Set up the phone</span><span class="layer-sub">The gateway joins your hotspot and the logger reads it through a public MQTT broker</span></summary>

1. Turn on your phone's hotspot. On an iPhone, switch on **Maximize Compatibility**: the board only sees 2.4 GHz.
2. In [the flasher]({{ site.baseurl }}/tools/flasher/), enter the hotspot's name and password. It makes up a gateway ID and fills in the broker for you. Flash both boards from the same computer, since they need the same network key.
3. Scan the flasher's QR code with the phone. It opens the logger with that gateway ID and connects.
4. Power the gateway. The chip turns to *gateway online* when the board checks in. An iPhone only shows its hotspot while the Personal Hotspot screen is open, so keep it open until then.

Readings pass through a free public broker, and the saved sessions can be read by anyone with the link: fine for a test, not for anything sensitive. Keep the screen on, since readings that arrive while it's locked are lost, and a locked phone stops its mic.

With a laptop and a cable, use **Connect USB** instead. Phones can't read a USB board from a web page. Plugging in the detector as well adds its confidence score.

The gateway hears from the detector when it alarms, when it clears, and once a minute in between. That once-a-minute check-in is what the radio walk counts. Leave **Beep on alarm** off while recording.
</details>

<details class="layer" id="phone-meter" markdown="block">
<summary><span class="layer-title">Set the phone's meter, and check the speaker</span><span class="layer-sub">Once per phone, at home; the phone is the sound meter and the recorder</span></summary>

1. **Read a steady sound with a meter app.** Pick something that doesn't change: a fan, or pink noise playing from the laptop. Hold the phone 3 ft from it and read the level in a free sound meter app, set to A-weighting. NIOSH SLM is a good one on an iPhone.
2. **Type it into the logger.** Without moving the phone or changing the sound, switch to the logger, tap **Start this phone's mic** and allow the microphone. Wait 5 s, type the app's reading and tap **Set**. The logger remembers it.
3. **Check the speaker.** Pair it, keep the mic on, and in *Speaker test* tap **Play calibration**. It should sound the same as it did with the mic off.

Phone mics differ by several dB, and every 6 dB halves or doubles the distance the speaker emulates, which is why the meter is set once. Even then, a phone is not a measuring instrument: its readings are good to a few dB, which is why the speaker test aims at 60–65 dB(A) rather than an exact figure. The recording weighs about 45 MB an hour.

**If the speaker sounds thin once the mic is on,** like a phone call, the phone has switched it into call mode, which cuts the high notes the detector listens for. Some speakers with a built-in mic do this. Use a speaker without a mic, an aux cable, or a second phone as the mic: open *Or use a second phone as the mic* under *Sound at the mic* and scan its code with the second phone, then set that phone's meter on its own page.
</details>

<details class="layer" id="speaker-test" markdown="block">
<summary><span class="layer-title">Run the speaker test</span><span class="layer-sub">Everything from the logger: the sound, the level at the mic, the plays and the recording</span></summary>

1. **Set up.** Silent mode off on the phone. Speaker on a chair 16 ft from the mic, facing it. The phone beside the mic, with its mic on.
2. **Calibrate.** In the logger's *Speaker test*, pick a sound and tap **Play calibration**. Use the volume buttons, on the phone or the speaker, until *Sound at the mic* reads 60–65 dB(A). Then tap **Measure at the mic**: the phone reads 10 s with the speaker off and 10 s of calibration, and both readings fill in. Don't touch the volume again. Without the phone's mic, type the two readings from any sound meter.
3. **Start sequence.** The logger starts the recording, plays each distance for 60 s, three times over with 20 s of quiet between, and logs every play as a *Speaker* run. The default, 80 ft to 1,000 ft, takes about 28 minutes. Then it records 30 minutes of background as a *No drone* run, with the speaker off, and stops the recording.

Each run keeps the level it aimed for, the level the phone measured and the detector's own level, so a play that came out wrong shows in the *Runs* table.

**Why not louder:** near full volume a small speaker distorts, and distortion adds the harmonics the detector listens for. The loudest step needs only 42 dB(A) at the mic.

The sounds are a DJI Mini 4 Pro and a 5-inch FPV from [batear-datasets](https://github.com/batear-io/batear-datasets) (MIT), or your own recording. Why a speaker can stand in for most distances, and what it misses: [the reasoning]({{ site.baseurl }}{% link mvp.md %}#speaker-reasoning).
</details>

<details class="layer" id="weekend-downloads" markdown="block">
<summary><span class="layer-title">Downloads and training clips</span><span class="layer-sub">The logger as one file, its sounds and the clip cutter</span></summary>

| File | What it's for | Get it |
|---|---|---|
| Logger | One file that also works offline over USB | <a href="{{ site.baseurl }}/tools/weekend/logger.html" download>logger.html</a> |
| Drone sounds | Built into the logger | <a href="{{ site.baseurl }}/tools/weekend/sounds/mini.mp3" download>mini.mp3</a> · <a href="{{ site.baseurl }}/tools/weekend/sounds/fpv.mp3" download>fpv.mp3</a> |
| Clip cutter | Fetches the saved session, lines the phone's recording up with the logger and cuts each run into labelled 1 s clips, noting whether Batear was alarming | <a href="{{ site.baseurl }}/tools/weekend/cut_clips.py" download>cut_clips.py</a> · <a href="{{ site.baseurl }}/tools/weekend/test_cut_clips.py" download>tests</a> |

Optional, afterwards (Python 3.11+, and [ffmpeg](https://ffmpeg.org/) for a phone's `.m4a`):

```bash
python cut_clips.py --session latest --recording S20261025-1003-mic.m4a --mic --tag mic05 --rate 16000 --out clips
```

`--mic` uses the start time the phone logged, good to a few tenths of a second, which is fine for 1 s clips. For a recording made any other way, clap next to it while tapping **Sync clap** and use `--sync`.

Hold out whole runs for testing, never clips from a run you trained on.
</details>
