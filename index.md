---
title: Overview
layout: home
nav_order: 1
---

<div class="hero" markdown="1">
<span class="hero-tag">RESEARCH NOTEBOOK · REVIEWED 2026-10-21</span>

# The drone-laid acoustic tripwire

Don't try to make a microphone hear farther. Drop cheap ones 2–4 km forward, so a front-line unit gets about a minute of warning of an incoming FPV instead of about ten seconds, including fibre-optic FPVs that emit no radio.
</div>

<div class="stats">
  <div class="stat"><p class="stat-num">~1 min</p><p class="stat-label">warning from a line 2 km out, against ~10 s from a ring near the unit (est.)</p></div>
  <div class="stat"><p class="stat-num">$17–50</p><p class="stat-label">per throwaway listener (parts estimate)</p></div>
  <div class="stat"><p class="stat-num">50–60 m</p><p class="stat-label">the only measured cheap-mic range; we plan on 100–300 m, unproven</p></div>
  <div class="stat"><p class="stat-num">3/5</p><p class="stat-label">feasibility: every part exists, the whole chain is untested</p></div>
</div>

{: .warning }
> **Nothing here has been built or field-tested yet.** Ranges, costs and warning times are estimates from published sources, labelled as such. The tests that would settle them are cheap, and listed under [Weekend test and MVP]({{ site.baseurl }}{% link mvp.md %}).

<p class="kicker">01 · The idea</p>

## Lay a line, listen quietly, report back, warn.

1. **Lay a line.** A small drone with no pilot drops 3–4 throwaway listeners per flight across the enemy's approach, 2–4 km out. Two lines, a few hundred metres apart.
2. **Listen quietly.** Each listener sleeps until it hears something drone-like, and transmits nothing while it waits.
3. **Report back.** A few-byte alert hops listener to listener to a listen-only receiver at the edge of the unit's tree line, wired back to the dugout, so the unit's position emits nothing.
4. **Warn.** Warning time is distance ÷ drone speed. A line 2 km out gives about 50–65 seconds against an FPV; a ring of microphones 300 m out gives 8–10 (both estimates).

The idea is to buy warning with distance rather than with sensitivity. A better microphone gains tens of metres; laying the line forward gains kilometres.

<p class="kicker">02 · Why it matters</p>

## The threat nothing cheap detects.

- **Drones cause about 80% of casualties** at the front, by analysts' estimates ([NPR, Oct 2026](https://www.tpr.org/news/2026-10-05/drones-buzz-overhead-troops-hunker-underground-in-ukraines-hellish-kill-zone)). Units cope by not moving, and every trip out is exposure.
- **Fibre-optic FPVs emit no radio**, so the radio detectors units carry miss them and jamming does nothing. In some sectors they are 30–50% or more of FPVs. A microphone hears them ([what troops have]({{ site.baseurl }}{% link research/frontline-kit.md %})).
- **Acoustic detection works at scale, against a different target.** Ukraine's Sky Fortress hears Shaheds and cruise missiles over the rear with thousands of cheap pole-mounted sensors. Loud, low-pitched engines carry for kilometres; small electric FPVs don't. Against FPVs at the front, no acoustic system has an independent test yet.
- **Our central guess is 1–4 of every 100 drone casualties averted**, almost all among people about to move ([estimate]({{ site.baseurl }}{% link research/lives-model.md %})). That is a guess, not a measurement.

Full evidence: [Is the problem worth solving?]({{ site.baseurl }}{% link research/problem-check.md %})

<p class="kicker">03 · How to assess it</p>

## Four things decide whether the tripwire is worth building.

<div class="assess">
<a class="assess-card" href="{{ site.baseurl }}{% link build-3d.md %}">
<span class="assess-num">02</span>
<span class="assess-title">3D models and downloads</span>
<span class="assess-q">Can a printed dart and harness carry, release and stand a listener?</span>
<span class="assess-body">Rotate the dart, the harness and the loaded X500, and watch them come apart. STL and STEP files for every printed part.</span>
</a>
<a class="assess-card" href="{{ site.baseurl }}{% link research/competitors.md %}">
<span class="assess-num">03</span>
<span class="assess-title">Competitors</span>
<span class="assess-q">Who else warns a position of FPVs, and at what cost?</span>
<span class="assess-body">Zvook NW0 at $834–950 a sensor, RADD, Komodo's drone-dropped sensor, DroneAlert. All claims, no independent FPV range.</span>
</a>
<a class="assess-card" href="{{ site.baseurl }}{% link mvp.md %}">
<span class="assess-num">04</span>
<span class="assess-title">Weekend test and MVP</span>
<span class="assess-q">How far does a mic near the ground hear a drone, and can a line report home?</span>
<span class="assess-body">An $80–90 weekend kit, then five gated layers to a six-listener line for about $600–750 in total.</span>
</a>
<a class="assess-card" href="{{ site.baseurl }}{% link models/tripwire.md %}">
<span class="assess-num">+</span>
<span class="assess-title">The full design</span>
<span class="assess-q">How each piece works, what it costs, and what could kill it.</span>
<span class="assess-body">Warning time, the listener, the delivery drone, getting alerts out of the trees, field limits and risks.</span>
</a>
</div>

<p class="kicker">04 · Where it stands</p>

## Three open questions, each under $500 to answer.

| Question | Why it decides the tripwire | Test | Status |
|---|---|---|---|
| **Can a line report back from under trees?** | A line that can't get its alerts home is useless | [T9]({{ site.baseurl }}{% link research/open-questions.md %}#t9-can-a-forward-line-report-back), ~$80 | Open ground probably works on published figures; under trees, unproven |
| **How far does a mic at 0.5–1 m hear an FPV?** | Range sets listener spacing, so the cost of a line. Under about 40 m the idea stops making sense | [T11]({{ site.baseurl }}{% link mvp.md %}#layer-2-hear-a-drone-from-near-the-ground-t11), ~$50 | Only measured cheap-mic range is 50–60 m, on a consumer drone |
| **Does a dropped dart land upright and working?** | Drone laying is what puts the line 2–4 km out | A weighted dummy dropped from the drone | Modelled, not printed or dropped |

Ratings are working judgements, not test results. [Build or scrap?]({{ site.baseurl }}{% link research/build-or-scrap.md %}) sets out what result would stop the project.

<p class="kicker">05 · The rest of the notebook</p>

## Other models, kept for reference.

This notebook started as a survey of eight ways to build a cheap acoustic sensor network: fixed mic-array meshes, phone networks, elevated nodes, aerostats and more. The tripwire came out of that survey as the use case worth testing first. The survey is still here: [the wider field]({{ site.baseurl }}{% link research/landscape.md %}) and [all sensor models]({{ site.baseurl }}{% link models/index.md %}).

## How to add to this

Each page is a Markdown file in the [repository](https://github.com/paulrenzi/drone-detection-research). Record rating changes and new research in the [changelog]({{ site.baseurl }}{% link changelog.md %}).
