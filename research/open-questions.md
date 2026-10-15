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
| T3 | Same nodes at 2 m vs. 10 m vs. rooftop | Range gain from height (M4) | ~$0 extra | Not started |
| T4 | Windscreen comparison at different wind speeds | How much range wind costs; best cheap windscreen | < $100 | Not started |
| T5 | Leave nodes running a week in a farm, town and near a road | False alarms per node per day | ~$0 extra | Not started |
| T6 | Obtain Shahed-class engine recordings (partner or surrogate engine of similar size) | Classifier accuracy on the real target | partnership | Not started |
| T7 | LoRa mesh with 20+ nodes reporting simultaneously | Latency and loss during a mass-raid burst | ~$1,000 | Not started |
| T8 | Measure each node's radio emissions (duty cycle, power, burst length) with an SDR | How detectable is a node? Backs the passive claim in SBIR proposals | < $300 | Not started |
| T9 | [Tripwire]({{ site.baseurl }}{% link models/tripwire.md %}): ground-to-ground LoRa range at 2–3 km, open ground and trees, raised receiver at the unit. [Evidence and test plan](#t9-can-a-forward-line-report-back) | Can a forward line report back at all? The deciding question for the tripwire | < $300 | Literature reviewed; field test designed, not run |
| T10 | Tripwire: drop-test printed dart bodies onto soil, sand, mud and grass | Do nodes land upright with the mic clear? | < $200 | Not started |
| T11 | Tripwire: FPV detection range for one mic on a 0.5–1 m spring mast | Node spacing along a line | < $300 | Not started |
| T12 | Tripwire: wake-on-sound battery life with a small drone classifier on a microcontroller, including the battery and temperature reports, in cold | Is "weeks on a small battery" real, and how much shorter in winter? | < $200 | Not started |
| T13 | Tripwire: autonomous drop sortie, 4 nodes on GPS points from a printed quad | Placement accuracy and payload | < $500 | Not started |
| T14 | Tripwire: the T13 sortie with GPS unavailable, flying on optical flow, compass and barometer from a known start point ([Delivery drone]({{ site.baseurl }}{% link research/delivery-drone.md %}#flying-when-gps-is-jammed)) | Can a line be laid under jamming, and how far off are the drops? | < $300 | Not started |
| T15 | Record friendly drone types (observation quads, bombers, resupply) and test whether the classifier, which line trips first, and friendly flight times can sort friend from foe, with node clocks kept in step without GPS, by neighbours relaying or by a rare time beacon from a surveyed point ([design]({{ site.baseurl }}{% link models/tripwire.md %}#solving-the-field-limits-at-no-extra-cost)) | Will a line raise false alarms on its own side's drones? | < $200 | Not started |
| T16 | [M1]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) and [M3]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}) under GPS jamming: survey 3–5 nodes and one anchor, then compare three ways to keep positions and clocks without GPS: time-of-flight ranging to the anchor (SX1280 boards), a time beacon from the anchor, and calibrating against the delivery drone's logged track as it flies over. Suggested by a reader. [Evidence](#t16-positions-and-clocks-without-gps) | Can nodes that need precise positions and clocks keep them under jamming, and how much do they have to transmit to do it? | < $300 (est.) | Not started |
| T19 | [Tripwire]({{ site.baseurl }}{% link models/tripwire.md %}): repeat the best T9 link next to a working ELRS jammer (900 MHz band), at 433, 868/915 MHz and every spreading factor ([why]({{ site.baseurl }}{% link research/build-or-scrap.md %}#2-the-radio-link-home-gets-jammed-or-found-t9-new-t19)) | Does the back-haul survive the jamming already common at the front? | < $300 (est.) | Not started |
| T17 | [Tripwire]({{ site.baseurl }}{% link models/tripwire.md %}): build a [listen-only edge receiver]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees), a LoRa board raised 5–10 m at a tree-belt edge with a small Yagi, wired 300–1,000 m to the dugout over RS-485, with a second receiver on the same wire. Confirm with an SDR that it emits nothing (as in T8) | Can a unit hear its lines from inside a tree line without transmitting from its position? | < $300 (est.) | Not started |

## T9: can a forward line report back?

The [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}) only works if a node sitting 0.5–1 m above the ground, 2–4 km forward, can get a few bytes back to the unit, either directly to a raised receiver or by hopping node to node. This section collects what is already published and sets out the test that would settle the rest.

### What has been measured

| Source | Setup | Result |
|---|---|---|
| [Callebaut et al., 2019](https://arxiv.org/abs/1909.08300) | 868 MHz, 20 dBm, SF7–12, **both antennas about 1.5 m up**; coastal, forest and urban | **Over 4 km in open line of sight at SF12.** About 1 km maximum in dense forest and in town. Range was limited by signal strength, not noise, so the highest spreading factor went farthest |
| [Iova et al., 2017](https://openpub.fmach.it/bitstream/10449/42132/1/madcom17.pdf) | 868 MHz, 7–14 dBm, short-range settings (SF6–8, 500 kHz), small antennas; open mountain field versus forest | 450–550 m in the open, **50–90 m in forest**: "an order of magnitude" less. Range nearly halved on a 36 °C day. Their setting for longer range (SF8 instead of SF6) nearly doubled the open-ground figure to 900 m |
| [Ferreira et al., 2020](https://doi.org/10.1007/s12243-020-00789-w) | **915 MHz**, 14 dBm, 7 dBi antennas, SF7/9/12 at 500 kHz; forest in a Brazilian national park, measured along a raised walkway | **Up to 250 m in forest**, with random drop-outs. 2 km along a road from a vehicle |
| [Bianco and Marrocco, 2023](https://arxiv.org/abs/2303.12754) | 868 MHz, 14 dBm, SF7; a drone hovering at 3, 10 and 30 m at the forest edge, receiver carried into a poplar wood about 10 m tall | About 590–680 m at 91–94% delivery at all three heights, with severe fading. The wood is only about 720 m across, so this cannot show whether more height would reach farther |

{: .note }
> Anecdotes, not measurements: Meshtastic users report records of hundreds of kilometres between mountain tops, and well under a kilometre through suburban trees. Both point the same way: height and a clear line decide range, not transmit power. [Batear](https://github.com/batear-io/batear) publishes no range figures.

### Why antenna height matters so much

At 915 MHz a radio link needs a clear zone around the straight line between the antennas (the first Fresnel zone). At the middle of a 2 km link that zone is about **13 m** in radius. A node at 0.5–1 m sits deep inside the ground's shadow. Two consequences, worked out here as estimates from textbook models, not measured:

- **Open ground:** with a 1 m node and a 10 m mast, the extra loss at 3 km over free space is roughly **18 dB** (two-ray ground model). An SX1262 at 22 dBm and SF12 has a link budget of roughly 159 dB, so this leaves a wide margin on paper. Raising the receiver to an aerostat at 50–100 m would remove most of the extra loss.
- **Forest:** trees add loss on top, and no published measurement shows how much a raised receiver wins back from a node under the canopy at 2 km or more.

### Verdict: existing evidence does not settle it

- **Open ground, direct to a raised receiver: probably yes.** Callebaut measured over 4 km with both ends at only 1.5 m. A raised receiver should only help. But nobody has measured a 0.5–1 m node at 915 MHz to a mast at 2–4 km.
- **Forest, direct at 2–4 km: unsupported.** Every forest measurement with low antennas stops at 1 km or less, most at 50–250 m.
- **Forest, hopping node to node at 200–300 m: marginal.** Ferreira's 250 m used 7 dBi antennas; stock antennas are weaker. In dense forest, plan on hops of 100–200 m until measured, which means more nodes than the 12 per line the tripwire page assumes.

**Only a field test can settle the forest case**, and the forest case is the one that matters, because a line laid along a treeline or through woods is the realistic deployment.

### Predicting it before the field test

Simple arithmetic isn't enough. Multiplying per-hop delivery (80% per hop with three retries is about 99.8%, so about 98% over 12 hops) assumes failures are random. Under trees most aren't: a link blocked by a trunk or a fold in the ground stays blocked, and retrying doesn't help. What decides it is whether every gap in the line has at least one working link, counting links that skip a neighbour.

A simulation could estimate that (not yet built):

1. Fit a path-loss model to the measurements above, adding foliage loss from a standard vegetation model such as [Weissberger's](https://en.wikipedia.org/wiki/Weissberger%27s_model) and random shadowing.
2. Scatter thousands of lines, each listener 20–50 m off its planned point, and check every link against the SX1262's sensitivity at SF7–12.
3. Report the chance a line connects at each spacing, in forest and in windbreak country, to a receiver under a belt and to a [raised edge receiver]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees).

Ready-made simulators cover the routing side: [Meshtasticator](https://github.com/meshtastic/Meshtasticator) (Meshtastic's own), [ns-3 LoRaWAN](https://github.com/signetlabdei/lorawan) and [FLoRa](https://flora.aalto.fi/). The result would be a prediction, not proof, but it would let the field test check the model at a few points instead of surveying blind.

**Nearest published work.** Nothing we found measures delivery against hop count under canopy:

- [Leenders et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10255751): 30 LoRa nodes relaying up to three hops on a university campus, mostly indoors. 90% of nodes delivered at least 70% of packets, and delivery fell with distance from the gateway because end-to-end delivery is the product of each hop's. Not a forest.
- [Cappelli et al., 2023](https://doi.org/10.1109/SAS58821.2023.10254173): LoRaWAN links of 50, 100 and 200 m in an artificial wood. Standard path-loss models matched at 50 and 100 m but underestimated the vegetation loss at 200 m.

### The test (T9)

{: .note }
> **Cheapest version, about $80:** two boards, an adapter cable and a free mast (a window, roof or tree), plus a margin method that lets a small woodlot stand in for most of the forest run. Parts with links: [MVP path, layer 1]({{ site.baseurl }}{% link mvp.md %}#layer-1-the-radio-test-t9).

Uses the two Heltec WiFi LoRa 32 V3 boards from the [weekend test kit]({{ site.baseurl }}{% link research/open-source-builds.md %}#weekend-test-kit-start-training-the-detector).

**Extra kit (estimates):** a telescoping fibreglass mast or pole that reaches 8–10 m (~$60–120), two stakes to hold a board at 0.5 m and 1 m, and a pair of 3–5 dBi 915 MHz antennas to compare against the stock ones (~$20–30). Total with the boards stays under **$300**.

**Set-up**

- **Receiver** at the "unit" end, logging every packet with time, RSSI and SNR to a laptop or SD card. Test it at **2 m** (tripod) and **8–10 m** (mast).
- **Transmitter** is the "node". It sends a numbered packet every few seconds. A phone carried with it records a GPS track, so each packet can be matched to a distance afterwards.
- **Settings:** the US region setting in the firmware, full power (22 dBm), 125 kHz bandwidth, at **SF7, SF10 and SF12**. The forest evidence says the long-range answer will come from SF12; SF7 shows what a fast, short burst gets, which matters for emissions and battery.

**Runs**

| Run | Terrain | Node height | Receiver height | Distances |
|---|---|---|---|---|
| A | Open ground | 0.5 m and 1 m | 2 m and 8–10 m | 250 m, 500 m, 1, 2, 3, 4 km |
| B | Forest (node under canopy, receiver at the edge or in a clearing) | 1 m | 8–10 m | 250 m, 500 m, 1, 1.5, 2 km |
| C | Forest, node to node (both under canopy) | 1 m both | — | 100, 150, 200, 300 m |
| D | Repeat the best and worst of A–C with the 3–5 dBi antennas | as above | as above | as above |
| E | Windbreak country: node in the open or at a belt edge, with 1, 2 and 3 belts between it and the receiver | 1 m | Edge receiver at a belt: 2 m inside the belt, then 5–10 m in the canopy, with and without a small Yagi ([design]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees)) | 1, 2, 3 km |

At each point: stake the node, send **at least 100 packets per spreading factor**, and log packets sent and received, RSSI, SNR, node and receiver heights, terrain and canopy, temperature and wind. Fading in forest is severe, so also move the node a few metres and repeat at each forest point. Run on at least **two different days**, one of them warm.

**Pass for "rises to 4"**

- **Open ground:** 90% or more of packets delivered at **3 km** from a 1 m node to the 8–10 m receiver, at any spreading factor.
- **Forest, one of:** 80% or more delivered **direct at 2 km** to the raised receiver, **or** 80% or more **node to node at 200 m** (so a hop chain at the planned spacing holds).
- **Windbreak country:** 90% or more delivered at **2 km across two belts** to a raised edge receiver.
- Both on two separate days.

**What a fail means:** if forest hops fall under 80% at 150 m, the tripwire still works in open country, but in woods it needs either far denser lines or a different way home: a relay drone left on high ground, or an [aerostat]({{ site.baseurl }}{% link models/m05-aerostats.md %}) at the unit. Either way, record the numbers on the tripwire page.

{: .warning }
> Two boards measure one link at a time. How well a chain of many hops holds up is estimated from single-link delivery rates, not measured, until T7's 20-node test.

## T16: positions and clocks without GPS

A reader's suggestion: one central node knows where it is, and the others work out their own positions from it, instead of every node carrying GPS. It matters most for [M1]({{ site.baseurl }}{% link models/m01-ground-array-mesh.md %}) and [M3]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %}), which locate drones from several nodes. The [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}#solving-the-field-limits-at-no-extra-cost) doesn't need that precision.

The anchor itself should be a surveyed point, not a GPS receiver: at the unit it would be jammed too ([source]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)).

### What has been measured

| Source | Setup | Result |
|---|---|---|
| [Müller et al., 2021](https://digitalcollection.zhaw.ch/bitstream/11475/22769/3/2021_Mueller-etal_Outdoor-ranging-and-positioning-based-on-LoRa-modulation.pdf) (ZHAW with armasuisse) | SX1280, 2.4 GHz, 400 kHz bandwidth, SF8; fixed node at 1.5 m, walking node at 2 m; 8.2 km route over flat farmland, up to 1.4 km apart, about 25,000 measurements | Average error **46 m**, spread 84 m. Distances read long because of reflections. Worst average error **91 m** at 950 m, where a forest shadowed the link. A straight-line correction fitted to the same route cut the average error below 10 m. Positioning from four reference nodes about 400 m × 130 m apart: about 30 m error per fix, about 5 m when filtered along a walked track. Clear line of sight throughout; the authors expect worse with obstacles |
| Same paper, from Semtech's figures | SX1280 at its maximum 12.5 dBm | Best link budget about **134.5 dB**, "up to a few kilometers" in the countryside. Compare roughly 159 dB estimated for the SX1262 in [T9](#t9-can-a-forward-line-report-back) |

{: .note }
> Semtech documents the SX1280's ranging in application notes AN1200.29 and AN1200.50; we have not read figures from them. Nothing above was measured under canopy, so ranging accuracy and reach in forest are unknown.

### What this suggests (inference)

- **Positions:** a node that never moves needs its position once. Surveying it at install, or calibrating it from a known drone flyby, avoids any recurring emission. Ranging gives tens of metres, which is coarse for M1 and far too coarse for M3 (10 m is about 30 ms of sound travel).
- **Clocks** are the recurring need, and a time beacon from the anchor is the part most worth testing. Its accuracy over LoRa is not measured here.
- **Calibration flyby** (our idea, not the reader's): the delivery drone logs its own track. Each node's detection time, and for M1 its bearing, compared against that log could correct both position and clock, and M1's compass, with no extra radio traffic.

## Open questions

- Where is the Ukraine/Norway open-source sound library? (see [Datasets]({{ site.baseurl }}{% link research/datasets.md %}))
- What price would a NATO buyer pay per node, and what certification would they demand?
- Is the better business the **node**, the **fusion software**, or the **training data**?
