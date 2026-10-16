"""v2: half the parts, half the cost.

DART: one 6 mm fibreglass rod is spike, spine and mast. A printed body holds the
cell low, a printed clip slid to the balance point is the hanger, and the head pod
sits on the rod's top end. No hinge, spring, bolt, pole sections or shock cord.
Carried FLAT under the drone, so it needs no tall legs; falls and must turn
point-down in the air (T10 tests that).

HARNESS: one plate, one rotor, ONE servo. Each dart's clip comes up through a
slot in the plate; its round head rests on the rotor's rim. The rim has one gap
per dart, at a different angle for each: turn the servo to the next step and the
next dart's gap comes round under its head, and that dart drops. The darts'
weight goes rotor -> ridge -> plate; the servo only turns the rotor.

Dart frame: rod along Z, tip at z=0, cell on the +Y side (up when hung).
Harness frame: plate top at z=0, centre at the servo shaft, darts along X, tips aft (-X).
"""
import math
import itertools
import cadquery as cq
from params import *

# ---- dart ------------------------------------------------------------------------
RD, RL = 6.0, 500.0        # rod: 6 x 500 mm solid fibreglass (Amazon listing; MEASURE the batch)
TIP_L = 12.0               # point sanded on the rod's front end
SPIKE = 70.0               # bare rod ahead of the body: the most that goes into soil
WALL = 1.6
CELL_BORE = CELL_D + 0.8
YC = (RD + 0.3) / 2 + WALL + CELL_BORE / 2          # cell centre off the rod axis
NOSE = 15.0                # solid front of the body, chamfered
BODY_L = NOSE + CELL_L + 3.0
POD_OD, POD_L, SOCKET = 32.0, 92.0, 28.0   # thin shell round the upright Heltec (27.5 mm diagonal)
CLIP_L, CLIP_W = 20.0, 12.0                          # hanger post footprint (along rod x across)
HEAD_D, NECK_D, HEAD_H = 12.0, 5.0, 3.5

# ---- harness -----------------------------------------------------------------------
PT = 3.0                   # plate thickness
SHAFT_ABOVE_TAB = SERVO[2] - SERVO_TAB_Z - SERVO_TAB_T   # 12.6: tab top to spline top (MEASURE)
SHAFT_OFF = SERVO[0] / 2 - 5.9                       # shaft ~5.9 mm from the case end (MEASURE)
RZ = -PT + SHAFT_ABOVE_TAB + 1.0                     # rotor underside = horn top (ESTIMATE; sand the ridge to match)
RT = 3.0                   # rotor thickness
RT_TONGUE = 62.0           # radius of the clip heads
RR = RT_TONGUE - NECK_D / 2 - 0.6                    # rotor radius: rim sits 0.6 mm off the neck
RIDGE = (46.0, 49.0)       # bearing ring under the rotor rim (inner, outer radius)
GAP_DEG = 20.0             # gap width in the rim
STEP_D = 16.0              # servo step between drops: drop k at k * 16 deg
DROP_ORDER = (0, 2, 1, 3)  # alternate sides so the load stays balanced
# heads: 4 positions on the circle, chosen so the darts sit 40 mm apart across the drone
TONGUE_DEG = [math.degrees(a) for a in (math.asin(20 / RT_TONGUE), math.pi - math.asin(60 / RT_TONGUE),
                                        math.pi + math.asin(20 / RT_TONGUE), 2 * math.pi - math.asin(60 / RT_TONGUE))]
ROD_Z = -PT - 2.0 - (YC + CELL_BORE / 2 + WALL)       # hung rod axis: body top 2 mm under the plate
CRADLE = (10.0, 14.0, 23.0)                          # rail posts: x, y, height (rail sits in a groove on top)
PLATE_R = 78.0             # disc that carries the slots
PLATE_X = 184.0            # bars out to the rail posts


def rod():
    r = cq.Workplane("XY").workplane(offset=TIP_L).circle(RD / 2).extrude(RL - TIP_L)
    return r.union(cq.Solid.makeCone(0.6, RD / 2, TIP_L))


