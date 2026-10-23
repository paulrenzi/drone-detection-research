"""Jamming model: how far a jammer blinds a dart, and what that does to the position net and the
road guard.

A dart's radio is jammed when the jammer's power in our 125 kHz channel, at the dart, is more than
the margin the link has in hand above the noise. Near the ground, nobody knows how fast a jammer's
signal fades with distance, so the model gives two bounds:

  low:  the ground hides a jammer as it hides our darts. Calibrated so that a dart's own signal
        dies at the lay model's 980 ft hop, then corrected for each antenna's height.
  high: plain two-ray loss over flat open ground, with none of the extra loss our hops suffer.

Measured hops near the ground are far shorter than plain two-ray predicts, so the truth is
probably nearer the low bound for a jammer near the ground, and nearer the high bound for one up
high. T19, run at range from a real jammer, settles it.

A jammed dart still hears drones and can still transmit; it cannot receive, so it cannot relay.

    py jam_model.py [--out out]

Stdlib only. Every number marked ASSUME is a planning number, not a measurement.
"""
import json, math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "laymodel")); sys.path.insert(0, os.path.join(HERE, "..", "routemodel"))
import lay_model as lm
import route_model as rm
from lay_model import dist

# ---- the radio -------------------------------------------------------------------------------
TX_DBM = 22.0          # SX1262 at full power
BW_KHZ = 125.0
NF_DB = 6.0
SNR_MIN = -12.5        # SF9 ASSUME: the settings are not chosen; SF7 is about 5 dB easier to jam, SF12 about 7.5 dB harder
NOISE = -174 + 10 * math.log10(BW_KHZ * 1e3) + NF_DB
MARGIN = lm.Z90 * lm.FADE_DB   # a median hop has about 5 dB in hand at the 980 ft hop
F_MHZ = 915.0
REF_FT = 3.3           # the height of the dart antennas the 980 ft hop assumes

# ---- jammers (ASSUME: powers and heights are typical of what is sold, not measured) -----------
# Most mobile jammers cover 868-915 MHz (Armada International, Feb 2026). We assume the power is
# spread evenly over 860-940 MHz.
JAMMERS = [
    {"name": "Trench jammer, 20 W, 5 ft up", "w": 20.0, "mhz": 80.0, "h": 5.0},
    {"name": "Vehicle jammer, 100 W, 8 ft up", "w": 100.0, "mhz": 80.0, "h": 8.0},
    {"name": "Jammer on a mast, 50 W, 33 ft up", "w": 50.0, "mhz": 80.0, "h": 33.0},
    {"name": "A LoRa hunter, 20 W all in our channel, 5 ft up", "w": 20.0, "mhz": BW_KHZ / 1000, "h": 5.0},
]
TARGETS = [
    {"name": "a dart", "h": REF_FT},
    {"name": "a post (whip on a stake)", "h": 5.0},
    {"name": "the position's raised receiver", "h": 23.0},
]


def in_channel(j): return 10 * math.log10(j["w"] * 1000) - 10 * math.log10(j["mhz"] * 1000 / BW_KHZ)


def reach_low(j, h_rx):
    """Calibrated: a dart's signal dies at the 980 ft hop; the jammer's fades the same way."""
    x = in_channel(j) - MARGIN - TX_DBM + SNR_MIN + 20 * math.log10(j["h"] / REF_FT) + 20 * math.log10(h_rx / REF_FT)
    return lm.MEDIAN_HOP * 10 ** (x / 40)


def reach_high(j, h_rx):
    """Plain two-ray over open ground (free space until the break point)."""
    allowed = in_channel(j) - (NOISE + MARGIN)
    hj, hr = j["h"] * 0.3048, h_rx * 0.3048
    lam = 299.792458 / F_MHZ
    def pl(d):
        fs = 20 * math.log10(4 * math.pi * d / lam)
        return max(fs, 40 * math.log10(d) - 20 * math.log10(hj * hr))
    lo, hi = 1.0, 1e6
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        if pl(mid) < allowed: lo = mid
        else: hi = mid
    return lo / 0.3048


def reach(j, h_rx, bound): return reach_low(j, h_rx) if bound == "low" else reach_high(j, h_rx)


