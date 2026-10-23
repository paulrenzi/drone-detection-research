---
title: "Delivery drone: airframes, control and software"
parent: Research Notes
nav_order: 4.5
---

# Delivery drone: airframes, control and software
{: .no_toc }

<p class="vz-lede">The <a href="{{ site.baseurl }}{% link models/tripwire.md %}">tripwire</a> needs a small drone that flies a planned route 1.2–2.5 mi out, drops 3–4 darts on set points and comes back, <strong>with no pilot flying it and no video link</strong>.</p>

<div class="vz-flow" role="img" aria-label="Plan the mission on a laptop, load it, fly it on autopilot with no radio link, drop a dart at each waypoint, return home">
  <div class="vz-node"><strong>Plan</strong><span>Mission Planner or QGroundControl, on a laptop</span></div>
  <div class="vz-arrow">load</div>
  <div class="vz-node vz-node-hot"><strong>Fly</strong><span>ArduPilot on a Pixhawk, in AUTO, no radio link</span></div>
  <div class="vz-arrow">at each point</div>
  <div class="vz-node vz-node-hot"><strong>Drop</strong><span>a servo step, DO_SET_SERVO</span></div>
  <div class="vz-arrow">mission ends</div>
  <div class="vz-node vz-node-dark"><strong>Return</strong><span>its log gives each dart's position</span></div>
</div>

<div class="vz-cards vz-4">
  <div class="vz-card"><p class="vz-card-num">X500</p><p>class quad with a Pixhawk 6C: the prototype airframe. Consumer DJI drones are the wrong base</p></div>
  <div class="vz-card"><p class="vz-card-num">ArduPilot</p><p>(GPLv3) as the brains; PX4 (BSD) is the alternative</p></div>
  <div class="vz-card"><p class="vz-card-num">0 links</p><p>in flight. A telemetry radio on the bench only</p></div>
  <div class="vz-card"><p class="vz-card-num">GPS jammed</p><p>is the hard part, not the software: fly on compass, optical flow and lidar (<a href="#flying-when-gps-is-jammed">how</a>)</p></div>
</div>

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="the-short-version-in-full" markdown="block">
<summary><span class="layer-title">The opening, as first written</span><span class="layer-sub">What the drone has to do</span></summary>

The [tripwire]({{ site.baseurl }}{% link models/tripwire.md %}) and [M7]({{ site.baseurl }}{% link models/m07-drone-deployed-nodes.md %}) need a small drone that flies a planned route 1.2–2.5 mi out, drops 3–4 nodes on set points and comes back, **with no pilot flying it and no video link**. This page covers which existing drones could do that, how one would be controlled, and which open-source software can be its brains.

</details>

<details class="layer" id="short-answer" markdown="block">
<summary><span class="layer-title">Short answer</span><span class="layer-sub">Control, brains, airframe, and the hard part</span></summary>

- **Control:** a flight controller running **ArduPilot** flies a GPS waypoint mission loaded before take-off. Each drop is a step in the mission. Once launched it needs no radio link at all.
- **Brains:** [ArduPilot](https://github.com/ArduPilot/ardupilot) (GPLv3), planned with Mission Planner or QGroundControl. [PX4](https://github.com/PX4/PX4-Autopilot) (BSD licence) is the alternative.
- **Airframe:** an open-autopilot kit quad for the prototype. Consumer DJI drones are the wrong base for this job.
- **The hard part is not the software. It is navigating when GPS is jammed**, which it is at the front ([Front-line conditions]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)).

</details>

<details class="layer" id="how-it-is-controlled" markdown="block">
<summary><span class="layer-title">How it is controlled</span><span class="layer-sub">A waypoint mission loaded before take-off, each drop a mission step</span></summary>

