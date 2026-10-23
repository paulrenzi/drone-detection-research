"""Lay model for the two-trunk net on How it works.

Plans a net on a sector map (positions, enemy edge, tree belts, ravines, slope), checks every
sortie against the battery in the forecast wind, writes one ArduPilot mission per sortie, then
lays the net many times in simulation with drop errors, bad landings, radio fading and
drop-then-confirm, and reports how often the net comes out whole.

    py lay_model.py [sector.json] [--runs 2000] [--seed 7] [--out out]

Stdlib only. Local frame in feet: x along the front, y toward the enemy, receiver at (0, 0).
Every number marked ASSUME is a planning number, not a measurement; the test that measures it
is named beside it.
"""
import json, math, os, random, sys

# ---- planning numbers (as on How it works) -------------------------------------------------
HEAR, ALT = 656.0, 165.0                       # hearing range; drone height (T11)
REFF = math.sqrt(HEAR ** 2 - ALT ** 2)         # hearing along the ground, ~635 ft
HOP = 980.0                                    # hop that works 90% of the time (T9) ASSUME
FTS = 88.0                                     # 60 mph
NEED = FTS * 65                                # a minute plus 5 s
W = 1640.0
DEPTH = NEED - math.sqrt(REFF ** 2 - HOP ** 2 / 4)

# ---- radio ----------------------------------------------------------------------------------
FADE_DB = 4.0          # spread of link loss from place to place, 1 sigma (T9) ASSUME
PLE = 4.0              # path-loss exponent near the ground (two-ray, past ~30 ft at 915 MHz)
Z90 = 1.2816
MEDIAN_HOP = HOP * 10 ** (Z90 * FADE_DB / 10 / PLE)   # the typical hop if 980 ft is the 90% hop
BELT_DB = 4.4          # one 33 ft windbreak at 915 MHz (tripwire page, Weissberger estimate)
SHADOW_DB = 10.0       # a dart in a ravine, no line of sight ASSUME
ANT_FT = 1.7           # antenna height on an upright dart

# ---- ground ---------------------------------------------------------------------------------
BELT_MARGIN = 40.0     # keep drop points this far outside a belt's edge (canopy + drop error)
RAVINE_MAX = 10.0      # a point more than 10 ft below the rim is in radio shadow
STANDOFF = 650.0       # keep darts one hearing range short of the enemy edge ASSUME

# ---- delivery drone (X500 V2 as on Build: hardware) ----------------------------------------
ANCHOR_MIN, ANCHOR_G = 18.0, 1700.0   # Holybro's 18 min hover, no payload, 4S 5000 mAh; AUW est.
HARNESS_G = 80.0                      # v2 plate, rotor, servo
KIT_G = 45.0                          # optical flow + lidar, confirm radio, mounts ASSUME
DART_G = 128.0                        # v3 dart, 4.5 oz
RESERVE = 0.20
CRUISE_MPH = 22.0                     # 10 m/s, the hardware page's reach figure; the planner picks per leg
RHO, DISK_M2 = 1.27, 0.2027          # air near freezing; four 10 in props
PROFILE = 0.15                        # share of hover power that doesn't fall with speed ASSUME
CDA_M2, ETA = 0.06, 0.6               # drag area with 4 darts hung flat; thrust per watt (T13) ASSUME
PACK_WH = 74.0                        # 4S 5000 mAh
VA_MIN, VA_MAX = 12.0, 40.0           # airspeeds the planner may pick, mph
CLIMB_K = 1.15
CRUISE_AGL, DROP_AGL = 100.0, 33.0    # over the tallest belts; release height (lidar-held)
LOW_AGL = 35.0                        # GPS jammed: cruise low so optical flow stays inside the 39 ft lidar range
BELT_HOP_FT = 60.0                    # climb to cross a belt when cruising low
V_UP, V_DN = 8.2, 4.9                 # ft/s, ArduPilot defaults 2.5 and 1.5 m/s
SETTLE_S, LISTEN_S = 3.0, 6.0         # hover before release; listen for the relay (overlaps climb)
LAUNCH = (300.0, -400.0)              # launch point behind the tree line, away from the positions
TURN_MIN, CHARGE_MIN = 5.0, 60.0      # reload + swap; one 1C charge
PACKS, CHANNELS = 6, 2                # flight packs; charger channels
CAPACITY = 4

# ---- landing (T10) ASSUME -------------------------------------------------------------------
P_UPRIGHT, P_TILTED = 0.85, 0.10      # the rest are duds that never report
P_DRONE_LOSS = 0.02
SPARE_STEP = 300.0
COMPASS_DEG, COMPASS_SORTIE_DEG = 2.0, 0.7   # GPS jammed: heading error per lay, and sortie to sortie (T14) ASSUME
FLOW_SCALE, FLOW_SORTIE = 0.02, 0.005        # optical-flow distance error, same split (T14) ASSUME
WHOLE_S = 55.0                        # a lay is whole if every track gets at least this much warning
MAX_EXTRA = 3                         # extra darts tried per point before it is left for the crew
END_INSET = -300.0                    # end darts 300 ft beyond the 45° edge line; the old plan set them 635 ft in
PLAN_FRAC = 1.0                       # plan hops at this share of the 90% hop