def body():
    """Cell holder, slid onto the rod from the tip. Cell goes in from the back; a zip tie
    through the two side holes closes the bay."""
    b = (cq.Workplane("XY").circle(RD / 2 + 0.15 + WALL).extrude(BODY_L)
         .union(cq.Workplane("XY").center(0, YC).circle(CELL_BORE / 2 + WALL).extrude(BODY_L))
         .union(cq.Workplane("XY").center(0, YC / 2).rect(2 * (RD / 2 + WALL), YC).extrude(BODY_L)))
    b = b.cut(cq.Workplane("XY").circle((RD + 0.3) / 2).extrude(BODY_L))
    b = b.cut(cq.Workplane("XY").workplane(offset=NOSE).center(0, YC).circle(CELL_BORE / 2).extrude(BODY_L))
    b = b.cut(cq.Workplane("YZ").workplane(offset=-20).center(YC, BODY_L - 1.8).rect(3.0, 1.6).extrude(40))
    # nose: chamfer the front so it parts soil instead of slapping it
    b = b.cut(cq.Workplane("YZ").workplane(offset=-20)
              .polyline([(YC + CELL_BORE / 2 + WALL + 1, -1), (YC + CELL_BORE / 2 + WALL + 1, 14), (RD / 2 + WALL, -1)])
              .close().extrude(40))
    return b.translate((0, 0, SPIKE))


def clip_post_h():
    """Height of the post from the rod axis to the rotor's underside, when hung."""
    return (RZ - 0.3) - ROD_Z


def clip(z0=0.0):
    """Hanger: sleeve on the rod, a post up through the plate, a neck at the rotor, a round head
    on top. Round neck and head: the same clip works at every position on the rotor."""
    h = clip_post_h()
    c = cq.Workplane("XY").circle(CLIP_W / 2).extrude(CLIP_L)
    c = c.union(cq.Workplane("XY").center(0, h / 2).rect(CLIP_W, h).extrude(CLIP_L))
    c = c.cut(cq.Workplane("XY").circle((RD + 0.3) / 2).extrude(CLIP_L))
    nh = (cq.Workplane("XY").circle(NECK_D / 2).extrude(RT + 0.6)
          .faces(">Z").workplane().circle(HEAD_D / 2).extrude(HEAD_H).faces(">Z").edges().chamfer(0.8))
    c = c.union(nh.rotate((0, 0, 0), (1, 0, 0), -90).translate((0, h, CLIP_L / 2)))
    return c.translate((0, 0, z0 - CLIP_L / 2))


def pod():
    """Thin shell: a cone from the rod socket up to a tube round the board, domed top."""
    cone = cq.Solid.makeCone(7.0, POD_OD / 2, SOCKET)
    tube = (cq.Workplane("XY").workplane(offset=SOCKET).circle(POD_OD / 2).extrude(POD_L - SOCKET)
            .faces(">Z").edges().fillet(8))
    shell = tube.union(cq.Workplane().add(cone))
    shell = shell.cut(cq.Workplane("XY").workplane(offset=SOCKET + 1.5).circle(POD_OD / 2 - 1.8)
                      .extrude(POD_L - SOCKET - 3.3).edges(">Z").fillet(6))
    shell = shell.cut(cq.Workplane("XY").circle((RD + 0.3) / 2).extrude(SOCKET))
    shell = shell.cut(cq.Solid.makeCone(0.1, POD_OD / 2 - 3.5, SOCKET - 4).translate((0, 0, 4)))
    shell = shell.cut(cq.Workplane("XY").workplane(offset=POD_L - 8).circle(2.0).extrude(10))   # mic port / whip
    return shell.translate((0, 0, RL - SOCKET))


def extras():
    """Mic foam on top of the pod and the whip (for renders and the balance point)."""
    top = RL - SOCKET + POD_L
    return [(cq.Workplane("XY").sphere(8).translate((0, 0, top + 4)), "fur"),
            (cq.Workplane("XY").circle(0.8).extrude(82).translate((0, 0, top + 6)), "steel")]


M_MIC_FOAM = 4.0     # breakout + foam cover, no fur (ESTIMATE)
M_WIRE = 6.0         # 2 wires along the rod, whip, zip ties (ESTIMATE)


