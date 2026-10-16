"""v3: three parts per dart, no loose hardware.

DART: rod + ONE printed body + head pod. The body is the nose (cell cradle) and the
hanger in one print: the cell snaps into an open cradle (no zip tie), and a sleeve runs
back along the rod to the hanger post, which sits at the balance point. Nothing is
glued at a measured spot and there is no separate clip. No foam: the mic looks out of
a side port under a printed hood.

HARNESS: unchanged from v2 (plate, rotor, one SG90). The hanger head is the same
round head on the same radius, so v2's plate and rotor carry v3 darts as they are.

Dart frame: rod along Z, tip at z=0, cell on +Y (up when hung). Body prints lying on
its flat underside (-Y), post and cradle opening up, no supports.
"""
import math
import cadquery as cq
from params import *
import v2
from v2 import (RD, RL, TIP_L, SPIKE, WALL, CELL_BORE, YC, NOSE, POD_OD, POD_L, SOCKET,
                CLIP_L, CLIP_W, HEAD_D, NECK_D, HEAD_H, RT, M_WIRE, rod, clip_post_h)

RT_OUT = (RD + 0.3) / 2 + WALL         # rod sleeve outer radius
BAY_Z0 = SPIKE + NOSE                  # cell bay front
BAY_Z1 = BAY_Z0 + CELL_L + 0.6         # cell bay back
BACK = 2.5                             # back wall of the bay
SNAP_W = 0.85 * CELL_D                 # cradle opening: narrower than the cell, so it snaps in
M_MIC = 2.0                            # INMP441 breakout, no foam (ESTIMATE)


def body(clip_z):
    """Nose + cell cradle + sleeve + hanger post, one print."""
    z0, z_end = SPIKE, clip_z + CLIP_L / 2
    # rod sleeve with a flat underside to print on
    s = (cq.Workplane("XY").circle(RT_OUT).extrude(z_end - z0)
         .union(cq.Workplane("XY").center(0, -RT_OUT / 2).rect(2 * RT_OUT, RT_OUT).extrude(z_end - z0)))
    # cell section: shell round the cell, web to the sleeve
    cl = BAY_Z1 + BACK - z0
    s = s.union(cq.Workplane("XY").center(0, YC).circle(CELL_BORE / 2 + WALL).extrude(cl))
    s = s.union(cq.Workplane("XY").center(0, YC / 2).rect(2 * RT_OUT, YC).extrude(cl))
    s = s.cut(cq.Workplane("XY").circle((RD + 0.3) / 2).extrude(z_end - z0))
    s = s.translate((0, 0, z0))
    # bay, and the snap opening on top: the cell presses down past the lips
    s = s.cut(cq.Workplane("XY").workplane(offset=BAY_Z0).center(0, YC).circle(CELL_BORE / 2).extrude(BAY_Z1 - BAY_Z0))
    lip = math.sqrt((CELL_BORE / 2) ** 2 - (SNAP_W / 2) ** 2)
    s = s.cut(cq.Workplane("XY").workplane(offset=BAY_Z0).center(0, YC + lip + 10).rect(SNAP_W, 20).extrude(BAY_Z1 - BAY_Z0))
    # wire notch in the back wall
    s = s.cut(cq.Workplane("XY").workplane(offset=BAY_Z1 - 1).center(0, YC + CELL_BORE / 2).rect(3.0, 6.0).extrude(BACK + 2))
    # nose: chamfer the front so it parts soil
    s = s.cut(cq.Workplane("YZ").workplane(offset=-20)
              .polyline([(YC + CELL_BORE / 2 + WALL + 1, z0 - 1), (YC + CELL_BORE / 2 + WALL + 1, z0 + 14), (RT_OUT, z0 - 1)])
              .close().extrude(40))
    # hanger post + neck + round head (v2's clip, now part of the body)
    h = clip_post_h()
    post = cq.Workplane("XY").center(0, h / 2).rect(CLIP_W, h).extrude(CLIP_L)
    nh = (cq.Workplane("XY").circle(NECK_D / 2).extrude(RT + 0.6)
          .faces(">Z").workplane().circle(HEAD_D / 2).extrude(HEAD_H).faces(">Z").edges().chamfer(0.8))
    post = post.union(nh.rotate((0, 0, 0), (1, 0, 0), -90).translate((0, h, CLIP_L / 2)))
    post = post.cut(cq.Workplane("XY").circle((RD + 0.3) / 2).extrude(CLIP_L))
    return s.union(post.translate((0, 0, clip_z - CLIP_L / 2)))


def pod():
    """v2's thin shell with the whip out of the top, plus a side mic port under a hood."""
    p = v2.pod()
    zt = RL - SOCKET + POD_L - 18
    p = p.cut(cq.Workplane().add(cq.Solid.makeCylinder(2.0, POD_OD, cq.Vector(0, 0, zt), cq.Vector(0, 1, 0))))
    hood = (cq.Workplane("XY").workplane(offset=zt + 4).center(0, POD_OD / 2 + 2).rect(12, 8).extrude(2.0)
            .cut(cq.Workplane("XY").workplane(offset=zt).circle(POD_OD / 2 - 1.8).extrude(8)))
    return p.union(hood)


def extras():
    top = RL - SOCKET + POD_L
    return [(cq.Workplane("XY").circle(0.8).extrude(82).translate((0, 0, top - 2)), "steel")]


def masses(clip_z):
    def printed(s):
        v = s.val()
        return v.Volume() / 1000 * PETG * 0.6, v.Center().z
    r = rod().val()
    items = [(r.Volume() / 1000 * FIBREGLASS, r.Center().z), printed(body(clip_z)), printed(pod())]
    items.append((M_CELL, BAY_Z0 + CELL_L / 2))
    items += [(M_HELTEC, RL + 2 + HELTEC[0] / 2), (M_MIC, RL - SOCKET + POD_L - 18), (M_WIRE, RL / 2)]
    return items


