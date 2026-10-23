// Animated repair model for the two-trunk net: a dart is knocked out, the daily roll call finds it,
// one sortie replaces it, and a re-lay flown on a compass 3° off is caught by confirm-after-release.
// Same geometry and scale as line-layout.js. All distances are in feet.
(function () {
  var box = document.getElementById("repair-model");
  if (!box) return;

  var NS = "http://www.w3.org/2000/svg";
  var FT = 0.058;
  var HEAR = 656, ALT = 165, HOP = 980;
  var NEED = 88 * 65;
  var REFF = Math.sqrt(HEAR * HEAR - ALT * ALT);
  var DEPTH = NEED - Math.sqrt(REFF * REFF - HOP * HOP / 4);
  var W = 1640, UX = 300, UY = 520;
  var ACC = "#c2562c", GREEN = "#4f7a3a", BLUE = "#1f5f8b", GREY = "#8a8a8a", RED = "#b3261e";
  var POS = [[-W / 2, 0], [0, 0], [W / 2, 0]];
  var DRIFT = 3, STEP_BACK = 300, KILL = 12;   // compass error in degrees; spare offset; relay 3, left trunk

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
  function rot(p, deg) { var t = deg * Math.PI / 180; return [p[0] * Math.cos(t) - p[1] * Math.sin(t), p[0] * Math.sin(t) + p[1] * Math.cos(t)]; }
  function commas(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }

  function frontRow() {
    var a = DEPTH * Math.PI / 4, len = W + 2 * a;
    function pt(u) {
      var th;
      if (u < a) { th = Math.PI / 4 * (1 - u / a); return [-W / 2 - DEPTH * Math.sin(th), DEPTH * Math.cos(th)]; }
      if (u <= a + W) return [-W / 2 + (u - a), DEPTH];
      th = Math.PI / 4 * (u - a - W) / a; return [W / 2 + DEPTH * Math.sin(th), DEPTH * Math.cos(th)];
    }
    var usable = len - 2 * REFF, n = Math.ceil(usable / HOP) + 1, step = usable / (n - 1), out = [];
    for (var i = 0; i < n; i++) out.push(pt(REFF + i * step));
    return out;
  }
  var FRONT = frontRow(), NF = FRONT.length;
  var PLAN = FRONT.slice();
  [1, NF - 2].forEach(function (j) { for (var k = 1; k <= 5; k++) PLAN.push([FRONT[j][0] * k / 6, FRONT[j][1] * k / 6]); });
  var SORTIE = [3, 4, 5, 6];   // the re-lay sortie that closes the front row between darts 2 and 7

  var svg = el("svg", { viewBox: "0 0 600 590", width: "100%", role: "img",
    "aria-labelledby": "rmTitle rmDesc", style: "font-family:inherit;color:inherit;display:block" }, box);
  el("title", { id: "rmTitle" }).textContent = "How the net is repaired, seen from above";
  el("desc", { id: "rmDesc" }).textContent = "To scale. A shell knocks out a relay dart on the left trunk and alerts re-route to the right trunk. " +
    "The daily roll call finds it missing and one drone sortie drops a replacement. Then a re-lay sortie flown on a compass 3 degrees off " +
    "lands its last dart 1,250 feet from its neighbour; the drone hears no relay, drops a spare 300 feet closer, and the link is confirmed.";

  el("rect", { x: 0, y: 0, width: 600, height: 590, fill: "#efe9d8" });
  el("rect", { x: 0, y: 0, width: 600, height: 84, fill: ACC, "fill-opacity": 0.1 });
  text(300, 32, "ENEMY SIDE", { "text-anchor": "middle", "font-size": 22, "font-weight": 700, "letter-spacing": "0.08em", fill: ACC });
  var clock = text(300, 60, "", { "text-anchor": "middle", "font-size": 16, "font-weight": 700, opacity: 0.85 });
  el("rect", { x: 0, y: UY - 13, width: 600, height: 26, fill: GREEN, "fill-opacity": 0.7 });
  POS.forEach(function (p, i) {
    var s = sx(p);
    el("rect", { x: s[0] - 6, y: s[1] - 5, width: 12, height: 10, rx: 2, fill: "#3b2f22" });
    if (i === 1) text(s[0], UY + 34, "P2 · receiver", { "text-anchor": "middle", "font-size": 15, "font-weight": 700 });
    else text(s[0] + (i ? 12 : -12), UY + 5, i ? "P3" : "P1", { "text-anchor": i ? "start" : "end", "font-size": 15, "font-weight": 700, fill: "#fff" });
  });
  var tally = text(300, UY + 58, "", { "text-anchor": "middle", "font-size": 15, "font-weight": 700, opacity: 0.85 });
  el("line", { x1: 20, y1: 570, x2: 20 + 2000 * FT, y2: 570, stroke: "currentColor", "stroke-width": 3 });
  text(20, 560, "2,000 ft", { "font-size": 13, opacity: 0.85 });
  text(300, 108, "circles: listening darts · squares: relay darts · dotted: planned points", { "text-anchor": "middle", "font-size": 13, opacity: 0.85 });

  var gGhost = el("g", {}), gLinks = el("g", {}), gNodes = el("g", {}), gFx = el("g", {});
  var bad = el("line", { stroke: RED, "stroke-width": 2.5, "stroke-dasharray": "6 4", opacity: 0 }, gFx);
  var badLbl = text(0, 0, "", { "font-size": 14, "font-weight": 700, fill: RED, "text-anchor": "middle" }, gFx);
  var blast = el("circle", { r: 0, fill: ACC, opacity: 0 }, gFx);
  var pulse = el("circle", { r: 0, fill: "none", stroke: ACC, "stroke-width": 2, opacity: 0 }, gFx);
  var packet = el("circle", { r: 5, fill: BLUE, opacity: 0 }, gFx);
  var drone = el("g", { opacity: 0 }, gFx);
  var ds = el("g", { transform: "scale(1.4)" }, drone);
  [[-5, -5], [5, -5], [-5, 5], [5, 5]].forEach(function (p) {
    el("circle", { cx: p[0], cy: p[1], r: 3.2, fill: "none", stroke: "#111", "stroke-width": 1.2 }, ds);
  });
  el("rect", { x: -3, y: -3, width: 6, height: 6, fill: "#111" }, ds);
  var ear = text(0, 0, "", { "font-size": 14, "font-weight": 700, "text-anchor": "start" }, gFx);

  var panel = document.getElementById("repair-status");
  var btn = document.getElementById("repair-play");
  function say(s) { if (panel && panel.textContent !== s) panel.textContent = s; }

  var nodes;
  function node(p, listen) {
    var s = sx(p), d = { p: p, listen: listen, dead: false, hidden: false, x: s[0], y: s[1] };
    d.dot = listen ? el("circle", { cx: d.x, cy: d.y, r: 5.5, "stroke-width": 2 }, gNodes)
                   : el("rect", { x: d.x - 5, y: d.y - 5, width: 10, height: 10, "stroke-width": 2 }, gNodes);
    d.xm = el("path", { d: "M" + (d.x - 6) + " " + (d.y - 6) + " l12 12 m0 -12 l-12 12", stroke: "#111", "stroke-width": 2.2, opacity: 0 }, gNodes);
    return d;
  }
  function move(d, p) {
    var s = sx(p); d.p = p; d.x = s[0]; d.y = s[1];
    if (d.listen) { d.dot.setAttribute("cx", d.x); d.dot.setAttribute("cy", d.y); }
    else { d.dot.setAttribute("x", d.x - 5); d.dot.setAttribute("y", d.y - 5); }
    d.xm.setAttribute("d", "M" + (d.x - 6) + " " + (d.y - 6) + " l12 12 m0 -12 l-12 12");
  }
  function live(d) { return !d.dead && !d.hidden; }

  // breadth-first from the receiver over live darts, hops of <= HOP ft
  function route() {
    var n = nodes.length, seen = [], q = [], i, j;
    while (gLinks.firstChild) gLinks.removeChild(gLinks.firstChild);
    for (i = 0; i < n; i++) seen.push(false);
    function link(a, b) { el("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: BLUE, "stroke-opacity": 0.55, "stroke-dasharray": "4 3" }, gLinks); }
    for (i = 0; i < n; i++) if (live(nodes[i]) && distFt(nodes[i].p, POS[1]) <= HOP) { seen[i] = true; q.push(i); link([nodes[i].x, nodes[i].y], sx(POS[1])); }
    while (q.length) {
      var a = q.shift();
      for (j = 0; j < n; j++) if (live(nodes[j]) && !seen[j] && distFt(nodes[a].p, nodes[j].p) <= HOP) {
        seen[j] = true; q.push(j); link([nodes[j].x, nodes[j].y], [nodes[a].x, nodes[a].y]);
      }
    }
    var up = 0, total = 0;
    nodes.forEach(function (d, k) {
      d.cut = live(d) && !seen[k];
      if (!d.hidden) { total++; if (seen[k]) up++; }
      d.dot.setAttribute("fill", d.dead ? "#ddd" : "#fff");
      d.dot.setAttribute("stroke", d.dead || d.cut ? GREY : (d.listen ? ACC : BLUE));
      d.dot.setAttribute("opacity", d.hidden ? 0 : 1);
      d.xm.setAttribute("opacity", d.dead && !d.hidden ? 1 : 0);
    });
    return { up: up, total: total };
  }

  // ghost rings at the planned points of the re-lay sortie
  SORTIE.forEach(function (i) { var s = sx(PLAN[i]); el("circle", { cx: s[0], cy: s[1], r: 7, fill: "none", stroke: ACC, "stroke-dasharray": "2 2", "stroke-opacity": 0.8 }, gGhost); });
  gGhost.setAttribute("opacity", 0);

  var DROPS = SORTIE.map(function (i) { return rot(PLAN[i], DRIFT); });
  var LAST = DROPS[DROPS.length - 1], NEXT = PLAN[SORTIE[SORTIE.length - 1] + 1];
  var GAP = distFt(LAST, NEXT);
  var SPARE = lerp(LAST, NEXT, STEP_BACK / GAP);

  function setDrone(p, show) { var s = sx(p); drone.setAttribute("transform", "translate(" + s[0] + " " + s[1] + ")"); drone.setAttribute("opacity", show ? 1 : 0); }
  function ring(el_, p, u) { var s = sx(p); el_.setAttribute("cx", s[0]); el_.setAttribute("cy", s[1]); el_.setAttribute("r", 6 + 34 * u); el_.setAttribute("opacity", 0.9 * (1 - u)); }
  function fly(path, u) { // position along a polyline, u in 0..1
    var L = 0, segs = [], i;
    for (i = 1; i < path.length; i++) { var l = distFt(path[i - 1], path[i]); segs.push(l); L += l; }
    var want = u * L;
    for (i = 0; i < segs.length; i++) { if (want <= segs[i]) return lerp(path[i], path[i + 1], segs[i] ? want / segs[i] : 0); want -= segs[i]; }
    return path[path.length - 1];
  }

  var spare;
  function reset() {
    while (gNodes.firstChild) gNodes.removeChild(gNodes.firstChild);
    nodes = PLAN.map(function (p, i) { return node(p, i < NF); });
    spare = node(SPARE, true); spare.hidden = true;
    nodes.push(spare);
    gGhost.setAttribute("opacity", 0);
    [bad, blast, pulse, packet].forEach(function (e) { e.setAttribute("opacity", 0); });
    badLbl.textContent = ""; ear.textContent = ""; drone.setAttribute("opacity", 0);
    var c = route(); tally.textContent = c.up + " of " + c.total + " darts reach the unit";
  }

  // scenes: [seconds, function(u, first)]
  var scenes = [
    [3, function (u) {
      clock.textContent = "Day 1, 02:10";
      say("A shell knocks out relay 3 on the left trunk.");
      if (u < 0.5) { var s = sx(PLAN[KILL]); blast.setAttribute("cx", s[0]); blast.setAttribute("cy", s[1]); blast.setAttribute("r", 4 + 40 * u * 2); blast.setAttribute("opacity", 0.6 * (1 - u * 2)); }
      else if (!nodes[KILL].dead) { blast.setAttribute("opacity", 0); nodes[KILL].dead = true; route(); }
    }],
    [4, function () {
      say("Alerts re-route along the front row to the right trunk. Nothing tells the unit yet: the net is now one-trunk fragile.");
    }],
    [5, function (u) {
      clock.textContent = "Day 1, 06:00";
      var n = nodes.length - 1, k = Math.min(n - 1, Math.floor(u * n * 1.2)), heard = 0;
      for (var i = 0; i < n; i++) if (live(nodes[i])) { if (i <= k) heard++; }
      var d = nodes[Math.min(k, n - 1)];
      if (live(d) && u < 0.83) ring(pulse, d.p, (u * n * 1.2) % 1); else pulse.setAttribute("opacity", 0);
      tally.textContent = "Roll call: " + heard + " of 20 answered";
      say(u < 0.83 ? "Daily roll call: every dart sends one check-in, and the others relay it once." :
        "19 of 20 answered. Missing: relay 3, left trunk. The receiver names it from the plan. Repair it on the next sortie.");
    }],
    [7, function (u) {
      clock.textContent = "Day 1, 06:20";
      var home = POS[1], at = PLAN[KILL], d = nodes[KILL];
      if (u < 0.35) { setDrone(lerp(home, at, u / 0.35), true); tally.textContent = "Repair: relay 3, left trunk"; say("Repair sortie: one relay dart to its planned point."); }
      else if (u < 0.65) {
        setDrone(at, true);
        if (d.dead) { d.dead = false; route(); d.dot.setAttribute("fill", "#cfe0ec"); }
        var v = (u - 0.35) / 0.3; ring(pulse, at, (v * 2) % 1);
        var nb = nodes[KILL - 1]; packet.setAttribute("opacity", 1); var s = sx(lerp(at, nb.p, Math.min(1, v * 1.5))); packet.setAttribute("cx", s[0]); packet.setAttribute("cy", s[1]);
        var ds_ = sx(at); ear.setAttribute("x", ds_[0] + 14); ear.setAttribute("y", ds_[1] + 5); ear.setAttribute("fill", GREEN); ear.textContent = v > 0.6 ? "✓ relayed" : "";
        say("The new dart sends 'landed'. Its neighbour relays it, and the drone hears that relay: the link works.");
      } else {
        pulse.setAttribute("opacity", 0); packet.setAttribute("opacity", 0); ear.textContent = "";
        setDrone(lerp(at, home, (u - 0.65) / 0.35), true);
        var c = route(); tally.textContent = c.up + " of " + c.total + " darts reach the unit";
        say("Two trunks again. Our cost: one relay dart, about $25, and about 10 minutes of flying.");
      }
      if (u > 0.99) drone.setAttribute("opacity", 0);
    }],
    [4, function () {
      clock.textContent = "Day 28, re-lay · GPS jammed";
      SORTIE.forEach(function (i) { nodes[i].hidden = true; });
      gGhost.setAttribute("opacity", 1); route();
      tally.textContent = "Last re-lay sortie: front darts 3 to 6";
      say("A re-lay with GPS jammed. The drone flies on compass, optical flow and barometer, and its compass is 3° off.");
    }],
    [9, function (u) {
      var path = [POS[1]].concat(DROPS), seg = u / 0.7;
      if (u < 0.7) {
        setDrone(fly(path, seg), true);
        var done = Math.floor(seg * (path.length - 1) + 0.02);
        SORTIE.forEach(function (i, k) { if (k < done && nodes[i].hidden) { move(nodes[i], DROPS[k]); nodes[i].hidden = false; route(); } });
        say("Each drop lands about " + commas(Math.round(DEPTH * Math.tan(DRIFT * Math.PI / 180) / 10) * 10) + " ft from its planned point. Darts in one sortie are off together, so they still reach each other.");
      } else {
        SORTIE.forEach(function (i, k) { if (nodes[i].hidden) { move(nodes[i], DROPS[k]); nodes[i].hidden = false; } });
        route(); setDrone(LAST, true);
        var a = sx(LAST), b = sx(NEXT);
        bad.setAttribute("x1", a[0]); bad.setAttribute("y1", a[1]); bad.setAttribute("x2", b[0]); bad.setAttribute("y2", b[1]); bad.setAttribute("opacity", 1);
        badLbl.setAttribute("x", (a[0] + b[0]) / 2 + 14); badLbl.setAttribute("y", (a[1] + b[1]) / 2 - 22); badLbl.textContent = commas(GAP) + " ft";
        ear.setAttribute("x", a[0] - 12); ear.setAttribute("y", a[1] + 26); ear.setAttribute("fill", RED); ear.setAttribute("text-anchor", "middle"); ear.textContent = "no relay heard";
        say("The last drop lands " + commas(GAP) + " ft from dart 7, out of reach. The drone hears no relay of its 'landed' message.");
      }
    }],
    [7, function (u) {
      if (u < 0.3) { setDrone(lerp(LAST, SPARE, u / 0.3), true); say("So it drops a spare " + STEP_BACK + " ft toward dart 7's logged point."); }
      else {
        setDrone(SPARE, true);
        if (spare.hidden) { spare.hidden = false; route(); bad.setAttribute("opacity", 0); badLbl.textContent = ""; }
        ear.setAttribute("text-anchor", "start"); var s = sx(SPARE); ear.setAttribute("x", s[0] + 14); ear.setAttribute("y", s[1] + 5); ear.setAttribute("fill", GREEN); ear.textContent = "✓ relayed";
        var c = route(); tally.textContent = c.up + " of " + c.total + " darts reach the unit";
        say("Dart 7 relays the spare's 'landed' message: the row is closed. It cost one spare dart; the drone never needed to know where it was to within a hop.");
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
