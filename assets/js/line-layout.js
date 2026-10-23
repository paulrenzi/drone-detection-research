// Animated top-down map of 12 darts relaying an alert back to a unit, hop by hop.
// Scale: 1 unit = 20 ft. Three layouts share the same darts and radio hop.
(function () {
  var box = document.getElementById("line-layout");
  if (!box) return;

  var NS = "http://www.w3.org/2000/svg";
  var FT = 1 / 20;                 // svg units per foot
  var HEAR = 490, HOP = 1000;      // ft: hearing range; longest radio hop allowed (~300 m)
  var R = HEAR * FT;
  var UX = 300, UY = 760;          // the unit
  var MPH = 45, FTS = MPH * 5280 / 3600;
  var SPEEDUP = 10, HOP_SECS = 0.35;
  var ACC = "#c2562c", GREEN = "#4f7a3a", BLUE = "#1f5f8b";

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
  function polar(rFt, phi) { return [UX + rFt * FT * Math.sin(phi), UY - rFt * FT * Math.cos(phi)]; }
  function fmt(s) { s = Math.max(0, Math.round(s)); return s >= 60 ? Math.floor(s / 60) + " min " + (s % 60) + " s" : s + " s"; }

  var svg = el("svg", { viewBox: "0 0 600 820", width: "100%", role: "img",
    "aria-labelledby": "llTitle llDesc", style: "font-family:inherit;color:inherit;display:block" }, box);
  var titleEl = el("title", { id: "llTitle" });
  var descEl = el("desc", { id: "llDesc" });
  var defs = el("defs", {});
  var mk = el("marker", { id: "llArr", viewBox: "0 0 10 10", refX: 5, refY: 5, markerWidth: 6, markerHeight: 6, orient: "auto-start-reverse" }, defs);
  el("path", { d: "M0,0 L10,5 L0,10 z", fill: "currentColor", "fill-opacity": 0.6 }, mk);

  // ground, enemy side, tree belts, the unit
  el("rect", { x: 0, y: 0, width: 600, height: 820, fill: "#efe9d8" });
  el("rect", { x: 0, y: 0, width: 600, height: 92, fill: ACC, "fill-opacity": 0.1 });
  text(300, 34, "ENEMY SIDE", { "text-anchor": "middle", "font-size": 22, "font-weight": 700, "letter-spacing": "0.08em", fill: ACC });
  text(300, 62, "drones launch from farther out, off the map", { "text-anchor": "middle", "font-size": 16, opacity: 0.85 });
  [330, 545].forEach(function (y) { el("rect", { x: 0, y: y, width: 600, height: 9, rx: 4, fill: GREEN, "fill-opacity": 0.5 }); });
  text(596, 323, "windbreak tree belt", { "text-anchor": "end", "font-size": 14, opacity: 0.8 });
  el("rect", { x: 0, y: UY - 15, width: 600, height: 30, fill: GREEN, "fill-opacity": 0.75 });
  el("circle", { cx: UX, cy: UY, r: R, fill: "none", stroke: BLUE, "stroke-dasharray": "3 3", "stroke-opacity": 0.8 });
  [-14, 0, 14].forEach(function (dx) { el("rect", { x: UX + dx - 5, y: UY - 4, width: 10, height: 8, rx: 2, fill: "#3b2f22" }); });
  text(UX + 30, UY + 5, "YOUR UNIT · dugouts, receiver", { "font-size": 15, "font-weight": 700, fill: "#fff" });
  text(300, UY + 40, "REAR · camp and resupply, farther back", { "text-anchor": "middle", "font-size": 15, "font-weight": 700, opacity: 0.7 });

  var gLay = el("g", {});
  var trail = el("path", { d: "", fill: "none", stroke: "#222", "stroke-opacity": 0.45, "stroke-dasharray": "2 4", "stroke-width": 1.5 });
  var pulse = el("circle", { r: 0, fill: "none", stroke: ACC, "stroke-width": 2, opacity: 0 });
  var packet = el("circle", { r: 5, fill: BLUE, opacity: 0 });
  var drone = el("g", {});
  var ds = el("g", { transform: "scale(1.5)" }, drone);
  [[-5, -5], [5, -5], [-5, 5], [5, 5]].forEach(function (p) {
    el("circle", { cx: p[0], cy: p[1], r: 3.2, fill: "none", stroke: "#111", "stroke-width": 1.2 }, ds);
  });
  el("rect", { x: -3, y: -3, width: 6, height: 6, fill: "#111" }, ds);

  // ---- the three layouts: 12 darts each, no hop longer than ~980 ft
  function trailLayout() {
    var d = [];
    for (var k = 1; k <= 12; k++) d.push(polar(980 * k, 0));
    return d;
  }
  function crossbarLayout() {
    var d = [], D = 6860;
    for (var k = 1; k <= 8; k++) d.push(polar(D * k / 8, 0));
    var c = polar(D, 0);
    [-980, -490, 490, 980].forEach(function (dx) { d.push([c[0] + dx * FT, c[1]]); });
    return d;
  }
  function arcLayout() {
    var d = [], D = 3900;
    for (var k = 1; k <= 3; k++) d.push(polar(D * k / 4, 0));
    for (var j = 0; j < 9; j++) d.push(polar(D, (j - 4) * 0.2308));
    return d;
  }
  var LAYOUTS = {
    trail: { label: "Trail", make: trailLayout, front: 11760,
      caption: "Trail: 12 darts in a chain, 980 ft apart, front dart 2.2 mi out",
      desc: "Twelve darts in a single file from the unit toward the enemy, 980 feet apart, so each can radio the one behind it. The front dart is 2.2 miles out." },
    crossbar: { label: "Trail + crossbar", make: crossbarLayout, front: 6860,
      caption: "Trail + crossbar: 8 in a chain, 4 across the head, 1.3 mi out",
      desc: "Eight darts in a chain from the unit, about 860 feet apart, to a crossbar of five darts 490 feet apart, 1.3 miles out." },
    arc: { label: "Arc", make: arcLayout, front: 3900,
      caption: "Arc: 3 in a chain, 9 in an arc 0.74 mi out, ~900 ft apart",
      desc: "Three darts in a chain from the unit to an arc of nine darts, about 900 feet apart, 0.74 miles out, spreading about 50 degrees either side." }
  };

  var lay, darts, hopTo;   // hopTo[i] = next node toward the unit (-1 = receiver)
  function build(name) {
    lay = LAYOUTS[name];
    while (gLay.firstChild) gLay.removeChild(gLay.firstChild);
    var pts = lay.make();
    // radio links: breadth-first from the receiver over hops of <= HOP ft
    var n = pts.length, hops = [], i, j;
    function dist(a, b) { return Math.hypot(a[0] - b[0], a[1] - b[1]) / FT; }
    for (i = 0; i < n; i++) hops.push(Infinity);
    hopTo = new Array(n);
    var q = [];
    for (i = 0; i < n; i++) if (dist(pts[i], [UX, UY]) <= HOP) { hops[i] = 1; hopTo[i] = -1; q.push(i); }
    while (q.length) {
      var a = q.shift();
      for (j = 0; j < n; j++) if (hops[j] === Infinity && dist(pts[a], pts[j]) <= HOP) { hops[j] = hops[a] + 1; hopTo[j] = a; q.push(j); }
    }
    darts = pts.map(function (p, k) { return { x: p[0], y: p[1], hops: hops[k] }; });
    darts.forEach(function (d, k) {
      var to = hopTo[k] === -1 ? [UX, UY] : [darts[hopTo[k]].x, darts[hopTo[k]].y];
      el("line", { x1: d.x, y1: d.y, x2: to[0], y2: to[1], stroke: BLUE, "stroke-opacity": 0.5, "stroke-dasharray": "4 3" }, gLay);
    });
    darts.forEach(function (d, k) {
      d.ring = el("circle", { cx: d.x, cy: d.y, r: R, fill: ACC, "fill-opacity": 0.08, stroke: ACC, "stroke-opacity": 0.35 }, gLay);
    });
    darts.forEach(function (d) { d.dot = el("circle", { cx: d.x, cy: d.y, r: 5, fill: "#fff", stroke: ACC, "stroke-width": 2 }, gLay); });

    // distance from the unit to the front, and labels
    var fy = UY - lay.front * FT;
    el("line", { x1: 24, y1: fy, x2: 24, y2: UY, stroke: "currentColor", "stroke-opacity": 0.6, "marker-start": "url(#llArr)", "marker-end": "url(#llArr)" }, gLay);
    var mi = (lay.front / 5280).toFixed(lay.front < 5280 ? 2 : 1);
    text(0, 0, mi + " mi from the unit to the front darts", { transform: "translate(18 " + ((fy + UY) / 2) + ") rotate(-90)", "text-anchor": "middle", "font-size": 15, "font-weight": 600 }, gLay);
    text(300, 116, lay.caption, { "text-anchor": "middle", "font-size": 16, "font-weight": 700, fill: ACC }, gLay);
    text(300, 136, "circles: what each dart hears, ~490 ft · dashes: radio hops back to the unit", { "text-anchor": "middle", "font-size": 13, opacity: 0.85 }, gLay);
    titleEl.textContent = "Twelve darts relaying back to a unit, seen from above: " + lay.label;
    descEl.textContent = "To scale. " + lay.desc + " A drone heading straight for the unit is heard by a forward dart, and the alert is passed back dart to dart. " +
      "A second drone comes in 30 degrees off to the side.";
  }

  // ---- two passes: straight in, then 30 degrees off the axis
  function approach(phiDeg) {
    var phi = phiDeg * Math.PI / 180;
    // start where the ray from the unit leaves the map (top or right edge)
    var rTop = (UY - 4) / Math.cos(phi) / FT, rSide = phi > 0 ? (596 - UX) / Math.sin(phi) / FT : Infinity;
    var r0 = Math.min(rTop, rSide);
    return { rFt: r0, pt: function (t) { return polar(r0 * (1 - t), phi); } };
  }
  var passes = [
    { name: "straight", a: approach(1.5), intro: "A drone heads straight for the unit at 45 mph." },
    { name: "side", a: approach(30), intro: "A second drone comes in 30° off to the side." }
  ];

  var panel = document.getElementById("line-layout-status");
  var btn = document.getElementById("line-layout-play");
  function say(s) { if (panel) panel.textContent = s; }

  var st, playing = false, last = 0;
  function reset(idx) {
    st = { idx: idx, t: 0, hit: -1, route: null, hopT: 0, warn: null, done: 0, d: [] };
    darts.forEach(function (d) { d.dot.setAttribute("fill", "#fff"); d.ring.setAttribute("fill-opacity", 0.08); });
    trail.setAttribute("d", ""); packet.setAttribute("opacity", 0); pulse.setAttribute("opacity", 0);
    var p0 = passes[idx].a.pt(0);
    drone.setAttribute("transform", "translate(" + p0[0] + " " + p0[1] + ")");
    say(passes[idx].intro);
  }

  function step(dt) {
    var p = passes[st.idx], a = p.a;
    if (st.done) { st.done += dt; if (st.done > 3.5) reset((st.idx + 1) % passes.length); return; }
    var dur = a.rFt / FTS / SPEEDUP;
    st.t = Math.min(1, st.t + dt / dur);
    var pos = a.pt(st.t), leftS = a.rFt * (1 - st.t) / FTS;
    drone.setAttribute("transform", "translate(" + pos[0] + " " + pos[1] + ")");
    st.d.push(pos[0].toFixed(1) + " " + pos[1].toFixed(1));
    trail.setAttribute("d", "M" + st.d.join(" L"));

    if (st.hit < 0) {
      for (var i = 0; i < darts.length; i++) {
        if (Math.hypot(pos[0] - darts[i].x, pos[1] - darts[i].y) < R) {
          st.hit = i; st.warn = leftS; st.hopT = 0;
          var route = [[darts[i].x, darts[i].y]], k = i;
          while (k !== -1) { k = hopTo[k]; route.push(k === -1 ? [UX, UY] : [darts[k].x, darts[k].y]); if (k !== -1) darts[k].dot.setAttribute("fill", "#f3c9b5"); }
          st.route = route;
          darts[i].dot.setAttribute("fill", ACC); darts[i].ring.setAttribute("fill-opacity", 0.25);
          break;
        }
      }
      if (st.hit < 0 && Math.hypot(pos[0] - UX, pos[1] - UY) < R) { st.hit = 99; st.warn = leftS; }
    }
    if (st.hit >= 0 && st.hit !== 99) {
      st.hopT += dt;
      var d = darts[st.hit], ph = (st.hopT % 0.8) / 0.8;
      pulse.setAttribute("cx", d.x); pulse.setAttribute("cy", d.y);
      pulse.setAttribute("r", 6 + 34 * ph); pulse.setAttribute("opacity", 0.9 * (1 - ph));
      var nh = st.route.length - 1, f = st.hopT / HOP_SECS;
      if (f < nh) {
        var s = Math.floor(f), u = f - s, A = st.route[s], B = st.route[s + 1];
        packet.setAttribute("opacity", 1);
        packet.setAttribute("cx", A[0] + (B[0] - A[0]) * u); packet.setAttribute("cy", A[1] + (B[1] - A[1]) * u);
        say("Dart " + (st.hit + 1) + " heard it. Passing the alert back, dart to dart: hop " + (s + 1) + " of " + nh + "…");
      } else {
        packet.setAttribute("opacity", 0);
        say("ALERT at the unit · drone arrives in about " + fmt(leftS) + ". Take cover.");
      }
    } else if (st.hit === 99) {
      say("No dart heard it. Only the unit's own ears catch it, about " + fmt(st.warn) + " out.");
    } else if (a.rFt * (1 - st.t) < lay.front) {
      say("Not heard yet: it is passing outside every dart's 490 ft.");
    }
    if (st.t >= 1) {
      st.done = 0.0001;
      say("Warning: " + (st.warn != null ? "about " + fmt(st.warn) : "none") + (st.hit >= 0 && st.hit !== 99 ? " from the darts" : "") +
        ". A sentry hearing it ~490 ft out gets about 7 s.");
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
  choose("trail");
  var lbs = document.querySelectorAll("[data-layout]");
  for (var i = 0; i < lbs.length; i++) lbs[i].addEventListener("click", function () { choose(this.getAttribute("data-layout")); play(); });
  if (btn) btn.addEventListener("click", function () { playing ? pause() : play(); });
  var replay = document.getElementById("line-layout-replay");
  if (replay) replay.addEventListener("click", function () { reset(0); play(); });

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? play() : pause(); }); }, { threshold: 0.3 }).observe(box);
  }
  window.__lineLayout = { choose: choose, step: step, reset: reset, passes: passes,
    state: function () { return st; }, darts: function () { return darts; }, R: R };
})();
