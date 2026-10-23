---
title: What the line gains in lives
parent: Research Notes
nav_order: 0.3
---

# What the forward line gains in lives
{: .no_toc }

We estimate what a minute of warning from a forward listening line does for troops' lives, compared with the ~10 seconds a sensor at the position gives, and with the partner systems each could cue. This is a Fermi estimate. Each input is marked **measured**, **claimed** (a source says so, unverified) or **guess** (ours). No source measures what warning does to drone casualties, so the result is a range, not a number. What troops already carry is on [What troops have, and what listening adds]({{ site.baseurl }}{% link research/frontline-kit.md %}). Reviewed 2026-10-15.

1. TOC
{:toc}

## Short answer

- **At a fixed position, a minute adds little over 10 seconds.** Shotguns, net-guns and turrets have the drone in range for only about 1–4 s, so seconds of warning are enough to have them ready ([A minute against the alternatives]({{ site.baseurl }}{% link research/problem-check.md %}#a-minute-against-the-alternatives)).
- **A minute matters for people about to move:** rotation, resupply, evacuation, recovery. About half of casualties happen in the rear doing exactly this. Ten seconds is too late for them, but a minute lets them hold or change a movement.
- **Our central guess:** the line averts **about 1–4 of every 100 drone casualties** in a unit that uses it. The plausible range is **0.3–14**.
  - The low end is a unit that already has a radio detector, in a sector with few fibre-optic FPVs.
  - The high end is a unit with no radio detector, in a sector where most FPVs are fibre-optic.
- **Partner systems:**
  - Jammers and interceptors make the line's minute more useful against radio-controlled drones.
  - Against fibre-optic drones, nothing but avoidance works, and only the line gives a minute's warning of them.
- **Three tests decide which end of the range is real:**
  - T18: do troops act on alerts?
  - T9/T17: does the alert get out of the trees?
  - T11: does a listener hear an FPV?

## Scale

| Input | Value | Type |
|---|---|---|
| Ukrainian casualties, Feb 2022 – Dec 2025 | 500,000–600,000, of whom 100,000–140,000 killed ([CSIS, Jan 2026](https://www.csis.org/analysis/russias-grinding-war-ukraine)) | claimed (estimate) |
| Share caused by drones | "80% was the most common answer, with a range of 75-95%", from 15+ battalion and brigade commanders ([Rob Lee, ChinaTalk, Oct 2025](https://www.chinatalk.media/p/ukraines-drone-war)) | claimed (interviews) |
| Share taken in the rear | "approximately 50% of their casualties are taken in the rear from Russian FPVs, artillery and glide bombs", during rotation, resupply and recovery ([RUSI, Feb 2025](https://static.rusi.org/tactical-developments-third-year-russo-ukrainian-war-february-2205.pdf)) | claimed (brigade reports) |
| Fibre-optic share of FPVs | 30–50% in some sectors, up to 90% in one Kharkiv sector ([sources]({{ site.baseurl }}{% link research/problem-check.md %}#the-threat-is-real-and-is-the-main-killer)); no front-wide figure | claimed, varies by sector |
| Casualties per company or per km of front | Not found | none |

**What this implies (our arithmetic):**
- Drones account for roughly 9,000–10,000 Ukrainian casualties a month (CSIS total × 80%, spread over about 46 months).
- If every unit fielded a line and the central guess held, that would be on the order of 100–400 casualties a month averted.
- That is an upper bound for the idea, not a forecast. No unit-level casualty rate was found, so we can't yet say what one line saves one battalion.

## The chain, per 100 drone casualties

A minute of warning only saves someone who meets all five conditions:
1. They are about to be exposed.
2. They are threatened by a drone that flies in across the line.
3. The line hears that drone.
4. The alert reaches them.
5. They act on it in a way that avoids the hit.

| Step | Central guess | Range | Type | What would measure it |
|---|---|---|---|---|
| Drone casualties among people moving in the rear (rotation, resupply, recovery, evacuation) | 50 of 100 | 35–60 | claimed (RUSI: about half, but that figure includes artillery and glide bombs) | unit casualty logs (T18) |
| …from FPVs that fly in across the line, not ones already waiting in ambush or launched inside it | 50% | 30–70% | guess. Fibre-optic FPVs wait by roads for up to 12 h ([Trench Art](https://www.trenchart.us/p/russias-best-drones-lie-in-wait-beside)) and stay silent until launch | T18 |
| …that the line hears | 60% | 40–85% | guess. No FPV has been range-tested acoustically | T11 |
| …where the alert gets through | 80% | 60–95% | guess | T9, T17 |
| …where troops act on it rather than ignoring it (false-alarm fatigue) | 60% | 30–80% | guess | T18 |
| …and acting avoids the hit (holding the run, stopping under trees, delaying the evacuation) | 50% | 30–70% | guess | T18 |
| **Averted, unit with no radio detector** | **≈3.6** | **≈0.4–14** | | |
| **Averted, unit that already has a radio detector** (the line adds only fibre-optic FPVs, 30–50% of them) | **≈1–2** | **≈0.1–7** (up to the full figure where fibre-optic is ~90%) | | |

The ranges multiply the low ends together and the high ends together, so the true value is very unlikely to sit at either extreme.

**Not yet subtracted:**
- **Harm from alerts themselves.** In Israel, people running for shelter after sirens are themselves injured. A front-line false alarm that sends troops into the open would cost lives.
- **Giving away positions.** An alert or a jammer that transmits can reveal the unit's position. The tripwire's listeners only receive at the unit, but a cued jammer transmits.
- **Hours lost.** Movements held on false alarms cost time; whether units would accept that is a T18 question.

## A minute against 10 seconds, with partner systems

| Partner system | With ~10 s (sensor at the position, or a soldier's ear) | With ~1 min (forward line) | What the minute adds in lives |
|---|---|---|---|
| **Shotgun, rifle, net-gun** | Enough: the drone is in range for about 1–4 s | Same | ≈0 |
| **AI turret** | Enough to slew and track | Same | ≈0 |
| **Cover at the position** | Enough if the dugout is a few yards away | Smoke and dispersal also become possible | small |
| **Holding a movement** (vehicle, resupply, walkers, evacuation) | Too late: they are already in the open | A go/no-go call before setting out. Russia's roadside drone "traffic lights" do this on roads ([Espreso, Dec 2024](https://global.espreso.tv/russia-ukraine-war-russia-installs-traffic-lights-to-counter-ukrainian-fpv-drones)) | **most of the chain above** |
| **Cued jammer** (e.g. CERBAIR MEDUSA, [partners]({{ site.baseurl }}{% link research/competitors.md %}#partners-and-the-budget-we-compete-for)) | Switches on while the drone is already on its final approach | Switches on early and only when a drone is coming, so it transmits less. Also covers radio links its own detector misses | radio FPVs only, and fading: "Jamming no longer works", says a brigade EW commander; **none against fibre-optic** |
| **Interceptor drone** | Can't launch and climb in time | Plausibly the minimum lead time (our inference; no source gives launch-to-intercept times against FPVs) | unknown |
| **Nets, tunnels, cable traps** | Need no warning | Need no warning | ≈0; they compete with the line for the same budget |

**What this shows (inference):**
- Against **radio-controlled FPVs**, a radio detector already gives a minute, and partner jammers already depend on it. The line adds little there beyond cueing jammers for drones the detector misses, and jamming itself is losing ground.
- Against **fibre-optic FPVs**, jammers do nothing and weapons get only seconds whatever the warning. The line's minute is the only early warning available, and its value is entirely in **avoidance by people who are about to move**.
- So the line's value grows with the fibre-optic share in a sector and with how much movement the unit has to make in the open.

## Is it worth the cost?

The tripwire costs about $1.9–2.9k for a unit's package and about $10.5–17k a year in re-lays at four-week cells ([running cost]({{ site.baseurl }}{% link models/tripwire.md %}#the-running-cost-lines-are-ammunition)).

**Inference (rule of thumb, no source):** if a battalion takes even a few dozen drone casualties a year, averting 1–4% of them is plausibly worth that cost. It is not worth it where:
- most drone casualties come from FPVs already waiting in ambush, or launched inside the line; or
- the roads are already netted.

## The Israeli analogue

- **What was found:** Zucker and Kaplan modelled rocket casualties in Sderot and found expected casualties per rocket would be "between three (best-case) and nine (worst-case) times higher" without civil defence ([Studies in Conflict & Terrorism, 2014](https://ideas.repec.org/a/taf/uterxx/v37y2014i3p258-266.html)).
- **Why it doesn't transfer directly:**
  - That civil defence was "safe rooms, bomb shelters, early detection alarms, and missile defense" together, so the share due to warning alone is not separated.
  - Civilians in a town are not soldiers on the move.
- **What it does show:** warning paired with somewhere to go saves many lives. Warning with nowhere to go saves few. The line's minute is worth most where troops have a real alternative to moving.

## What would change this estimate

- **T18 (interviews):**
  - What share of a unit's drone casualties happen while moving.
  - How many come from FPVs that wait in ambush.
  - Whether drivers and medics would hold a movement on an alert.
- **T11:** whether a listener hears an FPV at all, and at what distance.
- **T9/T17:** whether the alert gets out of the trees.
- **A unit casualty rate:** with one, the estimate becomes lives per battalion per year, and can be set against the re-lay cost.
