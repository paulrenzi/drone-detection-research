---
title: How it works
nav_primary: 2.1
---

# How it works
{: .no_toc }

How many darts it takes to give a unit a minute's warning of a drone, where they go, and how they get there. Listening darts sit in a row about a mile out. The one that hears a drone radios its neighbour, and relay darts carry the alert, hop by hop, back to the unit. The map is drawn to scale, and its animation runs ten times faster than real life.

The planning numbers, none measured yet:

- **Hearing: 656 ft (200 m).** A drone 165 ft up is heard about 635 ft away along the ground. [T11]({{ site.baseurl }}{% link mvp.md %}#layer-2-hear-a-drone-from-near-the-ground-t11) measures it.
- **Radio: 980 ft (300 m) per hop** near the ground. [T9]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back) measures it.
- **Drones: 60 mph, up to 165 ft up.** That is above the 37–50 mph an FPV usually flies with a warhead and below its 75 mph loaded maximum. Fibre-optic FPVs fly at 65–165 ft ([the drones]({{ site.baseurl }}{% link research/threat-profile.md %})).
- **Warning: at least a minute,** plus 5 s for recognition and relaying.

1. TOC
{:toc}

## The net

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

1. **Hear.** Every listening dart listens all the time, in every direction. It only answers one question: *is that a drone?*
2. **Pass it back.** The dart that hears it radios a few bytes to its neighbour. Each dart relays an alert once, until it reaches the receiver at the unit. Each hop takes about 0.05–1 s depending on the radio's settings.
3. **Warn.** The receiver passes the alarm to the other positions and to a phone or tablet. Warning is distance ÷ speed, from wherever the drone was first heard.

**It is a tripwire, not a microphone array.** An array combines its microphones to find a direction, which needs exact spacing and shared timing. Here each dart only says "I heard it", and the net carries that home.

## How deep

At 60 mph (88 ft a second), 65 s means hearing the drone **5,720 ft out**.

- **The worst case is a drone passing midway between two front darts.** With darts 980 ft apart, it is 490 ft from each as it crosses the row, and a dart hearing 635 ft along the ground first hears it about 400 ft before that.
- **So the front row sits 5,316 ft (1.01 mi) out.** Every drone heading for the unit is heard at least 5,720 ft away.
- **Each trunk is 6 hops: 5 relay darts.** Relays only carry the message, so they sit a full hop apart and need no microphone.

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

**We recommend the V.** Its 5 extra darts are the cheapest insurance in the design: with one trunk, a single dead relay silences the whole net. 11 hops at 0.05–1 s each add at most about 11 s, and short hops allow the fast radio settings (airtime estimate). What it costs is on [Projected costs]({{ site.baseurl }}{% link costs.md %}).

## Laying the net

Nobody walks a mile forward to plant darts. A small drone does it, with no pilot flying it and no video link ([delivery drone]({{ site.baseurl }}{% link research/delivery-drone.md %})).

