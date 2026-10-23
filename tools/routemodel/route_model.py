"""Route model: guarding a supply road with the tripwire.

Plans a guard on a road map: posts along the road, placed by hand, and a fence of air-dropped
darts about a mile out on every side a drone can come from, joined to the road by trunks: an FPV
fibre from a tip dart in the fence to a post, or with FIBRE off, a row of radio relays. Lays
the fence many times in simulation with the lay model's drop errors, bad landings, radio fading
and drop-then-confirm. Then scores the guard against drones flying in to strike and drones flying
in to land and wait, and against darts dying between repairs.

    py route_model.py [road.json] [--runs 200] [--seed 7] [--out out]

Stdlib only. Reuses tools/laymodel/lay_model.py for the radio, the battery, landings and the lay
loop. Local frame in feet: x along the front, y toward the enemy. Every number marked ASSUME is a
planning number, not a measurement.
"""
import json, math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "laymodel"))
import lay_model as lm
from lay_model import dist, sub, add, mul, lerp, seg_dist, seg_cross

# ---- planning numbers -----------------------------------------------------------------------
FTS = lm.FTS                                   # 60 mph


def derive():
    """Hearing along the ground (~635 ft), the hop (980 ft), fence spacing, and the fence offset
    (~5,316 ft, the position net's minute), from the lay model's planning numbers."""
    global REFF, HOP, STEP, D, POST_SPACING
    REFF = math.sqrt(lm.HEAR ** 2 - lm.ALT ** 2); lm.REFF = REFF
    lm.MEDIAN_HOP = lm.HOP * 10 ** (lm.Z90 * lm.FADE_DB / 10 / lm.PLE); HOP = lm.HOP
    STEP = min(HOP * lm.PLAN_FRAC, 1.8 * REFF)   # a track midway between two fence darts must still pass within hearing
    D = lm.NEED - math.sqrt(REFF ** 2 - (STEP / 2) ** 2)
    POST_SPACING = min(POST_MAX, 0.98 * 2 * math.sqrt(max(1.0, REFF ** 2 - LAND_OFF ** 2)))

THREAT_DEG = 60.0      # drones come from within 60 degrees of the enemy direction ASSUME
TRUNK_EVERY = 10560.0  # a trunk every 2 mi of fence, so no fence dart is more than ~6 hops from one
FIBRE = True           # a trunk is an FPV fibre from a tip dart to a post, not a row of radio relays (untested, T21)
FIBRE_FT = 6336.0      # a tip's spool, about 1.2 mi, as on the position net ASSUME
FIBRE_SLACK = 1.1      # fibre paid out from a drone runs about 10% longer than the straight line ASSUME
P_CUT_DAY = 0.01       # a laid fibre cut by shelling, vehicles or people, a day. A pure guess
END_EXTRA = 300.0      # run each fence 300 ft past where it stops being exposed, as the position net does
POST_MAX = 1100.0      # posts: any landing up to 300 ft off the road passes within hearing of one
POST_RANGE = 2500.0    # post to post: 2 ft whips on stakes, two-ray estimate with 20 dB in hand (T9) ASSUME
POST_SHOULDER = 40.0   # posts stand this far off the road edge
LAND_OFF = 300.0       # ambush drones land within this of the road ASSUME
RECOG_S, HOP_S = 3.0, 0.3   # recognising a drone; one relay hop, fast radio settings ASSUME
WHOLE_S = 55.0
VEH_MPH = 30.0
# daily losses: shelling, traffic, scavenging. Pure guesses; the roll call finds a loss within a day
P_LOSS_DART_DAY, P_LOSS_POST_DAY, REPAIR_DAYS = 0.005, 0.01, 1.0
derive()

# ---- costs, small batch, ours (Projected costs) ASSUME ------------------------------------------
DART_USD, POST_USD, RX_USD = 29.0, 45.0, 22.0   # a post: the dart's board, 4 cells, a 2 ft whip and a stake (est.)
TIP_USD = 94.0                                   # a tip dart: a dart plus ~1.2 mi of fibre and a laser (costs.md, small batch)
END_USD = 20.0                                   # a fibre's end at its post: light detector, connector, box (est.)
DRONE_USD, PACK_WEAR_USD = 850.0, 0.30
KIT_USD = 1397.0 + 360.0 + 100.0                 # the outfitted drone, plus 6 more packs and 2 more charger channels
RECEIVERS = 14                                   # 12 vehicles and 2 checkpoints
POST_LIFE_X = 4.0                                # 4 cells: a post lasts 4 times as long as a dart ASSUME (T12)


# ---- the road -------------------------------------------------------------------------------
class Road:
    def __init__(self, pts):
        self.p = [tuple(map(float, q)) for q in pts]
        self.cum = [0.0]
        for i in range(1, len(self.p)): self.cum.append(self.cum[-1] + dist(self.p[i - 1], self.p[i]))
        self.L = self.cum[-1]

    def seg(self, s):
        s = max(0.0, min(self.L, s))
        for i in range(len(self.p) - 1):
            if s <= self.cum[i + 1] or i == len(self.p) - 2: return i, s
        return len(self.p) - 2, s

    def at(self, s):
        i, s = self.seg(s); a, b = self.p[i], self.p[i + 1]; L = dist(a, b)
        return lerp(a, b, (s - self.cum[i]) / L), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)

    def dist(self, q): return min(seg_dist(q, self.p[i], self.p[i + 1]) for i in range(len(self.p) - 1))

    def proj(self, q):
        best = None
        for i in range(len(self.p) - 1):
            a, b = self.p[i], self.p[i + 1]; d = sub(b, a); L2 = d[0] ** 2 + d[1] ** 2
            u = max(0.0, min(1.0, ((q[0] - a[0]) * d[0] + (q[1] - a[1]) * d[1]) / L2))
            dd = dist(q, lerp(a, b, u))
            if best is None or dd < best[0]: best = (dd, self.cum[i] + u * math.sqrt(L2))
        return best[1]

    def seg_min_dist(self, a, b):
        """Least distance from segment ab to the road."""
        best = 1e18
        for i in range(len(self.p) - 1):
            c, d = self.p[i], self.p[i + 1]
            if seg_cross(a, b, c, d): return 0.0
            best = min(best, seg_dist(a, c, d), seg_dist(b, c, d), seg_dist(c, a, b), seg_dist(d, a, b))
        return best