# ---- the position net -------------------------------------------------------------------------
def position_net(bound, own=True, enemy=True, rx_fwd=0.0, jammer=0):
    """The lay model's planned net with our trench jammers at the positions and the enemy's along
    its edge, all switched on. rx_fwd moves the receiver straight forward of the positions, toward
    the net, on a wire (or a one-way fibre) back to the dugout."""
    cfg = json.load(open(os.path.join(HERE, "..", "laymodel", "sector.json")))
    cfg["receiver"] = [cfg["receiver"][0], cfg["receiver"][1] + rx_fwd]   # the trunks are planned to it
    sec = lm.Sector(cfg); P = lm.plan(sec)
    n = lm.Lay(sec, P, random.Random(0))
    for s_ in lm.lay_sequence(P): n.darts[s_["id"]] = {"p": s_["p"], "ok": True, "logged": s_["p"]}
    J = jammer_points(cfg, own, enemy)
    tj = JAMMERS[jammer]
    deaf = set()
    for name, d in n.darts.items():
        h = TARGETS[2]["h"] if name == "RX" and not rx_fwd else REF_FT   # a forward receiver is a dart with a tail
        if any(dist(d["p"], q) < reach(tj, h, bound) for q in J): deaf.add(name)
    # the receiver's wire back to the dugout is not a radio link; the rx-to-root hop is
    link = lambda a, b: a != b and dist(n.darts[a]["p"], n.darts[b]["p"]) <= sec.reach(n.darts[a]["p"], n.darts[b]["p"])
    seen, q = {"RX"}, ["RX"]
    while q:
        a = q.pop()
        if a in deaf: continue          # a jammed node cannot receive, so cannot pass anything on
        for b in n.darts:
            if b not in seen and link(a, b): seen.add(b); q.append(b)
    if "RX" in deaf: seen = {"RX"}
    w = n.warning(seen)
    return {"deaf": len(deaf - {"RX"}), "rx_deaf": "RX" in deaf, "reach": len(seen) - 1, "darts": len(n.darts) - 1, "warn": w}


def jammer_points(cfg, own, enemy, every=1640.0):
    pts = []
    if own:
        for p in cfg.get("positions", []): pts.append(tuple(p))
        if "positions_y" in cfg:
            x = -30000.0
            while x <= 30000: pts.append((x, cfg["positions_y"])); x += every
    if enemy:
        e = cfg["enemy_edge"]
        for i in range(len(e) - 1):
            L = dist(e[i], e[i + 1]); k = max(1, int(L / every))
            for t in range(k + 1): pts.append(lm.lerp(e[i], e[i + 1], t / k))
    return pts


# ---- the road guard ---------------------------------------------------------------------------
def hops_deaf(net, deaf, wired):
    """Hops to the road when deaf nodes cannot receive. On a wired spine every post shares what any
    post has, so a post that cannot receive by radio still passes on what it heard itself."""
    h, via, q = {}, {}, []
    for p in net.post:
        h[p] = 0; via[p] = p; q.append(p)
    i = 0
    while i < len(q):
        a = q[i]; i += 1
        if a in deaf: continue
        for b in net.adj[a]:
            if b in h or b in net.post: continue
            h[b] = h[a] + 1; via[b] = via[a]; q.append(b)
    return h, via


def road_case(path, bound, convoy=True, lines=False, wired=True):
    """Share of strike tracks with a minute, with jammers on. convoy: a vehicle jammer at the
    point each track aims at (the truck it would hit). lines: our trench jammers along our line
    and the enemy's along its edge."""
    cfg = json.load(open(path)); sec = lm.Sector(cfg); road = rm.Road(cfg["road"])
    P = rm.plan(sec, road); nodes = rm.planned_nodes(P); net = rm.Net(road, nodes, rm.planned_link(sec, nodes))
    T = rm.tracks(road)
    fixed = set()
    if lines:
        J = jammer_points(cfg, True, True); tj = JAMMERS[0]
        for n in net.ids:
            hgt = 5.0 if n in net.post else REF_FT
            if any(dist(net.p[n], q) < reach(tj, hgt, bound) for q in J): fixed.add(n)
    vj = JAMMERS[1]
    r_post, r_dart = reach(vj, 5.0, bound), reach(vj, REF_FT, bound)
    ok = 0; cache = {}
    for tr in T:
        s_t, tgt = tr[0], tr[1]
        deaf = set(fixed)
        if convoy:
            for n in net.ids:
                if dist(net.p[n], tgt) < (r_post if n in net.post else r_dart): deaf.add(n)
        key = frozenset(deaf)
        if key not in cache: cache[key] = hops_deaf(net, deaf, wired)
        h, via = cache[key]
        pts = [(n, net.p[n]) for n in net.ids if n in h]
        if not wired and convoy:
            continue    # a radio-only guard: the truck's receiver and the posts near it are deaf
        w = rm.warn_of(net, tr, rm.entries(tr, pts), h, via)
        ok += w >= rm.WHOLE_S
    return {"share55": ok / len(T), "fixed_deaf": len(fixed), "nodes": len(net.ids)}


