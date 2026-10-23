---
title: Localization methods (distance and direction)
parent: Research Notes
nav_order: 3
---

# Localization methods — getting distance and direction right
{: .no_toc }

<p class="vz-lede"><strong>Don't measure distance at one node.</strong> Measure direction at each node and let geometry give you the distance.</p>

<figure class="vz-figure vz-narrow">
<svg viewBox="0 0 420 300" role="img" aria-labelledby="loc-t">
  <title id="loc-t">Three nodes each measure a bearing to the drone; the lines cross at the drone. Each bearing has an error wedge, so the crossing is a small area, not a point.</title>
  <g fill="#d2451e" fill-opacity=".08" stroke="none">
    <path d="M60 260 L262 80 L252 66 Z"/><path d="M210 280 L250 72 L264 74 Z"/><path d="M380 250 L250 78 L262 66 Z"/>
  </g>
  <g stroke="#151515" stroke-width="2" stroke-dasharray="6 5"><line x1="60" y1="260" x2="257" y2="73"/><line x1="210" y1="280" x2="257" y2="73"/><line x1="380" y1="250" x2="257" y2="73"/></g>
  <g fill="#d2451e"><circle cx="60" cy="260" r="9"/><circle cx="210" cy="280" r="9"/><circle cx="380" cy="250" r="9"/></g>
  <g transform="translate(257 73)" stroke="#151515" stroke-width="3"><line x1="-10" y1="-10" x2="10" y2="10"/><line x1="10" y1="-10" x2="-10" y2="10"/>
    <g fill="#fff" stroke-width="2"><circle cx="-10" cy="-10" r="4.5"/><circle cx="10" cy="-10" r="4.5"/><circle cx="-10" cy="10" r="4.5"/><circle cx="10" cy="10" r="4.5"/></g></g>
  <text x="280" y="44" class="vz-t" style="font-size:17px">bearings cross</text>
  <text x="280" y="64" class="vz-t" style="font-size:17px">at the drone</text>
  <text x="20" y="292" class="vz-t-small" style="font-size:15px">each node: a small mic array</text>
</svg>
<figcaption>Each node gives a bearing; three or more crossing give a position. 5° of bearing error at 1.2 mi is about 570 ft sideways, so nodes viewing from different angles matter.</figcaption>
</figure>

<div class="vz-steps vz-4">
  <div class="vz-step"><p class="vz-step-num">1 · Direction</p><p>A small array times the sound at each mic: a bearing</p></div>
  <div class="vz-step"><p class="vz-step-num">2 · Position</p><p>Bearings from three or more nodes cross at the drone</p></div>
  <div class="vz-step"><p class="vz-step-num">3 · Cross-check</p><p>Time differences between nodes, where clocks allow</p></div>
  <div class="vz-step"><p class="vz-step-num">4 · Track</p><p>A tracking filter turns positions into a path</p></div>
</div>

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="the-short-version-in-full" markdown="block">
<summary><span class="layer-title">The opening, as first written</span><span class="layer-sub">The page's original introduction</span></summary>

This is the "hard part" in the original framing. The short version: **don't try to measure distance at a single node. Measure direction at each node and let geometry give you distance.**

</details>

<details class="layer" id="1-direction-at-a-node-direction-of-arrival" markdown="block">
<summary><span class="layer-title">1. Direction at a node (direction of arrival)</span><span class="layer-sub">GCC-PHAT, SRP-PHAT and MUSIC, array size, and true north</span></summary>

A small array of microphones hears the same sound at slightly different times. With known mic spacing, those time differences give a bearing.

| Method | Idea | Notes |
|---|---|---|
| GCC-PHAT | Cross-correlate mic pairs, find time lag | Simple, robust, cheap on a microcontroller |
| SRP-PHAT | Scan directions, pick the loudest steered response | More robust with multiple sources |
| MUSIC / subspace | Separate signal from noise directions | Sharper, more compute |

- Bigger arrays → better bearing precision, but too large an array for high frequencies causes ambiguity (spatial aliasing). 3.9–7.9 in suits drone frequencies.
- Realistic bearing error for a cheap 4-mic array outdoors: **a few degrees to ~10°** (to be measured).
- Bearing must be converted to *true north* with a compass and tilt sensor. Compass error adds directly to bearing error.

</details>

<details class="layer" id="2-position-from-several-nodes-triangulation" markdown="block">
<summary><span class="layer-title">2. Position from several nodes (triangulation)</span><span class="layer-sub">Crossing bearings, and how error grows with distance</span></summary>

Each node reports a bearing line. Where three or more lines cross is the target.

- **Error grows with distance:** 5° of bearing error at 1.2 mi ≈ 570 ft sideways error from that node. Nodes viewing from different angles cut it down.
- **Geometry matters:** nodes on one side of the target give long, thin error ellipses; surrounding the target gives tight fixes.
- With elevation angles too, the network can estimate altitude.

</details>

<details class="layer" id="3-cross-check-time-difference-between-nodes" markdown="block">
<summary><span class="layer-title">3. Cross-check: time difference between nodes</span><span class="layer-sub">Timing across nodes as a second fix</span></summary>

Nodes with GPS timing (PPS) can timestamp detections to well under a millisecond. Sound travels ~13 in per ms, so arrival-time differences between nodes give an independent range check. Hard to use alone for continuous drone noise (see [M3]({{ site.baseurl }}{% link models/m03-single-mic-tdoa.md %})), useful as a second opinion.

</details>

<details class="layer" id="4-tracking" markdown="block">
<summary><span class="layer-title">4. Tracking</span><span class="layer-sub">Filters and telling several drones apart</span></summary>

- A **Kalman filter** (or similar) turns noisy fixes into smooth tracks with speed and heading, and predicts where the target will be — what fire teams actually need.
- **Data association** — deciding which bearing belongs to which drone when several are in the air — is the hard algorithm problem in mass raids. Standard tools: multi-hypothesis tracking, JPDA, or using the classifier's sound fingerprint to group bearings.

</details>

<details class="layer" id="5-single-node-distance-estimation" markdown="block">
<summary><span class="layer-title">5. Single-node distance estimation</span><span class="layer-sub">Why one node can't reliably judge distance</span></summary>

Possible tricks (loudness falloff, Doppler shift, ratio of high to low frequencies) all depend on things the node doesn't know — how loud the drone actually is, its speed, the weather. **Treat as unreliable**; at most a rough hint for the tracker.

</details>

<details class="layer" id="validation-plan" markdown="block">
<summary><span class="layer-title">Validation plan</span><span class="layer-sub">Fly a logged drone over 3–5 nodes and compare</span></summary>

Fly a drone with a GPS logger over 3–5 nodes. Compare network tracks to the GPS log to measure bearing error, position error vs. distance, and detection range. The Western Sydney 24-mic dataset (see [Datasets]({{ site.baseurl }}{% link research/datasets.md %})) includes GPS flight logs and can be used before any hardware exists.

</details>
