---
title: Projected costs
nav_primary: 2.2
---

# Projected costs
{: .no_toc }

What one unit's package costs us at three scales, what it costs to keep up, and what it sells for once our markup is added. The package is everything a unit needs to lay and run the two-trunk net on [How it works]({{ site.baseurl }}{% link models/line-layout.md %}): the darts, the receivers, and the drone that lays them.

**Prototype prices are checked listings.** Small-batch and production prices are our estimates, marked "est.", until a supplier quotes.

1. TOC
{:toc}

## Short answer

- **One unit's package costs us about $1,810 today,** about $1,710 in a small batch and about $1,180 in production. That is 24 darts, 3 receivers, and a delivery drone with harness, batteries and charger.
- **The drone is more than half the package** until a production quad replaces the $946 kit.
- **The price is our cost plus our markup.** At 50%, the package sells for about $2,560 in a small batch, or about $855 per position.
- **Re-lays are the real bill.** At four weeks per cell, a unit re-lays 13 times a year. Battery life (T12) decides whether a year of re-lays costs us about $1,400 or $13,000.

## Per component

| Component | Prototype: retail, hand-built | Small batch: ~500 darts (est.) | Production: 5,000+ darts, custom board (est.) |
|---|---|---|---|
| Processor and radio | XIAO ESP32S3 + Wio-SX1262 kit, [$15.97](https://store.rokland.com/products/seeed-studio-xiao-esp32s3-wio-sx1262-kit-for-meshtastic-lora) | $13–15, bulk kits | $8–12: one board with an ESP32-S3 ($4–10) and an SX1262 ([Hardware]({{ site.baseurl }}{% link research/hardware.md %})) |
| Microphone, INMP441 | $2.50 ([5-pack, $12.51](https://www.amazon.com/dp/B09G4RNT3G)) | $1–2 | $1–2 |
| 18650 cell | $4.99 ([Samsung 25R](https://www.18650batterystore.com/products/samsung-25r-18650)) | $3–4 | $2.50–3.50: EVE cells at $2.50, when in stock |
| Rod, printed body and fins | $2.60: rod $1.10 ([10-pack, $11](https://www.amazon.com/dp/B0FNZQLH1P)) plus about $1.50 of PETG, wire and screws | $2 | $1–1.50, moulded |
| Windscreen, foam | $0.50 ([10-pack, $4.99](https://www.amazon.com/dp/B07X4VKKQ7)) | $0.50 | $0.30–0.50 |
| Assembly and test | not counted: our time | $5: 15 minutes at $20 an hour | $2–3 |
| **Listening dart** | **~$26.50** | **~$25–29** | **~$15–23** |
| **Relay dart** (no mic, no windscreen) | **~$23.50** | **~$23–26** | **~$14–20** |
| **Receiver** (same board, receive only, powered from the phone or tablet) | **~$20** | **~$22** | **~$14** |
| Delivery drone: X500 V2 with Pixhawk 6X, GPS and telemetry radio | [$946](https://pyrodrone.com/products/holybro-x500-v2-pixhawk-development-kit-with-the-pixhawk-6x-standard-m10-gps-915mhz-telemetry-radio) | ~$850, a dealer discount | ~$550: a smaller printed ArduPilot quad with the same electronics ($400–700) |
| Harness for 4 darts: printed plate and rotor, one release servo | ~$5 ([servo 2-pack, $4.99](https://www.amazon.com/dp/B0DFKPVRC2), plus filament) | ~$5 | ~$5 |
| Drone flight batteries, two | ~$140 (est.) | ~$120 | ~$100 |
| Battery charger | ~$60 (est.) | ~$50 | ~$50 |

The small batch costs about the same per dart as the prototype because it pays for assembly. Bulk pricing saves about what the labour adds. The phone or tablet that shows the alarm is the unit's own Android phone, so it is not in the package.

## One unit's package

The net always has two trunks: 10 listening and 10 relay darts. A single trunk would save 5 darts, but one dead relay would silence the whole net, so we don't offer it. The 4 spares are 2 listening and 2 relay darts. They cover a drop error of about ±66 ft, which needs 24 darts ([placement]({{ site.baseurl }}{% link models/line-layout.md %}#what-placement-has-to-get-right)), or replace darts that land badly.

| Part of the package | Prototype | Small batch (est.) | Production (est.) |
|---|---|---|---|
| 24 darts: 12 listening, 12 relay | $600 | $618 | $432 |
| 3 receivers | $60 | $66 | $42 |
| Delivery drone, harness, 2 batteries, charger | $1,151 | $1,025 | $705 |
| **Package: our total cost** | **~$1,810** | **~$1,710** | **~$1,180** |

Darts are costed at the middle of each range. A unit that already flies an ArduPilot quad could take the package without the drone, about $685 in a small batch.

## Keeping it up

Darts aren't recovered. Every net is re-laid when its cells run down, and darts lost to shelling are replaced. A re-lay is 20 darts and 5 sorties; the drone comes home and is reused.

| Cell life | Re-lays a year | Our cost at prototype (~$500 a re-lay) | Our cost in production (~$360 a re-lay, est.) |
|---|---|---|---|
| 2 weeks | 26 | ~$13,000 | ~$9,400 |
| 4 weeks | 13 | ~$6,500 | ~$4,700 |
| 12 weeks | 4 | ~$2,000 | ~$1,400 |

None of these cell lives is measured. Listening darts sleep until they hear something. Relay darts keep their radio listening, so they may run down first. Test T12 decides which row is real, and it is the biggest number in the whole budget.

## Pricing: our cost plus markup

The price is our total cost of the package plus our markup. At three markups:

| What a unit buys | Our cost, small batch | +30% | +50% | +100% |
|---|---|---|---|---|
| **Package:** 24 darts, 3 receivers, drone kit | ~$1,710 | ~$2,220 | **~$2,560** | ~$3,420 |
| Package without the drone | ~$685 | ~$890 | ~$1,030 | ~$1,370 |
| **Re-lay pack:** 20 darts | ~$515 | ~$670 | **~$775** | ~$1,030 |

| What a unit buys | Our cost, production | +30% | +50% | +100% |
|---|---|---|---|---|
| **Package** | ~$1,180 | ~$1,530 | **~$1,770** | ~$2,360 |
| Package without the drone | ~$475 | ~$615 | ~$710 | ~$950 |
| **Re-lay pack:** 20 darts | ~$360 | ~$470 | **~$540** | ~$720 |

**What the market charges, for comparison** (all from [the competitor analysis]({{ site.baseurl }}{% link research/competitors.md %})):

- **DroneAlert:** about $211 per LoRa acoustic module (seller's claims, out of stock).
- **Chuyka 3.0 radio detector:** $584 for defence buyers, $701 with VAT. Its maker calls it the most-requested item units buy with e-points.
- **Zvook NW0:** about $834–950 per sensor, plus 15–18 W of power.

At 50% on small-batch cost, the package is about $855 per position, about one NW0. Each dart stays under $100 at any of these markups.

**A unit's first year** is the package plus 12 re-lays at four-week cells. At 50% on small-batch cost, that is about $11,830, or about $4,880 at twelve-week cells (the package plus 3 re-lays). Quote both numbers, as [the competitor analysis]({{ site.baseurl }}{% link research/competitors.md %}#how-to-position) recommends.

**Sell like Chuyka:** a defence price without VAT with an end-user certificate, a Brave1 Market listing, then e-point eligibility.

Every cost here except the prototype column is an estimate, and every yearly figure rests on an unmeasured battery life.
