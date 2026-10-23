"""Cutter model: a wire and a trolley that cut a fibre-optic FPV's line where it crosses.

A line of 12.5 ga high-tensile fence wire, about 3 ft up on T-posts, split into spans. Each span
has one trolley parked at its charging post. A fibre FPV lays its line on whatever is under it,
so where its path crosses the wire the fibre drapes over it. On an alert the trolley runs along
its span with a V-notch blade and cuts what lies across.

Prints: wire sag, how long a cut takes and how far a drone gets meanwhile, a trolley's power,
and parts per mile at three scales with our markup.

    py cutter_model.py [--span 165] [--speed 20]

Stdlib only. Every number marked ASSUME is a planning number, not a measurement.
"""
import argparse, math, random

MILE = 5280.0
DRONE_MPH = 43.0        # a fibre FPV's top speed (threat-profile)
DETECT_S = 1.0          # from the drone passing to the trolley moving ASSUME (Chaharnyk claims 1 s)

# ---- the wire ------------------------------------------------------------------------------
WIRE_LB_FT = 99 / 4000  # 12.5 ga HT smooth wire: a 4,000 ft roll weighs 99 lb (Tractor Supply)
WIRE_BREAK_LB = 1500    # 200 kpsi class 3, about 1,500 lb
TENSION_LB = 250        # set tension, the usual for HT fence ASSUME
TROLLEY_LB = 2.0        # trolley with its pack ASSUME (a Wiral LITE is 1.3 lb)
POST_HEIGHT_FT = 3.0    # wire height at a post ASSUME

# ---- the fibre ------------------------------------------------------------------------------
FIBRE_PROOF_LBF = 8.5 / 4.448   # 100 kpsi proof on 125 um glass, about 8.5 N
FIBRE_VENDOR_LBF = 60 / 4.448   # vendors claim up to 50-60 N

# ---- the trolley's energy -------------------------------------------------------------------
TROLLEY_KG = TROLLEY_LB * 0.4536
DRIVE_EFF = 0.5         # motor, ESC and wheel ASSUME
ROLL_COEF = 0.05        # rolling resistance on wire ASSUME
IDLE_WH_DAY = 0.5       # board listening on LoRa all day, about a dart's 105 mAh at 3.7 V plus margin ASSUME
SWEEPS_DAY = 24         # an hourly sweep out and back, for drones waiting by a road ASSUME
PACK_WH = 3 * 3.6 * 2.5 # 3S 18650 pack, 2,500 mAh

# ---- parts, $ per trolley at prototype / small batch / production (est. except listed) --------
TROLLEY_PARTS = [
    ("Processor and radio: the dart's XIAO ESP32S3 + Wio-SX1262", 16, 14, 10),
    ("Drive: a 2212-class drone motor and ESC, belt to a 2 in grooved wheel", 25, 18, 12),
    ("Three V-groove bearing wheels and axles", 6, 5, 3),
    ("Two V-notch blades, ceramic, front and back", 5, 4, 2),
    ("3S 18650 pack and BMS", 18, 14, 10),
    ("Printed body, bolts, end-stop magnet and Hall sensor", 10, 8, 5),
    ("At the parking post: 10 W panel, charger, two contacts", 30, 24, 16),
    ("Assembly and test", 0, 5, 3),
]
FENCE_PARTS_MILE = [   # $ a mile, retail listings
    ("12.5 ga HT wire, 5,280 ft ($145 / 4,000 ft)", 5280 / 4000 * 145),
    ("6 ft T-posts: one per span end plus 4 braced ends a mile ($10.05)", None),
    ("Ratchet strainers ($3.69) and tension springs (~$10), 4 a mile", 4 * (3.69 + 10)),
    ("Clips, insulators and rubber end-stops", None),
]
MARKUP_OURS = (2.0, 3.0)   # +200-300% on our own hardware, as in costs.md
MARKUP_KIT = 0.3           # +30% on off-the-shelf fence hardware


def sag(span):
    wire = WIRE_LB_FT * span ** 2 / (8 * TENSION_LB)
    point = TROLLEY_LB * span / (4 * TENSION_LB)
    return wire, point


def cut_times(span, speed_fts, park="end", runs=20000, seed=7):
    """Seconds from the drone crossing to the cut, for a crossing uniform along the span."""
    rnd = random.Random(seed)
    out = []
    for _ in range(runs):
        x = rnd.uniform(0, span)
        d = x if park == "end" else abs(x - span / 2)
        out.append(DETECT_S + d / speed_fts)
    out.sort()
    return sum(out) / runs, out[int(0.9 * runs)], out[-1]


