"""Millimetres, grams. D=design choice, S=source; MEASURE values are centralized.

S1 Holybro official frame STEP, downloaded by fetch_sources.py (unscaled).
S2 Holybro X500MotorSpec.png, same product page; T1045II diameter stated 260 mm.
S3 TowerPro https://torqpro.com/product/sg90-digital/ and its dimensional drawing.
S4 Seeed XIAO and Wio-SX1262 OEM STEP archives; sources/xiao-manifest.json.
S5 Samsung INR18650-25R specification in sources/samsung-25r.pdf section 3.
S6 TDK INMP441 datasheet, outline page20; official product page.
S7 HellermannTyton T18R-PA66W-BK 111-01711 official dimension table.
S8 https://multimedia.3m.com/mws/media/2522949O/3m-ptfe-extruded-film-tape-5490.pdf
S9 Ruthex RX-M2x4 manufacturer STEP (manifest URL).
S10 DIN934 M2: AF4, height1.6mm, manufacturer dimensions at
https://www.accu.co.uk/hexagon-nuts/655596-HPN-M2-PCN (same dimensional standard).
"""
from dataclasses import dataclass, asdict

@dataclass
class Measurements:
    # MEASURE: purchased batches/undimensioned features; never silently exact.
    rod_d: float = 6.0                 # specified concept stock; verify batch OD
    rod_fit_bore: float = 5.95          # D nominal press lands; coupon sets actual
    rod_density: float = 1.90          # g/cm3, weigh cut 500 mm rod
    cell_d: float = 18.33              # S5 18.33 +/- .07; verify wrapped sample
    cell_l: float = 64.85              # S5 64.85 +/- .15
    cell_mass: float = 45.0            # S5 max45 g, conservative mass nominal
    cell_terminal_d: float = 6.0       # MEASURE: terminal details absent from S5 envelope
    cell_terminal_h: float = .35       # MEASURE: included in total cell length
    cell_insulator_d: float = 14.4     # MEASURE: cosmetic positive-end washer
    cell_insulator_t: float = .12      # MEASURE: washer thickness
    sg_case_l: float = 22.7            # S3 drawing B; product envelope text rounds23
    sg_case_w: float = 12.2            # S3 drawing D
    sg_case_h: float = 27.0            # S3 drawing C, excluding output spline
    sg_tabs_span: float = 32.3         # S3 drawing E
    sg_tab_z: float = 17.0             # S3 drawing F relative to case bottom
    sg_tab_t: float = 2.0              # MEASURE: not dimensioned on S3 drawing
    sg_hole_pitch: float = 27.5        # MEASURE: hole centres, not tab envelope
    sg_hole_d: float = 2.0             # MEASURE: bought servo tab holes
    sg_axis_from_end: float = 5.9      # MEASURE: spline centre offset
    sg_spline_d: float = 4.8           # MEASURE: original horn used, no printed spline
    sg_spline_teeth: int = 21          # MEASURE: SG90 batch-dependent
    sg_spline_h: float = 3.3           # S3 A-C =30.3-27.0
    sg_screw_d: float = 1.6            # MEASURE: actual factory output screw thread
    sg_gear_cap_h: float = 4.3         # MEASURE: stepped case from S3 manufacturer photo
    sg_gear_cap_r: float = 5.7         # MEASURE: undimensioned S3 case bulge
    sg_rear_cap_r: float = 3.2         # MEASURE: secondary bulge
    sg_rear_cap_h: float = 3.0         # MEASURE: secondary bulge height
    sg_case_corner_r: float = 1.0      # MEASURE: cosmetic molded edge radius
    sg_spline_groove_w: float = .35    # MEASURE: cosmetic spline grooves, original horn used
    horn_l: float = 27.0              # MEASURE: supplied double arm
    horn_w: float = 5.2               # MEASURE: widest arm envelope
    horn_t: float = 1.6               # MEASURE: arm plate thickness
    horn_boss_d: float = 7.0          # MEASURE: boss below arm
    horn_boss_h: float = 3.8          # MEASURE: spline engagement
    horn_pin_pitch: float = 18.0      # MEASURE: ream two holes +/-9 for M2 drive pins
    mic_board_w: float = 14.0         # MEASURE: generic round/flat breakout variant
    mic_board_l: float = 16.0         # MEASURE: generic variant has no manufacturer CAD
    mic_board_t: float = 1.0          # MEASURE: breakout PCB thickness
    mic_port_d: float = 1.0           # MEASURE: PCB sound hole; chip port S6=.25
    mic_port_x_offset: float = 0.0    # MEASURE: centre from breakout centre
    mic_pad_row_span: float = 11.0     # MEASURE: generic breakout pad centres
    mic_pad_pitch: float = 4.5         # MEASURE: generic breakout pad pitch
    mic_mass: float = 1.0             # MEASURE: complete soldered breakout
    xiao_mass: float = 2.2            # MEASURE populated XIAO, no headers
    wio_mass: float = 1.8             # MEASURE populated extension, no headers
    stack_spacing: float = 7.5        # MEASURE XIAO CAD datum to Wio PCB bottom
    fpc_l: float = 100.0              # MEASURE kit FPC LoRa antenna, not a whip
    fpc_w: float = 10.0               # MEASURE kit antenna batch
    fpc_t: float = .30                # MEASURE laminate envelope
    fpc_mass: float = .8              # MEASURE FPC, coax and U.FL
    wifi_l: float = 20.0              # MEASURE supplied WiFi/BLE FPC
    wifi_w: float = 6.0               # MEASURE supplied WiFi/BLE FPC
    wifi_mass: float = .35            # MEASURE FPC and coax
    stake_d: float = 10.0             # MEASURE single stake OD parameter, 8..13mm
    stake_burial: float = 100.0        # D hand insertion, set mic using actual soil
    ballast_density: float = 7.85     # MEASURE solid steel; weigh actual fill
    petg_density: float = 1.27         # MEASURE: filament density, modeled solid PETG
    petg_modulus: float = 1600.0       # MPa engineering estimate; printed coupon needed
    printed_allowable_strain: float = .015 # D conservative screening limit, not material certification
    wire_od: float = 1.05             # MEASURE: insulated 28AWG wire
    prop_plane_from_bottom_plate: float = 57.0 # MEASURE: fitted prop shoulder in S1 +Y frame
    prop_sweep_thickness: float = 4.0 # MEASURE: vertical blade-swept slab

