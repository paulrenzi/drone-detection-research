"""Generate the review package documentation from the measured CAD outputs."""
from pathlib import Path
import json, html
from parameters import *
ROOT=Path(__file__).resolve().parent
out=ROOT/'out'
mass=json.loads((out/'mass_properties.json').read_text())
checks=json.loads((out/'checks.json').read_text())
manifest=json.loads((out/'print_manifest.json').read_text())

def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+''.join('| '+' | '.join(str(x) for x in row)+' |\n' for row in rows)

def item(name):return next(r for r in checks['checks'] if r['check']==name)

sources=[
('S1','Holybro X500 V2 official frame STEP and product/assembly drawing','https://holybro.com/collections/multicopter-kit/products/px4-development-kit-x500-v2','Unscaled 2022-07-19 manufacturer CAD. Centre plates, tubes, motor assemblies, clamps, battery and companion platforms, stock legs, hardware. Rail axes 60mm apart; rail OD9.4 in CAD versus catalog10. Use10mm clearance. Coincident duplicate solids removed, logged in cache/model.json.'),
('S2','Holybro AIR2216II motor/prop drawing','https://cdn.shopify.com/s/files/1/0604/5905/7341/files/X500MotorSpec.png?v=1678791632','Motor outer geometry comes from S1. Drawing gives motor OD27.7 and body31; 1045 swept diameter is conservatively260mm per the drawing, rather than254mm nominal10in.'),
('S3','TowerPro SG90 Digital manufacturer page/drawing','https://towerpro.com.tw/product/sg90-7/','Drawing A30.3, B22.7, C27, D12.2, E32.3, F17mm; nominal9g and 1.8kg.cm stall at4.8V. Stepped case and seams reconstructed from manufacturer photo, not a block. Undimensioned spline, tabs and supplied horn remain MEASURE.'),
('S4','Heltec V3 datasheet Rev1.1 and manufacturer 3D directory','https://s.heltec.cn/download/WiFi_LoRa_32_V3/3D/','Detailed HTIT-WB32LAF_V3.7(3).step used for populated PCB/USB-C/U.FL/buttons/connectors. Source has no OLED: add33.28x18.56 module from Rev1.1 p14, stack height/thickness MEASURE. Datasheet PCB envelope50.2x25.5x10.2; V3.7 STEP PCB is51.689x25.4, including end shape. No scaling. Verify exact purchased revision. Older non-exact STEP was inspected and rejected as a primary geometry source.'),
('S5','Samsung INR18650-25R specification, manufacturer-authored PDF mirror','https://files.dcpower.eu/datasheets/samsung/INR18650-25R-datasheet.pdf','Diameter18.33+/-0.07; length64.85+/-0.15mm; mass45g maximum. Positive terminal/insulator detail is a MEASURE envelope. Use an unprotected flat-top 25R with factory welded leads; protected/button-top cells will not fit.'),
('S6','TDK INMP441 product and DS-INMP441-00 Rev1.1 Fig16','https://product.tdk.com/en/search/sw_piezo/mic/mems-mic/info?part_no=INMP441','Bare package4.72x3.76x1.00; bottom port0.25mm and1.07mm from right edge. Package offset1.29 aligns its port to breakout hole. Generic14x16mm breakout is not standardized: its outline, thickness, mass and PCB port are MEASURE.'),
('S6a','TDK application note AN1124, sealing bottom-port microphones','https://invensense.tdk.com/wp-content/uploads/2015/02/Recommendations-for-Sealing-InvenSense-Bottom-Port.pdf','Basis for soft membrane with an air cavity; modeled0.8mm cavity and0.05mm prototype silicone film. Dimensions/material response are design assumptions requiring acoustic and water tests, not a claimed IP rating.'),
('S7','HellermannTyton UV-stabilized T18R 111-01711','https://www.hellermanntyton.com.br/produtos/abracadeiras-com-serrilhado-interno/t18r/111-01711','100x2.5mm strap,1.0mm thick, head4.8x4.45x3.7;80N minimum catalog strength. Fitted closed loops and trimmed heads are modeled at their installed locations.'),
('S8','3M5490 PTFE film tape technical data','https://multimedia.3m.com/mws/media/2522949O/3m-ptfe-extruded-film-tape-5490.pdf?fn=3M-PTFE-Extruded-Film-Tape-5490.pdf','0.09mm total thickness; low-friction bearing strip on the printed ridge. Numerical friction coefficient0.12 is an engineering assumption, not a3M published value.'),
('S9','Ruthex RX-M2x4 manufacturer product/CAD','https://www.ruthex.de/products/ruthex-gewindeeinsatz-m2-70-stuck-rx-m2x4-messing-gewindebuchsen','Actual knurled STEP used. OD3.6 x4.0mm;3.2mm pilot/5.2mm depth. Four per pod. Fit pilot on filament coupon before heat setting.'),
('S10','M2 hex nut dimensional table, manufacturer Accu','https://www.accu.co.uk/hexagon-nuts/655596-HPN-M2-PCN','DIN934/ISO4032 envelope:4mm across flats,1.6mm height. The CAD uses metal hardware density; this linked variant demonstrates the shared dimensional standard, not the selected nut material.'),
]

