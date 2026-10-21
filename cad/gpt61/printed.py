"""Manufacturable prototype geometry, independent of the old v2/v3 scripts.

Design dimensions live here or parameters.py; bought dimensions cite S1-S7 there.
No global draft applied to FDM fits. Raised gussets taper at 45 degrees, internal
bores have teardrop roofs, and entry chamfers provide the useful FDM equivalent.
"""
import math
import cadquery as cq
from parameters import *
from geometry import *

def body(hanger,hanger_y=0.):
    end=hanger+11
    # Flat 1.6 mm sole and 11.2 mm-wide rod spine, rounded exterior edges.
    s=rounded(end-BODY_X0,11.2,10.8,2.0,at=((BODY_X0+end)/2,0,0))
    # The lateral CG offset needs a fully supported root station: its flat
    # foundation extends below both gussets, rather than suspending their tips
    # beside/beyond the narrow sleeve. Cut the rod/wire voids through it below.
    station=rounded(35,hanger_y+10.1,10.8,2,at=(hanger-6.5,(hanger_y-1.1)/2,0))
    s=s.fuse(station)
    # Seat is a real 1.6mm semicircular wall truncated below the cell equator.
    r=(M.cell_d+.50)/2
    seat=cyl(r+WALL,M.cell_l+8,(74,CELL_Y,CELL_Z),(1,0,0))
    seat=seat.intersect(box(90,40,8.4,at=(111,CELL_Y,0)))
    seat=seat.cut(cyl(r,M.cell_l+.7,(CELL_X0-.35,CELL_Y,CELL_Z),(1,0,0)))
    sole=rounded(M.cell_l+8,28,1.6,2,at=(74+(M.cell_l+8)/2,12,0))
    s=union(s,seat,sole)
    gutter=rounded(75,6.4,6.8,1.2,at=(111.5,28.5,0))
    gutter=gutter.cut(box(78,1.8,5,at=(111.5,29,3.8)))
    s=s.fuse(gutter)
    for x in (84,132):s=s.fuse(box(3.2,6.4,1.2,at=(x,28.5,6.2)))
    # End walls take axial landing load, not the slender fingers. Wire pockets
    # isolate the bought nickel tabs from PETG and prevent direct cell soldering.
    for x in (75.3,CELL_X0+M.cell_l+1.5):
        stop=rounded(2.6,21.8,13.0,1.1,at=(x,CELL_Y,0))
        stop=stop.cut(box(3.2,8,4,at=(x,CELL_Y,9)))
        s=s.fuse(stop)
    # Four independently relieved axial cantilevers. Root r=.8, tip lead-in
    # slopes outwards 45 deg, a horizontal lower face retains the cell.
    for root in (89.0,121.0):
        for sign in (-1,1):
            y=CELL_Y+sign*(r+.6)
            arm=rounded(SNAP_L+1.6,SNAP_T,SNAP_H,.48,at=(root+SNAP_L/2-.8,y,9.1))
            rootblock=rounded(3.2,3.0,10,0.8,at=(root-1,y,5.1))
            yl=CELL_Y+sign*SNAP_MOUTH/2
            yo=y+sign*SNAP_T/2
            # Profile is normal to X, cell insertion downward along Z.
            lip=cq.Workplane('YZ',origin=(root+SNAP_L-3.2,0,0)).polyline([
                (yl,15.9),(yo,15.9),(yo,19.1),(yl,17.1)]).close().extrude(3.2).val()
            s=union(s,rootblock,arm,lip)
    # Shaped webs below cradle at its ends tie the offset cell into the spine.
    for x in (81,113,143):
        web=cq.Workplane('YZ',origin=(x-1.2,0,0)).polyline([(3,1),(25,1),(25,4),(7,8)]).close().extrude(2.4).val()
        s=s.fuse(web)
    # Recut the real cell envelope after adding structural webs/root blocks.
    s=s.cut(cyl(r,M.cell_l+.7,(CELL_X0-.35,CELL_Y,CELL_Z),(1,0,0)))
    # Horizontal through-bore and three short press lands; the remainder has
    # .35 mm diameter clearance. Upper slot makes the fit locally compliant.
    s=s.cut(teardrop_x(BODY_X0-1,end-BODY_X0+2,(M.rod_d+.35)/2,0,ROD_Z))
    for x in (79,157,end-6):
        band=box(4,9.8,9.5,at=(x,0,.5)).cut(teardrop_x(x-3,6,M.rod_fit_bore/2,0,ROD_Z))
        s=s.fuse(band)
    s=s.cut(box(end-76,0.8,6,at=((76+end)/2,0,8.0)))
    # Hanger base is tapered both along and across the rod; neck carries in
    # tension, broad root spreads load into the continuous sleeve.
    post=rounded(14,9.0,33.6,2,at=(hanger,hanger_y,9.8))
    lateral=cq.Workplane('YZ',origin=(hanger-7,0,0)).polyline([(-4.8,9),(hanger_y+4.5,9),(hanger_y,26)]).close().extrude(14).val()
    post=post.fuse(lateral)
    post=post.fuse(cone(4.5,NECK_D/2,4,(hanger,hanger_y,41.6)))
    post=post.fuse(cyl(NECK_D/2,HEAD_BOTTOM-44,(hanger,hanger_y,44)))
    head=cyl(HEAD_D/2,HEAD_T,(hanger,hanger_y,HEAD_BOTTOM))
    head=chamfer(head,'>Z',.65)
    # Small root fillet is on the stem cone junction, generous gusset below.
    for side in (-1,1):
        run=22 if side<0 else 10 # aft gusset ends inside the flat root station
        g=cq.Workplane('XZ',origin=(0,hanger_y+2.2,0)).polyline([(hanger,11),(hanger+side*run,10),(hanger,36)]).close().extrude(4.4).val()
        g=cq.Workplane().add(g).edges().chamfer(.35).val()
        post=post.fuse(g)
    s=union(s,post,head)
    # Open power-wire gutter along +Y, plus a strain relief tie bridge at exit.
    s=s.cut(box(end-147,3.7,5.8,at=((147+end)/2,5.1,2.3)))
    relief=rounded(9,10,7,1.2,at=(end-13,5,1))
    relief=relief.cut(box(3.2,12,2,at=(end-13,5,3)))
    relief=relief.cut(teardrop_x(end-20,15,(M.rod_d+.35)/2,0,ROD_Z))
    s=s.fuse(relief)
    s=s.cut(box(end-148,3.7,4.4,at=((148+end)/2,5.1,4.1)))
    # Lead-in cones on press fit opening.
    s=s.cut(cone(M.rod_d/2+.65,M.rod_fit_bore/2,1.0,(BODY_X0,0,ROD_Z),(1,0,0)))
    # Dedicated wire reliefs are cut AFTER all webs: no buried pinched cable.
    for path in power_wire_paths():s=s.cut(pipe_path(path,.82))
    return s.clean()

