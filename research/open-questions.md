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
| T9 | [Tripwire]({{ site.baseurl }}{% link models/tripwire.md %}): ground-to-ground LoRa range at 2–3 km, open ground and trees, raised receiver at the unit | Can a forward line report back at all? The deciding question for the tripwire | < $300 | Not started |
| T10 | Tripwire: drop-test printed dart bodies onto soil, sand, mud and grass | Do nodes land upright with the mic clear? | < $200 | Not started |
| T11 | Tripwire: FPV detection range for one mic on a 0.5–1 m spring mast | Node spacing along a line | < $300 | Not started |
| T12 | Tripwire: wake-on-sound battery life with a small drone classifier on a microcontroller | Is "weeks on a small battery" real? | < $200 | Not started |
| T13 | Tripwire: autonomous drop sortie, 4 nodes on GPS points from a printed quad | Placement accuracy and payload | < $500 | Not started |

## Open questions

- Where is the Ukraine/Norway open-source sound library? (see [Datasets]({{ site.baseurl }}{% link research/datasets.md %}))
- What price would a NATO buyer pay per node, and what certification would they demand?
- Is the better business the **node**, the **fusion software**, or the **training data**?
