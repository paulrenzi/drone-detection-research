# XIAO listener and X500 release harness: first-print revision

## Changes from the Heltec version

The incorrect Heltec/OLED package has been replaced throughout the current assemblies, renders and web models by the owned Seeed XIAO ESP32S3 + Wio-SX1262 kit. The original brief and downloaded legacy sources are retained as history. Old model outputs have been removed.

| Model estimate | Old Heltec package | New XIAO package |
| --- | --- | --- |
| Populated processor/radio boards, g | 9.00 | 4.00 |
| Printed pod shell/lid/cap, g | 29.79 | 25.60 |
| Dart, g | 158.16 | 147.93 |
| Harness, g | 183.48 | 183.48 |
| Four darts + harness, g | 816.13 | 775.20 |
| Hanger from tip, mm | 265.73 | 254.44 |

Per the firmware brief, the listener reports alive by radio once per minute. That heartbeat replaces a visual status indication. Native OEM CAD may retain inactive onboard component bodies; no added LED, display or battery-divider circuit is fitted. A smaller cell could reduce nose mass, but its runtime and impact retention need testing; the specified18650 remains in the real listener models.

The electronics tray is now 46 x32 mm rather than 82 x36 mm, with a narrow socket neck that preserves the 500 mm rod and raises the sound port to 500 mm above soil (previously470 mm). There is no display window, added status LED or voltage-divider part. A removable end cap exposes USB-C and pin access to both BOOT/RESET buttons. Three lid screws replace four; the kit LoRa FPC sits on a light integral top backer. Five mic wires and direct underside BAT connections replace the old board wiring. A stake adapter, separate 18650 stake cradle and an inert ballasted dummy are included.

**Nothing has been printed, drop-tested or flown.** These are nominal geometry and mass estimates, not measured hardware qualification. The actual kit stack spacing, microphone breakout, antenna dimensions, printed fits and filament properties still require measurement. No self-righting, soil penetration, waterproofing, acoustic or radio range result is claimed.

## Files and reproduction

[REVIEW.html](REVIEW.html) indexes all current renders. `out/` contains twelve printed STEP/STL pairs, current bought-part CAD, carried/mid-release/stood aircraft assemblies, a stood dart, stake and dummy assemblies, mass/check reports, print manifest and `print-kit.zip`. All STLs are already placed on Z0 in the intended Vyper print orientation; STEP files retain assembly datums. Eighteen functional printed pieces make four real darts and one harness; the coupon, stake and dummy parts are optional alternatives/tools.

```powershell
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/fetch_sources.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/fetch_xiao.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/build.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/validate_exports.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/web_export.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/document.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/record_visual_review.py --reviewed
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/validate_package.py
& 'C:\Users\paulm\.venvs\cad\Scripts\python.exe' cad/gpt61/package.py
```

Inspect every newly generated PNG before running `record_visual_review.py --reviewed`; that command records an explicit inspection attestation and cannot perform visual review itself. All scripts write only in this package. `build.py --render-only`, `--exports-only` and `--verify-only` reuse its generated cache. Rebuild normally after any dimension/mass/source change. `sources/manifest.json` and `sources/xiao-manifest.json` retain source URLs, sizes and hashes.

## Primary source register

