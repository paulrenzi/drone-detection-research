"""Release harness v1, the simple one: ONE printed plate, four SG90s dropped into
pockets shaft-down, zip-tied to the X500's two 10 mm rails. The servo horn arm IS
the latch: it sits in the side-open notch on each dart's tongue and swings out
90 degrees to drop it. No pins, pushrods, saddles, caps or M3 hardware.

Origin: drone centre, plate top at z=0, rails along X on the plate top. Units mm.
Print: plate flat, top face down. No supports.
"""
import math
import cadquery as cq
from params import *
import dart

PLATE = (150.0, 120.0, 5.0)
POCKET = (SERVO[0] + 0.4, SERVO[1] + 0.4)     # SG90 drops in, tabs rest on the plate
SERVO_BELOW = 18.0                             # case + shaft tower below the tabs (ESTIMATE; MEASURE)
HORN_Z = -PLATE[2] - SERVO_BELOW - 1.0          # horn arm plane
HORN_R = 14.0                                  # tongue engages the arm 14 mm out from the shaft
NOTCH_Y = 1.5                                  # notch centre offset on the tongue (dart.py)
SHAFT_OFF = SERVO[0] / 2 - 5.9                 # shaft ~5.9 mm from one end (ESTIMATE; MEASURE)
SERVOS = [(-38, -26, 180), (-38, 26, 180), (38, -26, 0), (38, 26, 0)]   # arms point outboard   # x, y of case centre, yaw


def plate():
    p = (cq.Workplane("XY").workplane(offset=-PLATE[2]).rect(PLATE[0], PLATE[1]).extrude(PLATE[2])
         .edges("|Z").fillet(10))
    for x, y, yaw in SERVOS:
        pocket = cq.Workplane("XY").workplane(offset=-PLATE[2] - 1).rect(*POCKET).extrude(PLATE[2] + 2)
        p = p.cut(pocket.rotate((0, 0, 0), (0, 0, 1), yaw).translate((x, y, 0)))
        for s in (-1, 1):   # 2 mm pilot holes for the servo's own tab screws
            hole = cq.Workplane("XY").workplane(offset=-PLATE[2] - 1).center(s * 13.9, 0).circle(0.8).extrude(PLATE[2] + 2)
            p = p.cut(hole.rotate((0, 0, 0), (0, 0, 1), yaw).translate((x, y, 0)))
    # zip-tie slots either side of each rail, rail spacing from params (MEASURE; slots are long)
    for s in (-1, 1):
        for x in (-62, -8, 46):
            for dy in (-9, 9):
                p = p.cut(cq.Workplane("XY").workplane(offset=-PLATE[2] - 1)
                          .center(x + 8, s * X500_RAIL_SPACING / 2 + dy).rect(4.5, 3).extrude(PLATE[2] + 2))
    return p


def servo_at(x, y, yaw, theta):
    """SG90 shaft-down; theta = horn angle, 0 = latched (arm pointing at the dart)."""
    case = (cq.Workplane("XY").workplane(offset=-PLATE[2] - SERVO_BELOW).rect(SERVO[0], SERVO[1]).extrude(SERVO[2]))
    tabs = cq.Workplane("XY").rect(SERVO_TAB_SPAN, SERVO[1]).extrude(SERVO_TAB_T)
    shaft = cq.Workplane("XY").workplane(offset=HORN_Z).center(SHAFT_OFF, 0).circle(2.4).extrude(-HORN_Z - PLATE[2] - SERVO_BELOW + 0.5)
    t = math.radians(theta)
    arm = (cq.Workplane("XY").workplane(offset=HORN_Z - 0.8).center(SHAFT_OFF, 0).circle(3.5).extrude(1.6)
           .union(cq.Workplane("XY").workplane(offset=HORN_Z - 0.8).center(SHAFT_OFF + (HORN_R + 4) / 2, 0)
                  .rect(HORN_R + 4, 4).extrude(1.6))
           .rotate((SHAFT_OFF, 0, 0), (SHAFT_OFF, 0, 1), theta))
    out = []
    for s, c in ((case.union(tabs), "servo"), (shaft, "steel"), (arm, "print2")):
        out.append((s.rotate((0, 0, 0), (0, 0, 1), yaw).translate((x, y, 0)), c))
    return out


def tongue_point(x, y, yaw):
    """Where the arm crosses the tongue when latched (theta = 0)."""
    a = math.radians(yaw)
    px, py = SHAFT_OFF + HORN_R, 0.0
    return x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)


def hung_dart(x, y, yaw, drop=0.0):
    tx, ty = tongue_point(x, y, yaw)
    parts = []
    for shape, col in dart.assembly("stowed"):
        sh = shape.translate((-dart.TONGUE_X, -NOTCH_Y, -dart.TONGUE_HOLE_Z))
        sh = sh.rotate((0, 0, 0), (0, 0, 1), yaw)           # arm passes through the tongue; notch opens toward the swing
        parts.append((sh.translate((tx, ty, HORN_Z - drop)), col))
    return parts


def scene(released=False, rails=True):
    parts = [(plate(), "print")]
    for i, (x, y, yaw) in enumerate(SERVOS):
        rel = released and i == 0          # show dart 1 dropping, the others still held
        parts += servo_at(x, y, yaw, 90 if rel else 0)
        parts += hung_dart(x, y, yaw, drop=60 if rel else 0)
    if rails:
        for s in (-1, 1):
            parts.append((cq.Workplane("YZ").circle(X500_RAIL_D / 2).extrude(X500_RAIL_L)
                          .translate((-X500_RAIL_L / 2, s * X500_RAIL_SPACING / 2, X500_RAIL_D / 2)), "ghost"))
    return parts


if __name__ == "__main__":
    import pathlib
    from render import render
    out = pathlib.Path(__file__).parent / "out"
    p = plate()
    cq.exporters.export(p, str(out / "harness_simple_plate.stl"))
    cq.exporters.export(p, str(out / "harness_simple_plate.step"))
    cq.exporters.export(dart.cap(), str(out / "dart_cap.stl"))
    cq.exporters.export(dart.cap(), str(out / "dart_cap.step"))
    bb = p.val().BoundingBox()
    print("plate", round(bb.xlen), round(bb.ylen), round(bb.zlen), "mass ~%.0f g" % (p.val().Volume() / 1000 * PETG * 0.6))
    allp = scene()
    bb = cq.Compound.makeCompound([s.val() for s, _ in allp]).BoundingBox()
    print("footprint", round(bb.xlen), "x", round(bb.ylen), "lowest z", round(bb.zmin))
    img = pathlib.Path(__file__).parents[1] / "assets" / "images" / "build"
    render(scene(released=True), img / "harness-simple.png", elev=-15, azim=-55, size=(1200, 900), zoom=1.15)
    # close-up of one latch: arm in the notch
    x, y, yaw = SERVOS[0]
    tx, ty = tongue_point(x, y, yaw)
    close = [(s, c) for s, c in servo_at(x, y, yaw, 0)] + [(dart.cap().translate((-dart.TONGUE_X, -NOTCH_Y, -dart.TONGUE_HOLE_Z))
             .rotate((0, 0, 0), (0, 0, 1), yaw).translate((tx, ty, HORN_Z)), "print")]
    render(close, img / "harness-simple-latch.png", elev=-10, azim=-30, size=(900, 700), zoom=1.3)
