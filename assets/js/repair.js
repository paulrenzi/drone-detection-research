// Animated repair model for the fibre net: a shell cuts a fibre, the base box misses its heartbeat within 30 s,
// one sortie lays a new tip dart and fibre, and a re-lay flown on a compass 3° off is caught by confirm-after-release.
// Same geometry and scale as line-layout.js. All distances are in feet.
(function () {
  var box = document.getElementById("repair-model");
  if (!box) return;

  var NS = "http://www.w3.org/2000/svg";
  var FT = 0.05;
  var HEAR = 656, ALT = 165, HOP = 980;
  var NEED = 88 * 65;
  var REFF = Math.sqrt(HEAR * HEAR - ALT * ALT);
  var DEPTH = NEED - Math.sqrt(REFF * REFF - HOP * HOP / 4);
  var W = 1640, UX = 300, UY = 520;
  var ACC = "#c2562c", GREEN = "#4f7a3a", BLUE = "#1f5f8b", GREY = "#8a8a8a", RED = "#b3261e", FIBRE = "#6b3fa0";
  var POS = [[-W / 2, 0], [0, 0], [W / 2, 0]];
  var DRIFT = 3, STEP_BACK = 300;   // compass error in degrees; spare offset
  var END = -300, AR = Math.PI / 3;  // ends 300 ft past the 60° lines
  var BASE = [300, -400];            // base box at the launch point

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(e);
    return e;
  }
  function text(x, y, s, attrs, parent) {
    var a = { x: x, y: y, "font-size": 15, fill: "currentColor" };
    for (var k in attrs) a[k] = attrs[k];
    var t = el("text", a, parent);
    t.textContent = s;
    return t;
  }
  function sx(p) { return [UX + p[0] * FT, UY - p[1] * FT]; }
  function distFt(a, b) { return Math.hypot(a[0] - b[0], a[1] - b[1]); }
  function lerp(a, b, u) { return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]; }
  function rotAbout(p, c, deg) { var t = deg * Math.PI / 180, x = p[0] - c[0], y = p[1] - c[1]; return [c[0] + x * Math.cos(t) - y * Math.sin(t), c[1] + x * Math.sin(t) + y * Math.cos(t)]; }
  function commas(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }

  function frontRow() {
    var a = DEPTH * AR, len = W + 2 * a;
    function pt(u) {
      var th;
      if (u < a) { th = AR * (1 - u / a); return [-W / 2 - DEPTH * Math.sin(th), DEPTH * Math.cos(th)]; }
      if (u <= a + W) return [-W / 2 + (u - a), DEPTH];
      th = AR * (u - a - W) / a; return [W / 2 + DEPTH * Math.sin(th), DEPTH * Math.cos(th)];
    }
    var usable = len - 2 * END, n = Math.ceil(usable / HOP) + 1, step = usable / (n - 1), out = [];
    for (var i = 0; i < n; i++) out.push(pt(END + i * step));
    return out;
  }
  var PLAN = frontRow(), NF = PLAN.length;
  var TIPS = [1, NF - 2], TB = NF - 2;   // fibre B runs to the right-hand tip
  var CUT_AT = lerp(BASE, PLAN[TB], 0.55);
  var SORTIE = [4, 5, 6, 7];             // the last re-lay sortie: F5 to F8, closing the front row onto F9
  function nm(i) { return "F" + (i + 1); }

  var svg = el("svg", { viewBox: "0 0 600 590", width: "100%", role: "img",
    "aria-labelledby": "rmTitle rmDesc", style: "font-family:inherit;color:inherit;display:block" }, box);
  el("title", { id: "rmTitle" }).textContent = "How the net is repaired, seen from above";
  el("desc", { id: "rmDesc" }).textContent = "To scale. A shell cuts the right-hand fibre and alerts re-route along the front row to the left-hand fibre. " +
    "Within 30 seconds the base box misses the tip's heartbeat and says so. One drone sortie lays a new tip dart and fibre. Then a re-lay sortie flown on a compass 3 degrees off " +
    "lands its closing dart out of reach of " + nm(SORTIE[3] + 1) + "; the drone hears a relay from " + nm(SORTIE[2]) + " only, drops a spare 300 feet toward " + nm(SORTIE[3] + 1) + ", and the link is confirmed.";

  el("rect", { x: 0, y: 0, width: 600, height: 590, fill: "#efe9d8" });
  el("rect", { x: 0, y: 0, width: 600, height: 84, fill: ACC, "fill-opacity": 0.1 });
  text(300, 32, "ENEMY SIDE", { "text-anchor": "middle", "font-size": 22, "font-weight": 700, "letter-spacing": "0.08em", fill: ACC });
  var clock = text(300, 60, "", { "text-anchor": "middle", "font-size": 16, "font-weight": 700, opacity: 0.85 });
  el("rect", { x: 0, y: UY - 13, width: 600, height: 26, fill: GREEN, "fill-opacity": 0.7 });
  var bs = sx(BASE);
  el("path", { d: "M" + sx(POS[0]).join(" ") + " L" + sx(POS[2]).join(" ") + " M" + sx(POS[2]).join(" ") + " L" + bs.join(" "),
    fill: "none", stroke: "#3b2f22", "stroke-width": 1.5, "stroke-dasharray": "2 3" });
  POS.forEach(function (p, i) {
    var s = sx(p);
    el("rect", { x: s[0] - 6, y: s[1] - 5, width: 12, height: 10, rx: 2, fill: "#3b2f22" });
    text(s[0] + (i === 0 ? -12 : 12), UY + 5, "P" + (i + 1), { "text-anchor": i === 0 ? "end" : "start", "font-size": 15, "font-weight": 700, fill: "#fff" });
  });
  el("rect", { x: bs[0] - 6, y: bs[1] - 6, width: 12, height: 12, fill: FIBRE });
  text(bs[0] + 12, bs[1] + 5, "base box", { "font-size": 14, "font-weight": 700 });
  var tally = text(300, UY + 58, "", { "text-anchor": "middle", "font-size": 15, "font-weight": 700, opacity: 0.85 });
  el("line", { x1: 20, y1: 570, x2: 20 + 2000 * FT, y2: 570, stroke: "currentColor", "stroke-width": 3 });
  text(20, 560, "2,000 ft", { "font-size": 13, opacity: 0.85 });
  text(300, 108, "circles: listening darts · purple: fibres · dotted: planned points", { "text-anchor": "middle", "font-size": 13, opacity: 0.85 });

  var gGhost = el("g", {}), gFib = el("g", {}), gLinks = el("g", {}), gNodes = el("g", {}), gFx = el("g", {});
  var bad = el("line", { stroke: RED, "stroke-width": 2.5, "stroke-dasharray": "6 4", opacity: 0 }, gFx);
  var badLbl = text(0, 0, "", { "font-size": 14, "font-weight": 700, fill: RED, "text-anchor": "middle" }, gFx);
  var blast = el("circle", { r: 0, fill: ACC, opacity: 0 }, gFx);
  var pulse = el("circle", { r: 0, fill: "none", stroke: ACC, "stroke-width": 2, opacity: 0 }, gFx);
  var packet = el("circle", { r: 5, fill: FIBRE, opacity: 0 }, gFx);
  var drone = el("g", { opacity: 0 }, gFx);
  var ds = el("g", { transform: "scale(1.4)" }, drone);
  [[-5, -5], [5, -5], [-5, 5], [5, 5]].forEach(function (p) {
    el("circle", { cx: p[0], cy: p[1], r: 3.2, fill: "none", stroke: "#111", "stroke-width": 1.2 }, ds);
  });
  el("rect", { x: -3, y: -3, width: 6, height: 6, fill: "#111" }, ds);
  var ear = text(0, 0, "", { "font-size": 14, "font-weight": 700, "text-anchor": "start" }, gFx);
  var boxLbl = text(bs[0] + 12, bs[1] + 22, "", { "font-size": 13, "font-weight": 700 }, gFx);

  var panel = document.getElementById("repair-status");
  var btn = document.getElementById("repair-play");
  function say(s) { if (panel && panel.textContent !== s) panel.textContent = s; }

  var nodes, fibres;
  function node(p) {
    var s = sx(p), d = { p: p, dead: false, hidden: false, x: s[0], y: s[1] };
    d.dot = el("circle", { cx: d.x, cy: d.y, r: 5.5, "stroke-width": 2 }, gNodes);
    d.xm = el("path", { d: "M" + (d.x - 6) + " " + (d.y - 6) + " l12 12 m0 -12 l-12 12", stroke: "#111", "stroke-width": 2.2, opacity: 0 }, gNodes);
    return d;
  }
  function move(d, p) {
    var s = sx(p); d.p = p; d.x = s[0]; d.y = s[1];
    d.dot.setAttribute("cx", d.x); d.dot.setAttribute("cy", d.y);
    d.xm.setAttribute("d", "M" + (d.x - 6) + " " + (d.y - 6) + " l12 12 m0 -12 l-12 12");
  }
  function live(d) { return !d.dead && !d.hidden; }
  function fibre(to, tip) {
    var a = sx(BASE), b = sx(to), f = { tip: tip, cut: false, hidden: false };
    f.line = el("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], "stroke-width": 2.2 }, gFib);
    f.ring = el("circle", { cx: b[0], cy: b[1], r: 9.5, fill: "none", "stroke-width": 2 }, gFib);
    return f;
  }

  // down each whole fibre to its live tip, then radio hops of <= HOP ft between live darts
  function route() {
    var n = nodes.length, seen = [], q = [], i, j;
    while (gLinks.firstChild) gLinks.removeChild(gLinks.firstChild);
    for (i = 0; i < n; i++) seen.push(false);
    fibres.forEach(function (f) {
      var on = !f.cut && !f.hidden && live(nodes[f.tip]);
      f.line.setAttribute("stroke", f.cut ? GREY : FIBRE); f.line.setAttribute("stroke-dasharray", f.cut ? "6 5" : "none");
      f.line.setAttribute("opacity", f.hidden ? 0 : 1); f.ring.setAttribute("opacity", f.hidden ? 0 : 1);
      f.ring.setAttribute("stroke", f.cut ? GREY : FIBRE);
      if (on && !seen[f.tip]) { seen[f.tip] = true; q.push(f.tip); }
    });
    while (q.length) {
      var a = q.shift();
      for (j = 0; j < n; j++) if (live(nodes[j]) && !seen[j] && distFt(nodes[a].p, nodes[j].p) <= HOP) {
        seen[j] = true; q.push(j);
        el("line", { x1: nodes[j].x, y1: nodes[j].y, x2: nodes[a].x, y2: nodes[a].y, stroke: BLUE, "stroke-opacity": 0.55, "stroke-dasharray": "4 3" }, gLinks);
      }
    }
    var up = 0, total = 0;
    nodes.forEach(function (d, k) {
      d.cut = live(d) && !seen[k];
      if (!d.hidden) { total++; if (seen[k]) up++; }
      d.dot.setAttribute("fill", d.dead ? "#ddd" : "#fff");
      d.dot.setAttribute("stroke", d.dead || d.cut ? GREY : ACC);
      d.dot.setAttribute("opacity", d.hidden ? 0 : 1);
      d.xm.setAttribute("opacity", d.dead && !d.hidden ? 1 : 0);
    });
    var whole = fibres.filter(function (f) { return !f.cut && !f.hidden; }).length;
    return { up: up, total: total, fibres: whole };
  }
  function count(c) { return c.up + " of " + c.total + " darts reach the unit · " + c.fibres + " fibre" + (c.fibres === 1 ? "" : "s") + " home"; }

  // ghost rings at the planned points of the re-lay sortie
  SORTIE.forEach(function (i) { var s = sx(PLAN[i]); el("circle", { cx: s[0], cy: s[1], r: 7, fill: "none", stroke: ACC, "stroke-dasharray": "2 2", "stroke-opacity": 0.8 }, gGhost); });
  gGhost.setAttribute("opacity", 0);

  var DROPS = SORTIE.map(function (i) { return rotAbout(PLAN[i], BASE, DRIFT); });
  var LAST = DROPS[DROPS.length - 1], NEXT = PLAN[SORTIE[SORTIE.length - 1] + 1];
  var GAP = distFt(LAST, NEXT);
  var SPARE = lerp(LAST, NEXT, STEP_BACK / GAP);
  var NEWTIP = [PLAN[TB][0] - 60, PLAN[TB][1] - 40];   // the new tip lands beside the old one

  function setDrone(p, show) { var s = sx(p); drone.setAttribute("transform", "translate(" + s[0] + " " + s[1] + ")"); drone.setAttribute("opacity", show ? 1 : 0); }
  function ring(el_, p, u) { var s = sx(p); el_.setAttribute("cx", s[0]); el_.setAttribute("cy", s[1]); el_.setAttribute("r", 6 + 34 * u); el_.setAttribute("opacity", 0.9 * (1 - u)); }
  function fly(path, u) { // position along a polyline, u in 0..1
    var L = 0, segs = [], i;
    for (i = 1; i < path.length; i++) { var l = distFt(path[i - 1], path[i]); segs.push(l); L += l; }
    var want = u * L;
    for (i = 0; i < segs.length; i++) { if (want <= segs[i]) return lerp(path[i], path[i + 1], segs[i] ? want / segs[i] : 0); want -= segs[i]; }
    return path[path.length - 1];
  }

  var spare, newTip, newFibre;
  function reset() {
    while (gNodes.firstChild) gNodes.removeChild(gNodes.firstChild);
    while (gFib.firstChild) gFib.removeChild(gFib.firstChild);
    nodes = PLAN.map(function (p) { return node(p); });
    fibres = TIPS.map(function (j) { return fibre(PLAN[j], j); });
    spare = node(SPARE); spare.hidden = true; nodes.push(spare);
    newTip = node(NEWTIP); newTip.hidden = true; nodes.push(newTip);
    newFibre = fibre(NEWTIP, nodes.length - 1); newFibre.hidden = true; fibres.push(newFibre);
    gGhost.setAttribute("opacity", 0);
    [bad, blast, pulse, packet].forEach(function (e) { e.setAttribute("opacity", 0); });
    badLbl.textContent = ""; ear.textContent = ""; boxLbl.textContent = ""; drone.setAttribute("opacity", 0);
    tally.textContent = count(route());
  }

  // scenes: [seconds, function(u)]
  var scenes = [
    [3, function (u) {
      clock.textContent = "Day 1, 02:10";
      say("A shell lands on the right-hand fibre and cuts it.");
      var s = sx(CUT_AT);
      if (u < 0.5) { blast.setAttribute("cx", s[0]); blast.setAttribute("cy", s[1]); blast.setAttribute("r", 4 + 40 * u * 2); blast.setAttribute("opacity", 0.6 * (1 - u * 2)); }
      else if (!fibres[1].cut) { blast.setAttribute("opacity", 0); fibres[1].cut = true; tally.textContent = count(route()); }
    }],
    [5, function (u) {
      clock.textContent = "Day 1, 02:10:30";
      boxLbl.setAttribute("fill", RED); boxLbl.textContent = "fibre B dark";
      say("The tip checks in down its fibre every 10 s. After 30 s with nothing, the base box shows 'fibre B dark': cut, or the tip is dead. Alerts re-route along the front row to fibre A, so the unit is still covered, on one fibre.");
    }],
    [8, function (u) {
      clock.textContent = "Day 1, 06:20";
      var at = NEWTIP, path = [BASE, at];
      tally.textContent = "Repair: a new tip dart and fibre";
      if (u < 0.4) {
        var p = lerp(BASE, at, u / 0.4); setDrone(p, true);
        newFibre.hidden = false; var a = sx(BASE), b = sx(p);
        newFibre.line.setAttribute("x2", b[0]); newFibre.line.setAttribute("y2", b[1]); newFibre.line.setAttribute("opacity", 1);
        newFibre.line.setAttribute("stroke", FIBRE); newFibre.ring.setAttribute("opacity", 0);
        say("Repair sortie from the base box at dawn. The new tip's spool pays out a new fibre, tied off at the box, as the drone flies out.");
      } else if (u < 0.7) {
        setDrone(at, true);
        if (newTip.hidden) { newTip.hidden = false; var e = sx(at); newFibre.line.setAttribute("x2", e[0]); newFibre.line.setAttribute("y2", e[1]); tally.textContent = count(route()); }
        var v = (u - 0.4) / 0.3, a2 = sx(at), b2 = sx(BASE);
        packet.setAttribute("opacity", 1); packet.setAttribute("cx", a2[0] + (b2[0] - a2[0]) * Math.min(1, v * 1.5)); packet.setAttribute("cy", a2[1] + (b2[1] - a2[1]) * Math.min(1, v * 1.5));
        if (v > 0.6) { boxLbl.setAttribute("fill", GREEN); boxLbl.textContent = "✓ fibre B lit"; }
        say("The tip lands and checks in down the new fibre. The base box hears it: fibre B is lit.");
      } else {
        packet.setAttribute("opacity", 0);
        setDrone(lerp(at, BASE, (u - 0.7) / 0.3), true);
        tally.textContent = count(route());
        say("Two fibres again. Our cost: one tip dart, about $100 with its fibre, and about 10 minutes of flying.");
      }
      if (u > 0.99) drone.setAttribute("opacity", 0);
    }],
    [4, function () {
      clock.textContent = "Day 28, re-lay · GPS jammed"; boxLbl.textContent = "";
      SORTIE.forEach(function (i) { nodes[i].hidden = true; });
      gGhost.setAttribute("opacity", 1); tally.textContent = count(route());
      tally.textContent = "Last re-lay sortie: front darts " + nm(SORTIE[0]) + " to " + nm(SORTIE[3]);
      say("A re-lay with GPS jammed. The drone flies on compass, optical flow and lidar from an origin set at launch, and its compass is 3° off.");
    }],
    [9, function (u) {
      var path = [BASE].concat(DROPS), seg = u / 0.7;
      if (u < 0.7) {
        setDrone(fly(path, seg), true);
        var done = Math.floor(seg * (path.length - 1) + 0.02);
        SORTIE.forEach(function (i, k) { if (k < done && nodes[i].hidden) { move(nodes[i], DROPS[k]); nodes[i].hidden = false; route(); } });
        say("Each drop lands about " + commas(Math.round(distFt(PLAN[SORTIE[0]], DROPS[0]) / 10) * 10) + " ft from its planned point. Darts in one sortie are off together, so each is still relayed by the one before.");
      } else {
        SORTIE.forEach(function (i, k) { if (nodes[i].hidden) { move(nodes[i], DROPS[k]); nodes[i].hidden = false; } });
        route(); setDrone(LAST, true);
        var a = sx(LAST), b = sx(NEXT);
        bad.setAttribute("x1", a[0]); bad.setAttribute("y1", a[1]); bad.setAttribute("x2", b[0]); bad.setAttribute("y2", b[1]); bad.setAttribute("opacity", 1);
        badLbl.setAttribute("x", (a[0] + b[0]) / 2 + 14); badLbl.setAttribute("y", (a[1] + b[1]) / 2 - 22); badLbl.textContent = commas(GAP) + " ft";
        ear.setAttribute("x", a[0] - 12); ear.setAttribute("y", a[1] + 26); ear.setAttribute("fill", RED); ear.setAttribute("text-anchor", "middle"); ear.textContent = "relayed by " + nm(SORTIE[2]) + " only";
        say(nm(SORTIE[3]) + " closes the row, so it must be relayed from both sides. " + nm(SORTIE[2]) + " relays it; " + nm(SORTIE[3] + 1) + " doesn't: " + nm(SORTIE[3]) + " landed " + commas(GAP) + " ft from " + nm(SORTIE[3] + 1) + ", out of reach.");
      }
    }],
    [7, function (u) {
      if (u < 0.3) { setDrone(lerp(LAST, SPARE, u / 0.3), true); say("So it drops a spare " + STEP_BACK + " ft toward " + nm(SORTIE[3] + 1) + "'s logged point."); }
      else {
        setDrone(SPARE, true);
        if (spare.hidden) { spare.hidden = false; route(); bad.setAttribute("opacity", 0); badLbl.textContent = ""; }
        ear.setAttribute("text-anchor", "start"); var s = sx(SPARE); ear.setAttribute("x", s[0] + 14); ear.setAttribute("y", s[1] + 5); ear.setAttribute("fill", GREEN); ear.textContent = "✓ relayed by " + nm(SORTIE[3]) + " and " + nm(SORTIE[3] + 1);
        tally.textContent = count(route());
        say(nm(SORTIE[3]) + " and " + nm(SORTIE[3] + 1) + " both relay the spare's 'landed' message: the row is closed. It cost one spare dart; the drone never needed to know where it was to within a hop.");
      }
    }],
    [3, function () { drone.setAttribute("opacity", 0); ear.textContent = ""; }]
  ];

  var si = 0, t = 0, playing = false, last = 0;
  function step(dt) {
    t += dt;
    var sc = scenes[si];
    sc[1](Math.min(1, t / sc[0]));
    if (t >= sc[0]) { t = 0; si++; if (si >= scenes.length) { si = 0; reset(); } }
  }
  function frame(ts) {
    var dt = last ? Math.min(0.1, (ts - last) / 1000) : 0;
    last = ts;
    step(dt);
    if (playing) requestAnimationFrame(frame);
  }
  function play() { if (playing) return; playing = true; last = 0; requestAnimationFrame(frame); if (btn) btn.textContent = "Pause"; }
  function pause() { playing = false; if (btn) btn.textContent = "Play"; }
  function restart() { si = 0; t = 0; reset(); scenes[0][1](0); }

  restart();
  if (btn) btn.addEventListener("click", function () { playing ? pause() : play(); });
  var replay = document.getElementById("repair-replay");
  if (replay) replay.addEventListener("click", function () { restart(); play(); });
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? play() : pause(); }); }, { threshold: 0.3 }).observe(box);
  }
  window.__repair = { step: step, restart: restart, nodes: function () { return nodes; }, GAP: GAP, SPARE: SPARE, LAST: LAST, NEXT: NEXT,
    scene: function () { return si; }, route: route };
})();
