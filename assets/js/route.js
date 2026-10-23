// A guarded supply road: replays three drones scored by tools/routemodel/route_model.py on its example road.
// The road, posts, fence, trunks, every hearing and every warning come from the model's output
// (assets/data/route-demo.json); this script only draws them and moves the trucks. Feet, to scale.
// The enemy is to the right. Time is compressed except in the last scene.
(function () {
  var box = document.getElementById("route-model");
  if (!box) return;
  var NS = "http://www.w3.org/2000/svg";
  var ACC = "#c2562c", GREEN = "#4f7a3a", BLUE = "#1f5f8b", GREY = "#8a8a8a", RED = "#b3261e", ROAD = "#b39a6b";
  var svg, D, K, YMIN, XMAX, TOP = 64, scenes = [], total = 0, panel, btn, G = {};

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(e);
    return e;
  }
  function text(x, y, s, attrs, parent) {
    var a = { x: x, y: y, "font-size": 13, fill: "currentColor" };
    for (var k in attrs) a[k] = attrs[k];
    var t = el("text", a, parent); t.textContent = s; return t;
  }
  function sx(p) { return [10 + (p[1] - YMIN) * K, TOP + (XMAX - p[0]) * K]; }
  function lerp(a, b, u) { return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]; }
  function clamp(u) { return u < 0 ? 0 : u > 1 ? 1 : u; }
  function dist(a, b) { return Math.hypot(a[0] - b[0], a[1] - b[1]); }
  function say(s) { if (panel && panel.textContent !== s) panel.textContent = s; }
  function mi(s) { return (s / 5280).toFixed(1); }
  function hhmm(m) { m = Math.round(m); return ("0" + Math.floor(m / 60) % 24).slice(-2) + ":" + ("0" + m % 60).slice(-2); }
  function show(e, on) { e.setAttribute("opacity", on ? 1 : 0); }

  // ---- the road as a curve in s (feet along it)
  var cum = [];
  function roadAt(s) {
    var R = D.road; s = Math.max(0, Math.min(D.L, s));
    for (var i = 0; i < R.length - 1; i++) if (s <= cum[i + 1] || i === R.length - 2) {
      var u = (s - cum[i]) / (cum[i + 1] - cum[i]); return { p: lerp(R[i], R[i + 1], u), t: [R[i + 1][0] - R[i][0], R[i + 1][1] - R[i][1]] };
    }
  }
  function roadPath(s0, s1) {
    var pts = [], n = Math.max(2, Math.ceil((s1 - s0) / 200));
    for (var i = 0; i <= n; i++) pts.push(sx(roadAt(s0 + (s1 - s0) * i / n).p));
    return pts.map(function (q, i) { return (i ? "L" : "M") + q[0].toFixed(1) + " " + q[1].toFixed(1); }).join(" ");
  }
  function along(poly, u) {   // point a share u along a polyline in feet
    var L = 0, i; for (i = 1; i < poly.length; i++) L += dist(poly[i - 1], poly[i]);
    var want = clamp(u) * L;
    for (i = 1; i < poly.length; i++) { var d = dist(poly[i - 1], poly[i]); if (want <= d || i === poly.length - 1) return lerp(poly[i - 1], poly[i], d ? Math.min(1, want / d) : 0); want -= d; }
  }
  function polyLen(poly) { var L = 0; for (var i = 1; i < poly.length; i++) L += dist(poly[i - 1], poly[i]); return L; }

  function build() {
    cum = [0]; for (var i = 1; i < D.road.length; i++) cum.push(cum[i - 1] + dist(D.road[i - 1], D.road[i]));
    var xs = [], ys = [];
    Object.keys(D.nodes).forEach(function (n) { xs.push(D.nodes[n].p[0]); ys.push(D.nodes[n].p[1]); });
    YMIN = Math.min.apply(null, ys) - 900; var ymax = 6200;
    XMAX = Math.max.apply(null, xs) + 900; var xmin = Math.min.apply(null, xs) - 900;
    K = 580 / (ymax - YMIN);
    var H = Math.ceil(TOP + (XMAX - xmin) * K + 34);
    svg = el("svg", { viewBox: "0 0 600 " + H, width: "100%", role: "img", "aria-labelledby": "rtTitle rtDesc",
      style: "font-family:inherit;color:inherit;display:block" }, box);
    el("title", { id: "rtTitle" }).textContent = "A supply road guarded by posts and a fence of darts, with three drones from the route model";
    el("desc", { id: "rtDesc" }).textContent = "A top-down map of a 4 mile road running toward the front, enemy to the right. Posts stand along the road; " +
      "a fence of darts about a mile out wraps the road on every side a drone can come from, joined to the road by trunks. " +
      "A drone flying in to hunt the road is heard at the fence and the stretch it can reach goes hot about 84 seconds before it could get there; trucks stop. " +
      "A second drone flies in and lands beside the road; a post hears it come down and the stretch stays hot until a team clears it. " +
      "A third drone, carried in on foot and launched near the road, is heard about a second before it strikes.";
    el("rect", { x: 0, y: 0, width: 600, height: H, fill: "#efe9d8" });
    // enemy side and our positions
    var e = sx([0, 3000])[0], f = sx([0, 0])[0];
    el("rect", { x: e, y: TOP - 8, width: 600 - e, height: H - TOP - 26, fill: ACC, "fill-opacity": 0.13 });
    el("line", { x1: e, y1: TOP - 8, x2: e, y2: H - 34, stroke: RED, "stroke-width": 2, "stroke-dasharray": "7 4" });
    el("line", { x1: f, y1: TOP - 8, x2: f, y2: H - 34, stroke: GREEN, "stroke-width": 3, "stroke-dasharray": "3 3" });
    text(e + (600 - e) / 2, TOP + 8, "ENEMY", { "text-anchor": "middle", "font-size": 12, "font-weight": 700, fill: ACC, "letter-spacing": "0.06em" });
    text(f - 4, TOP + 8, "our positions", { "text-anchor": "end", "font-size": 11, "font-weight": 700, fill: GREEN });
    // tree belts
    (D.cfg.tree_belts || []).forEach(function (b) {
      var a = sx(b.line[0]), c = sx(b.line[1]);
      el("line", { x1: a[0], y1: a[1], x2: c[0], y2: c[1], stroke: GREEN, "stroke-width": 3.5, "stroke-opacity": 0.6 });
    });
    // hearing, links, the road
    G.hear = el("g", { opacity: 0.9 }); G.links = el("g", { opacity: 0.8 });
    Object.keys(D.nodes).forEach(function (n) {
      var q = sx(D.nodes[n].p);
      el("circle", { cx: q[0], cy: q[1], r: D.reff * K, fill: D.nodes[n].post ? GREEN : ACC, "fill-opacity": 0.06, stroke: D.nodes[n].post ? GREEN : ACC, "stroke-opacity": 0.18 }, G.hear);
    });
    D.links.forEach(function (l) {
      var a = sx(D.nodes[l[0]].p), b = sx(D.nodes[l[1]].p);
      if (D.nodes[l[0]].post && D.nodes[l[1]].post) return;
      el("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: BLUE, "stroke-opacity": 0.35, "stroke-width": 1 }, G.links);
    });
    el("path", { d: roadPath(0, D.L), fill: "none", stroke: ROAD, "stroke-width": 5, "stroke-linecap": "round" });
    G.hot = el("path", { d: "", fill: "none", stroke: RED, "stroke-width": 8, "stroke-opacity": 0.55, "stroke-linecap": "round" });
    G.hot2 = el("path", { d: "", fill: "none", stroke: RED, "stroke-width": 8, "stroke-opacity": 0.55, "stroke-linecap": "round" });
    var r0 = sx(D.road[0]), r1 = sx(D.road[D.road.length - 1]);
    text(r0[0] + 2, r0[1] + 22, "depot", { "text-anchor": "middle", "font-size": 11, "font-weight": 700 });
    // nodes
    G.dot = {};
    Object.keys(D.nodes).forEach(function (n) {
      var nd = D.nodes[n], q = sx(nd.p);
      G.dot[n] = nd.post ? el("rect", { x: q[0] - 2.6, y: q[1] - 2.6, width: 5.2, height: 5.2, fill: GREEN })
        : el("circle", { cx: q[0], cy: q[1], r: n[0] === "F" ? 2.8 : 2.2, fill: "#fff", stroke: n[0] === "F" ? ACC : BLUE, "stroke-width": 1.4 });
    });
    // labels for the parts
    G.parts = el("g", {});
    var lp = sx(D.nodes["F1.20"] ? D.nodes["F1.20"].p : D.road[0]);
    G.lblFence = text(lp[0], lp[1] - 8, "fence, 1 mi out", { "font-size": 11, "font-weight": 700, fill: ACC, "text-anchor": "middle" }, G.parts);
    var tp = D.posts[Math.round(D.posts.length * 0.3)].p, tq = sx(tp);
    G.lblPosts = text(tq[0], tq[1] + 16, "posts along the road", { "font-size": 11, "font-weight": 700, fill: GREEN, "text-anchor": "middle" }, G.parts);
    var tr = D.runs[0].trunks[1], trp = tr.relays[Math.floor(tr.relays.length / 2)], trq = sx(trp);
    G.lblTrunk = text(trq[0] + 6, trq[1] + 3, "trunk", { "font-size": 11, "font-weight": 700, fill: BLUE }, G.parts);
    // scale
    var mi1 = 5280 * K;
    el("line", { x1: 14, y1: H - 14, x2: 14 + mi1, y2: H - 14, stroke: "currentColor", "stroke-width": 3 });
    text(14 + mi1 + 6, H - 10, "1 mi", { "font-size": 11, opacity: 0.85 });
    // moving things
    G.fx = el("g", {});
    G.trucks = [0, 1, 2].map(function () { return el("rect", { x: -5, y: -3, width: 10, height: 6, rx: 1.5, fill: "#27221c", opacity: 0 }, G.fx); });
    G.team = el("rect", { x: -5, y: -3, width: 10, height: 6, rx: 1.5, fill: GREEN, stroke: "#fff", "stroke-width": 1, opacity: 0 }, G.fx);
    G.foot = el("path", { d: "M0 -6 L5 4 L-5 4 Z", fill: "#27221c", opacity: 0 }, G.fx);
    G.drone = el("g", { opacity: 0 }, G.fx);
    [[-3, -3], [3, -3], [-3, 3], [3, 3]].forEach(function (p) { el("circle", { cx: p[0], cy: p[1], r: 2.1, fill: "none", stroke: "#111", "stroke-width": 1 }, G.drone); });
    el("rect", { x: -1.8, y: -1.8, width: 3.6, height: 3.6, fill: "#111" }, G.drone);
    G.ring = el("circle", { r: 0, fill: "none", stroke: RED, "stroke-width": 2, opacity: 0 }, G.fx);
    G.blip = el("circle", { r: 3.2, fill: RED, opacity: 0 }, G.fx);
    G.mark = el("g", { opacity: 0 }, G.fx);
    el("circle", { r: 7, fill: "none", stroke: RED, "stroke-width": 2.2 }, G.mark);
    el("path", { d: "M-4 -4 L4 4 M4 -4 L-4 4", stroke: RED, "stroke-width": 2.2 }, G.mark);
    G.markLbl = text(0, 0, "", { "font-size": 11, "font-weight": 700, fill: RED }, G.fx);
    G.call = el("g", { opacity: 0 }, G.fx);
    el("circle", { r: 26, fill: "none", stroke: "#27221c", "stroke-width": 1.5, "stroke-dasharray": "3 3" }, G.call);
    G.callLbl = text(-20, -32, "launched 520 ft from the road", { "text-anchor": "start", "font-size": 11, "font-weight": 700 }, G.call);
    G.hit = el("g", { opacity: 0 }, G.fx);
    el("circle", { r: 9, fill: RED, "fill-opacity": 0.35 }, G.hit);
    // header
    G.clock = text(300, 18, "", { "text-anchor": "middle", "font-size": 14, "font-weight": 700, opacity: 0.85 });
    G.board = text(300, 38, "", { "text-anchor": "middle", "font-size": 14, "font-weight": 700 });
    G.count = text(590, 18, "", { "text-anchor": "end", "font-size": 12, "font-weight": 700 });
  }

  function place(e, p, t) {
    var q = sx(p), ang = t ? Math.atan2(-t[0], t[1]) * 180 / Math.PI : 0;
    e.setAttribute("transform", "translate(" + q[0].toFixed(1) + " " + q[1].toFixed(1) + ")" + (t ? " rotate(" + ang.toFixed(1) + ")" : ""));
  }
  function truck(i, s, on) {
    var r = roadAt(s); place(G.trucks[i], r.p, r.t); G.trucks[i].setAttribute("opacity", on === false ? 0 : 1);
  }
  function hot(g, s0, s1, op) { g.setAttribute("d", s1 > s0 ? roadPath(s0, s1) : ""); g.setAttribute("stroke-opacity", op === undefined ? 0.55 : op); }
  function lit(ids, on) { Object.keys(G.dot).forEach(function (n) { var d = G.dot[n]; var l = ids.indexOf(n) >= 0 && on; d.setAttribute(D.nodes[n].post ? "fill" : "fill", l ? RED : D.nodes[n].post ? GREEN : "#fff"); }); }
  function heardNow(ev, tr) { return Object.keys(ev.heard).filter(function (n) { return tr >= ev.heard[n][0] && tr <= ev.heard[n][1] + 1; }); }
  function pulse(n, w) { var q = sx(D.nodes[n].p); G.ring.setAttribute("cx", q[0]); G.ring.setAttribute("cy", q[1]); G.ring.setAttribute("r", 4 + 18 * (w % 1)); G.ring.setAttribute("opacity", 0.9 * (1 - w % 1)); }
  function blipAlong(path, u) {
    if (u <= 0 || u >= 1) { G.blip.setAttribute("opacity", 0); return; }
    var pts = path.map(function (n) { return D.nodes[n].p; });
    var q = sx(pts.length > 1 ? along(pts, u) : pts[0]); G.blip.setAttribute("cx", q[0]); G.blip.setAttribute("cy", q[1]); G.blip.setAttribute("opacity", 1);
  }
  function clearFx() {
    show(G.drone, false); G.ring.setAttribute("opacity", 0); G.blip.setAttribute("opacity", 0); show(G.mark, false); G.markLbl.textContent = "";
    show(G.hit, false); show(G.call, false); show(G.team, false); show(G.foot, false); hot(G.hot, 0, 0); hot(G.hot2, 0, 0); lit([], false);
    G.trucks.forEach(function (t) { t.setAttribute("opacity", 0); });
  }

  function sceneList() {
    var out = [], S = D.stats, E = D.events, V = D.veh_fts * 10;   // trucks at 30 mph, time x10
    var ev1 = E[0], ev2 = E[1], ev3 = E[2];
    var wmin = Math.floor(S.warn_fence.min);
    out.push([8, function (u) {
      clearFx(); G.parts.setAttribute("opacity", 1);
      G.clock.textContent = "A guarded road, to scale"; G.board.textContent = ""; G.count.textContent = "";
      say("A 4-mile road running toward the front. Posts every 1,060 ft along it, placed by hand. A fence of darts about a mile out on every side a drone can come from, dropped by drone and joined to the road by trunks every 2 mi.");
    }]);
    // ---- 1. a drone flies in to hunt the road
    var x1 = 10, heardAt = ev1.heard[ev1.first][0], alertAt = heardAt + 3 + 0.3 * ev1.home.length;
    var tA = ev1.arrive, tEnd = ev1.dur, dur1 = tA / x1 + (tEnd - tA) / 20 + 5;
    var hot1 = ev1.hot;
    out.push([dur1, function (u) {
      clearFx(); G.parts.setAttribute("opacity", 0);
      var at = u * dur1, tr = at <= tA / x1 ? at * x1 : at <= tA / x1 + (tEnd - tA) / 20 ? tA + (at - tA / x1) * 20 : tEnd + 1;
      var p = along(ev1.path, Math.min(1, tr / tEnd)); place(G.drone, p); show(G.drone, tr <= tEnd);
      // trucks: one inside the stretch that goes hot, one coming up behind it
      var sB = Math.min(10000 + Math.min(tr, alertAt) * D.veh_fts, D.L), sA = 1500 + tr * D.veh_fts;
      var held = tr >= alertAt && tr < tEnd;
      if (held) sA = Math.min(sA, Math.max(1500 + alertAt * D.veh_fts, hot1[0] - 400));
      if (tr >= tEnd) sB = Math.min(D.L, sB + (tr - tEnd) * D.veh_fts);
      truck(0, sA); truck(1, sB);
      G.clock.textContent = hhmm(5 * 60 + 40 + tr / 60);
      var ids = heardNow(ev1, tr); lit(ids, true);
      if (tr >= heardAt && tr < heardAt + 3) pulse(ev1.first, (tr - heardAt) / 1.5);
      blipAlong(ev1.home, (tr - heardAt - 1) / 2.5);
      if (held) hot(G.hot, hot1[0], hot1[1]);
      G.count.textContent = tr >= heardAt ? (tr < tEnd - 8 ? "drones inside: 1" : "drones inside: 0") : "drones inside: 0";
      if (tr < heardAt) { G.board.textContent = "Road clear"; G.board.setAttribute("fill", GREEN);
        say("A drone flies in from the enemy side to hunt the road. Two trucks are moving."); }
      else if (tr < tA) { G.board.textContent = "HOT: mile " + mi(hot1[0]) + " to " + mi(hot1[1]) + " · it can reach the road in " + Math.max(0, Math.round(tA - tr)) + " s"; G.board.setAttribute("fill", RED);
        say("A dart on a trunk hears it " + ((tA - heardAt) * D.fts / 5280).toFixed(1) + " mi from the road. The alert is at the road in about " + Math.round(3 + 0.3 * ev1.home.length) + " s, " + Math.round(ev1.warn) + " s before the drone can be. The truck inside the stretch stops under the trees; the one behind holds short."); }
      else if (tr < tEnd - 8) { G.board.textContent = "HOT: drone over the road"; G.board.setAttribute("fill", RED);
        say("It reaches the road and hunts along it. The posts track it as it goes, but nothing on the road is moving."); }
      else { G.board.textContent = tr < tEnd ? "HOT: drone leaving" : "Road clear"; G.board.setAttribute("fill", tr < tEnd ? RED : GREEN);
        say("The fence hears it go back out: one drone in, one out. The road goes clear and the trucks move again."); }
    }]);
    // ---- 2. a drone flies in to land and wait
    var hA = ev2.heard[ev2.first][0], land = ev2.dur, sp = ev2.spot_s, firstS = D.nodes[ev2.first].s;
    var dur2 = land / 10 + 4 + 9 + 3;
    out.push([dur2, function (u) {
      clearFx(); G.parts.setAttribute("opacity", 0);
      var at = u * dur2, tr = Math.min(at * 10, land), after = at - land / 10;
      place(G.drone, along(ev2.path, tr / land)); show(G.drone, true);
      G.clock.textContent = hhmm(7 * 60 + 10 + tr / 60 + Math.max(0, after) * 2);
      lit(after < 0 ? heardNow(ev2, tr) : [], true);
      if (tr >= hA && tr < hA + 3) pulse(ev2.first, (tr - hA) / 1.5);
      blipAlong(ev2.home, (tr - hA - 1) / 2.5);
      var hs0 = Math.max(0, firstS - 5280), hs1 = Math.min(D.L, firstS + 5280);
      truck(0, Math.min(sp - 6000, 9000 + at * 60)); truck(2, D.L - 600);
      G.count.textContent = tr >= hA ? "drones inside: 1" : "drones inside: 0";
      if (tr < hA) { G.board.textContent = "Road clear"; G.board.setAttribute("fill", GREEN);
        say("Later, another drone flies in. This one is going to land beside the road and wait for a truck."); }
      else if (after < 0) { hot(G.hot, hs0, hs1); G.board.textContent = "HOT: mile " + mi(hs0) + " to " + mi(hs1); G.board.setAttribute("fill", RED);
        say("The fence hears it come in, and the stretch it could reach goes hot."); }
      else {
        var q = sx(ev2.spot); G.mark.setAttribute("transform", "translate(" + q[0] + " " + q[1] + ")"); show(G.mark, after < 13);
        var post = ev2.loud, pn = post.slice(1);
        G.markLbl.setAttribute("x", q[0] - 10); G.markLbl.setAttribute("y", q[1] - 10); G.markLbl.setAttribute("text-anchor", "end");
        var cs = Math.max(0, sp - 1300), ce = Math.min(D.L, sp + 1300);
        if (after < 4) {
          show(G.drone, true); hot(G.hot, cs, ce); G.markLbl.textContent = "landed by post " + pn;
          G.board.textContent = "HOT: drone waiting near post " + pn + ", mile " + mi(sp); G.board.setAttribute("fill", RED);
          say("Post " + pn + " hears it come down " + ev2.err + " ft away and go quiet. One in, none out: it is waiting. The stretch round post " + pn + " stays hot until it is cleared.");
        } else if (after < 13) {
          hot(G.hot, cs, ce); G.markLbl.textContent = "landed by post " + pn;
          var ts = D.L - 600 - (after - 4) * 520, done = ts <= sp + 200;
          var rr = roadAt(Math.max(sp + 200, ts)); place(G.team, rr.p, rr.t); show(G.team, true); truck(2, D.L - 600, false);
          show(G.drone, !done || after < 11);
          G.board.textContent = done && after > 11 ? "Cleared" : "HOT: team going to post " + pn; G.board.setAttribute("fill", done && after > 11 ? GREEN : RED);
          say("A team goes to post " + pn + " and searches the " + Math.round((ce - cs) / 100) * 100 + " ft round it while the drone sits with its motors off.");
        } else {
          show(G.drone, false); show(G.mark, false); G.markLbl.textContent = ""; G.board.textContent = "Road clear"; G.board.setAttribute("fill", GREEN);
          G.count.textContent = "drones inside: 0";
          say("Cleared before any truck came through. Without the posts, the first sign of it would have been the strike.");
        }
      }
    }]);
    // ---- 3. the gap: launched inside the fence
    var dur3 = 4 + ev3.dur + 5, h3 = ev3.heard[ev3.first][0];
    out.push([dur3, function (u) {
      clearFx(); G.parts.setAttribute("opacity", 0);
      var at = u * dur3, tr = at - 4, lp = ev3.launch;
      place(G.foot, [lp[0] + 120, lp[1] - 260]); show(G.foot, true);
      var cq = sx(lp); G.call.setAttribute("transform", "translate(" + cq[0] + " " + cq[1] + ")"); show(G.call, true);
      G.callLbl.textContent = "team on foot, " + Math.round(dist(lp, roadAt(ev3.target_s + 300).p) / 10) * 10 + " ft from the road";
      var ts = ev3.target_s - (ev3.dur - Math.max(0, Math.min(tr, ev3.dur))) * D.veh_fts;
      truck(0, ts);
      G.clock.textContent = hhmm(9 * 60 + 30 + Math.max(0, tr) / 60) + " · real time";
      G.count.textContent = "drones inside: 0";
      if (tr < 0) { place(G.drone, lp); show(G.drone, true); G.board.textContent = "Road clear"; G.board.setAttribute("fill", GREEN);
        say("The gap. A team on foot carries a drone in and launches it " + Math.round(dist(lp, roadAt(ev3.target_s + 300).p) / 10) * 10 + " ft from the road. It never crosses the fence."); return; }
      place(G.drone, along(ev3.path, Math.min(1, tr / ev3.dur))); show(G.drone, tr < ev3.dur);
      lit(heardNow(ev3, tr), tr < ev3.dur);
      if (tr >= h3) { G.board.textContent = "HOT: drone over the road"; G.board.setAttribute("fill", RED); }
      if (tr >= h3 && tr < h3 + 2) pulse(ev3.first, (tr - h3) / 1);
      if (tr >= ev3.dur) { var q = sx(ev3.path[1]); G.hit.setAttribute("transform", "translate(" + q[0] + " " + q[1] + ")"); show(G.hit, true); }
      say("Shown in real time: a post hears it lift off, about " + Math.max(1, Math.round(ev3.warn)) + " s before it strikes. Drones launched inside the fence get the seconds a worn detector gives, no more.");
    }]);
    out.push([8, function () {
      clearFx(); G.parts.setAttribute("opacity", 1);
      G.clock.textContent = "The model's numbers for this road"; G.count.textContent = "";
      G.board.textContent = S.posts + " posts + " + S.air + " darts · every strike track ≥ " + wmin + " s · every landing within 300 ft heard"; G.board.setAttribute("fill", "currentColor");
      say("Every strike track the model flew at this road, from within 60° of the enemy, was heard at least " + wmin + " s out, and every landing within 300 ft of the road was heard by a post. Laying the fence takes about " + Math.round(S.lay_darts) + " darts and " + Math.round(S.lay_sorties) + " sorties.");
    }]);
    return out;
  }

  var at = 0, playing = false, last = 0;
  function seek(t) {
    at = t; var acc = 0;
    for (var i = 0; i < scenes.length; i++) {
      var d = scenes[i][0];
      if (t < acc + d || i === scenes.length - 1) { scenes[i][1](clamp((t - acc) / d)); return; }
      acc += d;
    }
  }
  function frame(ts) {
    var dt = last ? Math.min(0.1, (ts - last) / 1000) : 0; last = ts;
    var t = at + dt; if (t > total) t = 0;
    seek(t);
    if (playing) requestAnimationFrame(frame);
  }
  function play() { if (playing) return; playing = true; last = 0; requestAnimationFrame(frame); if (btn) btn.textContent = "Pause"; }
  function pause() { playing = false; if (btn) btn.textContent = "Play"; }

  function start(data) {
    D = data; build(); scenes = sceneList();
    total = scenes.reduce(function (a, s) { return a + s[0]; }, 0);
    panel = document.getElementById("route-status"); btn = document.getElementById("route-play");
    seek(0);
    if (btn) btn.addEventListener("click", function () { playing ? pause() : play(); });
    var rp = document.getElementById("route-replay");
    if (rp) rp.addEventListener("click", function () { at = 0; seek(0); play(); });
    window.__route = { seek: seek, total: total };
    if (box.getAttribute("data-autoplay") !== "no") {
      var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (!reduce && "IntersectionObserver" in window)
        new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? play() : pause(); }); }, { threshold: 0.3 }).observe(box);
    }
  }
  fetch(box.getAttribute("data-src")).then(function (r) { return r.json(); }).then(start);
})();
