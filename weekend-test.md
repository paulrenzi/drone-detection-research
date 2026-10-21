---
title: Saturday test
nav_primary: 4
---

# The Saturday test
{: .no_toc }

**One day, about $80–90, and no drone.** How far does a mic 20 in off the ground hear a drone, and how far can its alarm travel by radio? A Bluetooth speaker plays a recorded drone at the level it would reach the mic from 80 to 1,000 ft.

**Pass:** heard at 330 ft. **Fail:** under 200 ft.

**You need:** the two XIAO ESP32S3 + Wio-SX1262 kits with their antennas (one becomes the detector, the other the gateway), a USB-C data cable, a laptop with Chrome, an INMP441 mic with jumper wires (its pins need soldering), two fur windscreens, a Bluetooth speaker, two phones with mobile data (an old one will do for the mic phone) and a free sound meter app on either (NIOSH SLM on an iPhone), two power banks and a tape measure ([kit and prices]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector)).

## The steps

Do steps 1–3 at home the day before.

1. **Flash both boards** from [our flasher]({{ site.baseurl }}/tools/flasher/), antennas on: the *detector*, then the *gateway* with the hotspot of the phone you'll carry, the *logger phone* ([how](#phone-setup)). This replaces the Meshtastic firmware they came with. Then scan the flasher's QR code with the logger phone. It opens the logger, which runs the whole test.
2. **Wire the mic** to the detector: SCK to D3, WS to D4, SD to D5, L/R to GND, VDD to 3V3, GND to GND.
3. **Check it works.** Turn on the logger phone's hotspot and power both boards. The logger should show *gateway online*, and *last packet* should reset about once a minute as the detector checks in. In the logger's *Sound at the mic*, scan the code under *Set up the mic phone* with the other phone, tap **Start the mic** on it, and set its meter once ([how](#phone-meter)). Pair the speaker with the mic phone, then tap **Play calibration** in the logger's *Speaker test*, with the speaker next to the mic. You should see an alarm, and the speaker should sound full, not thin like a phone call ([why](#phone-meter)).
4. **Lay out the field** ([where everything goes](#field-layout)). The test has two ends. The *sound end* stays put: the detector 20 in up in its windscreen, the mic phone right beside it at the same height, and the speaker on a chair 16 ft away, facing the mic. The *receiving end* is you, carrying the logger phone and the gateway with its power bank. On both phones, turn on Do Not Disturb and set Auto-Lock to Never.
5. **Calibrate the speaker** from the logger: set the volume on the mic phone or the speaker until *Sound at the mic* reads 60–65 dB(A), then tap **Measure at the mic** ([how](#speaker-test)).
6. **Start the sweep.** Tap **Start sequence**, then walk 65 ft or more behind the speaker with the logger phone and the gateway, and stay quiet for about 10 minutes. You have 60 s before the first play; you'll hear it start. The mic phone records at the mic, plays each distance once (about 5 minutes), records 4 minutes of background with the speaker off, and stops the recording. The logger shows the countdown, the sound at the mic and each alarm as it arrives. Then walk back and tap **Save recording** on the mic phone.
7. **Walk the gateway away** from the detector, with the logger phone, stopping at 330, 660 and 1,300 ft and on. At each stop, set *Type* to *Radio walk*, enter the distance, tap **Start run**, and stop it once a packet arrives, about a minute. Turn back when none comes in two minutes. The sound end hasn't moved, so at any stop you can also tap **Start sequence** again and see real alarms arrive from that far.

**The result** is the logger's *Range so far* table: for each distance, whether the detector heard it, the level the phone measured at the mic, and the detector's own level. There's nothing to export: the logger saves every run online as it goes, so you can ask Claude to read the latest session from anywhere. The recording is for [training clips](#weekend-downloads).

<p><a class="btn btn-primary" href="{{ site.baseurl }}/tools/weekend/logger.html">Open the logger</a></p>

A speaker can't copy what 330 ft of real ground and wind does to the sound. A real flight checks that later, in [layer 2]({{ site.baseurl }}{% link mvp.md %}#layer-2-hear-a-drone-from-near-the-ground-t11).

## Details

<details class="layer" id="field-layout" markdown="block">
<summary><span class="layer-title">Where everything goes</span><span class="layer-sub">Two ends: the sound end stays put, and the receiving end goes wherever you go</span></summary>

The test uses two boards and two phones:

- **Board 1, the detector,** has the mic. It decides whether it hears a drone and sends each alarm by LoRa radio.
- **The mic phone** sits beside the mic. It measures and records the sound there, and plays the test sound to the speaker by Bluetooth.
- **Board 2, the gateway,** has no mic. It receives the detector's radio messages and passes them to the logger phone over its hotspot.
- **The logger phone** runs the logger and the hotspot, and tells the mic phone what to play and when.

So the test has two ends. The **sound end** (board 1, the mic, the mic phone and the speaker) never moves. The **receiving end** (board 2 and the logger phone) is you, and goes wherever you go. The only link between the ends is the one under test, LoRa; the two phones keep in touch over mobile data. A real system is the same chain: one gateway listening to detectors spread across a field.

<figure class="field-layout" style="margin:12px 0 16px;max-width:420px">
<svg viewBox="0 0 360 536" width="100%" role="img" aria-labelledby="flTitle flDesc" style="color:inherit;font-family:inherit">
<title id="flTitle">Field layout for the Saturday test</title>
<desc id="flDesc">Seen from above. The sound end: board 1, the detector, wired to the mic 20 inches up, with the mic phone beside it, and the Bluetooth speaker on a chair 16 feet away, facing the mic. The mic phone plays the speaker by Bluetooth. The receiving end: you, 65 feet or more behind the speaker, carrying board 2, the gateway, with its power bank, and the logger phone, whose hotspot the gateway joins by WiFi. The detector reaches the gateway by LoRa radio. Not to scale.</desc>
<rect x="6" y="6" width="348" height="480" rx="12" fill="#6a9a3a" fill-opacity="0.08" stroke="currentColor" stroke-opacity="0.3" stroke-dasharray="4 4"/>
<text x="20" y="32" font-size="13" fill="currentColor" fill-opacity="0.7">Grass, 16 ft or more from walls and cars</text>
<text x="20" y="56" font-size="12" font-weight="600" fill="currentColor" fill-opacity="0.7">SOUND END: STAYS PUT</text>
<line x1="48" y1="84" x2="48" y2="66" stroke="#534ab7" stroke-width="1.6"/>
<rect x="18" y="84" width="36" height="36" rx="5" fill="#534ab7" fill-opacity="0.15" stroke="#534ab7"/>
<text x="36" y="108" font-size="16" font-weight="700" text-anchor="middle" fill="#534ab7">1</text>
<line x1="54" y1="102" x2="64" y2="102" stroke="#1d9e75" stroke-width="1.6"/>
<circle cx="80" cy="102" r="16" fill="#1d9e75" fill-opacity="0.18" stroke="#1d9e75"/>
<text x="80" y="106" font-size="11" font-weight="600" text-anchor="middle" fill="currentColor">Mic</text>
<rect x="110" y="80" width="24" height="44" rx="5" fill="none" stroke="currentColor" stroke-width="1.4"/>
<line x1="118" y1="118" x2="126" y2="118" stroke="currentColor" stroke-width="1.4"/>
<text x="160" y="80" font-size="13" font-weight="600" fill="#534ab7">Board 1: detector</text>
<text x="160" y="97" font-size="13" fill="currentColor">wired to the mic, 20 in up</text>
<text x="160" y="118" font-size="13" font-weight="600" fill="currentColor">Mic phone, beside it</text>
<text x="160" y="135" font-size="13" fill="currentColor">meter, recorder, player</text>
<line x1="122" y1="126" x2="125" y2="250" stroke="#c2562c" stroke-width="1.6" stroke-dasharray="1 4" stroke-linecap="round"/>
<line x1="36" y1="122" x2="36" y2="410" stroke="#534ab7" stroke-width="1.6" stroke-dasharray="6 4"/>
<line x1="160" y1="170" x2="184" y2="170" stroke="#534ab7" stroke-width="1.6" stroke-dasharray="6 4"/>
<text x="190" y="174" font-size="12" fill="currentColor">LoRa: board 1 to 2</text>
<line x1="160" y1="190" x2="184" y2="190" stroke="#c2562c" stroke-width="1.6" stroke-dasharray="1 4" stroke-linecap="round"/>
<text x="190" y="194" font-size="12" fill="currentColor">Bluetooth: to speaker</text>
<line x1="160" y1="210" x2="184" y2="210" stroke="#1a7fa8" stroke-width="1.6" stroke-dasharray="2 3"/>
<text x="190" y="214" font-size="12" fill="currentColor">WiFi: board 2 to logger</text>
<rect x="90" y="250" width="70" height="46" rx="8" fill="#c2562c" fill-opacity="0.1" stroke="#c2562c"/>
<rect x="105" y="256" width="40" height="34" rx="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
<circle cx="125" cy="273" r="9" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="172" y="268" font-size="13" font-weight="600" fill="#c2562c">Chair, 16 ft from the mic</text>
<text x="172" y="285" font-size="13" fill="currentColor">Speaker, facing the mic</text>
<line x1="125" y1="298" x2="125" y2="384" stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="2 4"/>
<text x="138" y="346" font-size="13" fill="currentColor">65 ft or more</text>
<text x="50" y="380" font-size="12" font-weight="600" fill="currentColor" fill-opacity="0.7">RECEIVING END: MOVES WITH YOU</text>
<rect x="10" y="390" width="340" height="86" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-opacity="0.5"/>
<line x1="48" y1="414" x2="48" y2="398" stroke="#534ab7" stroke-width="1.6"/>
<rect x="18" y="414" width="36" height="36" rx="5" fill="#534ab7" fill-opacity="0.15" stroke="#534ab7"/>
<text x="36" y="438" font-size="16" font-weight="700" text-anchor="middle" fill="#534ab7">2</text>
<rect x="60" y="420" width="16" height="24" rx="3" fill="none" stroke="currentColor" stroke-opacity="0.6"/>
<line x1="78" y1="432" x2="98" y2="432" stroke="#1a7fa8" stroke-width="1.6" stroke-dasharray="2 3"/>
<rect x="100" y="410" width="24" height="44" rx="5" fill="none" stroke="currentColor" stroke-width="1.4"/>
<line x1="108" y1="448" x2="116" y2="448" stroke="currentColor" stroke-width="1.4"/>
<text x="140" y="412" font-size="13" font-weight="600" fill="currentColor">You, quiet, carrying</text>
<text x="140" y="430" font-size="13" font-weight="600" fill="#534ab7">Board 2: gateway</text>
<text x="140" y="447" font-size="13" fill="currentColor">and its power bank</text>
<text x="140" y="465" font-size="13" font-weight="600" fill="currentColor">Logger phone: hotspot</text>
<text x="8" y="508" font-size="12" fill="currentColor" fill-opacity="0.7">Not to scale. The two phones keep in touch by mobile</text>
<text x="8" y="525" font-size="12" fill="currentColor" fill-opacity="0.7">data. On the radio walk, only the receiving end moves.</text>
</svg>
</figure>

- **The mic phone sits at the mic,** at the same height, so what it measures and records is what the detector hears. It plays to the speaker by Bluetooth, which reaches about 33 ft, less through a body or a bag, so nobody stands between them.
- **Carry the gateway with the logger phone.** It talks to the phone by WiFi, and a phone hotspot reaches about 30 ft, so keep them together: a pocket each is fine. The detector reaches the gateway by LoRa, which goes hundreds of yards; the radio walk measures how far.
- **Each board gets its own power bank.** If *last packet* stops resetting, the detector's power bank may have switched itself off: some do when a board draws too little. Use another one.
- **Stay 16 ft or more from walls, cars and fences,** on grass. A hard surface behind the mic adds up to 3 dB and flatters the result.
- **Check for a cell signal** where you set up. Both phones need mobile data: the hotspot needs it, and the mic phone reaches the logger over the internet. Give the mic phone its own data, not the hotspot, which won't reach it once you walk away.
- **Do Not Disturb matters, on both phones.** A notification on the mic phone plays through the speaker at test volume and gets logged as drone sound, and a call stops the audio. Airplane mode won't work, because both phones need data.
- **Flash the gateway with the hotspot, not your home WiFi.** Otherwise it works in the garden and goes silent in the field. On an iPhone, switch on **Maximize Compatibility**: the board only sees 2.4 GHz.
</details>

<details class="layer" id="phone-setup" markdown="block">
<summary><span class="layer-title">Set up the phones</span><span class="layer-sub">The gateway joins the logger phone's hotspot, and both phones meet through a public MQTT broker</span></summary>

1. Turn on the logger phone's hotspot. On an iPhone, switch on **Maximize Compatibility**: the board only sees 2.4 GHz.
2. In [the flasher]({{ site.baseurl }}/tools/flasher/), enter the hotspot's name and password. It makes up a gateway ID and fills in the broker for you. Flash both boards from the same computer, since they need the same network key.
3. Scan the flasher's QR code with the logger phone. It opens the logger with that gateway ID and connects.
4. Power the gateway. The chip turns to *gateway online* when the board checks in. An iPhone only shows its hotspot while the Personal Hotspot screen is open, so keep it open until then.
5. In the logger's *Sound at the mic*, scan the code under *Set up the mic phone* with the other phone, on its own mobile data. Tap **Start the mic** on it and allow the microphone. That tap also lets it play the speaker. *Sound at the mic* in the logger then shows *live* under *mic phone*.

Readings pass through a free public broker, and the saved sessions can be read by anyone with the link: fine for a test, not for anything sensitive. Keep both screens on, since readings that arrive while the logger is locked are lost, and a locked mic phone stops its mic and the speaker.

**Only one phone?** Tap *Only one phone: use this phone's mic* instead. It works, but that phone has to stay at the mic and play the speaker, and the gateway has to stay within 30 ft of it, so the radio walk can't happen while the speaker plays.

With a laptop and a cable, use **Connect USB** instead. Phones can't read a USB board from a web page. Plugging in the detector as well adds its confidence score.

The gateway hears from the detector when it alarms, when it clears, and once a minute in between. That once-a-minute check-in is what the radio walk counts. Leave **Beep on alarm** off while recording.
</details>

<details class="layer" id="phone-meter" markdown="block">
<summary><span class="layer-title">Set the phone's meter, and check the speaker</span><span class="layer-sub">Once, at home; the mic phone is the sound meter and the recorder</span></summary>

1. **Read a steady sound with a meter app.** Pick something that doesn't change: a fan, or pink noise playing from the laptop. Hold the mic phone 3 ft from it and read the level in a free sound meter app, set to A-weighting, on the mic phone or on the other phone held right beside it. NIOSH SLM is a good one on an iPhone.
2. **Type it into the mic phone.** Without moving the phone or changing the sound, open the mic phone's page and tap **Start the mic**. Wait 5 s, type the app's reading under *Set this phone's meter* and tap **Set**. The phone remembers it.
3. **Check the speaker.** Pair it with the mic phone, keep the mic on, and in the logger's *Speaker test* tap **Play calibration**. It should sound the same as it did with the mic off.

Phone mics differ by several dB, and every 6 dB halves or doubles the distance the speaker emulates, which is why the meter is set once. Even then, a phone is not a measuring instrument: its readings are good to a few dB, which is why the speaker test aims at 60–65 dB(A) rather than an exact figure. The recording weighs about 45 MB an hour.

**If the speaker sounds thin once the mic is on,** like a phone call, the phone has switched it into call mode, which cuts the high notes the detector listens for. Some speakers with a built-in mic do this. Use a speaker without a mic, or an aux cable from the mic phone.
</details>

<details class="layer" id="speaker-test" markdown="block">
<summary><span class="layer-title">Run the speaker test</span><span class="layer-sub">Run from the logger phone; the mic phone plays the sound, measures it and records it</span></summary>

1. **Set up.** Silent mode off on the mic phone, and the speaker paired with it. Speaker on a chair 16 ft from the mic, facing it. The mic phone beside the mic, with its mic on.
2. **Calibrate.** In the logger's *Speaker test*, pick a sound and tap **Play calibration**. Use the volume buttons, on the mic phone or the speaker, until *Sound at the mic* reads 60–65 dB(A). Then tap **Measure at the mic**: the mic phone reads 10 s with the speaker off and 10 s of calibration, and both readings fill in. Don't touch the volume again. Without the mic phone, type the two readings from any sound meter.
3. **Start sequence.** The logger sends the whole sequence to the mic phone, which waits 60 s while you walk away (*Walk away, s*), then starts the recording, plays each distance once for 30 s with 10 s of quiet between, records 4 minutes of background with the speaker off, and stops the recording: about 10 minutes in all. The default, 80 ft to 1,000 ft, takes about 5 minutes of plays. The logger logs every play as a *Speaker* run and the background as a *No drone* run. The mic phone keeps its own time, so the sequence carries on if the logger phone loses signal. For a second pass, run it again, or raise *Plays each*.

Each run keeps the level it aimed for, the level the mic phone measured and the detector's own level, so a play that came out wrong shows in the *Runs* table.

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
