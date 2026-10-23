---
title: Open questions and field tests
parent: Research Notes
nav_order: 8
---

# Open questions and field tests
{: .no_toc }

The ratings on this site are judgements. These tests would turn them into measurements. Ordered roughly by value per dollar.

| # | Test | Answers | Est. cost | Status |
|---|---|---|---|---|
| T18 | Ask 5–10 people with recent front-line experience when they are exposed to FPVs and what they would do with 10 s, 1 min or 3 min of warning, at the position and on the move: drivers, medics, resupply ([questions]({{ site.baseurl }}{% link research/problem-check.md %}#the-next-step-ask-before-building-t18)) | Not a gate. Where a minute helps most, and how troops would place a line. Sets where the [lives estimate]({{ site.baseurl }}{% link research/lives-model.md %}) lands | $0 | Not started |
| T1 | Offline: run bearing + triangulation code on the Western Sydney 24-mic dataset with GPS logs | Does the software pipeline work before buying hardware? | $0 | Not started |
| T2 | Build 3–5 M1 nodes (ESP32-S3 + 4 mics + GPS); fly a consumer drone on a logged GPS track | Bearing error, position error vs. distance, detection range | < $500 | Not started |
| T3 | Same nodes at 6.6 ft vs. 33 ft vs. rooftop | Range gain from height (M4) | ~$0 extra | Not started |
| T4 | Windscreen comparison at different wind speeds | How much range wind costs; best cheap windscreen | < $100 | Not started |
| T5 | Leave nodes running a week in a farm, town and near a road | False alarms per node per day | ~$0 extra | Not started |
| T6 | Obtain Shahed-class engine recordings (partner or surrogate engine of similar size) | Classifier accuracy on the real target | partnership | Not started |
| T7 | LoRa mesh with 20+ nodes reporting simultaneously | Latency and loss during a mass-raid burst | ~$1,000 | Not started |
| T8 | Measure each node's radio emissions (duty cycle, power, burst length) with an SDR | How detectable is a node? Backs the passive claim in SBIR proposals | < $300 | Not started |
| T9 | [Tripwire]({{ site.baseurl }}{% link models/tripwire.md %}): ground-to-ground LoRa range at 1.2–1.9 mi, open ground and trees, raised receiver at the unit. [Evidence and test plan](#t9-can-a-forward-line-report-back) | Can a forward line report back at all? The deciding question for the tripwire | < $300 | Literature reviewed; field test designed, not run |
| T10 | Tripwire: drop-test printed dart bodies onto soil, sand, mud and grass | Do nodes land upright with the mic clear? Does a [v3 dart]({{ site.baseurl }}{% link build-hardware.md %}#1-v3-three-parts-per-dart), released flat, turn point-down within 16–49 ft? | < $200 | Not started |
| T11 | Tripwire: FPV detection range for one mic on a 1.6–3.3 ft spring mast | Node spacing along a line | < $300 | Not started |
| T12 | Tripwire: wake-on-sound battery life with a small drone classifier on a microcontroller, including the battery and temperature reports, in cold | Is "weeks on a small battery" real, and how much shorter in winter? | < $200 | Not started |
| T13 | Tripwire: autonomous drop sortie, 4 nodes on GPS points from a printed quad. Prediction to beat: an X500 with 4 v3 darts hovers about 11–12 min and reaches a line about 1.7 mi out ([estimate]({{ site.baseurl }}{% link build-hardware.md %}#payload-and-flight-time-estimates)) | Placement accuracy and payload | < $500 | Not started |
| T14 | Tripwire: the T13 sortie with GPS unavailable, flying on optical flow, compass and barometer from a known start point ([Delivery drone]({{ site.baseurl }}{% link research/delivery-drone.md %}#flying-when-gps-is-jammed)) | Can a line be laid under jamming, and how far off are the drops? | < $300 | Not started |
| T15 | Record friendly drone types (observation quads, bombers, resupply) and test whether the classifier, which line trips first, and friendly flight times can sort friend from foe, with node clocks kept in step without GPS, by neighbours relaying or by a rare time beacon from a surveyed point ([design]({{ site.baseurl }}{% link models/tripwire.md %}#solving-the-field-limits-at-no-extra-cost)) | Will a line raise false alarms on its own side's drones? | < $200 | Not started |
| T16 | [M1]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) and [M3]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}) under GPS jamming: survey 3–5 nodes and one anchor, then compare three ways to keep positions and clocks without GPS: time-of-flight ranging to the anchor (SX1280 boards), a time beacon from the anchor, and calibrating against the delivery drone's logged track as it flies over. Suggested by a reader. [Evidence](#t16-positions-and-clocks-without-gps) | Can nodes that need precise positions and clocks keep them under jamming, and how much do they have to transmit to do it? | < $300 (est.) | Not started |
| T19 | [Tripwire]({{ site.baseurl }}{% link models/tripwire.md %}): repeat the best T9 link next to a working ELRS jammer (900 MHz band), at 433, 868/915 MHz and every spreading factor, then with the jammer at 300 ft, 0.25 mi, 0.5 mi and 1 mi from the receiving dart, and with a vehicle jammer passing a post ([why]({{ site.baseurl }}{% link research/build-or-scrap.md %}#2-the-radio-link-home-gets-jammed-or-found-t9-new-t19), [model]({{ site.baseurl }}{% link models/line-layout.md %}#jamming)) | How far from a jammer does a link near the ground still work: a few hundred feet (our estimate) or about a mile (the worst case)? That decides whether a radio net can work near the front | < $300 (est.); a licensed range or Ukraine | Not started |
| T17 | [Tripwire]({{ site.baseurl }}{% link models/tripwire.md %}): build a [listen-only edge receiver]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees), a LoRa board raised 16–33 ft at a tree-belt edge with a small Yagi, wired 980–3,300 ft to the dugout over RS-485, with a second receiver on the same wire. Confirm with an SDR that it emits nothing (as in T8) | Can a unit hear its lines from inside a tree line without transmitting from its position? Keep the receiver at least about 1,000 ft from the unit's own jammers, or use a forward root on fibre ([why]({{ site.baseurl }}{% link models/line-layout.md %}#jamming)) | < $300 (est.) | Not started |
| T20 | [Guarding a road]({{ site.baseurl }}{% link models/route-guard.md %}): fly an FPV-size quad in, land it 50–600 ft from a post and cut the motors, with and without trucks passing | Can a post tell "landed" from "flew out of range", and how far does a passing truck cut its hearing? | < $200 (est.) | Not started |
| T21 | [How it works]({{ site.baseurl }}{% link models/line-layout.md %}#the-fibres-and-the-base-box): a tip dart's board driving a small laser into a full 1.2 mi spool of FPV fibre, read by a base box; then cut the fibre, and lay a spool from the drone over plough, grass and a windbreak | Does enough light get home? What do the laser and a heartbeat every 10 s cost the battery? How much does a tip weigh, and how often does fibre break while a drone lays it (1 in 20 assumed)? | < $300 (est.) | Not started |

## T9: can a forward line report back?

The [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}) only works if a node sitting 1.6–3.3 ft above the ground, 1.2–2.5 mi forward, can get a few bytes back to the unit, either directly to a raised receiver or by hopping node to node. This section collects what is already published and sets out the test that would settle the rest.

### What has been measured

| Source | Setup | Result |
|---|---|---|
| [Callebaut et al., 2019](https://arxiv.org/abs/1909.08300) | 868 MHz, 20 dBm, SF7–12, **both antennas about 4.9 ft up**; coastal, forest and urban | **Over 2.5 mi in open line of sight at SF12.** About 0.6 mi maximum in dense forest and in town. Range was limited by signal strength, not noise, so the highest spreading factor went farthest |
| [Iova et al., 2017](https://openpub.fmach.it/bitstream/10449/42132/1/madcom17.pdf) | 868 MHz, 7–14 dBm, short-range settings (SF6–8, 500 kHz), small antennas; open mountain field versus forest | 1,500–1,800 ft in the open, **160–300 ft in forest**: "an order of magnitude" less. Range nearly halved on a 97 °F day. Their setting for longer range (SF8 instead of SF6) nearly doubled the open-ground figure to 3,000 ft |
| [Ferreira et al., 2020](https://doi.org/10.1007/s12243-020-00789-w) | **915 MHz**, 14 dBm, 7 dBi antennas, SF7/9/12 at 500 kHz; forest in a Brazilian national park, measured along a raised walkway | **Up to 820 ft in forest**, with random drop-outs. 1.2 mi along a road from a vehicle |
| [Bianco and Marrocco, 2023](https://arxiv.org/abs/2303.12754) | 868 MHz, 14 dBm, SF7; a drone hovering at 10, 33 and 98 ft at the forest edge, receiver carried into a poplar wood about 33 ft tall | About 1,900–2,200 ft at 91–94% delivery at all three heights, with severe fading. The wood is only about 2,400 ft across, so this cannot show whether more height would reach farther |

{: .note }
> Anecdotes, not measurements: Meshtastic users report records of hundreds of miles between mountain tops, and well under a mile through suburban trees. Both point the same way: height and a clear line decide range, not transmit power. [Batear](https://github.com/batear-io/batear) publishes no range figures.

### Why antenna height matters so much

At 915 MHz a radio link needs a clear zone around the straight line between the antennas (the first Fresnel zone). At the middle of a 1.2 mi link that zone is about **43 ft** in radius. A node at 1.6–3.3 ft sits deep inside the ground's shadow. Two consequences, worked out here as estimates from textbook models, not measured:

- **Open ground:** with a 3.3 ft node and a 33 ft mast, the extra loss at 1.9 mi over free space is roughly **18 dB** (two-ray ground model). An SX1262 at 22 dBm and SF12 has a link budget of roughly 159 dB, so this leaves a wide margin on paper. Raising the receiver to an aerostat at 160–330 ft would remove most of the extra loss.
- **Forest:** trees add loss on top, and no published measurement shows how much a raised receiver wins back from a node under the canopy at 1.2 mi or more.

### Verdict: existing evidence does not settle it

- **Open ground, direct to a raised receiver: probably yes.** Callebaut measured over 2.5 mi with both ends at only 4.9 ft. A raised receiver should only help. But nobody has measured a 1.6–3.3 ft node at 915 MHz to a mast at 1.2–2.5 mi.
- **Forest, direct at 1.2–2.5 mi: unsupported.** Every forest measurement with low antennas stops at 0.6 mi or less, most at 160–820 ft.
- **Forest, hopping node to node at 660–980 ft: marginal.** Ferreira's 820 ft used 7 dBi antennas; stock antennas are weaker. In dense forest, plan on hops of 330–660 ft until measured, which means more nodes than the 12 per line the tripwire page assumes.

**Only a field test can settle the forest case**, and the forest case is the one that matters, because a line laid along a treeline or through woods is the realistic deployment.

### Predicting it before the field test

Simple arithmetic isn't enough. Multiplying per-hop delivery (80% per hop with three retries is about 99.8%, so about 98% over 12 hops) assumes failures are random. Under trees most aren't: a link blocked by a trunk or a fold in the ground stays blocked, and retrying doesn't help. What decides it is whether every gap in the line has at least one working link, counting links that skip a neighbour.

A simulation could estimate that (not yet built):

1. Fit a path-loss model to the measurements above, adding foliage loss from a standard vegetation model such as [Weissberger's](https://en.wikipedia.org/wiki/Weissberger%27s_model) and random shadowing.
2. Scatter thousands of lines, each listener 66–160 ft off its planned point, and check every link against the SX1262's sensitivity at SF7–12.
3. Report the chance a line connects at each spacing, in forest and in windbreak country, to a receiver under a belt and to a [raised edge receiver]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees).

Ready-made simulators cover the routing side: [Meshtasticator](https://github.com/meshtastic/Meshtasticator) (Meshtastic's own), [ns-3 LoRaWAN](https://github.com/signetlabdei/lorawan) and [FLoRa](https://flora.aalto.fi/). The result would be a prediction, not proof, but it would let the field test check the model at a few points instead of surveying blind.

**Nearest published work.** Nothing we found measures delivery against hop count under canopy:

- [Leenders et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10255751): 30 LoRa nodes relaying up to three hops on a university campus, mostly indoors. 90% of nodes delivered at least 70% of packets, and delivery fell with distance from the gateway because end-to-end delivery is the product of each hop's. Not a forest.
- [Cappelli et al., 2023](https://doi.org/10.1109/SAS58821.2023.10254173): LoRaWAN links of 160, 330 and 660 ft in an artificial wood. Standard path-loss models matched at 160 and 330 ft but underestimated the vegetation loss at 660 ft.

### The test (T9)

{: .note }
> **Cheapest version, about $80:** two boards, an adapter cable and a free mast (a window, roof or tree), plus a margin method that lets a small woodlot stand in for most of the forest run. Parts with links: [MVP path, layer 1]({{ site.baseurl }}{% link mvp.md %}#layer-1-the-radio-test-t9).

Uses the two Heltec WiFi LoRa 32 V3 boards from the [weekend test kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector).

**Extra kit (estimates):** a telescoping fibreglass mast or pole that reaches 26–33 ft (~$60–120), two stakes to hold a board at 20 in and 3.3 ft, and a pair of 3–5 dBi 915 MHz antennas to compare against the stock ones (~$20–30). Total with the boards stays under **$300**.

**Set-up**

- **Receiver** at the "unit" end, logging every packet with time, RSSI and SNR to a laptop or SD card. Test it at **6.6 ft** (tripod) and **26–33 ft** (mast).
- **Transmitter** is the "node". It sends a numbered packet every few seconds. A phone carried with it records a GPS track, so each packet can be matched to a distance afterwards.
- **Settings:** the US region setting in the firmware, full power (22 dBm), 125 kHz bandwidth, at **SF7, SF10 and SF12**. The forest evidence says the long-range answer will come from SF12; SF7 shows what a fast, short burst gets, which matters for emissions and battery.

**Runs**

| Run | Terrain | Node height | Receiver height | Distances |
|---|---|---|---|---|
| A | Open ground | 20 in and 3.3 ft | 6.6 ft and 26–33 ft | 820 ft, 1,600 ft, 0.6, 1.2, 1.9, 2.5 mi |
| B | Forest (node under canopy, receiver at the edge or in a clearing) | 3.3 ft | 26–33 ft | 820 ft, 1,600 ft, 0.6, 0.9, 1.2 mi |
| C | Forest, node to node (both under canopy) | 3.3 ft both | — | 330, 490, 660, 980 ft |
| D | Repeat the best and worst of A–C with the 3–5 dBi antennas | as above | as above | as above |
| E | Windbreak country: node in the open or at a belt edge, with 1, 2 and 3 belts between it and the receiver | 3.3 ft | Edge receiver at a belt: 6.6 ft inside the belt, then 16–33 ft in the canopy, with and without a small Yagi ([design]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees)) | 0.6, 1.2, 1.9 mi |

At each point: stake the node, send **at least 100 packets per spreading factor**, and log packets sent and received, RSSI, SNR, node and receiver heights, terrain and canopy, temperature and wind. Fading in forest is severe, so also move the node a few yards and repeat at each forest point. Run on at least **two different days**, one of them warm.

**Pass for "rises to 4"**

- **Open ground:** 90% or more of packets delivered at **1.9 mi** from a 3.3 ft node to the 26–33 ft receiver, at any spreading factor.
- **Forest, one of:** 80% or more delivered **direct at 1.2 mi** to the raised receiver, **or** 80% or more **node to node at 660 ft** (so a hop chain at the planned spacing holds).
- **Windbreak country:** 90% or more delivered at **1.2 mi across two belts** to a raised edge receiver.
- Both on two separate days.

**What a fail means:** if forest hops fall under 80% at 490 ft, the tripwire still works in open country, but in woods it needs either far denser lines or a different way home: a relay drone left on high ground, or an [aerostat]({{ site.baseurl }}{% link models/m05-aerostats.md %}) at the unit. Either way, record the numbers on the tripwire page.

{: .warning }
> Two boards measure one link at a time. How well a chain of many hops holds up is estimated from single-link delivery rates, not measured, until T7's 20-node test.

## T16: positions and clocks without GPS

A reader's suggestion: one central node knows where it is, and the others work out their own positions from it, instead of every node carrying GPS. It matters most for [M1]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) and [M3]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}), which locate drones from several nodes. The [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}#solving-the-field-limits-at-no-extra-cost) doesn't need that precision.

The anchor itself should be a surveyed point, not a GPS receiver: at the unit it would be jammed too ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)).

### What has been measured

| Source | Setup | Result |
|---|---|---|
| [Müller et al., 2021](https://digitalcollection.zhaw.ch/bitstream/11475/22769/3/2021_Mueller-etal_Outdoor-ranging-and-positioning-based-on-LoRa-modulation.pdf) (ZHAW with armasuisse) | SX1280, 2.4 GHz, 400 kHz bandwidth, SF8; fixed node at 4.9 ft, walking node at 6.6 ft; 5.1 mi route over flat farmland, up to 0.9 mi apart, about 25,000 measurements | Average error **150 ft**, spread 280 ft. Distances read long because of reflections. Worst average error **300 ft** at 3,100 ft, where a forest shadowed the link. A straight-line correction fitted to the same route cut the average error below 33 ft. Positioning from four reference nodes about 1,300 ft × 430 ft apart: about 98 ft error per fix, about 16 ft when filtered along a walked track. Clear line of sight throughout; the authors expect worse with obstacles |
| Same paper, from Semtech's figures | SX1280 at its maximum 12.5 dBm | Best link budget about **134.5 dB**, up to a couple of miles in the countryside. Compare roughly 159 dB estimated for the SX1262 in [T9](#t9-can-a-forward-line-report-back) |

{: .note }
> Semtech documents the SX1280's ranging in application notes AN1200.29 and AN1200.50; we have not read figures from them. Nothing above was measured under canopy, so ranging accuracy and reach in forest are unknown.

### What this suggests (inference)

- **Positions:** a node that never moves needs its position once. Surveying it at install, or calibrating it from a known drone flyby, avoids any recurring emission. Ranging gives tens of yards, which is coarse for M1 and far too coarse for M3 (33 ft is about 30 ms of sound travel).
- **Clocks** are the recurring need, and a time beacon from the anchor is the part most worth testing. Its accuracy over LoRa is not measured here.
- **Calibration flyby** (our idea, not the reader's): the delivery drone logs its own track. Each node's detection time, and for M1 its bearing, compared against that log could correct both position and clock, and M1's compass, with no extra radio traffic.

## Open questions

- Where is the Ukraine/Norway open-source sound library? (see [Datasets]({{ site.baseurl }}{% link research/datasets.md %}))
- What price would a NATO buyer pay per node, and what certification would they demand?
- Is the better business the **node**, the **fusion software**, or the **training data**?
