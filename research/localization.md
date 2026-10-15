---
title: Localization methods (distance and direction)
parent: Research Notes
nav_order: 3
---

# Localization methods — getting distance and direction right
{: .no_toc }

This is the "hard part" in the original framing. The short version: **don't try to measure distance at a single node. Measure direction at each node and let geometry give you distance.**

1. TOC
{:toc}

## 1. Direction at a node (direction of arrival)

A small array of microphones hears the same sound at slightly different times. With known mic spacing, those time differences give a bearing.

| Method | Idea | Notes |
|---|---|---|
| GCC-PHAT | Cross-correlate mic pairs, find time lag | Simple, robust, cheap on a microcontroller |
| SRP-PHAT | Scan directions, pick the loudest steered response | More robust with multiple sources |
| MUSIC / subspace | Separate signal from noise directions | Sharper, more compute |

- Bigger arrays → better bearing precision, but too large an array for high frequencies causes ambiguity (spatial aliasing). 10–20 cm suits drone frequencies.
- Realistic bearing error for a cheap 4-mic array outdoors: **a few degrees to ~10°** (to be measured).
- Bearing must be converted to *true north* with a compass and tilt sensor. Compass error adds directly to bearing error.

## 2. Position from several nodes (triangulation)

Each node reports a bearing line. Where three or more lines cross is the target.

- **Error grows with distance:** 5° of bearing error at 2 km ≈ 175 m sideways error from that node. Nodes viewing from different angles cut it down.
- **Geometry matters:** nodes on one side of the target give long, thin error ellipses; surrounding the target gives tight fixes.
- With elevation angles too, the network can estimate altitude.

## 3. Cross-check: time difference between nodes

Nodes with GPS timing (PPS) can timestamp detections to well under a millisecond. Sound travels ~34 cm per ms, so arrival-time differences between nodes give an independent range check. Hard to use alone for continuous drone noise (see [M3]({% link models/m03-single-mic-tdoa.md %})), useful as a second opinion.

## 4. Tracking

- A **Kalman filter** (or similar) turns noisy fixes into smooth tracks with speed and heading, and predicts where the target will be — what fire teams actually need.
- **Data association** — deciding which bearing belongs to which drone when several are in the air — is the hard algorithm problem in mass raids. Standard tools: multi-hypothesis tracking, JPDA, or using the classifier's sound fingerprint to group bearings.

## 5. Single-node distance estimation

Possible tricks (loudness falloff, Doppler shift, ratio of high to low frequencies) all depend on things the node doesn't know — how loud the drone actually is, its speed, the weather. **Treat as unreliable**; at most a rough hint for the tracker.

## Validation plan

Fly a drone with a GPS logger over 3–5 nodes. Compare network tracks to the GPS log to measure bearing error, position error vs. distance, and detection range. The Western Sydney 24-mic dataset (see [Datasets]({% link research/datasets.md %})) includes GPS flight logs and can be used before any hardware exists.
