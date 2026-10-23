// One lay, start to finish: replays a lay simulated by tools/laymodel/lay_model.py on its example sector.
// The map, the plan, every drop, every relay heard and every battery reading come from the model's output
// (assets/data/lay-demo.json); this script only draws them. Distances are in feet, to scale except the belts.
(function () {
  var box = document.getElementById("lay-model");
  if (!box) return;
  var src = box.getAttribute("data-src");
  var NS = "http://www.w3.org/2000/svg";
  var FT = 0.058, UX = 300, UY = 548;
  var ACC = "#c2562c", GREEN = "#4f7a3a", BLUE = "#1f5f8b", GREY = "#8a8a8a", RED = "#b3261e", BROWN = "#8a6a3b";
  var svg, D, scenes = [], total = 0, panel, btn;

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(e);
    return e;
  }
  function text(x, y, s, attrs, parent) {
    var a = { x: x, y: y, "font-size": 14, fill: "currentColor" };
    for (var k in attrs) a[k] = attrs[k];
    var t = el("text", a, parent); t.textContent = s; return t;
  }
  function sx(p) { return [UX + p[0] * FT, UY - p[1] * FT]; }
  function path(pts) { return pts.map(function (p, i) { var s = sx(p); return (i ? "L" : "M") + s[0].toFixed(1) + " " + s[1].toFixed(1); }).join(" "); }
  function lerp(a, b, u) { return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]; }
  function clamp(u) { return u < 0 ? 0 : u > 1 ? 1 : u; }
  function say(s) { if (panel && panel.textContent !== s) panel.textContent = s; }
  function hhmm(min) { var m = Math.round(5 * 60 + 10 + min); return ("0" + Math.floor(m / 60) % 24).slice(-2) + ":" + ("0" + m % 60).slice(-2); }
  function show(e, on) { e.setAttribute("opacity", on ? 1 : 0); }

  function build() {
    var S = D.sector;
    svg = el("svg", { viewBox: "0 0 600 640", width: "100%", role: "img", "aria-labelledby": "lyTitle lyDesc",
      style: "font-family:inherit;color:inherit;display:block" }, box);
    el("title", { id: "lyTitle" }).textContent = "One lay of the net, start to finish, from the lay model";
    el("desc", { id: "lyDesc" }).textContent = "A top-down map of an example sector with two windbreaks, a ravine and an enemy salient. " +
      "The first 20-dart plan fails on this ground; the planner moves darts off bad ground and adds darts where hops cross trees, " +
      "for 25 planned darts. Eight sorties lay them with GPS jammed. Each new dart is confirmed by a relay the drone hears; " +
      "darts out of reach get a spare 300 feet back, and tilted or silent darts are re-dropped. The lay uses 30 darts in about an hour and a half.";
    el("rect", { x: 0, y: 0, width: 600, height: 640, fill: "#efe9d8" });

    // the enemy side: everything beyond the edge line
    var edge = S.enemy_edge;
    el("path", { d: path(edge) + " L" + sx(edge[edge.length - 1])[0] + " 0 L" + sx(edge[0])[0] + " 0 Z", fill: ACC, "fill-opacity": 0.12 });
    el("path", { d: path(edge), fill: "none", stroke: RED, "stroke-width": 2, "stroke-dasharray": "7 4" });
    el("path", { d: path(edge.map(function (p) { return [p[0], p[1] - D.standoff]; })), fill: "none", stroke: RED, "stroke-opacity": 0.35, "stroke-dasharray": "2 4" });
    text(300, 24, "ENEMY SIDE", { "text-anchor": "middle", "font-size": 20, "font-weight": 700, "letter-spacing": "0.08em", fill: ACC });
    var e1 = sx(edge[2]); text(e1[0] + 8, e1[1] - 6, "enemy edge, a salient", { "font-size": 12, fill: RED, "font-weight": 700 });

    // ground: ravine, belts, own tree line
    var g = el("g", {}); D.ground = g;
    S.ravines.forEach(function (r) {
      el("path", { d: path(r.line), fill: "none", stroke: BROWN, "stroke-width": r.width * FT, "stroke-opacity": 0.28, "stroke-linecap": "round" }, g);
      var m = sx(r.line[0]); text(m[0] - 14, m[1] + 26, "ravine, 50 ft deep", { "font-size": 12, fill: BROWN, "font-weight": 700 }, g);
    });
    S.tree_belts.forEach(function (b, i) {
      el("path", { d: path(b.line), fill: "none", stroke: GREEN, "stroke-width": 5, "stroke-opacity": 0.75 }, g);
    });
    var b0 = sx([3700, 2740]); text(b0[0], b0[1] + 18, "windbreak", { "font-size": 12, fill: GREEN, "font-weight": 700 }, g);
    var b1 = sx([2990, 6400]); text(b1[0] + 6, b1[1], "windbreak", { "font-size": 12, fill: GREEN, "font-weight": 700 }, g);
    el("rect", { x: 0, y: UY - 10, width: 600, height: 20, fill: GREEN, "fill-opacity": 0.7 });
    S.positions.forEach(function (p, i) {
      var s = sx(p);
      el("rect", { x: s[0] - 6, y: s[1] - 5, width: 12, height: 10, rx: 2, fill: "#3b2f22" });
      text(s[0] + (i === 2 ? 10 : i === 0 ? -10 : 0), s[1] + (i === 1 ? -14 : 4), "P" + (i + 1), { "text-anchor": i === 2 ? "start" : i === 0 ? "end" : "middle", "font-size": 13, "font-weight": 700, fill: i === 1 ? "currentColor" : "#fff" });
    });
    var ls = sx(D.launch);
    el("path", { d: "M" + (ls[0] - 7) + " " + (ls[1] + 6) + " l7 -12 l7 12 z", fill: "#3b2f22" });
    text(ls[0] + 12, ls[1] + 5, "launch", { "font-size": 12, "font-weight": 700 });
    [[-1, S.positions[0]], [1, S.positions[2]]].forEach(function (e) {
      var a = sx(e[1]), len = 330;
      el("line", { x1: a[0], y1: a[1], x2: a[0] + e[0] * len, y2: a[1] - len, stroke: ACC, "stroke-opacity": 0.4, "stroke-dasharray": "6 5" });
    });
    // wind
    var wg = el("g", { transform: "translate(548 520)" });
    el("line", { x1: 0, y1: 18, x2: 0, y2: -18, stroke: "currentColor", "stroke-width": 2.5 }, wg);
    el("path", { d: "M-6 -10 L0 -20 L6 -10", fill: "none", stroke: "currentColor", "stroke-width": 2.5 }, wg);
    text(0, 36, "wind 9 mph", { "text-anchor": "middle", "font-size": 12, "font-weight": 700 }, wg);
    el("line", { x1: 20, y1: 625, x2: 20 + 2000 * FT, y2: 625, stroke: "currentColor", "stroke-width": 3 });
    text(20, 616, "2,000 ft", { "font-size": 12, opacity: 0.85 });

    // layers
    D.gOld = el("g", { opacity: 0 }); D.gPlan = el("g", { opacity: 0 }); D.gHear = el("g", { opacity: 0 });
    D.gLinks = el("g", {}); D.gDarts = el("g", {}); D.gFx = el("g", {});
    D.old_front.concat(D.old_trunks[0], D.old_trunks[1]).forEach(function (p) {
      var s = sx(p); el("circle", { cx: s[0], cy: s[1], r: 4.5, fill: "none", stroke: GREY, "stroke-width": 1.5 }, D.gOld);
    });
    D.old_bad_links.forEach(function (l) {
      var a = sx(l[0]), b = sx(l[1]);
      el("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: RED, "stroke-width": 2, "stroke-dasharray": "4 3" }, D.gOld);
    });
    D.old_why.forEach(function (w) {
      var s = sx(w);
      el("circle", { cx: s[0], cy: s[1], r: 9, fill: "none", stroke: RED, "stroke-width": 2.2 }, D.gOld);
      text(s[0] + (s[0] < 300 ? -12 : 12), s[1] - 10, "in a " + (w[2] === "ravine" ? "ravine" : "tree belt"), { "font-size": 12, "font-weight": 700, fill: RED, "text-anchor": s[0] < 300 ? "end" : "start" }, D.gOld);
    });
    D.planDots = D.plan.map(function (q) {
      var s = sx(q.p);
      return el("circle", { cx: s[0], cy: s[1], r: 6, fill: "none", stroke: q.id[0] === "F" ? ACC : BLUE, "stroke-dasharray": "2 2", "stroke-width": 1.4, opacity: 0 }, D.gPlan);
    });
    var pl = sx([-1684, 5246]);
    D.pullLbl = text(pl[0] + 4, pl[1] + 22, "pulled back 650 ft from the edge", { "font-size": 12, "font-weight": 700, fill: RED, "text-anchor": "middle", opacity: 0 }, D.gPlan);

    // the drone, its labels, the panel
    D.drone = el("g", { opacity: 0 }, D.gFx);
    var ds = el("g", { transform: "scale(1.4)" }, D.drone);
    [[-5, -5], [5, -5], [-5, 5], [5, 5]].forEach(function (p) { el("circle", { cx: p[0], cy: p[1], r: 3.2, fill: "none", stroke: "#111", "stroke-width": 1.2 }, ds); });
    el("rect", { x: -3, y: -3, width: 6, height: 6, fill: "#111" }, ds);
    D.ring = el("circle", { r: 0, fill: "none", stroke: BLUE, "stroke-width": 2, opacity: 0 }, D.gFx);
    D.lbl = text(0, 0, "", { "font-size": 13, "font-weight": 700 }, D.gFx);
    D.lblBg = null;
    D.clock = text(300, 48, "", { "text-anchor": "middle", "font-size": 15, "font-weight": 700, opacity: 0.85 });
    D.tally = text(300, 70, "", { "text-anchor": "middle", "font-size": 14, "font-weight": 700 });
    D.batBox = el("g", { transform: "translate(380 600)", opacity: 0 });
    el("rect", { x: 0, y: 0, width: 120, height: 14, rx: 3, fill: "none", stroke: "currentColor", "stroke-width": 1.5 }, D.batBox);
    D.bat = el("rect", { x: 2, y: 2, width: 116, height: 10, rx: 2, fill: GREEN }, D.batBox);
    el("line", { x1: 2 + 116 * 0.2, y1: -2, x2: 2 + 116 * 0.2, y2: 16, stroke: RED, "stroke-width": 1.5 }, D.batBox);
    D.batTxt = text(126, 12, "", { "font-size": 12, "font-weight": 700 }, D.batBox);
    D.sortTxt = text(370, 612, "", { "font-size": 12, "font-weight": 700, "text-anchor": "end" });
  }

  // ---- darts drawn during the lay
  var placed = {};
  function dart(ev) {
    if (placed[ev.id]) return placed[ev.id];
    var s = sx(ev.at), d = { s: s, ev: ev };
    d.dot = el("circle", { cx: s[0], cy: s[1], r: 5.5, "stroke-width": 2, fill: "#fff", stroke: ev.planned[0] === "F" ? ACC : BLUE }, D.gDarts);
    d.xm = el("path", { d: "M" + (s[0] - 5) + " " + (s[1] - 5) + " l10 10 m0 -10 l-10 10", stroke: "#111", "stroke-width": 2, opacity: 0 }, D.gDarts);
    placed[ev.id] = d; return d;
  }
  function pos(id) { return id === "RX" ? D.sector.receiver : D.final[id].p; }
  function setLabel(s, str, color, anchor) {
    D.lbl.setAttribute("x", s[0] + (anchor === "end" ? -12 : 12)); D.lbl.setAttribute("y", s[1] - 10);
    D.lbl.setAttribute("text-anchor", anchor || "start"); D.lbl.setAttribute("fill", color); D.lbl.textContent = str;
  }

  // ---- scenes: [seconds, render(u, t)]
  function sceneList() {
    var out = [];
    out.push([5, function (u) {
      D.clock.textContent = "Day 0, planning"; D.tally.textContent = "";
      say("The planning tool's inputs: the unit's positions, the enemy's forward edge, a map with windbreaks, a ravine and a slope rising 50 ft toward the front, and the wind forecast.");
    }]);
    out.push([7, function (u) {
      D.gOld.setAttribute("opacity", clamp(u * 3));
      D.tally.textContent = "First plan, laid on this ground: 6 of 20 darts reach the unit";
      say("The page's first plan ignores the ground. One dart falls in the ravine, one in a windbreak, and trunk hops that cross the windbreak are out of reach. Only 6 of 20 darts would get an alert home.");
    }]);
    out.push([7, function (u) {
      D.gOld.setAttribute("opacity", clamp(1 - u * 3));
      D.gPlan.setAttribute("opacity", 1);
      var n = Math.floor(u * 1.4 * D.planDots.length);
      D.planDots.forEach(function (c, i) { c.setAttribute("opacity", i < n ? 0.95 : 0); });
      D.pullLbl.setAttribute("opacity", u > 0.6 ? 1 : 0);
      D.tally.textContent = "This plan: 25 darts, 7 sorties in the forecast wind";
      say("The planner keeps darts off trees, the ravine floor and within 650 ft of the enemy edge, shortens every hop that crosses a windbreak, and runs the front row 300 ft past both 45° lines: 13 front darts and 6 relays a trunk.");
    }]);
    D.sorties.forEach(function (so, k) {
      var tr = so.track, segs = [], tt = 0, travel = 0, i;
      for (i = 1; i < tr.length; i++) if (tr[i].p[0] !== tr[i - 1].p[0] || tr[i].p[1] !== tr[i - 1].p[1]) travel += tr[i].t - tr[i - 1].t;
      for (i = 1; i < tr.length; i++) {
        var moving = tr[i].p[0] !== tr[i - 1].p[0] || tr[i].p[1] !== tr[i - 1].p[1];
        var dur = moving ? 3.2 * (tr[i].t - tr[i - 1].t) / travel : (tr[i].ev && tr[i].ev.id ? 1.6 : 0.15);
        segs.push({ a: tt, b: tt + dur, from: tr[i - 1], to: tr[i] }); tt += dur;
      }
      var dur = tt + 0.6;
      out.push([dur, function (u, t) {
        var lt = u * dur, cur = segs[segs.length - 1], v = 1;
        for (var j = 0; j < segs.length; j++) if (lt < segs[j].b) { cur = segs[j]; v = (lt - cur.a) / (cur.b - cur.a || 1); break; }
        // darts released before this moment
        segs.forEach(function (sg) {
          var ev = sg.to.ev;
          if (!ev || !ev.id || lt < sg.a) return;
          var d = dart(ev), done = lt >= sg.a + 0.8;
          var bad = ev.state !== "upright" || !ev.confirmed;
          d.dot.setAttribute("stroke", done && bad ? GREY : (ev.planned[0] === "F" ? ACC : BLUE));
          d.dot.setAttribute("fill", done && bad ? "#ddd" : "#fff");
          d.xm.setAttribute("opacity", done && ev.state !== "upright" ? 1 : 0);
          if (done && ev.confirmed && !d.link) {
            var a = sx(pos(ev.anchor));
            d.link = el("line", { x1: d.s[0], y1: d.s[1], x2: a[0], y2: a[1], stroke: BLUE, "stroke-opacity": 0.6, "stroke-dasharray": "4 3" }, D.gLinks);
          }
        });
        var p = lerp(cur.from.p, cur.to.p, v), s = sx(p), bat = cur.from.bat + (cur.to.bat - cur.from.bat) * v;
        D.drone.setAttribute("transform", "translate(" + s[0] + " " + s[1] + ")"); show(D.drone, u < 0.98);
        D.batBox.setAttribute("opacity", 1); D.pullLbl.setAttribute("opacity", 0);
        D.bat.setAttribute("width", Math.max(0, 116 * bat)); D.bat.setAttribute("fill", bat < 0.3 ? RED : GREEN);
        D.batTxt.textContent = Math.round(100 * bat) + "%";
        var realMin = so.start_min + (cur.from.t + (cur.to.t - cur.from.t) * v) / 60;
        D.clock.textContent = "Lay day, " + hhmm(realMin) + " · GPS jammed";
        D.sortTxt.textContent = "Sortie " + (k + 1) + " of " + D.sorties.length + " · battery";
        var used = 0; Object.keys(placed).forEach(function () { used++; });
        D.tally.textContent = used + " darts dropped";
        var ev = cur.to.ev && cur.to.ev.id && lt >= cur.a ? cur.to.ev : null;
        D.ring.setAttribute("opacity", 0); D.lbl.textContent = "";
        if (ev) {
          var w = (lt - cur.a) / (cur.b - cur.a), ds_ = sx(ev.at), anc = ev.anchor === "RX" ? "the receiver" : ev.anchor;
          var left = ds_[0] > 430;
          if (ev.state === "upright" && w > 0.25) {
            D.ring.setAttribute("cx", ds_[0]); D.ring.setAttribute("cy", ds_[1]); D.ring.setAttribute("r", 6 + 26 * ((w * 2) % 1)); D.ring.setAttribute("opacity", 0.8 * (1 - (w * 2) % 1));
          }
          if (w > 0.45) {
            if (ev.state === "tilted") setLabel(ds_, "lands tilted: re-drop", RED, left ? "end" : "start");
            else if (ev.state === "dud") setLabel(ds_, "silent: re-drop", RED, left ? "end" : "start");
            else if (ev.state === "in a tree") setLabel(ds_, "in a tree: re-drop", RED, left ? "end" : "start");
            else if (ev.confirmed) setLabel(ds_, ev.second ? "✓ relayed from both sides" : "✓ relayed by " + anc, GREEN, left ? "end" : "start");
            else if (ev.second && ev.joined) setLabel(ds_, "relayed by " + anc + " only: spare toward " + ev.second, RED, left ? "end" : "start");
            else setLabel(ds_, "no relay: spare 300 ft back", RED, left ? "end" : "start");
          }
        }
        var lastDrop = ev && so.drops[so.drops.length - 1] === ev;
        var later = lastDrop ? " This sortie is out of darts, so that happens first thing on the next one." : "";
        if (ev && ev.state === "upright" && !ev.confirmed && ev.second && ev.joined)
          say("The closing dart has to be relayed from both sides. " + anc + " relays it, " + ev.second + " doesn't: the next dart goes 300 ft from it toward " + ev.second + "." + later);
        else if (ev && ev.state === "upright" && !ev.confirmed)
          say("The drone hears this dart's own 'landed' message but no relay from " + anc + ": out of reach. The next dart goes 300 ft back toward " + anc + "." + later);
        else if (ev && ev.state === "tilted") say("This dart lands tilted, and its tilt sensor says so in its 'landed' message. The next dart goes on the same spot." + later);
        else if (ev && ev.state === "dud") say("Nothing at all is heard from this dart: a dud. The next dart goes on the same spot." + later);
        else if (k === 0) say("Sortie 1, GPS jammed: the drone flies on compass and optical flow 35 ft up, climbing over the windbreak. Each dart sends 'landed', and the drone waits for the relay from the dart before it.");
        else if (so.drops.length && so.drops[0].id.indexOf("+") > 0 && !(ev && ev !== so.drops[0]))
          say("Between sorties the crew swaps the pack and reloads 4 darts. The first dart finishes the point the last sortie ran out of darts for.");
        else if (k === 2) say("With 6 packs and a 2-channel charger, the drone never waits for a charge. Every link in the net is proved by a relay as it is made.");
        else if (k === D.sorties.length - 1) say("The last sortie closes the front row: the closing dart has to be relayed from both sides.");
        else say("Sortie " + (k + 1) + ": the battery check runs before every drop, with a 5 mph gust margin on the way home.");
      }]);
    });
    out.push([8, function (u) {
      show(D.drone, false); D.lbl.textContent = ""; D.ring.setAttribute("opacity", 0);
      D.gPlan.setAttribute("opacity", 0.35); D.pullLbl.setAttribute("opacity", 0);
      D.batBox.setAttribute("opacity", 0); D.sortTxt.textContent = "";
      if (!D.finalLinks) {
        D.finalLinks = el("g", {}, D.gLinks);
        D.links.forEach(function (l) { var a = sx(pos(l[0])), b = sx(pos(l[1])); el("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: BLUE, "stroke-opacity": 0.45 }, D.finalLinks); });
        Object.keys(D.final).forEach(function (n) {
          var f = D.final[n]; if (n === "RX" || !f.live) return;
          var s = sx(f.p); el("circle", { cx: s[0], cy: s[1], r: D.reff * FT, fill: ACC, "fill-opacity": 0.05, stroke: ACC, "stroke-opacity": 0.25 }, D.gHear);
        });
      }
      D.gHear.setAttribute("opacity", clamp(u * 3));
      Object.keys(placed).forEach(function (n) {   // a dart that never confirmed may still be in the net through its spare
        var d = placed[n]; if (!D.final[n] || !D.final[n].live) return;
        d.dot.setAttribute("stroke", d.ev.planned[0] === "F" ? ACC : BLUE); d.dot.setAttribute("fill", "#fff");
      });
      var sc = D.score;
      D.clock.textContent = "Lay day, " + hhmm(D.sorties[D.sorties.length - 1].end_min) + " · net whole";
      D.tally.textContent = sc.darts + " darts, " + sc.sorties + " sorties, " + (Math.round(sc.hours * 10) / 10) + " h · worst warning " + Math.round(sc.warn) + " s";
      say("Whole: every drone track within 45° of each position is heard at least " + Math.round(sc.warn) + " s out, and losing any one dart cuts off at most one other. 25 planned darts took " + sc.darts + ".");
    }]);
    out.push([3, function () {}]);
    return out;
  }

  function reset() {
    Object.keys(placed).forEach(function (k) { var d = placed[k]; d.dot.remove(); d.xm.remove(); if (d.link) d.link.remove(); });
    placed = {};
    if (D.finalLinks) { D.finalLinks.remove(); D.finalLinks = null; }
    while (D.gHear.firstChild) D.gHear.removeChild(D.gHear.firstChild);
    D.gHear.setAttribute("opacity", 0); D.gPlan.setAttribute("opacity", 0); D.gOld.setAttribute("opacity", 0);
    D.batBox.setAttribute("opacity", 0); D.sortTxt.textContent = ""; show(D.drone, false); D.lbl.textContent = "";
  }

  var at = 0, playing = false, last = 0;
  function seek(t) {
    if (t < at) reset();
    at = t;
    var acc = 0;
    for (var i = 0; i < scenes.length; i++) {
      var d = scenes[i][0];
      if (t < acc + d || i === scenes.length - 1) {
        // replay earlier scenes' end states once, so seeking forward lands in a consistent picture
        for (var j = 0; j < i; j++) scenes[j][1](1, 0);
        scenes[i][1](clamp((t - acc) / d), t);
        return;
      }
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
    panel = document.getElementById("lay-status"); btn = document.getElementById("lay-play");
    seek(0);
    if (btn) btn.addEventListener("click", function () { playing ? pause() : play(); });
    var rp = document.getElementById("lay-replay");
    if (rp) rp.addEventListener("click", function () { reset(); at = 0; seek(0); play(); });
    window.__lay = { seek: seek, total: total, reset: function () { reset(); at = 0; } };
    if (box.getAttribute("data-autoplay") !== "no") {
      var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (!reduce && "IntersectionObserver" in window)
        new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? play() : pause(); }); }, { threshold: 0.3 }).observe(box);
    }
  }
  fetch(src).then(function (r) { return r.json(); }).then(start);
})();
