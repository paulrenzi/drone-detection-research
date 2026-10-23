---
title: Projected costs
nav_primary: 2.2
---

# Projected costs
{: .no_toc }

What one unit's package costs us at three scales, what it costs to keep up, and what it sells for once our markup is added. The package is everything a unit needs to lay and run the net on [How it works]({{ site.baseurl }}{% link models/line-layout.md %}), a front row of darts with two FPV fibres home: the darts, the tip darts, the base box and its wire, and the drone that lays them, outfitted as the [lay model]({{ site.baseurl }}{% link models/line-layout.md %}#laying-the-net) requires.

**Prototype prices are checked listings.** Small-batch and production prices are our estimates, marked "est.", until a supplier quotes.

1. TOC
{:toc}

## Short answer

- **One unit's package costs us about $2,850 today,** about $2,580 in a small batch and about $1,860 in production. That is 22 darts, 4 tip darts with their fibre, a base box wired to the positions, and a delivery drone with its navigation and confirm kit, 6 packs and a 2-channel charger.
- **Fibre made it smaller.** A lay takes about 22 darts, against about 35 on radio trunks: 16 planned on real ground, plus about 6 for bad landings, short hops and broken fibres. The drone is now over half the package.
- **The price is our cost plus our markup.** At 50%, the package sells for about $3,870 in a small batch, about $1,290 per position.
- **A road costs more than a position.** Guarding 4 mi of supply road takes a package of about $5,700–6,800 and about $37–56k a year at four-week cells, $9–14k a mile ([below](#guarding-a-road)).
- **Re-lays are the real bill.** At four-week cells, a unit re-lays 13 times a year. Battery life (T12) decides whether a year costs us about $4,100 or $26,600 at prototype prices. Landing reliability (T10) is the next lever: at 95% upright instead of 85%, each lay uses about 2 fewer darts.

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
| Tip dart's extra: about 1.2 mi of FPV fibre on a spool, a small laser and its driver (est.) | ~$70: fibre about $40–70 at [$32–56 a mile](https://dronexl.co/2026/05/11/ukraine-fiber-optic-spool-price-ai-data-center-demand/), spool and laser ~$10 | ~$65 | ~$50 |
| **Tip dart** (a dart plus the above, about 10 oz) | **~$100** | **~$94** | **~$70** |
| **Base box** (a dart's board receiving only, two light detectors, box and two fibre connectors, est.) | ~$70 | ~$60 | ~$40 |
| **Wire to the positions** (about 2,300 ft of twisted pair, a serial line chip at each end, a USB adapter for each phone or tablet, est.) | ~$110 | ~$110 | ~$80 |
| Delivery drone: X500 V2 with Pixhawk 6X, GPS and telemetry radio | [$946](https://pyrodrone.com/products/holybro-x500-v2-pixhawk-development-kit-with-the-pixhawk-6x-standard-m10-gps-915mhz-telemetry-radio) | ~$850, a dealer discount | ~$550: a smaller printed ArduPilot quad with the same electronics ($400–700) |
| Harness for 4 darts: printed plate and rotor, one release servo | ~$5 ([servo 2-pack, $4.99](https://www.amazon.com/dp/B0DFKPVRC2), plus filament) | ~$5 | ~$5 |
| Optical flow and 39 ft lidar in one sensor: terrain following, release height, navigation with GPS jammed | [MicoAir MTF-01P, $41.99](https://pyrodrone.com/collections/all-products/products/micoair-mtf-01p-optical-flow-12m-range-2in1-sensor) | ~$40 | ~$35 |
| Confirm radio: a receive-only dart board on a Pixhawk serial port | ~$20: the dart kit plus an antenna | ~$22 | ~$14 |
| Flight packs, 4S 5,000 mAh, six | ~$420 (~$70 each, est.) | ~$360 | ~$300 |
| Chargers: two channels | ~$120: two [ISDT 608AC at $59.99](https://www.buddyrc.com/products/isdt-608ac-ac-battgo-smart-battery-charger) | ~$100 | ~$100 |
| Insulated pack bag | ~$20 (est.) | ~$20 | ~$20 |

The small batch costs about the same per dart as the prototype because it pays for assembly. Bulk pricing saves about what the labour adds. The phone or tablet that shows the alarm is the unit's own Android phone, so it is not in the package. The tip dart, the base box and the wire are a design, not yet built ([the fibres and the base box]({{ site.baseurl }}{% link models/line-layout.md %}#the-fibres-and-the-base-box)); their prices are estimates in every column.

## One unit's package

The lay model plans **16 darts** on its example sector, all in the front row, 2 of them tips. That is 1 more than open ground needs, because a hop that crosses a windbreak is shorter. Laying them takes **about 22 darts, and 26 in 9 lays out of 10**, because the drone confirms every link and re-drops darts that land badly or out of reach, and a tip whose fibre breaks is laid again. The package carries 22 darts and 4 tip darts.

| Part of the package | Prototype | Small batch (est.) | Production (est.) |
|---|---|---|---|
| 22 darts | $693 | $638 | $440 |
| 4 tip darts | $406 | $376 | $280 |
| Base box and the wire to the positions | $180 | $170 | $120 |
| Delivery drone, harness, navigation and confirm kit, 6 packs, 2 chargers, pack bag | $1,573 | $1,397 | $1,024 |
| **Package: our total cost** | **~$2,850** | **~$2,580** | **~$1,860** |

Darts are costed at the middle of each range. **What the lay model added to the drone:** the flow-and-lidar sensor ($42), the confirm radio ($20), 4 more packs and a second charger ($340) and a pack bag ($20), about $420 in all. A unit that already flies an ArduPilot quad can take the package without the drone and its packs: darts, tip darts, base box and wire, harness, flow sensor and confirm radio, about $1,250 in a small batch.

**What fibre changed:** the last plan, radio trunks, carried 40 darts and 3 receivers for about $2,620 in a small batch, and still needed about $60–100 of forward roots on fibre to survive the unit's own jammers. Fibre to the front row drops 12 relay darts and the receivers, adds 4 tip darts, a base box and a wire, and needs nothing more for our own jammers.

## Keeping it up

Darts aren't recovered. Every net is re-laid when its cells run down, and darts lost to shelling are replaced. **A re-lay is about 22 darts and 7 sorties:** about 20 darts and 2.6 tip darts on average. The drone comes home, except about 0.15 times a lay, at the model's guess of 2% lost per sortie. The base box and the wire stay.

| Cell life | Re-lays a year | Our cost at prototype (~$1,020 a re-lay) | Our cost in production (~$660 a re-lay, est.) |
|---|---|---|---|
| 2 weeks | 26 | ~$26,600 | ~$17,100 |
| 4 weeks | 13 | ~$13,300 | ~$8,500 |
| 12 weeks | 4 | ~$4,100 | ~$2,600 |

A re-lay's cost is about 22 darts, plus 0.15 of a drone (about $140 at prototype prices, $80 in production), plus about $2 of pack wear. **Repairs between re-lays** cost one dart each, about $27–31, or one tip dart, about $90–100, plus about $0.30 of pack wear a sortie; up to 4 darts go on one sortie ([When it breaks]({{ site.baseurl }}{% link models/line-layout.md %}#when-it-breaks)).

None of these cell lives is measured. Every dart now keeps its radio listening to relay its neighbours, and tip darts also flash a laser heartbeat every 10 s, so tips may run down first. Test T12 decides which row is real, and it is the biggest number in the whole budget. **T10 is next:** each dart that lands upright instead of tilted saves one re-drop, and at 95% upright a lay uses about 20 darts instead of 22, about $900 a year at small-batch prices and four-week cells.

## Guarding a road

From the [route model]({{ site.baseurl }}{% link models/route-guard.md %}), run on two invented 4 mi roads. Small-batch costs to us (est.). A **post** is about $45: the dart's board, 4 cells, a 2 ft whip and a stake. The drone is the position package's, with 6 more packs and 2 more charger channels so a fence goes in in a day. The fence comes home on FPV fibre: every 2 mi a **tip dart** (about $94) sends its alerts down a fibre to a post, which carries a **fibre end** (a light detector, connector and box, about $20, est.).

| | Road along the front | Road toward the front |
|---|---|---|
| **Package:** 25 posts, 50 or 80 air-dropped darts, 9 or 11 tip darts, 5 or 7 fibre ends, 14 receivers (12 vehicles, 2 checkpoints), the outfitted drone with 12 packs and 4 charger channels | **~$5,690** | **~$6,780** |
| Cable and a hooded lamp on every post (proposed, [why]({{ site.baseurl }}{% link models/route-guard.md %}#jamming-and-a-wire-along-the-road)) | ~$800 | ~$800 |
| One re-lay of the fence: about 46 or 76 darts (6 or 9 of them tip darts), 0.3–0.6 of a lost drone, pack wear | ~$2,000 | ~$3,270 |
| A year at two-week cells | ~$66,400 | ~$101,900 |
| **A year at four-week cells:** 13 re-lays, posts every 16 weeks, repairs between re-lays and cut fibres | **~$37,300** | **~$56,300** |
| A year at twelve-week cells | ~$17,900 | ~$25,900 |
| **A mile a year at four-week cells** | **~$9,300** | **~$14,000** |
| Package at +50% | ~$8,540 | ~$10,180 |

- **The fence is 70–76% of the bill.** Posts carry 4 cells and should last about 4 times as long as a dart (T12).
- **Fibre made it cheaper.** On radio trunks the package was about $5,900–7,060 and a year at four-week cells about $44,400–64,500. Each fibre replaces about 5 relay darts.
- **Cut fibres are a new running cost:** at a guessed 1% of days each, about 18–26 new tip darts a year, about $2,000–2,800.
- **The drone is the hidden cost again:** at 2% lost per sortie, a re-lay loses about $270–500 of drone.
- **Posts only,** with no fence: about $1,400 for 25 posts and 14 receivers, and about $6,500 a year. It hears drones land by the road but gives only 4–9 s of warning of a strike.
- **Zvook's NW0** is pitched for roads at 1,300–2,000 ft spacing, which is about 11–17 sensors on 4 mi, about $9–16k before power, with no fence ([competitors]({{ site.baseurl }}{% link research/competitors.md %})).

## Pricing: our cost plus markup

The price is our total cost of the package plus our markup. At three markups:

| What a unit buys | Our cost, small batch | +30% | +50% | +100% |
|---|---|---|---|---|
| **Package:** 22 darts, 4 tip darts, base box and wire, outfitted drone | ~$2,580 | ~$3,360 | **~$3,870** | ~$5,160 |
| Package without the drone and packs | ~$1,250 | ~$1,630 | ~$1,880 | ~$2,500 |
| **Re-lay pack:** 20 darts and 3 tip darts | ~$860 | ~$1,120 | **~$1,290** | ~$1,720 |

| What a unit buys | Our cost, production | +30% | +50% | +100% |
|---|---|---|---|---|
| **Package** | ~$1,860 | ~$2,420 | **~$2,800** | ~$3,730 |
| Package without the drone and packs | ~$890 | ~$1,160 | ~$1,340 | ~$1,790 |
| **Re-lay pack:** 20 darts and 3 tip darts | ~$610 | ~$790 | **~$920** | ~$1,220 |

**What the market charges, for comparison** (all from [the competitor analysis]({{ site.baseurl }}{% link research/competitors.md %})):

- **DroneAlert:** about $211 per LoRa acoustic module (seller's claims, out of stock).
- **Chuyka 3.0 radio detector:** $584 for defence buyers, $701 with VAT. Its maker calls it the most-requested item units buy with e-points.
- **Zvook NW0:** about $834–950 per sensor, plus 15–18 W of power.

At 50% on small-batch cost, the package is about $1,290 per position, a little more than one NW0. A dart sells for about $38–58 in a small batch at these markups, and a tip dart for about $120–190.

**A unit's first year** is the package plus 12 re-lays at four-week cells, and about 2 replacement drones. At 50% on small-batch cost, that is about $21,900, or about $8,500 at twelve-week cells (the package plus 3 re-lays and about half a replacement drone). Quote both numbers, as [the competitor analysis]({{ site.baseurl }}{% link research/competitors.md %}#how-to-position) recommends.

**Sell like Chuyka:** a defence price without VAT with an end-user certificate, a Brave1 Market listing, then e-point eligibility.

Every cost here except the prototype column is an estimate, and every yearly figure rests on an unmeasured battery life, an assumed landing rate and a guessed drone-loss rate.
