# Handoff: fix the false "we are not cheaper than NW0" claim

Written at `HEAD: 9375b42` (2026-10-15). Follows `2026-10-15-dugout-distance.md` (done) and the
competitor rebuild in `9375b42`. `_handoff/` is not published by Jekyll.

## Repo rules (unchanged)

- All work in this repo (`C:\Users\paulm\drone-detection-research`), never umbrella-arcades.
- `git pull --ff-only` first. Add files by explicit path, never `git add -A`. Commit with
  `git commit -F -` and a quoted heredoc. Edit with Write/Edit (never `open(p,"w")`).
- Every factual claim sourced, or labelled as inference/estimate. Plain short sentences.
- Add a newest-first row to `changelog.md` for each change.
- Verify by rendering the live page with `?cb=<sha>` after the Pages build, never an HTTP 200.
  Build check: `gh api repos/paulrenzi/drone-detection-research/pages/builds/latest`.
  Site: https://paulrenzi.github.io/drone-detection-research/
- kramdown turns an em dash in a heading into a double hyphen in the anchor.
- Subagents on sonnet or haiku, never opus.

## What went wrong (Paul called it a major error)

Commit `9375b42` told readers we are **not cheaper than Zvook NW0**. That is false.

- **Per sensor:** our tripwire listener is $17–50 (no GPS). A hand-placed node is about
  $125–300 all-in ($1,500–2,500 kit = 8–12 nodes plus local fusion). NW0 is $834–950 per sensor
  (MAMO listing, 37,550–42,757 UAH at 45 UAH/$), **plus** 15–18 W of power it needs from mains,
  solar or 12–48 V DC, which is not in its price. So we are roughly 3–50x cheaper per sensor.
- **The bad step:** I compared per *position*, giving NW0 its maker-claimed 150–450 m range
  (so 1–2 sensors per position) while giving ours our cautious measured-literature range
  (so 8–12 nodes). Asymmetric assumptions: a competitor's best-case claim against our own
  worst case. At equal real range we are cheaper per position too.
- **What is actually open:** range, not price. 450 m is above anything measured for a cheap
  sensor; 150 m is near measured results. T11 (our own FPV range test) and any independent NW0
  test decide the per-position number.

## The task

1. **Correct every instance** (found by grep at `9375b42`):
   - `research/competitors.md`
     - L15 important box: "the same as a radio detector... 'Cheaper than the competition' is no
       longer our pitch against it."
     - L29 priority row 3: "1–2 per position at the advised 400–600 m spacing" (that spacing is
       the maker's; say so, and give per-sensor price as the comparable number).
     - L38 "On price per position we are not cheaper than NW0..."
     - L101 "Not price per position." (under NW0 "Where we differ")
     - L168 "On price: match the radio detector, not undercut NW0..."
     - L182 cost honesty: "The hand-placed kit costs about what one or two NW0s do."
     - Re-read "What the list says (inference)" and "Risks to this positioning" for the same
       framing.
   - `index.md` L115: "So we don't win on price per position; we win on ..."
   - `changelog.md` L10 (top row): "price per position is no longer our edge over it."
     Leave the old row as history; add a new top row stating the correction plainly.
   - Correct framing to use: **much cheaper per sensor (with numbers), no mains or solar power
     needed; cost per position depends on real range, which nobody has measured for either.**
2. **Audit the rest of the site for the same mistake**: any comparison where a competitor gets
   its claimed figure and we get a measured or cautious one (or the reverse). Check the priority
   table rows for RADD, Komodo, the radio detector and fibre catchers, `models/tripwire.md`
   comparison table, and `research/problem-check.md`. Same assumptions on both sides, or label
   the asymmetry.
3. Commit, push, wait for the Pages build, render-verify with `?cb=<sha>` (anchors still
   resolve, the corrected sentences appear, the old ones are gone).

## Settled, do not redo or reopen unasked

- Dugout-to-edge leg is a wire.
- Not accepted: T18 outreach draft, windbreak Monte Carlo, edge-receiver firmware, the
  3-column table change.
- Open question for Paul, raise once only if relevant: is this an open design (impact) or a
  business?