doc=f'''# Tripwire listener and X500 release harness - first-print mechanical package

Built in CadQuery2.8.0, millimetres. All work and all downloaded references are inside this directory. No commit or push was made.

**Model estimate: {mass['dart_total_g']:.1f}g per dart; {mass['harness_total_g']:.1f}g harness; {mass['carried_payload_g']:.1f}g total four-dart payload.** The integral hanger is {mass['hanger_x_mm']:.2f}mm from the tip and {mass['hanger_y_mm']:.2f}mm to the cell side of the rod. The assembly is {POD_X1+M.whip_l:.0f}mm tip-to-whip. Sound port height is {MIC_X-BODY_X0:.0f}mm above soil at full70mm penetration.

This is a checked geometric prototype, not a printed, drop-qualified, waterproof or flight-qualified assembly. Source uncertainty is retained explicitly. The generic microphone breakout, servo variant, actual antenna, filament fit and installed aircraft must be measured before releasing a print for use.

## Deliverables and reproduction

- [REVIEW.html](REVIEW.html) is the local visual index. [renders/](renders/) contains the final CAD renders.
- [out/](out/) contains six printed-part STEP/STL pairs, the three full-aircraft states, a separate stood dart, bought-part references, machine-readable mass/check reports and export validation.
- STEP files retain design datums. STL files are already rotated and translated into their print orientation, resting atZ0. Do not auto-rotate them onto a different face.
- Five functional printed designs: body, pod shell, pod lid, harness plate, rotor. A sixth design is the disposable rod-fit coupon. A four-dart kit uses4 bodies,4 shells,4 lids,1 plate,1 rotor. This is14 functional pieces, plus one coupon.
- The large STEP files retain manufacturer electronic and aircraft detail. Shared listener subassemblies are instanced in the full system exports.

From the repository root in PowerShell:

```powershell
& 'C:\\Users\\paulm\\.venvs\\cad\\Scripts\\python.exe' cad/gpt61/fetch_sources.py
& 'C:\\Users\\paulm\\.venvs\\cad\\Scripts\\python.exe' cad/gpt61/build.py
& 'C:\\Users\\paulm\\.venvs\\cad\\Scripts\\python.exe' cad/gpt61/validate_exports.py
& 'C:\\Users\\paulm\\.venvs\\cad\\Scripts\\python.exe' cad/gpt61/document.py
```

`build.py --render-only`, `--verify-only`, `--exports-only` use the generated cache. `--geometry-only --no-render` rebuilds and checks without exporting. Remove only this directory's `cache/` if you replace an OEM reference asset; the immutable aircraft cache otherwise accelerates rebuilds. `parameters.py` holds source dimensions and the central MEASURE block. `printed.py` and `purchased.py` construct the actual B-reps; rendered pixels and meshes are never the geometry source.

## Source register

'''
for code,title,url,note in sources:doc+=f'- **{code}: [{title}]({url}).** {note}\n'
doc+='''
Downloaded files, original URLs, byte sizes and SHA256 hashes are in [sources/manifest.json](sources/manifest.json). Source STEP files are preserved. `sources/heltec-v3-datasheet.pdf-drawing.png`, `sources/inmp441-outline.png` and the TowerPro images are the drawing/photo review evidence. There is no manufacturer CAD for the selected generic mic module or the unspecified82mm antenna; those are deliberately parameterized reconstructions. Source documents retain their original ownership/licensing.

## Four-listener kit BOM

| Bought item | Kit quantity / size |
| --- | --- |
| Solid fibreglass rod | 4 x6mm x500mm |
| Samsung25R flat-top18650 with factory welded insulated leads | 4 |
| Heltec WiFi LoRa32 V3 board and OLED, tall headers left off | 4, verify purchased revision |
| INMP441 breakout | 4, verify the14x16mm nominal outline and port |
| Whip/U.FL pigtail | 4, verify82mm whip envelope and4mm boot |
| Genuine positional SG90 and supplied double horn | 1 |
| Ruthex RX-M2x4 heat-set inserts | 16 |
| M2x6 socket cap screws,3.8mm head diameter,2mm head height | 18:16 pod,2 servo mounting |
| M2x10 threaded drive studs | 2, adjust projection to the modeled stack |
| M2 hex nuts,4mm AF x1.6mm high | 6:4 drive-stud clamp nuts,2 captive servo nuts |
| Longer output-spline screw | 1 x10mm under-head, nominalM1.6; match the actual servo thread |
| Keeper spacer | 1,3mm OD x1.8mm ID x4.2mm long; adapt ID to measured screw |
| Keeper washer | 1,10mm OD x1.85mm ID x0.4mm thick |
| T18R UV-stabilized zip ties | 16:4 rails,4 body strain relief,8 along rods |
| Silicone perimeter cord | 1.2mm diameter, about220mm per pod plus joining allowance |
| Soft silicone sound film and cavity seals | 4 films,8mm diameter x0.05mm;4 annular seals,7.6mm OD x4mm ID x0.8mm |
| PCB foam pads | 16 small edge pads; additional removable mic preload pad |
| 3M5490 PTFE film | One annular strip,R48.3..50.7mm,0.09mm total thickness |
| Power wire, mic jumpers, battery connector, terminal insulation, removable neutral-cure RTV | Quantity to dress the modeled routes;28AWG power wire nominal1.05mm OD |

The stock X500 hardware is retained. Printed quantities are4 bodies,4 shells,4 lids,1 plate,1 rotor, and one optional fit coupon.

## Changes required to make the fixed concept assemble

1. Split the closed pod into a tray and screw lid. A closed one-piece shell cannot accept, wire and later service this populated board. Four heat-set M2 inserts, a locating lip, removable silicone cord, rod/cable RTV seals and a membrane-covered sound cavity make it serviceable. No USB or display opening breaks the seal; open the lid for service.
2. Move the board after the rod end: the20mm socket occupies480..500mm, the PCB starts around502.4mm, and the far insert bosses move beyond the actual PCB corners. The pod ends at562mm; the82mm assumed whip gives644mm overall. The old564mm figure described the pod end, not the complete dart plus whip.
3. Replace an unrelieved long C-shell snap with four independently relieved18mm axial beams. The saddle carries the cell; two end walls carry axial impact load; fingers have real lead-in and retention faces. Relief under the beams allows bending. The final cell cavity is recut through all support ribs so none enter the cell.
4. Align the integral hanger with BOTH longitudinal and lateral model CG. The battery is beside the spine, so a hanger over the rod axis would produce a roll moment. Tapered lateral and longitudinal gussets spread the offset hanger load into the rod sleeve. The balance is solved again from the complete model, including negative-terminal wiring.
5. Add a protected negative-lead gutter beside the cell, retention bridges, a two-wire spine gutter and a tie bridge. Both cell terminals now have continuous modeled routes to the pod; wires are not simply shown starting at the rear terminal. The500mm rod remains one solid part.
6. Lower the harness under the existing battery carrier. Rail-axis to deck is72mm. Rear saddles are atX=-85; forward ones atX=60, in clear rail regions between vendor clamps/platforms. The forward towers lean outward near the rotor, then back to the rails above it. Two open plate-edge notches clear the splayed stock landing legs. The stock frame and stock legs are retained.
7. Position the four heads at radius68mm, with transverse positions+22,+62,-22,-62mm. Matching slots pass the entire13mm head and the tapered stem. The inner pair releases first, on opposite sides, followed by the outer pair, at16,32,48,64degrees. The slots are recut after adding tower beams so no beam silently refills them.
8. The bearing ridge, with0.09mm PTFE film, supports the rotor directly. A concentric sliding pilot handles lateral guidance. The original bought horn drives two M2 round pins into axial-clearance holes; upper nuts have actual hex envelopes and clearance counterbores. Servo mount nuts are captive in measured across-flats traps. The shaft does not set the bearing height.
9. Add a loose axial keeper: a measured-thread replacement servo screw, a4.2mm bought spacer and a10mm washer sit0.4mm above the rotor. This prevents bounce-out while leaving the static dart weight on the ridge. Undo the screw to service the rotor. Output-screw thread is a mandatory MEASURE item.
10. Print plate flat and rotor top-face-down. The case tabs meet the underside of the3.2mm deck, and the bearing height rises to12mm. No downward mounting bosses suspend the plate above its print bed. The body needs local support under its round hanger flange and four elevated snap beams. Its offset hanger station is widened below the gussets, and the aft gusset ends inside the foundation. The pod tray needs small accessible supports below the exterior hood/socket lip and the two short interior mic-guide ledges. Lid, plate, rotor and coupon need none in their listed orientations.

## Key fits and mechanics

'''
doc+=table(['Feature','Nominal dimensions / allowance'],[
('Rod','6x500mm;12mm sharpened end; body begins70mm from tip'),
('Rod sleeve','6.35mm teardrop clearance bore; three4mm press lands at5.95mm;0.8mm compliance slit;1mm entry lead-in'),
('Cell cradle',f'{M.cell_d+.5:.2f}mm saddle ID;1.6mm wall;16.8mm throat;1.2mm beam thickness;18mm active length;6.8mm height'),
('Pod',f'480..562mm;36mm body width; hood increases installed width to41.4mm;1.6mm walls;2mm lid; minimum floor1.6mm'),
('Seam','1.5mm groove width,0.9mm depth;1.2mm silicone cord,25% squeeze and84% gland fill;0.30mm radial locating-lip clearance'),
('Mic','Bottom port looks sideways, atX540mm;4mm acoustic aperture;0.8mm cavity behind0.05mm film; upper rain hood drains downward'),
('Hanger','5mm neck,13mm round head,3.2mm flange; flat underside bears on rotor; stem14x9mm'),
('Plate / slots','3.2mm plate,83mm radius;20.4x15.4mm radiused head slots;12mm bearing plane'),
('Rotor','64.9mm radius,3.2mm web,6mm overall hub; four20degree release gaps, cut radially56..66.9mm'),
('Pilot','32mm OD;32.5mm mating ID:0.25mm radial sliding clearance;0.10mm roof clearance'),
('Bearing','R48..51mm printed ridge;0.3mm edge chamfers; filmR48.3..50.7mm; rotor contactZ12mm'),
('Horn dogs','Two M2 pins18mm apart;2.44mm drive holes;5.2mm nut-clearance counterbores; upper-nut roof clearance0.35mm'),
('Rail saddles','10.6mm seat bore for catalog10mm rail;60mm rail centre spacing;3.1x3.2mm tie tunnels'),
('M2 nut traps','4.3mm across flats for4.0mm ISO4032/DIN934 nuts; CadQuery polygon diameter converted correctly'),
('Inserts','Ruthex3.6x4.0;3.2mm pilot,5.2mm depth; bossOD7mm'),
])
snap=item('snap_flexure_screen');friction=item('bearing_friction_screen')
doc+=f'''
The beam screen uses maximum cell diameter18.40mm, a throat0.20mm undersize, and symmetrical bending: **{snap['per_arm_deflection_mm']:.2f}mm per arm**. `epsilon=3*t*delta/(2*L^2)` gives{100*snap['nominal_surface_strain']:.2f}% nominal strain; a2x root factor gives{100*snap['factored_strain']:.2f}% against the1.5% assumed screening limit. WithE=1600MPa, the four-arm tip-force estimate is{snap['four_arm_force_N']:.2f}N. This is a static elastic screen, not impact-retention or fatigue proof. PETG print direction, root relief, creep and actual filament must be tested. No mold-release draft is applied to functional FDM fits; the towers taper and entry ramps/chamfers provide the useful lead-ins.

At3g, the5mm hanger neck screens at{item('hanger_tension_screen')['stress_3g_MPa']:.3f}MPa axial stress against an assumed8MPa printed allowance. At rest each head has about26.73mm2 of rim support. The friction estimate with assumedmu=0.12 is{friction['static_torque_Nm']:.3f}N.m static and{friction['three_g_torque_Nm']:.3f}N.m at3g, versus0.177N.m rated SG90 stall. Stall is not a continuous operating rating: measure breakaway torque/current with the actual tape and full load. PTFE film is part of this fit and load-path stack.

## Mass and balance

All prototype printed parts use **100% infill**, four perimeter lines and six top/bottom layers. Thin walls are solid. Printed mass is real modeled material volume times1.27g/cm3, without an arbitrary whole-part60% multiplier. Material densities and assembly mass overrides are in the machine-readable report. The cell uses its45g datasheet maximum; PCB9g, mic1g, antenna1.2g and rod density remain MEASURE estimates. The electronic CAD centroid is a spatial proxy, not a component-by-component measured weight distribution. Adhesive/RTV, small solder and field dirt add unquantified mass; reweigh the built dart and update the parameters before fixing the production hanger.

'''
rows=[]
for n in ('body','pod_shell','pod_lid'):
    r=next(x for x in mass['dart'] if x['name']==n);rows.append([n,f"{r['mass_g']:.2f}",f"{r['volume_mm3']/1000:.3f}",f"{r['centroid_mm'][0]:.2f}"])
