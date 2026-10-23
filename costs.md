---
title: Projected costs
nav_primary: 2.2
---

# Projected costs
{: .no_toc }

What one unit's package costs us at three scales, what it costs to keep up, and what it sells for once our markup is added. The package is everything a unit needs to lay and run the two-trunk net on [How it works]({{ site.baseurl }}{% link models/line-layout.md %}): the darts, the receivers, and the drone that lays them, outfitted as the [lay model]({{ site.baseurl }}{% link models/line-layout.md %}#laying-the-net) requires.

**Prototype prices are checked listings.** Small-batch and production prices are our estimates, marked "est.", until a supplier quotes.

1. TOC
{:toc}

## Short answer

- **One unit's package costs us about $2,890 today,** about $2,620 in a small batch and about $1,870 in production. That is 40 darts, 3 receivers, and a delivery drone with its navigation and confirm kit, 6 packs and a 2-channel charger.
- **The lay model raised it.** A lay takes about 35 darts, not 20: 25 planned on real ground, plus about 10 for bad landings and short hops. The drone needs about $420 more kit to lay them under jamming.
- **The price is our cost plus our markup.** At 50%, the package sells for about $3,940 in a small batch, about $1,310 per position.
- **A road costs more than a position.** Guarding 4 mi of supply road takes a package of about $5,900–7,100 and about $44–64k a year at four-week cells, $11–16k a mile ([below](#guarding-a-road)).
- **Re-lays are the real bill.** At four-week cells, a unit re-lays 13 times a year. Battery life (T12) decides whether a year costs us about $5,200 or $33,500 at prototype prices. Landing reliability (T10) is the next lever: at 95% upright instead of 85%, each lay uses 4 fewer darts.

## Per component

| Component | Prototype: retail, hand-built | Small batch: ~500 darts (est.) | Production: 5,000+ darts, custom board (est.) |
|---|---|---|---|
| Processor and radio | XIAO ESP32S3 + Wio-SX1262 kit, [$15.97](https://store.rokland.com/products/seeed-studio-xiao-esp32s3-wio-sx1262-kit-for-meshtastic-lora) | $13–15, bulk kits | $8–12: one board with an ESP32-S3 ($4–10) and an SX1262 ([Hardware]({{ site.baseurl }}{% link research/hardware.md %})) |
| Microphone, INMP441 | $2.50 ([5-pack, $12.51](https://www.amazon.com/dp/B09G4RNT3G)) | $1–2 | $1–2 |
| Tilt sensor: a 3-axis accelerometer | ~$5, a LIS3DH breakout (est.) | ~$2 | ~$1, on the board |
| 18650 cell | $4.99 ([Samsung 25R](https://www.18650batterystore.com/products/samsung-25r-18650)) | $3–4 | $2.50–3.50: EVE cells at $2.50, when in stock |
| Rod, printed body and fins | $2.60: rod $1.10 ([10-pack, $11](https://www.amazon.com/dp/B0FNZQLH1P)) plus about $1.50 of PETG, wire and screws | $2 | $1–1.50, moulded |
| Windscreen, foam | $0.50 ([10-pack, $4.99](https://www.amazon.com/dp/B07X4VKKQ7)) | $0.50 | $0.30–0.50 |
| Assembly and test | not counted: our time | $5: 15 minutes at $20 an hour | $2–3 |
| **Dart** (every dart now has a microphone and a tilt sensor, so any dart can stand in anywhere) | **~$31.50** | **~$27–31** | **~$16–24** |
| **Receiver** (same board, receive only, powered from the phone or tablet) | **~$20** | **~$22** | **~$14** |
| Delivery drone: X500 V2 with Pixhawk 6X, GPS and telemetry radio | [$946](https://pyrodrone.com/products/holybro-x500-v2-pixhawk-development-kit-with-the-pixhawk-6x-standard-m10-gps-915mhz-telemetry-radio) | ~$850, a dealer discount | ~$550: a smaller printed ArduPilot quad with the same electronics ($400–700) |
| Harness for 4 darts: printed plate and rotor, one release servo | ~$5 ([servo 2-pack, $4.99](https://www.amazon.com/dp/B0DFKPVRC2), plus filament) | ~$5 | ~$5 |
| Optical flow and 39 ft lidar in one sensor: terrain following, release height, navigation with GPS jammed | [MicoAir MTF-01P, $41.99](https://pyrodrone.com/collections/all-products/products/micoair-mtf-01p-optical-flow-12m-range-2in1-sensor) | ~$40 | ~$35 |
| Confirm radio: a receive-only dart board on a Pixhawk serial port | ~$20: the dart kit plus an antenna | ~$22 | ~$14 |
| Flight packs, 4S 5,000 mAh, six | ~$420 (~$70 each, est.) | ~$360 | ~$300 |
| Chargers: two channels | ~$120: two [ISDT 608AC at $59.99](https://www.buddyrc.com/products/isdt-608ac-ac-battgo-smart-battery-charger) | ~$100 | ~$100 |
| Insulated pack bag | ~$20 (est.) | ~$20 | ~$20 |

The small batch costs about the same per dart as the prototype because it pays for assembly. Bulk pricing saves about what the labour adds. The phone or tablet that shows the alarm is the unit's own Android phone, so it is not in the package.

## One unit's package

The lay model plans **25 darts** on its example sector: 13 front darts and 6 relays a trunk. That is 5 more than open ground needs, because the ends now reach past the 45° lines and the hops that cross a windbreak are shorter. Laying them takes **about 35 darts, and 40 in 9 lays out of 10**, because the drone confirms every link and re-drops darts that land badly or out of reach. The package carries 40, including the root dart placed by hand beside the receiver.

| Part of the package | Prototype | Small batch (est.) | Production (est.) |
|---|---|---|---|
| 40 darts | $1,260 | $1,160 | $800 |
| 3 receivers | $60 | $66 | $42 |
| Delivery drone, harness, navigation and confirm kit, 6 packs, 2 chargers, pack bag | $1,573 | $1,397 | $1,024 |
| **Package: our total cost** | **~$2,890** | **~$2,620** | **~$1,870** |

Darts are costed at the middle of each range. **What the lay model added to the drone:** the flow-and-lidar sensor ($42), the confirm radio ($20), 4 more packs and a second charger ($340) and a pack bag ($20), about $420 in all. A unit that already flies an ArduPilot quad can take the package without the drone and its packs: darts, receivers, harness, flow sensor and confirm radio, about $1,290 in a small batch.

**Not yet in the total: forward roots on fibre.** The [jamming model]({{ site.baseurl }}{% link models/line-layout.md %}#jamming) says the unit's own jammers deafen receivers at the positions. The proposed fix is a root dart about 1,000 ft forward at the foot of each trunk, each sending alerts home one way down about 0.2 mi of FPV fibre (about $10 at $20–35 a km), with a wire between the positions: about $60–100 a unit (est.), untested.

## Keeping it up

Darts aren't recovered. Every net is re-laid when its cells run down, and darts lost to shelling are replaced. **A re-lay is about 35 darts and 9 sorties.** The drone comes home, except about 0.2 times a lay, at the model's guess of 2% lost per sortie.

| Cell life | Re-lays a year | Our cost at prototype (~$1,290 a re-lay) | Our cost in production (~$810 a re-lay, est.) |
|---|---|---|---|
| 2 weeks | 26 | ~$33,500 | ~$21,100 |
| 4 weeks | 13 | ~$16,800 | ~$10,500 |
| 12 weeks | 4 | ~$5,200 | ~$3,200 |

A re-lay's cost is about 35 darts, plus 0.2 of a drone (about $190 at prototype prices, $110 in production), plus about $3 of pack wear. **Repairs between re-lays** cost one dart each, about $27–31, plus about $0.30 of pack wear a sortie; up to 4 go on one sortie ([When it breaks]({{ site.baseurl }}{% link models/line-layout.md %}#when-it-breaks)).

None of these cell lives is measured. Listening darts sleep until they hear something; relay darts keep their radio listening, so they may run down first. Test T12 decides which row is real, and it is the biggest number in the whole budget. **T10 is next:** each dart that lands upright instead of tilted saves one re-drop, and at 95% upright a lay uses about 31 darts instead of 35, about $1,500 a year at small-batch prices and four-week cells.

## Guarding a road

From the [route model]({{ site.baseurl }}{% link models/route-guard.md %}), run on two invented 4 mi roads. Small-batch costs to us (est.). A **post** is about $45: the dart's board, 4 cells, a 2 ft whip and a stake. The drone is the position package's, with 6 more packs and 2 more charger channels so a fence goes in in a day.

| | Road along the front | Road toward the front |
|---|---|---|
| **Package:** 25 posts, 90 or 130 air-dropped darts, 14 receivers (12 vehicles, 2 checkpoints), the outfitted drone with 12 packs and 4 charger channels | **~$5,900** | **~$7,060** |
| Cable and a hooded lamp on every post (proposed, [why]({{ site.baseurl }}{% link models/route-guard.md %}#jamming-and-a-wire-along-the-road)) | ~$800 | ~$800 |
| One re-lay of the fence: about 77 or 119 darts, 0.5–0.7 of a lost drone, pack wear | ~$2,630 | ~$4,020 |
| A year at two-week cells | ~$81,700 | ~$119,800 |
| **A year at four-week cells:** 13 re-lays, posts every 16 weeks, repairs between re-lays | **~$44,400** | **~$64,500** |
| A year at twelve-week cells | ~$19,500 | ~$27,600 |
| **A mile a year at four-week cells** | **~$11,100** | **~$16,000** |
| Package at +50% | ~$8,850 | ~$10,590 |

- **The fence is 75–80% of the bill.** Posts carry 4 cells and should last about 4 times as long as a dart (T12).
- **The drone is the hidden cost again:** at 2% lost per sortie, a re-lay loses about $400–570 of drone.
- **Posts only,** with no fence: about $1,400 for 25 posts and 14 receivers, and about $6,500 a year. It hears drones land by the road but gives only 4–9 s of warning of a strike.
- **Zvook's NW0** is pitched for roads at 1,300–2,000 ft spacing, which is about 11–17 sensors on 4 mi, about $9–16k before power, with no fence ([competitors]({{ site.baseurl }}{% link research/competitors.md %})).

## Pricing: our cost plus markup

The price is our total cost of the package plus our markup. At three markups:

| What a unit buys | Our cost, small batch | +30% | +50% | +100% |
|---|---|---|---|---|
| **Package:** 40 darts, 3 receivers, outfitted drone | ~$2,620 | ~$3,410 | **~$3,940** | ~$5,250 |
| Package without the drone and packs | ~$1,290 | ~$1,680 | ~$1,940 | ~$2,590 |
| **Re-lay pack:** 35 darts | ~$1,015 | ~$1,320 | **~$1,520** | ~$2,030 |

| What a unit buys | Our cost, production | +30% | +50% | +100% |
|---|---|---|---|---|
| **Package** | ~$1,870 | ~$2,430 | **~$2,800** | ~$3,730 |
| Package without the drone and packs | ~$900 | ~$1,170 | ~$1,340 | ~$1,790 |
| **Re-lay pack:** 35 darts | ~$700 | ~$910 | **~$1,050** | ~$1,400 |

**What the market charges, for comparison** (all from [the competitor analysis]({{ site.baseurl }}{% link research/competitors.md %})):

- **DroneAlert:** about $211 per LoRa acoustic module (seller's claims, out of stock).
- **Chuyka 3.0 radio detector:** $584 for defence buyers, $701 with VAT. Its maker calls it the most-requested item units buy with e-points.
- **Zvook NW0:** about $834–950 per sensor, plus 15–18 W of power.

At 50% on small-batch cost, the package is about $1,310 per position, a little more than one NW0. A dart sells for about $38–58 in a small batch at these markups.

**A unit's first year** is the package plus 12 re-lays at four-week cells, and about 2–3 replacement drones. At 50% on small-batch cost, that is about $25,500, or about $9,500 at twelve-week cells (the package plus 3 re-lays and about one replacement drone). Quote both numbers, as [the competitor analysis]({{ site.baseurl }}{% link research/competitors.md %}#how-to-position) recommends.

**Sell like Chuyka:** a defence price without VAT with an end-user certificate, a Brave1 Market listing, then e-point eligibility.

Every cost here except the prototype column is an estimate, and every yearly figure rests on an unmeasured battery life, an assumed landing rate and a guessed drone-loss rate.
