---
title: Projected costs
nav_primary: 2.2
---

# Projected costs
{: .no_toc }

What one unit's net costs to build at three scales, what it costs to keep up, and a suggested price for the proposal. The net is the 20-dart V on [How it works]({{ site.baseurl }}{% link models/line-layout.md %}): 10 listening darts, 10 relay darts and a receiver at each of 3 positions.

**Prototype prices are checked listings.** Small-batch and production prices are our estimates, marked "est.", until a supplier quotes.

1. TOC
{:toc}

## Short answer

- **One unit's net costs about $560 in parts today,** about $580 in a small batch once assembly is paid for, and about $400 in production.
- **The suggested price is $1,795** for a kit of 24 darts and 3 receivers. That is about $600 per position, the price of one radio detector.
- **Re-lays are the real bill.** At four weeks per cell, a unit re-lays 13 times a year. Battery life (T12) decides whether a year of re-lays costs about $1,400 or $13,000.

## Per component

| Component | Prototype: retail, hand-built | Small batch: ~500 darts (est.) | Production: 5,000+ darts, custom board (est.) |
|---|---|---|---|
| Processor and radio | XIAO ESP32S3 + Wio-SX1262 kit, [$15.97](https://store.rokland.com/products/seeed-studio-xiao-esp32s3-wio-sx1262-kit-for-meshtastic-lora) | $13–15, bulk kits | $8–12: one board with an ESP32-S3 ($4–10) and an SX1262 ([Hardware]({{ site.baseurl }}{% link research/hardware.md %})) |
| Microphone, INMP441 | $2.50 ([5-pack, $12.51](https://www.amazon.com/dp/B09G4RNT3G)) | $1–2 | $1–2 |
| 18650 cell | $4.99 ([Samsung 25R](https://www.18650batterystore.com/products/samsung-25r-18650)) | $3–4 | $2.50–3.50: EVE cells at $2.50, when in stock |
| Rod, printed body and fins | $2.60: rod $1.10 ([10-pack, $11](https://www.amazon.com/dp/B0FNZQLH1P)) plus about $1.50 of PETG, wire and screws | $2 | $1–1.50, moulded |
| Windscreen, foam | $0.50 ([10-pack, $4.99](https://www.amazon.com/dp/B07X4VKKQ7)) | $0.50 | $0.30–0.50 |
| Assembly and test | not counted: your time | $5: 15 minutes at $20 an hour | $2–3 |
| **Listening dart** | **~$26.50** | **~$25–29** | **~$15–23** |
| **Relay dart** (no mic, no windscreen) | **~$23.50** | **~$23–26** | **~$14–20** |
| **Receiver** (same board, receive only, powered from the phone or tablet) | **~$20** | **~$22** | **~$14** |

The small batch costs about the same as the prototype because it pays for assembly. Bulk pricing saves about what the labour adds.

**Equipment a unit needs once:**

| Item | Prototype | Production (est.) |
|---|---|---|
| Delivery drone: X500 V2 with Pixhawk 6X, GPS and telemetry radio | [$946](https://pyrodrone.com/products/holybro-x500-v2-pixhawk-development-kit-with-the-pixhawk-6x-standard-m10-gps-915mhz-telemetry-radio) | $400–700: a smaller printed ArduPilot quad with the same electronics |
| Harness for 4 darts: printed plate and rotor, one release servo | about $5: [servo 2-pack, $4.99](https://www.amazon.com/dp/B0DFKPVRC2), plus filament | about $5 |
| Phone or tablet for the alarm and map | the unit's own Android phone | the unit's own Android phone |

## One unit's net

| Build | One trunk: 15 darts | V: 20 darts | V with 4 spares: 24 darts |
|---|---|---|---|
| Prototype | ~$440 | **~$560** | ~$660 |
| Small batch (est.) | ~$460 | **~$580** | ~$685 |
| Production (est.) | ~$320 | **~$400** | ~$475 |

Each net includes its 3 receivers. The 4 spares are 2 listening and 2 relay darts. They cover a drop error of about ±66 ft, which needs 24 darts ([placement]({{ site.baseurl }}{% link models/line-layout.md %}#what-placement-has-to-get-right)), or replace darts that land badly. Add the drone once per unit, or once per several units that share it.

## Keeping it up

Darts aren't recovered. Every net is re-laid when its cells run down, and darts lost to shelling are replaced. A re-lay is 20 darts and 5 sorties.

| Cell life | Re-lays a year | Prototype (~$500 per re-lay) | Production (~$360 per re-lay, est.) |
|---|---|---|---|
| 2 weeks | 26 | ~$13,000 | ~$9,400 |
| 4 weeks | 13 | ~$6,500 | ~$4,700 |
| 12 weeks | 4 | ~$2,000 | ~$1,400 |

None of these cell lives is measured. Listening darts sleep until they hear something. Relay darts keep their radio listening, so they may run down first. Test T12 decides which row is real, and it is the biggest number in the whole budget.

## Suggested pricing for the proposal

The market sets the anchors:

- **DroneAlert:** about $211 per LoRa acoustic module (seller's claims, out of stock).
- **Chuyka 3.0 radio detector:** $584 for defence buyers, $701 with VAT. Its maker calls it the most-requested item units buy with e-points.
- **Zvook NW0:** about $834–950 per sensor, plus 15–18 W of power.

All three are from [the competitor analysis]({{ site.baseurl }}{% link research/competitors.md %}). We set the price so a volunteer appeal can cover a unit's kit, and so one dart stays under $100.

| Item | Suggested price | Margin at small-batch cost | Margin at production cost |
|---|---|---|---|
| **Unit kit:** 24 darts (20 + 4 spares), 3 receivers, mission files for the net | **$1,795** | ~62% | ~74% |
| Dart, either kind, sold singly | $69 | ~63% | ~74% |
| Receiver | $49 | ~55% | ~71% |
| **Re-lay pack:** 20 darts | **$980** ($49 a dart) | ~47% | ~63% |
| Harness only, for a unit's own ArduPilot quad | $89 | high | high |
| Delivery drone with harness, set up and tested | ~$1,250 | ~25% on today's retail parts | higher on a production quad |

- **$1,795 is about $600 per position,** the defence price of one Chuyka. The pitch is "the second box next to the radio detector", for the drones it can't hear.
- **Re-lays are priced lower than the kit,** because a unit buys them every few weeks. They are ammunition, not equipment.
- **A unit's first year at four-week cells** is the kit plus 12 re-lay packs: about $13,500, or about $4,700 at twelve-week cells (the kit plus 3 re-lays). Quote both numbers, as [the competitor analysis]({{ site.baseurl }}{% link research/competitors.md %}#how-to-position) recommends.
- **Sell like Chuyka:** a defence price without VAT with an end-user certificate, a Brave1 Market listing, then e-point eligibility.

These are suggestions for discussion, not a price list. Every margin rests on estimated costs, and every yearly figure on an unmeasured battery life.
