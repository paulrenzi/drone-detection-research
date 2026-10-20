# Handoff: Phase 0 codec and relay simulator built

Written 2026-10-19 at research-repo HEAD 346a200 (before this commit). Supersedes the "Next: Phase 0" list in `2026-10-19-software-plan-start-building.md`; its "Watch upstream", "Risks" and "Open, Paul's call" sections still stand.

## Repos (all PRIVATE under paulrenzi, approved by Paul 2026-10-19)
- **tripwire-firmware**: Batear's full history (upstream `5908f0e`), remote `upstream` = batear-io/batear. **Not a GitHub fork:** GitHub won't make a fork of a public repo private, so it's a private copy. A public fork can be cut later for upstream PRs (ask Paul first).
- **tripwire-tools**: Python codec, vectors, relay simulator, report.
- **tripwire-display**: README only.

## Done
1. **Nonce fix (I1a)** in Batear's own detector and gateway (`tripwire-firmware` 9503e25). Nonce is `[u16 sender_id][u16 boot][u32 counter]` LE. Boot is stored in NVS under `lora_nonce/boot` and persisted before the first transmit; the listener refuses to transmit if the write fails. Packet is 40 B. The gateway's replay check uses the nonce, and the nonce's sender must equal `device_id`. **CI builds all three Batear roles green.** Not run on a board.
2. **I1 codec** in C (`components/tw_codec`, pure C, AES-GCM behind a hook: PSA on the board, OpenSSL on the host) and Python (`tripwire/codec.py`). **One vector file** (`tripwire-tools/vectors/i1_vectors.txt`, generated; byte-identical copy in the firmware repo). It covers reboot, counter wrap, relays re-encrypted under the relay's ID, tampering, the nonce state machine and the replay check. C: 102 checks pass under ASan/UBSan (GitHub CI and claude-dev). Python: passes. A mutated vector fails both.
3. **Spec gap closed:** I2 rule 2 deduped on the origin's (boot, counter), but a relayed copy carries the relay's nonce. Two of the three spare plaintext bytes are now `tag` (origin boot and counter, low byte each). `build-software.md` is updated.
4. **Relay simulator** (`tripwire/relaysim.py`) and report (`reports/relay-sim-phase0.md`). Checked against exact results from Meshtastic's client rule (read from firmware source today) on three simple cases. It has **not** been compared side by side with Meshtasticator or field data.

## What the simulator says (model, presets fitted to T9 literature)
- Dense forest: ~70 m spacing for 90% delivery from the far end of 20–30 listeners. Light forest ~200 m, open ~900 m.
- 10–30 s to the edge, ~2 s per hop. The 1 s listening cycle forces a 1.07 s preamble, so airtime is 1.5 s.
- **Hop cap 15 is too low** for 30 listeners in dense forest (48% delivered vs 77% at cap 63). The spec now says 63+.
- **Open decision for Paul:** cancel a relay after 1 duplicate (I2 now: ~half the transmissions, loses alerts when the front listener hears a copy from behind) or after 2 (+7–17 points delivered, ~1.5× transmissions).

## Next
- Paul: the cancel rule (above).
- Build the `listener` and `edge` roles in the fork's CI (plan Phase 0 bullet 1, not yet started).
- Phase 1 needs Heltec V3 boards. Ask Paul whether he has them.
- Optional: run Meshtasticator (now CC BY 4.0, not unlicensed as the plan says) on the same simple cases for an independent check.

## Gotchas
- No C compiler on Paul's PC. Host C tests run on `ubuntu@claude-dev` (gcc + libssl) or in GitHub CI (`make -C components/tw_codec/test`).
- Batear's "Deploy Docs" workflow is **disabled** in the private copy (it publishes docs.batear.io). "Publish Firmware" still runs on push and makes a private `firmware-latest` prerelease.
- After changing the vectors: run `python -m tripwire.vectors > vectors/i1_vectors.txt`, then copy the file to the firmware repo. The tools tests fail if the copies differ.
