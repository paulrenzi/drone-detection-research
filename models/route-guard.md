---
title: Guarding a road
nav_primary: 2.15
---

# Guarding a supply road
{: .no_toc }

A net in front of a position protects people who are a few yards from a dugout, where seconds of warning already help. People on a road have nowhere to go in seconds. About half of casualties come in the rear, during rotation and resupply ([RUSI, Feb 2025](https://static.rusi.org/tactical-developments-third-year-russo-ukrainian-war-february-2205.pdf)), and fibre-optic FPVs now hunt roads and land beside them to wait ([Trench Art](https://www.trenchart.us/p/russias-best-drones-lie-in-wait-beside)). This page is a working model of a permanent guard on a road: [`route_model.py`](https://github.com/paulrenzi/tripwire/blob/main/tools/routemodel/route_model.py), built on the [lay model]({{ site.baseurl }}{% link models/line-layout.md %}#laying-the-net), run on two invented 4 mi roads. Nothing in it is measured yet.

## Short answer

- **A guard has two parts.** Posts stand along the road, placed by hand. A fence of air-dropped darts runs about a mile out on every side a drone can come from. Every 2 mi a **tip dart** in the fence sends its alerts to a post down an FPV fibre, as on the [position net]({{ site.baseurl }}{% link models/line-layout.md %}#the-fibres-and-the-base-box), so nothing between the fence and the road uses radio.
- **The fence gives the minute.** In the model, every drone flying in to strike the road, from anywhere within 60° of the enemy, is heard at least 60 s before it can reach the road; the median is 72–102 s. Posts alone give 4–9 s.
- **The posts catch drones landing to wait.** Every landing within 300 ft of the road is heard, about 340 ft from the post that hears it loudest. The alert, "drone waiting near post 17", stays up until someone clears it.
- **How many:** 21 posts and 35–58 darts for 4 mi of road, **about 14–20 a mile**. A road running toward the front costs more than one running along it, because the fence has to wrap both sides and the forward end. Fibre took out the 25–35 relay darts the radio trunks needed.
- **What it costs us:** a package of about **$5,700–6,800**, then about **$37–56k a year** at four-week cells, **$9–14k a mile**. Posts alone cost about $1,400 and $6,500 a year; they find landings but give no minute.
- **Jamming: the trucks' own jammers are the threat, and a wire answers it.** A truck's jammer deafens its own receiver and the posts near it, so a radio-only guard tells a jamming truck nothing on the move. Posts on a cable along the verge, each with a hooded lamp facing the road, keep the warning in the model (100% of tracks with a minute) for about $200 a mile more (est.). In the worst case for jamming, the truck's jammer reaches the fence too, and the fibres only partly save it.
- **What it misses:** drones parked before it was laid, drones carried in on foot, and landings more than about 600 ft from the road. Our own drone crews, who live in this strip, are a risk worse here than at a position.

1. TOC
{:toc}

## The guard

<figure style="margin:12px 0 8px;max-width:600px">
<div id="route-model" data-src="{{ '/assets/data/route-demo.json' | relative_url }}"></div>
<figcaption style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px">
<button type="button" id="route-play" class="btn btn-sm">Play</button>
<button type="button" id="route-replay" class="btn btn-sm">Replay</button>
<span id="route-status" aria-live="polite" style="font-weight:600;flex:1 1 220px"></span>
</figcaption>
</figure>
<script src="{{ '/assets/js/route.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>

The model's example road, to scale, with the enemy to the right: 4 mi running toward the front, from a depot 5.7 mi back to 1.7 mi behind our positions. Every position, hearing and warning comes from the model; time runs ten times faster, except in the last scene.

1. **Hear.** Every dart and post listens all the time. A fence dart that hears a drone passes "drone, heading in" to its neighbour.
2. **Get it to the road.** The alert hops along the fence to the nearest tip dart, at most 6 hops, and the tip sends it down its fibre to a post as flashes of a small laser. Light only goes one way, home, and a heartbeat every 10 s shows the fibre is whole.
3. **Spread it along the road.** Posts relay every alert along the road. Their 2 ft whips on stakes should reach about 2,500 ft, more than two posts' spacing, so one dead post breaks nothing (an estimate; T9 measures it). Proposed: a cable along the verge as well, so posts share alerts where radio is jammed ([below](#jamming-and-a-wire-along-the-road)).
4. **Show it.** Every vehicle carries a receiver that never transmits, so a truck gives nothing away. It and a board at each checkpoint show which stretches are hot. Drivers check before setting out; anyone on a hot stretch stops under cover.
5. **Count in and out.** A drone heard crossing the fence inward stays on the count until it is heard leaving, heard landing, or cleared.

## Two alerts

| Alert | What sets it off | What it says | When it clears |
|---|---|---|---|
| **Inbound** | A fence dart hears a drone | "Hot: mile 0.7 to 2.7". The stretch a drone could reach | The fence hears it leave, or a set time passes with nothing heard |
| **Waiting** | A post hears a drone close by, then nothing: no strike, nothing heard leaving | "Drone waiting near post 17, mile 3.2" | A team clears it |

**The waiting alert is the one nothing else gives.** A drone waiting with its motors off is silent, but it had to fly there, and it lands within earshot of a post. It then sits on the ground for hours, unable to move fast. That is when to deal with it. In the model, the stretch to search is the post's neighbourhood, about 2,600 ft of road. Two posts hear the landing only 13–24% of the time, so a finer fix needs posts on both sides of the road.

**Landing far from the road is the soft spot.** Only 10–13% of landings 600–1,500 ft out are heard by a post. The fence still heard the drone come in, so the guard knows one drone is inside and unaccounted for, but not where.

## How many darts

| Road, 4 mi | Posts | Fence | Fence darts | Of them, tip darts (fibre) | Air-dropped | Per mile, all |
|---|---|---|---|---|---|---|
| Running along the front, 2.3 mi back | 21 | 6.2 mi | 35 | 5 (5.6 mi of fibre) | 35 | **14** |
| Running toward the front, 1.7–5.7 mi back | 21 | 10.2 mi | 58 | 7 (7.8 mi of fibre) | 58 | **20** |

On radio trunks the same fences needed 60 and 93 air-dropped darts: 25–35 of them were relays.

**The rules the planner uses:**

- **Posts every 1,100 ft at most.** Then any landing up to 300 ft off the road passes within 635 ft of a post. Posts stand 40 ft off the road.
- **The fence sits 5,316 ft out,** the same distance as the position net's front row, for the same reason: a drone at 60 mph crossing midway between two darts is heard 65 s out.
- **The fence only goes where a drone heading for the road would cross.** The planner flies tracks at every point of the road from every angle within 60° of the enemy, and puts the fence where they cross 5,316 ft from the road, plus 300 ft at each end. Behind the depot no track crosses, so the back is left open.
- **Fence darts sit about 960 ft apart,** one radio hop, as on the position net. **A fibre every 2 mi** brings alerts to the road, so no fence dart is more than about 6 hops from a tip, and every fence dart has two ways home.
- **Each fibre runs from its tip to the nearest post,** about a mile. A tip's spool holds about 1.2 mi, and the planner allows 10% for the fibre not lying straight, so it moves a tip to the next fence dart if its fibre would be too long.
- **Fibre must not lie across the road,** where trucks would cut it. Posts stand on one side, so where the fence is across the road from them, the fibre ends at a box on the near verge, joined to its post by a short cable buried under the road, laid by hand with the posts (est. a few dollars; not modelled).
- **The planner moves darts off trees.**

## What the model found

Every drone flies straight at 60 mph toward a point on the road, from 7.5 mi out, at every 0.1 mi of road and every 5° within 60° of the enemy: about 1,000 tracks a road. Recognising a drone takes 3 s and each hop 0.3 s (assumed).

| Road, 4 mi | Guard | Worst warning | 1 track in 10 below | Median | Tracks with a minute (55 s) |
|---|---|---|---|---|---|
| Along the front | Posts only | 0 s | 2 s | 4 s | 0% |
| Along the front | **Posts and fence** | **60 s** | 63 s | 72 s | **100%** |
| Toward the front | Posts only | 2 s | 4 s | 9 s | 9% |
| Toward the front | **Posts and fence** | **61 s** | 69 s | 102 s | **100%** |

- **Landings within 300 ft of the road: all heard by a post.** The loudest post is a median 340–350 ft from the drone, and 9 in 10 within 525–585 ft.
- **One dead dart or post costs little.** The worst single loss leaves 98% of tracks with a minute.
- **One cut fibre costs nothing in the model.** Its tip still relays by radio along the fence to the next tip, so 100% of tracks keep a minute.
- **Between repairs**, assuming each dart is lost 0.5% of days, each post 1% and each fibre is cut 1% (shelling, traffic, scavenging: guesses), and the daily roll call or the fibre's heartbeat finds a loss within a day: about one node is down at a time. Tracks with a minute average 100%, 83–98% on the worst day sampled (on the road toward the front, a tip and a dart six places along from it down on the same day); landings heard average 99%.
- **Laying the fence, GPS jammed, every dart confirmed,** 200 lays: about 46 darts and 18 sorties for the road along the front, 76 darts and 28 sorties for the road toward it, 6–9 of them tip darts. On radio trunks it was 77–119 darts and 23–35 sorties. The planned net is whole after 100% of lays.

**If the planning numbers are wrong, the fix is more darts,** as on the position net (per mile, posts and darts):

| Case | Along the front | Toward the front |
|---|---|---|
| **Plan** | **14** | **20** |
| Drones come within 45° of the enemy, not 60° | 13 | 18 |
| Drones come within 75° | 15 | 20 |
| Radio hop 800 ft, not 980 | 16 | 22 |
| Hearing 500 ft, not 656 | 18 | 24 |
| A fibre every 3 mi, not 2 | 14 | 20 |
| The last plan: radio relay trunks | 20 | 28 |

A fibre costs no extra darts, since its tip is a fence dart, so fewer fibres save nothing but tip darts. If 1 fibre in 5 breaks while it is laid, not 1 in 20, a lay uses about 2 more darts.

## Jamming, and a wire along the road

{: .warning }
> From the [jamming model]({{ site.baseurl }}{% link models/line-layout.md %}#jamming) ([`jam_model.py`](https://github.com/paulrenzi/tripwire/blob/main/tools/jamming/jam_model.py)): estimates, with jammer powers assumed and every jammer on all the time.

**On a road, the jammers that matter are our own.** Trucks carry jammers against radio FPVs, and "most mobile jammers" cover 868–915 MHz ([Armada International, Feb 2026](https://www.armadainternational.com/2026/02/the-curran-papers-no-5-jamming-uninhabited-aerial-vehicle-video-signals-electronic-warfare/)). A 100 W vehicle jammer (assumed) deafens the receiver in its own cab, and posts within about 910 ft on the main estimate, or 2.7 mi in the worst case. So a radio-only guard can't tell a jamming truck anything on the move, which is when it matters. Trench jammers on both sides are too far from these fences to matter on the main estimate; in the worst case they deafen the forward end of the road toward the front.

**Proposed: put the posts on a cable, and give each a lamp.**

- **Twisted pair along the verge,** laid on the same night as the posts. RS-485 runs about 0.7 mi a segment ([TI](https://www.ti.com/document-viewer/SN65HVD72/datasheet/typical-application-sllse118349)), and every post repeats it, so every post knows what any post has heard, with no radio. Posts keep their radios as a backup, so a cut costs nothing unless a jammer is on at the same place.
- **A hooded lamp on each post, facing the road.** Posts on a hot stretch light up. A driver sees them with the jammer on, and a truck needs no receiver at all. It is the Russian roadside traffic light, driven by the guard. The hood has to hide the lamp from drones overhead; not designed.
- **Why copper, not fibre:** both are unjammable, but every post on a fibre would need an optical converter at each end, and copper can also carry power. Fibre is light enough to pay out from a drone, which is why the trunks out to the fence are fibre: nobody walks a mile out to lay them. Along the verge a crew already stops at every post.

| Road, 4 mi | Jammers on | Tracks with a minute, radio guard | Cable and lamps, main estimate | Cable and lamps, worst case |
|---|---|---|---|---|
| Along the front | Trench jammers on both sides | 100% | 100% | 100% |
| Along the front | The truck's own | **0%**: its receiver hears nothing | **100%** | 21% |
| Toward the front | Trench jammers on both sides | 100% | 100% | 82% |
| Toward the front | The truck's own | **0%** | **100%** | 46% |

**In the worst case the truck's jammer also reaches the fence** a mile out and stops its darts relaying. Fibre takes the trunks out of that: 21–46% of tracks keep a minute, against 2–22% on radio trunks. What is left is the fence itself, whose darts relay along the row by radio, and the cable can't fix that. Then a truck has to switch its jammer off on a hot stretch, since it does nothing against fibre-optic FPVs anyway. T19, run at range from a vehicle jammer, decides whether the worst case is real.

**The cable adds about $800 a road, $200 a mile** (est.): about $650 of twisted pair, $2–5 of RS-485 chip and $3 of lamp a post. It saves most of the vehicle receivers.

## Laying it

- **Posts go in by hand,** from a vehicle at night: 21 stops on a 4 mi road, each post checked with a handheld receiver before the crew moves on. That puts a crew on the shoulder of the road it is guarding. Verges are often mined.
- **The fence goes in by drone,** with the [lay model's]({{ site.baseurl }}{% link models/line-layout.md %}#laying-the-net) loop: the drone drops 4 darts a sortie and confirms every dart by hearing its neighbour relay it. **Tips go first,** each as the first drop of its own sortie: the crew ties the fibre off at its post, the drone pays it out on the way to the fence, and the tip's heartbeat at the post confirms it. A tip whose fibre breaks is laid again with a new fibre. So every fence dart has a way home before the next one lands.
- **It is a day's work with more packs.** The road toward the front takes about 5.1 h of flying and charging with 12 packs and a 4-channel charger, 11.7 h with the position package's 6 packs and 2 channels; the road along the front 3.1 h or 6.5 h. With GPS jammed it is a daylight job, so the larger kit is the difference between one day and two on the longer fence.
- **The fence is re-laid when its cells run down;** posts carry 4 cells and should last about 4 times as long (T12).

## Cost

Small-batch cost to us, from [Projected costs]({{ site.baseurl }}{% link costs.md %}#guarding-a-road). A post is about $45 (est.): the dart's board, 4 cells, a 2 ft whip and a stake.

| | Along the front | Toward the front |
|---|---|---|
| **Package:** 25 posts, 50 or 80 darts, 9 or 11 tip darts and a fibre end at each fibre's post, 14 receivers (12 vehicles, 2 checkpoints), the outfitted drone with 12 packs and 4 charger channels | **~$5,690** | **~$6,780** |
| One re-lay of the fence: about 46 or 76 darts (6 or 9 of them tip darts), about 0.3–0.6 of a lost drone, pack wear | ~$2,000 | ~$3,270 |
| **A year at four-week cells:** 13 re-lays, posts, repairs between re-lays | **~$37,300** | **~$56,300** |
| A year at two-week cells | ~$66,400 | ~$101,900 |
| A year at twelve-week cells | ~$17,900 | ~$25,900 |
| **A mile a year at four-week cells** | **~$9,300** | **~$14,000** |

- **Battery life sets the bill,** as on the position net: the fence's re-lays are 70–76% of a year at four-week cells.
- **Fibre made it cheaper.** A tip dart costs about $94 against a dart's $29, but each fibre replaces about 5 relay darts, and fewer darts means fewer sorties and fewer lost drones. A re-lay costs about 19–24% less than on radio trunks.
- **Cut fibres are a new running cost:** at the guessed 1% of days each, about 18–26 new tips a year, each on its own sortie, about $2,000–2,800.
- **The drone is the hidden cost again.** At the guessed 2% lost per sortie, a re-lay loses about 0.3–0.6 drones, about $270–500.
- **Posts only:** about $1,400 for 25 posts and 14 receivers, and about $6,500 a year. No drone is needed. It finds landings by the road but gives 4–9 s of warning of a strike.
- **The cable and lamps** add about $800 a road ([above](#jamming-and-a-wire-along-the-road)). Repairs to cuts are not costed.

## Against what's already on roads

- **Nets and net tunnels** are going up fast: Ukraine plans another 2,500 mi of net-covered road in 2026 ([Liga.net](https://news.liga.net/en/politics/news/another-4000-km-of-roads-will-be-covered-with-anti-drone-tunnels-in-ukraine-by-the-end-of-the-year-photo)). But waiting drones "can also hide under the nets", and fibre-optic FPVs fly underneath them ([What troops have]({{ site.baseurl }}{% link research/frontline-kit.md %})). Posts along a netted road would hear those landings; the fence would warn of the ones that fly under.
- **Russia's roadside "traffic lights"** already time movement round distant drones ([Espreso](https://global.espreso.tv/russia-ukraine-war-russia-installs-traffic-lights-to-counter-ukrainian-fpv-drones)). That is this job, and someone already pays for it.
- **Radio detectors** like the Chuyka ride in the cab, but cannot hear fibre-optic drones at all.
- **Zvook already pitches acoustic sensors for roads.** Its maker describes NW0 networks "protecting… logistics routes" with sensors 400–600 m (about 1,300–2,000 ft) apart, reporting over Ethernet, fibre, twisted pair, LTE or LoRa ([Militarnyi](https://militarnyi.com/en/news/ukraine-develops-acoustic-detector-for-fpv-drones/), [dev.ua](https://dev.ua/en/news/ukrainska-kompaniia-zvook-stvoryla-akustychnyi-sensor-dlia-vyiavlennia-fpv-droniv-za-zvukom-1769187556)). That is the posts, wired, at about $834–950 a sensor against our $45. It is a direct rival on the road. What it lacks is the fence a mile out, which is what gives the minute ([competitors]({{ site.baseurl }}{% link research/competitors.md %})).

## What it misses

| Gap | What happens | What helps | Status |
|---|---|---|---|
| **Drones parked before the guard went in** | Never heard: they don't fly again until they strike | Search the road once after laying | Procedure |
| **Drones carried in on foot** and launched near the road | Cross no fence. In the model a post hears it lift off about 1 s before it strikes | Patrols; nothing in the guard | Not fixable by the guard |
| **Landings more than about 600 ft from the road** | Known to be inside, not where | A second row of posts, or posts on both sides | Not modelled |
| **The convoy's own jammer** | A vehicle jammer covering 900 MHz blinds the truck's receiver and posts within about 900 ft, on the move, when it matters | Posts on a cable with lamps facing the road: modelled, 100% on the main estimate | Proposed; T19 at range |
| **The truck's jammer reaching the fence** | In the worst case for jamming, darts a mile out can't relay while it passes | Fibre trunks (now the plan) keep 21–46% of tracks; a jammer off on a hot stretch keeps the rest | Unknown until T19 |
| **A cut fibre** | Shelling, vehicles or people cut a fibre lying a mile across the ground. Guessed at 1% of days each | The tip still relays by radio to the next tip, so no single cut costs a track in the model. The heartbeat shows the cut within 30 s; a new tip is laid on its own sortie | Modelled; T21 |
| **A cut cable** | Shelling or traffic cuts the cable along the verge | Posts fall back to radio; the roll call finds the break | Not costed |
| **Our own drones** | Our drone crews live in this strip and cross the fence both ways all day | A cheap beacon on our drones that darts recognise; flight corridors and times (T15) | Not designed |
| **Traffic noise** | A convoy passing may deafen a post just when a drone lands near it | The fence is far from traffic; landings usually come before the traffic | T20 |
| **Drones from behind,** past 60° | The back of the road is open | Fence at 75° costs about 1 more dart a mile | A choice |
| **Posts on the verge** | Mines, traffic, scavenging. Assumed lost 1% of days | Stakes set back from the edge; the roll call | Guess |
| **A shot-down drone looks like a landing** | A false "waiting" alert | Check it anyway; it is cheap to look | Accepted |

## What has to be tested

- **T20 (new): hear a landing beside a road.** Fly an FPV-size quad in, land it 50–600 ft from a post, and cut the motors, with and without trucks passing. Does the post tell "landed" from "flew out of range", and how far does a passing truck cut its hearing?
- **T21 on a road:** lay a tip's fibre from a post a mile out across the ground beside a road, and count how often vehicles, people and weather cut it (1% of days assumed).
- **T9 with whips:** the post-to-post hop on 2 ft whips, which this page assumes reaches about 2,500 ft.
- **T19 with a vehicle jammer,** as well as a trench jammer, and at range: how far from a jammer does a post or a dart still receive? That number decides whether the fence works beside a jamming convoy.
- **A lamp drivers can see and drones can't:** how well does a hood hide it from above?
- **T18 with drivers and medics:** would they hold or stop on a "hot" board, and how far from the road do waiting drones actually land?
- T11 and T12 decide the count and the bill, as for the position net.
