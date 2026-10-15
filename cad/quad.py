"""Printed carrier quad v0 ("TL-1"): X500 electronics (2216 KV920 motors, 10 in
props, Pixhawk 6C, 4S pack) on a PETG frame sized for a 245 mm bed, with the
dart bay built into the hull. Also prints the payload / flight-time estimate.

Origin: hull centre, hull floor at z=0. Units mm.
"""
import math
import cadquery as cq
from params import *
import dart
import harness

WHEELBASE = 450.0                 # motor to motor diagonal; 10 in props clear (318 mm between neighbours)
HULL = (150.0, 130.0, 46.0)       # outer; one print
WALL = 2.4
ARM_W, ARM_H = 24.0, 20.0
ARM_ROOT_R = 70.0                 # radius where the arm enters the hull
LEG_L = 250.0                     # clears the hanging darts (lowest point ~219 mm below the release pin)
PROP_D = 254.0


def hull():
    h = (cq.Workplane("XY").rect(HULL[0], HULL[1]).extrude(HULL[2])
         .edges("|Z").fillet(18).faces(">Z").shell(-WALL))
    # arm sockets on the four corners
    for a in (45, 135, 225, 315):
        boss = (cq.Workplane("XY").rect(44, ARM_W + 2 * WALL + 2).extrude(ARM_H + 2 * WALL)
                .translate((ARM_ROOT_R, 0, 0)).rotate((0, 0, 0), (0, 0, 1), a))
        h = h.union(boss)
        sock = (cq.Workplane("XY").workplane(offset=WALL).rect(46, ARM_W + 0.4).extrude(ARM_H + 0.4)
                .translate((ARM_ROOT_R + 4, 0, 0)).rotate((0, 0, 0), (0, 0, 1), a))
        h = h.cut(sock)
    # dart bay: the four release blocks hang from the floor, same pattern as the X500 harness
    for gx in (-1, 1):
        for gy in (-1, 1):
            blk = (harness.release_block(gx * harness.GRID_X, gy * harness.GRID_Y, gx)
                   .translate((0, 0, -harness.PLATE_TOP + harness.PLATE[2])))
            h = h.union(blk)
    # floor windows for wiring and weight
    h = h.cut(cq.Workplane("XY").workplane(offset=-1).rect(40, 22).extrude(4).edges("|Z").fillet(4))
    return h


def arm():
    """One arm, printed flat. Box section, motor pad with 16x16 and 19x19 holes, leg socket below."""
    length = WHEELBASE / 2 - ARM_ROOT_R + 22
    a = (cq.Workplane("XY").rect(length, ARM_W).extrude(ARM_H)
         .faces(">Z").shell(-2.0)
         .translate((length / 2, 0, 0)))
    pad = cq.Workplane("XY").circle(19).extrude(5).translate((length, 0, ARM_H - 5))
    a = a.union(pad)
    for p in ((8, 8), (-8, 8), (8, -8), (-8, -8)):
        a = a.cut(cq.Workplane("XY").center(length + p[0], p[1]).circle(1.6).extrude(ARM_H + 1))
    for r in (9.5,):
        for ang in (0, 90, 180, 270):
            a = a.cut(cq.Workplane("XY").center(length + r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang)))
                      .circle(1.6).extrude(ARM_H + 1))
    a = a.cut(cq.Workplane("XY").center(length, 0).circle(4.5).extrude(ARM_H + 1))     # motor shaft clearance
    leg_sock = cq.Workplane("XY").workplane(offset=-14).circle(9).extrude(14).translate((length - 20, 0, 0))
    a = a.union(leg_sock).cut(cq.Workplane("XY").workplane(offset=-14).circle(6.2).extrude(13).translate((length - 20, 0, 0)))
    return a.translate((ARM_ROOT_R - 18, 0, WALL))


def leg():
    """Printed leg: 12 mm tube with a foot. Breaks before the arm does (intended)."""
    l = cq.Workplane("XY").circle(6).extrude(LEG_L).faces("<Z").workplane().circle(14).extrude(4)
    return l