1. **Plan on the ground.** Draw the route and the drop points in a ground-station app on a laptop or tablet.
2. **Add a drop at each point.** ArduPilot has two mission steps for this: `DO_GRIPPER` opens a gripper during a mission in AUTO mode ([ArduPilot gripper docs](https://ardupilot.org/copter/docs/common-gripper-servo.html)), and `DO_SET_SERVO` moves any servo, such as a simple release pin, to a set position ([ArduPilot servo docs](https://ardupilot.org/plane/docs/common-servo.html)). The mission reads: waypoint, release, waypoint, release, … return home.
3. **Upload, then launch with every radio off.** ArduPilot can be set to carry on with an AUTO mission when the pilot's radio link is lost: `FS_OPTIONS` bit 0, "Continue if in auto mode on Radio Failsafe" ([ArduPilot radio failsafe](https://ardupilot.org/copter/docs/radio-failsafe.html)). Loss of the ground-station link has its own failsafe, which can also be set not to abort the mission ([ArduPilot GCS failsafe](https://ardupilot.org/copter/docs/gcs-failsafe.html)).
4. **It flies home** at the end of the mission, or when its battery runs low.

{: .warning }
> Failsafe behaviour must be proven in simulation (ArduPilot's SITL) and on the bench for the exact firmware version before any flight. Forum reports describe copters returning home when the owner expected them to continue ([ArduPilot forum](https://discuss.ardupilot.org/t/rf-throttle-failsafe-triggered-but-the-drone-rtl-instead-of-continuing-mission/98732)).

Because no link is used in flight, the drone emits nothing while laying the line, which is the same rule the nodes follow.

</details>

<details class="layer" id="existing-airframes" markdown="block">
<summary><span class="layer-title">Existing airframes</span><span class="layer-sub">Kit quads, consumer drones and why not</span></summary>

| Option | How it's controlled | Fits this job? |
|---|---|---|
| **Consumer DJI** (Mini, Mavic) | DJI apps, or Android apps built on DJI's Mobile SDK v5. Waypoint support in the SDK covers enterprise models (Matrice 30/300, Mavic 3 Enterprise) ([DJI SDK forum](https://sdk-forum.dji.net/hc/en-us/articles/12584358291097-What-is-the-store-logic-of-an-kmz-file)); third-party apps such as Litchi add waypoints on some consumer models ([Litchi forum](https://forum.flylitchi.com/t/new-litchi-pilot-beta/10621)) | **No.** Closed firmware, no confirmed drop step on consumer models, and DJI drones broadcast identification that can be used to locate them ([CSO Online](https://www.csoonline.com/article/3653352/are-ukraine-s-drone-capabilities-being-throttled-in-russia-ukraine-conflict.html)). DJI suspended business in Ukraine and Russia in 2022 ([Fox 26](https://www.fox26houston.com/news/dji-halts-business-in-ukraine-russia-to-prevent-drone-misuse)), and China has restricted drone exports since September 2024 ([CSIS](https://www.csis.org/analysis/why-chinas-uav-supply-chain-restrictions-weaken-ukraines-negotiating-power)) |
| **Open-autopilot kit quad**, e.g. Holybro X500 V2 with a Pixhawk 6C or 6X | ArduPilot or PX4, out of the box | **Yes, for the prototype.** Documented, open firmware, servo and gripper missions, no DJI identification broadcast. Listed at $508 for the base kit ([Holybro](https://shop.holybro.com/x500-kit_p1180.html)) and $946 with flight controller, GPS and telemetry radio from a US retailer ([Pyrodrone](https://pyrodrone.com/products/holybro-x500-v2-pixhawk-development-kit-with-the-pixhawk-6x-standard-m10-gps-915mhz-telemetry-radio)). Bigger than needed; a smaller ArduPilot quad or a printed frame with the same electronics is the production path |
| **Ukrainian heavy drop drones**, e.g. the "Vampire" ("Baba Yaga") | Proprietary; the autopilot isn't publicly confirmed | **Too big.** Press figures: 33 lb payload, about 12 mi range ([Army Recognition](https://www.armyrecognition.com/archives/archives-land-defense/defense-news-army-2025/landeuro-2025-ukrainian-vampire-drone-emerges-as-fearsome-night-striking-tool-against-russian-forces)), costing roughly $10,000–20,000 by conflicting reports. Ukrainian units can order custom drones to a payload specification through the [Brave1 Market](https://brave1.gov.ua/en/news/custom-drones-on-brave1-market), a possible route to a purpose-built carrier |

ArduPilot is already reported in Ukrainian use: press reports say Operation Spider Web in June 2025 ran on it ([404 Media](https://www.404media.co/ukraines-massive-drone-attack-was-powered-by-open-source-software/)), though the evidence given publicly is thin.

</details>

<details class="layer" id="open-source-software-for-the-brains" markdown="block">
<summary><span class="layer-title">Open-source software for the brains</span><span class="layer-sub">ArduPilot, PX4 and their ground stations</span></summary>

Licences, stars and activity read from GitHub on 2026-10-15.

| Software | Licence | What it does | Use it? |
|---|---|---|---|
| [ArduPilot](https://github.com/ArduPilot/ardupilot) | GPL-3.0 | The autopilot: flight control, missions, failsafes, position estimate. ~16,000 stars, active | **Yes: the brains** |
| [PX4](https://github.com/PX4/PX4-Autopilot) | BSD-3-Clause | Alternative autopilot. The permissive licence is easier inside a closed product. ~12,800 stars, active | Alternative |
| [INAV](https://github.com/iNavFlight/inav) | GPL-3.0 | Lighter autopilot for hobby quads and wings, with waypoints | Possible for a cheap fixed-wing; drop support unchecked |
| [Mission Planner](https://github.com/ArduPilot/MissionPlanner) | GPL-3.0 | Windows ground station: plan missions, set parameters | Yes, for planning and set-up |
| [QGroundControl](https://github.com/mavlink/qgroundcontrol) | Apache-2.0 | Ground station for ArduPilot and PX4, runs on phones and tablets | Yes, for units in the field |
| [MAVProxy](https://github.com/ArduPilot/MAVProxy) | GPL-3.0 | Command-line ground station | For scripted, repeatable mission loading |
| [MAVSDK](https://github.com/mavlink/MAVSDK) | BSD-3-Clause | Programming interface (C++, Python and more) for missions | For a custom "lay a line" app |
| [pymavlink](https://github.com/ArduPilot/pymavlink) | check before use | Low-level Python library for the drone's message protocol (MAVLink) | For tooling |
| [DroneKit-Python](https://github.com/dronekit/dronekit-python) | Apache-2.0 | Older Python interface; no commits since May 2024 | **No:** stale |
| [mLRS](https://github.com/olliw42/mLRS), [ExpressLRS](https://github.com/ExpressLRS/ExpressLRS) | GPL-3.0 | Open long-range control and telemetry links | Only for testing; in operation fly with no link |
| [OpenHD](https://github.com/OpenHD/OpenHD) | GPL-3.0 | Digital video link | **No:** we don't want video |

{: .note }
> GPLv3 means anyone who distributes a modified ArduPilot build must offer its source code to the people they give it to. PX4's BSD licence carries no such duty. Export controls on navigation and autopilot technology need legal advice ([Export controls]({{ site.baseurl }}{% link research/regulation-funding.md %})).

</details>

<details class="layer" id="flying-when-gps-is-jammed" markdown="block">
<summary><span class="layer-title">Flying when GPS is jammed</span><span class="layer-sub">Optical flow, compass and lidar from a known start</span></summary>

GPS jamming is routine at the front ([Front-line conditions]({{ site.baseurl }}{% link research/field-conditions.md %}#electronic-warfare)). ArduPilot rejects GPS readings that disagree sharply with its own motion estimate ([EKF failsafe docs](https://ardupilot.org/copter/docs/common-ekf-inav-failsafe.html)), but that handles glitches, not a slow, deliberate spoof. Options without GPS:

| Approach | Good enough for a 1–2.5 mi leg? |
|---|---|
| **Optical flow camera + rangefinder** | Holds position and speed, but drifts over miles with no absolute fix ([ArduPilot non-GPS navigation](https://ardupilot.org/copter/docs/common-non-gps-navigation-landing-page.html)). Not enough on its own |
| **Visual odometry** (camera-based motion tracking) | PX4 documents how to feed it in ([PX4 docs](https://docs.px4.io/v1.17/en/ros/external_position_estimation)). Also drifts without a reference |
| **Matching the camera view to satellite maps** | Open research code exists, e.g. [WildNav](https://github.com/TIERS/wildnav), but nothing found that plugs into ArduPilot. Needs a camera and an onboard computer, adding weight and cost. Ukrainian systems doing this are reported but proprietary |
| **Anti-jam antennas (CRPA)** | Around $7,000–8,000 each for the units found ([Nordsint](https://nordsint.org/2026/05/08/geraniums-in-bloom-how-a-major-chinese-antenna-manufacturer-powers-russias-drone-fleet/)). Far beyond this budget |

**Our working approach (an inference, to be tested):** a net doesn't need yard accuracy if every dart is confirmed by radio as it lands ([Laying the net]({{ site.baseurl }}{% link models/line-layout.md %}#laying-the-net)). So start with plain GPS, measure how badly it fails at realistic sites, and fall back to compass, optical flow and lidar (an MTF-01P, about $42) from an origin set at launch, cruising 35 ft up in daylight. Map matching is the upgrade if tests show GPS is unusable. This is tracked as T14 in [Open questions]({{ site.baseurl }}{% link research/open-questions.md %}).

</details>

<details class="layer" id="recommended-prototype" markdown="block">
<summary><span class="layer-title">Recommended prototype</span><span class="layer-sub">Airframe, release, mission, links, scripting and navigation, and what's still unknown</span></summary>

1. **Airframe:** an X500-class quad with a Pixhawk 6C, running ArduPilot Copter.
2. **Release:** one servo-driven pin per node, triggered by `DO_SET_SERVO` after each drop waypoint.
3. **Mission:** planned in Mission Planner or QGroundControl, flown in AUTO with the radio failsafe set to continue the mission.
4. **Links:** none in flight. A telemetry radio on the bench only.
5. **Scripting:** MAVProxy or pymavlink to load identical missions repeatably.
6. **Navigation:** plain GPS first; add optical flow before anything costlier.

**Still unknown:** flight time and range of a small quad carrying 3–4 nodes. No sourced figure was found; it gets measured in the autonomous drop sortie test (T13).

</details>
