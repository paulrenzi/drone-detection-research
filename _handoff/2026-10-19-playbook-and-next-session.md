# Handoff: playbook written, start the next session here

Written 2026-10-19 at research-repo HEAD 81f3f0f (before this commit). Supersedes
`2026-10-19-phase0-codec-and-simulator-built.md` as the place to start; that file and
`2026-10-19-software-plan-start-building.md` are history.

## Read first
1. `git pull --ff-only` in all four repos (`drone-detection-research` is on **main**).
2. `docs/PLAYBOOK-DRONE-DETECTION.md` — the current authority: repos, packet and nonce
   architecture, relay rule, simulator, findings, how to run and debug, gotchas.
3. `build-software.md` and `build-software-plan.md` for the specs and phases.

## State at this commit
| Repo | HEAD | State |
|---|---|---|
| drone-detection-research | this commit | playbook added (`docs/`, excluded from the site) |
| tripwire-firmware (private) | 6fe7fea | nonce fix + tw_codec; CI green (3 ESP-IDF roles, host test, Cppcheck) |
| tripwire-tools (private) | 0b3ddb0 | codec, vectors, simulator, report; 17 tests pass |
| tripwire-display (private) | 1d56a1d | README only |

Phase 0 laptop work is done. Nothing has run on a board.

## Next
- **Waiting on Paul:** relay cancels after 1 duplicate (fewer transmissions, loses alerts)
  or 2 (+7–17 points delivered, ~1.5× transmissions). Update I2 and the simulator default
  once he decides.
- Build the `listener` and `edge` roles in `tripwire-firmware` CI (plan Phase 0 bullet 1).
- When I2 goes into firmware, raise `TW_HOPS_MAX` (15 in `tw_codec.h`) and the simulator's
  default `hop_limit` (15) to 63; the spec already says 63+.
- Ask Paul whether he has Heltec V3 boards (Phase 1).
- Optional: an independent Meshtasticator run on the simple cases.

## Standing rules for this work
- Never open a PR to Batear without asking Paul.
- No C compiler on the PC: C tests run on `ssh ubuntu@claude-dev` or in GitHub CI.
- Subagents are discouraged (token cost); never use the paid Anthropic API.
