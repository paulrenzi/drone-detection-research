# Handoff: listener and edge roles in CI, hop cap 63

Written 2026-10-19 at research-repo HEAD a3dc54e (before this commit). Supersedes
`2026-10-19-playbook-and-next-session.md` as the place to start. The playbook
(`docs/PLAYBOOK-DRONE-DETECTION.md`) is the authority; this is history.

## State at this commit
| Repo | HEAD | State |
|---|---|---|
| tripwire-firmware | 310ff7b | `listener` + `edge` roles; all 5 roles build, codec host test, Cppcheck green |
| tripwire-tools | da93d01 | hop cap 63, vectors + report regenerated; 17 tests pass |
| tripwire-display | 1d56a1d | README only |

## What changed
- `TRIPWIRE_LISTENER` (detector variant, only the boot log differs so far) and
  `TRIPWIRE_EDGE` (gateway variant: no MqttTask/Wi-Fi, RadioLib transmit calls poisoned).
  CI proves the poison fails a build. Edge image 457 KB vs gateway 1,103 KB.
- `TW_HOPS_MAX`, Python `HOPS_MAX`, simulator `hop_limit` 15 -> 63. Report rows that the
  cap cut off now deliver (dense forest, 30 listeners, 100 m: 7% -> 74%).

## Next
- **Waiting on Paul:** relay cancel after 1 or 2 duplicates.
- Ask Paul whether he has Heltec V3 boards (Phase 1).

## Standing rules
- Never open a PR to Batear without asking Paul.
- `gh` in tripwire-firmware defaults to Batear: pass `-R paulrenzi/tripwire-firmware`.
