# Handoff: a central anchor node as the GPS-jamming workaround

Written at `HEAD: df73497` (2026-10-15). Supersedes nothing; this is the first file in `_handoff/`.
`_handoff/` starts with an underscore, so Jekyll does not publish it.

## The task

A friend's suggestion, in their words:

> "I was thinking central node has gps and distributed nodes use dead reckoning / calibrated
> distance measures to central node as a workaround for gps jamming"

Paul asked to add it to the site's considerations. Do that in this session: a short note on the
tripwire page, and an open question for the models that need precise positions (M1, M3).

## Where the site stands

- Live: https://paulrenzi.github.io/drone-detection-research/ (Jekyll 3.9, Just the Docs 0.10.0,
  custom layout `_layouts/default.html`).
- `models/tripwire.md` was reorganised into layers on 2026-10-15: a summary, a "Front-line
  problems, in plain terms" table, then 8 fold-out sections (`<details class="layer" id="..."
  markdown="block">`). The fold-out script lives in `_includes/head_custom.html`; styles in
  `_sass/custom/custom.scss`.
- The tripwire's listeners already carry **no GPS** (section `#solving-the-field-limits-at-no-extra-cost`).
  Position = drop plan + the release point in the delivery drone's ArduPilot log. Clock = set at
  loading, kept in step with neighbours via relays. That clock sync is test **T15**.
- M1 (`models/m01-ground-array-mesh.md`) still lists a GPS with timing pulse (PPS), $8–15, for
  position and time sync. M1 and M3 are where jamming would hurt most.
- Tests live in `research/open-questions.md` (T1–T15). Jamming facts are sourced in
  `research/field-conditions.md#electronic-warfare` (R-330Zh, 20–25 km against ground radios).

## The assessment already given to Paul (agreed direction)

**Keep:**
- **One known reference instead of GPS on every node.** For the tripwire this is already the design;
  the delivery drone is the reference.
- **The anchor doesn't need GPS either.** At the unit it would be jammed too (20–25 km jammer
  range). The unit's position is known from a map or a one-off survey, so make it a surveyed point.
- **A central time source** is simpler than neighbours syncing with each other. The cost is that the
  anchor transmits, and a regular emitter at the unit marks the unit (see T8). A rare time beacon, or
  one placed away from the unit, may be acceptable.

**Doesn't fit:**
- **Dead reckoning is for moving things.** A dropped node doesn't move. The drone dead-reckons
  already (T14).
- **Ranging to the anchor** runs into the same reach problem as T9: a node 2–4 km out under trees
  may not hear the anchor at all, and ranging hop by hop accumulates error.
  - SX1262 (the current radio) has no time-of-flight ranging. SX1280 (2.4 GHz LoRa) has it built in,
    but 2.4 GHz carries less, especially through foliage.
  - RSSI ranging is poor, especially under trees. UWB is short-range.
  - Every ranging exchange is another emission.
  - 🛑 **No accuracy or range figure for SX1280 ranging has been checked.** Source it (Semtech
    datasheet / app note) before writing a number, or label it as unverified.
- **The tripwire doesn't need precision.** Nodes are 100–300 m apart; 20–50 m position error
  doesn't change "a drone crossed near node 7".

**Where it pays off:** M1 and M3, which locate a drone from several microphones and need node
positions (and clocks) to a few metres / milliseconds. There, ranging to a surveyed anchor is a
serious alternative to GPS under jamming.

**Also worth writing up** (my idea, not the friend's): calibrate node positions from the delivery
drone's own known track as it flies back over the line, using each node's acoustic detection of the
flyby. No extra radio emissions.

## What to do

1. Research and source: SX1280 ranging accuracy and range (Semtech), and any published LoRa / sub-GHz
   time-of-flight ranging results under foliage. Label anything unsourced as an estimate.
2. Tripwire page: add a short "Considered: anchoring to a central node" note. Best home is probably
   inside the `solving-the-field-limits-at-no-extra-cost` fold-out (or `limits-and-risks`). Credit the
   suggestion as reader feedback, not by name. Keep it short; the page was just simplified.
3. M1 (and M3 if it relies on GPS): add the anchor + ranging idea as an alternative to GPS/PPS under
   jamming, and add a new open question **T16** in `research/open-questions.md` (cost, what it
   answers, "Not started").
4. Optionally consider whether T15 should mention a central time beacon as one of the sync options.
5. Add a `changelog.md` row (newest first, `{{ site.baseurl }}{% link ... %}` links).
6. Commit, push, then verify by rendering the live page with `?cb=<sha>` after the Pages build
   (`gh api repos/paulrenzi/drone-detection-research/pages/builds/latest`).

## Rules for this repo

- Only claim what is true and sourced; label estimates as estimates.
- Edit with Python scripts that assert exactly one match per replacement, write `.new`, then `os.replace`.
- Links: `{{ site.baseurl }}{% link path %}`.
- 🛑 The layout compresses HTML onto one line: never put `//` comments in inline scripts (use `/* */`).
- Commit with `git commit -F -` and a quoted heredoc; add files by explicit path, never `git add -A`.
- Never use the paid Anthropic API; subagents run on sonnet or haiku only.
- Verify a page by rendering it with `?cb=`, never by an HTTP 200. Pages caches for 600 s.

## Open offer, never answered

The 4-column "Front-line problems, in plain terms" table on the tripwire page is tall on a phone.
Offered to cut it to 3 columns or cards; Paul hasn't replied. Don't do it unasked.
