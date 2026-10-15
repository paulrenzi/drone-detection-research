---
title: Is the problem worth solving?
parent: Research Notes
nav_order: 0.25
---

# Is the problem worth solving?
{: .no_toc }

Before building more, check the premise: are units' current methods failing, would earlier warning change anything, and is someone already solving it? Every point is sourced; where nothing was found, this page says so. Reviewed 2026-10-15.

1. TOC
{:toc}

## Short answer

**The case for the problem is strong.** Drones are the biggest killer at the front. Troops survive mainly by staying hidden and not moving, which is coping, not protection. The fastest-growing part of the threat, fibre-optic FPVs, defeats the cheap detectors units carry, and the expensive camera systems are not at the front. A Ukrainian firm is now building acoustic FPV sensors for positions, which supports the approach.

**One link is unproven:** whether **earlier warning changes what troops do**. No source measures it, and it is the claim the tripwire rests on. It is also the cheapest thing to check: ask the people who would use it (T18), before any more hardware.

## What the evidence says

### The threat is real and is the main killer

- **Drones cause about 80% of casualties**, according to analyst Rob Lee and others. Most casualties fall in the kill zone, a band roughly 10–20 miles deep on each side of the line ([NPR, 5 Oct 2026](https://www.tpr.org/news/2026-10-05/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)).
- **Tree-line positions are targets in themselves.** Incendiary drones are flown along tree lines to burn away the foliage troops hide in ([RUSI](https://www.rusi.org/news-and-comment/in-the-news/ukraines-fire-dropping-drones-can-find-shock-russian-troops-experts)). Night is no refuge: FPVs carry thermal cameras (same NPR report).
- **Fibre-optic FPVs are a large share in some sectors.** Estimates run from 30–50% of FPV operations in some sectors ([drone-warfare.com](https://drone-warfare.com/research/fpv-drone-warfare/), rated medium confidence there) to a claim of 90% of Russian attacks in one Kharkiv-region sector by a Ukrainian operator ([Gwara Media](https://gwaramedia.com/en/russians-expand-area-for-using-fiber-optic-drones-in-kharkiv-oblast-in-2026-military-says/)). No front-wide figure was found.

### What units do today, and how well it works

There is no single "current model". At the front it is a set of coping measures:

| Measure | What it does | Where it falls short |
|---|---|---|
| **Stay underground and hidden** | The main defence. Troops move on foot, slowly, and hide when they hear a drone: one group took four hours to cover 1 km ([NPR](https://www.tpr.org/news/2026-10-05/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)) | It works by not moving, at a huge cost: rotations take hours to days, and some infantry have gone more than a year without one (same source) |
| **Nets** | Physical barrier over positions and routes (same source) | Static; no warning |
| **Listening by ear** | Troops hide when they hear one (same source) | Short-range. In a quiet field, 2 of 24 people faintly heard a Mavic-class drone at 150 m and none at 250 m ([Li et al. 2020](https://www.mdpi.com/2076-3417/10/16/5501)). No figure for FPVs or combat noise |
| **Radio detectors** (Chuyka and similar, ~$584–701) | Warn of FPVs by their video signal, up to about 4 km ([site note]({{ site.baseurl }}{% link research/competitors.md %})) | Blind to fibre-optic FPVs ([Kyiv Independent](https://kyivindependent.com/as-russias-fiber-optic-drones-flood-the-battlefield-ukraine-is-racing-to-catch-up/)) |
| **Shotguns** | Last-ditch kill | FPVs close at close to 100 km/h, giving infantry "only a moment to react" ([RFU News, Nov 2025](https://www.rfunews.com/articles/insider-annual-why-shotguns-are-suddenly-the-most-valuable-defense-against-fpv-drones)) |
| **Interceptor drones** | Kill drones in the air | Built mostly for Shaheds and reconnaissance wings. They work only inside a radar or acoustic sensor's detection zone ([Ukrainska Pravda, Mar 2026](https://www.pravda.com.ua/eng/articles/2026/03/11/8025014/)) |

**Cameras like Anduril's WISP are not the current model at the front.** We found no reporting of WISP deployed in Ukraine; the published deployment is the Washington National Guard training on it for World Cup security ([DroneXL](https://dronexl.co/2026/08/06/anduril-wisp-washington-national-guard-drones-birds/)). It also needs line of sight, which tree lines block.

### Is ten seconds enough?

**No published figure answers this.** No source we found says how many seconds of warning troops need, or measures what a detector's warning saves. Detector makers describe the value as seconds to find cover. The serious analyses argue for warning but don't measure it:
- **RUSI (Oct 2024)** says smoke against FPVs and Lancets is "highly effective" if the unit is warned promptly, and only with a low false-alarm rate. Neither claim has a footnote ([Watling & Bronk](https://afghanistan.wilsoncenter.org/sites/default/files/media/uploads/documents/protecting-the-force-from-uncrewed-uas.pdf), p.17).
- **RUSI (Feb 2025):** Ukrainian brigades report about half their casualties in the rear, during rotation, resupply and recovery ([Watling & Reynolds](https://static.rusi.org/tactical-developments-third-year-russo-ukrainian-war-february-2205.pdf)). Warning that covers only the position misses those.
- **An Israeli vendor's CEO** says "we just need 30 seconds warning" to take defensive action ([Ynet](https://www.ynetnews.com/article/s1oz79p011x)). That is a vendor's view, not a measurement.

What follows is inference:

- **Troops already underground** need warning only when they are exposed: on the move, collecting a drone-delivered resupply, observing, repairing, fighting.
- **Ten seconds** is enough to step into a dugout a few metres away. It is not enough for people strung out on a four-hour walk, or to launch an interceptor.
- **A minute** could let walkers get off a path and under cover, or hold a resupply pickup until the drone has passed. Whether units would act on it is the open question.

### Someone is already building the near-unit layer

**ZVOOK NW0** (announced January 2026): a Ukrainian acoustic sensor for FPVs, including fibre-optic ones. Claimed 150–450 m range, 360°, 15–20 W, linked by fibre, twisted pair, LTE or LoRa, spaced 400–600 m, pitched for front-line positions, frontline towns and logistics routes. No deployment reported ([Militarnyi](https://militarnyi.com/en/news/ukraine-develops-acoustic-detector-for-fpv-drones/)).

**Every performance figure is the maker's claim.** The specs come from Zvook's own announcement, which news sites repeated. It is now on public sale at about $834–950 per sensor, but we found no independent test and no unit reported using it ([profile]({{ site.baseurl }}{% link research/competitors.md %}#zvook-nw0--direct-competitor-claims-only)). So it's weak validation: a credible team with existing customers thinks acoustic FPV detection is worth building. It isn't proof that the approach works. It's also competition.

**Nor does anyone else prove it.** The US Army's March 2026 review of Ukrainian acoustic networks says they detect FPVs. Its cited sources cover Shaheds and cruise missiles over the rear, not FPVs at the front ([details]({{ site.baseurl }}{% link research/competitors.md %}#two-markets-only-one-of-them-ours)). Cheap acoustic detection is proven against Shaheds. Against FPVs at a position, it's still unproven, for us and for Zvook alike. Where we would still differ: battery power for weeks instead of 15–20 W of wired power, throwaway cost, and lines laid forward rather than sensors at the unit.

## What a minute buys

Suppose a unit knows a drone is coming a minute before it arrives. What do troops actually do with that? Against fibre-optic FPVs, jamming does nothing, so every defence is physical: avoid being found, block the drone, or shoot it down.

| Defence | In use? | Does warning help? |
|---|---|---|
| **Get under cover and stop moving** | The main defence. Troops already hide when they hear a drone ([NPR](https://www.tpr.org/news/2026-10-05/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)) | **Yes, most.** A minute gets people off a path, out of the open and below ground, or lets the unit hold a resupply pickup, a vehicle run or a casualty evacuation until the drone has passed (inference) |
| **Shotguns and mobile shooter teams** | Yes. Two shotgun-armed shooters per vehicle, and teams that patrol known drone routes ([United24, Oct 2025](https://united24media.com/war-in-ukraine/can-fiber-optic-drones-be-stopped-how-ukraine-faces-the-unjammable-threat-12502)). Their task is to "detect drones quickly" ([VGI, May 2026](https://vgi.com.ua/en/nets-fire-teams-and-lasers-inside-the-fight-against-fiber-optic-drones/)) | **Yes.** A shooter who knows a drone is inbound, and from which line, is ready and facing the right way instead of reacting at the last moment (inference) |
| **Net-guns** | Yes, carried as a "last-resort" weapon for a drone already very close ([United24](https://united24media.com/war-in-ukraine/can-fiber-optic-drones-be-stopped-how-ukraine-faces-the-unjammable-threat-12502)) | A little: readiness only |
| **Automated turrets** | A Brave1-developed AI turret that can shoot down fibre-optic FPVs was in more than ten front-line units by May 2026; sensors and weapon not published ([Euromaidan Press](https://euromaidanpress.com/?p=405676)). Scan Horizon, a net-firing demonstrator, hears drones at up to 20 m with microphones ([Defense Post](https://thedefensepost.com/2026/05/08/ukraine-autonomous-net-turret/amp/)) | **Possibly.** A cue could wake a turret or point it the right way. Whether these turrets accept outside cues is not published |
| **Nets over positions, dugouts and roads** | Everywhere: "All positions, 'from infantry to artillery,' are draped with nets" ([United24](https://united24media.com/war-in-ukraine/can-fiber-optic-drones-be-stopped-how-ukraine-faces-the-unjammable-threat-12502)). They burn and melt (same source), and small gaps let drones through ([VGI](https://vgi.com.ua/en/nets-fire-teams-and-lasers-inside-the-fight-against-fiber-optic-drones/)) | No. Static, always up |
| **Cable traps** (barbed wire, heated wire) | Reported, not standard ([VGI](https://vgi.com.ua/en/nets-fire-teams-and-lasers-inside-the-fight-against-fiber-optic-drones/), [United24](https://united24media.com/war-in-ukraine/can-fiber-optic-drones-be-stopped-how-ukraine-faces-the-unjammable-threat-12502)) | No. Passive |
| **Interceptor drones** | Scaling fast, but built mostly for Shaheds and reconnaissance drones, working inside a radar or acoustic sensor's coverage ([Ukrainska Pravda](https://www.pravda.com.ua/eng/articles/2026/03/11/8025014/)). No verified report found of one stopping an FPV attacking a position | Only if one is ready to launch; unproven against FPVs |
| **Lasers** | Explored, including burning through the fibre ([VGI](https://vgi.com.ua/en/nets-fire-teams-and-lasers-inside-the-fight-against-fiber-optic-drones/)) | Unknown |

**What this means (inference):**

- **Warning mostly buys avoidance, not a kill.** The biggest gain is people not being in the open when the drone arrives. That fits how troops already survive.
- **It turns a reflex shot into a prepared one** for shooters, and could cue the automated turrets now reaching units.
- **It matters most where exposure is a choice of timing:** resupply pickups, walking rotations, vehicle runs, casualty evacuation. In those moments a unit can wait a minute.
- **It does nothing against a drone already waiting** on the ground in ambush, or against one launched from inside the line.

So the question for T18 is not just "would warning help?" but **which of these moments matter most, and how often**.

## A minute against the alternatives

The table above asks whether warning helps. This one asks **how much each defence needs**, and so what a minute adds over the few seconds that other sources of warning already give. Reviewed 2026-10-15.

### How much warning each source gives

Warning is the distance at which the drone is detected, divided by its speed. FPVs reach "a top speed of 140 kilometers an hour" ([ERR, Nov 2025](https://news.err.ee/1609861089/err-in-ukraine-up-close-with-ukraine-s-counter-drone-air-defense-teams)), so the figures below take 100–140 km/h (28–39 m/s). They are our arithmetic, not measurements, and they ignore the second or two needed to recognise the sound.

| Source of warning | Detects at | Warning vs an FPV (est.) | Against fibre-optic FPVs? |
|---|---|---|---|
| None: drone seen at the last moment | — | 0 s | — |
| A sentry's ear | ~150 m (Mavic-class, quiet field, [measured](https://www.mdpi.com/2076-3417/10/16/5501)) | ~4–5 s | Yes, if it is heard |
| Acoustic sensor at the position | 120 m (DroneAlert) to 450 m (NW0), both makers' claims | ~3–16 s | Yes, on the makers' claims |
| Radio detector (Chuyka 3.0) | "up to 4 kilometers", scanning every "4 to 8 seconds" ([Militarnyi, May 2025](https://militarnyi.com/en/news/ukraine-develops-chuyka-3-0-drone-video-signal-detector/)) | ~1.5–2.5 min | **No**: it hears only analog video |
| **Forward listener line** | 2–4 km out | **~50 s–2.5 min** | Yes, if the listeners hear it (T11) |

**A minute is not new. A radio detector already gives one against radio-controlled FPVs.** What is new is a minute against fibre-optic FPVs, where every other source drops to seconds.

### What each defence needs, and what each window buys

The middle column is sourced. The four right-hand columns are our inference from it. ✅ the window is enough; 🟡 helps partly; ❌ not enough; — makes no difference.

| Defence | What it needs (sourced) | 0 s | ~5 s | ~15 s | ~1 min |
|---|---|:-:|:-:|:-:|:-:|
| **Net-gun** | Range "up to 25 metres", net open "within 0.2 seconds" ([MITLA-1, Ukrainska Pravda, Jul 2025](https://www.pravda.com.ua/eng/news/2025/07/12/7521456/)); up to 30 m, 2 s reload ([Ptashka 2.0, Mezha](https://oboronka.mezha.ua/en/ptashka-drones-predstavila-sitkomet-ptashka-2-0-310877/)). At FPV speed that is about one second of flight in range | 🟡 last ditch | ✅ in hand, facing it | ✅ | — |
| **Shotgun or rifle** | 10–15 m from a large FPV is "life-threatening"; shoot at "at least 40–50 meters", rifles at 50–100 m ([Militarnyi, Jun 2026](https://militarnyi.com/en/news/shotguns-ineffective-15-inch-fpv-drones/)). That is about 1–4 s of flight in range | 🟡 reflex | ✅ weapon up | ✅ facing the right way | 🟡 team moves to the threatened side |
| **AI turret** | Detects and tracks itself; the operator "only needs to confirm engagement with a single button press" ([Ukrinform, May 2026](https://ukrinform.net/rubric-ato/4121457-ukraines-defense-minister-shows-ai-turret-used-in-combat-to-intercept-drones-on-battlefield.html)). Reaction time and whether it takes outside cues: not published | 🟡 on its own sensors | — | — | 🟡 only if it accepts cues |
| **Smoke** | "highly effective if the unit being targeted can be warned promptly"; no seconds given ([RUSI, Oct 2024](https://static.rusi.org/protecting-the-force-from-uncrewed-uas.pdf)). It "risks drawing Russia's attention" ([Business Insider, Dec 2025](https://www.aol.com/articles/hunted-drones-ukrainian-forces-hide-113401181.html)) | ❌ | 🟡 a screen may not be up in time | ✅ probably | ✅ |
| **Get under cover** | No published distance to shelter or time to reach it. On foot at 3–5 m/s (our assumption), 5 s covers ~15–25 m and 1 min ~200–300 m | ❌ | 🟡 next to a dugout | 🟡 within ~50–75 m | ✅ off a path and under cover |
| **Hold a movement** (vehicle run, resupply pickup) | Russian roadside "traffic lights" (yellow means "a distant drone detection") let drivers "navigate risky areas at safer times" ([Espreso, Dec 2024](https://global.espreso.tv/russia-ukraine-war-russia-installs-traffic-lights-to-counter-ukrainian-fpv-drones)) | ❌ | ❌ | ❌ | ✅ don't set off; stop under cover |
| **Casualty evacuation** | Troops "often have to wait for nighttime, fog, or rain" to evacuate; the golden hour has become a "golden day" ([Business Insider, Dec 2025](https://www.aol.com/articles/hunted-drones-ukrainian-forces-hide-113401181.html)) | ❌ | ❌ | ❌ | 🟡 may let a team move between drones rather than wait for dark; unproven |
| **Interceptor drone** | Piloted "using VR goggles", over 160 km/h, built for Shaheds ([Militarnyi, Oct 2024](https://militarnyi.com/en/news/ukrainian-engineers-launch-sting-interceptor-against-shahed-drones)). No published time from cue to launch, and no verified kill of an FPV attacking a position | ❌ | ❌ | ❌ | 🟡 only with one on the pad and a pilot ready; also needs a track, which a line crossing doesn't give |
| **Laser** (Tryzub) | FPVs at "around 800–900 meters", with radar integration ([Euromaidan Press, May 2026](https://euromaidanpress.com/2026/05/08/tryzub-laser/)). Time needed on target: not published. Rare at the front | ❌ | ❌ | 🟡 | 🟡 cue to slew, if one is present |
| **Nets, net tunnels, cable traps** | Always up. Ukraine plans another 4,000 km of net-covered road by the end of 2026 ([Liga.net, Feb 2026](https://news.liga.net/en/politics/news/another-4000-km-of-roads-will-be-covered-with-anti-drone-tunnels-in-ukraine-by-the-end-of-the-year-photo)) | ✅ | — | — | — |
| **Jamming** | Triggers the drone's own fail-safe by drowning its radio and GNSS links. Crews use detectors to decide when to switch jammers on ([Foreign Policy, Aug 2024](https://foreignpolicy.com/2024/08/05/ukraine-russia-war-drone-detectors-jamming-tsukorok/)); site jammers such as CERBAIR MEDUSA are built to be switched on by a detector's cue ([spec sheet](https://comsecfl.com/wp-content/uploads/2022/04/Specsheet_Medusa.pdf)). **No effect on fibre-optic FPVs** | ❌ | 🟡 radio FPVs only | ✅ radio FPVs only | ✅ radio FPVs only; less time transmitting |

### What this shows (inference)

- **Weapons need seconds, not a minute.** A net-gun, shotgun or rifle has about 1–4 seconds of the drone's flight in range. A few seconds' warning gets the weapon up and facing the right way; more adds little. A sensor at the position, if it works and gives a bearing, already covers most of that. **The minute is not a weapons cue.** The tripwire should not be pitched as one.
- **The minute buys one thing nothing else gives against fibre-optic FPVs: a go/no-go call on exposure.** Don't set off, stop the vehicle under cover, hold the resupply pickup, get the walkers off the path. Seconds can't do this; only something 1–4 km out can.
- **Someone already pays for this.** Russia's roadside traffic lights exist to time movement around drones. That is the same job as a forward line, done for roads.
- **Above a minute, units fall back on hours.** Evacuations wait for night, fog or rain. A minute's warning competes with that free, slow default. Whether units would trade it for faster moves between drones is exactly what T18 must ask.
- **Always-on defences need no warning at all.** Nets, net tunnels and cable traps are scaling fast, and anything a minute protects must be outside them.

**Pairing, not replacing:** a forward line for go/no-go decisions, and the ear, a radio detector or a sensor at the position for the last seconds a weapon needs.

**In lives:** our central guess is that the line averts about 1–4 of every 100 drone casualties in a unit that uses it (range 0.3–14), almost all among people about to move. See [What the line gains in lives]({{ site.baseurl }}{% link research/lives-model.md %}) and [what troops already have]({{ site.baseurl }}{% link research/frontline-kit.md %}).

{: .warning }
> Almost every timing here is inference. No source gives the seconds of warning a defence needs, the time to reach cover, the time to build a smoke screen, or the time from cue to interceptor launch. A shallow search also found nothing on Scan Horizon or Sky Sentinel reaction times. These are T18 questions.

## What would make it a waste

Any of these, found by asking users or by testing:

1. **Warning doesn't change behaviour.** Troops stay hidden by default, hear drones themselves in time, and would not act differently with a minute.
2. **Exposure is mostly on the move, not at positions.** Then the tripwire must be re-aimed: lines along approach paths and covered footpaths to warn walkers, not around a position. That is a change of aim, not a dead end (inference).
3. **A cheap enough sensor is already in units' hands**, such as the NW0 at scale.
4. **Radio can't get out of the trees**, even with a [wired edge receiver]({{ site.baseurl }}{% link models/tripwire.md %}#getting-alerts-out-of-the-trees) (T9, T17).

## The next step: ask before building (T18)

Talk to 5–10 people with recent front-line experience: soldiers, the volunteers who equip units, Brave1, and Ukrainian drone and EW firms. Ask:

1. When are you most exposed to FPVs: in position, on rotation, at resupply pickups, observing?
2. How do you know a drone is coming now, and how much warning does that give?
3. What would you do differently with 10 seconds, one minute, three minutes? Would you hold a resupply pickup, a vehicle run or an evacuation? Would shooters or a turret be ready?
4. Roughly what share of FPVs attacking you are fibre-optic?
5. Would you place 10 listeners by hand, or accept a receiver on a pole at your tree-line edge?
6. Who decides what kit a unit gets, and who pays: the unit, volunteers, or the state?
7. Is your position in a windbreak, a forest, a field or ruins?
8. Roughly how far is it from the tree edge that faces open ground?

**Pass:** most say a minute's warning would change what they do, and name the moment it matters. **Fail:** most say it wouldn't. Either answer is worth more than T9.