def pod_shell():
    # Compact 44x32 tray, with a narrow closed socket neck to put mic at500mm.
    L=POD_X1-POD_TRAY_X0;cx=(POD_TRAY_X0+POD_X1)/2
    s=rounded(L,POD_W,POD_SEAM-POD_BOTTOM,4,at=(cx,0,POD_BOTTOM))
    s=s.cut(rounded(L-2*WALL,POD_W-2*WALL,20,2.4,at=(cx,0,POD_BOTTOM+WALL)))
    neck=rounded(POD_TRAY_X0-POD_X0+3,13.6,12.8,2,at=((POD_X0+POD_TRAY_X0+3)/2,0,POD_BOTTOM))
    neck=neck.cut(teardrop_x(479,21.2,(M.rod_d+.15)/2,0,ROD_Z))
    # Hollow riser after rod stop; accessible wire duct, 45degree bore roof.
    neck=neck.cut(teardrop_x(500,40,3.6,0,ROD_Z))
    s=s.fuse(neck)
    s=s.cut(teardrop_x(479,21.1,(M.rod_d+.15)/2,0,ROD_Z))
    s=s.cut(cone(3.75,3.075,1.4,(480,0,ROD_Z),(1,0,0)))
    rim=rounded(L,POD_W,2,4,at=(cx,0,POD_SEAM-2))
    rim=rim.cut(rounded(L-5,POD_W-5,2.3,1.5,at=(cx,0,POD_SEAM-2.1)))
    s=s.fuse(rim)
    groove=rounded(L-1,POD_W-1,.9,3.5,at=(cx,0,POD_SEAM-.9))
    groove=groove.cut(rounded(L-4,POD_W-4,1.1,2,at=(cx,0,POD_SEAM-1)))
    for x,y in POD_SCREWS:
        boss=cyl(3.3,POD_SEAM-POD_BOTTOM-WALL,(x,y,POD_BOTTOM+WALL))
        boss=boss.cut(cyl(INSERT_HOLE/2,5.2,(x,y,POD_SEAM-5.2)))
        boss=boss.cut(cone(1.6,1.85,.5,(x,y,POD_SEAM-.5)))
        s=s.fuse(boss)
    # Supports contact the XIAO underside edge only; no castellated pins fitted.
    for x in (555,565):
        for y in (-8.3,8.3):s=s.fuse(rounded(3,1,1.95,.35,at=(x,y,.8)))
    for y in (-9.7,9.7):
        for x in (554,566):s=s.fuse(rounded(4,1,3.6,.35,at=(x,y,.8)))
    # Five direct soldered I2S wires stay in the clear side aisle.
    s=s.cut(cyl(2,5,(MIC_X,-18,MIC_Z),(0,1,0)))
    s=s.cut(cyl(4.3,.65,(MIC_X,-14.6,MIC_Z),(0,-1,0)))
    for dx in (-M.mic_board_l/2-.8,M.mic_board_l/2+.8):
        s=s.fuse(box(1.2,3.6,M.mic_board_w+1.4,at=(MIC_X+dx,-13.7,MIC_Z-M.mic_board_w/2-.5)))
    hood=cq.Workplane('XY').workplane(offset=MIC_Z-5.5).polyline([
        (MIC_X+4,-15.4),(MIC_X+10,-15.4),(MIC_X+10,-21.4),(MIC_X+8.4,-21.4),(MIC_X+4,-17)]).close().extrude(11).val()
    s=s.fuse(hood)
    for x in (489,525):
        anchor=box(3,5,5,at=(x,4.5,.8)).cut(box(4,3,1.6,at=(x,4.5,2)))
        s=s.fuse(anchor)
    # Removable end cap exposes USB and both buttons to a pin from +X.
    opening=rounded(14,19,5,1.2).rotate((0,0,0),(0,1,0),90)
    b=opening.BoundingBox()
    opening=opening.translate((POD_X1-2-b.xmin,0,8.5-(b.zmin+b.zmax)/2))
    s=s.cut(opening)
    # LoRa coax gland sits above microphone, clear of removable service cap.
    s=s.cut(cyl(1.1,5,(577,-11.5,14.4),(1,0,0)))
    for path in power_wire_paths():s=s.cut(pipe_path(path,.82))
    return s.cut(groove).clean()

