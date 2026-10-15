---
title: Competitor analysis and positioning
parent: Research Notes
nav_order: 0
---

# Competitor analysis and positioning
{: .no_toc }

**Use case:** warning **front-line positions** of FPVs, especially fibre-optic ones that radio detectors can't hear. Lancet-type loitering munitions and small grenade-dropping quads come in the same final kilometres. Shahed-class drones and cruise missiles over the rear are a different market, and it's already served (see below).

## Two markets, only one of them ours

"Acoustic drone detection in Ukraine" covers two different jobs. Reporting, including the US Army's own review, blurs them together. That's why it was hard to say who we compete with.

| | Rear-area air defence | Protecting front-line positions |
|---|---|---|
| **Threat** | Shaheds and cruise missiles: loud engines, slow, flying across the country | FPVs, including fibre-optic: quiet, fast, final 1–2 km |
| **Acoustic players** | Sky Fortress, Zvook's parabolic stations, FENEK | Zvook NW0 only, announced and unproven |
| **Evidence it works** | Yes: reported by US commanders and in Ukrainian press, though never independently tested | **None found** |
| **Who buys** | The state, at national scale | Units, volunteers, Brave1 |
| **Us** | Not our market | **The gap** |

**The US Army review doesn't close the gap.** The Center for Army Lessons Learned published "Listening to the Sky" in March 2026. It says Ukrainian acoustic networks detect FPVs. But it's a 12-page desk review, and every source it cites is a news article or company website ([CALL, Mar 2026](https://api.army.mil/e2/c/downloads/2026/04/30/af450e75/no-26-1115-listening-to-the-sky-acoustic-drone-detection-in-ukraine-mar-26.pdf)):
- Its Sky Fortress sources are about Shaheds and never mention FPVs ([Defense One](https://www.defenseone.com/defense-systems/2024/07/ukraines-cheap-sensors-are-helping-troops-fight-waves-russian-drones/398204/), [TWZ](https://www.twz.com/air/ukraines-acoustic-drone-detection-network-eyed-by-u-s-as-low-cost-air-defense-option)).
- Its Zvook sources are about cruise missiles.
- Its range figure for FPVs ("hundreds to a few thousand meters") cites a vendor web page that now redirects to another company.

**So for us, the review settles that cheap acoustic sensors work against Shaheds. It doesn't show they work against FPVs at the front.**

**Who we actually compete with at a position:**
1. **A soldier listening.** This is the real baseline, and nobody has measured it. If a sentry hears a fibre-optic FPV as early as a sensor would, an alarm adds only reliability: it keeps listening through sleep, shelling and ear protection. T18 asks this ([question 2]({{ site.baseurl }}{% link research/problem-check.md %}#the-next-step-ask-before-building-t18)).
2. **The radio detector already in the dugout** (Chuyka-type). It isn't a rival but a partner: it catches radio-controlled FPVs, and we catch the fibre-optic ones it can't. We sell as **the second box next to it**.
3. **Zvook NW0**, the only direct competitor. So far it's an announcement, not a fielded product.

Anduril, radar and the national networks are not who we compete with at a position. They aren't there. Later on, they're systems to feed data into.

{: .warning }
> Prices for defence products are rarely published. Figures below come from public contract values, press reports and civilian list prices, and are marked as estimates. Correct them as better data turns up.

1. TOC
{:toc}

## The landscape at a glance

| Tier | Example | Sensing | Small-drone range (claimed) | Price (est.) | Passive? |
|---|---|---|---|---|---|
| **Integrated prime systems** | Anduril WISP + Pulsar + Lattice | Infrared 360° camera + passive RF + fusion software | 3–10 mi (WISP) | Six to seven figures per site | Yes |
| | DroneShield DroneSentry | RF direction-finding, radar, cameras, jammers | km-class | $280k Air Force base contract | Mostly |
| | Hensoldt Xpeller / Dedrone (Axon) | Multi-sensor incl. Squarehead acoustic | km-class | Six figures+ per site | Mixed |
| **Small radars** | Echodyne EchoGuard | Electronically scanned radar | ~1.5 km (small), 3–5 km (medium) | $40k–160k per radar | **No — emits** |
| **Acoustic specialists** | Squarehead Discovair G2 (Norway) | Large mic array | "Several hundred metres" | High (sold inside prime systems) | Yes |
| | Microflown AVISA Skysentry (Netherlands) | Acoustic vector sensors | 400 m for small, quiet drones | High | Yes |
| | Sky Fortress (Ukraine) | Phones + mics on poles, national network, **rear-area market** | km-class vs. Shaheds | $400–1,000 per sensor | Yes |
| | Zvook (Ukraine) | Tower-mounted and vehicle acoustic, **rear-area market** | Not published | Not published | Yes |
| | FENEK (Ukraine) | Acoustic network for regions and infrastructure, **rear-area market** | Not published | Not published | Yes |
| | Zvook NW0 (Ukraine, announced Jan 2026) | Acoustic FPV sensor for positions and routes, incl. fibre-optic; 15–20 W, wired or LoRa. **Maker's claims only** | 150–450 m (claimed) | Not published | Yes |
| **Soldier-worn RF detectors** | MyDefence Wingman (Denmark) | RF control/video link detection | up to 6 km | Not published; US Army bought 400 | Yes |
| | BlueBird Chuyka 3.0 (Ukraine) | Analog FPV video detection | up to 4 km | ~$750–850 | Yes |
| **Crowd-sourced** | Drone Rada (Lithuania) | Volunteers' phones | Short | ~$0 to operator | Yes |

## Competitor profiles

### Anduril — WISP, Pulsar, Lattice
- **WISP:** passive 360° infrared camera system with AI detection; claims automated drone detection at ~3–10 miles and filters out birds. Hard to detect because it transmits nothing.
- **Pulsar:** RF sensing (and electronic warfare); can locate drone operators.
- **Lattice:** the fusion and command software. The **US Army awarded Anduril an enterprise contract worth up to $20B over 10 years**, and JIATF-401 picked Lattice as its counter-UAS command-and-control platform.
- **Strengths:** long range, bird/drone discrimination, a dominant software position.
- **Gaps:** cameras need **line of sight** — low FPVs behind trees, buildings and ridges are hidden. RF sensing is blind to **fibre-optic and radio-silent drones**. Tower-mounted, expensive, not something every platoon gets.
- **Implication:** Anduril is the system we should **plug into**, not fight. Lattice is becoming the US Army's counter-drone backbone.

### DroneShield (Australia)
- RF direction-finding (RfOne), handheld/wearable detectors (RfPatrol), DroneSentry multi-sensor systems, jammers. Public contract values: $280k for an Air Force base, up to $700k for an Australian Army RfPatrol buy, $33M from a US agency.
- Resells **Squarehead's acoustic array**, so acoustic is already a recognised layer.
- **Gaps:** core strength is RF, so the same blindness to fibre-optic and autonomous drones.

### Echodyne (US) — small radar
- EchoGuard radars at **$40k–160k**, detecting small drones at ~1.5 km (short-range model) to 3–5 km (medium).
- **Strengths:** accurate range and speed, works day/night, any drone type.
- **Gaps:** **it transmits**, so the enemy can detect and target it. It needs line of sight, and it costs 25–100× a full acoustic kit.

### Squarehead Discovair (Norway) and Microflown AVISA (Netherlands) — acoustic specialists
- The closest technology to ours, high-end versions of it. Discovair: large array, "several hundred metres", no line of sight needed. AVISA: acoustic vector sensors, **400 m against small, low-noise drones**, aimed at urban use.
- **Gaps:** expensive, single large sensors sold through prime contractors — not cheap, numerous or easy to throw out.
- **Implication:** they show the **range ceiling** for acoustics against small drones is a few hundred metres even with premium hardware. We should match that with **more, cheaper nodes**, not a better single sensor.

### Sky Fortress, Zvook and FENEK (Ukraine) — the rear-area market
- They show low-cost acoustic networks work in war, **against Shaheds and cruise missiles**.
- **Sky Fortress:** about 9,500 sensors at $400–500 each, per a US general in 2024 ([Defense One](https://www.defenseone.com/defense-systems/2024/07/ukraines-cheap-sensors-are-helping-troops-fight-waves-russian-drones/398204/)). Later reports say ~14,000 sensors at $400–1,000.
  - Alerts go to mobile fire teams with guns, who see flight routes on an iPad.
  - "All but four of 84" drones in one raid were downed, by that general's account. We found no independent check.
- **Zvook:** tower-mounted stations, now trialling a vehicle version with NATO.
- **FENEK:** pitched for regional networks and infrastructure. Its site gives no range, price or customers ([FENEK](https://fenek.com.ua/en/)).
- **Gaps for our use case:** built for **area** coverage of loud engine drones, not for units facing FPVs. No source shows them detecting FPVs at the front.
- **Implication:** a different market, not our competitors. Possible **partners** for recordings, and proof that buyers trust acoustic sensors.

### Zvook NW0 — the one direct competitor (claims only)
- Announced January 2026: an acoustic FPV sensor, fibre-optic included, for front-line positions, frontline towns and logistics routes ([Militarnyi](https://militarnyi.com/en/news/ukraine-develops-acoustic-detector-for-fpv-drones/)).
- **Everything known is the maker's claim**, repeated by news sites:
  - 150–450 m range, 360° coverage;
  - 15–20 W of power;
  - linked by fibre, twisted pair, LTE or LoRa;
  - spaced 400–600 m apart.
- **Not found:** a price, an independent test, or any unit reported using it.
  - The Ukrainian coverage calls the range "declared" and credits the specs to Zvook's own Facebook post ([Militarnyi, Ukrainian](https://militarnyi.com/uk/news/v-ukrayini-stvoryly-akustychnyj-detektor-fpv-droniv/)).
  - The roughly $500 figure in some reports is for Zvook's older stations, not the NW0.
- **Plausibility (inference):** 450 m is at the top of what premium arrays claim against small drones ("several hundred metres", Discovair), and that would be in good conditions.
- **Its real lead:** a team with existing customers. Unlike us, it has a product.
- **Where we'd differ:**
  - battery power for weeks, not 15–20 W from a wire;
  - a throwaway price;
  - placement forward of the unit (the [tripwire]({{ site.baseurl }}{% link models/tripwire.md %})).

### Soldier-worn RF detectors — MyDefence Wingman, Chuyka
- Cheap, popular and proven: Chuyka 3.0 ~$750–850, detects analog FPV video at up to 4 km; Wingman up to 6 km, US Army bought 400.
- **Gaps:** detect radio, not drones. **Fibre-optic FPVs, digital/encrypted links and pre-programmed drones are invisible to them.** Usually no direction or position, so nothing to put on a map.
- **Implication:** the price anchor a soldier already understands (~$1k per detector). Our pitch is what they miss. They're a partner in the dugout, not a rival: we're the second box beside them.

### A soldier listening — the baseline nobody has measured
- Troops already hide when they hear a drone ([NPR, Oct 2026](https://www.tpr.org/news/2026-10-05/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)). The human ear is the free acoustic sensor every position already has.
- **Not found:** how early a sentry hears a fibre-optic FPV compared with a microphone.
- **Implication:** a sensor at the position has to beat that ear on warning time, or on staying alert through sleep, shelling and ear protection. Placing listeners forward (the tripwire) is the only way to beat it clearly on time, because a microphone's range doesn't grow with better hardware (inference from the premium arrays above).

## Who covers which threat

| Threat | Prime (WISP/Pulsar) | Radar (Echodyne) | RF wearables | Premium acoustic | **Our acoustic kit** |
|---|:-:|:-:|:-:|:-:|:-:|
| FPV, radio-controlled, line of sight | ✅ | ✅ | ✅ | ✅ | ✅ (short range) |
| **Fibre-optic FPV** | ⚠️ camera only | ✅ if line of sight | ❌ | ✅ | ✅ |
| **Pre-programmed / radio-silent drone** | ⚠️ camera only | ✅ | ❌ | ✅ | ✅ |
| **Low drone behind trees, buildings, ridges** | ❌ | ❌ | ⚠️ if it transmits | ✅ | ✅ |
| Shahed-class at long range (rear-area market, already served) | ✅ | ✅ | ❌ | ✅ | not our aim |
| Drones at altitude, long range | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| Undetectable by the enemy (passive) | ✅ | ❌ | ✅ | ✅ | ✅ (low-power bursts) |
| Affordable for every small unit | ❌ | ❌ | ✅ | ❌ | ✅ |

The gap no cheap product fills: **passive, non-line-of-sight detection of drones that don't transmit, at a price every unit can carry.** Only premium acoustic sensors cover it today, and they're priced for prime contractors.

## Cost comparison for one protected position

| Option | What you get | Est. cost |
|---|---|---|
| Anduril WISP + Pulsar tower | Long-range passive camera + RF + fusion | Six to seven figures |
| Echodyne radar + camera | ~1.5–5 km radar coverage, emitting | $50k–200k |
| Squarehead / AVISA acoustic sensor | One premium array, few hundred metres | High five figures+ (est.) |
| 4 × RF wearables (Chuyka/Wingman class) | Radio alarms, no fibre-optic, no map | ~$3k–10k |
| **Our kit: 8–12 acoustic nodes + local fusion on a laptop/phone** | Bearings → tracks in ATAK, fibre-optic and non-line-of-sight coverage around a ~500 m perimeter | **~$1,500–2,500** |
| **Our drone-laid tripwire** | Two forward lines, about a minute of warning; listeners are consumables | **~$1,500–2,500 kit, then ≈ $5–16k a year in re-lays** ([est.]({{ site.baseurl }}{% link models/tripwire.md %}#the-running-cost-lines-are-ammunition)) |
| Zvook NW0 | Claimed 150–450 m around a position, 15–20 W wired power | Not published |

## Conclusion — how to position

**On the market:** we sell to front-line positions facing FPVs, not into rear-area air defence. There, the bar to clear is a soldier's own ears, and the product to sit beside is the radio detector the unit already has. Shaheds, national networks and comparisons with Anduril or radar belong to the other market. Leave them out of the pitch.

**On cost:** sit at the **price of a soldier's RF detector** ($1–3k per kit), not the price of a sensor system. That's 20–100× below radar and prime systems and close to what units already buy with their own budgets or donations. The comparison to lead with: *"a whole perimeter for the price of two Chuykas."*

**On capability:** don't compete on range or long-distance accuracy — WISP and radar win there. Own the gaps they leave:

1. **Hears what radio detectors can't:** fibre-optic and autonomous drones, the fastest-growing FPV threat.
2. **Hears what cameras and radar can't see:** low drones masked by terrain, trees and buildings.
3. **Passive and low-signature:** no radar emission for the enemy to target.
4. **Many and cheap:** losing a node costs $100; losing a radar costs $100k.

**On integration:** be a **sensor, not a platform**. Output Cursor-on-Target to ATAK, SAPIENT for NATO, and target a Lattice integration — Lattice is becoming the US Army's counter-drone backbone, so being a cheap sensor that feeds it is worth more than a competing dashboard. Acoustic bearings that point WISP or a camera at a drone it couldn't otherwise find makes the expensive systems better.

**Front-line evidence backs this.** Drones cause about 80% of casualties, fibre-optic FPVs beat the radio detectors units carry, and WISP-class camera systems aren't at the front. See [Is the problem worth solving?]({{ site.baseurl }}{% link research/problem-check.md %})

**One-line positioning:**
> *An acoustic alarm for front-line positions that hears the FPVs radio detectors can't, especially fibre-optic ones: the second box next to the radio detector.*

**Cost honesty:** "a whole perimeter for the price of two Chuykas" holds for the hand-placed kit. The tripwire is a consumable with a yearly re-lay bill, so quote both numbers.

## Risks to this positioning

- **Sky Fortress or Zvook** ship a portable unit kit first — they already have data, combat credibility and NATO customers. Partner, or move faster on the field-kit form factor. **Update (2026-10-15):** Zvook announced the [NW0](https://militarnyi.com/en/news/ukraine-develops-acoustic-detector-for-fpv-drones/), an acoustic FPV sensor for front-line positions and routes, in January 2026. No price, independent test or deployment reported yet; every figure is the maker's claim ([profile](#zvook-nw0--the-one-direct-competitor-claims-only)).
- **A listening sentry is good enough.** If troops hear fibre-optic FPVs about as early as a microphone at the position would, a sensor there adds little beyond reliability. Then only forward placement pays. T18 decides it.
- **A prime adds cheap acoustics.** DroneShield already resells Squarehead; Anduril could add an acoustic sensor to Lattice. Our defence is price, speed, and being Lattice-compatible from day one.
- **Short range against FPVs** (~100–300 m, so ~5–10 s warning) may not satisfy buyers alone. The answer is placing nodes outward (rings 300–800 m out) and cueing other sensors — sell it as a layer, not a complete system.
- **No proprietary moat in the hardware.** The lasting advantage is **training data** (real combat recordings, local negatives) and fielded integrations.

## Sources

- [Military & Aerospace Electronics — Anduril WISP](https://militaryaerospace.com/computers/article/14303950/artificial-intelligence-ai-sensor-fusion-counter-uav)
- [DroneXL — WISP with Washington National Guard](https://dronexl.co/2026/08/06/anduril-wisp-washington-national-guard-drones-birds/)
- [Army.mil — Washington Guard counter-drone system](https://www.army.mil/article/294224/washington_national_guard_advances_counter_drone_capabilities_with_new_technology)
- [DefenseScoop — Anduril $20B Army contract](https://defensescoop.com/2026/03/14/anduril-20-billion-dollar-army-contract/)
- [Inside Unmanned Systems — Lattice as Army C-UAS core platform](https://insideunmannedsystems.com/u-s-army-enterprise-contract-with-anduril-positions-lattice-as-core-platform-for-c-uas-operations/)
- [SmallCaps — DroneShield $280k US Air Force contract](https://smallcaps.com.au/droneshield-wins-security-contract-us-air-force)
- [Defence Connect — DroneShield Australian Army RfPatrol contract](https://www.defenceconnect.com.au/joint-capabilities/4874-droneshield-wins-australian-army-contract)
- [Fierce Electronics — DroneShield $33M US deal](https://www.fierceelectronics.com/sensors/drone-defense-firm-droneshield-lands-33m-us-government-deal)
- [CALL — Listening to the Sky: acoustic drone detection in Ukraine (Mar 2026)](https://api.army.mil/e2/c/downloads/2026/04/30/af450e75/no-26-1115-listening-to-the-sky-acoustic-drone-detection-in-ukraine-mar-26.pdf)
- [Defense One — Ukraine's cheap sensors (Jul 2024)](https://www.defenseone.com/defense-systems/2024/07/ukraines-cheap-sensors-are-helping-troops-fight-waves-russian-drones/398204/)
- [TWZ — Ukraine's acoustic network eyed by US (Jul 2024)](https://www.twz.com/air/ukraines-acoustic-drone-detection-network-eyed-by-u-s-as-low-cost-air-defense-option)
- [FENEK](https://fenek.com.ua/en/)
- [Militarnyi — Zvook NW0 (EN)](https://militarnyi.com/en/news/ukraine-develops-acoustic-detector-for-fpv-drones/) and [(UK)](https://militarnyi.com/uk/news/v-ukrayini-stvoryly-akustychnyj-detektor-fpv-droniv/)
- [Janes — Echodyne radars under $50k](https://janes.com/defence-news/news-detail/update-echodyne-develops-family-of-metamaterial-electronically-scanning-array-radars)
- [Hvylya — Echodyne $40k–160k, range figures](https://en.hvylya.net/news/1263-bill-gates-backed-radar-firm-claims-10x-cost-edge-over-traditional-air-defense)
- [Unmanned Airspace — Microflown AVISA Skysentry](https://unmannedairspace.info/?p=17423)
- [Hensoldt — Xpeller adds Squarehead Discovair](https://hensoldt.net/news/hensoldt-expands-xpeller-counter-uav-product-family)
- [Mezha — Chuyka 3.0 price and specs](https://mezha.ua/en/blogs/pidtrimayte-zbir-na-pristriy-rer-chuyka-3-0-dlya-zsu-306257/)
- [Foreign Policy — Ukraine's pocket-sized drone detectors](https://foreignpolicy.com/2024/08/05/ukraine-russia-war-drone-detectors-jamming-tsukorok/)
- [everythingRF — MyDefence Wingman 105 specs](https://www.everythingrf.com/products/cuas-counter-unmanned-aerial-system/mydefence/1075-2458-wingman-105)
- [US Army contracts MyDefence for 400 wearables](https://ssbcrackexams.com/us-army-contracts-mydefence-for-400-wearable-counter-unmanned-aerial-systems/)
