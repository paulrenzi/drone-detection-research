"""Listener dart v0: steel-tipped printed body carrying the cell, a folding
shock-corded mast, and a head pod with the board, mic and antenna at the top.

Axis Z, steel tip at z=0, deployed mast pointing +Z. Units mm.
Printed parts: body, cap (hinge ears + release tongue), hinge socket, head pod.
"""
import cadquery as cq
from params import *

OD = 26.0                 # body outside diameter
ROD_OUT = 50.0            # steel protruding below the printed cone
CONE_L = 50.0
CELL_BAY_L = CELL_L + 2.0
BODY_TOP = ROD_OUT + CONE_L + CELL_BAY_L + 4.0   # z where the cap sits
CAP_T = 5.0
DECK = BODY_TOP + CAP_T                         # top face of the cap
PIVOT_Z = DECK + 12
HINGE_PIN_D = 3.2         # M3 bolt
TONGUE_X, TONGUE_H, TONGUE_HOLE_Z = -8.0, 26.0, DECK + 21
HOOK = True               # v1 release: horn-as-latch notch (False = v0 pin hole)
NOTCH_H = 2.6             # SG90 horn arm ~1.6 mm thick (MEASURE) + clearance
POD_OD, POD_L = 34.0, 92.0
SOCKET = 28.0             # pole depth into the pod


def rod():
    return cq.Workplane("XY").circle(ROD_D / 2).extrude(ROD_L)


def body():
    """Cone + cell bay, one print. Open at the top; the cap closes it."""
    prof = (cq.Workplane("XZ")
            .moveTo(0, ROD_OUT).lineTo(5.0, ROD_OUT)
            .lineTo(OD / 2, ROD_OUT + CONE_L)
            .lineTo(OD / 2, BODY_TOP).lineTo(0, BODY_TOP).close())
    b = prof.revolve(360, (0, 0, 0), (0, 1, 0))
    b = b.cut(cq.Workplane("XY").workplane(offset=ROD_OUT - 1)       # rod bore, press fit + epoxy
              .circle((ROD_D + 0.3) / 2).extrude(ROD_L - ROD_OUT + 1))
    b = b.cut(cq.Workplane("XY").workplane(offset=BODY_TOP - CELL_BAY_L)
              .circle((CELL_D + 0.8) / 2).extrude(CELL_BAY_L + 1))
    return b


def cap():
    """Plugs the cell bay. Carries the mast hinge ears and the release tongue."""
    c = (cq.Workplane("XY").workplane(offset=BODY_TOP - 8)
         .circle((CELL_D + 0.4) / 2).extrude(8)                     # spigot into the bay
         .faces(">Z").workplane().circle(OD / 2).extrude(CAP_T))
    ear = (cq.Workplane("XY").workplane(offset=DECK)
           .center(4, 0).rect(14, 3.5).extrude(18).edges("|Y and >Z").fillet(1.6))
    for y in (-6.75, 6.75):
        c = c.union(ear.translate((0, y, 0)))
    c = c.cut(cq.Workplane("XZ").workplane(offset=-20).center(6, PIVOT_Z)
              .circle(HINGE_PIN_D / 2).extrude(40))
    tongue = (cq.Workplane("XY").workplane(offset=DECK).center(TONGUE_X, 0)
              .rect(4, 8).extrude(TONGUE_H).edges("|X and >Z").fillet(2))
    if HOOK:   # side-open notch: the servo horn arm sits in it and swings out sideways to release
        tongue = tongue.cut(cq.Workplane("XY").workplane(offset=TONGUE_HOLE_Z - NOTCH_H / 2)
                            .center(TONGUE_X, 1.5).rect(6, 5.2).extrude(NOTCH_H))
    else:      # v0: hole for a 3 mm pin
        tongue = tongue.cut(cq.Workplane("YZ").workplane(offset=TONGUE_X - 5).center(0, TONGUE_HOLE_Z)
                            .circle(1.8).extrude(10))
    c = c.union(tongue)
    c = c.cut(cq.Workplane("XY").workplane(offset=BODY_TOP - 9).center(6, -2).rect(3, 3).extrude(20))  # power wire
    return c


def hinge(angle=0):
    """Mast socket pivoting between the ears. 0 = upright, 90 = folded flat for carrying."""
    h = (cq.Workplane("XY").rect(9.4, 9.4).extrude(18)
         .faces(">Z").workplane().circle(POLE_D / 2 + 2.4).extrude(16)
         .faces(">Z").workplane().hole(POLE_D + 0.3, 26)
         .edges("|Z").fillet(1.5))
    h = h.cut(cq.Workplane("XZ").workplane(offset=-10).center(0, 6)
              .circle(HINGE_PIN_D / 2).extrude(20))
    h = h.translate((0, 0, -6)).rotate((0, 0, 0), (0, 1, 0), angle).translate((6, 0, PIVOT_Z))
    return h