def boundary_loop(road, r, step=60.0):
    """Points at distance r round the road, in order: left side out, far end cap, right side back, near cap."""
    pts = []
    def side(sign):
        segs = list(range(len(road.p) - 1))
        if sign < 0: segs = segs[::-1]
        out = []
        for k, i in enumerate(segs):
            a, b = road.p[i], road.p[i + 1]
            if sign < 0: a, b = b, a
            L = dist(a, b); t = ((b[0] - a[0]) / L, (b[1] - a[1]) / L); n = (-t[1], t[0])
            m = max(1, int(L / step))
            for j in range(m + 1): out.append(add(lerp(a, b, j / m), mul(n, r)))
            if k < len(segs) - 1:   # round the vertex
                j2 = segs[k + 1]; c, d = road.p[j2], road.p[j2 + 1]
                if sign < 0: c, d = d, c
                L2 = dist(c, d); t2 = ((d[0] - c[0]) / L2, (d[1] - c[1]) / L2); n2 = (-t2[1], t2[0])
                a0, a1 = math.atan2(n[1], n[0]), math.atan2(n2[1], n2[0])
                da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
                for j in range(1, 12): th = a0 + da * j / 12; out.append(add(b, (r * math.cos(th), r * math.sin(th))))
        return out
    def cap(end, t):
        n = (-t[1], t[0]); a0 = math.atan2(n[1], n[0])
        return [add(end, (r * math.cos(a0 - math.pi * j / 160), r * math.sin(a0 - math.pi * j / 160))) for j in range(1, 160)]
    t_end = road.at(road.L)[1]; t_start = road.at(0)[1]
    pts += side(1) + cap(road.p[-1], t_end) + side(-1) + cap(road.p[0], (-t_start[0], -t_start[1]))
    return [q for q in pts if road.dist(q) >= r - 2]


def entry_point(road, start, d, R, r):
    """Where a straight track toward the road first comes within r of it."""
    lo = 0.0
    for t in range(0, int(R), 200):
        if road.dist(add(start, mul(d, t))) <= r:
            hi = float(t)
            for _ in range(10):
                m = (lo + hi) / 2
                if road.dist(add(start, mul(d, m))) <= r: hi = m
                else: lo = m
            return add(start, mul(d, hi))
        lo = float(t)
    return None


def fence_runs(road, r):
    """The fence goes where strike tracks cross the line r from the road, and END_EXTRA beyond."""
    loop = boundary_loop(road, r)
    n = len(loop); ex = [False] * n
    for tr in tracks(road, step=264.0, R=r + 30000.0, deg_step=2.5):
        q = entry_point(road, tr[2], tr[3], tr[4], r)
        if q is None: continue
        i = min(range(n), key=lambda j: (loop[j][0] - q[0]) ** 2 + (loop[j][1] - q[1]) ** 2)
        ex[i] = True
    cum = [0.0]
    for i in range(1, n): cum.append(cum[-1] + dist(loop[i - 1], loop[i]))
    keep = [any(ex[j] for j in range(n) if abs(cum[j] - cum[i]) <= END_EXTRA) for i in range(n)]
    runs, cur = [], []
    for i in range(n):
        if keep[i] and (not cur or dist(cur[-1], loop[i]) < 400): cur.append(loop[i])
        elif keep[i]: runs.append(cur); cur = [loop[i]]
        elif cur: runs.append(cur); cur = []
    if cur: runs.append(cur)
    if len(runs) > 1 and dist(runs[-1][-1], runs[0][0]) < 400 and keep[0] and keep[-1]:
        runs[0] = runs.pop() + runs[0]
    return [rn for rn in runs if len(rn) > 3]


def polyfn(pl):
    cum = [0.0]
    for i in range(1, len(pl)): cum.append(cum[-1] + dist(pl[i - 1], pl[i]))
    def f(u):
        u = max(0.0, min(cum[-1], u))
        for i in range(len(pl) - 1):
            if u <= cum[i + 1]: return lerp(pl[i], pl[i + 1], (u - cum[i]) / max(1e-9, cum[i + 1] - cum[i]))
        return pl[-1]
    return f, cum[-1]