1. **Plan on a map.** The planning tool splits the net into drop points, groups them 4 per sortie, and writes one mission file per sortie ([software plan]({{ site.baseurl }}{% link build-software.md %})). It gets the unit's positions, the ±45° edges and the spacing from the numbers above. Each dart's ID is tied to its drop point, so the receiver can show which dart heard a drone.
2. **Load and launch.** Four darts hang on a harness under an ArduPilot quad, one release servo each ([3D models]({{ site.baseurl }}{% link build-3d.md %}#2-the-harness-loaded-with-four-darts)). The drone flies the mission with every radio off, drops each dart point first from a short hover, and flies home.
3. **Lay the trunks first, then the front row.** A dart can only report once the darts behind it are down. Laid from the unit outward, every new dart checks in through the net as soon as it lands, so the crew sees each one arrive.
4. **Check the net.** The receiver lists every dart that has checked in and how strong its link is. A missing or weak dart gets a spare dropped beside it on the next sortie.

**The V's 20 darts are 5 sorties:** two for the trunks and three for the front row. The longest flies about 1.1 mi out, along about half a mile of the row and back. An X500-class quad with 4 darts is estimated at 11–12 minutes' hover ([Hardware]({{ site.baseurl }}{% link build-hardware.md %})); whether a sortie that long fits one battery is test T13.

### Finding the drop points when GPS is jammed

GPS is jammed routinely at the front ([field conditions]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)). The darts carry no GPS. A dart's position is its planned drop point, corrected by where the drone's flight log says it released. The drone needs to know where it is, in this order of cost:

| Method | What it needs | Good enough? |
|---|---|---|
| **Plain GPS** | Nothing extra | Where it isn't jammed. Each flight log records where GPS failed or jumped, so the unit learns its own map of jamming |
| **Short legs on compass, barometer and optical flow** from a point the crew can confirm by eye | A downward optical-flow camera and rangefinder | Drifts over distance with no fixed reference, so legs stay short ([ArduPilot](https://ardupilot.org/copter/docs/common-non-gps-navigation-landing-page.html)) |
| **Computer vision: matching the camera's view to satellite maps** | A camera, an onboard computer and stored map tiles | The upgrade if GPS proves unusable. Open research code exists ([WildNav](https://github.com/TIERS/wildnav)), but nothing found plugs into ArduPilot. Ukrainian systems doing this are reported but proprietary |
| **By hand** | Troops walking in at night | Only for the trunk darts nearest the unit, an inference |

A downward camera could also record each drop, so the crew can check after landing that a dart stood upright. That adds weight but no radio link (an idea, untested).

## What placement has to get right

**Accuracy decides the dart count.** The 20-dart V assumes every dart lands on its point. A dart that lands off its point can end up beyond radio reach of its neighbour. So the plan has to shrink every gap by twice the expected drop error:

| Drop error | Planned spacing | Front row | Relays per trunk | V total |
|---|---|---|---|---|
| none | 980 ft | 10 | 5 | **20** |
| ±33 ft | 914 ft | 11 | 6 | **23** |
| ±66 ft | 848 ft | 12 | 6 | **24** |
| ±160 ft | 660 ft | 14 | 8 | **30** |

How close a drop lands is test T13. The tripwire page's working figure, that drops 66–160 ft off still make a line, needs revisiting: at 160 ft off, this net needs 30 darts, not 20.

**The other requirements:**

- **Land upright, point first, in soil.** The tip goes in about 2.8 in, holding the microphone about 20 in up. Whether the fins turn a dart nose-down in time is the first drop test ([dart model]({{ site.baseurl }}{% link build-3d.md %}#why-it-should-fall-point-first)).
- **Nothing solid between neighbours.** A ridge, a building or a thick tree belt between two darts can break a hop. Plan hops along open ground and shorten them under trees, which also shortens hearing.
- **Relay darts keep their radio listening.** A listening dart can sleep until it hears something, but a relay has to be awake to catch its neighbour's packet. How long its cell lasts in the cold is unknown until the battery test (T12). Relays may need re-laying sooner than listening darts.
- **A receiver at every position.** P1 and P3 sit 820 ft from P2, within one hop, so the receiver at P2 passes the alarm on.
- **Keep the unit's own drones out of the alarm.** Ukrainian FPVs sound like Russian ones. The proposed answer is to alarm only on drones heading inbound, outside the unit's own flight times (test T15).
- **Re-lay before the cells run out,** and replace darts lost to shelling. The darts' battery reports forecast when.

## What the net misses

- **Fibre-optic FPVs already parked in ambush.** They sit silent by a road and lift off seconds before they strike.
- **Drones launched from inside the net,** drones flying higher than a dart can hear, and drones coming in flatter than 45°.
- **Direction.** A dart hearing a drone can't tell if it is the unit's own, unless the unit's drones fly at set times.

Everything here is geometry on the planning numbers above, not measurements. If a dart hears less than 656 ft, the front row needs more darts. If the radio reaches less than 980 ft, both the front row and the trunks do.
