---
title: Saturday test
nav_primary: 4
---

# The Saturday test
{: .no_toc }

**One day, about $80–90, and no drone.** How far does a mic half a metre off the ground hear a drone, and how far can its alarm travel by radio? A Bluetooth speaker plays a recorded drone at the level it would reach the mic from 25 to 300 m.

**Pass:** heard at 100 m. **Fail:** under 60 m.

**You need:** the two XIAO ESP32S3 + Wio-SX1262 kits with their antennas, a USB-C data cable, a laptop with Chrome, an INMP441 mic with jumper wires (its pins need soldering), two fur windscreens, a Bluetooth speaker, two phones, two power banks and a tape measure ([kit and prices]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector)).

## The steps

Do steps 1–3 at home the day before.

1. **Flash both boards** from [our flasher]({{ site.baseurl }}/tools/flasher/), antennas on: the *detector*, then the *gateway* with your phone's hotspot ([how](#phone-setup)). This replaces the Meshtastic firmware they came with. Then scan the flasher's QR code with the logger phone, and the code under the logger's *Sound at the mic* with the second phone. The second phone becomes the **mic phone**: the sound meter and recorder, run from the logger.
2. **Wire the mic** to the detector: SCK to D3, WS to D4, SD to D5, L/R to GND, VDD to 3V3, GND to GND.
3. **Check it works.** Turn on the hotspot and power both boards. The logger should show *gateway online*, and *last packet* should reset about once a minute as the detector checks in. Pair the speaker, then in the logger's *Speaker test* tap **Play calibration** next to the mic. You should see an alarm. On the mic phone, tap **Start the mic** and set its meter once ([how](#mic-phone)).
4. **Lay out the field** ([where everything goes](#field-layout)). Put the detector and the mic phone side by side, 0.5 m up, in windscreens. Put the speaker on a chair 5 m away, with the logger phone and gateway on the chair too. On the logger phone, turn on Do Not Disturb and set Auto-Lock to Never.
5. **Calibrate the speaker** from the logger: set the volume until *Sound at the mic* reads 60–65 dB(A), then tap **Measure at the mic** ([how](#speaker-test)).
6. **Start the sweep.** Tap **Start sequence**, then walk 20 m behind the speaker and stay quiet for about an hour. The logger starts the mic phone recording, plays every distance (about 28 minutes), records 30 minutes of background with the speaker off, and stops the recording. Then tap **Save recording** on the mic phone.
7. **Walk the gateway away** with the logger phone, stopping at 100, 200 and 400 m and on. At each stop, set *Type* to *Radio walk*, enter the distance, tap **Start run**, and stop it once a packet arrives, about a minute. Turn back when none comes in two minutes.

**The result** is the logger's *Range so far* table: for each distance, whether the detector heard it, the level the mic phone measured, and the detector's own level. There's nothing to export: the logger saves every run online as it goes, so you can ask Claude to read the latest session from anywhere. The mic phone's recording is for [training clips](#weekend-downloads).

<p><a class="btn btn-primary" href="{{ site.baseurl }}/tools/weekend/logger.html">Open the logger</a> <a class="btn" href="{{ site.baseurl }}/tools/weekend/logger.html?demo=1">Try it with demo data</a></p>

A speaker can't copy what 100 m of real ground and wind does to the sound. A real flight checks that later, in [layer 2]({{ site.baseurl }}{% link mvp.md %}#layer-2-hear-a-drone-from-near-the-ground-t11).

## Details

<details class="layer" id="field-layout" markdown="block">
<summary><span class="layer-title">Where everything goes</span><span class="layer-sub">No house WiFi needed: the gateway joins the logger phone's hotspot</span></summary>

```
mic + detector, 0.5 m up
        mic phone beside it: meter and recorder
        │
        │  5 m, measured with a tape
        │
chair:  speaker, facing the mic
        logger phone + gateway + its power bank
        │
        │  20 m or more
        │
you, quiet, behind the speaker
```

- **Each board gets its own power bank,** since they sit 5 m apart. If *last packet* stops resetting, the detector's power bank may have switched itself off: some do when a board draws too little. Use another one.
- **Keep the gateway within a few metres of the logger phone** all day. It reaches the logger through the phone's hotspot. The detector reaches the gateway by LoRa, which goes hundreds of metres.
- **The mic phone needs mobile data** to reach the logger, like the hotspot. Keep its screen on.
- **Keep the logger phone beside the speaker.** Bluetooth only reaches about 10 m, less through a body or a bag. The sequence runs on its own, so nobody needs to hold the phone.
- **Stay 5 m or more from walls, cars and fences,** on grass. A hard surface behind the mic adds up to 3 dB and flatters the result.
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

Readings pass through a free public broker, and the saved sessions can be read by anyone with the link: fine for a test, not for anything sensitive. Keep the screen on, since readings that arrive while it's locked are lost.

With a laptop and a cable, use **Connect USB** instead. Phones can't read a USB board from a web page. Plugging in the detector as well adds its confidence score.

The gateway hears from the detector when it alarms, when it clears, and once a minute in between. That once-a-minute check-in is what the radio walk counts. Leave **Beep on alarm** off while recording.
</details>

<details class="layer" id="mic-phone" markdown="block">
<summary><span class="layer-title">Set up the mic phone</span><span class="layer-sub">The second phone is the sound meter and the recorder; the logger runs it</span></summary>

1. On the logger, open *Sound at the mic* and scan its code with the second phone. It opens the logger's mic page for the same gateway ID.
2. Tap **Start the mic** and allow the microphone.
3. **Set its meter, once per phone.** Phone microphones differ by several dB, and every 6 dB halves or doubles the distance the speaker emulates. Play a steady sound (the logger's calibration will do) and hold another phone running a free sound meter app, set to A-weighting, right beside the mic phone. The logger phone will do. Enter the meter's reading and tap **Set**. The page remembers it. Don't switch apps on the mic phone itself: that stops its mic.

The mic phone sends one reading a second to the logger and records when the logger tells it to. After the sweep, tap **Save recording** to keep the file. It weighs about 45 MB an hour. The phone's mic is not a measuring instrument: its readings are good to a few dB, which is why the speaker test aims at 60–65 dB(A) rather than an exact figure.
</details>

<details class="layer" id="speaker-test" markdown="block">
<summary><span class="layer-title">Run the speaker test</span><span class="layer-sub">Everything from the logger: the sound, the level at the mic, the plays and the recording</span></summary>

1. **Set up.** Silent mode off on the logger phone. Speaker on a chair 5 m from the mic, facing it, with the logger phone beside it. The mic phone beside the mic.
2. **Calibrate.** In the logger's *Speaker test*, pick a sound and tap **Play calibration**. Use the volume buttons, on the phone or the speaker, until *Sound at the mic* reads 60–65 dB(A). Then tap **Measure at the mic**: the mic phone reads 10 s with the speaker off and 10 s of calibration, and both readings fill in. Don't touch the volume again. Without a mic phone, type the two readings from any sound meter.
3. **Start sequence.** The logger starts the mic phone recording, plays each distance for 60 s, three times over with 20 s of quiet between, and logs every play as a *Speaker* run. The default, 25 m to 300 m, takes about 28 minutes. Then it records 30 minutes of background as a *No drone* run, with the speaker off, and stops the recording.

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
| Clip cutter | Fetches the saved session, lines the mic phone's recording up with the logger and cuts each run into labelled 1 s clips, noting whether Batear was alarming | <a href="{{ site.baseurl }}/tools/weekend/cut_clips.py" download>cut_clips.py</a> · <a href="{{ site.baseurl }}/tools/weekend/test_cut_clips.py" download>tests</a> |

Optional, afterwards (Python 3.11+, and [ffmpeg](https://ffmpeg.org/) for a phone's `.m4a`):

```bash
python cut_clips.py --session latest --recording S20261025-1003-mic.m4a --mic --tag mic05 --rate 16000 --out clips
```

`--mic` uses the start time the mic phone logged, good to a few tenths of a second, which is fine for 1 s clips. For a recording made any other way, clap next to it while tapping **Sync clap** and use `--sync`.

Hold out whole runs for testing, never clips from a run you trained on.
</details>

{: .note }
> The tools are tested on demo data and synthetic audio, not yet on a real board.
