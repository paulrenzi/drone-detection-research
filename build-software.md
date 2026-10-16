---
title: "Build: software"
nav_order: 1.7
---

# Build: software, from listener to dugout
{: .no_toc }

The six programs the [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}) needs, the interfaces between them, and how much of each [Batear]({{ site.baseurl }}{% link research/open-source-builds.md %}#batear) (MIT licence) already covers. Hardware: [Build: hardware]({{ site.baseurl }}{% link build-hardware.md %}).

{: .warning }
> **A design, not code.** Nothing here is written or tested yet. Batear's behaviour was read from its source and docs on 2026-10-15 (last push 2026-10-06). Every byte count and timing below is a proposal or an estimate unless a source is linked.

1. TOC
{:toc}

## Short answer

- **Six components.** Listener firmware, edge receiver firmware, dugout display, mission tooling, classifier pipeline, test harness.
- **Batear covers about half of the two firmwares.** It has the audio front end, a harmonic detector, LoRa transmit and receive, encryption, battery reads and a receive-only gateway. It lacks wake-on-sound, relaying, a wired output, line awareness, and a nonce scheme that is safe with more than one detector (below).
- **Batear covers none of the other four.** Mission tooling and the display are new. The classifier pipeline and test harness reuse public datasets and ArduPilot's simulator.
- **One interface carries the design:** the alert packet. Its contents fix what the display can show, what relays must do, and how many bytes each alert costs on air.
- **Order:** fork Batear for layers 1–3 of the [MVP]({{ site.baseurl }}{% link mvp.md %}), fix its nonce, add the RS-485 output, then add relaying and wake-on-sound for layers 4–5. Mission tooling waits for T13.

## The chain

```
 PLAN (laptop)                 FIELD                                   UNIT
 ─────────────                 ─────                                   ────
 line.geojson ──► lay_line ──► mission.waypoints ──► ArduPilot drone
                    │                                   │ drops, logs release points
                    │          drop log (.bin) ◄────────┘
                    ▼
               listeners.json ─────────────────────────────────────► dugout display
               (id → position)                                            ▲
                                                                          │ RS-485
 listener ──LoRa──► listener ──LoRa──► … ──LoRa──► edge receiver ─────────┘
 (hears, alerts)   (relays once)                 (never transmits)
```

## Components and what Batear covers

| # | Component | Runs on | In → out | Batear covers | New work |
|---|---|---|---|---|---|
| 1 | **Listener firmware** | ESP32-S3 + SX1262 (Heltec V3 now, custom board later) | sound → alert packet; neighbours' packets → one relay | I²S mic, 1024-point FFT harmonic detector, hysteresis, AES-128-GCM packet, battery read, heartbeat ([source](https://github.com/batear-io/batear/blob/main/docs/architecture.md)) | Wake-on-sound sleep, learned classifier stage, relay with dedup, temperature, safe nonce, check-in at most 1–2 a day |
| 2 | **Edge receiver firmware** | Same board, radio in receive only | LoRa packets → RS-485 frames | LoRa receive, decrypt, per-device replay check. Its gateway already never transmits on LoRa: no ACKs, by design ([protocol](https://github.com/batear-io/batear/blob/main/docs/protocol.md)) | Wi-Fi and MQTT off and compiled out, RS-485 output, RSSI/SNR per packet, a reboot-safe replay check |
| 3 | **Dugout display** | Phone or tablet over a USB–RS-485 adapter, or a laptop | frames + `listeners.json` → map, alarm, line health | Nothing (Batear goes to Home Assistant) | All |
| 4 | **Mission tooling** (`lay_line`) | Laptop, Python | planned line → ArduPilot mission; flight log → `listeners.json` | Nothing | All |
| 5 | **Classifier pipeline** | Laptop or cloud GPU, offline | labelled audio → model file baked into the next batch's firmware | Its SD-card alarm recordings collect field audio ([config](https://github.com/batear-io/batear/blob/main/docs/configuration.md)) | Dataset assembly, training, on-device export, scoring against Batear's detector |
| 6 | **Test harness** | Laptop + bench boards + SDR | recorded audio, simulated flights → pass/fail | Nothing | SITL drop missions, audio replay into a listener, RF silence check |

Owner for all six: us. ArduPilot, pymavlink and the public datasets are upstream dependencies, not components.

## Interfaces

### I1. The alert packet (listener → air)

Keep Batear's envelope: **36 bytes on air**, `[4 B nonce][16 B ciphertext][16 B GCM tag]`, about 0.5 s at SF10/BW125 ([Batear protocol](https://github.com/batear-io/batear/blob/main/docs/protocol.md)). Replace its 16-byte plaintext, which spends 7 bytes on firmware version, uptime and free heap, with fields the line uses:

| Bytes | Field | Notes |
|---|---|---|
| 2 | `listener_id` | 0–65,535. Batear's 1-byte ID caps a network at 256, too few once lines from many units share a map |
| 1 | `type` | ALARM, CLEAR, CHECKIN |
| 2 | `age_ds` | Tenths of a second since the sound began, **updated by each relay**. Replaces clock sync (below) |
| 1 | `hops` | Incremented by each relay |
| 1 | `f0_bin` | Main tone, as Batear |
| 1 | `rms_db` | Loudness, as Batear |
| 1 | `conf` | Classifier confidence, 0–255 |
| 1 | `dur_s` | How long the sound lasted, for CLEAR |
| 1 | `vbat_cv` | As Batear: V = 2.50 + 0.01 × value |
| 1 | `temp_c` | Chip temperature + 40 |
| 1 | `rssi_hint` | Weakest link RSSI on the way in, for line health |
| 3 | spare | Classifier version, flags |

**Why age, not clocks:** a relay already decrypts the packet to check it, so it can add its own holding time to `age_ds` and re-encrypt. The receiver then dates the sound as *arrival time − age − airtime × (hops + 1)*. Airtime is fixed for a fixed spreading factor. That gives each crossing a time good to well under a second without any listener knowing the time of day. The 1–2 s neighbour-sync problem in [T15]({{ site.baseurl }}{% link models/tripwire.md %}#what-has-to-be-proven) goes away for line-order direction (an inference, to be checked on the bench).

### I1a. The nonce: a defect in Batear to fix first

Batear builds the 12-byte GCM IV from the first 8 bytes of the network key plus a packet counter ([`lora_crypto.h` L79–95](https://github.com/batear-io/batear/blob/main/main/lora_crypto.h)). That counter is a `uint16_t` that starts at 0 on every boot ([`lora_task.cpp` L80, L290](https://github.com/batear-io/batear/blob/main/main/lora_task.cpp)), and every detector shares the key. So:

- **Two detectors reuse the same IV under the same key.** Detector 1's packet 5 and detector 2's packet 5 are encrypted identically. In GCM, a reused nonce leaks the XOR of the two plaintexts and lets an attacker who collects such pairs recover the authentication key and forge packets ([NIST SP 800-38D §8](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf) requires unique IVs per key).
- **A reboot silences a detector.** The gateway drops any packet whose counter is at or below the last one it saw from that device ([`gateway_task.cpp` L246](https://github.com/batear-io/batear/blob/main/main/gateway_task.cpp)). After a detector reboots, every alert is rejected as a replay until the counter climbs past the old value. The same happens when the counter wraps at 65,536.

**Fix:** IV = `listener_id` (2 B) + boot count stored in flash (2 B) + 32-bit packet counter (4 B), with 4 B of key prefix. On air the nonce grows from 4 to 8 bytes, so a packet is 40 bytes. The receiver keys its replay check on (`listener_id`, boot, counter). A relay re-encrypts under **its own** ID and counter, so relays never reuse an IV either. Worth offering upstream as a pull request.

### I2. Relay rules (listener → listener)

Managed flooding with duplicate suppression, the scheme Meshtastic uses ([Meshtastic docs](https://meshtastic.org/docs/overview/mesh-algo/)), cut down:

1. **Listen in short windows only.** A sleeping listener can't hear neighbours. It wakes the radio in receive mode briefly on a fixed cycle, using LoRa channel-activity detection ([Semtech AN1200.85](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262)), so an alert is preceded by a preamble long enough to span one cycle. Cycle and preamble length trade battery against delay; T12 sizes them.
2. **Relay each (origin, boot, counter) once.** Keep the last 32 seen in RAM.
3. **Wait 100–600 ms at random before relaying.** If a neighbour relays the same alert first and it was heard louder than ours would be, stay quiet.
4. **No hop limit is needed** on a line of 12–30, since each listener relays each alert once. Cap `hops` at 15 anyway.
5. **CHECKIN packets are not relayed by default**, so a quiet line stays quiet. The unit can turn relaying on for one day's check-in to get a health map.

### I3. RS-485 frame (edge receiver → dugout)

One line of ASCII per received packet at 9,600 baud, so any serial terminal can read it if the display fails:

```
$TW,<listener_id>,<type>,<age_ds>,<hops>,<f0_bin>,<rms_db>,<conf>,<vbat_cv>,<temp_c>,<rssi>,<snr>,<rx_id>*<crc8>
```

`rx_id` names which edge receiver heard it, since several share one wire ([design]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees)). Receivers on a shared pair answer only when polled by the display, which avoids collisions on the wire and keeps the dugout the only master. The receiver decrypts, so it holds the key; the dugout needs none.

### I4. `listeners.json` (mission tooling → display)

```json
{"line": "A", "laid": "2026-11-02T03:10Z", "sortie": 4,
 "listeners": [{"id": 1031, "planned": [48.512, 37.991],
                "released": [48.5122, 37.9913], "fix": "3D", "hdop": 0.9}]}
```

`released` comes from the drone's log at the moment the servo moved. If the log shows no GPS fix there, `released` is the dead-reckoned estimate and `fix` says so. The display draws an error circle from it.

### I5. Mission file (mission tooling → drone)

Standard QGroundControl plain-text waypoint format, loaded with MAVProxy or pymavlink ([format](https://mavlink.io/en/file_formats/)). The file's first line is `QGC WPL 110`, then one tab-separated line per item: index, current, frame, command, params 1–4, lat, lon, alt, autocontinue. Per listener: `NAV_WAYPOINT` (16) to the drop point at drop height, with param 1 = 2 s hold to settle; `DO_SET_SERVO` (183) with param 1 = the output number and param 2 = the release PWM in µs; then the next waypoint. `RETURN_TO_LAUNCH` (20) at the end ([ArduPilot mission commands](https://ardupilot.org/copter/docs/common-mavlink-mission-command-messages-mav_cmd.html)).

On a Pixhawk 6C, the [v2 harness]({{ site.baseurl }}{% link build-hardware.md %}#1-v2-one-rod-one-servo) uses **AUX 1** only, with `SERVO9_FUNCTION = 0`: each drop is a `DO_SET_SERVO` to that dart's step on the rotor, so the PWM rises by one step per listener. ArduPilot needs an unassigned output for `DO_SET_SERVO`, and advises against servos on the 400 Hz MAIN outputs ([ArduPilot servo docs](https://ardupilot.org/copter/docs/common-servo.html)). The v1 harness used AUX 1–4, one servo per dart, so a stuck servo cost one listener. With v2, a jammed rotor keeps the rest of the sortie's darts on board.

## The components in detail

### 1. Listener firmware

**States:** `ARMED-WAIT` → `SLEEP` ⇄ `LISTEN` → `CLASSIFY` → `ALARM` → `CLEAR` → `SLEEP`.

- **`ARMED-WAIT`.** Loaded into the harness powered on, the listener stays silent for a set time (default 10 minutes) so it can't transmit from the drone or over the unit's position. It then counts its boot and starts.
- **`SLEEP`.** The processor and radio are off except for the wake source and the relay receive windows (I2). The wake source is the main open choice:

The digital mic can't be the wake source by itself: in deep sleep the ESP32-S3 powers down its I²S block, and its low-power coprocessor can poll only the ADC, touch pins and GPIO ([Espressif sleep modes](https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32s3/api-reference/system/sleep_modes.html)).

| Wake source | How | Cost | Risk |
|---|---|---|---|
| **A. Duty-cycled FFT** | Wake from deep sleep every 1–2 s, start I²S, sample 64 ms, run Batear's harmonic test, sleep | No extra parts | A drone is audible for tens of seconds, so a look every 2 s should catch most crossings (estimate). Average current is set by wake-up overhead |
| **B. Analog energy gate** | An analog mic, a band-pass (150–3,000 Hz) and a comparator on an RTC GPIO wake the processor | ~$1–2 | Wind trips it; needs filtering |
| **C. Wake-on-sound MEMS mic** | Vesper VM1010: about 10 µA in wake-on-sound mode, raising a pin on sound ([datasheet](https://www.mouser.com/datasheet/2/960/vesper_tech_06182019_VM1010-1605563.pdf)) | ~$2–5 | Single source |

Start with **A**, because it needs no hardware change and T12 measures it. **The board, not the method, may set the floor:** Heltec quotes under 10 µA in deep sleep for the V3 ([Heltec](https://wiki.heltec.org/docs/devices/open-source-hardware/esp32-series/lora-32/wifi-lora-32-v3/)), but its regulator, charger, USB chip and display keep Heltec ESP32 LoRa boards well above the chip's datasheet figure in practice ([The Things Network forum](https://www.thethingsnetwork.org/forum/t/is-there-a-esp32-lorawan-board-for-battery-operation/35266)). One Meshtastic user saw about 2 mA on a V3, possibly while it was on USB power. At 2 mA, a 3,000 mAh cell lasts about 2 months before any listening. Measure the bare board's sleep current in T12 first. If it is in milliamps, the custom board is what makes "weeks" possible, and B or C becomes worth its cost.

- **`CLASSIFY`.** Stage 1 is Batear's harmonic detector, which is cheap and always on while awake. Stage 2 is a small learned model run only when stage 1 fires, which cuts false alarms (pipeline below). Alarm needs both.
- **`ALARM` / `CLEAR`.** Send ALARM at once and CLEAR when the sound has gone. One retry, as Batear does. A listener that alarms more than N times an hour with low confidence mutes itself for an hour and says so in its next CHECKIN, so a listener next to a generator can't flood the line.
- **No GPS, no over-the-air updates.** Position comes from I4. A new classifier ships in the next batch of listeners ([why]({{ site.baseurl }}{% link models/tripwire.md %}#rules-that-keep-it-cheap-and-quiet)).
- **From Batear, unchanged:** I²S set-up, FFT and harmonic scoring, battery divider gating, the RadioLib HAL. **From Batear, changed:** the packet (I1), the nonce (I1a), the heartbeat (every 30 min in Batear; at most 1–2 a day here, since every transmission can give a listener away).

### 2. Edge receiver firmware

Batear's gateway role minus Wi-Fi and MQTT, plus:

- **A build-time guarantee that it cannot transmit:** the transmit functions are compiled out, not just unused, and T17's SDR check confirms nothing is emitted.
- RS-485 output (I3) through a MAX3485-class transceiver on a spare UART.
- The reboot-safe replay table from I1a, stored in flash, so a receiver reboot doesn't accept old replays.
- RSSI and SNR on every frame, for line health.

### 3. Dugout display

**Shows:** a map of each line, listeners as dots coloured by last contact, a full-screen alarm naming the listener and its line, **time since crossing** counting up, confidence, and direction when both lines have tripped (outer first = inbound).

**False-alarm policy (proposed):**

| Condition | Display does |
|---|---|
| One listener, confidence high | Alarm |
| One listener, confidence low | Quiet log entry; alarm if a neighbour or the other line confirms within 30 s |
| Inside a friendly flight window the unit entered | Log only, labelled "friendly window" |
| Listener muted itself (I1 flags) | Grey dot, no alarms from it |

**Line health:** last check-in and battery per listener, listeners silent for over a day (possibly destroyed, [a signal in itself]({{ site.baseurl }}{% link models/tripwire.md %}#what-the-unit-gets)), weakest-link RSSI, and a re-lay forecast from battery trends.

**Build:** a single offline HTML page, served from the device and reading the serial port through the browser's Web Serial API, is the least code. It runs in Chrome on a laptop or an Android tablet. Offline map tiles are loaded before deployment. A TAK output (CoT messages) comes later ([integration]({{ site.baseurl }}{% link research/integration.md %})).

### 4. Mission tooling: `lay_line`

```
lay_line plan   line.geojson --spacing 150 --per-sortie 4 --alt 15  →  sortie-1.waypoints, sortie-2.waypoints, …
lay_line sitl   sortie-1.waypoints                                    →  simulated flight + release positions
lay_line ingest 00000042.BIN --sortie 1                               →  listeners.json (I4)
```

- **plan:** splits the line into drop points at the set spacing (from T11's range), groups them 3–4 per sortie, orders each sortie so the farthest drop comes first and the drone lightens as it returns, and writes I5 files. It warns if a sortie's distance exceeds the flight-time budget measured in T13.
- **ingest:** reads the ArduPilot DataFlash log with pymavlink, finds each servo output change, and takes the position and GPS quality at that moment. The same pass writes the jamming map the [tripwire describes]({{ site.baseurl }}{% link models/tripwire.md %}#the-fixes).
- **IDs:** each listener's ID is printed on its body and scanned or typed into the sortie at loading time, so the harness slot maps to an ID.

### 5. Classifier pipeline

1. **Data:** the public sets on [Training data]({{ site.baseurl }}{% link research/datasets.md %}), the layer 2 recordings, and Batear's alarm recordings from field listeners. Negatives (wind, vehicles, generators, birds, voices) carry as much weight as drone clips.
2. **Features:** log-mel spectrogram at 16 kHz, matching Batear's sample rate, so one front end serves both stages.
3. **Model:** a small convolutional network, int8-quantised, sized to run in tens of milliseconds on the ESP32-S3 with Espressif's ESP-DL or TensorFlow Lite Micro (both support the S3; timing is an estimate until benchmarked).
4. **Score:** detections per hour against false alarms per hour, at each distance, against Batear's harmonic detector alone. A model that doesn't beat it doesn't ship ([the weekend test's bar]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector)).
5. **Ship:** the model file is compiled into the firmware of the next batch, with its version in the packet's spare byte so the display knows which model raised an alarm.

### 6. Test harness

| Test | Tool | Pass |
|---|---|---|
| Drop missions | ArduPilot SITL running `lay_line` output ([SITL](https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html)) | Every `DO_SET_SERVO` fires at its point; the mission continues with the radio failsafe triggered |
| Classifier on the board | Recorded clips played through a speaker at a listener in a box, at set levels | Same detections as on the laptop, within the time budget |
| Relay and dedup | 6 bench listeners at low power, one alarm source | Every alert reaches the receiver once; no listener relays twice |
| Silence | SDR next to the edge receiver and an armed-wait listener (T17, T8) | Nothing above the noise floor |
| Reboot and nonce | Reboot a listener mid-test | Its next alert is accepted; no two packets share an IV |

## Order of work

| Step | Goes with | Work |
|---|---|---|
| 1 | MVP layer 1 (T9) | Flash Batear as is. Log RSSI and SNR |
| 2 | Layer 3 (T17) | Edge receiver: transmit compiled out, RS-485 output, the nonce fix |
| 3 | Layer 3 | Display v0: serial log to a list and a beep |
| 4 | Layer 4 (T12) | Wake-on-sound option A, temperature, the new packet; measure battery |
| 5 | Layer 5 (MVP) | Relay rules, display map and line health |
| 6 | After layer 2 data | Classifier stage 2 |
| 7 | T13 | `lay_line`, SITL first |