def pod_lid():
    L=POD_X1-POD_TRAY_X0;cx=(POD_TRAY_X0+POD_X1)/2
    s=rounded(L,POD_W,2,4,at=(cx,0,POD_SEAM))
    lip=rounded(L-5.6,POD_W-5.6,1.4,1.2,at=(cx,0,POD_SEAM-1.4))
    lip=lip.cut(rounded(L-8,POD_W-8,1.6,.6,at=(cx,0,POD_SEAM-1.5)))
    for x,y in POD_SCREWS:lip=lip.cut(cyl(3.65,3,(x,y,POD_SEAM-2)))
    lip=lip.cut(box(24,8,3,at=(MIC_X,-15,POD_SEAM-2)))
    lip=lip.cut(box(7,22,3,at=(579,0,POD_SEAM-2)))
    s=s.fuse(lip)
    for x,y in POD_SCREWS:
        s=s.cut(cyl(1.2,5,(x,y,POD_SEAM-2)))
        s=s.cut(cyl(2.1,1,(x,y,POD_SEAM+1)))
    # Wio PCB-edge foam pads at z12.1..13.1; no pressure on RF can.
    for x in (557,565):
        for y in (-8.3,8.3):s=s.fuse(rounded(3,1,3.9,.35,at=(x,y,13.1)))
    s=s.fuse(rounded(5,1.5,1.5,.4,at=(MIC_X,-12.7,15.5)))
    # Integral light FPC backer: no metal whip, no SMA fitting, no OLED window.
    support=rounded(FPC_X0+M.fpc_l+2-572, max(12,M.fpc_w+2),1.2,1,at=((572+FPC_X0+M.fpc_l+2)/2,0,17.8))
    for x in (590,FPC_X0+M.fpc_l-8):
        for y in (-4,4):support=support.cut(box(3,1.4,3,at=(x,y,17)))
    s=s.fuse(support)
    return s.clean()