for n in ('plate','rotor'):
    r=next(x for x in mass['harness'] if x['name']==n);rows.append([n,f"{r['mass_g']:.2f}",f"{r['volume_mm3']/1000:.3f}",f"{r['centroid_mm'][0]:.2f}"])
rows.append(['fit coupon','4.49','3.537','not carried'])
doc+=table(['Printed design','Mass g','Material cm3','Centroid X mm, design datum'],rows)
doc+=f'''
Full individual bought-part and consumable masses and XYZ centroids: [out/mass_properties.csv](out/mass_properties.csv), [out/mass_properties.json](out/mass_properties.json). This includes all screws, actual insert volumes, nickel tabs, cell wiring, cord/film, rod ties, stock horn, drive hardware, keeper and rail ties.

- Dart total: **{mass['dart_total_g']:.2f}g**. Model CG: **({mass['dart_cg_mm'][0]:.2f}, {mass['dart_cg_mm'][1]:.2f}, {mass['dart_cg_mm'][2]:.2f})mm**, tip/rod/print datum.
- Hanger axis: X{mass['hanger_x_mm']:.2f}, Y{mass['hanger_y_mm']:.2f}mm. Longitudinal solve residual{mass['balance_residual_mm']:.4f}mm. Tolerance is not a claim about the real article; measured part weights control the actual balance.
- Harness complete: **{mass['harness_total_g']:.2f}g**, CG({', '.join(f'{x:.2f}' for x in mass['harness_cg_mm'])})mm in harness coordinates.
- Four darts plus harness: **{mass['carried_payload_g']:.2f}g**. This excludes the existing aircraft, flight battery and avionics. No flight-time, useful payload or stability qualification is inferred.

## Assembly checks and limits

{sum(r['pass_'] for r in checks['checks'])}/{len(checks['checks'])} generated checks pass. Full data: [out/checks.json](out/checks.json) and [out/checks.md](out/checks.md). Printed STEP round-trip and STL manifold/volume evidence is in [out/export_validation.json](out/export_validation.json).

The actual B-reps are intersected after broad-phase pruning. Buried PCB/mic/cell/lid/wire fits are checked separately. External aircraft checks conservatively fill the pod envelope, including its hood. The intentionally interfering rod press lands and heat-set inserts, solder/threads and compressed seals are declared separately. Aircraft distance numbers in the report are **axis-aligned bounding-box lower bounds**, not precise gap measurements; a zero lower bound with zero interference does not mean a zero real gap.

'''
doc+=table(['Case','Scope / result'],[
('Carried','All four darts versus frame/rails/clamps, motors,260mm prop swept slabs, stock legs, harness and one another. Modelled solids have no unwanted overlap at the nominal parameters.'),
('Ground, carried',f"Lowest dart envelope is{item('carried_dart1_ground')['clearance_mm']:.2f}mm above the stock-skid ground plane. The printed harness also remains above it. Prop swept-slab separation has a conservative123.6mm lower bound at the nominal fitted prop plane."),
('Rotor / release','Head contact sampled every0.5deg across0..64deg. Each dart has full support through its preceding detent, and no footprint at its release detent. Neck/body-to-rotor checked every2deg.'),
('Extraction','Each dart translated0..90mm down in5mm samples, with its matching rotor gap aligned; checked against the complete aircraft and harness. This includes the head passing the plate.'),
('Pitch after separation','A prescribed0..90deg nose-down path in5deg samples is checked only AFTER430mm downward separation. The aircraft is lifted1500mm above its stock ground datum for this clearance case. This demonstrates a possible clear geometric path, not the actual fall/rotation timing.'),
('Mid-release rendering',f"Rotor16deg; first dart70mm down, three retained;{item('carried_dart1_ground')['clearance_mm']-70:.2f}mm remaining ground clearance at the stock-skid datum. This is an explicit assembly state, not a dynamic simulation."),
('Stood','70mm tip penetration, body nose on ground and electronics above ground. Full assembly_stood also includes the aircraft on its stock skids with three listeners and the upright listener650mm beside it; this separation is a review layout, not a deployment spacing recommendation.'),
])
doc+='''
Release order is dart1 at16, dart3 at32, dart2 at48, dart4 at64degrees. Full clearance windows are approximately11..21,27..37,43..53,59..69degrees; the sampled sweep ends at64, so the final report clips the last window there. A head begins losing area during the commanded transition before its target stop. It is not claimed to remain supported until the exact mathematical detent. Keep calibrated position error below2degrees for prototype bench work and determine actual positions under load.

The continuous interval between samples, flexible prop motion, airflow-induced bowing, frame compliance, acceleration, line snagging, inversion, actual self-righting, impact, soil penetration and acoustic/radio performance have not been simulated or tested. In particular, no model establishes that this dart naturally waits430mm before rotating. Test that trajectory physically with inert mass dummies before any flight release. The rod must be free of splinters and the printed hanger must survive the required proof load. An actual installed aircraft/servo/board measurement supersedes nominal CAD.

## MEASURE register

Every uncertain fit/property used as a model input is a single field in the `Measurements` dataclass in `parameters.py`. Some have sourced nominal dimensions but still need incoming-part verification. The generic breakout and actual whip are the largest unresolved purchased-item identities. No manufacturer datasheet was found for a standardized14x16mm INMP441 breakout or the old82mm whip estimate. Do not substitute the bare microphone IC dimensions for a breakout, and do not assume a50mm Heltec antenna has an82mm envelope.

'''
doc+=table(['Parameter','Current nominal'],[(n,v) for n,v in measure_dict().items()])
doc+='''
Also verify these installed interfaces: X500 rail OD/60mm spacing and the exact clamp/platform arrangement against S1; unobstructed saddle zones atX=-85/+60; prop actual diameter/plane;1.2mm silicone cord; gasket compression;3.2mm insert pilot after printing; tape thickness; and total hardware/RTV/solder mass. If these differ, update the corresponding parameter/design choice and rerun the geometry checks. Cosmetic reconstructions are not manufacturing drawings for the bought parts.

## Print settings

PETG; dry filament;0.4mm nozzle;0.20mm layer;0.42mm line width if your slicer permits, four perimeters; six top/bottom layers;100% infill. Use the filament maker's temperature range (typical prototype starting point235C nozzle/80C bed, then tune). External walls30mm/s, first layer20mm/s, modest cooling after the first layers. Deburr sliding/contact faces; keep brim out of functional holes. PETG creep and layer adhesion need the physical checks below.

'''
print_rows=[]
for row in manifest:
    n=row['part'];dims=' x '.join(f'{x:.1f}' for x in row['print_bbox_mm'])
    orient={'body':'Flat sole down; cradle and post up','pod_shell':'Floor down; open side up','pod_lid':'Outside face down; lip and fingers up','plate':'Flat deck underside down; towers up','rotor':'Top face down; hub/pockets up','fit_coupon':'Linked block bases down'}[n]
    support='Local support under hanger flange and four snap beams. Allow supports on the model;0.20mm top/bottom Z gaps, one interface layer. Clear0.7mm beam reliefs; block rod-bore supports.' if n=='body' else 'Small local supports below exterior rain hood/socket lip and two short interior mic-guide ledges; remove before electronics installation.' if n=='pod_shell' else 'None; small designed bridges/teardrop roofs only.'
    print_rows.append([n,row['quantity'],dims,orient,support])