def main(argv):
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    md = []
    def say(line=""): print(line, flush=True); md.append(line)
    say("# Jamming: how far a jammer blinds our radio, and what that does to the nets")
    say()
    say("Assumed: jammer power spread over 860-940 MHz, SF9, 125 kHz, 5 dB link margin, always on. Near the ground: the "
        "jammer's signal fades as our darts' does (the main estimate for a jammer near the ground). Clear path: plain two-ray "
        "over open ground while our hops stay as short as planned (the worst case; nearer the truth for a jammer up high).")
    say()
    say("## Reach: inside this distance the radio cannot receive")
    say("| Jammer | " + " | ".join(t["name"] for t in TARGETS) + " |")
    say("|---|" + "---|" * len(TARGETS))
    reach_tab = {}
    for j in JAMMERS:
        cells = []
        for t in TARGETS:
            lo, hi = reach_low(j, t["h"]), reach_high(j, t["h"])
            reach_tab[(j["name"], t["name"])] = (lo, hi)
            cells.append("%s to %s" % (ft(lo), ft(hi)))
        say("| %s | %s |" % (j["name"], " | ".join(cells)))
    say()
    say("## The position net (the lay model's sector), every jammer on")
    say("| Case | Path | Darts jammed | Receiver jammed | Darts that reach the unit | Worst warning |")
    say("|---|---|---|---|---|---|")
    pos = {}
    for lab, kw in (("Enemy trench jammers along their edge", {"own": False}),
                    ("LoRa hunters along their edge", {"own": False, "jammer": 3}),
                    ("Our trench jammers at the positions", {"enemy": False}),
                    ("Ours, receiver 1,000 ft forward on a wire, at dart height", {"enemy": False, "rx_fwd": 1000.0}),
                    ("Ours, receiver 0.5 mi forward on a fibre", {"enemy": False, "rx_fwd": 2640.0})):
        for b in ("low", "high"):
            r = position_net(b, **kw); pos[(lab, b)] = r
            say("| %s | %s | %d | %s | %d of %d | %s |" % (lab, {"low": "near the ground", "high": "clear"}[b], r["deaf"], "yes" if r["rx_deaf"] else "no", r["reach"], r["darts"], rm.fmt_s(r["warn"])))
    say()
    say("## The road guard: share of strike tracks with a minute (55 s)")
    say("| Road | Case | Near the ground | Clear path |")
    say("|---|---|---|---|")
    road = {}
    for f in ("road-lateral.json", "road-radial.json"):
        p = os.path.join(HERE, "..", "routemodel", f)
        name = json.load(open(p))["name"]
        for lab, kw in (("Our and the enemy's trench jammers on", {"convoy": False, "lines": True}),
                        ("The truck's own jammer on, radio guard", {"convoy": True, "wired": False}),
                        ("The truck's own jammer on, posts on a wire with lamps", {"convoy": True, "wired": True}),
                        ("All of them, posts on a wire with lamps", {"convoy": True, "lines": True, "wired": True})):
            rr = [road_case(p, b, **kw) for b in ("low", "high")]
            road[(f, lab)] = rr
            say("| %s | %s | %.0f%% | %.0f%% |" % (name, lab, 100 * rr[0]["share55"], 100 * rr[1]["share55"]))
    open(os.path.join(out, "jam-summary.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")


def ft(x): return "%.1f mi" % (x / 5280) if x >= 2640 else "%.0f ft" % (round(x / 10) * 10)


if __name__ == "__main__":
    main(sys.argv[1:])
