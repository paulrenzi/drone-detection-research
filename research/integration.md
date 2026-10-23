---
title: Central API and military integration
parent: Research Notes
nav_order: 6
---

# Central API and military integration
{: .no_toc }

<p class="vz-lede">The military doesn't want a new app. <strong>It wants tracks to appear in the tools it already uses.</strong> So the fusion server speaks their standard formats.</p>

<div class="vz-flow" role="img" aria-label="Nodes send small detection reports to a fusion server, which associates, triangulates and tracks, then sends Cursor-on-Target to TAK, SAPIENT to command systems, and feeds to Anduril Lattice and a web map">
  <div class="vz-node vz-node-hot"><strong>Nodes</strong><span>time, position, bearing, class, confidence: small enough for LoRa</span></div>
  <div class="vz-arrow">reports</div>
  <div class="vz-node"><strong>Fusion server</strong><span>associate, triangulate, track, classify the threat</span></div>
  <div class="vz-arrow">standard formats</div>
  <div class="vz-node vz-node-dark"><strong>Their tools</strong><span>CoT to TAK · SAPIENT to C2 · Anduril Lattice · a web map</span></div>
</div>

<div class="vz-cards">
  <div class="vz-card"><p class="vz-card-num">Lattice first</p><p>Anduril's fusion software is the US Army's counter-drone backbone: the first integration target</p></div>
  <div class="vz-card"><p class="vz-card-num">TAK via CoT</p><p>Cursor-on-Target XML, native to ATAK, used by US, allied and Ukrainian forces</p></div>
  <div class="vz-card"><p class="vz-card-num">Secure by default</p><p>Per-device keys, encrypted links, and no raw audio ever leaves a node</p></div>
</div>

## The details

Each section opens for the full reasoning, numbers and sources.

<button type="button" class="layer-toggle" data-layers-toggle>Open all sections</button>

<details class="layer" id="what-a-centralized-api-to-plot-drones-should-mean" markdown="block">
<summary><span class="layer-title">What "a centralized API to plot drones" should mean</span><span class="layer-sub">The standard formats to output, and why each matters</span></summary>

The military doesn't want a new app. It wants tracks to appear in the tools it already uses. Build the fusion server to **output standard formats**:

| Standard | What it is | Why it matters |
|---|---|---|
| **Cursor-on-Target (CoT)** | Simple XML event format for "something is at this place" | Native to **TAK** (ATAK/WinTAK/iTAK), used widely by US and allied forces and by Ukraine |
| **Anduril Lattice** | Anduril's sensor-fusion and command-and-control software | The US Army's counter-drone backbone; **first integration target** (see below) |
| **SAPIENT** | UK MOD open interface standard for counter-UAS sensors and fusion nodes | Adopted in NATO counter-UAS interoperability work; lets a sensor plug into others' C2 systems |
| GeoJSON / REST / WebSocket | Plain web API | For dashboards, partners, testing |

For the systems Ukrainian troops already carry, and which to target first, see [Partners for the alert]({{ site.baseurl }}{% link research/partners.md %}).

</details>

<details class="layer" id="suggested-data-flow" markdown="block">
<summary><span class="layer-title">Suggested data flow</span><span class="layer-sub">Node to server to users, step by step</span></summary>

1. **Node → server:** detection report (time, node position, bearing, elevation, class, confidence). Small enough for LoRa.
2. **Server:** association → triangulation → tracking → threat classification.
3. **Server → users:** CoT to TAK, SAPIENT to C2, GeoJSON to a web map; alerts to fire teams with predicted path.

</details>

<details class="layer" id="anduril-lattice" markdown="block">
<summary><span class="layer-title">Anduril Lattice</span><span class="layer-sub">What it is, and how a cheap sensor plugs in</span></summary>

Lattice is the integration that matters most. The US Army awarded Anduril an enterprise contract worth up to $20B over 10 years, and JIATF-401 picked Lattice as its counter-UAS command-and-control platform (see [Competitors]({{ site.baseurl }}{% link research/competitors.md %})). A sensor that feeds Lattice reaches the buyer directly.

**What we would send:** each detection as a Lattice track or entity, with position (or bearing from the node), time, class and confidence. Acoustic bearings can cue Anduril's own WISP cameras onto drones they would otherwise miss behind terrain or trees.

**How partners plug in:** Anduril publishes a Lattice SDK for partners, with data model definitions, API bindings, code samples and reference implementations, and runs a Lattice Partner Program. In a CENTCOM exercise, more than 10 sensor teams used it to bring their sensors into one Lattice picture.

{: .warning }
> From press and secondary sources, not Anduril's own docs: live Lattice environments are reportedly partner-gated and subject to US export controls (ITAR/EAR). Confirm the access process, licensing and the exact entity schema directly with Anduril.

**Next step:** a conversation with Anduril about the partner path: what it takes to get SDK and sandbox access, whether a passive acoustic sensor fills a gap they see, and what a pilot looks like.

</details>

<details class="layer" id="security" markdown="block">
<summary><span class="layer-title">Security</span><span class="layer-sub">Keeping the feed and the nodes safe</span></summary>

- Authenticate nodes (per-device keys) so an adversary can't inject fake drones.
- Encrypt links; assume radios and cell networks are monitored.
- No raw audio leaves nodes — reduces privacy risk and intelligence value if intercepted.
- Keep node radio emissions short and rare so the network stays passive in practice, not just in name.

</details>

<details class="layer" id="sources" markdown="block">
<summary><span class="layer-title">Sources</span><span class="layer-sub">Every source on this page</span></summary>

- [OCBJ — Anduril enabling partners to operate on Lattice (Lattice SDK)](https://www.ocbj.com/defense-2/anduril-industries-enabling-partners-to-operate-on-lattice/)
- [The Defense Post — CENTCOM exercise uses Lattice to integrate 10+ sensor teams](https://thedefensepost.com/2024/11/14/us-centcom-exercise-anduril-lattice/amp/)

</details>