# ---- the plan -------------------------------------------------------------------------------
def plan(sec, road, fence=True):
    posts, s = [], 0.0
    n = max(1, math.ceil(road.L / POST_SPACING))
    for i in range(n + 1):
        p, t = road.at(road.L * i / n); nrm = (-t[1], t[0])
        posts.append({"id": "P%d" % (i + 1), "s": road.L * i / n, "p": add(p, mul(nrm, -POST_SHOULDER))})
    P = {"posts": posts, "runs": [], "seq": []}
    if not fence: return P
    for ri, rn in enumerate(fence_runs(road, D)):
        fn, L = polyfn(rn)
        pts, _ = lm.even_or_greedy(sec, fn, 0.0, L, STEP, {})
        F = [p for u, p in pts]; us = [u for u, p in pts]
        k = max(1, math.ceil(L / TRUNK_EVERY))
        tips = sorted(set(min(range(len(F)), key=lambda i: abs(us[i] - L * j / k)) for j in range(k + 1)))
        trunks = []
        for ti0 in tips:
            # a trunk that would run along a tree belt, or a fibre too long for its spool, can't be
            # laid; try the fence darts either side
            for ti in sorted(range(len(F)), key=lambda i: abs(i - ti0))[:7]:
                tip = F[ti]
                post = min(posts, key=lambda q: dist(q["p"], tip))
                L2 = dist(post["p"], tip)
                if FIBRE:
                    if L2 * FIBRE_SLACK > FIBRE_FT: continue
                    trunks.append({"tip": ti, "post": post["id"], "relays": [], "fibre": True}); break
                g = lambda u, a=post["p"], b=tip, L2=L2: lerp(a, b, u / L2)
                try: tr, _ = lm.even_or_greedy(sec, g, 0.0, L2, HOP * lm.PLAN_FRAC, {})
                except RuntimeError: continue
                trunks.append({"tip": ti, "post": post["id"], "relays": [p for u, p in tr][1:-1]}); break
            else: raise RuntimeError("no trunk can be laid near fence dart %d" % ti0)
        trunks.sort(key=lambda t: t["tip"])
        P["runs"].append({"line": rn, "front": F, "trunks": trunks})
    P["seq"] = lay_sequence(P)
    return P


def lay_sequence(P):
    seq = []
    def push(name, p, anchor, kind, second=None):
        seq.append({"id": name, "p": p, "anchor": anchor, "kind": kind, "second": second})
    for ri, R in enumerate(P["runs"]):
        F, T = R["front"], R["trunks"]
        fid = lambda i: "F%d.%d" % (ri + 1, i + 1)
        def trunk(j):
            t = T[j]; prev = t["post"]
            if t.get("fibre"): push(fid(t["tip"]), F[t["tip"]], prev, "tip"); return
            for i, p in enumerate(t["relays"]):
                name = "T%d.%d.%d" % (ri + 1, j + 1, i + 1); push(name, p, prev, "relay"); prev = name
            push(fid(t["tip"]), F[t["tip"]], prev, "front")
        trunk(0)
        for j in range(len(T) - 1):
            trunk(j + 1)
            a, b = T[j]["tip"], T[j + 1]["tip"]; mid = (a + b) // 2
            for i in range(a + 1, mid + 1): push(fid(i), F[i], fid(i - 1), "front")
            for i in range(b - 1, mid, -1): push(fid(i), F[i], fid(i + 1), "front", second=fid(mid) if i == mid + 1 and mid > a else None)
    return seq


def launch_for(posts, sq):
    """Launch beside the post nearest the sortie's drops; a tip's sortie launches from the post its
    fibre is tied off at."""
    if sq[0]["kind"] == "tip": return tuple(next(q["p"] for q in posts if q["id"] == sq[0]["anchor"]))
    pts = [s["p"] for s in sq]
    c = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    return tuple(min(posts, key=lambda q: dist(q["p"], c))["p"])


def chunk(sec, P):
    out, i, seq = [], 0, P["seq"]
    while i < len(seq):
        k = lm.tip_cap(seq[i:])
        while k > 0:
            lm.LAUNCH = launch_for(P["posts"], seq[i:i + k])
            ok, f = lm.sortie_fits(sec, [s["p"] for s in seq[i:i + k]], tip=seq[i]["kind"] == "tip")
            if ok: break
            k -= 1
        if k == 0: raise RuntimeError("one dart to %s does not fit a battery" % seq[i]["id"])
        out.append((seq[i:i + k], f, lm.LAUNCH)); i += k
    return out


# ---- simulated lay: the lay model's loop, launched from the road ----------------------------
class RouteLay(lm.Lay):
    def __init__(self, sec, P, rng, jammed=True, confirm=True):
        self.sec, self.P, self.rng, self.jammed, self.confirm = sec, P, rng, jammed, confirm
        self.seq = P["seq"]
        self.plan_at = {s["id"]: s["p"] for s in self.seq}
        self.darts = {q["id"]: {"p": q["p"], "ok": True, "logged": q["p"], "post": True} for q in P["posts"]}
        self.fade, self.links = {}, {}
        self.lay_seed = rng.random()
        self.sorties, self.used, self.lost_drones, self.gaps = [], 0, 0, []
        self.holder = {q["id"]: q["id"] for q in P["posts"]}
        self.anchor_of = {s["id"]: s["anchor"] for s in self.seq}
        self.tips_used = 0

    def link(self, a, b):
        if a == b: return False
        da, db = self.darts[a], self.darts[b]
        if not (da["ok"] and db["ok"]): return False
        if da.get("fibre") == b or db.get("fibre") == a: return True   # light down a fibre, no radio
        if da.get("post") and db.get("post"): return dist(da["p"], db["p"]) <= POST_RANGE
        if dist(da["p"], db["p"]) > 2 * HOP: return False
        return lm.Lay.link(self, a, b)

    def run(self):
        queue = [dict(x) for x in self.seq]
        while queue:
            k = lm.tip_cap(queue); tip = queue[0]["kind"] == "tip"
            while k > 1:
                lm.LAUNCH = launch_for(self.P["posts"], queue[:k])
                if lm.sortie_fits(self.sec, [s["p"] for s in queue[:k]], tip=tip)[0]: break
                k -= 1
            todo = queue[:k]
            lm.LAUNCH = launch_for(self.P["posts"], todo)
            f = lm.Flight(self.sec, lm.CAPACITY, self.sec.wind, low=self.jammed, tip=tip); nav = self.nav()
            log = {"plan": [s["id"] for s in todo], "drops": [], "launch": lm.LAUNCH}
            if self.rng.random() < lm.P_DRONE_LOSS:
                self.lost_drones += 1; log["lost"] = True; self.sorties.append((log, f)); continue
            left, done = lm.CAPACITY, 0
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
                    if s["kind"] == "tip":
                        self.tips_used += 1
                        if self.rng.random() >= lm.P_SNAG: self.darts[name]["fibre"] = anchor   # the fibre reached its post
                    if st == "upright": group.append(name)
                    side = self.joined(anchor, group)
                    ok = bool(side) and (second is None or second in self.joined(anchor, group, [second]))
                    if not self.confirm and st == "upright": ok = True; side = [name]
                    ev = {"id": name, "planned": s["id"], "at": [round(f.at[0]), round(f.at[1])], "state": st,
                          "confirmed": bool(ok), "anchor": anchor, "second": second, "joined": bool(side)}
                    log["drops"].append(ev); f.track[-1]["ev"] = ev
                    if ok or not self.confirm:
                        if side: self.holder[s["id"]] = min(side, key=lambda n: dist(self.darts[n]["logged"], s["p"]))
                        break
                    if tries >= lm.MAX_EXTRA: self.gaps.append(s["id"]); break
                    if s["kind"] == "tip":   # a new tip needs a new fibre from its post: next sortie, same spot
                        s["resume"] = (tries + 1, s["p"], []); slipped = True; break
                    if st == "upright":
                        if not side: frm, to = spot, self.darts[anchor]["logged"]
                        else:
                            frm = self.darts[max(side, key=lambda n: -dist(self.darts[n]["logged"], self.darts[second]["logged"]))]["logged"]
                            to = self.darts[second]["logged"]
                        spot = add(frm, mul(sub(to, frm), lm.SPARE_STEP / max(1.0, dist(to, frm))))
                    tries += 1
                    if left == 0 or not f.can_afford(spot):
                        s["resume"] = (tries, spot, group); slipped = True; break
                if slipped: break
                done += 1
            f.land(); log["used"] = round(f.used, 3)
            self.sorties.append((log, f))
            queue = queue[done:]
        return self