- **S1: [Holybro X500 V2 official frame CAD and assembly](https://holybro.com/collections/multicopter-kit/products/px4-development-kit-x500-v2).** Unscaled OEM STEP: centre plates, arms, motors, skids, payload rails and clamps; duplicate solids removed, original indices retained. Rail spacing60 mm, CAD OD9.4 mm; design clearance uses catalog10 mm.
- **S2: [Holybro motor and prop drawing](https://cdn.shopify.com/s/files/1/0604/5905/7341/files/X500MotorSpec.png?v=1678791632).** Conservative260 mm prop swept diameter; fitted plane and 4 mm slab thickness remain MEASURE. Translucent swept discs are clearance volumes, not propeller blades.
- **S3: [TowerPro SG90 drawing](https://towerpro.com.tw/product/sg90-7/).** 22.7 x12.2 x27 mm case,32.3 mm tab span,9 g catalog mass and 1.8 kg.cm stall torque. Horn, spline, mounting holes and exact batch remain MEASURE.
- **S4: [Seeed kit wiki: both OEM STEP archives, schematic and XIAO DXF](https://wiki.seeedstudio.com/xiao_esp32s3_&_wio_SX1262_kit_for_meshtastic/).** Native XIAO ESP32S3 STEP and Wio-SX1262-for-XIAO STEP used without scaling. B2B kit connection, USB flashing and underside battery-pad connection are documented here. sources/xiao-manifest.json records exact download URLs and SHA256.
- **S4a: [Seeed XIAO ESP32S3 dimensions and pin map](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/).** 21 x17.8 mm PCB nominal; D3=GPIO4, D4=GPIO5, D5=GPIO6. Native STEP includes USB-C, BOOT/RESET and WiFi U.FL. Archive top/bottom images identify BAT pads and castellated pins.
- **S4b: [Seeed bare kit SKU102010611 and included FPC antenna](https://www.seeedstudio.com/Wio-SX1262-with-XIAO-ESP32S3-p-5982.html).** Manufacturer identifies separate WiFi and LoRa antennas and included FPC. No dimensioned antenna drawing was found. Both antenna envelopes, masses and coax lengths are MEASURE. The kit FPC is not the optional195 mm SMA antenna.
- **S4c: [Wio-SX1262 radio-module datasheet](https://files.seeedstudio.com/products/SenseCAP/Wio_SX1262/Wio-SX1262_Module_Datasheet.pdf).** Bare radio module11.6 x11 x2.95 mm is NOT the complete extension board. Extension outline comes from its kit-specific OEM STEP, not this module envelope.
- **S4d: [Rokland XIAO ESP32S3 + Wio-SX1262 kit](https://store.rokland.com/products/seeed-studio-xiao-esp32s3-wio-sx1262-kit-for-meshtastic-lora).** Retailer identifies SKU102010611 and links the same kit-specific Seeed Wio STEP and schematic. It supplies no additional antenna dimensional drawing; confirm the actual shipped antenna batch.
- **S5: [Samsung INR18650-25R manufacturer specification mirror](https://files.dcpower.eu/datasheets/samsung/INR18650-25R-datasheet.pdf).** 18.33 +/-0.07 mm diameter,64.85 +/-0.15 mm length,45 g maximum. Keep flat-top cell and existing cradle. Terminal/insulator details and actual mass MEASURE.
- **S6: [TDK INMP441 outline](https://product.tdk.com/en/search/sw_piezo/mic/mems-mic/info?part_no=INMP441).** Bare IC4.72 x3.76 x1 mm, bottom port0.25 mm. Generic breakout14 x16 x1 mm and its hole/pads/mass remain MEASURE.
- **S6a: [TDK AN1124 microphone sealing guidance](https://invensense.tdk.com/wp-content/uploads/2015/02/Recommendations-for-Sealing-InvenSense-Bottom-Port.pdf).** Prototype soft film and 0.8 mm acoustic cavity are design assumptions; acoustic transfer and water resistance untested.
- **S7: [HellermannTyton T18R UV-stable tie](https://www.hellermanntyton.com.br/produtos/abracadeiras-com-serrilhado-interno/t18r/111-01711).** 100 x2.5 x1 mm strap,80 N catalog minimum loop strength; installed closed loops reconstructed.
- **S8: [3M5490 PTFE film tape](https://multimedia.3m.com/mws/media/2522949O/3m-ptfe-extruded-film-tape-5490.pdf).** 0.09 mm total thickness. Friction coefficient0.12 is an engineering assumption, not a manufacturer specification.
- **S9: [Ruthex RX-M2x4 insert CAD](https://www.ruthex.de/products/ruthex-gewindeeinsatz-m2-70-stuck-rx-m2x4-messing-gewindebuchsen).** Actual knurled manufacturer STEP.3.6 mm OD,4 mm long;3.2 mm pilot and 5.2 mm pocket are design fit choices.
- **S10: [M2 hex nut dimensions](https://www.accu.co.uk/hexagon-nuts/655596-HPN-M2-PCN).** DIN934 envelope4 mm across flats x1.6 mm height; metal nuts modelled. Dummy traps have side-loading slots.

Native CAD inspection reports are `sources/xiao-cad-inspection.json` and `sources/wio-cad-inspection.json`. XIAO PCB envelope in its original model is 20.955 x17.780 mm; USB projection makes the full length22.482 mm. Wio extension PCB envelope is 21.440 x17.780 x1.6 mm, including its outline tab; its supplied model spans7.3 mm vertically including the underside connector. Neither CAD has been scaled to make the nominal 21 mm dimension fit. The source XIAO model lacks a resolved mating B2B connector, so its envelope is reconstructed and flagged MEASURE.

## Pod, wiring and service

The46 x32 mm rounded tray has1.6 mm walls and floor,17 mm seam height and 2 mm lid. Its narrow13.6 mm socket neck extends fromX480 to 539; the rod enters20 mm and stops atX500. The hollow riser carries the two power wires from the rod to the shorter electronics tray, which begins atX536. This axial neck is needed because a500 mm rod buried70 mm ends only 430 mm above soil, while the mic must be at 500 mm. Reducing tray length without this offset would lower the microphone.

The XIAO rests on four underside edge supports. The Wio extension plugs into the kit B2B connector above it; the model places Wio PCB bottom atZ10.5, with an11.55 mm overall stack envelope. The7.5 mm mating offset is MEASURE; verify it before printing. Lid fingers compress four 1 mm foam pads against Wio PCB edges, away from the RF can. No soldered tall pin headers are fitted. Locating fences have about 0.3 mm clearance outside the XIAO edges.

The mic board stands along the negative Y wall, with its bottom port atX570,Z8. Its actual port is 500 mm above the body soil stop. A4 mm cavity,0.8 mm annular silicone spacer and 0.05 mm soft prototype film connect it to the side opening under an integral45degree rain hood. Breakout dimensions and pad/hole placement are MEASURE. Do not assume the waterproof/acoustic performance of this untested membrane.

| INMP441 connection | XIAO pad | GPIO |
| --- | --- | --- |
| SCK / BCLK | D3 | 4 |
| WS / LRCLK | D4 | 5 |
| SD / data | D5 | 6 |
| VDD | 3V3 | Supply |
| GND and L/R select | GND | Ground |

Five short insulated wires are modelled; the microphone L/R select is a local solder bridge to ground, not a sixth long wire. Wire dress and exact solder points remain MEASURE. The long cell pair runs in the original body gutter and along the rod, enters the socket neck through relieved ducts and terminates at the XIAO underside BAT+/BAT- pads. Sourced bottom-view images identify these pads; their small copper envelopes/centres are reconstructed. The XIAO charger does not provide a mechanical battery connector. Use factory-welded insulated cell leads, never solder directly to the can. Verify the actual cell protection arrangement; charger presence alone does not establish pack protection.

The kit LoRa FPC has an explicitly unmeasured100 x10 x0.3 mm nominal envelope; its separate U.FL coax exits a2.2 mm gland above the microphone. A1.2 mm PETG backer extends from the lid, with small tape/tie slots; its outer face is coplanar with the lid so both print flat together. The socket neck floor is also coplanar with the tray base; its teardrop duct has at least1.7 mm roof thickness. Strain-relieve the coax before it reaches U.FL, and seal the gland with removable neutral-cure silicone. The separate WiFi/BLE FPC is on the positive Y wall. Do not replace these with the optional195 mm SMA antenna without recomputing mass, balance and clearance. The default overall dart length is 686 mm; the larger figure than the old644 mm package comes from the deliberately provisional FPC envelope.

A19 x14 mm end opening gives access to USB-C and a0.7 mm pin path to either button with the printed cap removed. The cap has0.3 mm skirt clearance and a1.2 mm overlapping flange. Seal its perimeter with a removable thin silicone bead or weather tape; it is a prototype service closure, not a tested IP seal. The full pod lid need not be removed to flash. Cable overmould envelope11 x6.2 mm is MEASURE. The lid perimeter has a1.5 x0.9 mm gland for1.2 mm cord (25% nominal compression); three RX-M2x4 inserts and M2x6 screws clamp it. RTV, solder and service tape are not resolved as exact solids or weighed consumables.

## Body, balance and harness

The body retains the specified6 x500 mm fibreglass spine,70 mm nose/soil stop, flat-top18650 open snap cradle, axial sleeve, integral post and wire gutters. Three short5.95 mm nominal press lands sit in a6.35 mm relieved teardrop bore; the coupon determines the actual fit. Four1.2 mm thick,18 mm long cantilevers retain the cell through a16.8 mm throat with lead-in ramps. Axial end walls take impact load rather than the flexible latch tips. The rod tip is a12 mm cone with a0.6 mm blunt point for the nominal CAD envelope.

The mass solver moves the post and its sleeve until its X/Y axis agrees with the recomputed dart centre of mass. The nominal CG is **(254.434, 7.087, 9.026) mm**; the hanger is **X254.439, Y7.086 mm** from the tip/rod datum. Residual X error is-0.00471 mm. This numerical residual is not a real assembly tolerance; weighed stock and printed mass control actual balance.

The smaller head lowers the modelled load. The existing harness geometry is retained after rechecking all four moved darts:83 mm deck radius,3.2 mm deck,48..51 mm bearing ridge,64.9 mm rotor radius,3.2 mm rotor web and 20degree release gaps. Slots are20.4 x15.4 mm for13 mm heads and 5 mm necks. The pilot has0.25 mm radial clearance. Payload rail centres are60 mm apart; saddles use 10.6 mm seats and four T18R ties. Tall towers are explicitly hollow CAD geometry, not a density multiplier.

The load path remains head -> rotor rim -> PTFE-covered bearing ridge -> plate -> saddles/rails. The SG90 stock horn drives two 18 mm-spaced M2 studs with axial slip; a keeper washer has0.4 mm running gap and does not clamp the rotor onto the servo shaft. The model checks the case, horn, nuts, pilot and rotor throughout the release sequence. Dart1 releases at 16degrees, dart3 at 32, dart2 at 48 and dart4 at 64. Servo travel, torque under friction, creep and shock remain physical qualification items.

## Masses and print settings

**Recommended prototype infill is 100% for every printed part, including the plate.** This is intentional: load-carrying skins/ribs and small fit features should be solid for the first test; large lightening pockets and tower cores are already removed in CAD. The plate estimate is its actual model volume times1.27 g/cm3 PETG, with no hidden35% or other infill multiplier. A lighter slicer profile would require a fresh sliced/printed mass and structural assessment. No slicer has been run and no part has been weighed; actual extrusion width, perimeter overlap, holes and filament density will change the result.

| Printed design | Mass g at 100% | CAD volume cm3 |
| --- | --- | --- |
| body | 40.983 | 32.270 |
| pod_shell | 18.980 | 14.945 |
| pod_lid | 5.707 | 4.494 |
| usb_cap | 0.916 | 0.721 |
| plate | 131.678 | 103.683 |
| rotor | 38.622 | 30.411 |
| fit_coupon | 4.492 | 3.537 |
| stake_adapter | 13.380 | 10.535 |
| stake_cell_holder | 30.546 | 24.052 |
| dummy_body | 50.427 | 39.707 |
| dummy_lid | 4.075 | 3.209 |
| dummy_head_insert | 1.872 | 1.474 |

| Assembly | Nominal g |
| --- | --- |
| One real dart | 147.931 |
| Harness including servo/hardware/ties | 183.479 |
| Four real darts + harness | 775.202 |
| Inert dummy with ballast | 147.931 |

Complete stake installation, including the full 1219.2 mm nominal 10 mm stake and 18650: **308.892 g**. Stake density and all small-stock masses are unmeasured; this total is separate from flight payload.

Full per-component grams, volumes, assumptions and XYZ centroids are in [out/mass_properties.csv](out/mass_properties.csv) and [out/mass_properties.json](out/mass_properties.json), including auxiliary printed and dummy parts. Board masses2.2 g XIAO/1.8 g Wio,1 g mic,0.8 g LoRa antenna and 0.35 g WiFi antenna are unmeasured estimates; the 45 g cell figure is a datasheet maximum. Hardware uses nominal material density and shape centroids. Solder, final adhesive, tape and small protection/connector additions require a weighed allowance before qualification.

Four-dart kit bought hardware:

| Item | Quantity |
| --- | --- |
| 6 x500 mm fibreglass rods | 4 |
| XIAO ESP32S3 + Wio-SX1262 kits, with both FPC antennas | 4 |
| INMP441 breakouts | 4 |
| Flat-top18650 cells with factory-welded insulated leads | 4 |
| SG90 positional servo and supplied double horn | 1 |
| RX-M2x4 heat-set inserts | 12 |
| M2x6 pod screws + servo tab screws | 12 +2 |
| M2 drive studs, nominal 10 mm; nuts for drive and servo | 2 studs;6 nuts |
| Measured-thread keeper screw, spacer and washer | 1 each |
| T18R ties: body/rod + rails | 12 +4 |
| 1.2 mm cord, mic film/cavity seals and foam pads | 4 pod sets |
| PTFE bearing film | 1 annular strip |
| Power pair and 5 short mic wires | 4 wired sets |

Stake option adds one 40 mm fibreglass offcut and five installation ties; it reuses one complete pod and one cell. Dummy option adds two M2x8 screws, two M2 nuts and the four weighed ballast portions. `out/kits.json` lists printed quantities separately for each option.

Use the Anycubic Vyper245 x245 x260 mm, dry PETG,0.4 mm nozzle,0.20 mm layers, four perimeters, six top/bottom layers and 100% infill. Start within the filament manufacturer temperature range (typically235C nozzle/80C bed), then tune adhesion and fit. Use slow external walls and first layer; do not let supports lock snap reliefs or fill teardrop ducts. All supplied orientations fit the bed.

| Part | Kit/optional qty | STL bounds mm | Orientation | Supports |
| --- | --- | --- | --- | --- |
| body | 4 | 195.4 x 37.3 x 53.2 | Flat sole down; post and snaps up | Local only: hanger flange and four snap beams. Clear the flexure reliefs. |
| pod_shell | 4 | 102.0 x 37.4 x 17.8 | Tray floor/neck flat down, opening up | Local only: rain hood, socket lip and mic guide ledges. Block teardrop ducts. |
| pod_lid | 4 | 150.0 x 32.0 x 5.9 | Outside face and FPC backer together on bed | None. Backer top is coplanar with lid outside face. |
| usb_cap | 4 | 16.4 x 21.4 x 3.4 | Outside flange face down, skirt up | None. |
| plate | 1 | 177.0 x 164.7 x 76.2 | Deck underside down, four towers up | None; hollow towers and tie bridges are designed in CAD. |
| rotor | 1 | 129.3 x 129.8 x 6.0 | Head-support face down, hub up | None. |
| fit_coupon | 1 | 55.0 x 11.6 x 10.8 | Four linked block bases down | None; bores5.9/6.0/6.1/6.2 mm increase inX. |
| stake_adapter | 1 | 44.0 x 42.0 x 17.0 | Flat bracket base down; V saddles up | None; small tie-channel bridges; offcut saddle is open. |
| stake_cell_holder | 1 | 80.5 x 70.6 x 19.1 | Flat cradle sole down, snap arms up | Local only under snap beams, as on body. |
| dummy_body | 1 | 195.4 x 37.3 x 53.2 | Flat sole down, pockets up | Local only under hanger flange; nut slots bridge4.3 mm. |
| dummy_lid | 1 | 77.0 x 21.0 x 2.0 | Outside face down | None. |
| dummy_head_insert | 1 | 23.0 x 17.8 x 7.0 | Floor down, ballast pockets up | None. |

## Hand-placed stake adapter

Use a48 in (1219.2 mm) fibreglass garden/driveway stake. `Measurements.stake_d` is the single unmeasured OD parameter, default10 mm. Two90degree V saddles with independent zip ties accept8..13 mm without reprinting; the circle axis rises as radius*sqrt(2), and all three nominal/end-point sizes are intersected against the clamp. No nominal 10 mm closed bore is being passed off as an adjustable clamp. A short5.8..6 mm fibreglass offcut (40 mm long) joins the adapter sleeve to the same pod socket; the external bracket stays clear of the pod neck.

Place the pod midway up the stake, not on its1.2 m top. Insert the stake by hand, then slide/tie the adapter until the actual mic port is 500 mm above the actual soil. The depicted burial is 100 mm only; insertion depth does not determine port height. A separate retaining tie goes around the pod neck and stake through its own adapter tunnel; the offcut is a locator, not a friction-only restraint. Two additional ties hold the separate printed18650 snap cradle lower down (five stake-installation ties total). This retains the owned cell and direct BAT wiring rather than assuming a USB power bank stays awake at the listener load. The stake battery holder is an optional replacement for the flying body, not extra flight mass. Its cell/cable configuration is shown in stake_assembled.step and stake.glb.

## Inert drop-test dummy

The dummy uses the same6 x500 mm rod, hanger location, pod shell/lid/service cap and external FPC backer. A closed twin-pocket ballast cassette replaces the cell cradle inside the dummy body; there is no cell, microphone or electronic stack. A small two-pocket printed head insert replaces the boards. The external backer is retained for approximate shape, while the flexible FPC itself is omitted; matching mass/CG does not match exact aerodynamic flexibility or inertia. Two M2x8 screws and side-loaded M2 captive nuts close the body ballast lid. Foam and adhesive retain the four weighed ballast portions; include their mass within the listed target portions.

Empty dummy assembly estimate: **111.107 g**. Add **36.823 g** total steel ballast to target **147.931 g** and CG **(254.434, 7.087, 9.026) mm**. All three model moment residuals are below 0.001 mm.

| Pocket | Weighed steel + fixative g | Required centre XYZ mm | Equivalent solid-steel block mm |
| --- | --- | --- | --- |
| body_front | 11.629 | 92.000, 16.762, 9.662 | 20.000 x 12.000 x 6.172 |
| body_rear | 20.252 | 130.000, 16.762, 9.662 | 20.000 x 12.000 x 10.750 |
| head_front | 2.471 | 554.000, 0.000, 7.000 | 6.500 x 13.000 x 3.725 |
| head_rear | 2.471 | 566.000, 0.000, 7.000 | 6.500 x 13.000 x 3.725 |

Steel density7.85 g/cm3 sets only the equivalent CAD blocks. Steel nuts, washers or shot can be used if their combined weighed mass and packed centre match the table. Locate each portion with foam spacers; immobilise it so impact cannot move the balance. Avoid loose shot. Pocket clearance and positive capacity are checked from the model. Weigh the actual empty print, solve again with measured values, and compare to the actual real dart target; the numerical nominal match alone is insufficient. Use the dummy for controlled bench release and soil drops to determine whether it turns nose-down, when rotation begins, whether it sticks and whether the snaps/post/rod survive. No model result demonstrates these behaviours.

## Checks, limits and assembly

Current run: **140/140 checks pass**. [checks.md](out/checks.md) and [checks.json](out/checks.json) retain every value and scope; STEP/STL round trips and topology are in [export_validation.json](out/export_validation.json).

Local board/mic/lid/cap/wire/ballast fits use actual B-rep intersection volumes with a0.02 mm3 threshold. Rod press lands, inserts, threads/solder and compressed soft seals have declared intended contact. Frame/prop/leg/ground checks use current exterior parts including the long FPC backer. Vehicle distance numbers are conservative AABB lower bounds; zero does not mean a measured zero gap. Rotor/head contact uses0.5degree samples, rotor/body sweep2degree, extraction0..90 mm in5 mm steps, and prescribed later pitch0..90degrees in5degree steps. These are discrete geometric checks, not a continuous or aerodynamic proof.

| State | Scope |
| --- | --- |
| Carried | Four changed darts against frame/rails,260 mm prop sweeps, skids, harness, ground and each other. |
| Mid-release | Rotor16degrees; dart1 translated70 mm down, three carried. Included in extraction sweep. |
| After extraction | Pitch begins only after 430 mm downward translation with aircraft1500 mm above stock ground. No claim that real fall timing follows this path. |
| Stood | 70 mm rod penetration, body soil stop atZ0, microphone500 mm up. Parked aircraft and three carried darts are offset650 mm from the stood dart for end-state review. |
| Stake | Adapter at 8/10/13 mm stock diameters; mic500 mm above soil; separate cell holder. |
| Dummy | Mass and all three moments matched; all four ballast blocks fit their pockets. |

Assembly order:

1. Measure the actual XIAO/Wio stack, kit FPC antennas, mic breakout, servo, cell and rod. Confirm the aircraft rail/clamp arrangement against the OEM model. Print the fit coupon and tune rod_fit_bore before the long body.
2. Print in supplied STL orientations. Remove local supports and deburr; verify every snap flexes independently and the cell wrap cannot touch a sharp edge. Dry-fit with an inert cell-sized gauge.
3. Heat-set three M2 inserts per pod. Seat the mic film and annular seal, install the breakout with port facing the hood and add its soft preload pad. Do not fill the acoustic cavity with rigid adhesive.
4. Solder BAT wires to underside pads before installing the XIAO. Connect INMP441 to D3/D4/D5/3V3/GND and bridge L/R to ground for the selected channel. Keep headers off; inspect solder for shorts. Plug in Wio via B2B and connect the correct LoRa and WiFi U.FLs.
5. Seat the stack on edge supports, dress all five short wires and route cell leads through the neck/gutter strain reliefs. Fit the supplied FPC to the backer without creasing its feed. Seal gland/rod entry with removable neutral-cure silicone.
6. Slide body until its nose is 70 mm from the sharpened tip. Snap the factory-wired flat-top18650 into the retained cradle; insulate terminals, fit strain relief/body tie and two rod ties. Press the pod onto the final20 mm of rod.
7. Fit perimeter cord and foam pads, close the lid with three M2x6 screws and install/seal the USB cap. Remove only the cap for flashing; use a pin for BOOT/RESET if needed. Check actual plug/pin reach before final sealing.
8. Weigh and balance a completed dart. Update the model if the real balance differs materially from the integral hanger; source estimates are not permission to ignore that difference.
9. Mount SG90 below the plate using two M2 nuts/screws. Fit stock horn, two round M2 drive studs and locking nuts, PTFE bearing film, rotor and loose axial keeper. Match replacement screw thread to the actual servo; never clamp payload load into its shaft.
10. Tie four saddles to the rails. Route servo cable through the fixed gutter; use Pixhawk AUX1 signal, regulated servo supply and common ground. Calibrate0/16/32/48/64degree positions with inert loads. Load in reverse release order.
11. For stake use, fit a40 mm offcut between adapter and pod, tie V saddles to the stake, set the actual mic height to 500 mm, and fit the lower cell holder and insulated leads.
12. For dummy use, fit/immobilise each weighed ballast portion, side-load the two nuts, screw the body lid down and retain head weights under the pod lid. Confirm actual total mass and balance before release tests.
13. Record bench cycling, proof load, vibration, water/acoustic tests and controlled dummy drops before any field release qualification. The present package has completed none of these physical tests.

## Open MEASURE inputs

The central Measurements dataclass includes sourced stock nominals requiring incoming inspection as well as fully unmeasured estimates. Highest-priority unknowns are B2B spacing, exact kit antenna envelopes/weights, microphone breakout/port, BAT pad location, wire dress, cell/rod/filament mass and printed friction/fit. The garden stake OD is one parameter; clamp geometry spans8..13 mm.

| Parameter | Nominal input |
| --- | --- |
| rod_d | 6.0 |
| rod_fit_bore | 5.95 |
| rod_density | 1.9 |
| cell_d | 18.33 |
| cell_l | 64.85 |
| cell_mass | 45.0 |
| cell_terminal_d | 6.0 |
| cell_terminal_h | 0.35 |
| cell_insulator_d | 14.4 |
| cell_insulator_t | 0.12 |
| sg_case_l | 22.7 |
| sg_case_w | 12.2 |
| sg_case_h | 27.0 |
| sg_tabs_span | 32.3 |
| sg_tab_z | 17.0 |
| sg_tab_t | 2.0 |
| sg_hole_pitch | 27.5 |
| sg_hole_d | 2.0 |
| sg_axis_from_end | 5.9 |
| sg_spline_d | 4.8 |
| sg_spline_teeth | 21 |
| sg_spline_h | 3.3 |
| sg_screw_d | 1.6 |
| sg_gear_cap_h | 4.3 |
| sg_gear_cap_r | 5.7 |
| sg_rear_cap_r | 3.2 |
| sg_rear_cap_h | 3.0 |
| sg_case_corner_r | 1.0 |
| sg_spline_groove_w | 0.35 |
| horn_l | 27.0 |
| horn_w | 5.2 |
| horn_t | 1.6 |
| horn_boss_d | 7.0 |
| horn_boss_h | 3.8 |
| horn_pin_pitch | 18.0 |
| mic_board_w | 14.0 |
| mic_board_l | 16.0 |
| mic_board_t | 1.0 |
| mic_port_d | 1.0 |
| mic_port_x_offset | 0.0 |
| mic_pad_row_span | 11.0 |
| mic_pad_pitch | 4.5 |
| mic_mass | 1.0 |
| xiao_mass | 2.2 |
| wio_mass | 1.8 |
| stack_spacing | 7.5 |
| fpc_l | 100.0 |
| fpc_w | 10.0 |
| fpc_t | 0.3 |
| fpc_mass | 0.8 |
| wifi_l | 20.0 |
| wifi_w | 6.0 |
| wifi_mass | 0.35 |
| stake_d | 10.0 |
| stake_burial | 100.0 |
| ballast_density | 7.85 |
| petg_density | 1.27 |
| petg_modulus | 1600.0 |
| printed_allowable_strain | 0.015 |
| wire_od | 1.05 |
| prop_plane_from_bottom_plate | 57.0 |
| prop_sweep_thickness | 4.0 |

## Exploded web models and visual review

`web_export.py` writes dart, harness, aircraft and stake GLBs in metres with Y up, using named physical-part nodes and an8-second `explode` clip. Dart/harness/aircraft views expose the populated board stack, mic, cap, lid, seals, wiring and hardware; aircraft first lowers its loaded harness400 mm. The stake clip withdraws the retained pod subassembly100 mm from the offcut. This is an illustration: disconnect wires, cut disposable ties and unscrew hardware in actual service. Motion does not simulate threads, flexures, cables, falls or continuous collision-free disassembly.

The current mass report supplies per-node mass estimates and source/uncertainty facts in `web/manifest.json`. Servo/horn share the 9 g catalog mass; aircraft solid masses remain null. `validation-readback.json` checks every sampled animation translation and loads each GLB with trimesh; `validation-khronos.json` holds Khronos results. `exploded_checks.json` checks independent endpoint subassemblies for overlap. Full-resolution STEP/STL files remain the manufacturing geometry.

Every final PNG is listed in REVIEW.html. Visual inspection covers all assembled, sectioned, exploded and print orientations; a per-file review receipt is stored in `out/visual_review.json` after inspection. No visual claim replaces a physical fit test.
