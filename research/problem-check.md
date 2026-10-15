---
title: Is the problem worth solving?
parent: Research Notes
nav_order: 0.25
---

# Is the problem worth solving?
{: .no_toc }

Before building more, check the premise: are units' current methods failing, would earlier warning change anything, and is someone already solving it? Every point is sourced; where nothing was found, this page says so. Reviewed 2026-10-15.

1. TOC
{:toc}

## Short answer

**Not a waste, but not proven worth it either.** The threat is real, it is the biggest killer at the front, and the fastest-growing part of it (fibre-optic FPVs) defeats the cheap detectors units carry. What nobody has published is whether **earlier warning changes what troops do**, and that is the claim the tripwire rests on. It is also the cheapest thing to check: ask the people who would use it (T18), before any more hardware.

## What the evidence says

### The threat is real and is the main killer

- **Drones cause about 80% of casualties**, according to analyst Rob Lee and others. Most casualties fall in the kill zone, a band roughly 10–20 miles deep on each side of the line ([NPR, 5 Oct 2026](https://www.tpr.org/news/2026-10-05/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)).
- **Tree-line positions are targets in themselves.** Incendiary drones are flown along tree lines to burn away the foliage troops hide in ([RUSI](https://www.rusi.org/news-and-comment/in-the-news/ukraines-fire-dropping-drones-can-find-shock-russian-troops-experts)). Night is no refuge: FPVs carry thermal cameras (same NPR report).
- **Fibre-optic FPVs are a large share in some sectors.** Estimates run from 30–50% of FPV operations in some sectors ([drone-warfare.com](https://drone-warfare.com/research/fpv-drone-warfare/), rated medium confidence there) to a claim of 90% of Russian attacks in one Kharkiv-region sector by a Ukrainian operator ([Gwara Media](https://gwaramedia.com/en/russians-expand-area-for-using-fiber-optic-drones-in-kharkiv-oblast-in-2026-military-says/)). No front-wide figure was found.

### What units do today, and how well it works

There is no single "current model". At the front it is a set of coping measures:

| Measure | What it does | Where it falls short |
|---|---|---|
| **Stay underground and hidden** | The main defence. Troops move on foot, slowly, and hide when they hear a drone: one group took four hours to cover 1 km ([NPR](https://www.tpr.org/news/2026-10-05/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)) | It works by not moving, at a huge cost: rotations take hours to days, and some infantry have gone more than a year without one (same source) |
| **Nets** | Physical barrier over positions and routes (same source) | Static; no warning |
| **Listening by ear** | Troops hide when they hear one (same source) | Detection by ear is short-range; no measured figure found |
| **Radio detectors** (Chuyka and similar, ~$750–850) | Warn of FPVs by their video signal, up to about 4 km ([site note]({{ site.baseurl }}{% link research/competitors.md %})) | Blind to fibre-optic FPVs ([Kyiv Independent](https://kyivindependent.com/as-russias-fiber-optic-drones-flood-the-battlefield-ukraine-is-racing-to-catch-up/)) |
| **Shotguns** | Last-ditch kill | FPVs close at close to 100 km/h, giving infantry "only a moment to react" ([RFU News, Nov 2025](https://www.rfunews.com/articles/insider-annual-why-shotguns-are-suddenly-the-most-valuable-defense-against-fpv-drones)) |
| **Interceptor drones** | Kill drones in the air | Built mostly for Shaheds and reconnaissance wings. They work only inside a radar or acoustic sensor's detection zone ([Ukrainska Pravda, Mar 2026](https://www.pravda.com.ua/eng/articles/2026/03/11/8025014/)) |

**Cameras like Anduril's WISP are not the current model at the front.** We found no reporting of WISP deployed in Ukraine; the published deployment is the Washington National Guard training on it for World Cup security ([DroneXL](https://dronexl.co/2026/08/06/anduril-wisp-washington-national-guard-drones-birds/)). It also needs line of sight, which tree lines block.

### Is ten seconds enough?

**No published figure answers this.** No source we found says how many seconds of warning troops need, or measures what a detector's warning saves. Detector makers describe the value as seconds to find cover. What follows is inference:

- **Troops already underground** need warning only when they are exposed: on the move, collecting a drone-delivered resupply, observing, repairing, fighting.
- **Ten seconds** is enough to step into a dugout a few metres away. It is not enough for people strung out on a four-hour walk, or to launch an interceptor.
- **A minute** could let walkers get off a path and under cover, or hold a resupply pickup until the drone has passed. Whether units would act on it is the open question.

### Someone is already building the near-unit layer

**ZVOOK NW0** (announced January 2026): a Ukrainian acoustic sensor for FPVs, including fibre-optic ones. Claimed 150–450 m range, 360°, 15–20 W, linked by fibre, twisted pair, LTE or LoRa, spaced 400–600 m, pitched for front-line positions, frontline towns and logistics routes. No price or deployment reported ([Militarnyi](https://militarnyi.com/en/news/ukraine-develops-acoustic-detector-for-fpv-drones/)).

That is both validation (a Ukrainian team building from the front thinks acoustic FPV detection is worth fielding) and competition. Where we would still differ: battery power for weeks instead of 15–20 W of wired power, throwaway cost, and lines laid forward rather than sensors at the unit.

## What would make it a waste

Any of these, found by asking users or by testing:

1. **Warning doesn't change behaviour.** Troops stay hidden by default, hear drones themselves in time, and would not act differently with a minute.
2. **Exposure is mostly on the move, not at positions.** Then the tripwire must be re-aimed: lines along approach paths and covered footpaths to warn walkers, not around a position. That is a change of aim, not a dead end (inference).
3. **A cheap enough sensor is already in units' hands**, such as the NW0 at scale.
4. **Radio can't get out of the trees**, even with a [wired edge receiver]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees) (T9, T17).

## The next step: ask before building (T18)

Talk to 5–10 people with recent front-line experience: soldiers, the volunteers who equip units, Brave1, and Ukrainian drone and EW firms. Ask:

1. When are you most exposed to FPVs: in position, on rotation, at resupply pickups, observing?
2. How do you know a drone is coming now, and how much warning does that give?
3. What would you do differently with 10 seconds, one minute, three minutes?
4. Roughly what share of FPVs attacking you are fibre-optic?
5. Would you place 10 listeners by hand, or accept a receiver on a pole at your tree-line edge?
6. Who decides what kit a unit gets, and who pays: the unit, volunteers, or the state?

**Pass:** most say a minute's warning would change what they do, and name the moment it matters. **Fail:** most say it wouldn't. Either answer is worth more than T9.