def masses(clip_z):
    """(mass g, centroid z) of every item. Printed parts at 60% of solid (ESTIMATE)."""
    def printed(s):
        v = s.val()
        return v.Volume() / 1000 * PETG * 0.6, v.Center().z
    r = rod().val()
    items = [(r.Volume() / 1000 * FIBREGLASS, r.Center().z), printed(body()), printed(clip(clip_z)), printed(pod())]
    items.append((M_CELL, SPIKE + NOSE + CELL_L / 2))
    pod_mid = RL - SOCKET + SOCKET + 2 + HELTEC[0] / 2
    items += [(M_HELTEC, pod_mid), (M_MIC_FOAM, RL - SOCKET + POD_L), (M_WIRE, RL / 2)]
    return items


def balance():
    """Slide the clip until it sits at the balance point: iterate, the clip moves the CG a little."""
    z = RL / 2
    for _ in range(6):
        it = masses(z)
        z = sum(m * c for m, c in it) / sum(m for m, _ in it)
    return z, sum(m for m, _ in masses(z))


CLIP_Z, DART_G = balance()


def dart(state="hung"):
    parts = [(rod(), "pole"), (body(), "print"), (clip(CLIP_Z), "print2"), (pod(), "print2")] + extras()
    return parts


# ---- harness -----------------------------------------------------------------------
def tongue_xy(i):
    a = math.radians(TONGUE_DEG[i])
    return RT_TONGUE * math.cos(a), RT_TONGUE * math.sin(a)


def to_harness(shape, i, drop=0.0):
    """Dart frame -> harness frame: dart Z -> +X, dart X -> +Y, dart Y -> +Z; clip head over tongue i."""
    s = shape.rotate((0, 0, 0), (1, 0, 0), 90).rotate((0, 0, 0), (0, 0, 1), 90)
    tx, ty = tongue_xy(i)
    return s.translate((tx - CLIP_Z, ty, ROD_Z - drop))


def plate():
    p = cq.Workplane("XY").workplane(offset=-PT).circle(PLATE_R).extrude(PT)
    for sy in (-1, 1):
        p = p.union(cq.Workplane("XY").workplane(offset=-PT).center(0, sy * X500_RAIL_SPACING / 2)
                    .rect(PLATE_X, CRADLE[1] + 4).extrude(PT).edges("|Z").fillet(4))
    p = p.union(cq.Workplane("XY").circle(RIDGE[1]).circle(RIDGE[0]).extrude(RZ))
    # servo: mounted from below, tabs on the underside, case top + shaft up through this pocket
    p = p.cut(cq.Workplane("XY").workplane(offset=-PT - 1).center(-SHAFT_OFF, 0)
              .rect(SERVO[0] + 0.6, SERVO[1] + 0.6).extrude(PT + 2))
    for s in (-1, 1):
        p = p.cut(cq.Workplane("XY").workplane(offset=-PT - 1).center(-SHAFT_OFF + s * 13.9, 0).circle(0.8).extrude(PT + 2))
    # lightening windows inside the ridge, either side of the servo
    for s in (-1, 1):
        p = p.cut(cq.Workplane("XY").workplane(offset=-PT - 1).circle(RIDGE[0] - 4).extrude(PT + 2)
                  .intersect(cq.Workplane("XY").workplane(offset=-PT - 1).center(0, s * 26).rect(90, 30).extrude(PT + 2)))
    # a slot per dart for the clip post
    for i in range(4):
        tx, ty = tongue_xy(i)
        p = p.cut(cq.Workplane("XY").workplane(offset=-PT - 1).center(tx, ty)
                  .rect(CLIP_L + 0.6, CLIP_W + 0.6).extrude(PT + 2))
    # rail posts: groove on top for the 10 mm rail, zip-tie hole through
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (PLATE_X / 2 - CRADLE[0] / 2 - 2), sy * X500_RAIL_SPACING / 2
            post = cq.Workplane("XY").center(x, y).rect(CRADLE[0], CRADLE[1]).extrude(CRADLE[2])
            post = post.cut(cq.Workplane("YZ").workplane(offset=x - 10).center(y, CRADLE[2] + 1)
                            .circle(X500_RAIL_D / 2 + 0.3).extrude(20))
            post = post.cut(cq.Workplane("XZ").workplane(offset=-y - 10).center(x, CRADLE[2] - 11)
                            .rect(4.5, 3.0).extrude(20))
            p = p.union(post)
    return p


