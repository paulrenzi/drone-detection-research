// Animated top-down map of a dart net in front of a unit of three positions.
// Listening darts form a front row; relay darts carry the alert home. Tap a dart to knock it out.
// Scale: 1 svg unit = 1/FT ft. All distances below are in feet.
(function () {
  var box = document.getElementById("line-layout");
  if (!box) return;

  var NS = "http://www.w3.org/2000/svg";
  var FT = 0.058;                       // svg units per foot (~17 ft per unit)
  var HEAR = 656, ALT = 165, HOP = 980; // hearing range; drone height; longest radio hop (~300 m)
  var MPH = 60, FTS = MPH * 5280 / 3600, NEED = FTS * 65; // a minute plus 5 s to pass it back
  var REFF = Math.sqrt(HEAR * HEAR - ALT * ALT);           // hearing along the ground at 165 ft up
  var SPACE = HOP;                                          // front darts must reach each other by radio
  var DEPTH = NEED - Math.sqrt(REFF * REFF - SPACE * SPACE / 4); // front row distance from the unit
  var W = 1640;                         // 3 positions, 820 ft apart
  var R = REFF * FT;
  var UX = 300, UY = 520;               // the middle position, with the receiver
  var SPEEDUP = 10, HOP_SECS = 0.3;
  var ACC = "#c2562c", GREEN = "#4f7a3a", BLUE = "#1f5f8b", GREY = "#8a8a8a";
  var POS = [[-W / 2, 0], [0, 0], [W / 2, 0]];

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
  function fmt(s) { s = Math.max(0, Math.round(s)); return s >= 60 ? Math.floor(s / 60) + " min " + (s % 60) + " s" : s + " s"; }
  function commas(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }

  // ---- the front row: an arc around the positions, ±45° from each, one radio hop apart
  function frontRow() {
    var a = DEPTH * Math.PI / 4, len = W + 2 * a;
    function pt(u) {
      var th;
      if (u < a) { th = Math.PI / 4 * (1 - u / a); return [-W / 2 - DEPTH * Math.sin(th), DEPTH * Math.cos(th)]; }
      if (u <= a + W) return [-W / 2 + (u - a), DEPTH];
      th = Math.PI / 4 * (u - a - W) / a; return [W / 2 + DEPTH * Math.sin(th), DEPTH * Math.cos(th)];
    }
    var usable = len - 2 * REFF, n = Math.ceil(usable / SPACE) + 1, step = usable / (n - 1), out = [];
    for (var i = 0; i < n; i++) out.push(pt(REFF + i * step));
    return out;
  }
  function leg(to) { // 5 relays, evenly spaced from the receiver to a front dart
    var out = [];
    for (var k = 1; k <= 5; k++) out.push([to[0] * k / 6, to[1] * k / 6]);
    return out;
  }
  var FRONT = frontRow(), NF = FRONT.length;
  var LAYOUTS = {
    v: { label: "two trunks", legs: [1, NF - 2] }
  };

  var svg = el("svg", { viewBox: "0 0 600 590", width: "100%", role: "img",
    "aria-labelledby": "llTitle llDesc", style: "font-family:inherit;color:inherit;display:block" }, box);
  var titleEl = el("title", { id: "llTitle" });
  var descEl = el("desc", { id: "llDesc" });

  // ground, enemy side, the 45° edges, the positions
  el("rect", { x: 0, y: 0, width: 600, height: 590, fill: "#efe9d8" });
  el("rect", { x: 0, y: 0, width: 600, height: 84, fill: ACC, "fill-opacity": 0.1 });
  text(300, 32, "ENEMY SIDE", { "text-anchor": "middle", "font-size": 22, "font-weight": 700, "letter-spacing": "0.08em", fill: ACC });
  text(300, 60, "drones launch from farther out, off the map", { "text-anchor": "middle", "font-size": 16, opacity: 0.85 });
  [[-1, POS[0]], [1, POS[2]]].forEach(function (e) {
    var a = sx(e[1]), len = (UY - 90);
    el("line", { x1: a[0], y1: a[1], x2: a[0] + e[0] * len, y2: a[1] - len, stroke: ACC, "stroke-opacity": 0.45, "stroke-dasharray": "6 5" });
  });
  text(118, 330, "45°", { "font-size": 15, "font-weight": 700, fill: ACC });
  text(462, 330, "45°", { "font-size": 15, "font-weight": 700, fill: ACC });
  el("rect", { x: 0, y: UY - 13, width: 600, height: 26, fill: GREEN, "fill-opacity": 0.7 });
  POS.forEach(function (p, i) {
    var s = sx(p);
    el("circle", { cx: s[0], cy: s[1], r: R, fill: "none", stroke: BLUE, "stroke-dasharray": "3 3", "stroke-opacity": 0.7 });
    el("rect", { x: s[0] - 6, y: s[1] - 5, width: 12, height: 10, rx: 2, fill: "#3b2f22" });
    if (i === 1) text(s[0], UY + 34, "P2 · receiver", { "text-anchor": "middle", "font-size": 15, "font-weight": 700 });
    else text(s[0] + (i ? 12 : -12), UY + 5, i ? "P3" : "P1", { "text-anchor": i ? "start" : "end", "font-size": 15, "font-weight": 700, fill: "#fff" });
  });
  text(300, UY + 58, "YOUR UNIT · 3 positions, 1,640 ft across", { "text-anchor": "middle", "font-size": 15, "font-weight": 700, opacity: 0.75 });
  // scale bar, 2,000 ft
  el("line", { x1: 20, y1: 570, x2: 20 + 2000 * FT, y2: 570, stroke: "currentColor", "stroke-width": 3 });
  text(20, 560, "2,000 ft", { "font-size": 13, opacity: 0.85 });

  var gLinks = el("g", {}), gLay = el("g", {});
  var trail = el("path", { d: "", fill: "none", stroke: "#222", "stroke-opacity": 0.45, "stroke-dasharray": "2 4", "stroke-width": 1.5 });
  var pulse = el("circle", { r: 0, fill: "none", stroke: ACC, "stroke-width": 2, opacity: 0 });
  var packet = el("circle", { r: 5, fill: BLUE, opacity: 0 });
  var drone = el("g", {});
  var ds = el("g", { transform: "scale(1.4)" }, drone);
  [[-5, -5], [5, -5], [-5, 5], [5, 5]].forEach(function (p) {
    el("circle", { cx: p[0], cy: p[1], r: 3.2, fill: "none", stroke: "#111", "stroke-width": 1.2 }, ds);
  });
  el("rect", { x: -3, y: -3, width: 6, height: 6, fill: "#111" }, ds);

  var netEl = document.getElementById("line-layout-net");
  var lay, nodes, hopTo;   // hopTo[i] = next node toward the receiver (-1 = receiver, undefined = cut off)

  function build(name) {
    lay = LAYOUTS[name];
    while (gLay.firstChild) gLay.removeChild(gLay.firstChild);
    nodes = FRONT.map(function (p) { return { p: p, listen: true, dead: false }; });
    lay.legs.forEach(function (j) { leg(FRONT[j]).forEach(function (p) { nodes.push({ p: p, listen: false, dead: false }); }); });
    nodes.forEach(function (d) {
      var s = sx(d.p); d.x = s[0]; d.y = s[1];
      if (d.listen) d.ring = el("circle", { cx: d.x, cy: d.y, r: R, fill: ACC, "fill-opacity": 0.08, stroke: ACC, "stroke-opacity": 0.35 }, gLay);
    });
    nodes.forEach(function (d, k) {
      d.dot = d.listen ? el("circle", { cx: d.x, cy: d.y, r: 5.5, "stroke-width": 2 }, gLay)
                       : el("rect", { x: d.x - 5, y: d.y - 5, width: 10, height: 10, "stroke-width": 2 }, gLay);
      d.x1 = el("path", { d: "M" + (d.x - 6) + " " + (d.y - 6) + " l12 12 m0 -12 l-12 12", stroke: "#111", "stroke-width": 2.2, opacity: 0 }, gLay);
      var hit = el("circle", { cx: d.x, cy: d.y, r: 13, fill: "transparent", style: "cursor:pointer" }, gLay);
      hit.addEventListener("click", function () { d.dead = !d.dead; route(); reset(st ? st.idx : 0); });
    });
    var top = sx([0, DEPTH]);
    text(300, top[1] - R - 10, "front row: " + NF + " listening darts, " + (DEPTH / 5280).toFixed(2) + " mi out", { "text-anchor": "middle", "font-size": 15, "font-weight": 700, fill: ACC }, gLay);
    text(300, 108, "circles: what each dart hears · squares: relay darts, no mic", { "text-anchor": "middle", "font-size": 13, opacity: 0.85 }, gLay);
    var total = nodes.length;
    titleEl.textContent = "A net of " + total + " darts in front of a unit, seen from above: " + lay.label;
    descEl.textContent = "To scale. " + NF + " listening darts sit in an arc " + (DEPTH / 5280).toFixed(2) +
      " miles in front of three positions, covering 45 degrees either side of each. " +
      (lay.legs.length > 1 ? "Two chains of five relay darts, one at each end of the arc, carry the alert back to the receiver."
                           : "One chain of five relay darts carries the alert from the middle of the arc back to the receiver.") +
      " Drones come in at 60 mph straight on, 30 degrees from the left and 45 degrees from the right.";
    route();
  }

  // radio links: breadth-first from the receiver over live darts, hops of <= HOP ft
  function route() {
    var n = nodes.length, hops = [], i, j, q = [];
    hopTo = new Array(n);
    for (i = 0; i < n; i++) hops.push(Infinity);
    for (i = 0; i < n; i++) if (!nodes[i].dead && distFt(nodes[i].p, POS[1]) <= HOP) { hops[i] = 1; hopTo[i] = -1; q.push(i); }
    while (q.length) {
      var a = q.shift();
      for (j = 0; j < n; j++) if (!nodes[j].dead && hops[j] === Infinity && distFt(nodes[a].p, nodes[j].p) <= HOP) { hops[j] = hops[a] + 1; hopTo[j] = a; q.push(j); }
    }
    while (gLinks.firstChild) gLinks.removeChild(gLinks.firstChild);
    var dead = 0, cut = 0;
    nodes.forEach(function (d, k) {
      d.cut = !d.dead && hopTo[k] === undefined;
      if (d.dead) dead++; else if (d.cut && d.listen) cut++;
      if (hopTo[k] !== undefined) {
        var to = hopTo[k] === -1 ? sx(POS[1]) : [nodes[hopTo[k]].x, nodes[hopTo[k]].y];
        el("line", { x1: d.x, y1: d.y, x2: to[0], y2: to[1], stroke: BLUE, "stroke-opacity": 0.55, "stroke-dasharray": "4 3" }, gLinks);
      }
    });
    paint();
    if (netEl) netEl.textContent = !dead ? "All " + nodes.length + " darts reach the unit. Tap a dart to knock it out." :
      dead + " knocked out · " + (cut ? cut + " listening dart" + (cut > 1 ? "s" : "") + " cut off from the unit." : "every live listening dart still reaches the unit.");
  }
  function paint() {
    nodes.forEach(function (d) {
      var off = d.dead || d.cut;
      d.dot.setAttribute("fill", d.dead ? "#ddd" : "#fff");
      d.dot.setAttribute("stroke", off ? GREY : (d.listen ? ACC : BLUE));
      d.x1.setAttribute("opacity", d.dead ? 1 : 0);
      if (d.ring) { d.ring.setAttribute("fill-opacity", off ? 0.03 : 0.08); d.ring.setAttribute("stroke", off ? GREY : ACC); }
    });
  }

  // ---- three passes at 60 mph
  function approach(target, phiDeg) {
    var phi = phiDeg * Math.PI / 180, dir = [Math.sin(phi), Math.cos(phi)];
    var rTop = ((UY - 90) / FT - target[1]) / dir[1];
    var rSide = dir[0] ? ((dir[0] > 0 ? 296 : -296) / FT - target[0]) / dir[0] : Infinity;
    var r0 = Math.min(rTop, rSide);
    return { rFt: r0, at: function (t) { var r = r0 * (1 - t); return [target[0] + r * dir[0], target[1] + r * dir[1]]; } };
  }
  var passes = [
    { a: approach(POS[1], 0), intro: "A drone flies straight at P2, exactly between two front darts: the worst case." },
    { a: approach(POS[0], -30), intro: "A drone comes in at P1 from 30° to the left." },
    { a: approach(POS[2], 45), intro: "A drone comes in at P3 from 45° to the right, the edge of the net." }
  ];

  var panel = document.getElementById("line-layout-status");
  var btn = document.getElementById("line-layout-play");
  function say(s) { if (panel) panel.textContent = s; }

  var st, playing = false, last = 0;
  function reset(idx) {
    st = { idx: idx, t: 0, hit: -1, route: null, hopT: 0, warn: null, done: 0, d: [], cutHeard: false };
    paint();
    trail.setAttribute("d", ""); packet.setAttribute("opacity", 0); pulse.setAttribute("opacity", 0);
    var p0 = sx(passes[idx].a.at(0));
    drone.setAttribute("transform", "translate(" + p0[0] + " " + p0[1] + ")");
    say(passes[idx].intro);
  }

  function step(dt) {
    var a = passes[st.idx].a;
    if (st.done) { st.done += dt; if (st.done > 3.5) reset((st.idx + 1) % passes.length); return; }
    st.t = Math.min(1, st.t + dt / (a.rFt / FTS / SPEEDUP));
    var g = a.at(st.t), pos = sx(g), leftS = a.rFt * (1 - st.t) / FTS;
    drone.setAttribute("transform", "translate(" + pos[0] + " " + pos[1] + ")");
    st.d.push(pos[0].toFixed(1) + " " + pos[1].toFixed(1));
    trail.setAttribute("d", "M" + st.d.join(" L"));

    if (st.hit < 0) {
      for (var i = 0; i < nodes.length; i++) {
        var d = nodes[i];
        if (!d.listen || d.dead || distFt(g, d.p) > REFF) continue;
        if (d.cut) { st.cutHeard = true; continue; }
        st.hit = i; st.warn = leftS; st.hopT = 0;
        var route = [[d.x, d.y]], k = i;
        while (k !== -1) { k = hopTo[k]; route.push(k === -1 ? sx(POS[1]) : [nodes[k].x, nodes[k].y]); if (k !== -1) nodes[k].dot.setAttribute("fill", "#cfe0ec"); }
        st.route = route;
        d.dot.setAttribute("fill", ACC); d.ring.setAttribute("fill-opacity", 0.25);
        break;
      }
      if (st.hit < 0 && POS.some(function (p) { return distFt(g, p) < REFF; })) { st.hit = 99; st.warn = leftS; }
    }
    if (st.hit >= 0 && st.hit !== 99) {
      st.hopT += dt;
      var h = nodes[st.hit], ph = (st.hopT % 0.8) / 0.8;
      pulse.setAttribute("cx", h.x); pulse.setAttribute("cy", h.y);
      pulse.setAttribute("r", 6 + 34 * ph); pulse.setAttribute("opacity", 0.9 * (1 - ph));
      var nh = st.route.length - 1, f = st.hopT / HOP_SECS;
      if (f < nh) {
        var s = Math.floor(f), u = f - s, A = st.route[s], B = st.route[s + 1];
        packet.setAttribute("opacity", 1);
        packet.setAttribute("cx", A[0] + (B[0] - A[0]) * u); packet.setAttribute("cy", A[1] + (B[1] - A[1]) * u);
        say("A front dart heard it " + commas(st.warn * FTS) + " ft out. Passing the alert home: hop " + (s + 1) + " of " + nh + "…");
      } else {
        packet.setAttribute("opacity", 0);
        say("ALERT at all 3 positions · drone arrives in about " + fmt(leftS) + ". Take cover.");
      }
    } else if (st.hit === 99) {
      say("No dart could get it home. Only the unit's own ears catch it, about " + fmt(st.warn) + " out.");
    } else if (st.cutHeard) {
      say("A dart heard it, but a knocked-out dart cut its route home.");
    }
    if (st.t >= 1) {
      st.done = 0.0001;
      say("Warning: " + (st.warn != null ? "about " + fmt(st.warn) : "none") + (st.hit >= 0 && st.hit !== 99 ? " from the darts, before a few seconds of relaying" : "") + ".");
    }
  }

  function frame(ts) {
    var dt = last ? Math.min(0.1, (ts - last) / 1000) : 0;
    last = ts;
    step(dt);
    if (playing) requestAnimationFrame(frame);
  }
  function play() { if (playing) return; playing = true; last = 0; requestAnimationFrame(frame); if (btn) btn.textContent = "Pause"; }
  function pause() { playing = false; if (btn) btn.textContent = "Play"; }

  function choose(name) {
    build(name); reset(0);
    var bs = document.querySelectorAll("[data-layout]");
    for (var i = 0; i < bs.length; i++) bs[i].setAttribute("aria-pressed", bs[i].getAttribute("data-layout") === name ? "true" : "false");
  }
  choose("v");
  var lbs = document.querySelectorAll("[data-layout]");
  for (var i = 0; i < lbs.length; i++) lbs[i].addEventListener("click", function () { choose(this.getAttribute("data-layout")); play(); });
  if (btn) btn.addEventListener("click", function () { playing ? pause() : play(); });
  var replay = document.getElementById("line-layout-replay");
  if (replay) replay.addEventListener("click", function () { reset(0); play(); });

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? play() : pause(); }); }, { threshold: 0.3 }).observe(box);
  }
  window.__lineLayout = { choose: choose, step: step, reset: reset, passes: passes, route: route,
    state: function () { return st; }, nodes: function () { return nodes; }, DEPTH: DEPTH, REFF: REFF, NF: NF };
})();