def assembly():
    parts = [(hull(), "print")]
    length = WHEELBASE / 2 - ARM_ROOT_R + 22
    for a in (45, 135, 225, 315):
        parts.append((arm().rotate((0, 0, 0), (0, 0, 1), a), "print2"))
        lx = ARM_ROOT_R - 18 + length - 20
        parts.append((leg().translate((lx, 0, WALL - 14 - LEG_L)).rotate((0, 0, 0), (0, 0, 1), a), "print2"))
        mx = ARM_ROOT_R - 18 + length
        motor = cq.Workplane("XY").circle(14).extrude(26).translate((mx, 0, WALL + ARM_H))
        prop = cq.Workplane("XY").circle(PROP_D / 2).extrude(1.5).translate((mx, 0, WALL + ARM_H + 30))
        parts.append((motor.rotate((0, 0, 0), (0, 0, 1), a), "carbon"))
        parts.append((prop.rotate((0, 0, 0), (0, 0, 1), a), "ghost"))
    pin_z = -harness.PLATE_TOP + harness.PLATE[2] + harness.PIN_Z
    for gx in (-1, 1):
        for gy in (-1, 1):
            for s, c in harness.stowed_dart(gx * harness.GRID_X, gy * harness.GRID_Y, gx):
                parts.append((s.translate((0, 0, pin_z - harness.PIN_Z)), c))
    return parts


def frame_mass_g():
    vol = hull().val().Volume() + 4 * arm().val().Volume() + 4 * leg().val().Volume()
    return vol / 1000.0 * PETG * 0.75     # thin walls print near solid: ESTIMATE


# ---- flight time ---------------------------------------------------------------
# Hover power scales as mass^1.5 for fixed props (momentum theory). Anchor: Holybro's
# 18 min hover, no payload, 4S 5000 mAh. The X500's all-up weight with that pack is not
# published; 1.6-1.8 kg is OUR ESTIMATE (610 g frame + ~500 g pack + motors, ESCs, FC, GPS).
def hover_min(auw_g, anchor_auw_g, anchor_min=18.0):
    return anchor_min * (anchor_auw_g / auw_g) ** 1.5


if __name__ == "__main__":
    import pathlib
    from render import render
    out = pathlib.Path(__file__).parent / "out"
    for name, fn in (("quad_hull", hull), ("quad_arm", arm), ("quad_leg", leg)):
        s = fn()
        cq.exporters.export(s, str(out / f"{name}.stl"))
        cq.exporters.export(s, str(out / f"{name}.step"))
        bb = s.val().BoundingBox()
        print(name, "bbox", round(bb.xlen), round(bb.ylen), round(bb.zlen),
              "fits bed" if max(bb.xlen, bb.ylen) <= BED[0] and bb.zlen <= BED[2] else "TOO BIG")
    fm = frame_mass_g()
    dm = dart.mass_g()["total"]
    harness_g = 4 * M_SERVO + 110        # plate, saddles, blocks, pins: ESTIMATE
    print(f"printed frame ~{fm:.0f} g vs X500 frame 610 g; dart ~{dm:.0f} g; X500 harness ~{harness_g:.0f} g")
    print("| Carrier | Darts | AUW (kg) | Hover (min) | Reach out, 20% reserve, 10 m/s (km) |")
    for anchor in (1600, 1800):
        for label, base, h in (("X500 V2 + harness", anchor, harness_g), ("Printed TL-1", anchor - 610 + fm, 0)):
            for n in (2, 3, 4):
                auw = base + h + n * dm
                t = hover_min(auw, anchor)
                reach = t * 0.8 * 60 * 10 / 2 / 1000
                print(f"| {label} (anchor {anchor/1000:.1f} kg) | {n} | {auw/1000:.2f} | {t:.1f} | {reach:.1f} |")
    img = pathlib.Path(__file__).parents[1] / "assets" / "images" / "build"
    render(assembly(), img / "quad-tl1.png", elev=18, azim=-55, size=(1200, 1000), zoom=1.2)