def pod():
    """Head pod: board upright, mic facing up under the fur, whip out the top."""
    shell = (cq.Workplane("XY").circle(POD_OD / 2).extrude(POD_L)
             .faces(">Z").edges().fillet(8).faces("<Z").edges().fillet(4))
    shell = shell.cut(cq.Workplane("XY").workplane(offset=SOCKET + 2.0)
                      .rect(HELTEC[1] + 1.0, HELTEC[2] + 6.0).extrude(HELTEC[0] + 6))
    shell = shell.cut(cq.Workplane("XY").circle((POLE_D + 0.3) / 2).extrude(SOCKET))
    shell = shell.faces(">Z").workplane().hole(4.0, 6)              # mic port / whip exit
    return shell


def assembly(state="deployed", soil=True):
    parts = [(rod(), "steel"), (body(), "print"), (cap(), "print")]
    pole_len = POLE_SEG * POLE_SEGS
    if state == "deployed":
        parts.append((hinge(0), "print2"))
        z0 = PIVOT_Z + 6
        pole = cq.Workplane("XY").circle(POLE_D / 2).extrude(pole_len).translate((6, 0, z0))
        parts.append((pole, "pole"))
        ptop = z0 + pole_len
        parts.append((pod().translate((6, 0, ptop - SOCKET)), "print2"))
        parts.append((cq.Workplane("XY").sphere(24).translate((6, 0, ptop - SOCKET + POD_L + 4)), "fur"))
        parts.append((cq.Workplane("XY").circle(0.8).extrude(82).translate((6, 0, ptop - SOCKET + POD_L + 20)), "steel"))
        if soil:  # steel plus most of the cone buried (ESTIMATE; T10 measures it)
            parts.append((cq.Workplane("XY").rect(140, 140).extrude(ROD_OUT + CONE_L * 0.6), "ghost"))
    else:  # stowed: hinge folded flat, sections Z-folded down the body on their shock cord
        parts.append((hinge(90), "print2"))
        top = PIVOT_Z
        for i in range(POLE_SEGS):
            x = OD / 2 + POLE_D / 2 + 3 + i * (POLE_D + 0.8)
            seg = cq.Workplane("XY").circle(POLE_D / 2).extrude(POLE_SEG).translate((x, 0, top - POLE_SEG))
            parts.append((seg, "pole"))
        xp = OD / 2 + 3 + POLE_SEGS * (POLE_D + 0.8) + POD_OD / 2
        parts.append((pod().translate((xp, 0, top - POD_L)), "print2"))
    return parts


def mass_g():
    vol = sum(f().val().Volume() for f in (body, cap, hinge, pod)) / 1000.0
    printed = vol * PETG * 0.6           # ~60% of solid at 3 walls + 25% infill: ESTIMATE
    rod_g = 3.1416 * (ROD_D / 20) ** 2 * (ROD_L / 10) * STEEL
    pole_g = 3.1416 * ((POLE_D / 20) ** 2 - (POLE_D / 20 - 0.1) ** 2) * (POLE_SEG * POLE_SEGS / 10) * FIBREGLASS
    total = printed + rod_g + pole_g + M_HELTEC + M_CELL + M_MIC_FUR + 6  # +6 g wire, whip, fasteners
    return dict(printed=printed, rod=rod_g, pole=pole_g, total=total)


def stowed_size():
    bb = cq.Compound.makeCompound([s.val() for s, _ in assembly("stowed")]).BoundingBox()
    return bb.xlen, bb.ylen, bb.zlen


if __name__ == "__main__":
    import pathlib, json
    from render import render
    out = pathlib.Path(__file__).parent / "out"
    out.mkdir(exist_ok=True)
    for name, fn in (("dart_body", body), ("dart_cap", cap), ("dart_hinge", hinge), ("dart_pod", pod)):
        s = fn()
        cq.exporters.export(s, str(out / f"{name}.stl"))
        cq.exporters.export(s, str(out / f"{name}.step"))
        bb = s.val().BoundingBox()
        print(name, "bbox", round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1),
              "fits bed" if max(bb.xlen, bb.ylen) <= BED[0] and bb.zlen <= BED[2] else "TOO BIG")
    print("mass", json.dumps({k: round(v, 1) for k, v in mass_g().items()}))
    print("stowed bundle", [round(v) for v in stowed_size()], "deployed mic height above soil ~",
          round(PIVOT_Z + 6 + POLE_SEG * POLE_SEGS - SOCKET + POD_L - (ROD_OUT + CONE_L * 0.6)))
    img = pathlib.Path(__file__).parents[1] / "assets" / "images" / "build"
    img.mkdir(parents=True, exist_ok=True)
    render(assembly("deployed"), img / "dart-deployed.png", elev=10, azim=-55, size=(600, 1400), zoom=0.95)
    render(assembly("stowed"), img / "dart-stowed.png", elev=18, azim=-65, size=(900, 1000), zoom=0.9)
