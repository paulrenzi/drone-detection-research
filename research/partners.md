---
title: Partners for the alert
parent: Research Notes
nav_order: 0.4
nav_primary: 3.1
nav_label: Partners
---

# Partners: getting the alert to troops on the move
{: .no_toc }

The people who need a road alert are the ones walking or driving it, not someone at a checkpoint screen. This page asks what they already carry that our alerts could ride on, so they get one warning on a device they trust instead of a new box. It goes with [Guarding a road]({{ site.baseurl }}{% link models/route-guard.md %}) and [Central API and military integration]({{ site.baseurl }}{% link research/integration.md %}). Reviewed 2026-10-23.

{: .important }
> **Target Hrafit's Sova module first.** It already pushes FPV alerts to drivers' phones along their route, and it is built from radio intelligence, so it should share the fibre-optic blind spot we fill. Build a TAK output as the fallback that also reaches Delta. Keep our own receiver for units with neither. **First step: ask the Hrafit team whether they take outside sensor feeds.**

1. TOC
{:toc}

## The candidates

| Partner | What troops do with it | How our alert would get in | Fit | What's missing |
|---|---|---|---|---|
| **Hrafit / Sova** | A phone push alert when an FPV or glide bomb approaches. Sova is for "logistics crews, drivers, and medical evacuation" and moves its watch area with the vehicle | A gateway at a checkpoint, or in a vehicle with Starlink, posts our alerts to Hrafit | **Best.** Same users, same job, and our alert shows against the route on the phone | No public interface found. A partnership, not a plug-in |
| **Delta** | The army's map: air, ground and naval picture, messenger, streams | Through TAK, which Delta already links to, or a direct feed via the Ministry of Defence | Commanders and checkpoints more than a driver in the moment | No developer route found |
| **ATAK** | A map app; takes Cursor-on-Target (CoT) position and alert messages | A small gateway turns each alert into a CoT message. Outside sensors do this routinely | **The realistic technical route,** and a way into Delta | How many Ukrainian units run ATAK itself: not found |
| **Meshtastic handhelds** | Texts and position sharing on cheap LoRa radios | A vehicle receiver re-sends each alert as a Meshtastic text, so anyone on foot with one gets a buzz | Closest to our hardware: our boards are sold as Meshtastic kits | Thin, second-hand evidence of use. The receiver would transmit, breaking "a truck gives nothing away". We'd write our own sender, not use their GPL code |
| **Chuyka** | The most common warning device: sound and light alarm against radio FPVs. Now has a phone app that manages several detectors | Nothing today | A partner in the field, the [second box]({{ site.baseurl }}{% link research/competitors.md %}) beside ours | No wired alarm output or third-party protocol found. Shared alert data in its app is only a stated plan |

## Hrafit and Sova

- **What it does:** "pulls together data from nearly all available radio-technical intelligence and surveillance into a single picture". On the ground, it "comes down to one short push notification", to the observation point, sector command and commander at once ([Euromaidan Press, Sep 2026](https://euromaidanpress.com/2026/09/05/from-hq-to-the-zero-line-ukraines-hrafit-system-answers-one-important-question-on-an-ordinary-phone-in-a-trench-and-on-the-road/)).
- **Who has it:** the army, National Guard, SBU and Border Guard. It runs on Android, iOS and the web, and needs a protected phone and satellite internet such as Starlink.
- **Why it fits:** its alerts already follow a moving vehicle, which is the job the road guard needs done. It also solves "where am I": a road alert names a stretch between posts, and a phone shows that against the route, where a bare receiver can't.
- **The gap we fill (inferred):** it lists FPVs, Mavic-type quadcopters, Molniya and Privet drones and glide bombs, and its sources are radio. The article doesn't mention fibre-optic FPVs. That it can't hear them is our inference from its sources, not a quote.
- **Unknown:** whether it accepts outside sensors, and in what format.

## Delta and ATAK

- **Delta** takes data from drones, sensor networks, satellites and partners, is built to NATO standards, and is reported to link with Virazh, Kropyva, Hrafit and the US **ATAK** system, so an alert fed into Hrafit may reach Delta too ([Wikipedia](https://en.wikipedia.org/wiki/Delta_(situational_awareness_system)), [Ukraine's Arms Monitor](https://ukrainesarmsmonitor.substack.com/p/combat-software-in-the-service-of), [Armada International](https://www.armadainternational.com/2024/10/ukraine-delta-system-milcom/)). No developer route was found; access runs through the Ministry of Defence.
- **ATAK** takes CoT, the format the [integration plan]({{ site.baseurl }}{% link research/integration.md %}) already names. A CoT output is the one piece we can build without anyone's permission, and it is the likeliest door into Delta.

## Meshtastic

- Ukrainian units are reported to use Meshtastic for texts and position sharing when other links are down, and a mesh to relay air-raid warnings ([Ukraine War Analytics](https://ukraine-war-analytics.com/cyber/mesh-networking-ukraine.html), [Meshtastic forum](https://meshtastic.discourse.group/t/using-in-ukraine/5685), [Hacker News](https://hn.nuxt.dev/item/47069724)). No official source confirms how widely.
- **The trade:** troops on foot get an alert on a radio some already carry, at no cost. But a vehicle receiver that re-sends is a transmitter, and that's a choice for the unit, not a default.

## Chuyka

- It sounds and flashes on radio-drone activity, and its phone app manages several detectors from one screen; syncing trigger data was a plan, not a feature ([BlueBird](https://www.blue-bird.tech/en/products/chuyka-4-0/), [Razom](https://razomua.media/en/news/tekhnolohiyi/smartfon-zamist-okremoho-prystroyu-chuyka-teper-keruyetsya-z-telefonu-i-bachyt-fpv-za-4-km)).
- No alarm output or protocol was found, so there's nothing to integrate today. If its app opens up, our alerts could appear beside its own on the same phone.

## Next steps

1. **Ask the Hrafit team** whether Hrafit or Sova takes outside sensor feeds, in what format, and whether fibre-optic FPVs are a known gap for them.
2. **Build a CoT output** on the checkpoint gateway: each alert as a TAK event naming the hot stretch. It needs no partner.
3. **Write a Meshtastic sender** only if a unit asks for it, and only as an option they switch on.
4. **Ask BlueBird** whether the Chuyka app will take outside alerts.
