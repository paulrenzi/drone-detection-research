---
title: The drones it has to hear
parent: Research Notes
nav_order: 0.27
nav_tripwire: 3.5
---

# The drones it has to hear
{: .no_toc }

How fast and how high the drones that attack Ukrainian troops fly, and whether a microphone on the ground can hear them in time. Speeds and heights below are makers' figures or reported field figures. None is an independent measurement.

1. TOC
{:toc}

## Speed and height, by drone

| Drone | What it does | Speed | Height |
|---|---|---|---|
| **FPV with a warhead** (radio-controlled) | The main infantry killer. A pilot in goggles flies it into the target | Usually **37–50 mph, at most 75 mph** when carrying a bomb. Racing builds reach 160 mph or more, but not when loaded ([Kyiv Post](https://www.kyivpost.com/post/39057)). Top speed about 87 mph ([ERR](https://news.err.ee/1609861089/err-in-ukraine-up-close-with-ukraine-s-counter-drone-air-defense-teams)) | No sourced figure. It climbs to keep its radio link |
| **Fibre-optic FPV** (e.g. Russia's KVN) | Steered by cable: no radio, so jammers and radio detectors miss it | **Up to about 43 mph** | **65–165 ft**, following the terrain ([Wikipedia](https://en.wikipedia.org/wiki/Ushkuynik_KVN)) |
| **Fibre-optic FPV in ambush** | Lands by a road, listens through its own microphone, takes off when it hears a target | **Parked and silent for up to 12 hours** ([TASS](https://tass.com/defense/2186125), [UNITED24](https://united24media.com/war-in-ukraine/can-fiber-optic-drones-be-stopped-how-ukraine-faces-the-unjammable-threat-12502)) | On the ground |
| **Lancet** | Fixed-wing loitering munition, mostly against vehicles | Cruises at **50 mph**, dives at about **185 mph** ([GlobalSecurity](https://www.globalsecurity.org/military/world/russia/lancet-specs.htm)) | No sourced figure |
| **Molniya-2** | Cheap fixed-wing strike drone, 20–30 mi reach | No published figure | No published figure |
| **Heavy night bomber** ("Baba Yaga" class) | Drops 30–45 lb at night | Slow, and very loud | Up to 1,300 ft ([Espreso](https://global.espreso.tv/russia-ukraine-war-baba-yaga-hexacopter-drone-has-become-invading-russian-armys-nightmare)) |
| **Geran-2 / Shahed** | Long-range strikes on the rear, not the trench line | Up to **115 mph** | **200–13,000 ft** ([GlobalSecurity](https://www.globalsecurity.org/intell/world/russia/geran-2.htm)) |

## What it means for a microphone

**Speed doesn't stop a microphone hearing a drone; it only shortens the warning.** Warning is distance ÷ speed. This site's warning figures use FPV top speed, 67–89 mph, so they are the worst case. At the 37–50 mph an FPV usually flies with a warhead, every figure is about 1.5–2 times longer:

| Where the listeners sit | At top speed, 67–89 mph | At usual combat speed, 37–50 mph |
|---|---|---|
| Ring placed by hand, ~980 ft out | ~8–10 s | ~13–18 s |
| Row laid by drone, about 1 mi out (the modelled net) | ~45–60 s | ~1.3–1.8 min |
| A deeper row, 2.5 mi out | ~1.5–2 min | ~3–4 min |

These are our arithmetic, not measurements.

**Height barely matters against FPVs.** A fibre-optic FPV at 165 ft that is 490 ft away along the ground is about 520 ft from the microphone. Height only costs range when it approaches the detection range itself. Drones at thousands of feet (Geran, recon planes) are outside the tripwire's job. Their engines are loud enough for Ukraine's Sky Fortress network, which already hears them over the rear.

**Range in wind is the open question.** Zvook claims 490–1,480 ft with 20 in dish reflectors ([Militarnyi](https://militarnyi.com/en/news/ukraine-develops-acoustic-detector-for-fpv-drones/)). ARes claims 660–980 ft for FPVs with a microphone array ([Militarnyi](https://militarnyi.com/en/news/ukraine-developed-the-ares-acoustic-system-for-targeting-drones-and-missiles/)). Both are makers' claims. In one published outdoor test, a good microphone 5 ft up heard a test tone at about 340–455 ft in calm air. In an 11 mph mean wind that fell to 95–315 ft, and a windscreen added 31–131% ([outdoor study, 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12656299/)). Hence the windscreen, and [T11]({{ site.baseurl }}{% link mvp.md %}#layer-2-hear-a-drone-from-near-the-ground-t11).

## Where a microphone can't help

- **Drones already parked in ambush.** A landed fibre-optic FPV is silent until it lifts off, seconds from its target. A listener line warns only of drones flying in, not of one already waiting by the road. Posts along the road can hear one land, which is when it is exposed ([Guarding a road]({{ site.baseurl }}{% link models/route-guard.md %})).
- **Friendly drones.** Ukrainian FPVs sound like Russian ones. The tripwire's answer is to alarm only on drones crossing the lines inbound, outside the unit's own flight times ([the fix]({{ site.baseurl }}{% link models/tripwire.md %}#solving-the-field-limits-at-no-extra-cost)). That is proposed, not tested (T15).
- **Wind and battle noise.** Strong wind can more than halve range, and artillery and engines mask the drone.

## The fit

The best target for a ground microphone is the one nothing else cheap catches. That is a fibre-optic FPV flying in at 65–165 ft and up to about 43 mph: low, slow, emitting no radio. Speed and height don't rule audio out. What decides it is range in wind, ambush drones and friend-or-foe.

Not found: a sourced flying height for radio-controlled FPVs, or for drones dropping grenades, and any Molniya-2 performance figures.