# ---- scoring --------------------------------------------------------------------------------
class Net:
    """A snapshot of the guard: which darts and posts are working, and where they are."""
    def __init__(self, road, nodes, linkf):
        self.road = road
        self.ids = list(nodes)
        self.p = {n: nodes[n]["p"] for n in self.ids}
        self.post = {n for n in self.ids if nodes[n].get("post")}
        self.s = {n: road.proj(self.p[n]) for n in self.post}
        self.adj = {n: [] for n in self.ids}
        for i, a in enumerate(self.ids):
            for b in self.ids[i + 1:]:
                if abs(self.p[a][0] - self.p[b][0]) < POST_RANGE + 10 and abs(self.p[a][1] - self.p[b][1]) < POST_RANGE + 10 and linkf(a, b):
                    self.adj[a].append(b); self.adj[b].append(a)
        self.fibre = {}   # tip dart -> the post its fibre ends at
        for n in self.ids:
            o = nodes[n].get("fibre")
            if o in self.p and linkf(n, o):
                self.fibre[n] = o
                if o not in self.adj[n]: self.adj[n].append(o); self.adj[o].append(n)

    def hops(self, dead=(), cut=()):
        """Hops from each node to the posts, and the post its alert arrives at. cut: tip darts whose
        fibre is cut (the tip still relays by radio)."""
        dead = set(dead); h, via, q = {}, {}, []
        for n in self.post:
            if n not in dead: h[n] = 0; via[n] = n; q.append(n)
        i = 0
        while i < len(q):
            a = q[i]; i += 1
            for b in self.adj[a]:
                if b in dead or b in h: continue
                if (b in cut and self.fibre.get(b) == a) or (a in cut and self.fibre.get(a) == b): continue
                if b in self.post: continue
                h[b] = h[a] + 1; via[b] = via[a]; q.append(b)
        return h, via

    def post_hops(self, s1, s2): return math.ceil(abs(s1 - s2) / (POST_RANGE * 0.88))


def tracks(road, step=528.0, R=40000.0, deg_step=5.0):
    out = []
    n = max(1, int(road.L / step)); m = int(round(2 * THREAT_DEG / deg_step))
    for i in range(n + 1):
        s = road.L * i / n; tgt = road.at(s)[0]
        for j in range(m + 1):
            k = -THREAT_DEG + j * deg_step
            d = (math.sin(math.radians(k)), math.cos(math.radians(k)))
            out.append((s, tgt, add(tgt, mul(d, R)), (-d[0], -d[1]), R, k))
    return out


def entries(track, pts):
    """Where a straight track first comes within hearing of each node, as distance flown."""
    s_t, tgt, start, d, R, k = track; out = []
    for n, p in pts:
        m = (start[0] - p[0], start[1] - p[1]); b = -(m[0] * d[0] + m[1] * d[1])
        c = m[0] * m[0] + m[1] * m[1] - REFF * REFF; disc = b * b - c
        if disc < 0: continue
        e = b - math.sqrt(disc)
        if e < 0: e = 0.0 if c < 0 else None
        if e is not None and e <= R: out.append((e, n))
    out.sort()
    return out


def warn_of(net, track, ents, h, via):
    s_t, tgt, start, d, R, k = track
    best = None
    for e, n in ents:
        if n not in h: continue
        w = (R - e) / FTS - RECOG_S - HOP_S * (h[n] + net.post_hops(net.s[via[n]], s_t))
        if best is None or w > best: best = w
        if (R - e) / FTS < (best or -1e9): break   # later entries cannot beat it
    return best if best is not None else -1e9


def score_tracks(net, T, dead=(), cache=None, cut=()):
    h, via = net.hops(dead, cut)
    pts = [(n, net.p[n]) for n in net.ids if n in h]
    ws = []
    for i, tr in enumerate(T):
        ents = cache[i] if cache is not None else entries(tr, pts)
        ws.append(warn_of(net, tr, ents, h, via))
    return ws