def step_angles():
    """Drop k at k * STEP_D. Gap i sits STEP[i] behind its head. Margin = the closest any gap
    comes to a head it must still hold (0 = the gap edge touches the head's edge)."""
    head_half = math.degrees((HEAD_D + 0.6) / 2 / (RR - 2))
    step = [0.0] * 4
    for k, i in enumerate(DROP_ORDER):
        step[i] = STEP_D * (k + 1)
    gaps = [TONGUE_DEG[i] - step[i] for i in range(4)]
    margin = 999.0
    for i in range(4):
        for phi in [x / 2 for x in range(0, int(2 * step[i]) + 1)]:
            for j in range(4):
                if j == i and phi >= step[i] - STEP_D - 1e-9:
                    continue          # its own gap arriving: fine after the previous stop
                dist = abs((gaps[j] + phi - TONGUE_DEG[i] + 180) % 360 - 180)
                margin = min(margin, dist - GAP_DEG / 2 - head_half)
    return margin, step, gaps


MARGIN, STEP, GAP_AT = step_angles()


def rotor(phi=0.0):
    r = cq.Workplane("XY").workplane(offset=RZ).circle(RR).extrude(RT)
    for g in GAP_AT:
        w = cq.Workplane("XY").workplane(offset=RZ - 1).polyline(
            [(0, 0)] + [((RR + 5) * math.cos(math.radians(g + t)), (RR + 5) * math.sin(math.radians(g + t)))
                        for t in (-GAP_DEG / 2, 0, GAP_DEG / 2)]).close().extrude(RT + 2)
        r = r.cut(w.cut(cq.Workplane("XY").workplane(offset=RZ - 2).circle(RR - 8).extrude(RT + 4)))
    r = r.cut(cq.Workplane("XY").workplane(offset=RZ - 1).circle(1.6).extrude(RT + 2))       # horn screw
    for s in (-1, 1):                                                                       # horn arm screws
        r = r.cut(cq.Workplane("XY").workplane(offset=RZ - 1).center(s * 9, 0).circle(0.8).extrude(RT + 2))
    for k in range(6):                                                                      # windows inside the ridge
        a = math.radians(30 + 60 * k)
        r = r.cut(cq.Workplane("XY").workplane(offset=RZ - 1).center(26 * math.cos(a), 26 * math.sin(a))
                  .circle(9).extrude(RT + 2))
    return r.rotate((0, 0, 0), (0, 0, 1), phi)


def servo(phi=0.0):
    tab_top = -PT
    case = (cq.Workplane("XY").workplane(offset=tab_top - SERVO_TAB_T - SERVO_TAB_Z).center(-SHAFT_OFF, 0)
            .rect(SERVO[0], SERVO[1]).extrude(SERVO[2] - 4.0))
    tabs = cq.Workplane("XY").workplane(offset=tab_top - SERVO_TAB_T).center(-SHAFT_OFF, 0).rect(SERVO_TAB_SPAN, SERVO[1]).extrude(SERVO_TAB_T)
    horn = (cq.Workplane("XY").workplane(offset=RZ - 1.5).rect(30, 5).extrude(1.5)
            .rotate((0, 0, 0), (0, 0, 1), phi))
    return [(case.union(tabs), "servo"), (horn, "print2")]


def hung(i, drop=0.0):
    return [(to_harness(s, i, drop), c) for s, c in dart()]


def scene(phi=0.0, dropped=(), rails=True):
    parts = [(plate(), "print"), (rotor(phi), "print2")] + servo(phi)
    for i in range(4):
        if i in dropped:
            continue
        parts += hung(i)
    if rails:
        for s in (-1, 1):
            parts.append((cq.Workplane("YZ").circle(X500_RAIL_D / 2).extrude(X500_RAIL_L)
                          .translate((-X500_RAIL_L / 2, s * X500_RAIL_SPACING / 2, CRADLE[2] + 1)), "ghost"))
    return parts


def head_on_rim(i, phi):
    """Volume of rotor under dart i's head, projected down through the rotor plane. 0 = free."""
    tx, ty = tongue_xy(i)
    col = cq.Workplane("XY").workplane(offset=RZ - 1).center(tx, ty).circle(HEAD_D / 2).extrude(RT + 2)
    return rotor(phi).intersect(col).val().Volume()


def clash(a, b):
    try:
        return a.intersect(b).val().Volume()
    except Exception:
        return 0.0