def usb_cap():
    # End-access cover with shallow locating skirt; seal with removable RTV.
    outer=rounded(16.4,21.4,1.6,1.8)
    skirt=rounded(13.4,18.4,1.8,1.0,at=(0,0,-1.8))
    skirt=skirt.cut(rounded(10.2,15.2,2, .7,at=(0,0,-1.9)))
    s=outer.fuse(skirt)
    s=s.rotate((0,0,0),(0,1,0),90)
    b=s.BoundingBox()
    return s.translate((POD_X1,0,8.5-(b.zmin+b.zmax)/2))

def stake_adapter():
    # Two 90deg V saddles take any8..13mm stake using independent zip ties.
    # Datums match dart: stand_transform puts microphone at500mm, adapter at430.
    s=rounded(44,35,5,2,at=(502,15,-4))
    for x in (489,515):
        block=box(8,18,13,at=(x,26,0))
        v=cq.Workplane('YZ',origin=(x-5,0,0)).polyline([(17,14),(26,5),(35,14)]).close().extrude(10).val()
        block=block.cut(v)
        for y in (17.8,34.2):block=block.cut(box(3.2,3.2,8,at=(x,y,-5)))
        s=s.fuse(block)
    mount=rounded(24,14,9,1.6,at=(492,0,-4))
    mount=mount.cut(teardrop_x(479,26,3.2,0,ROD_Z))
    s=s.fuse(mount)
    # Separate6mm fibreglass offcut is held here and in the unchanged pod socket.
    for x in (486,497):s=s.cut(box(3.2,17,2.2,at=(x,0,-1)))
    s=s.translate((-32,0,0))
    s=s.cut(box(60,16,18,at=(509,0,-2)))
    for x in (457,483):
        s=s.cut(box(3.2,44,1.4,at=(x,26,-4)))
        s=s.cut(box(3.2,3.2,9,at=(x,14.5,-4)))
    s=s.cut(box(3.2,46,1.4,at=(490,13,-2))) # separate pod-retention tie
    return s.clean()

def stake_cell_holder():
    # Reuse exactly the qualified-by-geometry snap cradle; no hanger/spine tail.
    s=body(180,5).intersect(box(81,44,25,at=(110,15,0)))
    s=s.fuse(rounded(62,39,3,2,at=(110,43,0)))
    for x in (84,136):
        block=box(8,18,13,at=(x,56,0))
        v=cq.Workplane('YZ',origin=(x-5,0,0)).polyline([(47,14),(56,5),(65,14)]).close().extrude(10).val()
        s=s.fuse(block.cut(v))
        s=s.cut(box(3.2,44,1.4,at=(x,56,-.2)))
        s=s.cut(box(3.2,3.2,4,at=(x,44.5,-.2)))
    return s.clean()

def dummy_body(hanger,hanger_y):
    # Real body's exterior/hanger retained; closed ballast cartridge replaces cell.
    s=body(hanger,hanger_y)
    s=s.cut(box(78,34,25,at=(111,22.5,1.5)))
    cartridge=rounded(70,20,18.6,2,at=(111,CELL_Y,1.4))
    s=s.fuse(cartridge)
    # Two independent axial ballast stations set both mass and longitudinal CG.
    for x in (92,130):s=s.cut(rounded(24,15,16.4,1.5,at=(x,CELL_Y,3.6)))
    # Screw-retained common lid, captiveM2 nuts reached from below.
    for x in (77,145):
        s=s.fuse(cyl(4,8.4,(x,CELL_Y,11.6)))
        s=s.cut(cyl(1.1,11,(x,CELL_Y,10.6)))
        trap=cq.Workplane('XY').workplane(offset=16.4).center(x,CELL_Y).polygon(6,M2_TRAP_CIRC).extrude(1.8).val()
        s=s.cut(trap)
        s=s.cut(box(4.3,14,1.8,at=(x,22,16.4))) # side-load captive nut
    return s.clean()

def dummy_lid():
    s=rounded(77,21,2,2,at=(111,CELL_Y,20))
    for x in (77,145):s=s.cut(cyl(1.2,4,(x,CELL_Y,19)))
    return s.clean()