def landing_spots(road, step=264.0, offs=(-300, -200, -100, 100, 200, 300)):
    out = []
    n = max(1, int(road.L / step))
    for i in range(n + 1):
        p, t = road.at(road.L * i / n); nrm = (-t[1], t[0])
        for o in offs: out.append(add(p, mul(nrm, o)))
    return out


def score_landings(net, spots, dead=()):
    """A landing is placed if a working post hears the drone come down; the stretch to search is
    centred on the post that heard it loudest (the nearest)."""
    dead = set(dead); heard, two, errs = 0, 0, []
    posts = [(n, net.p[n]) for n in net.post if n not in dead]
    for q in spots:
        ds = sorted(dist(q, p) for n, p in posts if dist(q, p) <= REFF)
        if ds: heard += 1; errs.append(ds[0]); two += len(ds) >= 2
    errs.sort()
    return {"heard": heard / len(spots), "two": two / len(spots),
            "err50": errs[len(errs) // 2] if errs else None, "err90": errs[int(0.9 * len(errs))] if errs else None}


def summarise(ws):
    ok = [w for w in ws if w > -1e8]
    return {"min": min(ws), "p10": lm.pct(ws, 0.1), "share55": sum(w >= WHOLE_S for w in ws) / len(ws),
            "share30": sum(w >= 30 for w in ws) / len(ws), "share10": sum(w >= 10 for w in ws) / len(ws),
            "median": lm.pct(ws, 0.5), "heard": len(ok) / len(ws)}


def planned_nodes(P):
    nodes = {q["id"]: {"p": q["p"], "post": True} for q in P["posts"]}
    for s in P["seq"]: nodes[s["id"]] = {"p": s["p"], "fibre": s["anchor"] if s["kind"] == "tip" else None}
    return nodes


def planned_link(sec, nodes):
    def f(a, b):
        if nodes[a].get("fibre") == b or nodes[b].get("fibre") == a: return True
        pa, pb = nodes[a]["p"], nodes[b]["p"]
        if nodes[a].get("post") and nodes[b].get("post"): return dist(pa, pb) <= POST_RANGE
        return dist(pa, pb) <= sec.reach(pa, pb) + 1
    return f


# ---- report ---------------------------------------------------------------------------------
def fmt_s(w): return "none" if w < -1e8 else "%.0f s" % w


def main(argv):
    path = next((a for a in argv if a.endswith(".json")), os.path.join(os.path.dirname(os.path.abspath(__file__)), "road-radial.json"))
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else 200
    seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 7
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    tag = os.path.splitext(os.path.basename(path))[0]
    os.makedirs(out, exist_ok=True)
    cfg = json.load(open(path)); sec = lm.Sector(cfg); road = Road(cfg["road"])
    md = []
    def say(line=""): print(line, flush=True); md.append(line)
    miles = road.L / 5280
    say("# %s: %.2f mi of road" % (cfg["name"], miles))
    T = tracks(road); spots = landing_spots(road)

    # ---- posts only
    P0 = plan(sec, road, fence=False)
    n0 = planned_nodes(P0); net0 = Net(road, n0, planned_link(sec, n0))
    w0 = summarise(score_tracks(net0, T)); l0 = score_landings(net0, spots)
    # ---- posts and fence
    P = plan(sec, road, fence=True)
    nodes = planned_nodes(P); net = Net(road, nodes, planned_link(sec, nodes))
    h, via = net.hops()
    cut = [n for n in nodes if n not in h]
    wsP = score_tracks(net, T); wP = summarise(wsP); lP = score_landings(net, spots)
    nf = sum(len(R["front"]) for R in P["runs"]); nt = sum(len(t["relays"]) for R in P["runs"] for t in R["trunks"])
    ntr = sum(len(R["trunks"]) for R in P["runs"]); tips = [s["id"] for s in P["seq"] if s["kind"] == "tip"]
    fence_len = sum(polyfn(R["line"])[1] for R in P["runs"]) / 5280
    fibre_mi = sum(dist(nodes[t]["p"], nodes[nodes[t]["fibre"]]["p"]) for t in tips) * FIBRE_SLACK / 5280
    say()
    say("## Plan")
    if FIBRE:
        say("posts %d (one every %.0f ft), fence %.1f mi in %d run(s): %d fence darts, %d of them tip darts on fibre trunks to a post (%.1f mi of fibre, the longest %.0f ft laid); %d air-dropped darts in all"
            % (len(P["posts"]), road.L / (len(P["posts"]) - 1), fence_len, len(P["runs"]), nf, len(tips), fibre_mi,
               max(dist(nodes[t]["p"], nodes[nodes[t]["fibre"]]["p"]) for t in tips) * FIBRE_SLACK, nf + nt))
    else:
        say("posts %d (one every %.0f ft), fence %.1f mi in %d run(s): %d fence darts, %d radio trunks with %d relays; %d air-dropped darts in all"
            % (len(P["posts"]), road.L / (len(P["posts"]) - 1), fence_len, len(P["runs"]), nf, ntr, nt, nf + nt))
    say("per mile of road: %.1f posts, %.1f darts; longest route to a post %d hops; nodes cut off in the plan: %d"
        % (len(P["posts"]) / miles, (nf + nt) / miles, max(h.values()), len(cut)))
    say()
    say("## Strike tracks (drone flying in at 60 mph within %d degrees of the enemy direction, %d tracks)" % (THREAT_DEG, len(T)))
    say("| Guard | Darts | Worst warning | 10th pct | Median | Tracks with a minute (55 s) | 30 s | 10 s |")
    say("|---|---|---|---|---|---|---|---|")
    for lab, n_, w in (("Posts only", len(P0["posts"]), w0), ("Posts and fence", len(P["posts"]) + nf + nt, wP)):
        say("| %s | %d | %s | %s | %s | %.0f%% | %.0f%% | %.0f%% |" % (lab, n_, fmt_s(w["min"]), fmt_s(w["p10"]), fmt_s(w["median"]), 100 * w["share55"], 100 * w["share30"], 100 * w["share10"]))
    say()
    say("## Landings within %d ft of the road (%d spots)" % (LAND_OFF, len(spots)))
    say("heard by a post %.0f%%, by two or more %.0f%%; distance to the loudest post: median %.0f ft, 90th pct %.0f ft"
        % (100 * lP["heard"], 100 * lP["two"], lP["err50"], lP["err90"]))
    far = landing_spots(road, offs=(-1500, -1000, -600, 600, 1000, 1500))
    lf = score_landings(net, far)
    say("landings 600-1,500 ft off the road: heard by a post %.0f%% (the rest only as a drone in, none out)" % (100 * lf["heard"]))

    # ---- one dead node at a time, on the plan
    ptsall = [(n, net.p[n]) for n in net.ids if n in h]
    cache = [entries(tr, ptsall) for tr in T]
    worst_one, bad = 1.0, 0
    for n in nodes:
        sh = summarise(score_tracks(net, T, dead=[n], cache=cache))["share55"]
        worst_one = min(worst_one, sh); bad += sh < wP["share55"] - 0.02
    say()
    say("## One dead node, on the plan")
    say("worst single loss leaves %.0f%% of tracks with a minute; %d of %d nodes cost more than 2 points" % (100 * worst_one, bad, len(nodes)))
    one_cut = None
    if FIBRE:
        one_cut = min(summarise(score_tracks(net, T, cache=cache, cut=[t]))["share55"] for t in tips)
        say("worst single fibre cut leaves %.0f%% of tracks with a minute (the tip still relays to its neighbours by radio)" % (100 * one_cut))

    # ---- holes between repairs
    rng = random.Random(seed); snaps = []
    for _ in range(150):
        dead = [n for n in nodes if rng.random() < (P_LOSS_POST_DAY if nodes[n].get("post") else P_LOSS_DART_DAY) * REPAIR_DAYS]
        cuts = [t for t in tips if rng.random() < P_CUT_DAY * REPAIR_DAYS] if FIBRE else []
        ws = score_tracks(net, T, dead=dead, cache=cache, cut=cuts)
        snaps.append((len(dead) + len(cuts), summarise(ws)["share55"], score_landings(net, spots, dead)["heard"]))
    say()
    say("## Holes between repairs (each dart lost %.1f%% a day, each post %.1f%%%s, found and fixed within %g day)"
        % (100 * P_LOSS_DART_DAY, 100 * P_LOSS_POST_DAY, ", each fibre cut %.0f%%" % (100 * P_CUT_DAY) if FIBRE else "", REPAIR_DAYS))
    say("dead at a time: mean %.1f; tracks with a minute: mean %.0f%%, worst day %.0f%%; landings heard: mean %.0f%%"
        % (sum(a for a, b, c in snaps) / len(snaps), 100 * sum(b for a, b, c in snaps) / len(snaps), 100 * min(b for a, b, c in snaps), 100 * sum(c for a, b, c in snaps) / len(snaps)))

    # ---- laying the fence
    groups = chunk(sec, P)
    tl6 = lm.timeline([f.t / 60 for g, f, l in groups]); tl12 = lm.timeline([f.t / 60 for g, f, l in groups], 12, 4)
    say()
    say("## Laying the fence")
    say("planned: %d darts in %d sorties; %.1f h with 6 packs and 2 charger channels, %.1f h with 12 packs and 4" % (len(P["seq"]), len(groups), tl6[-1][1] / 60, tl12[-1][1] / 60))
    for i, (g, f, l) in enumerate(groups):
        lm.LAUNCH = l
        open(os.path.join(out, "%s-sortie-%d.waypoints" % (tag, i + 1)), "w").write(lm.mission(sec, g))
    res = []
    rng = random.Random(seed)
    for r in range(runs):
        L = RouteLay(sec, P, rng).run()
        live = {n: d for n, d in L.darts.items() if d["ok"]}
        nl = Net(road, live, L.link)
        hh, vv = nl.hops()
        ptsl = [(n, nl.p[n]) for n in nl.ids if n in hh]
        ws = [warn_of(nl, tr, entries(tr, ptsl), hh, vv) for tr in T[::3]]
        dur = [f.t / 60 for lg, f in L.sorties]
        res.append({"darts": L.used, "tips": L.tips_used, "sorties": len(L.sorties), "h6": lm.timeline(dur)[-1][1] / 60, "h12": lm.timeline(dur, 12, 4)[-1][1] / 60,
                    "share55": sum(w >= WHOLE_S for w in ws) / len(ws), "lost": L.lost_drones, "gaps": len(L.gaps), "L": L})
    m = lambda k: sum(x[k] for x in res) / len(res)
    say("simulated, GPS jammed, confirm, %d lays: darts %.1f (9 in 10 within %d), %.1f of them tip darts (9 in 10 within %d), sorties %.1f, %.1f h (6 packs) / %.1f h (12 packs), drones lost %.2f, points left for repair %.2f"
        % (runs, m("darts"), lm.pct([x["darts"] for x in res], 0.9), m("tips"), lm.pct([x["tips"] for x in res], 0.9), m("sorties"), m("h6"), m("h12"), m("lost"), m("gaps")))
    say("tracks with a minute after the lay: mean %.0f%%, lays with at least 97%%: %.0f%%"
        % (100 * m("share55"), 100 * sum(x["share55"] >= 0.97 for x in res) / len(res)))
    stats = {"miles": miles, "posts": len(P["posts"]), "fence_darts": nf, "relays": nt, "air": nf + nt, "fence_mi": fence_len,
             "fibre": FIBRE, "trunks": ntr, "tips": len(tips), "fibre_mi": fibre_mi, "one_cut": one_cut,
             "lay_tips": m("tips"), "lay_tips90": lm.pct([x["tips"] for x in res], 0.9),
             "warn_posts": w0, "warn_fence": wP, "land": lP, "land_far": lf, "lay_darts": m("darts"), "lay_darts90": lm.pct([x["darts"] for x in res], 0.9),
             "lay_sorties": m("sorties"), "lay_h6": m("h6"), "lay_h12": m("h12"), "lay_lost": m("lost"), "lay_share55": m("share55"),
             "snap_dead": sum(a for a, b, c in snaps) / len(snaps), "snap_share55": sum(b for a, b, c in snaps) / len(snaps),
             "snap_worst": min(b for a, b, c in snaps), "snap_land": sum(c for a, b, c in snaps) / len(snaps), "one_worst": worst_one}
    say()
    say("## Costs, ours, small batch (est.)")
    carry_tips = stats["lay_tips90"] + (1 if FIBRE else 0)                      # one spare for a cut fibre
    carry_air, carry_posts = 10 * math.ceil((stats["lay_darts90"] - stats["lay_tips90"]) / 10), len(P["posts"]) + 4
    pkg = carry_air * DART_USD + carry_tips * TIP_USD + len(tips) * END_USD + carry_posts * POST_USD + RECEIVERS * RX_USD + KIT_USD
    relay_cost = ((stats["lay_darts"] - stats["lay_tips"]) * DART_USD + stats["lay_tips"] * TIP_USD
                  + stats["lay_lost"] * DRONE_USD + stats["lay_sorties"] * PACK_WEAR_USD)
    say("package: %d air-dropped darts, %d tip darts and %d fibre ends, %d posts, %d receivers, outfitted drone with 12 packs and 4 channels: $%.0f ($%.0f a mile)"
        % (carry_air, carry_tips, len(tips), carry_posts, RECEIVERS, pkg, pkg / miles))
    say("one re-lay of the fence: $%.0f (%.0f darts, %.1f of them tip darts, %.2f drones, pack wear)" % (relay_cost, stats["lay_darts"], stats["lay_tips"], stats["lay_lost"]))
    say("| Dart cell life | Fence re-lays a year | Fence | Posts | Repairs between re-lays | A year | A mile a year |")
    say("|---|---|---|---|---|---|---|")
    yearly = {}
    for wk in (2, 4, 12):
        n = 52.0 / wk
        fence = n * relay_cost
        posts = 52.0 / (wk * POST_LIFE_X) * len(P["posts"]) * POST_USD
        lost_d = stats["air"] * P_LOSS_DART_DAY * 365; lost_p = len(P["posts"]) * P_LOSS_POST_DAY * 365
        lost_t = len(tips) * P_LOSS_DART_DAY * 365; cuts = len(tips) * P_CUT_DAY * 365   # a cut fibre: a new tip, on its own sortie
        rep = (lost_d * DART_USD + lost_p * POST_USD + lost_d / lm.CAPACITY * (lm.P_DRONE_LOSS * DRONE_USD + PACK_WEAR_USD)
               + lost_t * (TIP_USD - DART_USD) + cuts * (TIP_USD + lm.P_DRONE_LOSS * DRONE_USD + PACK_WEAR_USD))
        tot = fence + posts + rep; yearly[wk] = tot
        say("| %d weeks | %.1f | $%.0f | $%.0f | $%.0f | $%.0f | $%.0f |" % (wk, n, fence, posts, rep, tot, tot / miles))
    stats.update({"pkg": pkg, "pkg_mile": pkg / miles, "relay_cost": relay_cost, "yearly": yearly, "carry_air": carry_air, "carry_tips": carry_tips, "carry_posts": carry_posts})
    json.dump(stats, open(os.path.join(out, "%s-stats.json" % tag), "w"), indent=1)
    if "--demo" in argv: demo(cfg, sec, road, P, nodes, net, out, stats)
    if "--cases" in argv:
        say()
        say("## If the planning numbers are wrong (%d lays each)" % max(10, runs // 4))
        say("| Case | Posts | Air-dropped darts | Per mile | Tracks with a minute, plan | Darts used a lay | Sorties |")
        say("|---|---|---|---|---|---|---|")
        for lab, kv in (("Plan", {}), ("Drones come within 45 degrees, not 60", {"THREAT_DEG": 45.0}),
                        ("Drones come within 75 degrees", {"THREAT_DEG": 75.0}), ("Radio hop 800 ft, not 980", {"HOP": 800.0}),
                        ("Hearing 500 ft, not 656", {"HEAR": 500.0}), ("A trunk every 3 mi, not 2", {"TRUNK_EVERY": 15840.0}),
                        ("Landings 95% upright, not 85%", {"P_UPRIGHT": 0.95, "P_TILTED": 0.03}),
                        ("1 fibre in 5 breaks while laid, not 1 in 20", {"P_SNAG": 0.20}),
                        ("The last plan: radio relay trunks", {"FIBRE": False})):
            r = case_row(cfg, kv, max(10, runs // 4), seed)
            say("| %s | %d | %d | %.1f | %.0f%% | %.1f | %.1f |" % (lab, r["posts"], r["air"], (r["posts"] + r["air"]) / miles, 100 * r["share55"], r["darts"], r["sorties"]))
    open(os.path.join(out, "%s-summary.md" % tag), "w", encoding="utf-8").write("\n".join(md) + "\n")


def case_row(cfg, kv, runs, seed):
    g, gl = globals(), vars(lm)
    where = lambda k: g if k == "FIBRE" else gl if k in gl else g     # planning numbers live in the lay model; route ones here
    old = {k: where(k)[k] for k in kv}
    for k, v in kv.items(): where(k)[k] = v
    derive()
    try:
        sec = lm.Sector(cfg); road = Road(cfg["road"]); P = plan(sec, road)
        nodes = planned_nodes(P); net = Net(road, nodes, planned_link(sec, nodes)); T = tracks(road)
        share = summarise(score_tracks(net, T))["share55"]
        rng = random.Random(seed); used = sorties = 0
        for _ in range(runs):
            L = RouteLay(sec, P, rng).run(); used += L.used; sorties += len(L.sorties)
        return {"posts": len(P["posts"]), "air": len(P["seq"]), "share55": share, "darts": used / runs, "sorties": sorties / runs}
    finally:
        for k, v in old.items(): where(k)[k] = v
        derive()


# ---- the animation's data: the plan, and three drones scored by the model -------------------
def demo(cfg, sec, road, P, nodes, net, out, stats):
    h, via = net.hops()
    pts = [(n, net.p[n]) for n in net.ids if n in h]
    def path_home(n):
        """The relay path from n to its post: walk down the hop count."""
        path = [n]
        while h[path[-1]] > 0:
            a = path[-1]; path.append(min((b for b in net.adj[a] if b in h and h[b] == h[a] - 1), key=lambda b: dist(net.p[b], net.p[a])))
        return path
    def heard_along(poly, step=88.0):
        """For a flight path, the times (s at 60 mph) each node can hear it."""
        fn, L = polyfn(poly); hear = {}
        u = 0.0
        while u <= L:
            q = fn(u)
            for n, p in pts:
                if dist(q, p) <= REFF: hear.setdefault(n, []).append(round(u / FTS, 1))
            u += step
        return {n: [v[0], v[-1]] for n, v in hear.items()}, L / FTS
    events = []
    # 1. a strike drone, flying in to hunt the road
    s1 = road.L * 0.42; tgt, t = road.at(s1); k = 35
    d = (math.sin(math.radians(k)), math.cos(math.radians(k))); start = add(tgt, mul(d, 12000))
    hunt_end = road.at(s1 - 2400)[0]
    out_pt = add(hunt_end, (6500, 9000))
    poly = [start, tgt, hunt_end, out_pt]
    hear, Lt = heard_along(poly)
    first = min(hear, key=lambda n: hear[n][0])
    arrive = 12000 / FTS
    warn = arrive - hear[first][0] - RECOG_S - HOP_S * (h[first] + net.post_hops(net.s[via[first]], s1))
    events.append({"kind": "strike", "path": poly, "heard": hear, "first": first, "home": path_home(first), "arrive": round(arrive, 1),
                   "warn": round(warn, 1), "target_s": s1, "dur": round(Lt, 1),
                   "hot": [max(0, s1 - 5280), min(road.L, s1 + 5280)]})
    # 2. an ambush drone, flying in to land by the road
    s2 = road.L * 0.8; p2, t2 = road.at(s2); nrm = (-t2[1], t2[0])
    spot = add(p2, mul(nrm, 180)); k = -25
    d = (math.sin(math.radians(k)), math.cos(math.radians(k))); start = add(spot, mul(d, 11000))
    poly = [start, add(spot, mul(d, 600)), spot]
    hear, Lt = heard_along(poly)
    first = min(hear, key=lambda n: hear[n][0])
    posts_heard = sorted((n for n in hear if n in net.post), key=lambda n: dist(net.p[n], spot))
    events.append({"kind": "ambush", "path": poly, "heard": hear, "first": first, "home": path_home(first), "spot": spot,
                   "loud": posts_heard[0], "posts": posts_heard, "err": round(dist(net.p[posts_heard[0]], spot)),
                   "spot_s": s2, "dur": round(Lt, 1)})
    # 3. a gap: a drone carried in on foot and launched 500 ft from the road
    s3 = road.L * 0.18; p3, t3 = road.at(s3); nrm = (-t3[1], t3[0])
    lp = add(p3, mul(nrm, 520)); truck = road.at(s3 - 300)[0]
    poly = [lp, truck]
    hear, Lt = heard_along(poly, step=20.0)
    first = min(hear, key=lambda n: hear[n][0])
    events.append({"kind": "inside", "path": poly, "heard": hear, "first": first, "home": [first], "launch": lp,
                   "target_s": s3 - 300, "warn": round(max(0.0, Lt - hear[first][0] - RECOG_S), 1), "dur": round(Lt, 1)})
    links = [[a, b] for a in net.ids for b in net.adj[a] if a < b]
    D_ = {"cfg": cfg, "road": road.p, "L": road.L, "posts": [{"id": q["id"], "p": q["p"], "s": q["s"]} for q in P["posts"]],
          "runs": [{"line": R["line"][::4] + [R["line"][-1]], "front": R["front"], "trunks": R["trunks"]} for R in P["runs"]],
          "nodes": {n: {"p": [round(nodes[n]["p"][0]), round(nodes[n]["p"][1])], "post": bool(nodes[n].get("post")),
                        "tip": n in net.fibre, "h": h.get(n), "s": round(road.proj(nodes[n]["p"]))} for n in nodes},
          "links": [l for l in links if net.fibre.get(l[0]) != l[1] and net.fibre.get(l[1]) != l[0]],
          "fibres": [[t, o] for t, o in sorted(net.fibre.items())], "reff": REFF, "D": D, "fts": FTS, "events": events, "veh_fts": VEH_MPH * 5280 / 3600,
          "stats": {k: v for k, v in stats.items() if not isinstance(v, dict) or k in ("warn_fence", "land")}}
    json.dump(D_, open(os.path.join(out, "route-demo.json"), "w"), separators=(",", ":"))


if __name__ == "__main__":
    main(sys.argv[1:])
