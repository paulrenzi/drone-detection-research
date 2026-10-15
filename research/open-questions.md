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
| T12 | Tripwire: wake-on-sound battery life with a small drone classifier on a microcontroller | Is "weeks on a small battery" real? | < $200 | Not started |
| T13 | Tripwire: autonomous drop sortie, 4 nodes on GPS points from a printed quad | Placement accuracy and payload | < $500 | Not started |

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

### The test (T9)

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

At each point: stake the node, send **at least 100 packets per spreading factor**, and log packets sent and received, RSSI, SNR, node and receiver heights, terrain and canopy, temperature and wind. Fading in forest is severe, so also move the node a few metres and repeat at each forest point. Run on at least **two different days**, one of them warm.

**Pass for "rises to 4"**

- **Open ground:** 90% or more of packets delivered at **3 km** from a 1 m node to the 8–10 m receiver, at any spreading factor.
- **Forest, one of:** 80% or more delivered **direct at 2 km** to the raised receiver, **or** 80% or more **node to node at 200 m** (so a hop chain at the planned spacing holds).
- Both on two separate days.

**What a fail means:** if forest hops fall under 80% at 150 m, the tripwire still works in open country, but in woods it needs either far denser lines or a different way home: a relay drone left on high ground, or an [aerostat]({{ site.baseurl }}{% link models/m05-aerostats.md %}) at the unit. Either way, record the numbers on the tripwire page.

{: .warning }
> Two boards measure one link at a time. How well a chain of many hops holds up is estimated from single-link delivery rates, not measured, until T7's 20-node test.

## Open questions

- Where is the Ukraine/Norway open-source sound library? (see [Datasets]({{ site.baseurl }}{% link research/datasets.md %}))
- What price would a NATO buyer pay per node, and what certification would they demand?
- Is the better business the **node**, the **fusion software**, or the **training data**?
