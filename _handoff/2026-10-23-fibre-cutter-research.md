# Handoff: research an automated cutter for a fibre-optic drone's line

Written 2026-10-23 at tripwire HEAD 8b5431b (this handoff is the next commit). This starts a
**new line of research**. It does not replace `2026-10-23-road-guard-practical-questions.md`,
which stays the place to start for road work. The playbook (`docs/PLAYBOOK-DRONE-DETECTION.md`)
is still the authority for the software, and this file is history.

## Why
A fibre-optic FPV trails a hair-thin glass line back to its pilot. Radio jamming can't touch it,
so today troops often answer one with a shotgun at close range. Paul finds that horrifying and
dangerous, and wants to know whether the tripwire can do the job instead: **notice a fibre
crossing our line and cut it automatically, with nobody standing up to shoot.**

## State at this commit
- **Everything is pushed and live** at https://paulrenzi.github.io/tripwire. The only thing
  not committed is `_scratch_ui/`, which is never committed.
- **Latest commits:**
  - `1cfd265`: feasibility is now 4/5; the markup is split (+200–300% on our parts, +30% on the
    drone kit); costs include the 4-mic array; the upkeep floor is lower, with a second-cell
    option.
  - `8b5431b`: the tripwire stat card reads 22 darts a lay, 4 of them tips with fibre.
- **Today's numbers** (all models, nothing field-measured):
  - Darts: ~$38 small batch, ~$128 for a tip dart.
  - Package: ~$2,900 at cost, $6.3–7.8k at our price.
  - Upkeep with solar: $1.6–6.3k a year.

## What already exists that a cutter could build on
- **Darts on the ground, in a line.** Each dart has 4 MEMS mics, a compass, LoRa, and solar.
  Tip darts carry ~1.2 mi of FPV fibre home to a base box. See `models/tripwire.md`,
  `build-hardware.md`, and `cad/`.
- **A fibre FPV usually flies low,** about 65–165 ft and following the terrain, at up to
  ~43 mph. It can also park silent by a road for up to 12 h. See `research/threat-profile.md`.
- **Its fibre is left lying across the ground and the vegetation behind it.** That is the line
  a cutter would meet. Whether it lies there long enough, and how slack or taut it is near
  our line, is unknown.
- **Road guard:** posts every ≤1,100 ft along a road, plus a fence of air-dropped darts. See
  `models/route-guard.md`.

## Open questions to research (not answered yet; ask Paul for his first)
1. **What the fibre physically is:** diameter, coating, tensile strength, colour, spool lengths
   (6–25 mi?), and how it lies (a straight run, slack, or snagged on trees).
2. **What happens when it's cut:** does the drone fall, hover, return, or carry on under
   terminal autonomy or a locked target? This decides whether cutting is worth anything.
   It may only help before the drone reaches the strike zone.
3. **Sensing a crossing:** acoustic (we already hear the drone pass), a tripwire filament or
   mesh, a capacitive or optical break-beam, or a camera. And how a dart knows the fibre is
   *on* it, not just near it.
4. **Cutting mechanisms:** a spinning blade, a hot wire or nichrome, a guillotine, a
   pyrotechnic cutter, a laser, or a rotating snag arm that breaks the line by tension.
   Compare power, weight, cost and reliability.
5. **Severing far from the dart:** the fibre may lie yards from any dart. Options include a
   sweeping arm, a launched entangling line, or a cheap ground "comb" between darts.
6. **What's already out there:** fielded or proposed anti-fibre tools in Ukraine or Russia,
   patents, and defence-tech startups.
7. **Safety and false triggers:** our own tip darts carry fibre home, so the cutter must never
   cut our own line. Also civilians, animals, and debris.
8. **Rough cost per mile,** in the same form as `costs.md`.

## Rules carried over (Paul's standing brief)
- `git pull --ff-only` first.
- **Ask Paul for his questions before building anything.** Answer them directly, and change
  the model or pages only when he says so.
- US units only. Run Python with `py`.
- Do the research yourself, with no subagents. Never use the paid Anthropic API.
- Check pages by rendering them with `?cb=`.
- Commit by explicit path. Never `git add -A`, and never commit `_scratch_ui`.
- Write `.new`, then `os.replace`. Commit with `-F -` and a quoted heredoc.
- No backslashes through a bash heredoc.
