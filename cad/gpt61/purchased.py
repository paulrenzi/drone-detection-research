"""Bought components, with sources in parameters.py and sources/manifest.json.

Original manufacturer B-reps are retained at 1:1 scale. Details absent from a
manufacturer CAD file have explicit MEASURE parameters rather than false precision.
"""
from pathlib import Path
import math
import cadquery as cq
from geometry import *
from parameters import *

ROOT=Path(__file__).resolve().parent

def cached_asset(stem):
    p=ROOT/'sources'/(stem+'.brep')
    if p.exists():return cq.Shape.importBrep(str(p))
    s=cq.importers.importStep(str(ROOT/'sources'/(stem+'.step'))).val()
    s.exportBrep(str(p))
    return s

def rod():
    return union(cone(.30,M.rod_d/2,TIP_L,(0,0,ROD_Z),(1,0,0)),
        cyl(M.rod_d/2,ROD_L-TIP_L,(TIP_L,0,ROD_Z),(1,0,0)))

def cell():
    # S5 can: total envelope includes the .35mm raised positive terminal.
    r=M.cell_d/2
    can=cyl(r,M.cell_l-M.cell_terminal_h,(CELL_X0,CELL_Y,CELL_Z),(1,0,0))
    can=chamfer(can,'%Circle',.18)
    positive=cyl(M.cell_terminal_d/2,M.cell_terminal_h,(CELL_X0+M.cell_l-M.cell_terminal_h,CELL_Y,CELL_Z),(1,0,0))
    washer=cyl(M.cell_insulator_d/2,M.cell_insulator_t,(CELL_X0+M.cell_l-M.cell_terminal_h-.02,CELL_Y,CELL_Z),(1,0,0)).cut(cyl(M.cell_terminal_d/2+.1,.4,(CELL_X0+M.cell_l-.5,CELL_Y,CELL_Z),(1,0,0)))
    return [('cell_wrap',can,'cell'),('positive_terminal',positive,'metal'),('positive_insulator',washer,'white')]

def heltec():
    # S4 detailed V3.7 manufacturer STEP: PCB and all connector/chip placements.
    # It omits the OLED glass; add it using the V3 physical drawing and MEASURE
    # module thickness/height. Original non-exact CAD remains as reference only.
    s=cached_asset('heltec-v3.7')
    rows=[]
    for i,a in enumerate(s.Solids()):
        if a.Volume()<.003:continue  # omit decal/zero-volume silkscreen solids only
        col='board' if i==0 else 'metal' if i in (2,171) else 'oled'
        rows.append((f'heltec_cad_{i:03}',a.translate((POD_BOARD_X,0,POD_BOARD_Z)),col))
    # Both 18-way header rows exist as plated through holes in vendor PCB.
    # The supplied long male strips are left unsoldered for this enclosure.
    # Gold rings show that interface explicitly; .025mm plating is cosmetic.
    for side in (-1,1):
        for j in range(18):
            x=POD_BOARD_X+j*2.54
            ring=cyl(.85,.04,(x,side*11.43,POD_BOARD_Z+.01)).cut(cyl(.51,.08,(x,side*11.43,POD_BOARD_Z)))
            rows.append((f'header_pad_{side}_{j}',ring,'gold'))
    oled=rounded(M.oled_l,M.oled_w,M.oled_t,.65,at=(POD_BOARD_X+33.56,0,POD_BOARD_Z+M.oled_z))
    rows.append(('oled_glass',oled,'oled'))
    active=box(M.oled_active_l,M.oled_active_w,.05,at=(POD_BOARD_X+33.56,0,POD_BOARD_Z+M.oled_z+M.oled_t)) # MEASURE active area
    rows.append(('oled_active',active,(.15,.33,.40)))
    # Two adhesive foam strips below the glass represent its real spacer.
    for y in (-7,7):rows.append((f'oled_spacer_{y}',box(28,2,1.4,at=(POD_BOARD_X+33.56,y,POD_BOARD_Z+M.oled_z-1.4)),'gasket'))
    return rows

