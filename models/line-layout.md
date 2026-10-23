---
title: 12 darts in the field
nav_tripwire: 1.5
---

# 12 darts in the field
{: .no_toc }

What 12 darts look like in front of a unit, seen from above and drawn to scale. The darts form a chain: the one that hears a drone radios the dart behind it, which passes the alert on, hop by hop, back to the unit. Each hop is about 980 ft (300 m), our working figure for a dart's radio near the ground ([T9]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back) measures it). Each dart hears about 490 ft, the Saturday test's pass mark, not yet measured ([T11]({{ site.baseurl }}{% link mvp.md %}#layer-2-hear-a-drone-from-near-the-ground-t11)). The animation runs ten times faster than real life.

1. TOC
{:toc}

## The layout

<figure style="margin:12px 0 8px;max-width:600px">
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px">
<button type="button" class="btn btn-sm" data-layout="trail">Trail</button>
<button type="button" class="btn btn-sm" data-layout="crossbar">Trail + crossbar</button>
<button type="button" class="btn btn-sm" data-layout="arc">Arc</button>
</div>
<div id="line-layout"></div>
<figcaption style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px">
<button type="button" id="line-layout-play" class="btn btn-sm">Play</button>
<button type="button" id="line-layout-replay" class="btn btn-sm">Replay</button>
<span id="line-layout-status" aria-live="polite" style="font-weight:600;flex:1 1 220px"></span>
</figcaption>
</figure>
<script src="{{ '/assets/js/line-layout.js' | relative_url }}" defer></script>

Each layout uses the same 12 darts, and no hop is longer than 980 ft. Each plays two drones at 45 mph: one heading straight for the unit, then one coming in 30° off to the side.

## How the alert gets back

1. **Hear.** Every dart listens all the time, in every direction. It only answers one question: *is that a drone?*
2. **Pass it back.** The dart that hears it radios a few bytes to the dart behind it, which passes them on, until the last dart reaches the receiver at the unit. Each hop takes about 0.05–1 s depending on the radio's settings, so 12 hops add at most about 12 s, and short hops allow the fast settings (airtime estimate).
3. **Warn.** The tablet sounds the alarm. Warning is distance ÷ speed, from wherever the drone was first heard.

**It is a tripwire, not a microphone array.** An array combines its microphones to find a direction, which needs exact spacing and shared timing. Here each dart only says "I heard it", and the chain carries that home.

## Depth against width

The same 12 darts can reach far out in a narrow trail or spread wide closer in. A drone heading for the unit is caught only if it passes within 490 ft of a dart, so the shape decides which drones get a minute.

| Layout | Front darts | Warning, straight in (45 mph / 75 mph) | Drone 30° off to the side | Approach angles given a minute or more at 45 mph |
|---|---|---|---|---|
| **Trail**: 12 in a chain, 980 ft apart | 2.2 mi | ~3 min / ~1 min 50 s | missed by the darts; the unit hears it ~7 s out | **±7°** |
| **Trail + crossbar**: 8 in a chain, 5 across the head | 1.3 mi | ~1 min 50 s / ~1 min 7 s | caught by the nearest chain dart, ~15 s | **±12°** |
| **Arc**: 3 in a chain, 9 in an arc ~900 ft apart | 0.74 mi | ~1 min 6 s / ~40 s | caught by the arc, ~1 min 5 s | **±60°** |

All figures are our geometry on the planning numbers above, not measurements. 45 mph is about what an FPV flies with a warhead; 75 mph is the most reported for a loaded one ([the drones]({{ site.baseurl }}{% link research/threat-profile.md %})).

- **A trail is right when drones come down a known route,** such as a road, a gap between tree belts or a valley. Then its extra depth is minutes of warning.
- **When drones can come from anywhere on the enemy's side, width matters more than depth.** A minute at 45 mph needs a drone heard about 0.75 mi out. The arc puts every dart past the chain at that distance, so a minute covers about ±60° instead of ±7°.
- **Darts are cheap, so mix them:** a chain along the likeliest route, with an arc or crossbar at the one-minute distance.

## Spacing rules

- **Chain darts: no farther apart than the radio reaches,** about 980 ft (300 m) near the ground, less under trees. At that spacing their 490 ft hearing circles just touch, so the chain also hears anything crossing it.
- **Arc and crossbar darts: under about 920 ft apart,** so a drone flying 165 ft up midway between two darts is still within 490 ft of one. Fibre-optic FPVs fly at about 65–165 ft.
- **A dead dart breaks the chain.** Everything in front of it goes silent. Placing chain darts at half the radio's reach lets each skip one dead neighbour, at the cost of twice as many chain darts.
- **Closer under trees and in strong wind,** which shorten both hearing and radio range.

## What 12 darts miss

- **Drones that don't pass within 490 ft of a dart,** which for a trail is most drones not coming down its line.
- **Fibre-optic FPVs already parked in ambush.** They sit silent by a road and lift off seconds before they strike.
- **Drones launched from inside the layout,** and drones flying higher than a dart can hear.
- **Direction.** A dart hearing a drone can't tell if it is the unit's own, unless the unit's drones fly at set times.

At under $100 a dart (the parts list comes to about $17–50), 12 darts cost $200–1,200. Whether 490 ft hearing and 980 ft hops hold is what the Saturday test, T9 and T11 decide. If a dart hears only 160–200 ft, every layout here needs two to three times as many darts for the same cover.