def cold_factor(temp_f, warmed):
    f = 1.0 if temp_f >= 59 else 0.88 + (temp_f - 32) * (0.12 / 27) if temp_f >= 32 else 0.88 - (32 - temp_f) * (0.13 / 18)
    return max(f, 0.95) if warmed else max(f, 0.5)


# ---- geometry -------------------------------------------------------------------------------
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def mul(a, k): return (a[0] * k, a[1] * k)
def dist(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
def lerp(a, b, u): return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
def rot(p, deg):
    t = math.radians(deg)
    return (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))


def seg_dist(p, a, b):
    d = sub(b, a); L2 = d[0] ** 2 + d[1] ** 2
    u = 0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) / L2))
    return dist(p, lerp(a, b, u))


def poly_dist(p, line):
    return min(seg_dist(p, line[i], line[i + 1]) for i in range(len(line) - 1))


def seg_cross(a, b, c, d):
    def o(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


class Sector:
    def __init__(self, cfg):
        self.cfg = cfg
        self.belts = cfg.get("tree_belts", [])
        self.ravines = cfg.get("ravines", [])
        self.edge = [tuple(p) for p in cfg["enemy_edge"]]
        self.slope = cfg.get("slope_ft_per_ft", 0.0)
        w = cfg.get("wind", {"mph": 0, "toward_deg": 0, "gust_margin_mph": 0})
        t = math.radians(w["toward_deg"])
        self.wind = (w["mph"] * math.sin(t), w["mph"] * math.cos(t))
        self.gust = w.get("gust_margin_mph", 0)
        self.cap = cold_factor(cfg.get("air_temp_f", 59), cfg.get("packs_warmed", True))

    def edge_y(self, x):
        e = self.edge
        for i in range(len(e) - 1):
            if e[i][0] <= x <= e[i + 1][0]:
                return e[i][1] + (e[i + 1][1] - e[i][1]) * (x - e[i][0]) / (e[i + 1][0] - e[i][0])
        return e[0][1] if x < e[0][0] else e[-1][1]

    def ravine_depth(self, p):
        best = 0.0
        for r in self.ravines:
            d, h = poly_dist(p, r["line"]), r["width"] / 2
            if d < h: best = max(best, r["depth"] * (1 - (d / h) ** 2))
        return best

    def elev(self, p): return self.slope * p[1] - self.ravine_depth(p)

    def in_belt(self, p, margin=BELT_MARGIN):
        return any(poly_dist(p, b["line"]) <= b["width"] / 2 + margin for b in self.belts)

    def why_not(self, p):
        if self.in_belt(p): return "tree belt"
        if self.ravine_depth(p) > RAVINE_MAX: return "ravine"
        if p[1] > self.edge_y(p[0]) - STANDOFF or poly_dist(p, self.edge) < STANDOFF: return "enemy edge"
        return None

    def belts_crossed(self, a, b):
        n = 0
        for bl in self.belts:
            L = bl["line"]
            if any(seg_cross(a, b, L[i], L[i + 1]) for i in range(len(L) - 1)): n += 1
        return n

    def blocked(self, a, b):
        ha, hb = self.elev(a) + ANT_FT, self.elev(b) + ANT_FT
        for k in range(1, 20):
            u = k / 20
            if self.elev(lerp(a, b, u)) > ha + (hb - ha) * u: return True
        return False

    def loss_db(self, a, b):
        return BELT_DB * self.belts_crossed(a, b) + (SHADOW_DB if self.blocked(a, b) else 0.0)

    def reach(self, a, b, fade_db=0.0, median=False):
        return (MEDIAN_HOP if median else HOP * PLAN_FRAC) * 10 ** ((fade_db - self.loss_db(a, b)) / 10 / PLE)


# ---- the plan -------------------------------------------------------------------------------
def arc_point(u, depth):
    a = depth * math.pi / 4
    if u < a:
        th = math.pi / 4 * (1 - u / a); return (-W / 2 - depth * math.sin(th), depth * math.cos(th))
    if u <= a + W: return (-W / 2 + (u - a), depth)
    th = math.pi / 4 * (u - a - W) / a; return (W / 2 + depth * math.sin(th), depth * math.cos(th))


def pulled(sec, p, notes):
    """Pull a point toward the unit until it clears the enemy edge by STANDOFF."""
    q = p
    for k in range(60):
        if sec.why_not(q) != "enemy edge": break
        q = mul(p, 1 - 0.01 * (k + 1))
    if q != p: notes.append(("pulled in", p, q))
    return q


def place(sec, pts_fn, u0, u1, step_max, notes):
    """Greedy along a parameterised path: each next point as far along as possible such that it is
    allowed ground and within radio reach (and step_max) of the previous one."""
    def ok_at(u):
        p = pulled(sec, pts_fn(u), [])
        return p if sec.why_not(p) is None else None
    out, u = [], u0
    p = ok_at(u)
    while p is None and u < u1: u += 10; p = ok_at(u)
    out.append((u, p))
    while True:
        if u1 - u <= 40:
            if u1 - u > 1e-6: out[-1] = (u1, ok_at(u1) or p)
            break
        best = None
        cand = min(u1, u + step_max * 1.4)
        while cand > u + 20:
            q = ok_at(cand)
            if q is not None and dist(q, p) <= min(step_max, sec.reach(p, q)):
                best = (cand, q); break
            cand -= 10
        if best is None: raise RuntimeError("no allowed point within reach after u=%.0f" % u)
        u, p = best; out.append(best)
    return out


def even_or_greedy(sec, pts_fn, u0, u1, step_max, notes):
    g = place(sec, pts_fn, u0, u1, step_max, notes)
    n = len(g)
    # try the same count evenly spaced, each slid up to 200 ft along the path to dodge bad ground
    us = [u0 + (u1 - u0) * i / (n - 1) for i in range(n)]
    pts = []
    for u in us:
        got = None
        for off in [0] + [s * k for k in range(10, 210, 10) for s in (1, -1)]:
            uu = min(u1, max(u0, u + off))
            p = pulled(sec, pts_fn(uu), [])
            if sec.why_not(p) is None: got = (uu, p, off); break
        if got is None: return g, []
        pts.append(got)
    for i in range(1, n):
        a, b = pts[i - 1][1], pts[i][1]
        if dist(a, b) > min(step_max, sec.reach(a, b)): return g, []
    moved = [(pts_fn(u), p, off) for u, (uu, p, off) in zip(us, pts) if abs(off) > 0]
    return [(uu, p) for uu, p, off in pts], moved


def plan(sec):
    notes = {"moved": [], "pulled": []}
    a = DEPTH * math.pi / 4; L = W + 2 * a
    nominal_n = math.ceil((L - 2 * REFF) / HOP) + 1
    fr, moved = even_or_greedy(sec, lambda u: arc_point(u, DEPTH), END_INSET, L - END_INSET, HOP * PLAN_FRAC, notes)
    front = [p for u, p in fr]
    for orig, p, off in moved: notes["moved"].append({"from": orig, "to": p, "why": sec.why_not(pulled(sec, orig, [])) or "spacing"})
    for i, p in enumerate(front):
        q = arc_point(fr[i][0], DEPTH)
        if dist(p, q) > 1: notes["pulled"].append({"from": q, "to": p})
    rx = tuple(sec.cfg["receiver"])
    trunks = []
    for j in (1, len(front) - 2):
        tip = front[j]
        L2 = dist(rx, tip)
        fn = lambda u, tip=tip: lerp(rx, tip, u / L2)
        tr, mv = even_or_greedy(sec, fn, 0.0, L2, HOP * PLAN_FRAC, notes)
        for orig, p, off in mv: notes["moved"].append({"from": orig, "to": p, "why": sec.why_not(orig) or "spacing"})
        trunks.append([p for u, p in tr][1:-1])   # drop the receiver and the front dart itself
    return {"front": front, "trunks": trunks, "nominal_front": nominal_n, "notes": notes, "rx": rx}


def lay_sequence(P):
    """Darts in laying order, each with the dart it must be confirmed against."""
    F, (TL, TR) = P["front"], P["trunks"]
    n = len(F); seq = []
    def push(name, p, anchor, kind, second=None):
        seq.append({"id": name, "p": p, "anchor": anchor, "kind": kind, "second": second})
    for i, p in enumerate(TL): push("L%d" % (i + 1), p, "RX" if i == 0 else "L%d" % i, "relay")
    push("F2", F[1], "L%d" % len(TL), "front"); push("F1", F[0], "F2", "front")
    mid = n // 2   # left side lays F3..F(mid); right side lays down to F(mid+1)
    for i in range(2, mid): push("F%d" % (i + 1), F[i], "F%d" % i, "front")
    for i, p in enumerate(TR): push("R%d" % (i + 1), p, "RX" if i == 0 else "R%d" % i, "relay")
    push("F%d" % (n - 1), F[n - 2], "R%d" % len(TR), "front"); push("F%d" % n, F[n - 1], "F%d" % (n - 1), "front")
    for i in range(n - 3, mid - 1, -1):
        push("F%d" % (i + 1), F[i], "F%d" % (i + 2), "front", second=("F%d" % i) if i == mid else None)
    return seq


# ---- flight and battery ---------------------------------------------------------------------
def hover_min(mass_g): return ANCHOR_MIN * (ANCHOR_G / mass_g) ** 1.5


def power_ratio(mass_g, va_mph):
    """Power in level flight / hover power, momentum theory plus body drag."""
    v = va_mph * 0.44704; wt = mass_g / 1000 * 9.81
    drag = 0.5 * RHO * CDA_M2 * v * v
    thrust = math.hypot(wt, drag)
    vh = math.sqrt(thrust / (2 * RHO * DISK_M2))
    s = (v / vh) ** 2
    induced = (thrust / wt) * math.sqrt((-s + math.sqrt(s * s + 4)) / 2)
    p_hover = PACK_WH / (hover_min(mass_g) / 60)
    return PROFILE + (1 - PROFILE) * induced + drag * v / ETA / p_hover


def best_speed(d, wind, mass_g):
    """Airspeed that spends the least battery per foot of ground on this leg."""
    best = None
    va = VA_MIN
    while va <= VA_MAX + 1e-9:
        gs = ground_speed(d, wind, va)
        if gs > 1:
            cost = power_ratio(mass_g, va) / gs
            if best is None or cost < best[0]: best = (cost, va, gs)
        va += 1
    return best


def ground_speed(d, wind, va=CRUISE_MPH):
    L = math.hypot(*d)
    if L == 0: return va
    ux, uy = d[0] / L, d[1] / L
    along = wind[0] * ux + wind[1] * uy
    cross = -wind[0] * uy + wind[1] * ux
    if abs(cross) >= va: return 0.0
    return along + math.sqrt(va ** 2 - cross ** 2)


class Flight:
    """Battery and clock for one sortie. Energy is a fraction of a full pack."""
    def __init__(self, sec, darts, wind, low=False):
        self.sec, self.wind, self.low = sec, wind, low
        self.agl = LOW_AGL if low else CRUISE_AGL
        self.mass = ANCHOR_G + HARNESS_G + KIT_G + DART_G * darts
        self.used, self.t, self.track, self.at = 0.0, 0.0, [], LAUNCH
        self.burn(self.agl / V_UP, CLIMB_K); self.mark()

    def burn(self, secs, k=1.0):
        self.used += secs * k / (hover_min(self.mass) * 60) / self.sec.cap
        self.t += secs

    def mark(self, ev=None): self.track.append({"t": round(self.t, 1), "p": [round(self.at[0]), round(self.at[1])], "bat": round(1 - self.used, 3), "ev": ev})

    def leg_cost(self, a, b, mass=None, wind=None):
        m = mass or self.mass
        if dist(a, b) < 1: return 0.0, 0.0
        b_ = best_speed(sub(b, a), wind or self.wind, m)
        if b_ is None: return float("inf"), float("inf")
        cost, va, gs = b_
        secs = dist(a, b) / (gs * 5280 / 3600)
        self.last_gs = gs
        return secs, secs * power_ratio(m, va) / (hover_min(m) * 60) / self.sec.cap

    def go(self, b):
        if self.low:   # hop over each tree belt on the way
            for _ in range(self.sec.belts_crossed(self.at, b)):
                self.burn(BELT_HOP_FT / V_UP, CLIMB_K); self.burn(BELT_HOP_FT / V_DN)
        secs, e = self.leg_cost(self.at, b)
        self.used += e; self.t += secs; self.at = b; self.mark()

    def drop(self):
        down = (self.agl - DROP_AGL) / V_DN; up = (self.agl - DROP_AGL) / V_UP
        self.burn(down); self.burn(SETTLE_S); self.mass -= DART_G; self.mark("release")
        self.burn(up, CLIMB_K); self.burn(max(0.0, LISTEN_S - up))

    def home_cost(self, frm=None, gust=True):
        w = self.wind
        if gust:
            m = math.hypot(*w) or 1.0
            w = mul(w, (m + self.sec.gust) / m) if math.hypot(*w) > 0 else (0.0, -self.sec.gust)
        secs, e = self.leg_cost(frm or self.at, LAUNCH, wind=w)
        land = self.agl / V_DN + 10
        return e + land / (hover_min(self.mass) * 60) / self.sec.cap

    def can_afford(self, b):
        """Fly to b, release there, and still get home in the gust wind with the reserve intact."""
        secs, e = self.leg_cost(self.at, b)
        drop_e = ((self.agl - DROP_AGL) / V_DN + SETTLE_S + LISTEN_S * 1.2) / (hover_min(self.mass) * 60) / self.sec.cap
        return self.used + e + drop_e + self.home_cost(b) <= 1 - RESERVE

    def land(self):
        self.go(LAUNCH); self.burn(self.agl / V_DN + 10); self.mark("land")


def sortie_fits(sec, pts, darts=CAPACITY):
    f = Flight(sec, darts, sec.wind)
    for p in pts:
        if not f.can_afford(p): return False, f
        f.go(p); f.drop()
    f.land()
    return f.used <= 1 - RESERVE, f


def chunk(sec, seq):
    out, i = [], 0
    while i < len(seq):
        k = CAPACITY
        while k > 0:
            ok, f = sortie_fits(sec, [s["p"] for s in seq[i:i + k]])
            if ok: break
            k -= 1
        if k == 0: raise RuntimeError("one dart to %s does not fit a battery" % seq[i]["id"])
        out.append((seq[i:i + k], f)); i += k
    return out


def timeline(durations_min, packs=PACKS, channels=CHANNELS):
    ready = [0.0] * packs; chargers = [0.0] * channels; t = 0.0; out = []
    for d in durations_min:
        k = min(range(packs), key=lambda j: ready[j])
        start = max(t, ready[k]); end = start + d
        c = min(range(channels), key=lambda j: chargers[j])
        cs = max(end, chargers[c]); chargers[c] = cs + CHARGE_MIN; ready[k] = cs + CHARGE_MIN
        out.append((start, end)); t = end + TURN_MIN
    return out


# ---- missions (QGC WPL 110, ArduPilot) ------------------------------------------------------
def to_latlon(origin, p, bearing_deg):
    q = rot(p, -bearing_deg)   # threat bearing: +y points along it
    lat0, lon0 = origin
    lat = lat0 + q[1] * 0.3048 / 111320.0
    lon = lon0 + q[0] * 0.3048 / (111320.0 * math.cos(math.radians(lat0)))
    return lat, lon


def mission(sec, darts):
    o, b = sec.cfg["origin_latlon"], sec.cfg.get("threat_bearing_deg", 0)
    rows, n = [], 0
    def row(cmd, frame, p1=0, p2=0, p3=0, p4=0, lat=0, lon=0, alt=0, cur=0):
        nonlocal n
        rows.append("\t".join(str(v) for v in [n, cur, frame, cmd, p1, p2, p3, p4, "%.7f" % lat, "%.7f" % lon, "%.2f" % alt, 1])); n += 1
    hl = to_latlon(o, LAUNCH, b)
    row(16, 0, lat=hl[0], lon=hl[1], cur=1)                              # home
    row(22, 10, alt=CRUISE_AGL * 0.3048)                                 # takeoff
    at, mass = LAUNCH, ANCHOR_G + HARNESS_G + KIT_G + DART_G * CAPACITY
    for k, d in enumerate(darts):
        la, lo = to_latlon(o, d["p"], b)
        sp = best_speed(sub(d["p"], at), sec.wind, mass)
        row(178, 0, p1=1, p2="%.1f" % (sp[2] * 0.44704), p3=-1)         # DO_CHANGE_SPEED: this leg's ground speed
        row(16, 10, lat=la, lon=lo, alt=CRUISE_AGL * 0.3048)            # over the point
        row(16, 10, p1=SETTLE_S, lat=la, lon=lo, alt=DROP_AGL * 0.3048) # down to release height
        row(183, 0, p1=9, p2=1000 + 180 * (k + 1))                      # DO_SET_SERVO, AUX 1, rotor step
        row(16, 10, lat=la, lon=lo, alt=CRUISE_AGL * 0.3048)            # back up
        at, mass = d["p"], mass - DART_G
    sp = best_speed(sub(LAUNCH, at), sec.wind, mass)
    row(178, 0, p1=1, p2="%.1f" % (sp[2] * 0.44704), p3=-1)
    row(20, 0)                                                           # RETURN_TO_LAUNCH
    return "QGC WPL 110\n" + "\n".join(rows) + "\n"


# ---- simulation -----------------------------------------------------------------------------
class Lay:
    def __init__(self, sec, P, rng, jammed=True, confirm=True):
        self.sec, self.P, self.rng, self.jammed, self.confirm = sec, P, rng, jammed, confirm
        self.seq = lay_sequence(P)
        self.plan_at = {s["id"]: s["p"] for s in self.seq}
        self.darts = {"RX": {"p": P["rx"], "ok": True, "logged": P["rx"]}}   # id -> actual position, state
        self.fade, self.links = {}, {}
        self.lay_seed = rng.random()
        self.sorties, self.used, self.lost_drones, self.gaps = [], 0, 0, []
        self.holder = {"RX": "RX"}                                          # planned point -> dart that holds it
        self.anchor_of = {s["id"]: s["anchor"] for s in self.seq}

    def joined(self, anchor, group, extra=()):
        """Darts of this point's group (and extra darts) that reach the anchor through the group."""
        pool = list(group) + list(extra); seen, q = {anchor}, [anchor]
        while q:
            a = q.pop()
            for b in pool:
                if b not in seen and self.link(a, b): seen.add(b); q.append(b)
        return [n for n in pool if n in seen]

    def resolve(self, pid):
        while pid not in self.holder: pid = self.anchor_of[pid]
        return self.holder[pid]

    def link(self, a, b):
        if a == b or not (self.darts[a]["ok"] and self.darts[b]["ok"]): return False
        key = (a, b) if a < b else (b, a)
        pa, pb = self.darts[a]["p"], self.darts[b]["p"]
        hit = self.links.get(key)
        if hit is not None and hit[0] == (pa, pb): return hit[1]
        if key not in self.fade:   # one fade per pair, independent of the order links are checked in
            self.fade[key] = random.Random("%r|%s|%s" % (self.lay_seed, key[0], key[1])).gauss(0, FADE_DB)
        d = dist(pa, pb)
        ok = d <= MEDIAN_HOP * 10 ** (self.fade[key] / 10 / PLE) and d <= self.sec.reach(pa, pb, self.fade[key], median=True)
        self.links[key] = ((pa, pb), ok)
        return ok

    def nav(self):
        if not self.jammed: return lambda p: (p[0] + self.rng.gauss(0, 10), p[1] + self.rng.gauss(0, 10))
        if not hasattr(self, "common"):   # compass and flow-scale error shared by every sortie of one drone, one day
            self.common = (self.rng.gauss(0, COMPASS_DEG), self.rng.gauss(0, FLOW_SCALE))
        bias = self.common[0] + self.rng.gauss(0, COMPASS_SORTIE_DEG)
        scale = self.common[1] + self.rng.gauss(0, FLOW_SORTIE)
        def f(p):
            q = add(LAUNCH, mul(rot(sub(p, LAUNCH), bias), 1 + scale))
            return (q[0] + self.rng.gauss(0, 15), q[1] + self.rng.gauss(0, 15))
        return f

    def land_one(self, name, actual):
        r = self.rng.random()
        st = "upright" if r < P_UPRIGHT else "tilted" if r < P_UPRIGHT + P_TILTED else "dud"
        if st == "upright" and self.sec.in_belt(actual, margin=0): st = "in a tree"
        self.darts[name] = {"p": actual, "ok": st == "upright", "state": st}
        self.used += 1
        return st

    def run(self):
        queue = [dict(x) for x in self.seq]
        while queue:
            # take as many planned points as fit (confirm needs no slot reserved: a spare is the next dart)
            k = CAPACITY
            while k > 1 and not sortie_fits(self.sec, [s["p"] for s in queue[:k]])[0]: k -= 1
            todo, carried = queue[:k], CAPACITY
            f = Flight(self.sec, carried, self.sec.wind, low=self.jammed); nav = self.nav()
            log = {"plan": [s["id"] for s in todo], "drops": []}
            if self.rng.random() < P_DRONE_LOSS:
                self.lost_drones += 1; log["lost"] = True; self.sorties.append((log, f)); continue   # spare drone flies it again
            left = carried; done = 0
            for s in todo:
                if left == 0 or not f.can_afford(s["p"]): break
                anchor = self.resolve(s["anchor"])
                second = self.resolve(s["second"]) if s["second"] and s["second"] in self.holder else None
                tries, spot, group = s.get("resume", (0, s["p"], []))
                slipped = False
                while True:
                    f.go(nav(spot))
                    name = s["id"] if tries == 0 else "%s+%d" % (s["id"], tries)
                    st = self.land_one(name, f.at); f.drop(); left -= 1
                    self.darts[name]["logged"] = spot
                    if st == "upright": group.append(name)
                    # The drone hears the new dart's own 'landed' (unless it is a dud) and which neighbours
                    # relayed it: each relay carries the relayer's ID. So it knows which side is joined.
                    side = self.joined(anchor, group)
                    ok = bool(side) and (second is None or second in self.joined(anchor, group, [second]))
                    if not self.confirm and st == "upright": ok = True; side = [name]
                    ev = {"id": name, "planned": s["id"], "at": [round(f.at[0]), round(f.at[1])], "state": st,
                          "confirmed": bool(ok) if self.confirm else None, "anchor": anchor, "second": second, "joined": bool(side)}
                    log["drops"].append(ev); f.track[-1]["ev"] = ev
                    if ok or not self.confirm:
                        if side: self.holder[s["id"]] = min(side, key=lambda n: dist(self.darts[n]["logged"], s["p"]))
                        break
                    if tries >= MAX_EXTRA: self.gaps.append(s["id"]); break
                    if st == "upright":
                        if not side:   # no relay from the anchor side: step back toward the anchor's logged point
                            frm, to = spot, self.darts[anchor]["logged"]
                        else:          # closing dart joined one side only: step from the joined dart toward the other
                            frm = self.darts[max(side, key=lambda n: -dist(self.darts[n]["logged"], self.darts[second]["logged"]))]["logged"]
                            to = self.darts[second]["logged"]
                        spot = add(frm, mul(sub(to, frm), SPARE_STEP / max(1.0, dist(to, frm))))
                    # tilted (the dart reports it) or a dud (nothing heard at all): re-drop on the same spot
                    tries += 1
                    if left == 0 or not f.can_afford(spot):   # finish this point on the next sortie
                        s["resume"] = (tries, spot, group); slipped = True; break
                if slipped: break
                done += 1
            f.land(); log["used"] = round(f.used, 3)
            self.sorties.append((log, f))
            queue = queue[done:]
        return self

    # ---- how good is the net that came out ----
    def graph(self, drop=None):
        names = [n for n, d in self.darts.items() if d["ok"] and n != drop]
        seen, q = {"RX"}, ["RX"]
        while q:
            a = q.pop()
            for b in names:
                if b not in seen and self.link(a, b): seen.add(b); q.append(b)
        return seen

    def warning(self, live):
        pts = [self.darts[n]["p"] for n in live if n != "RX"]
        worst = 1e9
        for tgt in self.sec.cfg["positions"]:
            for ang in range(-45, 46, 5):
                d = (math.sin(math.radians(ang)), math.cos(math.radians(ang)))
                start = add(tgt, mul(d, 12000.0)); d = (-d[0], -d[1])   # flying in toward the position
                best = None
                for p in pts:   # first entry into a dart's hearing circle along the track
                    m = sub(start, p); b = -(m[0] * d[0] + m[1] * d[1]); c = m[0] ** 2 + m[1] ** 2 - REFF ** 2
                    disc = b * b - c
                    if disc < 0: continue
                    s = b - math.sqrt(disc)
                    if 0 <= s <= 12000 and (best is None or s < best): best = s
                w = -1e9 if best is None else (12000 - best) / FTS - 5
                worst = min(worst, w)
        return worst

    def score(self):
        live = self.graph()
        warn = self.warning(live)
        tol = True
        for n in sorted(live):
            if n == "RX": continue
            if len(live) - len(self.graph(drop=n)) > 2: tol = False; break
        lay_min = timeline([f.t / 60 for _, f in self.sorties])
        return {"warn": warn, "whole": warn >= WHOLE_S, "tolerant": tol and warn >= WHOLE_S, "darts": self.used,
                "sorties": len(self.sorties), "hours": (lay_min[-1][1]) / 60, "lost": self.lost_drones, "gaps": len(self.gaps)}


# ---- report ---------------------------------------------------------------------------------
def pct(xs, q):
    xs = sorted(xs); return xs[min(len(xs) - 1, int(q * len(xs)))]


def run_case(sec, P, runs, seed, **kw):
    rng = random.Random(seed); res = []
    for _ in range(runs): res.append(Lay(sec, P, rng, **kw).run().score())
    n = float(len(res))
    return {"whole": sum(r["whole"] for r in res) / n, "tolerant": sum(r["tolerant"] for r in res) / n,
            "darts": sum(r["darts"] for r in res) / n, "darts90": pct([r["darts"] for r in res], 0.9),
            "sorties": sum(r["sorties"] for r in res) / n, "hours": sum(r["hours"] for r in res) / n,
            "lost": sum(r["lost"] for r in res) / n, "warn10": pct([r["warn"] for r in res], 0.1)}


def derive():
    """Recompute the numbers that follow from the planning numbers (after a sensitivity change)."""
    global DEPTH, MEDIAN_HOP
    DEPTH = NEED - math.sqrt(REFF ** 2 - HOP ** 2 / 4)
    MEDIAN_HOP = HOP * 10 ** (Z90 * FADE_DB / 10 / PLE)


def with_params(cfg, kv, fn):
    g = globals(); old = {k: g[k] for k in kv if k in g}
    c = json.loads(json.dumps(cfg))
    for k, v in kv.items():
        if k in g: g[k] = v
        elif k == "wind_mph": c["wind"]["mph"] = v
        elif k in ("air_temp_f", "packs_warmed"): c[k] = v
    derive()
    try: return fn(c)
    finally:
        g.update(old); derive()


def old_plan(sec):
    """The page's first plan: ends inset one hearing range, trunks at sixths, no ground checks."""
    a = DEPTH * math.pi / 4; L = W + 2 * a; n = math.ceil((L - 2 * REFF) / HOP) + 1
    F = [arc_point(REFF + i * (L - 2 * REFF) / (n - 1), DEPTH) for i in range(n)]
    T = [[(F[j][0] * k / 6, F[j][1] * k / 6) for k in range(1, 6)] for j in (1, n - 2)]
    return {"front": F, "trunks": T, "nominal_front": n, "notes": {"moved": [], "pulled": []}, "rx": tuple(sec.cfg["receiver"])}


def secs(w): return "none (a track no dart hears)" if w < -1e8 else "%.0f s" % w


def fmt_case(label, r):
    return "| %s | %.0f%% | %.0f%% | %.1f | %d | %.1f | %.1f h | %s | %.2f |" % (
        label, 100 * r["whole"], 100 * r["tolerant"], r["darts"], r["darts90"], r["sorties"], r["hours"], secs(r["warn10"]), r["lost"])


def nominal_warn(sec, PP):
    n = Lay(sec, PP, random.Random(0))
    for s_ in lay_sequence(PP): n.darts[s_["id"]] = {"p": s_["p"], "ok": True, "logged": s_["p"]}
    n.link = lambda a, b: a != b and dist(n.darts[a]["p"], n.darts[b]["p"]) <= sec.reach(n.darts[a]["p"], n.darts[b]["p"])
    g = n.graph()
    return n.warning(g), len(g) - 1, len(n.darts) - 1


def main(argv):
    path = next((a for a in argv if a.endswith(".json")), os.path.join(os.path.dirname(__file__), "sector.json"))
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else 1000
    seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 7
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(os.path.dirname(__file__), "out")
    cfg = json.load(open(path)); sec = Sector(cfg); P = plan(sec)
    seq = lay_sequence(P); groups = chunk(sec, seq)
    os.makedirs(out, exist_ok=True)
    md = []
    def say(line=""): print(line); md.append(line)
    say("## Plan")
    say("front darts %d (open-ground plan %d), relays per trunk %s, total %d" % (len(P["front"]), P["nominal_front"], [len(t) for t in P["trunks"]], len(seq)))
    for m in P["notes"]["moved"]: say("- moved off %s: (%.0f, %.0f) to (%.0f, %.0f)" % (m["why"], m["from"][0], m["from"][1], m["to"][0], m["to"][1]))
    for m in P["notes"]["pulled"]: say("- pulled in from the enemy edge: (%.0f, %.0f) to (%.0f, %.0f)" % (m["from"][0], m["from"][1], m["to"][0], m["to"][1]))
    w, a, b = nominal_warn(sec, P); say("planned net with no errors: worst warning %s, %d of %d darts reach the unit" % (secs(w), a, b))
    OP = old_plan(sec)
    w, a, b = nominal_warn(sec, OP); say("the page's first 20-dart plan on this ground, no errors: worst warning %s, %d of %d darts reach the unit" % (secs(w), a, b))
    say()
    say("| Sortie | Darts | Miles | Minutes | Battery used |")
    say("|---|---|---|---|---|")
    for i, (g, f) in enumerate(groups):
        miles = sum(dist(f.track[j]["p"], f.track[j + 1]["p"]) for j in range(len(f.track) - 1)) / 5280
        say("| %d | %s | %.1f | %.1f | %.0f%% |" % (i + 1, " ".join(s_["id"] for s_ in g), miles, f.t / 60, 100 * f.used))
        open(os.path.join(out, "sortie-%d.waypoints" % (i + 1)), "w").write(mission(sec, g))
    tl = timeline([f.t / 60 for _, f in groups])
    say("planned lay: %.1f h with %d packs and a %d-channel charger; %.1f h with 2 packs and 1 channel" % (tl[-1][1] / 60, PACKS, CHANNELS, timeline([f.t / 60 for _, f in groups], 2, 1)[-1][1] / 60))
    say()
    say("## Wind: sorties needed for the planned darts (wind toward the enemy, plus the gust margin)")
    for wmph in (0, 5, 9, 12, 15, 18):
        def f_(c):
            try: return len(chunk(Sector(c), lay_sequence(plan(Sector(c)))))
            except RuntimeError: return "grounded"
        say("- %d mph: %s" % (wmph, with_params(cfg, {"wind_mph": wmph}, f_)))
    say()
    say("## Simulated lays (%d each)" % runs)
    say("| Case | Whole | Survives any one loss | Darts used | 90th pct darts | Sorties | Hours | Worst warning, 10th pct | Drones lost |")
    say("|---|---|---|---|---|---|---|---|---|")
    def case(label, kv, PP=None, **kw):
        def f_(c):
            sc_ = Sector(c); pp = PP if PP is not None else plan(sc_)
            return run_case(sc_, pp, runs, seed, **kw)
        say(fmt_case(label, with_params(cfg, kv, f_)))
    case("First plan, GPS working, no confirm", {}, PP=OP, jammed=False, confirm=False)
    case("This plan, GPS working, no confirm", {}, jammed=False, confirm=False)
    case("This plan, GPS working, confirm", {}, jammed=False, confirm=True)
    case("This plan, GPS jammed, confirm", {}, jammed=True, confirm=True)
    case("  landings 95% upright", {"P_UPRIGHT": 0.95, "P_TILTED": 0.03}, jammed=True, confirm=True)
    case("  radio hop 800 ft, not 980", {"HOP": 800.0}, jammed=True, confirm=True)
    case("  compass 4 degrees, not 2", {"COMPASS_DEG": 4.0, "COMPASS_SORTIE_DEG": 1.4}, jammed=True, confirm=True)
    case("  15 mph wind", {"wind_mph": 15}, jammed=True, confirm=True)
    case("  14 F, packs not warmed", {"air_temp_f": 14, "packs_warmed": False}, jammed=True, confirm=True)
    # one representative lay for the animation: jammed, confirmed, whole, with a step-back spare, a tilt and a dud
    for k in range(3000):
        L = Lay(sec, P, random.Random(seed * 1000 + k), jammed=True, confirm=True).run(); sc = L.score()
        evs = [d for lg, f in L.sorties for d in lg["drops"]]
        steps = [d for d in evs if "+" in d["id"] and d["state"] == "upright"]
        if sc["whole"] and sc["tolerant"] and not L.lost_drones and steps and any(d["state"] == "tilted" for d in evs) \
           and any(d["state"] == "dud" for d in evs) and len(L.sorties) <= 9 and sc["darts"] <= 31:
            break
    tlL = timeline([f.t / 60 for _, f in L.sorties])
    live = L.graph()
    old_seq = lay_sequence(OP)
    old_pts = {x["id"]: x["p"] for x in old_seq}; old_pts["RX"] = P["rx"]
    old_why = [[round(x["p"][0]), round(x["p"][1]), sec.why_not(x["p"])] for x in old_seq if sec.why_not(x["p"])]
    old_bad = [[[round(c) for c in old_pts[x["anchor"]]], [round(c) for c in x["p"]]] for x in old_seq
               if dist(old_pts[x["anchor"]], x["p"]) > sec.reach(old_pts[x["anchor"]], x["p"])]
    demo = {"sector": cfg, "old_why": old_why, "old_bad_links": old_bad, "packs": PACKS, "channels": CHANNELS, "launch": LAUNCH, "standoff": STANDOFF, "reff": REFF, "front_plan": P["front"], "trunks": P["trunks"],
            "moved": P["notes"]["moved"], "pulled": P["notes"]["pulled"], "old_front": OP["front"], "old_trunks": OP["trunks"],
            "plan": [{"id": s_["id"], "p": s_["p"], "anchor": s_["anchor"]} for s_ in seq],
            "sorties": [{"start_min": round(a, 1), "end_min": round(b, 1), "plan": lg["plan"], "drops": lg["drops"], "track": f.track, "used": lg.get("used")}
                        for (lg, f), (a, b) in zip(L.sorties, tlL)],
            "final": {n: {"p": [round(d["p"][0]), round(d["p"][1])], "ok": d["ok"], "state": d.get("state"), "live": n in live} for n, d in L.darts.items()},
            "links": [[a, b] for a in live for b in live if a < b and L.link(a, b)],
            "score": sc, "seed": seed * 1000 + k}
    json.dump(demo, open(os.path.join(out, "demo-lay.json"), "w"), separators=(",", ":"))
    say()
    say("demo lay (seed %d): %d darts, %d sorties, %.1f h, worst warning %.0f s" % (demo["seed"], sc["darts"], sc["sorties"], sc["hours"], sc["warn"]))
    open(os.path.join(out, "summary.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