def microphone():
    # Generic breakout is not standardized: outer dimensions/port location are
    # MEASURE. Bare INMP441 can is S6 4.72 x3.76 x1.00, bottom port .25 dia.
    board=rounded(M.mic_board_l,M.mic_board_w,M.mic_board_t,1.2)
    # Build PCB in XY, then rotate it upright to make its bottom face look -Y.
    board=board.cut(cyl(M.mic_port_d/2,3,(M.mic_port_x_offset,0,-1)))
    parts=[('mic_pcb',board,'board')]
    # S6 outline Fig16: port centre is 1.07mm from the package right edge,
    # i.e. +1.29mm from package centre. Offset can so its port aligns to PCB.
    chip=box(4.72,3.76,1.0,at=(M.mic_port_x_offset-1.29,0,M.mic_board_t))
    chip=chamfer(chip,'>Z',.1)
    chip=chip.cut(cyl(.125,.20,(M.mic_port_x_offset,0,M.mic_board_t-.05)))
    parts.append(('INMP441_can',chip,'metal'))
    # Six plated solder pads; direct wires, supplied pin headers not fitted.
    for x in (-M.mic_pad_row_span/2,M.mic_pad_row_span/2):
        for z in (-M.mic_pad_pitch,0,M.mic_pad_pitch):
            pad=cyl(.8,.05,(x,z,-.02)).cut(cyl(.45,.15,(x,z,-.05)))
            parts.append((f'mic_pad_{x}_{z}',pad,'gold'))
    # This rotation maps local +Z thickness to +Y (interior).
    return [(n,s.rotate((0,0,0),(1,0,0),-90).translate((MIC_X,-15.8,MIC_Z)),c) for n,s,c in parts]

def m2_insert(x,y,z):
    # Actual Ruthex manufacturer CAD is used instead of a featureless cylinder.
    s=cached_asset('ruthex-m2x4')
    b=s.BoundingBox()
    s=s.translate((-(b.xmin+b.xmax)/2,-(b.ymin+b.ymax)/2,-b.zmin))
    return s.translate((x,y,z))

def screw(d,L,p=(0,0,0),head=3.8,head_h=1.5):
    # Purchased metric screw envelope: ISO4762-ish socket head, threads shown
    # as major-diameter cylinders for honest interference and practical file size.
    shaft=cyl(d/2,L,p)
    h=cyl(head/2,head_h,(p[0],p[1],p[2]+L))
    socket=cq.Workplane('XY').workplane(offset=p[2]+L+head_h-.75).center(p[0],p[1]).polygon(6,d*.85).extrude(1).val()
    return union(shaft,h.cut(socket))

def dart_hardware():
    parts=[]
    for i,(x,y) in enumerate(POD_SCREWS):
        parts.append((f'pod_insert_{i}',m2_insert(x,y,POD_SEAM-4.1),'gold'))
        parts.append((f'pod_M2x6_{i}',screw(2,6,(x,y,POD_SEAM-5),head=3.8,head_h=2.0),'metal'))
    # Closed1.2mm cord in1.5 wide x.9 deep gland ->25% squeeze,84% fill.
    # Rectangular-equivalent compressed section .9x1.26 conserves cord area.
    L=POD_X1-POD_X0
    g=rounded(L-1.24,POD_W-1.24,.9,4.38,at=((POD_X0+POD_X1)/2,0,POD_SEAM-.9))
    g=g.cut(rounded(L-3.76,POD_W-3.76,1.1,3.12,at=((POD_X0+POD_X1)/2,0,POD_SEAM-1)))
    parts.append(('perimeter_silicone_seal',g,'gasket'))
    # TDK AN1124 soft membrane with cavity: .05mm silicone prototype film,
    # diameter8, supported outside central4mm cavity; acoustic response to test.
    parts.append(('mic_waterproof_film',cyl(4.0,.05,(MIC_X,-16.65,MIC_Z),(0,1,0)),'gasket'))
    micseal=cyl(3.8,.8,(MIC_X,-16.6,MIC_Z),(0,1,0)).cut(cyl(2,.9,(MIC_X,-16.65,MIC_Z),(0,1,0)))
    parts.append(('mic_silicone_cavity_seal',micseal,'gasket'))
    # Compression pads only on PCB edge strips, outside OLED span.
    for x in (513,548):
        for y in (-11.65,11.65):parts.append((f'board_retention_foam_{x}_{y}',box(4,1.5,2.25,at=(x,y,2.25)),'gasket'))
    # Factory spot-welded nickel tabs, not soldering iron on the cell can.
    for x in (CELL_X0-.18,CELL_X0+M.cell_l):
        tab=box(.15,5,9,at=(x,CELL_Y,7.2))
        parts.append((f'nickel_tab_{x}',tab,'metal'))
    # Whip, axial boot, and lead to the actual U.FL area on vendor board.
    parts.append(('whip',cyl(M.whip_d/2,M.whip_l,(POD_X1,0,7),(1,0,0)),'wire'))
    parts.append(('whip_boot',cyl(M.whip_base_d/2,M.whip_boot_l,(POD_X1-M.whip_boot_l/2,0,7),(1,0,0)),'wire'))
    # Actual U.FL of V3.7 is at top of PCB; curved pigtail avoids OLED.
    parts.append(('RF_pigtail',pipe_path([(550.5,0,3.2),(554,3,4.3),(554,3,7),(POD_X1,0,7)],.565),'wire'))
    # Two insulated 28AWG power wires in the gutter and alongside rod. Short
    # local service loops modeled; mass calculation includes bought connector.
    for i,points in enumerate(power_wire_paths()):
        parts.append((f'power_wire_{i}',pipe_path(points,M.wire_od/2),'red' if i==0 else 'wire'))
    # Rod wire ties use S7 band dimensions, are trimmed after closing.
    for x in (320,420):parts+=zip_tie_x(x,1.5,ROD_Z,10.0,6.8,name=f'rod_tie_{x}')
    # Power lead strain relief around the body sleeve, clear of cell flexures.
    parts+=zip_tie_x(163,.6,5.4,14.4,12.8,name='body_strain_relief_tie')
    return parts

