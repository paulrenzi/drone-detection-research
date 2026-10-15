---
title: Build or scrap?
parent: Research Notes
nav_order: 0.1
---

# Build or scrap?
{: .no_toc }

A review of whether the case for our model holds, after a fresh sweep of competitors' prices and capabilities, FPV acoustics, forward ground sensors, enemy counters and whether warning helps. Reviewed 2026-10-15.

{: .important }
> **Verdict: don't scrap, but narrow.**
> - **Keep the forward-laid tripwire.** It is the one part nobody sells, and the one part that physics favours. What it buys is a go/no-go minute for people about to move: about 1–4 of every 100 drone casualties averted, on our central guess ([estimate]({{ site.baseurl }}{% link research/lives-model.md %})).
> - **Drop the hand-placed node as a product.** A Ukrainian LoRa acoustic module is already listed at about $211, inside our $125–300 band.
> - **The case is not bulletproof, and more desk research won't make it so.** Three things could still kill it. A $0 interview round (T18) and two field tests under $300 each (T9, T19) decide them.

1. TOC
{:toc}

## Why the forward line holds

**Warning time is distance divided by speed.** No microphone changes that. Take an FPV at about 100 km/h (28 m/s; an assumption, and FPVs fly slower and faster), and take off 1–2 s to classify the sound:

