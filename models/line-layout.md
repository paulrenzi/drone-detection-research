---
title: A net in front of a unit
nav_tripwire: 1.5
---

# A net in front of a unit
{: .no_toc }

How many darts it takes to give a unit a minute's warning of a drone, seen from above and drawn to scale. Listening darts sit in a row about a mile out. The one that hears a drone radios its neighbour, and relay darts carry the alert, hop by hop, back to the unit. The animation runs ten times faster than real life.

The planning numbers, none measured yet:

- **Hearing: 656 ft (200 m).** A drone 165 ft up is heard about 635 ft away along the ground. [T11]({{ site.baseurl }}{% link mvp.md %}#layer-2-hear-a-drone-from-near-the-ground-t11) measures it.
- **Radio: 980 ft (300 m) per hop** near the ground. [T9]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back) measures it.
- **Drones: 60 mph, up to 165 ft up.** That is above the 37–50 mph an FPV usually flies with a warhead and below its 75 mph loaded maximum. Fibre-optic FPVs fly at 65–165 ft ([the drones]({{ site.baseurl }}{% link research/threat-profile.md %})).
- **Warning: at least a minute,** plus 5 s for recognition and relaying.

1. TOC
{:toc}

## The layout

<figure style="margin:12px 0 8px;max-width:600px">
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px">
<button type="button" class="btn btn-sm" data-layout="v">V: two trunks · 20 darts</button>
<button type="button" class="btn btn-sm" data-layout="trunk">One trunk · 15 darts</button>
</div>
<div id="line-layout"></div>
<figcaption style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px">
<button type="button" id="line-layout-play" class="btn btn-sm">Play</button>
<button type="button" id="line-layout-replay" class="btn btn-sm">Replay</button>
<span id="line-layout-status" aria-live="polite" style="font-weight:600;flex:1 1 220px"></span>
</figcaption>
<p id="line-layout-net" aria-live="polite" style="margin:6px 0 0;font-size:0.9em"></p>
</figure>
<script src="{{ '/assets/js/line-layout.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

Three drones fly in at 60 mph: one straight at the middle position, exactly between two front darts (the worst case), one from 30° to the left, and one from 45° to the right. **Tap any dart to knock it out** and see which darts can still get an alert home.

## How deep

Warning is distance ÷ speed. At 60 mph (88 ft a second), 65 s means hearing the drone **5,720 ft out**.

- **The worst case is a drone passing midway between two front darts.** With darts 980 ft apart, it is 490 ft from each as it crosses the row, and a dart hearing 635 ft along the ground first hears it about 400 ft before that.
- **So the front row sits 5,316 ft (1.01 mi) out.** Every drone heading for the unit is heard at least 5,720 ft away.
- **The trunk is 6 hops: 5 relay darts.** Relays only carry the message, so they sit a full hop apart and need no microphone.

**The radio sets the spacing, not the ear.** A 656 ft ear alone would allow front darts 1,270 ft apart. But each front dart has to reach its neighbour by radio, so they sit about 970 ft apart. A better ear than this saves almost nothing. A longer radio hop is what would cut darts.

## How wide

**A unit is small and spread out.** Kofman describes "nine men in three defensive positions" with "250 meters of open ground" between them, and about 15 soldiers per km of front on average ([hvylya](https://en.hvylya.net/news/2036-15-soldiers-per-kilometer-kofman-on-how-europe-s-biggest-war-emptied-the-front-line)). Neighbouring positions are reported 650–3,300 ft apart ([EMPR](https://empr.media/opinion/investigation/widening-gaps-on-the-front-why-ukraines-forces-struggle-to-hold-back-advancing-russians/)). So the map protects **three positions 820 ft apart, 1,640 ft across.**

**Each position gets ±45°.** A drone can be heard coming within 45° of straight on at any of the three positions, so the front row is a 90° arc split open by the unit's width, **1.7 mi from end to end.** Coming in flatter than 45° means starting farther to the side than in front. A crew a mile forward would have to launch more than a mile to the side, in front of the neighbouring unit. That is our reasoning; we found no source on how far to the side FPV crews launch. ±60° would take about 3–4 more front darts.

**The net is wider than the unit.** 1.7 mi of front is roughly what 40 soldiers hold at 15 per km. Neighbouring units can share one continuous front row, at about 5.5 darts per mile of front, and each adds only its own trunk.

## Depth against failure

| Layout | Darts | Longest route home | One dart knocked out |
|---|---|---|---|
| **One trunk** from the middle of the row | **15**: 10 listening + 5 relay | 11 hops | A trunk dart: the whole net goes silent. A front dart: every dart beyond it |
| **V: two trunks**, one from each end of the row | **20**: 10 listening + 10 relay | 9 hops | **Never more than 1 other dart.** Alerts go the other way along the front row to the other trunk |

For one position instead of three, the row is 9 darts: **14** with one trunk, **19** with the V.

**We recommend the V.** Its 5 extra darts are the cheapest insurance in the design: with one trunk, a single dead relay silences the whole net. 11 hops at 0.05–1 s each add at most about 11 s, and short hops allow the fast radio settings (airtime estimate).

## What it costs

Hobby prices, before any windscreen. The parts are on [the MVP list]({{ site.baseurl }}{% link mvp.md %}#shopping-list) and [Hardware v3]({{ site.baseurl }}{% link build-hardware.md %}#6-parts-to-buy-v3-4-darts-and-the-harness).

- **Listening dart, about $33:** Heltec V3 (about $22.50 from a 2-pack), INMP441 mic (about $2.50), 18650 cell ($5), rod and printed body (about $2).
- **Relay dart, about $30:** the same dart with no mic.
- **Receiver, about $22.50:** a Heltec V3, one at each position. P1 and P3 are 820 ft from P2, within one hop.

| Layout | Three positions | One position | If every dart cost the full $100 cap |
|---|---|---|---|
| One trunk | **~$550** (15 darts) | ~$470 (14) | $1,500 / $1,400 |
| V: two trunks | **~$700** (20 darts) | ~$620 (19) | $2,000 / $1,900 |

At 4 darts per drone sortie, 20 darts is 5 sorties.

## Spacing rules

- **Front row: no farther apart than the radio reaches,** about 980 ft, so each dart can pass an alert to its neighbour. At that spacing a drone 165 ft up crossing midway is still heard about 400 ft before the row.
- **Trunks: a full radio hop apart,** about 950 ft. That leaves little margin, so place a trunk dart closer wherever the ground or trees block the line.
- **Closer under trees and in strong wind,** which shorten both hearing and radio range.

## What the net misses

- **Fibre-optic FPVs already parked in ambush.** They sit silent by a road and lift off seconds before they strike.
- **Drones launched from inside the net,** drones flying higher than a dart can hear, and drones coming in flatter than 45°.
- **Direction.** A dart hearing a drone can't tell if it is the unit's own, unless the unit's drones fly at set times.

Everything here is geometry on the planning numbers above, not measurements. If a dart hears less than 656 ft, the front row needs more darts. If the radio reaches less than 980 ft, both the front row and the trunks do.