M=Measurements()
ROD_L=500.0                           # fixed concept; square end at500
TIP_L=12.0                            # D blunt .6 mm tip, sharpen by abrasion
ROD_Z=5.2                             # D rod centre above body print datum
CELL_Y=16.5; CELL_Z=11.6               # D beside spine; cradle opening upwards
CELL_X0=78.0                          # D cell nose 8 mm behind soil stop
BODY_X0=70.0                         # fixed concept soil stop
WALL=1.6                             # D 4 lines at .4 nozzle; .2 layers
SNAP_T=1.2; SNAP_L=18.0; SNAP_H=6.8    # D axial cantilevers, 3 lines thick
SNAP_MOUTH=16.8                      # D two relaxed retention lip edges
POD_X0=480.0; POD_TRAY_X0=536.0; POD_X1=582.0
POD_W=32.0; POD_BOTTOM=-.8; POD_SEAM=17.0
POD_BOARD_X=550.0; POD_BOARD_Z=3.0     # S4 PCB datum, USB points +X
MIC_X=570.0; MIC_Z=8.0; MIC_Y=-14.0  # D mic500mm above soil
FPC_X0=584.0; FPC_Z=POD_SEAM+2.0
INSERT_HOLE=3.2; INSERT_OD=3.6; INSERT_L=4.0 # Ruthex RX-M2x4 manufacturer CAD
POD_SCREWS=((540.0,-11),(540.0,11),(576.0,11)) # D leave mic corner clear
PLATE_T=3.2; PLATE_R=83.0              # D plate deck printed on back face
BEARING_RI=48.0; BEARING_RO=51.0; BEARING_Z=12.0
BEARING_FILM_T=.09                    # S8 3M5490 TDS total thickness; verify tape sample
ROTOR_R=64.9; ROTOR_T=3.2; ROTOR_TOP=BEARING_Z+ROTOR_T
HORN_Z=BEARING_Z-2.2                  # D stock horn arm bottom, .6mm below bearing
M2_NUT_AF=4.0; M2_NUT_T=1.6          # ISO4032/DIN934 M2; AF is across flats
M2_NUT_CIRC=M2_NUT_AF/(3**.5/2)      # CadQuery polygon() takes circumscribed diameter
M2_TRAP_CIRC=4.3/(3**.5/2)            # D .30mm across-flats clearance
PILOT_R=16.0; PILOT_CLEAR=.25          # D radial sliding clearance, outside stock double horn
HEAD_D=13.0; NECK_D=5.0; HEAD_T=3.2
HEAD_BOTTOM=50.0                      # D in dart coordinates; carries on rotor top
HEAD_R=68.0; GAP_DEG=20.0; STEP_DEG=16.0
RAIL_AXIS=72.0                       # D offset below drone from interference solve
RAIL_D=10.0; RAIL_SPACING=60.0         # S1 STEP spacing60; S1 OD9.4 vs catalog10 -> conservative10
SADDLE_X=(-85.0,60.0)                 # D free zones between vendor clamps/platforms
DRONE_DZ=85.0                         # S1 rail centre -13 ->72
PROP_D=260.0                          # S2 drawing says260 (conservative vs nominal10in)
GROUND_Z=-130.2764334894              # S1 lowest stock skid +85
BED=(245.0,245.0,260.0)                # Vyper specified in user project context

def measure_dict():return asdict(M)

def power_wire_paths():
    # D: terminal tabs -> strain-relieved external gutter -> rod -> pod gland.
    positive=[(CELL_X0+M.cell_l+.15,CELL_Y,11.6),(146.5,CELL_Y,11.6),(151,4.3,4.8),(478,4.3,4.8),(485,3,4.8),(510,3,4.8),(536,3,2),(558,3,2),(560.8,4.7,2.2),(560.8,4.7,2.7)]
    negative=[(CELL_X0-.18,CELL_Y,11.6),(75,22.5,11.6),(75,29,4.6),(148,29,4.6),(153,5.7,4.8),(478,5.7,4.8),(485,5,4.8),(510,5,4.8),(536,5,2),(559,6.5,2),(563.3,6.5,2),(563.3,4.7,2.7)]
    return [positive,negative]