| Sensor | Where it sits | Range it relies on | Warning (estimate) |
|---|---|---|---|
| A sentry's ear | At the position | ~150 m (Mavic-class, quiet field, measured) | ~4 s |
| DroneAlert module | At the position | 120 m (seller's claim) | ~3 s |
| Zvook NW0 | At the position | 450 m (maker's claim, best case) | ~14 s |
| **Our listener line** | **2–4 km forward** | **Only needs to hear the drone cross the line** | **~70–140 s** |

Every sensor at the position gives seconds, even on its maker's best figure. Only distance gives a minute. **A listener's range sets how many listeners a line needs, not how much warning it gives.** That makes the tripwire the part of the case least exposed to the range question.

## What it costs at equal range

Earlier comparisons gave competitors their claimed ranges. Here every row uses the **same range**, so the comparison is fair. A 3 km line, one sensor per detection range (as the [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}) plans it). Arithmetic on listed prices; the ranges are unmeasured for everyone.

| If every sensor hears an FPV at… | Sensors per 3 km | Our listeners ($17–50) | DroneAlert ($211) | Zvook NW0 ($834–950, plus power) |
|---|---|---|---|---|
| 250 m | 12 | $200–600 | ~$2,500 | ~$10–11k |
| 100 m | 30 | $510–1,500 | ~$6,300 | ~$25–29k |
| 50 m | 60 | $1,020–3,000 | ~$12,700 | ~$50–57k |

**At equal range we are about 4–12x cheaper than DroneAlert and about 17–56x cheaper than NW0.** Add the yearly re-lay cost for a consumable line ([estimate]({{ site.baseurl }}{% link models/tripwire.md %}#the-running-cost-lines-are-ammunition)). A line of 60 listeners re-laid often could cost more than a radio detector bought once.

**How far does a cheap microphone hear an FPV?** Still nobody knows. We found no measured FPV sound level and no controlled FPV range test anywhere. A first-principles estimate (sound falling off with distance, air absorption, rural background noise) puts a single cheap microphone at about **100 m in wind and 150–250 m in calm, quiet air**. That assumes an FPV is 85–95 dB(A) at 1 m, which is louder than a Phantom because its props spin about 3x faster at the tips. The same model gives 30–100 m for a Phantom, which brackets the measured 50–60 m, so the model is in the right range. **Plan on 20–30 listeners per 3 km line, not 12**, until T11 measures it.

## What changed in the market

- **A cheap LoRa acoustic module exists.** DroneAlert, sold by Flash Army (Ukraine), is listed at 9,500 UAH (~$211) per module, with a 2,500 UAH gateway. The seller claims:
  - a 120 m detection radius and a bearing;
  - up to 500 hours on a 3.7 V battery;
  - LoRa up to 10 km;
  - IP55.
  
  It's out of stock, names no maker, has no reviews and doesn't mention fibre-optic FPVs ([Flash Army](https://flasharmy.com.ua/dronealert-lora-merezha-akustychnyi-modul-vyiavlennia-droniv), news item Jun 2026). **It has our architecture.** Our listener is still 4–12x cheaper, but the architecture is no moat.
- **Other new entrants, all claims only:**
  - **SKANER 2.1** (Belarus): 100–300 m against FPVs, fibre-optic included; 1.2 kg; 12 h ([Militarnyi, May 2026](https://militarnyi.com/uk/news/bilorus-predstavyla-akustychnyj-radar-skaner-2-1-dlya-vyyavlennya-fpv-droniv-na-optovolokni/)).
  - **Arcani HARK** (UK): aimed at FPVs, with a Ukraine test planned for May 2026 and no result found ([Janes, Apr 2026](https://www.janes.com/osint-insights/defence-news/c4isr/arcani-plans-to-test-hark-acoustic-sensor-in-ukraine)).
  - **Neuron Soundware Sound Shield** (Czechia): under 1 W per sensor, at a reported €100–150 production cost, for borders ([dev.ua, Jun 2026](https://dev.ua/news/sound-shield-1781192277)).
  - **ZVOOK Tracking**: a bearing-capable array at about $2,670 ([Flash Army](https://flasharmy.com.ua/sensor-zvook-tracking)).
- **Nobody sells forward lines.** Komodo's star is still the only acoustic sensor sold as drone-droppable, and it's priced and pitched as a capable Shahed sensor.
- **No independent test of any acoustic FPV detector** was found: not NW0, RADD, Komodo, DroneAlert or SKANER. Poland's seven-system trial at Ustka (April 2026) published no results.
- **At the front, the kit is shifting** ([inventory]({{ site.baseurl }}{% link research/frontline-kit.md %})). Jamming is failing ("Jamming no longer works", a brigade EW commander). An AI turret that tracks fibre-optic drones is in more than 10 units. Interceptors are the most-ordered category on Brave1 Market. None of it gives a minute's warning of fibre-optic FPVs.
- **Money is moving into acoustic, for the rear.** NATO's procurement agency (NSPA) named a Bionic System Solutions-led consortium as one of five counter-drone framework contractors (July 2026). Lithuania is piloting Sky Fortress, and a Czech fund has invested in Zvook (Oct 2026). None of this is for FPVs at a position.

## What could still kill it

Ranked by how likely each is to end the idea, with the test that decides it.

### 1. Warning matters; whether this warning fills a gap is unproven (T18)

We found **no study, after-action report or soldier account comparing outcomes with and without warning**. What exists:

- **Seconds of warning are used every day.** Cheap beepers give "seconds to take cover" ([Telegraph, Jul 2025](https://www.yahoo.com/news/inside-ukraine-drone-infested-grey-090000135.html)). Crews use radio detectors to decide when to switch on jammers or run to shelter ([Foreign Policy, Aug 2024](https://foreignpolicy.com/2024/08/05/ukraine-russia-war-drone-detectors-jamming-tsukorok/)).
- **Demand for detectors is high**, but that is a signal of value, not a measurement of lives saved. The Tsukorok developer said demand far outran supply (same source). Ukraine's former defence minister said everyone should carry a Chuyka ([BlueBird, Aug 2026](https://www.blue-bird.tech/en/news-en/everyone-should-have-a-chuyka-from-schoolchildren-to-minibus-drivers-says-mykhailo-fedorov/)).
- **Against:** the Tsukorok designer calls his detector a last warning device that loses value where drones are everywhere (Foreign Policy). Troops already cope by staying put for a month or more and moving at night ([RUSI, Feb 2025](https://static.rusi.org/tactical-developments-third-year-russo-ukrainian-war-february-2205.pdf)).
- **Where the evidence points instead: routes.** About half of casualties are in the rear, during rotation and resupply (RUSI). Fibre-optic FPVs now hunt roads and wait beside them for hours ([Mezha, Nov 2025](https://oboronka.mezha.ua/en/droni-zhduni-yak-pracyuyut-novi-rosiyski-droni-306465/)).

  A line across the approach would warn a convoy of drones flying in. It **would not** warn of one already waiting with its motors off, which is silent until it launches (inference).

**Weapons need seconds; a minute buys go/no-go calls on movement.** Russia's roadside drone "traffic lights" already serve that purpose ([the comparison]({{ site.baseurl }}{% link research/problem-check.md %}#a-minute-against-the-alternatives)). In lives, our central guess is about 1–4 of every 100 drone casualties averted, range 0.3–14 ([estimate]({{ site.baseurl }}{% link research/lives-model.md %})).

**Scrap the tripwire if** T18 interviewees say a minute changes nothing for them, at the position or on the move. Ask specifically about drivers, medics and resupply runs.

### 2. The radio link home gets jammed or found (T9, new T19)

- **The bands are already contested.** Russia's Groza-07K jammer covers 100 MHz–1.1 GHz, which includes 433, 868 and 915 MHz ([Armada International, Sep 2026](https://www.armadainternational.com/2026/09/russia-tishina-software-defined-jammer-electronic-warfare/)). Jammers on both sides sit near the line to defeat 900 MHz drone control links.
- **A LoRa-hunting jammer is in development.** The same article, by an analyst from KI Insights, describes "Tishina", a Russian *prototype* designed to detect and suppress LoRa and ELRS signals. No field results are reported.
- **Emitters get struck.** Ukraine has found and hit Russian mesh relay stations by their emissions ([DroneXL, Feb 2026](https://dronexl.co/2026/02/28/ukraine-shahed-drone-relay-stations-belarus)). Those were high-power towers, not small sensors. We found no case of small, rarely-transmitting sensors being hunted, and no case showing they are safe.

Listeners that sit quiet are hard to find. **The receiver at the unit and any relay chain are the parts that are exposed.** The [listen-only edge receiver]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees) already keeps the unit's end silent.

**Scrap or rethink the back-haul if** T19 shows packets don't get through near a working ELRS jammer at any band or spreading factor.

### 3. The real range is very short (T11)

Below about 50 m, a 3 km line needs 60 or more listeners and each re-lay takes 15–20 drone sorties. The cost per line still beats every competitor at equal range, but the re-lay workload may not be worth it to a unit. **The idea stops making sense below roughly 40 m** (an inference from the table above). The estimate says 100 m or more is likely, which keeps this the least likely of the three to kill the idea.

## What not to claim any more

- **"Our hand-placed node is much cheaper than the market."** At $125–300 it isn't cheaper than DroneAlert's ~$211. Only the throwaway listener is.
- **"Nobody sells cheap LoRa acoustic sensors."** DroneAlert does, on paper.
- **"The line is silent."** The listeners are silent until they report. The reports, any relays and any receiver that transmits are not.

## What would make the case bulletproof

1. **T18:** 5–10 front-line interviews, including drivers and medics. $0.
2. **T11:** fly a real FPV past one cheap microphone on a mast and log the range in calm and in wind. Under $300.
3. **T19:** run the T9 radio test again next to a working ELRS jammer. Under $300.
4. **An independent test of NW0 or DroneAlert alongside ours.** Buying one DroneAlert kit (~$670 for three modules and a gateway) would give the first like-for-like range figure anyone has published.

Desk research has reached diminishing returns. Every remaining unknown is a measurement or an interview.

## Sources

Beyond those linked above:
- [Jekateryńczuk & Piotrowski, *Sensors* 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12656299/): consumer-drone levels and tones, and range against a calibrated tone in calm and wind.
- [Miguel-Ayala et al., Forum Acusticum 2025](https://dael.euracoustics.org/confs/fa2025/data/articles/000656.pdf): measured hover levels of the Mavic 4, Phantom 4 and Matrice 300.
- [Cabell et al., NASA, NOISE-CON 2016](https://ntrs.nasa.gov/api/citations/20160010139/downloads/20160010139.pdf): small multicopter noise.
- [Tejera-Berengue et al., Forum Acusticum 2025](https://dael.euracoustics.org/confs/fa2025/data/articles/000072.pdf): modelled FPV audibility.
- [Defence-Industry.eu: NSPA counter-drone framework (Jul 2026)](https://defence-industry.eu/nato-procurement-agency-selects-five-suppliers-for-counter-drone-framework-as-allies-seek-faster-access-to-c-uas-systems/)
- [Militarnyi: Lithuania's Sky Fortress pilot (Oct 2026)](https://militarnyi.com/en/news/lit-ukr-skyfortress-acoustic-uav-detection/)
- [Kyiv Post: DEPO Ventures invests in Zvook (Oct 2026)](https://kyivpost.com/post/86941)
- [Defence24: Ustka acoustic trial (Apr 2026)](https://defence24.pl/polityka-obronna/drony-bez-szans-mon-ujawnia-przelomowe-testy)
- [NPR: the kill zone (Oct 2026)](https://www.npr.org/2026/10/05/nx-s1-5925803/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)