doc+=table(['Part','Kit qty','STL bounds mm','Orientation','Support'],print_rows)
doc+='''
All oriented bounds fit the245x245x260mm Vyper. The coupon's5.9/6.0/6.1/6.2mm bores increase inX order. Print it first in the same material/profile. Choose the light interference fit that does not split or excessively stress the rod, and set `rod_fit_bore` accordingly. Do not force a500mm rod through an uncalibrated long press fit. The closed sections have a45degree teardrop roof and the compliance slot opens above the round contact area.

## Assembly sequence

1. Identify and measure the exact bought servo, cell, rod, board revision, microphone breakout and antenna. Check the rail zones with the aircraft unpowered and props removed. Print the rod-fit coupon and one cell cradle/body first. Tune the fit parameters if necessary.
2. Print the14 kit pieces in the supplied STL orientations. Remove the local flange and snap-beam supports and the pod's hood/socket/guide supports, deburr ramps/holes, inspect beam roots and test each finger independently. Clear every0.7mm relief beneath a snap beam with a thin blade from its open outer edge; no support may remain to lock the beam to the saddle. Dry-fit the cell with an inert18.33mm dummy first. Keep cell sleeves and nickel leads away from sharp print edges.
3. Heat-set four RX-M2x4 inserts into each shell using a depth stop. Leave the sealing land flat and avoid pushing into the floor. Clean and test the groove. Put the silicone film over the sound port on the inside, with the0.8mm soft cavity seal in front of the mic PCB. Slide the breakout into its guides, sound hole facing the membrane/side hood. Use a removable foam pad under the lid tab to preload the board gently. Do not cover the acoustic cavity with rigid glue.
4. Seat the headerless Heltec PCB on its four edge pads, USB toward the rod socket, components/OLED facing the lid. Leave the supplied tall18-way pin headers unsoldered; the plated rows are present and modeled. Connect short flexible mic wires to header pads; route them in the open side volume outside the OLED/fingers, verify lid closure with no pinched wires, and retain with removable silicone. The package models the long power wires explicitly; internal mic jumpers must be dressed during assembly and are not individually resolved in CAD.
5. Use a factory spot-welded/prewired flat-top25R, with insulated terminal tabs. Thread its negative lead through the external gutter/bridges and positive lead through the rear strain relief. Snap the cell downward past all four lips. It must seat on the saddle and against the end-wall pads without permanent beam deformation. Insulate exposed tabs with heat-shrink/removable neutral-cure silicone. Do not solder directly to the cell can.
6. Slide the body onto the unsharpened rod end until its nose is70mm from the tip. The sleeve's press lands carry the fit; confirm pull-off resistance. Sharpen the last12mm without cutting the500mm overall length. Route both power wires in the side gutter and along the rod with the two modeled small ties; fit the body strain-relief tie around the sleeve atX163mm. The second molded bridge is an additional RTV/strain-relief anchor. Trim tie tails flush.
7. Fit the shell over the last20mm of rod. Seat to the socket stop; add a removable neutral-cure RTV bead around the rod entry, wire gland and whip boot. Anchor the power service loop at the two molded internal tie/RTV saddles. Connect the board's battery plug and U.FL lead without loading the tiny connector. The antenna boot, not U.FL, should carry cable strain.
8. Fit the1.2mm silicone cord in the perimeter groove; join its ends with compatible silicone outside the acoustic cavity. Add the four small compliant PCB-edge pads. Close the lid and tighten four M2x6 socket cap screws gradually by hand, checking uniform seal squeeze and no PCB/OLED contact. Verify mic airflow/acoustic response and water ingress separately; the hood alone does not seal the microphone, and FDM walls are not inherently watertight.
9. Weigh one complete dart and measure its balance inX andY. Enter measured masses/properties, rerun and compare to the integral post. A meaningful change requires a revised body print; do not pretend the calculated0.01mm solver residual is real balance precision.
10. Press the two M2 nuts into the plate's top-accessible traps. Mount the SG90 from underneath with two M2x6 screws through its tabs. Ensure the actual case and shaft height match the parameters. Apply the0.09mm PTFE strip only to the flat crown of the bearing ridge; keep adhesive and steps out of the sliding pilot.
11. Fit the original double horn to the servo spline. Ream the two measured holes to accept M2 round drive studs18mm apart; lock each with an M2 nut above and below the horn. Adjust upper nuts to the modeled height. Place the rotor on the ridge with dogs in its two holes; verify axial/radial freedom and that the upper nuts clear the counterbores through the full0..64degree sweep.
12. Fit the bought4.2mm spacer,10mm keeper washer and the longer screw with exactly the measured servo thread. The spacer clamps the horn; keeper underside is0.4mm above the rotor. Confirm the washer does not press the rotor onto the servo. Route the servo lead through its feedthrough and fixed top gutter. Drive from the specified Pixhawk AUX1 signal, with a suitable regulated4.8-5V servo supply and common ground. Calibrate angle/pulse stops on the bench; no generic PWM numbers are supplied as if universal.
13. Zip-tie the four saddles to the two payload rails using the modeled T18R locations. Use two stations per rail, not one tie for the entire harness. The saddle seats and braces carry the normal load. Confirm the complete assembly clears actual clamps, skids, battery, wiring and props.
14. Load in reverse sequence:64degrees last dart,48 third,32 second,16 first, then return0. Use inert masses first. With all four loaded, verify free rotation, no axial servo load, individual release in each16degree command, full head passage, and positive retention between stops. Bench-cycle, shake, proof-load and perform controlled dummy drop/soil tests before qualification. Record actual rotation timing, battery retention, layer cracking and rod insertion depth.

## Visual QA

Every final PNG was inspected after generation. Sections are boolean cuts viewed from the cut side; the pod exploded view exposes the insert bosses, supports and lid fingers. Each print render includes a build surface and uses the exact supplied STL orientation. The single stood view includes a thin cutaway soil slab so the70mm buried tip remains visible. The full stood scene includes the actual aircraft and a thick ground solid. Early reference/iteration images are archived with the sources, separate from the final gallery.
'''
(ROOT/'DESIGN.md').write_text(doc,encoding='utf-8')

