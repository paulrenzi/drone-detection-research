# Handoff: software plan written, start Phase 0

Written at HEAD 37a73dc (2026-10-19). Supersedes the "Next" list in `2026-10-15-build-pages-done.md` for software work; its hardware "measure before printing" list still stands.

## Where things stand
- Site: https://paulrenzi.github.io/drone-detection-research/ (Jekyll, just-the-docs, GitHub Pages from `master`).
- **The plan is `build-software-plan.md`** (live at `/build-software-plan.html`, render-verified). It is the authority for what to build and in what order. `build-software.md` holds the component and interface specs (I1 packet, I1a nonce, I2 relay rules, I3 RS-485 frame) the plan refers to.
- **No code exists yet.** None of the three repos has been created.

## Decisions already made (don't reopen)
- Firmware = **fork of batear-io/batear** (MIT) on **RadioLib**, with two new build roles, `listener` and `edge`. Meshtastic, MeshCore and LoRaMesher are reference only: they transmit routinely, and Meshtastic is GPL.
- Relay wait is **signal-weighted** (heard weakest relays first, cancel on hearing it relayed), from Meshtastic's managed flooding. Already written into I2 rule 3.
- Relay listening uses RadioLib `SX126x::startReceiveDutyCycleAuto()`, with the ESP32 in deep sleep woken on DIO1 (GPIO 14 on the Heltec V3).
- Three repos: `tripwire-firmware` (the fork), `tripwire-tools` (Python: codec, relay simulator, `lay_line`, classifier pipeline, tests), and `tripwire-display` (one HTML file plus PMTiles, no build step). The C and Python codecs are both tested against **one shared test-vector file**, which is the contract between the repos.
- Al-Emadi drone audio set is **academic and non-commercial only**: benchmark with it, never train a shipping model on it. Usable sets: batear-datasets (MIT) and the Saarmets FPV set (CC BY 4.0).

## Next: Phase 0 (laptop only, $0)
1. Fork Batear and get its CI building the `listener` and `edge` roles. 🛑 **Creating the fork and repos under Paul's GitHub is outward-facing, so confirm public or private with Paul first.**
2. Write the I1 packet and the I1a nonce in C and Python, plus the shared test vectors. They must cover reboot, counter wrap, and a relayed packet re-encrypted under the relay's own ID. The nonce defect is still in upstream `lora_crypto.h`, so the fix comes first.
3. Relay simulator (M): 12–30 nodes, forest path loss from the T9 literature, cycle and preamble length, and the signal-weighted wait. It outputs delivery rate, delay to the edge and transmissions per alert, all against spacing.
4. **Done when:** the codec tests pass in both languages, and the simulator reproduces Meshtastic's published behaviour on a simple case.

Phase 1 (T9 range test, flash Batear as-is plus RSSI/SNR logging) needs Heltec V3 boards in hand. Ask Paul whether he has them; don't assume.

## Watch upstream
- Batear issue #51 (open): a mesh firmware where every node detects and relays, which overlaps our relay. Read it before writing relay code.
- Batear PR #49 (closed, unmerged): a TFLite Micro int8 CNN on `[1,32,40,1]` log-mel input, adding about 114 KB of flash. It's the starting point for Phase 5.
- Offering our nonce fix and relay back as PRs is outward-facing, so ask Paul first.

## Risks to settle early
- **Chrome on Android reading a wired USB serial adapter is unproven** (Phase 2). The laptop works either way. The fallback is a small native app on `mik3y/usb-serial-for-android` (MIT).

## Open, Paul's call
- Add the flyover check pass after laying (alive, actual hearing range, alert delay) to the tripwire page and the tests table? It's already in plan Phase 6.
- Demote the old v1–v3 renders on the hardware page?

## Rules for this repo
Commit by explicit path; `git commit -F -` with a quoted heredoc; verify pages by rendering with `?cb=<sha>`; kramdown anchors keep the parenthesised part of a heading (e.g. `#phase-2-edge-receiver-and-display-v0-t17-layer-3-m`). Never write backslashes through a heredoc. Commit and push before the session ends.