def balance():
    z = RL / 2
    for _ in range(6):
        it = masses(z)
        z = sum(m * c for m, c in it) / sum(m for m, _ in it)
    return z, sum(m for m, _ in masses(z))


CLIP_Z, DART_G = balance()


def dart():
    return [(rod(), "pole"), (body(CLIP_Z), "print"), (pod(), "print2")] + extras()


def to_harness(shape, i, drop=0.0):
    s = shape.rotate((0, 0, 0), (1, 0, 0), 90).rotate((0, 0, 0), (0, 0, 1), 90)
    tx, ty = v2.tongue_xy(i)
    return s.translate((tx - CLIP_Z, ty, v2.ROD_Z - drop))


def hung(i, drop=0.0):
    return [(to_harness(s, i, drop), c) for s, c in dart()]


def scene(phi=0.0, dropped=(), rails=True):
    parts = [(v2.plate(), "print"), (v2.rotor(phi), "print2")] + v2.servo(phi)
    for i in range(4):
        if i not in dropped:
            parts += hung(i)
    if rails:
        for s in (-1, 1):
            parts.append((cq.Workplane("YZ").circle(X500_RAIL_D / 2).extrude(X500_RAIL_L)
                          .translate((-X500_RAIL_L / 2, s * X500_RAIL_SPACING / 2, v2.CRADLE[2] + 1)), "ghost"))
    return parts


if __name__ == "__main__":
    import pathlib
    from render import render
    out = pathlib.Path(__file__).parent / "out"
    img = pathlib.Path(__file__).parents[1] / "assets" / "images" / "build"
    b = body(CLIP_Z)
    for name, s in (("v3_dart_body", b), ("v3_dart_pod", pod())):
        cq.exporters.export(s, str(out / f"{name}.stl"))
        cq.exporters.export(s, str(out / f"{name}.step"))
        bb = s.val().BoundingBox()
        print(name, "bbox", round(bb.xlen), round(bb.ylen), round(bb.zlen),
              "fits bed lying down" if sorted((bb.xlen, bb.ylen, bb.zlen))[-1] <= BED[0] else "TOO BIG",
              "~%.0f g" % (s.val().Volume() / 1000 * PETG * 0.6))
    print("dart ~%.0f g (v2 %.0f g); hanger at %.0f mm from the tip = %.0f%% of %.0f mm"
          % (DART_G, v2.DART_G, CLIP_Z, 100 * CLIP_Z / (RL - SOCKET + POD_L), RL - SOCKET + POD_L))
    for m, c in masses(CLIP_Z):
        print("   %.1f g at z=%.0f" % (m, c))
    # snap: the opening must be narrower than the cell, and the cradle must wrap past half
    wrap = 360 - 2 * math.degrees(math.asin(SNAP_W / CELL_BORE))
    print("cradle opening %.1f mm for an %.1f mm cell, wraps %.0f deg" % (SNAP_W, CELL_D, wrap))
    assert SNAP_W < CELL_D and wrap > 180
    # release + clash checks, as v2 but with v3 darts
    order = sorted(range(4), key=lambda i: v2.STEP[i])

    def head_on_rim(i, phi):
        tx, ty = v2.tongue_xy(i)
        col = cq.Workplane("XY").workplane(offset=v2.RZ - 1).center(tx, ty).circle(HEAD_D / 2).extrude(RT + 2)
        return v2.rotor(phi).intersect(col).val().Volume()
    for k, i in enumerate(order):
        for phi in range(0, int(v2.STEP[i]) + 1):
            for j in order[k + 1:]:
                assert head_on_rim(j, phi) > 1.0, f"dart {j} uncovered at {phi} deg"
        assert head_on_rim(i, v2.STEP[i]) < 1e-6
    print("release: each dart held until its own step, free at it: OK")
    pl = v2.plate()
    dz = [cq.Compound.makeCompound([s.val() for s, c in hung(i)]) for i in range(4)]
    worst = 0.0
    for phi in range(0, int(max(v2.STEP)) + 1, 4):
        r = v2.rotor(phi)
        for i in range(4):
            worst = max(worst, v2.clash(cq.Workplane().add(dz[i]), r))
    sv = v2.servo()[0][0]
    for i in range(4):
        worst = max(worst, v2.clash(cq.Workplane().add(dz[i]), pl), v2.clash(cq.Workplane().add(dz[i]), sv))
        for j in range(i + 1, 4):
            worst = max(worst, v2.clash(cq.Workplane().add(dz[i]), cq.Workplane().add(dz[j])))
    print("worst clash volume: %.3f mm3" % worst)
    bb = cq.Compound.makeCompound([s.val() for s, _ in scene()]).BoundingBox()
    print("hung footprint %d x %d mm; lowest point %.0f mm below the rail axis" % (bb.xlen, bb.ylen, v2.CRADLE[2] + 1 - bb.zmin))
    first = order[0]
    sc = scene(v2.STEP[first], dropped=(first,)) + [(s.translate((0, 0, -90)), c) for s, c in hung(first)]
    render(sc, img / "v3-harness.png", elev=-18, azim=-58, size=(1300, 700), zoom=1.8)
    soil = cq.Workplane("XY").rect(120, 120).extrude(SPIKE)
    render(dart() + [(soil, "ghost")], img / "v3-dart.png", elev=8, azim=-60, size=(500, 1300), zoom=0.95)
    flat = b.rotate((0, 0, 0), (1, 0, 0), 90)
    render([(flat, "print")], img / "v3-body.png", elev=35, azim=-60, size=(1000, 500), zoom=1.0)
