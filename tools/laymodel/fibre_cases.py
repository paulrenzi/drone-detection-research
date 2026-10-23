"""Fibre trunks and wider coverage, on the lay model's example sector.

Compares the last plan (radio trunks, each position covered +/-45 deg) with fibre trunks and with
+/-60 deg coverage (the plan now, and lay_model.py's defaults), laying each 1,000 times with GPS jammed and drop-then-confirm. Writes
out/fibre-summary.md.

    py fibre_cases.py [--runs 1000] [--seed 7]

A fibre trunk: the drone flies out from home carrying the tip dart, whose spool pays out FPV fibre
tied off at the receiver, and drops the tip at the trunk's front dart. The tip hears the front row
by radio and sends alerts home down the fibre. Every number marked ASSUME in lay_model.py applies.
"""
import json, os, random, sys
import lay_model as lm

DART_USD = 29.0          # a dart, small batch (Projected costs)
TIP_EXTRA_USD = 70.0     # ~1.2 mi of fibre at $20-35/km, plus spool and laser, est.


def one(sec, P, rng):
    L = lm.Lay(sec, P, rng, jammed=True, confirm=True).run()
    sc = L.score()
    live = L.graph()
    # hops home: breadth-first from the receiver over working links
    depth, q, names = {"RX": 0}, ["RX"], [n for n in live if n != "RX"]
    while q:
        a = q.pop(0)
        for b in names:
            if b not in depth and L.link(a, b): depth[b] = depth[a] + 1; q.append(b)
    sc["hops"] = max(depth.values())
    tips_tried = sum(1 for n in L.darts if n != "RX" and n.split("+")[0] in {s["id"] for s in L.seq if s["kind"] == "tip"})
    sc["tips"] = tips_tried
    sc["usd"] = (sc["darts"] - tips_tried) * DART_USD + tips_tried * (DART_USD + TIP_EXTRA_USD)
    return sc


def case(cfg, kv, runs, seed):
    def f(c):
        sec = lm.Sector(c); P = lm.plan(sec); seq = lm.lay_sequence(P)
        groups = lm.chunk(sec, seq)
        rng = random.Random(seed); rs = [one(sec, P, rng) for _ in range(runs)]
        n = float(runs)
        cuts = [r["cut"] for r in rs if r["cut"] is not None]
        return {"front": len(P["front"]), "relays": sum(len(t) for t in P["trunks"]), "planned": len(seq), "planned_sorties": len(groups),
                "whole": sum(r["whole"] for r in rs) / n, "tolerant": sum(r["tolerant"] for r in rs) / n,
                "darts": sum(r["darts"] for r in rs) / n, "darts90": lm.pct([r["darts"] for r in rs], 0.9),
                "sorties": sum(r["sorties"] for r in rs) / n, "hours": sum(r["hours"] for r in rs) / n,
                "hops": lm.pct([r["hops"] for r in rs], 0.5), "hops90": lm.pct([r["hops"] for r in rs], 0.9),
                "usd": sum(r["usd"] for r in rs) / n, "cut": (sum(cuts) / len(cuts)) if cuts else None,
                "warn10": lm.pct([r["warn"] for r in rs], 0.1)}
    return lm.with_params(cfg, kv, f)


def main(argv):
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else 1000
    seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 7
    here = os.path.dirname(os.path.abspath(__file__))
    cfg = json.load(open(os.path.join(here, "sector.json")))
    md = []
    def say(x=""): print(x); md.append(x)
    say("## Fibre trunks and wider coverage (%d lays each, GPS jammed, confirm)" % runs)
    say()
    say("| Case | Front darts | Relays | Planned | Planned sorties | Whole | Survives any one dart loss | Survives one fibre cut | Darts used | 9 in 10 | Sorties | Hours | Hops home, median / 9 in 10 | Cost of a lay | Worst warning, 10th pct |")
    say("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    def row(label, kv):
        r = case(cfg, kv, runs, seed)
        say("| %s | %d | %d | %d | %d | %.0f%% | %.0f%% | %s | %.1f | %d | %.1f | %.1f | %d / %d | $%.0f | %s |" % (
            label, r["front"], r["relays"], r["planned"], r["planned_sorties"], 100 * r["whole"], 100 * r["tolerant"],
            "-" if r["cut"] is None else "%.0f%%" % (100 * r["cut"]), r["darts"], r["darts90"], r["sorties"], r["hours"],
            r["hops"], r["hops90"], r["usd"], lm.secs(r["warn10"])))
    row("Last plan: radio trunks, +/-45", {"FIBRE": False, "COVER_DEG": 45.0})
    row("Fibre trunks, +/-45", {"FIBRE": True, "COVER_DEG": 45.0})
    row("Radio trunks, +/-60", {"FIBRE": False, "COVER_DEG": 60.0})
    row("**Fibre trunks, +/-60 (the plan)**", {"FIBRE": True, "COVER_DEG": 60.0})
    row("  same, judged at +/-45", {"FIBRE": True, "COVER_DEG": 60.0, "JUDGE_DEG": 45})
    row("  compass 4 deg, not 2", {"FIBRE": True, "COVER_DEG": 60.0, "COMPASS_DEG": 4.0, "COMPASS_SORTIE_DEG": 1.4})
    row("  radio hop 800 ft, not 980", {"FIBRE": True, "COVER_DEG": 60.0, "HOP": 800.0})
    row("  landings 95% upright", {"FIBRE": True, "COVER_DEG": 60.0, "P_UPRIGHT": 0.95, "P_TILTED": 0.03})
    row("  1 fibre in 5 breaks while laid", {"FIBRE": True, "COVER_DEG": 60.0, "P_SNAG": 0.20})
    row("  15 mph wind", {"FIBRE": True, "COVER_DEG": 60.0, "wind_mph": 15})
    row("Fibre trunks, +/-45, compass 4 deg", {"FIBRE": True, "COVER_DEG": 45.0, "COMPASS_DEG": 4.0, "COMPASS_SORTIE_DEG": 1.4})
    row("Fibre trunks, +/-60, compass 4 deg, judged at +/-45", {"FIBRE": True, "COVER_DEG": 60.0, "JUDGE_DEG": 45, "COMPASS_DEG": 4.0, "COMPASS_SORTIE_DEG": 1.4})
    row("Radio trunks, +/-45, compass 4 deg", {"FIBRE": False, "COVER_DEG": 45.0, "COMPASS_DEG": 4.0, "COMPASS_SORTIE_DEG": 1.4})
    row("Radio trunks, +/-60, compass 4 deg", {"FIBRE": False, "COVER_DEG": 60.0, "COMPASS_DEG": 4.0, "COMPASS_SORTIE_DEG": 1.4})
    os.makedirs(os.path.join(here, "out"), exist_ok=True)
    p = os.path.join(here, "out", "fibre-summary.md")
    open(p + ".new", "w", encoding="utf-8").write("\n".join(md) + "\n"); os.replace(p + ".new", p)


if __name__ == "__main__":
    main(sys.argv[1:])
