// Animated top-down map of one tripwire line. Scale: 1 unit = 12 ft.
(function () {
  var box = document.getElementById("line-layout");
  if (!box) return;

  var NS = "http://www.w3.org/2000/svg";
  var FT = 1 / 12;                 // svg units per foot
  var R = 490 * FT;                // hearing range, and the spacing
  var LINE_Y = 150, UNIT_X = 300, UNIT_Y = 678;   // 1.2 mi apart
  var MPH = 45, FTS = MPH * 5280 / 3600;          // 66 ft/s
  var SPEEDUP = 10;
  var ACC = "#c2562c", GREEN = "#4f7a3a", BLUE = "#1f5f8b";

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(e);
    return e;
  }
  function text(x, y, s, attrs, parent) {
    var a = { x: x, y: y, "font-size": 12, fill: "currentColor" };
    for (var k in attrs) a[k] = attrs[k];
    var t = el("text", a, parent);
    t.textContent = s;
    return t;
  }

  var svg = el("svg", { viewBox: "0 0 600 780", width: "100%", role: "img",
    "aria-labelledby": "llTitle llDesc", style: "font-family:inherit;color:inherit;display:block" }, box);
  el("title", { id: "llTitle" }).textContent = "One tripwire line, seen from above";
  el("desc", { id: "llDesc" }).textContent =
    "To scale. Twelve darts stand in a row 1.2 miles in front of the unit's tree line, 490 feet apart, each hearing about 490 feet. " +
    "A drone flying toward the unit crosses the line between two darts; the nearer dart hears it and radios the receiver at the unit, " +
    "giving about a minute and a half of warning at 45 mph. A second drone flies round the end of the line, is missed, " +
    "and is heard only by the unit itself, about 7 seconds out.";

  // ground
  el("rect", { x: 0, y: 0, width: 600, height: 780, fill: "#efe9d8" });
  el("rect", { x: 0, y: 0, width: 600, height: 100, fill: ACC, "fill-opacity": 0.1 });
  text(300, 36, "ENEMY SIDE", { "text-anchor": "middle", "font-size": 22, "font-weight": 700, "letter-spacing": "0.08em", fill: ACC });
  text(300, 66, "drones launch from farther out, off the map", { "text-anchor": "middle", "font-size": 16, opacity: 0.85 });

  // windbreak tree belts (illustrative)
  [[0, 335, 600], [0, 490, 600]].forEach(function (b) {
    el("rect", { x: b[0], y: b[1], width: b[2], height: 9, rx: 4, fill: GREEN, "fill-opacity": 0.55 });
  });
  text(596, 328, "windbreak tree belt", { "text-anchor": "end", "font-size": 14, opacity: 0.8 });

  // the unit's own tree line, unit, receiver
  el("rect", { x: 0, y: UNIT_Y - 15, width: 600, height: 30, fill: GREEN, "fill-opacity": 0.75 });
  el("circle", { cx: UNIT_X, cy: UNIT_Y, r: R, fill: "none", stroke: BLUE, "stroke-dasharray": "3 3", "stroke-opacity": 0.8 });
  [-14, 0, 14].forEach(function (dx) {
    el("rect", { x: UNIT_X + dx - 5, y: UNIT_Y - 4, width: 10, height: 8, rx: 2, fill: "#3b2f22" });
  });
  var RX = UNIT_X - 62, RY = UNIT_Y - 14;
  el("line", { x1: RX, y1: RY, x2: RX, y2: RY - 14, stroke: BLUE, "stroke-width": 2 });
  var rxDot = el("circle", { cx: RX, cy: RY - 15, r: 4, fill: BLUE });
  text(RX + 4, RY - 26, "receiver + tablet", { "text-anchor": "end", "font-size": 15, fill: BLUE, "font-weight": 600 });
  text(UNIT_X + 30, UNIT_Y + 5, "YOUR UNIT · dugouts", { "font-size": 15, "font-weight": 700, fill: "#fff" });
  text(300, UNIT_Y + 42, "dashed circle: what the unit hears itself, ~490 ft, about 7 s", { "text-anchor": "middle", "font-size": 14, fill: BLUE });
  text(300, 760, "REAR · camp and resupply, farther back", { "text-anchor": "middle", "font-size": 15, "font-weight": 700, opacity: 0.7, "letter-spacing": "0.05em" });

  // distance from line to unit
  el("line", { x1: 24, y1: LINE_Y, x2: 24, y2: UNIT_Y, stroke: "currentColor", "stroke-opacity": 0.6, "marker-start": "url(#llArr)", "marker-end": "url(#llArr)" });
  var defs = el("defs", {});
  var mk = el("marker", { id: "llArr", viewBox: "0 0 10 10", refX: 5, refY: 5, markerWidth: 6, markerHeight: 6, orient: "auto-start-reverse" }, defs);
  el("path", { d: "M0,0 L10,5 L0,10 z", fill: "currentColor", "fill-opacity": 0.6 }, mk);
  text(0, 0, "1.2 mi from the line to the unit", { transform: "translate(18 " + ((LINE_Y + UNIT_Y) / 2) + ") rotate(-90)", "text-anchor": "middle", "font-size": 16, "font-weight": 600 });

  // the darts
  var darts = [];
  for (var i = 0; i < 12; i++) {
    var x = UNIT_X + (i - 5.5) * R;
    var ring = el("circle", { cx: x, cy: LINE_Y, r: R, fill: ACC, "fill-opacity": 0.07, stroke: ACC, "stroke-opacity": 0.35 });
    var dot = el("circle", { cx: x, cy: LINE_Y, r: 5, fill: "#fff", stroke: ACC, "stroke-width": 2 });
    text(x, LINE_Y - 10, String(i + 1), { "text-anchor": "middle", "font-size": 14, "font-weight": 700, fill: ACC });
    darts.push({ x: x, ring: ring, dot: dot });
  }
  var x0 = darts[0].x, x1 = darts[1].x;
  el("line", { x1: x0, y1: LINE_Y + R + 10, x2: x1, y2: LINE_Y + R + 10, stroke: "currentColor", "stroke-opacity": 0.7, "marker-start": "url(#llArr)", "marker-end": "url(#llArr)" });
  text(x1 + 8, LINE_Y + R + 15, "490 ft apart = one hearing range", { "font-size": 16, "font-weight": 600 });
  text(300, LINE_Y + R + 50, "12 darts cover about 1.1 mi of front", { "text-anchor": "middle", "font-size": 20, "font-weight": 700, fill: ACC });
  text(300, LINE_Y + R + 74, "circle = what one dart hears: ~490 ft, not yet measured", { "text-anchor": "middle", "font-size": 15, opacity: 0.85 });

  // moving parts
  var trail = el("path", { d: "", fill: "none", stroke: "#222", "stroke-opacity": 0.45, "stroke-dasharray": "2 4", "stroke-width": 1.5 });
  var packet = el("circle", { r: 4, fill: BLUE, opacity: 0 });
  var link = el("line", { stroke: BLUE, "stroke-width": 1.5, "stroke-dasharray": "5 4", opacity: 0 });
  var pulse = el("circle", { r: 0, fill: "none", stroke: ACC, "stroke-width": 2, opacity: 0 });
  var drone = el("g", {});
  var droneShape = el("g", { transform: "scale(1.5)" }, drone);
  [[-5, -5], [5, -5], [-5, 5], [5, 5]].forEach(function (p) {
    el("circle", { cx: p[0], cy: p[1], r: 3.2, fill: "none", stroke: "#111", "stroke-width": 1.2 }, droneShape);
  });
  el("rect", { x: -3, y: -3, width: 6, height: 6, fill: "#111" }, droneShape);

  // the status panel under the map
  var panel = document.getElementById("line-layout-status");
  var btn = document.getElementById("line-layout-play");

  // two passes: one crosses between darts 7 and 8, one goes round the end
  function lerp(a, b, t) { return a + (b - a) * t; }
  var passes = [
    { name: "a", pt: function (t) { return [lerp(353, UNIT_X, t), lerp(-10, UNIT_Y - 2, t)]; } },
    { name: "b", pt: function (t) {
        var u = 1 - t;
        return [u * u * 592 + 2 * u * t * 612 + t * t * UNIT_X, u * u * -10 + 2 * u * t * 440 + t * t * (UNIT_Y - 2)];
      } }
  ];
  passes.forEach(function (p) {          // path length in svg units, by sampling
    var L = 0, prev = p.pt(0);
    for (var k = 1; k <= 400; k++) { var q = p.pt(k / 400); L += Math.hypot(q[0] - prev[0], q[1] - prev[1]); prev = q; }
    p.len = L;
    p.dur = (L / FT) / FTS / SPEEDUP;    // real seconds
  });

  var state, raf = null, last = 0, playing = false;
  function reset(idx) {
    state = { idx: idx, t: 0, hit: -1, hitAt: 0, unitHeard: false, done: 0, d: [] };
    darts.forEach(function (d) { d.dot.setAttribute("fill", "#fff"); d.ring.setAttribute("fill-opacity", 0.07); });
    trail.setAttribute("d", "");
    packet.setAttribute("opacity", 0); link.setAttribute("opacity", 0); pulse.setAttribute("opacity", 0);
    rxDot.setAttribute("r", 4);
    say(idx === 0
      ? "A drone heads for the unit at 45 mph. Watch the line."
      : "A second drone flies round the end of the line.");
  }
  function say(s) { if (panel) panel.textContent = s; }
  function fmt(s) { s = Math.max(0, Math.round(s)); return s >= 60 ? Math.floor(s / 60) + " min " + (s % 60) + " s" : s + " s"; }

  function step(dt) {
    var p = passes[state.idx];
    if (state.done) {
      state.done += dt;
      if (state.done > 3.2) reset((state.idx + 1) % passes.length);
      return;
    }
    state.t = Math.min(1, state.t + dt / p.dur);
    var pos = p.pt(state.t);
    drone.setAttribute("transform", "translate(" + pos[0] + " " + pos[1] + ")");
    state.d.push(pos[0].toFixed(1) + " " + pos[1].toFixed(1));
    trail.setAttribute("d", "M" + state.d.join(" L"));
    var leftFt = (1 - state.t) * p.len / FT;

    if (state.hit < 0) {
      for (var i = 0; i < darts.length; i++) {
        if (Math.hypot(pos[0] - darts[i].x, pos[1] - LINE_Y) < R) {
          state.hit = i; state.hitAt = 0; state.warn = leftFt / FTS;
          darts[i].dot.setAttribute("fill", ACC); darts[i].ring.setAttribute("fill-opacity", 0.22);
          link.setAttribute("x1", darts[i].x); link.setAttribute("y1", LINE_Y);
          link.setAttribute("x2", RX); link.setAttribute("y2", RY - 15);
          break;
        }
      }
    }
    if (state.hit >= 0) {
      state.hitAt += dt;
      var d = darts[state.hit], a = Math.min(1, state.hitAt / 1.2);
      pulse.setAttribute("cx", d.x); pulse.setAttribute("cy", LINE_Y);
      pulse.setAttribute("r", 6 + 40 * ((state.hitAt % 0.8) / 0.8)); pulse.setAttribute("opacity", 0.9 * (1 - (state.hitAt % 0.8) / 0.8));
      link.setAttribute("opacity", 0.7);
      packet.setAttribute("opacity", a < 1 ? 1 : 0);
      packet.setAttribute("cx", lerp(d.x, RX, a)); packet.setAttribute("cy", lerp(LINE_Y, RY - 15, a));
      if (a >= 1) {
        rxDot.setAttribute("r", 4 + 2 * Math.abs(Math.sin(state.hitAt * 6)));
        say("ALERT · dart " + (state.hit + 1) + " heard a drone. It arrives in about " + fmt(leftFt / FTS) + ". Take cover.");
      } else {
        say("Dart " + (state.hit + 1) + " hears it and radios the unit…");
      }
    } else if (p.name === "b" && Math.hypot(pos[0] - UNIT_X, pos[1] - UNIT_Y) < R) {
      if (!state.unitHeard) { state.unitHeard = true; state.warn = leftFt / FTS; }
      say("Missed by the line. Only the unit's own ears catch it: " + fmt(state.warn) + " of warning.");
    } else if (p.name === "b" && pos[1] > LINE_Y + R) {
      say("Missed: it flew round the end of the line, outside every dart's range.");
    }
    if (state.t >= 1) {
      state.done = 0.0001;
      say(p.name === "a"
        ? "Warning from the line: about " + fmt(state.warn) + ". A sentry hearing it ~490 ft out gets about 7 s."
        : "Warning: about " + fmt(state.warn) + ". A line only protects the front it covers.");
    }
  }

  function frame(ts) {
    var dt = last ? Math.min(0.1, (ts - last) / 1000) : 0;
    last = ts;
    step(dt);
    raf = playing ? requestAnimationFrame(frame) : null;
  }
  function play() { if (playing) return; playing = true; last = 0; raf = requestAnimationFrame(frame); if (btn) btn.textContent = "Pause"; }
  function pause() { playing = false; if (btn) btn.textContent = "Play"; }

  reset(0);
  var p0 = passes[0].pt(0);
  drone.setAttribute("transform", "translate(" + p0[0] + " " + p0[1] + ")");
  if (btn) btn.addEventListener("click", function () { playing ? pause() : play(); });
  var replay = document.getElementById("line-layout-replay");
  if (replay) replay.addEventListener("click", function () { reset(0); play(); });

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.isIntersecting ? play() : pause(); });
    }, { threshold: 0.3 }).observe(box);
  }
  window.__lineLayout = { passes: passes, darts: darts, R: R, LINE_Y: LINE_Y, step: step, reset: reset, state: function () { return state; } };
})();