if __name__ == "__main__":
    import pathlib
    from render import render
    out = pathlib.Path(__file__).parent / "out"
    img = pathlib.Path(__file__).parents[1] / "assets" / "images" / "build"
    for name, s in (("v2_dart_body", body()), ("v2_dart_clip", clip()), ("v2_dart_pod", pod()),
                    ("v2_plate", plate()), ("v2_rotor", rotor())):
        cq.exporters.export(s, str(out / f"{name}.stl"))
        cq.exporters.export(s, str(out / f"{name}.step"))
        bb = s.val().BoundingBox()
        print(name, "bbox", round(bb.xlen), round(bb.ylen), round(bb.zlen),
              "fits bed" if max(bb.xlen, bb.ylen) <= BED[0] and bb.zlen <= BED[2] else "TOO BIG",
              "~%.0f g" % (s.val().Volume() / 1000 * PETG * 0.6))
    print("dart mass ~%.0f g, clip at %.0f mm from the tip (dart %.0f mm long with pod)" % (DART_G, CLIP_Z, RL - SOCKET + POD_L))
    for m, c in masses(CLIP_Z):
        print("   %.1f g at z=%.0f" % (m, c))
    print("steps (deg from rest) per dart:", STEP, "gap centres:", [round(g, 1) for g in GAP_AT], "margin %.1f deg" % MARGIN)
    harness_g = (plate().val().Volume() + rotor().val().Volume()) / 1000 * PETG * 0.6 + M_SERVO
    print("harness ~%.0f g" % harness_g)
    # --- checks -------------------------------------------------------------------
    order = sorted(range(4), key=lambda i: STEP[i])
    for i in range(4):
        assert head_on_rim(i, 0) > 1.0, f"dart {i} not held at rest"
    for k, i in enumerate(order):
        held = [j for j in order[k + 1:]]
        for phi in range(0, int(STEP[i]) + 1):
            for j in held:
                assert head_on_rim(j, phi) > 1.0, f"dart {j} uncovered at {phi} deg"
        assert head_on_rim(i, STEP[i]) < 1e-6, f"dart {i} still held at its step {STEP[i]}"
    print("release: each dart held until its own step, free at it: OK")
    pl, rot = plate(), rotor()
    dz = [cq.Compound.makeCompound([s.val() for s, c in hung(i) if c != "fur"]) for i in range(4)]
    worst = 0.0
    for phi in range(0, int(max(STEP)) + 1, 4):
        r = rotor(phi)
        for i in range(4):
            worst = max(worst, clash(cq.Workplane().add(dz[i]), r))
    for i in range(4):
        worst = max(worst, clash(cq.Workplane().add(dz[i]), pl))
        sv = servo()[0][0]
        worst = max(worst, clash(cq.Workplane().add(dz[i]), sv))
        for j in range(i + 1, 4):
            worst = max(worst, clash(cq.Workplane().add(dz[i]), cq.Workplane().add(dz[j])))
    print("worst clash volume (dart vs rotor at every angle, plate, servo, other darts): %.3f mm3" % worst)
    allp = scene()
    bb = cq.Compound.makeCompound([s.val() for s, _ in allp]).BoundingBox()
    rail_axis = CRADLE[2] + 1
    print("hung footprint %d x %d mm; lowest point %.0f mm below the rail axis" % (bb.xlen, bb.ylen, rail_axis - bb.zmin))
    # --- renders ------------------------------------------------------------------
    first = order[0]
    sc = scene(STEP[first], dropped=(first,)) + [(s.translate((0, 0, -90)).rotate((0, 0, 0), (0, 0, 1), 0), c)
                                                 for s, c in hung(first)]
    render(sc, img / "v2-harness.png", elev=-18, azim=-58, size=(1300, 700), zoom=1.8)
    clips = [(to_harness(clip(CLIP_Z), i), "print2") for i in range(4)]
    render([(pl, "print"), (rotor(STEP[first]), "carbon")] + [c for k, c in enumerate(clips) if k != first],
           img / "v2-rotor.png", elev=60, azim=-90, size=(1000, 800), zoom=1.25)
    soil = cq.Workplane("XY").rect(120, 120).extrude(SPIKE)
    render(dart() + [(soil, "ghost")], img / "v2-dart.png", elev=8, azim=-60, size=(500, 1300), zoom=0.95)
