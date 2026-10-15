"""Release harness v0 for the Holybro X500 V2: one printed plate clamped to the
two 10 mm payload rails, four pin-puller releases (one SG90 each, on Pixhawk 6C
AUX 1-4), four stowed darts hanging upright in a 2 x 2 grid.

Origin: drone centre, rail centrelines at z=0, X forward. Units mm.
"""
import cadquery as cq
from params import *
import dart

PLATE = (210.0, 120.0, 4.0)
PLATE_TOP = -X500_RAIL_D / 2 - 3.0          # saddles lift the rails 3 mm off the plate
BLOCK = (26.0, 16.0, 20.0)                  # release block under the plate
PIN_Z = PLATE_TOP - PLATE[2] - BLOCK[2] / 2
SLOT_W = 5.0                                # tongue is 4 thick
GRID_X, GRID_Y = 52.0, 21.0                 # tongue positions: (+-GRID_X, +-GRID_Y)


def plate():
    p = (cq.Workplane("XY").workplane(offset=PLATE_TOP - PLATE[2])
         .rect(PLATE[0], PLATE[1]).extrude(PLATE[2]).edges("|Z").fillet(8))
    # rail clamp slots: 4 x M3, slide 40-90 mm rail spacing (spacing not published: MEASURE)
    for x in (-80, 80):
        for s in (-1, 1):
            p = p.cut(cq.Workplane("XY").workplane(offset=PLATE_TOP - 10)
                      .center(x, s * 32.5).slot2D(25, 3.4, 90).extrude(20))
    # lightening windows between the release blocks
    p = p.cut(cq.Workplane("XY").workplane(offset=PLATE_TOP - 10)
              .rect(50, 26).extrude(20).edges("|Z").fillet(5))
    return p


def saddle(y):
    """Rail cradle: sits on the plate, grooved for the 10 mm rod; a printed cap screws over it."""
    s = (cq.Workplane("XY").workplane(offset=PLATE_TOP).rect(22, 18).extrude(X500_RAIL_D / 2 + 3)
         .cut(cq.Workplane("YZ").workplane(offset=-15).circle(X500_RAIL_D / 2 + 0.2).extrude(30)))
    cap = (cq.Workplane("XY").workplane(offset=0).rect(22, 18).extrude(X500_RAIL_D / 2 + 3)
           .cut(cq.Workplane("YZ").workplane(offset=-15).circle(X500_RAIL_D / 2 + 0.2).extrude(30)))
    return s.translate((0, y, 0)).union(cap.translate((0, y, 0)))


def release_block(x, y, flip):
    """Slot takes the dart tongue from below; a 3 mm steel pin crosses the slot along X."""
    b = (cq.Workplane("XY").workplane(offset=PLATE_TOP - PLATE[2] - BLOCK[2])
         .rect(BLOCK[0], BLOCK[1]).extrude(BLOCK[2]).edges("|Z").fillet(2))
    b = b.cut(cq.Workplane("XY").workplane(offset=PLATE_TOP - PLATE[2] - BLOCK[2] - 1)
              .rect(SLOT_W, 10.0).extrude(BLOCK[2] - 3))
    b = b.cut(cq.Workplane("YZ").workplane(offset=-20).center(0, PIN_Z).circle(1.65).extrude(40))
    return b.translate((x, y, 0))


def servo(x, y, flip):
    """SG90 hanging from the plate beside its block; horn drives a pushrod to the pin."""
    sx = x + flip * 30
    body = (cq.Workplane("XY").workplane(offset=PLATE_TOP - PLATE[2] - SERVO[1])
            .rect(SERVO[2] * 0.73, SERVO[0]).extrude(SERVO[1]))
    tabs = (cq.Workplane("XY").workplane(offset=PLATE_TOP - PLATE[2] - SERVO_TAB_T)
            .rect(SERVO_TAB_SPAN, SERVO[0]).extrude(SERVO_TAB_T))
    s = body.union(tabs).translate((sx, y, 0))
    horn = cq.Workplane("XY").workplane(offset=PLATE_TOP - PLATE[2] - SERVO[1] - 2).rect(5, 18).extrude(2)
    pin = (cq.Workplane("YZ").workplane(offset=x - 18 if flip > 0 else x - 12)
           .center(y, PIN_Z).circle(1.5).extrude(30))
    rod = (cq.Workplane("YZ").workplane(offset=min(x, sx) + 6)
           .center(y + 7, PIN_Z).circle(0.6).extrude(abs(sx - x) - 10))
    return s, horn.translate((sx, y, 0)), pin, rod


