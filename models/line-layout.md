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
2. **Pass it back.** The dart that hears it radios a few bytes to its neighbour. Each dart relays an alert once, until it reaches the **root dart**, placed by hand beside the receiver at P2, which repeats it once more. Each hop takes about 0.05–1 s depending on the radio's settings.
3. **Warn.** Every position has a receiver within a hop of the root dart. Receivers never transmit; each passes the alarm to a phone or tablet. Warning is distance ÷ speed, from wherever the drone was first heard. Receivers beside the unit's own jammers go deaf whenever those are on, so the model now proposes a root dart about 1,000 ft forward with a wire or fibre to the positions ([Jamming](#jamming)).

**It is a tripwire, not a microphone array.** An array combines its microphones to find a direction, which needs exact spacing and shared timing. Here each dart only says "I heard it", and the net carries that home.

## How deep

At 60 mph (88 ft a second), 65 s means hearing the drone **5,720 ft out**.

- **The worst case is a drone passing midway between two front darts.** With darts 980 ft apart, it is 490 ft from each as it crosses the row, and a dart hearing 635 ft along the ground first hears it about 400 ft before that.
- **So the front row sits 5,316 ft (1.01 mi) out.** Every drone heading for the unit is heard at least 5,720 ft away.
- **Each trunk is 6 hops: 5 relay darts.** Relays only carry the message, so they sit a full hop apart and need no microphone.

**The radio sets the spacing, not the ear.** A 656 ft ear alone would allow front darts 1,270 ft apart. But each front dart has to reach its neighbour by radio, so they sit about 960 ft apart. A better ear than this saves almost nothing. A longer radio hop is what would cut darts.

## How wide