def zip_tie_x(x,y,z,span_y,span_z,name='tie'):
    # S7 T18R: width2.5 thickness1 head4.8x4.45x3.7, minimum80N.
    # Fitted loop conservatively rectangular with radius3; top has locking head.
    outer=rounded(span_y+2,span_z+2,2.5,min(3,(span_y+2)/3))
    inner=rounded(span_y,span_z,3, max(.5,min(2,span_y/3)),at=(0,0,-.2))
    loop=outer.cut(inner).rotate((0,0,0),(0,1,0),90).rotate((0,0,0),(1,0,0),90)
    b=loop.BoundingBox();loop=loop.translate((x-(b.xmin+b.xmax)/2,y-(b.ymin+b.ymax)/2,z-(b.zmin+b.zmax)/2))
    head=rounded(4.8,4.45,3.7,1,at=(x,y+span_y/2+1,z+span_z/2-1))
    return [(name,compound([loop,head]),'wire')]

def sg90():
    # S3 axes: shaft at origin, tabs top=-7.2; case dimensions central M.
    off=M.sg_case_l/2-M.sg_axis_from_end
    bottom=-PLATE_T-M.sg_tab_z-M.sg_tab_t
    case=rounded(M.sg_case_l,M.sg_case_w,M.sg_case_h-M.sg_gear_cap_h,M.sg_case_corner_r,at=(-off,0,bottom))
    # Real stepped upper gear bulge, seam at the three-section case joints.
    cap=cyl(M.sg_gear_cap_r,M.sg_gear_cap_h,(0,0,bottom+M.sg_case_h-M.sg_gear_cap_h))
    cap=cap.fuse(cyl(M.sg_rear_cap_r,M.sg_rear_cap_h,(-5,0,bottom+M.sg_case_h-M.sg_rear_cap_h)))
    case=case.fuse(cap)
    for z in (bottom+3.8,bottom+M.sg_case_h-5.0):
        seam=rounded(M.sg_case_l+.1,M.sg_case_w+.1,.25,.8,at=(-off,0,z))
        inner=rounded(M.sg_case_l-.5,M.sg_case_w-.5,.5,.5,at=(-off,0,z-.1))
        case=case.cut(seam.cut(inner))
    tab=rounded(M.sg_tabs_span,M.sg_case_w,M.sg_tab_t,1,at=(-off,0,bottom+M.sg_tab_z))
    for sign in (-1,1):tab=tab.cut(cyl(M.sg_hole_d/2,4,(-off+sign*M.sg_hole_pitch/2,0,bottom+M.sg_tab_z-1)))
    case=case.fuse(tab)
    # Spline grooves are explicitly represented (M tooth count/OD). The stock
    # moulded horn, not a PETG copy of this spline, is used in the mechanism.
    spline=cyl(M.sg_spline_d/2,M.sg_spline_h,(0,0,bottom+M.sg_case_h))
    for i in range(M.sg_spline_teeth):
        tooth=box(M.sg_spline_groove_w,M.sg_spline_groove_w,M.sg_spline_h+.2,at=(M.sg_spline_d/2,0,bottom+M.sg_case_h-.1)).rotate((0,0,0),(0,0,1),i*360/M.sg_spline_teeth)
        spline=spline.cut(tooth)
    spline=spline.cut(cyl(.8,4,(0,0,bottom+M.sg_case_h)))
    horn=rounded(M.horn_l,M.horn_w,M.horn_t,2.2,at=(0,0,HORN_Z))
    boss=cyl(M.horn_boss_d/2,M.horn_boss_h,(0,0,HORN_Z-M.horn_boss_h)).cut(cyl(M.sg_spline_d/2+.05,3.2,(0,0,HORN_Z-M.horn_boss_h-.1)))
    horn=horn.fuse(boss).cut(cyl(1.0,7,(0,0,HORN_Z-4)))
    for sign in (-1,1):
        for distance in (6,9,12):horn=horn.cut(cyl(.6,3,(sign*distance,0,HORN_Z-.5)))
    # Reamed +/-9mm holes receive M2 screws as round dogs. Captive M2 nuts
    # under the supplied horn retain them; long shanks are free axially.
    for x in (-M.horn_pin_pitch/2,M.horn_pin_pitch/2):
        horn=horn.cut(cyl(1.0,3,(x,0,HORN_Z-.5)))
    parts=[('SG90_case_tabs',case,'servo'),('SG90_output_spline',spline,'white'),('SG90_stock_double_horn',horn,'horn')]
    # A positive keeper, with .4mm gap above rotor, prevents axial bounce-out.
    # Spacer clamps the stock horn; static payload remains on the plate ridge.
    # Thread of the longer replacement screw MUST match the measured servo.
    parts.append(('SG90_spline_screw',screw(M.sg_screw_d,10.0,(0,0,ROTOR_TOP+.8-10),head=3.1,head_h=1.1),'metal'))
    spacer=cyl(1.5,4.2,(0,0,HORN_Z+M.horn_t)).cut(cyl((M.sg_screw_d+.2)/2,4.4,(0,0,HORN_Z+M.horn_t-.1)))
    keeper=cyl(5,.4,(0,0,ROTOR_TOP+.4)).cut(cyl((M.sg_screw_d+.25)/2,.6,(0,0,ROTOR_TOP+.3)))
    parts.extend([('rotor_keeper_spacer',spacer,'metal'),('rotor_keeper_washer',keeper,'metal')])
    for x in (-M.horn_pin_pitch/2,M.horn_pin_pitch/2):
        dog=cyl(1.0,9.7,(x,0,HORN_Z-2.3))
        nut=cq.Workplane('XY').workplane(offset=HORN_Z-1.6).center(x,0).polygon(6,M2_NUT_CIRC).extrude(M2_NUT_T).val().cut(cyl(.85,2,(x,0,HORN_Z-1.8)))
        topnut=nut.translate((0,0,3.2))
        parts.extend([(f'drive_pin_{x}',dog,'metal'),(f'drive_pin_lower_nut_{x}',nut,'metal'),(f'drive_pin_upper_nut_{x}',topnut,'metal')])
    for sign in (-1,1):
        x=-off+sign*M.sg_hole_pitch/2
        nut=cq.Workplane('XY').workplane(offset=-1.4).center(x,0).polygon(6,M2_NUT_CIRC).extrude(M2_NUT_T).val().cut(cyl(.85,2,(x,0,-1.5)))
        sc=screw(2,6.0,(x,0,0),head=3.8,head_h=2.0).rotate((x,0,0),(x+1,0,0),180).translate((0,0,.8))
        parts.extend([(f'servo_mount_nut_{sign}',nut,'metal'),(f'servo_M2x6_{sign}',sc,'metal')])
    # Three-color cable/plug routed out the fixed deck's rear channel.
    for i,col in enumerate(('wire','red','body')):
        parts.append((f'servo_lead_{i}',pipe_path([(-off-M.sg_case_l/2, i-1,bottom+3),(-24,-10+i-1,-7),(-24,-10+i-1,.8),(-65,-10+i-1,.8)],.5),col))
    parts.append(('servo_JR_plug',rounded(8,7.5,3,1,at=(-69,-10,-.7)),'wire'))
    return parts