def head_positions():
    a=math.degrees(math.asin(22/HEAD_R))
    b=math.degrees(math.asin(62/HEAD_R))
    angles=[a,180-b,180+a,360-b]
    return [(HEAD_R*math.cos(math.radians(t)),HEAD_R*math.sin(math.radians(t)),t) for t in angles]

def release_steps():return [16.,48.,32.,64.]

def gap_angles():return [p[2]-t for p,t in zip(head_positions(),release_steps())]

def plate():
    s=cyl(PLATE_R,PLATE_T,(0,0,-PLATE_T))
    # Large radiused lightening pockets leave a continuous perimeter and
    # radial 8mm webs; surface ring transfers the load directly into this deck.
    for a in (45,135,225,315):
        cut=sector(24,42,a,55,-PLATE_T-1,PLATE_T+2)
        s=s.cut(cut)
    ridge=cyl(BEARING_RO,BEARING_Z-BEARING_FILM_T).cut(cyl(BEARING_RI,BEARING_Z+1))
    ridge=chamfer(ridge,'>Z',.3)
    s=s.fuse(ridge)
    # Low central pilot carries radial load. Servo/horn stay loose vertically.
    pilot=cyl(PILOT_R,BEARING_Z).cut(cyl(14.4,BEARING_Z+1))
    s=s.fuse(pilot)
    # Servo case clears a real offset rectangular pocket; tabs attach below.
    off=M.sg_case_l/2-M.sg_axis_from_end
    s=s.cut(rounded(M.sg_case_l+.7,M.sg_case_w+.7,PLATE_T+10,1,
        at=(-off,0,-PLATE_T-1)))
    for sign in (-1,1):
        x=-off+sign*M.sg_hole_pitch/2
        boss=cyl(4.0,PLATE_T,(x,0,-PLATE_T)).cut(cyl(1.1,PLATE_T+2,(x,0,-PLATE_T-1)))
        # Top-accessible hex trap for DIN934 M2 nut, supported by thin floor.
        nut=cq.Workplane('XY').workplane(offset=-1.4).center(x,0).polygon(6,M2_TRAP_CIRC).extrude(1.5).val()
        boss=boss.cut(nut)
        s=s.fuse(boss)
    # Recut through the common deck after fusion, so no nut pockets refill.
    for sign in (-1,1):
        x=-off+sign*M.sg_hole_pitch/2
        s=s.cut(cyl(1.1,10,(x,0,-8)))
        s=s.cut(cq.Workplane('XY').workplane(offset=-1.4).center(x,0).polygon(6,M2_TRAP_CIRC).extrude(1.6).val())
    for x,y,t in head_positions():
        # Entire 13mm head and 14x9 tapered root can pass through.
        slot=rounded(20.4,15.4,PLATE_T+2,2.4,at=(x,y,-PLATE_T-1))
        s=s.cut(slot)
    # Four ribbed towers at verified free rail locations, not through the
    # stock battery board or optional forward platform. Includes tie tunnels.
    for x in SADDLE_X:
        for y in (-RAIL_SPACING/2,RAIL_SPACING/2):
            ybase=y+(24 if y>0 else -24) if x>0 else y
            s=s.fuse(rounded(18,18,PLATE_T,2.5,at=(x,ybase,-PLATE_T)))
            # 4mm walls, 1.5deg taper over the vertical load path.
            outer=cq.Workplane('XY').center(x,ybase).rect(11.8,13.8).workplane(offset=RAIL_AXIS-3).center(0,y-ybase).rect(8.2,10.2).loft().val()
            # Windows remove the tall core but leave end walls connected.
            core=cq.Workplane('XY').workplane(offset=5).center(x,ybase+(y-ybase)*5/(RAIL_AXIS-3)).rect(4.2,5.6).workplane(offset=RAIL_AXIS-23).center(0,(y-ybase)*(RAIL_AXIS-23)/(RAIL_AXIS-3)).rect(3.0,4.4).loft().val()
            outer=outer.cut(core)
            saddle=rounded(8.2,14.4,9,1.5,at=(x,y,RAIL_AXIS-8))
            saddle=saddle.cut(cyl(RAIL_D/2+.3,12,(x-6,y,RAIL_AXIS),(1,0,0)))
            tower=union(outer,saddle)
            tower=tower.cut(cyl(RAIL_D/2+.3,16,(x-8,y,RAIL_AXIS),(1,0,0)))
            # 2.5x1 T18R band, including its curved corner, has a 3.1x3.2
            # tunnel opening through the saddle below the rod.
            tower=tower.cut(box(3.1,18,3.2,at=(x,y,RAIL_AXIS-8.0)))
            s=s.fuse(tower)
            # Gussets stay within x free zones at height of vendor boards.
            for side in (-1,1):
                rib=cq.Workplane('YZ',origin=(x-1.4,0,0)).polyline([
                    (ybase,1),(ybase+side*15,1),(ybase+(y-ybase)*27/(RAIL_AXIS-3),27)]).close().extrude(2.8).val()
                s=s.fuse(rib)
            # Base beam ties the outboard saddle to deck.
            s=s.fuse(bar((x,ybase),(x*.75,ybase),9,-PLATE_T,PLATE_T+1.6))
    # Printed route to the rear for the servo lead; no loose loop at rotor.
    cable=bar((-22,-10),(-62,-10),6,0,2.2)
    s=s.fuse(cable)
    s=s.cut(box(42,3.4,1.6,at=(-42,-10,.3)))
    s=s.cut(rounded(4.0,4.0,8,1,at=(-24,-10,-PLATE_T-1)))
    # Recut pockets after fusing bosses; the case must clear the inner boss faces.
    s=s.cut(rounded(M.sg_case_l+.7,M.sg_case_w+.7,18,1,at=(-off,0,-8)))
    # Stock splayed 16mm legs cross the edge of the plate. Two radiused open
    # notches provide 1.5+mm radial clearance without cutting the bearing ring.
    for sy in (-1,1):s=s.cut(rounded(21,35,9,3,at=(0,sy*83,-6)))
    for x,y,t in head_positions():
        s=s.cut(rounded(20.4,15.4,10,2.4,at=(x,y,-PLATE_T-1)))
    return s.clean()