def stowed_dart(x, y, flip):
    """Dart bundle hung by its tongue; flip=-1 mirrors it so heads point outboard."""
    parts = []
    for shape, col in dart.assembly("stowed"):
        sh = shape.translate((-dart.TONGUE_X, 0, -dart.TONGUE_HOLE_Z))
        if flip < 0:
            sh = sh.rotate((0, 0, 0), (0, 0, 1), 180)
        parts.append((sh.translate((x, y, PIN_Z)), col))
    return parts


def x500_ghost():
    """Outline of the X500 V2 for scale: 144 mm plates, 16 mm arms, 500 mm wheelbase, 215 mm gear (Holybro)."""
    g = cq.Workplane("XY").workplane(offset=20).rect(144, 144).extrude(2)
    g = g.union(cq.Workplane("XY").workplane(offset=48).rect(144, 144).extrude(2))
    for a in (45, 135, 225, 315):
        arm = (cq.Workplane("YZ").circle(X500_ARM_D / 2).extrude(X500_WHEELBASE / 2 - 20)
               .translate((20, 0, 35)).rotate((0, 0, 0), (0, 0, 1), a))
        g = g.union(arm)
    for s in (-1, 1):
        rail = cq.Workplane("YZ").circle(X500_RAIL_D / 2).extrude(X500_RAIL_L).translate((-X500_RAIL_L / 2, s * X500_RAIL_SPACING / 2, 0))
        g = g.union(rail)
    # landing gear left out: its leg positions are not published (MEASURE before drawing extensions)
    return g


def harness_parts():
    parts = [(plate(), "print")]
    for s in (-1, 1):
        for x in (-80, 80):
            parts.append((saddle(s * X500_RAIL_SPACING / 2).translate((x, 0, 0)), "print"))
    for gx in (-1, 1):
        for gy in (-1, 1):
            x, y = gx * GRID_X, gy * GRID_Y
            parts.append((release_block(x, y, gx), "print"))
            s, horn, pin, rod = servo(x, y, gx)
            parts += [(s, "servo"), (horn, "ghost"), (pin, "steel"), (rod, "steel")]
    return parts


if __name__ == "__main__":
    import pathlib
    from render import render
    out = pathlib.Path(__file__).parent / "out"
    out.mkdir(exist_ok=True)
    cq.exporters.export(plate(), str(out / "harness_plate.stl"))
    cq.exporters.export(plate(), str(out / "harness_plate.step"))
    cq.exporters.export(release_block(0, 0, 1), str(out / "harness_release_block.stl"))
    cq.exporters.export(saddle(0), str(out / "harness_saddle.stl"))
    print("plate fits bed:", PLATE[0] <= BED[0] and PLATE[1] <= BED[1])
    darts = []
    for gx in (-1, 1):
        for gy in (-1, 1):
            darts += stowed_dart(gx * GRID_X, gy * GRID_Y, gx)
    bb = cq.Compound.makeCompound([s.val() for s, _ in darts]).BoundingBox()
    print("dart bundle footprint", round(bb.xlen), "x", round(bb.ylen), "lowest point z", round(bb.zmin),
          "| X500 feet at z", 20 - X500_GEAR_H, "-> extension needed >=", round(20 - X500_GEAR_H - bb.zmin + 20))
    ghost = x500_ghost()
    img = pathlib.Path(__file__).parents[1] / "assets" / "images" / "build"
    render(harness_parts() + darts, img / "harness-x500-close.png", elev=-18, azim=-60, size=(1200, 900), zoom=1.15)
    render([(ghost, "ghost")] + harness_parts() + darts,
           img / "harness-x500.png", elev=16, azim=-55, size=(1200, 900), zoom=1.25)