gallery=[('assembly_carried.png','Carried on X500'),('assembly_mid_release.png','Mid-release'),('assembly_stood.png','Full stood state'),('release_detail.png','Release mechanism'),('dart_stood.png','One listener standing'),('section_body.png','Body longitudinal section'),('section_body_snap.png','Cell snap section'),('section_pod.png','Pod section'),('pod_exploded.png','Pod service assembly')]+[(f'print_{n}.png',f'Print: {n}') for n in ('body','pod_shell','pod_lid','plate','rotor','fit_coupon')]+[('bought_heltec.png','Manufacturer-based Heltec'),('bought_servo.png','SG90, stock horn and keeper')]
cards=''.join(f'<figure><a href="renders/{f}"><img src="renders/{f}" alt="{html.escape(t)}" loading="lazy"></a><figcaption>{html.escape(t)}</figcaption></figure>' for f,t in gallery)
page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tripwire mechanical review</title><style>body{{font:16px/1.5 system-ui;background:#edf2f4;color:#203442;margin:0}}header{{background:#173340;color:white;padding:3rem 6vw}}main{{max-width:1500px;margin:auto;padding:2rem}}h1{{font-size:2.1rem;margin:.2em 0}}.meta{{opacity:.85}}nav a{{display:inline-block;color:#153b50;background:#fff;padding:.5em 1em;margin:.5em;border-radius:4px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(480px,1fr));gap:1.3rem}}figure{{margin:0;background:white;border-radius:7px;overflow:hidden}}img{{width:100%;height:440px;object-fit:contain;background:#f4f7f9}}figcaption{{padding:1rem;font-weight:600}}@media(max-width:600px){{.grid{{display:block}}figure{{margin-bottom:1rem}}img{{height:auto}}}}</style><header><div class="meta">CADQUERY / FIRST-PRINT PROTOTYPE</div><h1>Tripwire listener and X500 release harness</h1><p>{mass['dart_total_g']:.1f}g per listener &middot; {mass['harness_total_g']:.1f}g harness &middot; {POD_X1+M.whip_l:.0f}mm overall</p><p class="meta">Sourced bought-part CAD, real wall sections, snaps, seals, load path and FDM fits. Measurements and physical qualification remain open.</p><nav><a href="DESIGN.md">Design and assembly</a><a href="out/">CAD exports</a><a href="out/checks.md">Geometry checks</a><a href="out/mass_properties.csv">Mass table</a></nav></header><main><div class="grid">{cards}</div></main></html>'''
(ROOT/'REVIEW.html').write_text(page,encoding='utf-8')
print('Wrote DESIGN.md and REVIEW.html')
