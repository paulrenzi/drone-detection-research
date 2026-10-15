# Handoff: where units live relative to the tree edge (and the wired leg)

Written at `HEAD: a682536` (2026-10-15). Follows `2026-10-15-central-anchor.md`, whose task is
done (commits `682baf8` to `a682536`). `_handoff/` is not published by Jekyll.

## Repo rules (unchanged)

- All work in this repo (`C:\Users\paulm\drone-detection-research`), never umbrella-arcades.
- `git pull --ff-only` first. Add files by explicit path, never `git add -A`. Commit with
  `git commit -F -` and a quoted heredoc. Edit with Write/Edit or a Python script that writes
  `.new` then `os.replace` (never `open(p,"w")` on the real file).
- Every factual claim sourced, or labelled as inference/estimate. Plain short sentences.
- Add a newest-first row to `changelog.md` for each change.
- Verify by rendering the live page with `?cb=<sha>` after the Pages build, never an HTTP 200.
  Site: https://paulrenzi.github.io/drone-detection-research/ (Jekyll 3.9, Just the Docs).
- Subagents on sonnet or haiku, never opus.

## The task

Add two things, both agreed with Paul:

1. **Two new T18 interview questions** in `research/problem-check.md`, section
   `## The next step: ask before building (T18)` (numbered list, currently 6 items):
   - Is your position in a windbreak, a forest, a field or ruins?
   - Roughly how far is it from the tree edge that faces open ground?
2. **A "Not found" line** in `research/field-conditions.md`, section
   `## Where infantry actually sit: tree lines` (next to the existing "Not found" bullet, line ~21):
   no published figure for how far positions sit from a tree-line edge. Add the sourced context
   below.

Optionally (only if it fits naturally): one sentence in the tripwire's
`#getting-alerts-out-of-the-trees` fold-out (`models/tripwire.md`) saying the wired leg works in
every terrain case, and the open risk is the listener-to-edge radio leg (T9 run E).

## What was found (2026-10-15 research)

**No source gives a distance from tree edge to a unit's dugout**, in English or Ukrainian searches.

Sourced context:
- Belts are planned at 3–5 rows, about 7.5–15 m wide ([IUAF](https://iuaf.org/ukraine/amp/));
  one Luhansk belt "a few metres wide" ([Stars and Stripes](https://www.stripes.com/theaters/europe/2024-10-28/ukraine-farming-vital-battlefield-land-15653560.html)).
  Already on `field-conditions.md`.
- Infantry live in hand-dug burrows about a metre wide, with underground rooms and tunnels;
  terrain listed includes tree belts, river floodplains, steppe and slag heaps; no location
  relative to a tree line given ([Texty, "how infantry survive underground"](https://texty.org.ua/articles/118179/chym-dovshe-tym-krashche-yak-pixota-vyzhyvaye-v-norax/)).
  Russian forces control the sky over forest belts (same source).
- A belt believed occupied may be empty but under constant enemy drone watch
  ([450 Tactical](https://450tactical.com/yak-diiaty-pid-chas-shturmu-posadky-korotko-zhorstko-pravylno/)).
- Real-forest fighting exists (Serebryansky forest near Kreminna, on foot)
  ([Kyiv Post](https://www.kyivpost.com/post/52057), [CEPA](https://cepa.org/article/firefights-and-fear-in-ukraines-forest-war/)).
- Some southern approaches have "no fields or forest strips", only ruins ([Texty](https://texty.org.ua/articles/117451/why-ukrainians-soldiers-havent-left-their-combat-positions-for-months/)).

Inference (label it as such on the site):
- In a 7.5–15 m windbreak no point is more than about 4–8 m from an edge, so the wired leg is
  metres to tens of metres.
- In a real forest it could be hundreds of metres: still easy for a wire (RS-485 ~1.2 km), but the
  listener radio leg is the hard forest case.
- In ruins or open ground there is no tree edge; the receiver goes on a roof or pole near the
  position.
- Some units may dig beside belts rather than in them, because belts are watched. No source says
  how often.

## Settled direction (don't reopen)

- Dugout-to-edge leg = **a wire** (copper twisted pair, which can also power the edge receiver; or
  salvaged FPV fibre). Emits nothing at the unit. Fallback: second wire route, or low-power
  433 MHz used only when the wire is down (20/50/100 m of trees ≈ 6/10/16 dB, Weissberger, our
  calculation, vs ~159 dB budget).
- Remaining risks: listener-to-edge radio across fields and belts (T9 run E), and whether warning
  changes behaviour (T18, do first).

## Still offered, not accepted

Draft T18 outreach (save in repo, don't send); windbreak Monte Carlo simulation; edge-receiver
firmware. Don't do the 3-column table change on the tripwire unasked.