def sweep_wh(span, speed_fts):
    v = speed_fts * 0.3048
    ke = 0.5 * TROLLEY_KG * v ** 2
    roll = ROLL_COEF * TROLLEY_KG * 9.81 * span * 0.3048
    joules = 2 * (2 * ke + roll) / DRIVE_EFF     # out and back, speeding up and braking each way
    return joules / 3600


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--span", type=float, default=165.0)
    ap.add_argument("--speed", type=float, default=20.0, help="trolley mph")
    a = ap.parse_args()
    drone_fts = DRONE_MPH * MILE / 3600
    speed_fts = a.speed * MILE / 3600

    print(f"Fibre breaks at about {FIBRE_PROOF_LBF:.1f}-{FIBRE_VENDOR_LBF:.0f} lbf; the wire breaks at {WIRE_BREAK_LB} lb.\n")

    print("Span   sag(wire+trolley)  low point   cut: mean / 90% / worst   drone travels meanwhile")
    for span in (165.0, 330.0):
        w, p = sag(span)
        for park in ("end", "middle"):
            m, p90, worst = cut_times(span, speed_fts, park)
            print(f"{span:4.0f} ft  {w:.2f}+{p:.2f} ft        {POST_HEIGHT_FT - w - p:.1f} ft  "
                  f"parked {park:6s} {m:4.1f} / {p90:4.1f} / {worst:4.1f} s   "
                  f"{m * drone_fts:4.0f} / {p90 * drone_fts:4.0f} / {worst * drone_fts:4.0f} ft")
    print(f"(trolley {a.speed:.0f} mph, drone {DRONE_MPH:.0f} mph, {DETECT_S:.0f} s to start)\n")

    swh = sweep_wh(a.span, speed_fts)
    day = IDLE_WH_DAY + SWEEPS_DAY * swh
    print(f"Energy: a sweep out and back on {a.span:.0f} ft is {swh:.3f} Wh; a day with {SWEEPS_DAY} sweeps "
          f"is {day:.1f} Wh; the pack holds {PACK_WH:.0f} Wh, about {PACK_WH / day:.0f} days with no sun.\n")

    spans = MILE / a.span
    posts = math.ceil(spans) + 1 + 4 * 2      # a post per span end, and 4 braced ends of 3 posts
    fence = []
    for name, cost in FENCE_PARTS_MILE:
        if cost is None and name.startswith("6 ft"):
            cost = posts * 10.05
        elif cost is None:
            cost = posts * 1.0 + math.ceil(spans) * 2.0
        fence.append((name, cost))
    fence_total = sum(c for _, c in fence)
    scale_fence = (1.0, 0.92, 0.85)            # bulk farm-store pricing ASSUME

    print(f"Parts a mile, {a.span:.0f} ft spans: {spans:.0f} trolleys, {posts} posts")
    tot = [sum(p[i + 1] for p in TROLLEY_PARTS) for i in range(3)]
    for name, *c in TROLLEY_PARTS:
        print(f"  {name:72s} ${c[0]:>4} ${c[1]:>4} ${c[2]:>4}")
    print(f"  {'Trolley':72s} ${tot[0]:>4} ${tot[1]:>4} ${tot[2]:>4}")
    for name, c in fence:
        print(f"  {name:72s} ${c:,.0f} a mile")
    for i, label in enumerate(("Prototype", "Small batch (est.)", "Production (est.)")):
        trol = spans * tot[i]
        fen = fence_total * scale_fence[i]
        cost = trol + fen
        lo = trol * (1 + MARKUP_OURS[0]) + fen * (1 + MARKUP_KIT)
        hi = trol * (1 + MARKUP_OURS[1]) + fen * (1 + MARKUP_KIT)
        print(f"  {label:20s} trolleys ${trol:,.0f} + fence ${fen:,.0f} = ${cost:,.0f} a mile; "
              f"our price ${lo:,.0f}-{hi:,.0f}")

    # a year's upkeep a mile, small batch
    blades = spans * 2 * 4            # blades swapped spring and autumn
    packs = spans * 14 / 3            # a pack every 3 years
    losses = (0.05 * spans * tot[1], 0.20 * spans * tot[1])   # 5-20% of trolleys lost a year ASSUME
    wire = (25, 100)                  # splices and a re-tension after shelling ASSUME
    lo = blades + packs + losses[0] + wire[0]
    hi = blades + packs + losses[1] + wire[1]
    print(f"\nA year a mile, small batch: blades ${blades:,.0f}, packs ${packs:,.0f}, "
          f"trolleys lost ${losses[0]:,.0f}-{losses[1]:,.0f}, wire ${wire[0]}-{wire[1]}: "
          f"${lo:,.0f}-{hi:,.0f}, plus trimming grass under the wire twice a summer.")


if __name__ == "__main__":
    main()