**A unit is small and spread out.** Kofman describes "nine men in three defensive positions" with "250 meters of open ground" between them, and about 15 soldiers per km of front on average ([hvylya](https://en.hvylya.net/news/2036-15-soldiers-per-kilometer-kofman-on-how-europe-s-biggest-war-emptied-the-front-line)). Neighbouring positions are reported 650–3,300 ft apart ([EMPR](https://empr.media/opinion/investigation/widening-gaps-on-the-front-why-ukraines-forces-struggle-to-hold-back-advancing-russians/)). So the map protects **three positions 820 ft apart, 1,640 ft across.**

**Each position gets ±45°.** A drone can be heard coming within 45° of straight on at any of the three positions, so the front row is a 90° arc split open by the unit's width, 1.7 mi long. **The row runs on 300 ft past both 45° lines, 2.0 mi from end dart to end dart,** so a net rotated a few degrees by compass error still covers both edges ([Drop, then confirm](#drop-then-confirm)). Coming in flatter than 45° means starting farther to the side than in front. A crew a mile forward would have to launch more than a mile to the side, in front of the neighbouring unit. That is our reasoning; we found no source on how far to the side FPV crews launch. ±60° would take about 3 more front darts.

**The net is wider than the unit.** 1.7 mi of front is roughly what 40 soldiers hold at 15 per km. Neighbouring units can share one continuous front row, at about 5.5 darts per mile of front, and each adds only its own trunk.

## Two trunks, for redundancy

**The net always has two trunks,** one from each end of the front row: **22 darts** on open, flat ground, 12 in the front row and 10 relays, plus the root dart placed by hand. For one position instead of three, the row is 11 darts, so 21 in all. Laying them takes more: on flat ground the [lay model](#laying-the-net) uses about 29 darts and 8 sorties, after bad landings and short hops. Real ground takes more again: on its example sector it plans 25 and uses about 35.

- **No single dart can silence it.** Knocking out any one dart cuts off at most 1 other. If a trunk dart dies, alerts run the other way along the front row to the other trunk.
- **A single trunk is not offered.** It would save 5 darts, but one dead relay would silence the whole net, and every front dart beyond a dead one would go quiet.
- **The longest route home is 11 hops,** counting the root dart. At 0.05–1 s a hop that adds at most about 11 s, so the fast radio settings matter, and short hops allow them (airtime estimate).

What the package costs is on [Projected costs]({{ site.baseurl }}{% link costs.md %}).

## Laying the net

Nobody walks a mile forward to plant darts. A small drone does it, with no pilot flying it and no video link ([delivery drone]({{ site.baseurl }}{% link research/delivery-drone.md %})). This section is a working model of that job: a planner and simulator, [`lay_model.py`](https://github.com/paulrenzi/tripwire/blob/main/tools/laymodel/lay_model.py), that plans a net on a map, checks every sortie against the battery and the wind, writes the ArduPilot missions, and then lays the net 1,000 times with drop errors, bad landings and radio fading.

<figure style="margin:12px 0 8px;max-width:600px">
<video controls muted playsinline loop preload="metadata" poster="{{ '/assets/video/lay-net-poster.png' | relative_url }}" style="width:100%;display:block;border:1px solid #ddd">
<source src="{{ '/assets/video/lay-net.mp4' | relative_url }}" type="video/mp4">
</video>
<figcaption style="font-size:0.9em;margin-top:6px">One lay from the model, about 1 min 50 s. An example sector (invented, to scale): two windbreaks, a 50 ft ravine, ground rising 50 ft toward the front, an enemy salient and a 9 mph wind toward it. GPS is jammed. Every position, battery reading and relay shown comes from the model's output.</figcaption>
</figure>

### How a lay works

1. **Scout.** The unit's own recon drone flies the planned row the day before. Map data is months old; craters, wires and fallen trees are not on it. The crew moves any point the footage puts on bad ground.
2. **Plan.** The crew gives the tool its positions, the **enemy's forward edge as a line** (not just a direction), and the wind forecast. The tool reads a free elevation map (Copernicus GLO-30, about 100 ft grid) and a free land-cover map (ESA WorldCover, about 33 ft grid). It keeps every drop point off trees, off ravine floors and at least 650 ft short of the enemy edge, shortens every hop that crosses a windbreak or a rise, and runs the front row 300 ft past both 45° lines. Then it groups the darts into sorties that pass the battery check and writes one mission per sortie: terrain-relative heights, a ground speed for every leg, a release step for every dart.
3. **Fly.** The drone follows the terrain using its downward lidar, and releases each dart from 33 ft above the ground, not above the launch point. With GPS working it cruises at 100 ft. With GPS jammed it cruises at 35 ft, where its optical-flow sensor stays inside the lidar's 39 ft range, and climbs only to cross the windbreaks the map shows.
4. **Confirm every dart** (table below). Each dart sends "landed" with its tilt, its neighbour relays it, and every relay carries the relayer's ID. The dart that closes the front row needs relays from both sides. A point gets at most 3 extra darts; after that it is left for a repair sortie. A hand-placed **root dart** beside the receiver relays for the first dart on each trunk, because the receiver never transmits.
5. **Check the battery before every drop.** The drone must be able to release here and still get home into the wind plus a 5 mph gust, with 20% left. If it can't, it flies home with the darts still on board, and they go on the next sortie.
6. **Turn round.** Swap the pack, reload 4 darts, scan their IDs. With 6 packs and a 2-channel charger, the drone never waits for a charge.

**What the drone's receive-only radio hears after each drop, and what it does next:**

| The drone hears | It means | Next |
|---|---|---|
| A relay from the planned neighbour | Linked | Fly on |
| "Landed" but no relay | Out of reach | Next dart 300 ft back toward the neighbour |
| "Landed, tilted" | Lying flat or in a tree | Next dart on the same spot |
| Nothing | A dud | Next dart on the same spot |

If a sortie runs out of darts or battery partway through, the points it didn't finish go first on the next sortie.

### What the model found

The example sector, 1,000 lays per row. **"Whole"** means every drone track within 45° of each position is heard at least 55 s out. That is 5 s short of the minute target, which leaves room for small drop errors.

| Case | Whole | Survives any one loss | Darts used | Darts, 9 lays in 10 | Sorties | Hours |
|---|---|---|---|---|---|---|
| The first 20-dart plan, GPS working, no confirm | 0% | 0% | 20 | 20 | 5.1 | 1.0 |
| This plan (25 darts), GPS working, no confirm | 5% | 0% | 25 | 25 | 7.1 | 1.3 |
| This plan, GPS working, confirm | 100% | 99% | 32.2 | 36 | 8.6 | 1.9 |
| **This plan, GPS jammed, confirm** | **99%** | **93%** | **34.9** | **40** | **9.3** | **2.2** |
| … if 95% of darts land upright, not 85% | 100% | 98% | 30.7 | 34 | 8.2 | 1.7 |
| … if the radio hop is 800 ft, not 980 | 100% | 94% | 40.9 | 46 | 10.8 | 2.9 |
| … if the compass is off 4°, not 2° | 91% | 87% | 35.1 | 40 | 9.3 | 2.2 |
| … in a 15 mph wind | 100% | 95% | 34.8 | 40 | 10.3 | 2.7 |
| … at 14 °F, with packs not kept warm | 99% | 95% | 34.8 | 40 | 17.6 | 6.3 |

- **A lay takes about 35 darts and 9 sorties, not 20 and 5.** The 25 planned darts are the floor. Darts that land badly (15%, assumed) and hops that fall short take about 10 more.
- **Without confirmation, the net is almost never whole.** 980 ft is the hop that works 9 times in 10. With about 25 links, nearly every lay has one that fails, and nothing on the ground says which.
- **On real ground, the first plan fails.** Hops across a windbreak lose about 4 dB, so the 980 ft hop becomes about 760 ft. Only 6 of the first plan's 20 darts would reach the unit, even with perfect drops.
- **Wind:** 7 sorties up to 12 mph, 8 at 15 mph and 13 at 18 mph. Above about 15 mph, don't lay.
- **Cold packs double the sorties.** Keep them warm until launch.
- **The drone is a consumable.** At 2% lost per sortie (a guess), a lay costs about 0.2 drones: 2–3 a year at four-week re-lays.

### Holes found, and the fixes now in the model

| Hole | What it did | Fix | Cost |
|---|---|---|---|
| The plan ignored the ground | Darts in trees and ravines; hops across windbreaks out of reach | Elevation and land-cover checks in the planner | Free data |
| Mission heights were relative to the launch point | Over ground rising 50 ft, a 33 ft release height would put the drone into the ground | Terrain following plus a downward lidar | MTF-01P flow and lidar, ~$42 |
| Optical flow loses its scale above the lidar's range | Jammed-GPS navigation drifts at 100 ft | Cruise at 35 ft when jammed; climb only over mapped belts | None |
| Optical flow needs light | At night with GPS jammed, only the compass is left | When GPS is jammed, lay at dawn or dusk | None |
| Without GPS, ArduPilot has no origin, and so no position to look up magnetic declination | Missions won't run, or headings are off by the local declination | The tool sets the origin and the declination at the launch point before each sortie ([ArduPilot](https://ardupilot.org/copter/docs/common-non-gps-navigation-landing-page.html)) | None |
| Nothing checked that a link worked | 95% of lays broken somewhere | Drop, then confirm, on every dart | Receive-only radio, ~$20 |
| Any relay counted as a confirmation | A dart out of reach of its planned neighbour could pass on a relay from the dart before it | Relays carry the relayer's ID; the closing dart needs both sides | 2 bytes a packet |
| The receiver can't transmit | The first dart on each trunk can't be confirmed, and P2 can't pass an alarm to P1 and P3 | A hand-placed root dart beside the receiver relays every alert once more, within one hop of all three positions | One dart |
| A bad landing was invisible | A flat or snagged dart checks in normally but hears and radios much worse | An accelerometer in every dart | ~$1–2 a dart |
| The harness drops in a fixed order | A spare is just the next dart, and relay darts can't stand in for listening darts | Every dart gets a microphone. Points a sortie runs out for move to the next one | ~$3 a former relay dart |
| End darts sat 635 ft inside the 45° lines | Every drone track along a 45° line only grazed a dart, and a rotation of 3° left one edge unheard | Ends 300 ft past the 45° lines | One dart |
| A fixed 22 mph cruise | Against 14 mph, the drone couldn't take even one dart to the end of a trunk and get home | Least-energy ground speed per leg (ArduPilot DO_CHANGE_SPEED); battery check with gust margin before every drop | None |
| 2 packs and a 1-channel charger | A lay took 5.2 h | 6 packs and a 2-channel charger: about 2 h | ~$340 |
| Cold packs | Up to 25% less capacity (assumed) | An insulated bag | ~$20 |

**Still open, not modelled:**
- The drone's return shows the enemy where it launched from. Launch 300–500 ft from the positions, and vary the spot.
- The unit's own trench jammers cover our 900 MHz band. A [jamming model](#jamming) now says what that does: it deafens receivers at the positions, so the root needs a wire. T19 has to measure it.
- The trunks point at the positions.
- A sortie can't be recalled.
- Handing the net over to a relieving unit isn't designed.

### What each test now has to report

The model turns on five numbers. Each test should report a spread, not one figure:

- **T9:** the hop that works 90% of the time, and how much it varies from place to place (4 dB assumed).
- **T10:** the share of drops that land upright in plough, pasture and frozen ground (85% assumed). This is the cheapest saving: at 95%, each lay uses 4 fewer darts.
- **T13:** power against airspeed with 4 darts, and the battery each sortie uses.
- **T14:** compass error with GPS jammed, split into the error shared by a whole day and the change from one sortie to the next (2° and 0.7° assumed). At 4°, 9% of lays leave a gap. Also the lidar's real range over dark plough and snow: the 35 ft cruise assumes the full 39 ft.
- **T12:** pack capacity at 14 °F, warm and cold.

### What the drone knows

**Coordinates, a few rules and its own sensors.** It knows nothing about north, the enemy or spacing.

- **North and position:** GPS and compass, or with GPS jammed, compass, optical flow and lidar from an origin set at launch (below).
- **The enemy:** only through the plan, which keeps every point 650 ft short of the forward edge the crew drew.
- **Spacing:** proved by radio, one relay at a time, never measured.
- **The darts know nothing.** "Dart 7" is a place only because the drone's log ties that ID to where it was released.

### Finding the drop points when GPS is jammed

GPS is jammed routinely at the front ([field conditions]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)). The darts carry no GPS. A dart's position is where the drone's log says it released. The drone needs to know where it is, in this order of cost:

| Method | What it needs | Good enough? |
|---|---|---|
| **Plain GPS** | Nothing extra | Where it isn't jammed. Each flight log records where GPS failed or jumped, so the unit learns its own map of jamming |
| **Compass, barometer and optical flow** from an origin set at launch | The MTF-01P flow and lidar sensor (now in the kit), daylight, a 35 ft cruise | The model's choice under jamming. Drifts with distance, but darts in one sortie drift together, and drop, then confirm repairs the joins ([ArduPilot](https://ardupilot.org/copter/docs/common-non-gps-navigation-landing-page.html)) |
| **Computer vision: matching the camera's view to satellite maps** | A downward camera, a Jetson Orin NX-class computer (several hundred dollars, est.) and stored map tiles | Not used yet; the upgrade if T14 shows a compass error well over 2°. Best open candidate: [NGPS](https://github.com/snktshrma/ngps_flight) (MIT licence, ROS 2, feeds ArduPilot), whose author reports about 10–20 ft error over 5 real flights at 200–490 ft up ([paper](https://arxiv.org/abs/2607.18936)). [gnss-denied-nav](https://github.com/koksalan/gnss-denied-nav) (MIT) reports a 79 ft median on unseen regions and refuses to fix when seasons change the ground; simulation and datasets only. [WildNav](https://github.com/TIERS/wildnav) relies on SuperGlue, whose licence bars commercial use. Ukrainian systems doing this are reported but proprietary |
| **By hand** | Troops walking in at night | The root dart beside the receiver, and trunk darts near the unit (an inference) |

## What placement has to get right

**Accuracy decides the dart count, unless every link is confirmed.** The 22-dart net assumes every dart lands on its point. A dart that lands off its point can end up beyond radio reach of its neighbour. So the plan has to shrink every gap by twice the expected drop error:

| Drop error | Planned spacing | Front row | Relays per trunk | Total |
|---|---|---|---|---|
| none | 980 ft | 12 | 5 | **22** |
| ±33 ft | 914 ft | 13 | 6 | **25** |
| ±66 ft | 848 ft | 14 | 6 | **26** |
| ±160 ft | 660 ft | 18 | 8 | **34** |

How close a drop lands is test T13. The tripwire page's working figure, that drops 66–160 ft off still make a line, needs revisiting: at 160 ft off, this net needs 34 darts, not 22. The [lay model](#laying-the-net) takes the other route: it plans at the full hop and confirms every link as it is made, which costs fewer darts than planning for the error.

**The other requirements:**

- **Land upright, point first, in soil.** The tip goes in about 2.8 in, holding the microphone about 20 in up. Whether the fins turn a dart nose-down in time is the first drop test ([dart model]({{ site.baseurl }}{% link build-3d.md %}#why-it-should-fall-point-first)).
- **Nothing solid between neighbours.** A ridge, a building or a thick tree belt between two darts can break a hop. Plan hops along open ground and shorten them under trees, which also shortens hearing.
- **Relay darts keep their radio listening.** A listening dart can sleep until it hears something, but a relay has to be awake to catch its neighbour's packet. How long its cell lasts in the cold is unknown until the battery test (T12). Relays may need re-laying sooner than listening darts.
- **A receiver at every position, and a root dart.** Receivers never transmit. Every alert ends at a dart placed by hand about 250 ft in front of P2, which relays it once more; P1 and P3 are about 860 ft from it, within one hop, so all three receivers hear it. If the root dart dies, alerts still reach P2 directly, but P1 or P3 can miss them, so the roll call checks it first and the crew replaces it by hand.
- **Keep the unit's own drones out of the alarm.** Ukrainian FPVs sound like Russian ones. The proposed answer is to alarm only on drones heading inbound, outside the unit's own flight times (test T15).
- **Re-lay before the cells run out,** and replace darts lost to shelling. The darts' battery reports forecast when.

## When it breaks

<figure style="margin:12px 0 8px;max-width:600px">
<div id="repair-model"></div>
<figcaption style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px">
<button type="button" id="repair-play" class="btn btn-sm">Play</button>
<button type="button" id="repair-replay" class="btn btn-sm">Replay</button>
<span id="repair-status" aria-live="polite" style="font-weight:600;flex:1 1 220px"></span>
</figcaption>
</figure>
<script src="{{ '/assets/js/repair.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

Same map, with time compressed. A relay is knocked out, found by the roll call and replaced; then a re-lay sortie flown on a compass 3° off is caught by drop, then confirm.

| Failure | What the unit loses | Fix | Our cost |
|---|---|---|---|
| **A front dart** | A blind gap about 660 ft wide: its neighbours end up 1,926 ft apart and each hears 635 ft | One sortie drops a dart on its point | ~$27–31 |
| **A trunk dart** | No coverage, but the net is down to one trunk | Same, and first | ~$27–31 |
| **Two darts** | One on each trunk silences the net: 36 of the 231 possible pairs do that | Repair after the first loss | Per dart |
| **The receiver** | Everything, until swapped | By hand, at the position | ~$22 |
| **The root dart** | P1 and P3 may miss alerts; P2 still hears. With the proposed forward roots on fibre, one trunk | By hand, at the position | ~$29 |
| **Cells run down** | Darts drop out one by one | A re-lay: about 35 darts, 9 sorties | ~$1,190, with drone wear |
| **The drone** | Any repair or re-lay | A new quad | ~$850–920 |
| **The unit's own jammer on** | Receivers at the positions go deaf: everything, for as long as it is on | Forward roots on a wire or fibre ([Jamming](#jamming)) | ~$60–100 (est.) |
| **An enemy jammer near the front row** | Darts within a few hundred feet of it can't relay; a LoRa hunter would open a gap | Pull the row back from it; a second band, 433 MHz (untested) | none |

**The repair model.** The receiver lists the darts that have gone quiet, the crew taps "re-drop", and the planning tool writes one mission for up to 4 darts. The flight to the farthest point is about 1.1 mi and about 10 minutes. A dead trunk dart or front dart goes on the next sortie; anything else waits for the next re-lay. Battery wear is about $0.30 a sortie. **The drone is the hidden cost:** a 2% chance of losing it adds about $20 to every sortie, as much as the dart it carries. So repairs are batched, and a spare drone is worth quoting.

**Roll call: how the unit knows a dart is dead** (a design change). As planned, check-ins aren't relayed ([software plan]({{ site.baseurl }}{% link build-software.md %})), so a dead dart goes unnoticed. Proposed: once a day every dart sends one check-in and every other dart relays it once. That is about 400 short bursts across the net, a second or two of airtime per dart. A dart missing from the roll call is named from the plan within a day.

### Drop, then confirm

**Compass navigation over a mile is worse than the placement budget.** With GPS jammed, each degree of compass error puts a dart 93 ft sideways at 5,316 ft; 3° is about 280 ft. Inside one sortie that mostly doesn't matter: every drop is off the same way, and consecutive drops about 960 ft apart are only about 50 ft off each other. **The joins between sorties break.** Each sortie starts again from the unit, and the sortie that closes the front row has two joins; at 3°, one closes to about 680 ft and the other opens to about 1,250 ft.

**Proposed fix (untested):** the drone carries a receive-only LoRa board (about $20, transmits nothing).

1. Each dart sends "landed" once it is down, and its neighbour relays it, once.
2. The drone, still hovering, hears that relay. That proves the new dart reached its neighbour.
3. If it hears nothing, or the dart closing the row is relayed from one side only, the drone drops a spare about 300 ft toward the silent neighbour's logged point and listens again.

That measures every link as it is made, so the drone never needs to know where it is to within a hop, and a failed join costs one spare. Absolute error is cheap in the middle of the row, at most about 3 s of warning for 280 ft. **It is not cheap at the ends:** a net rotated 3° moves an end dart about 280 ft along the row, and the old ends, 635 ft inside the 45° lines, then left one edge unheard. The lay model puts the ends 300 ft past the 45° lines instead, and confirms every dart, not just the joins ([Laying the net](#laying-the-net)).

**If the planning numbers are wrong, the fix is more darts, not a redesign:**

| Radio hop | Front darts | Relays per trunk | Total |
|---|---|---|---|
| 650 ft | 17 | 8 | 33 |
| 800 ft | 15 | 7 | 29 |
| **980 ft (plan)** | **12** | **5** | **22** |
| 1,250 ft | 10 | 4 | 18 |

## Jamming

{: .warning }
> Estimates from a link-budget model, [`jam_model.py`](https://github.com/paulrenzi/tripwire/blob/main/tools/jamming/jam_model.py), run on the example sector with every jammer on all the time. Jammer powers and heights are assumed, not measured. [T19]({{ site.baseurl }}{% link research/open-questions.md %}) measures it.

**Jamming is everywhere near the front, and it covers our band.** RUSI counted at least one major Russian jamming system per 6 mi (10 km) of front ([via Wikipedia](https://en.wikipedia.org/wiki/Electronic_Warfare_Troops_of_the_Russian_Federation)). "Most mobile jammers" cover 868–915 MHz, and FPV control links run on the same LoRa chips our darts use ([Armada International, Feb 2026](https://www.armadainternational.com/2026/02/the-curran-papers-no-5-jamming-uninhabited-aerial-vehicle-video-signals-electronic-warfare/)). So the jammers on both sides are already built against our radio. More in [field conditions]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare).

**What decides it is distance, not how common jamming is.** A jammer is a transmitter like a dart. It spreads its power across the band, about 640 of our 125 kHz channels, so a 20 W trench jammer puts less into our channel than a dart's 0.16 W does. Near the ground its signal fades as fast as ours. So it blinds a dart only from closer than about 0.4 of a hop:

| Jammer (assumed) | Blinds a dart within | Worst case |
|---|---|---|
| Trench jammer, 20 W, 5 ft up | **about 390 ft** | 1.1 mi |
| Vehicle jammer, 100 W, 8 ft up | about 740 ft | 2.2 mi |
| Jammer on a mast, 50 W, 33 ft up | about 1,260 ft | 3.7 mi |
| A LoRa hunter like Tishina, 20 W all in our channel | about 1,970 ft | 5.7 mi |

The worst case assumes the jammer's signal crosses open ground with none of the losses that hold our own hop to 980 ft. That is nearer the truth for a jammer up high than for one in a trench. A jammed dart still hears drones and still transmits. It can't receive, so it can't relay.

**What that does to the net:**

| Jammers on | Main estimate | Worst case |
|---|---|---|
| The enemy's trench jammers, every 1,640 ft along their edge | Net whole, 60 s | Net silent |
| A LoRa hunter every 1,640 ft along their edge | 7 front darts can't relay; gaps in the row | Net silent |
| **Our own trench jammers, at the positions** | **Receivers deaf: net silent** | Net silent |
| Ours, with the root 1,000 ft forward on a wire to the positions | Net whole, 60 s, 24 darts | Net silent |

- **The first threat is our own jammers.** The plan puts the receivers in the positions, beside the unit's trench jammers, so whenever those are on, the net is deaf. **Proposed fix:** a root dart at the foot of each trunk, about 1,000 ft forward, out of their reach, each sending alerts home down its own fibre or wire. Nothing at a position then has to receive by radio. The drone can pay out the fibre as it flies the root out, the way fibre-optic FPVs do: about 0.2 mi of FPV fibre, about $10 at today's $20–35 a km ([DroneXL, May 2026](https://dronexl.co/2026/05/11/ukraine-fiber-optic-spool-price-ai-data-center-demand/)). The link only has to run one way, so the root needs just an LED that flashes when there is an alert, and the dugout end draws on the unit's power. A design idea, untested; about $60–100 for both roots and the wire between positions (est.).
- **Enemy jammers matter only near their edge,** on the main estimate. A LoRa hunter would open gaps in the front row. Pulling the row back from a known jammer costs warning; a second band at 433 MHz, which most mobile jammers don't list ([Armada](https://www.armadainternational.com/2026/02/the-curran-papers-no-5-jamming-uninhabited-aerial-vehicle-video-signals-electronic-warfare/)), costs a second radio. Both need T19.
- **Jammers aren't always on.** Crews switch them on when a detector warns ([problem check]({{ site.baseurl }}{% link research/problem-check.md %})). The net's alert comes a minute before the drone, so it may get home before the jammers go on. Not modelled.
- **Why not fibre everywhere?** Fibre can't be jammed and gives off nothing to find. But an air-dropped row can't share one: every dart would need its own run, and a single cut would silence everything beyond it. Fibre fits the fixed links that sit beside jammers: the roots here, and the posts along a road ([Guarding a road]({{ site.baseurl }}{% link models/route-guard.md %}#jamming-and-a-wire-along-the-road)).
- **Which case is real decides the project.** If the main estimate holds, jamming is a placement problem: keep radios a few hundred feet from jammers. If the worst case holds, a radio net cannot work near the front at all. T19 now has to measure at range from a jammer, not only beside one.

## What the net misses

- **Fibre-optic FPVs already parked in ambush.** They sit silent by a road and lift off seconds before they strike. A guard on the road itself is the answer: posts that hear them land ([Guarding a road]({{ site.baseurl }}{% link models/route-guard.md %})).
- **Drones launched from inside the net,** drones flying higher than a dart can hear, and drones coming in flatter than 45°.
- **Direction.** A dart hearing a drone can't tell if it is the unit's own, unless the unit's drones fly at set times.

Everything here is geometry on the planning numbers above, not measurements. If a dart hears less than 656 ft, the front row needs more darts. If the radio reaches less than 980 ft, both the front row and the trunks do.
