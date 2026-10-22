# Handoff: make the weekend-test UI simpler and more intuitive

Written 2026-10-21 at tripwire HEAD 2170f5a (before this commit). Supersedes
`2026-10-19-roles-and-hop-cap.md` as the place to start. The playbook
(`docs/PLAYBOOK-DRONE-DETECTION.md`) is the authority; this is history.

## State at this commit
| Repo | HEAD | State |
|---|---|---|
| tripwire (site, paulrenzi.github.io/tripwire) | 2170f5a | flasher serves CI firmware 9337879; logger has role picker + field hotspot setup |
| tripwire-firmware (PUBLIC since 10-21) | 9337879 | all CI green: 7 roles, Cppcheck, codec host test; `firmware-latest` release updated |

## What the test UI is today
- **Flasher** `tools/flasher/index.html` (205 lines): 1. Detector, 2. Gateway (optional
  hotspot, made-up gateway ID), "If it won't connect" (boot button, mic pins, what gets
  written). Patches NVS at 0x9000 into the merged bin in the browser.
- **Logger** `tools/weekend/logger.html` (1826 lines, one file): role picker first
  (Logger phone / Mic phone / Just watching), then Connect, Sound at the mic, Run, Let
  someone else watch, Speaker test, Range so far, Runs, Readings, Raw log, and a
  "What the numbers mean" guide. Panels are hidden/collapsed per role.
- **Guide** `weekend-test.md` (202 lines): the written walkthrough, incl. `#phone-setup`.
- Field hotspot flow: gateway with no known hotspot opens `tw-… setup`; the logger phone
  joins it, types its hotspot into the captive page (or 192.168.4.1), then turns the
  hotspot on. The gateway shows up under Connect ~30 s later.

## Next session's job
Make the flasher + logger simpler and more intuitive for a first-time tester. Start by
rendering both pages on a phone-sized viewport per role and listing every word, choice
and panel a tester sees before the first run; cut or defer anything not needed for that
first run. Candidate ideas, not decisions:
- One guided step at a time per role (a "next step" card) instead of many panels.
- Hide Runs / Readings / Raw log / guide behind one "More" until a run exists.
- Say what state each phone/board is in (waiting for gateway, connected, ready) in one line.

## Not proven
- Nothing has run on a real XIAO. The captive popup on real phones is untested.

## How to verify (standing)
- Render with Playwright and `?cb=<n>`, never trust an HTTP 200. Render script:
  `python tools/render_check.py https://paulrenzi.github.io/tripwire` (checks flasher labels, fw version, NVS keys, logger role
  text, page errors). Bump its `cb=` values after each deploy.
- US units only on every page and the logger.

## Standing rules
- Never open a PR to Batear without asking Paul.
- `gh` in tripwire-firmware defaults to Batear: pass `-R paulrenzi/tripwire-firmware`;
  `gh run list -c` needs the full sha.
- Commit your own files by explicit path. Never fan out subagents.