def drone():
    raw=cached_asset('x500v2-frame')
    seen=set();rows=[];duplicates=[]
    for i,a in enumerate(raw.Solids()):
        b=xyz_bounds(a)
        key=tuple(round(v,3) for v in b)+(round(a.Volume(),2),)
        if key in seen:duplicates.append(i);continue
        seen.add(key)
        # S1 +Y is up; transform to +Z, preserving fore/aft rail direction X.
        s=a.rotate((0,0,0),(1,0,0),90).translate((0,0,DRONE_DZ))
        if 2<=i<=33:cat='landing_gear'
        elif 142<=i<=175:cat='payload_rails_clamps'
        elif i in (56,83,110,137,188,189,190,191):cat='motors'
        else:cat='frame'
        col='metal' if a.Volume()<450 else 'carbon'
        if i in (158,159):col='metal'
        if cat=='motors':col='metal'
        rows.append((f'x500_{cat}_{i:03}',s,col))
    # S2 actual prop outline260mm (not254mm nominal); MEASURE4mm swept slab.
    # Nominal shoulder is57mm above the lower centre plate in the OEM frame.
    motor_xy=[(-177.101,177.102),(-177.102,-177.101),(177.101,-177.102),(177.102,177.101)]
    for i,(x,y) in enumerate(motor_xy):rows.append((f'prop_swept_{i}',cyl(PROP_D/2,M.prop_sweep_thickness,(x,y,M.prop_plane_from_bottom_plate+DRONE_DZ)),'prop'))
    return rows,duplicates
