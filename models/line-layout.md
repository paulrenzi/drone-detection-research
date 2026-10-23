---
title: What a line looks like
nav_tripwire: 1.5
---

# What a line looks like
{: .no_toc }

One line of 12 darts in front of a unit, seen from above and drawn to scale. The animation runs time ten times faster than real life. Every distance is a planning figure. The one that decides everything, how far a dart hears an FPV, is not measured yet ([T11]({{ site.baseurl }}{% link mvp.md %}#layer-2-hear-a-drone-from-near-the-ground-t11)).

1. TOC
{:toc}

## The layout

<figure style="margin:12px 0 8px;max-width:600px">
<div id="line-layout"></div>
<figcaption style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px">
<button type="button" id="line-layout-play" class="btn btn-sm">Play</button>
<button type="button" id="line-layout-replay" class="btn btn-sm">Replay</button>
<span id="line-layout-status" aria-live="polite" style="font-weight:600;flex:1 1 220px"></span>
</figcaption>
</figure>
<script src="{{ '/assets/js/line-layout.js' | relative_url }}" defer></script>

- **The darts stand in a row 1.2 mi in front of the unit,** across the way drones come in. They are dropped by a small drone or placed by hand at night, each on a stake with its mic about 20 in up.
- **The receiver sits at the edge of the unit's own tree line,** where the radio carries best, wired back to a tablet in the dugout ([design]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees)).
- **Tree belts** cross the ground between them. Under canopy, darts sit closer together, because trees shorten both hearing and radio range.

## How a dart catches a drone

1. **Hear.** Every dart listens all the time, in every direction; it doesn't matter which way it faces. It only answers one question: *is that a drone?*
2. **Tell.** The first dart that hears one radios a few bytes to the receiver: *dart 8 heard a drone*. Darts also pass on their neighbours' alerts.
3. **Warn.** The tablet sounds the alarm. Warning is distance ÷ speed: from 1.2 mi out, at the 37–50 mph an FPV usually flies with a warhead, that is **about 1.5–2 minutes**. A sentry who hears it at the trench gets about 7 seconds ([the drones]({{ site.baseurl }}{% link research/threat-profile.md %})).

**It is a tripwire, not a microphone array.** An array combines its microphones to find a direction, which needs exact spacing and shared timing. The darts don't combine anything. Each one just says "I heard it", like the sensors on a fence. So no dart needs to know where the others are, and losing one only opens a gap.

## Spacing rules

- **Space darts one hearing range apart.** A drone crossing the line passes no farther than half a gap from the nearest dart, so this spacing hears it with room to spare.
- **That spare room buys height, or a dead dart.** It hears a drone midway between two darts up to about 0.87 times the hearing range above the ground. Or, for a drone flying low, it still covers the hole left by one dead dart. Not both at once.
- **Closer under trees,** and closer in strong wind, which can halve hearing range.

How much front 12 darts cover depends on that hearing range:

| How far one dart hears an FPV | Spacing | 12 darts cover | Heard between darts up to | Darts for a 1.9 mi front |
|---|---|---|---|---|
| 160–200 ft (the only measured figure for a cheap mic, a consumer drone in wind) | ~200 ft | ~0.45 mi | ~170 ft up | ~50 |
| 330 ft | 330 ft | ~0.75 mi | ~290 ft up | ~30 |
| **490 ft (the Saturday test's pass mark; the map above)** | **490 ft** | **~1.1 mi** | **~420 ft up** | **~20** |
| 980 ft (the optimistic case) | 980 ft | ~2.2 mi | ~850 ft up | ~10–12 |

Fibre-optic FPVs fly at about 65–165 ft, under every height in the table. At under $100 a dart (the parts list comes to about $17–50), 12 darts cost $200–1,200.

## Distances

| | Distance | Why |
|---|---|---|
| Line in front of the unit | 1.2–2.5 mi | Warning grows with distance. 2.5 mi gives about 3–4 minutes at usual FPV speed |
| Second line, if used | a few hundred yards behind the first | Which line trips first says whether a drone is coming in or going home. That sorts out the unit's own drones, and needs 24 darts, not 12 |
| Receiver | at the edge of the unit's tree line | The radio has to reach it from 1.2 mi or more. Trees in between are the hard part ([T9]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back)) |

## What a line misses

- **Drones that go round the end.** A line protects only the front it covers; the second drone in the animation shows this.
- **Drones flying higher than the darts can hear,** midway between two darts.
- **Fibre-optic FPVs already parked in ambush.** They sit silent by a road and lift off seconds before they strike.
- **Drones launched from inside the line.**
- **One line can't tell direction,** so on its own it alarms on the unit's own drones too, unless they fly at set times.

So the claim is narrower than "most drones": **most low-flying FPVs that cross the covered front, in light to moderate wind.** If one dart hears an FPV at about 490 ft, 12 darts cover about a mile. If it hears only 160–200 ft, the idea still works but needs three to five times as many darts. The Saturday test and T11 decide which.