def rotor():
    # 3.2mm web with six radiused windows and continuous bearing annulus.
    s=cyl(ROTOR_R,ROTOR_T,(0,0,BEARING_Z))
    for a in range(0,360,60):s=s.cut(sector(20,43,a,42,BEARING_Z-1,ROTOR_T+2))
    for a in gap_angles():s=s.cut(sector(56,ROTOR_R+2,a,GAP_DEG,BEARING_Z-1,ROTOR_T+2))
    # The printed pilot has .25mm radial and .3mm bottom clearance.
    hub=cyl(19.2,6.0,(0,0,BEARING_Z-2.8))
    hub=hub.cut(cyl(PILOT_R+PILOT_CLEAR,3.1,(0,0,BEARING_Z-3.0)))
    s=s.fuse(hub)
    # Clearance well for the stock horn and spline screw. Two vertical slots
    # engage round drive pins on the horn; rotor lifts off for service. No
    # rigid axial screw couples dart weight back into the servo shaft.
    s=s.cut(cyl(4.2,9,(0,0,BEARING_Z-3.5)))
    for x in (-M.horn_pin_pitch/2,M.horn_pin_pitch/2):
        s=s.cut(cyl(1.22,8,(x,0,BEARING_Z-3)))
        s=s.cut(cyl(2.6,4.35,(x,0,BEARING_Z-3))) # clearance for real M2 hex upper nut, .35mm axial
    # Horn arm sits below the hub at z=5.8..7.4, with .6mm roof clearance.
    pocket=rounded(M.horn_l+.8,M.horn_w+.8,2.5,2,at=(0,0,BEARING_Z-3))
    s=s.cut(pocket)
    return s.clean()

def fit_coupon():
    # Four short coaxial-bore blocks joined by a single 1.6 mm raft; layout
    # gives a real independent press fit, not four overlapping holes.
    blocks=[]
    for i,d in enumerate((5.9,6.0,6.1,6.2)):
        x=i*15
        b=rounded(10,11.2,10.8,1.5,at=(x,0,0))
        b=b.cut(teardrop_x(x-6,12,d/2,0,ROD_Z))
        b=b.cut(box(12,.8,4,at=(x,0,8)))
        blocks.append(b)
    return union(*blocks,box(55,2,1.2,at=(22.5,-5,0)))

def dummy_head_insert():
    s=rounded(23,17.8,7,1,at=(560,0,3))
    for x in (554,566):s=s.cut(rounded(8,15,6, .8,at=(x,0,4.2)))
    return s.clean()
