---
title: Competitor analysis and positioning
parent: Research Notes
nav_order: 0
---

# Competitor analysis and positioning
{: .no_toc }

**Use case assumed:** protecting **bases and units in the field** — not national-scale area coverage. Main threats: FPVs (including fibre-optic), Lancet-type loitering munitions, small surveillance and grenade-dropping quads, plus Shahed-class one-way attack drones.

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
| | Sky Fortress (Ukraine) | Phones + mics on poles, national network | km-class vs. Shaheds | $400–1,000 per sensor | Yes |
| | Zvook (Ukraine) | Tower-mounted and vehicle acoustic | Not published | Not published | Yes |
| | Zvook NW0 (Ukraine, announced Jan 2026) | Acoustic FPV sensor for positions and routes, incl. fibre-optic; 15–20 W, wired or LoRa | 150–450 m | Not published | Yes |
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

### Sky Fortress and Zvook (Ukraine)
- Prove that low-cost acoustic networks work in war. Sky Fortress: ~14,000 sensors, $400–1,000 each, national scale, tuned for Shaheds and cruise missiles. Zvook: tower-mounted, now trialling a vehicle version with NATO.
- **Gaps for our use case:** built for **area** coverage of loud engine drones over cellular networks, not portable kits for units facing FPVs.
- **Implication:** the closest direct competitors on cost, already selling to NATO countries (Lithuania). Possible **partners** for Shahed/Lancet recordings.

### Soldier-worn RF detectors — MyDefence Wingman, Chuyka
- Cheap, popular and proven: Chuyka 3.0 ~$750–850, detects analog FPV video at up to 4 km; Wingman up to 6 km, US Army bought 400.
- **Gaps:** detect radio, not drones. **Fibre-optic FPVs, digital/encrypted links and pre-programmed drones are invisible to them.** Usually no direction or position, so nothing to put on a map.
- **Implication:** the price anchor a soldier already understands (~$1k per detector). Our pitch is what they miss.

## Who covers which threat

| Threat | Prime (WISP/Pulsar) | Radar (Echodyne) | RF wearables | Premium acoustic | **Our acoustic kit** |
|---|:-:|:-:|:-:|:-:|:-:|
| FPV, radio-controlled, line of sight | ✅ | ✅ | ✅ | ✅ | ✅ (short range) |
| **Fibre-optic FPV** | ⚠️ camera only | ✅ if line of sight | ❌ | ✅ | ✅ |
| **Pre-programmed / radio-silent drone** | ⚠️ camera only | ✅ | ❌ | ✅ | ✅ |
| **Low drone behind trees, buildings, ridges** | ❌ | ❌ | ⚠️ if it transmits | ✅ | ✅ |
| Shahed-class at long range | ✅ | ✅ | ❌ | ✅ | ✅ |
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

## Conclusion — how to position

**On cost:** sit at the **price of a soldier's RF detector** ($1–3k per kit), not the price of a sensor system. That's 20–100× below radar and prime systems and close to what units already buy with their own budgets or donations. The comparison to lead with: *"a whole perimeter for the price of two Chuykas."*

**On capability:** don't compete on range or long-distance accuracy — WISP and radar win there. Own the gaps they leave:

1. **Hears what radio detectors can't:** fibre-optic and autonomous drones, the fastest-growing FPV threat.
2. **Hears what cameras and radar can't see:** low drones masked by terrain, trees and buildings.
3. **Passive and low-signature:** no radar emission for the enemy to target.
4. **Many and cheap:** losing a node costs $100; losing a radar costs $100k.

**On integration:** be a **sensor, not a platform**. Output Cursor-on-Target to ATAK, SAPIENT for NATO, and target a Lattice integration — Lattice is becoming the US Army's counter-drone backbone, so being a cheap sensor that feeds it is worth more than a competing dashboard. Acoustic bearings that point WISP or a camera at a drone it couldn't otherwise find makes the expensive systems better.

**One-line positioning:**
> *The passive acoustic layer that catches the drones radio detectors and cameras miss — at the price of a radio detector.*

## Risks to this positioning

- **Sky Fortress or Zvook** ship a portable unit kit first — they already have data, combat credibility and NATO customers. Partner, or move faster on the field-kit form factor. **Update (2026-10-15):** Zvook announced the [NW0](https://militarnyi.com/en/news/ukraine-develops-acoustic-detector-for-fpv-drones/), an acoustic FPV sensor for front-line positions and routes, in January 2026. No price or deployment reported yet. See [Is the problem worth solving?]({{ site.baseurl }}{% link research/problem-check.md %})
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
- [Janes — Echodyne radars under $50k](https://janes.com/defence-news/news-detail/update-echodyne-develops-family-of-metamaterial-electronically-scanning-array-radars)
- [Hvylya — Echodyne $40k–160k, range figures](https://en.hvylya.net/news/1263-bill-gates-backed-radar-firm-claims-10x-cost-edge-over-traditional-air-defense)
- [Unmanned Airspace — Microflown AVISA Skysentry](https://unmannedairspace.info/?p=17423)
- [Hensoldt — Xpeller adds Squarehead Discovair](https://hensoldt.net/news/hensoldt-expands-xpeller-counter-uav-product-family)
- [Mezha — Chuyka 3.0 price and specs](https://mezha.ua/en/blogs/pidtrimayte-zbir-na-pristriy-rer-chuyka-3-0-dlya-zsu-306257/)
- [Foreign Policy — Ukraine's pocket-sized drone detectors](https://foreignpolicy.com/2024/08/05/ukraine-russia-war-drone-detectors-jamming-tsukorok/)
- [everythingRF — MyDefence Wingman 105 specs](https://www.everythingrf.com/products/cuas-counter-unmanned-aerial-system/mydefence/1075-2458-wingman-105)
- [US Army contracts MyDefence for 400 wearables](https://ssbcrackexams.com/us-army-contracts-mydefence-for-400-wearable-counter-unmanned-aerial-systems/)
