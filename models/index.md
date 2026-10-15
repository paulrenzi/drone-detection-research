---
title: Sensor Models
nav_order: 2
has_children: true
permalink: /models/
---

# Sensor Models

Each page describes one way of deploying listeners, with a feasibility rating, an estimated cost, how it works, what limits it, and the open questions that would change the rating.

The [overview matrix]({% link index.md %}#feasibility-matrix) compares them side by side.

## Recommended combination (current view)

1. **Core:** [M1 fixed mic-array nodes]({% link models/m01-ground-array-mesh.md %}) mounted per [M4 elevated placement]({% link models/m04-elevated-nodes.md %}).
2. **Bootstrap / surge:** [M2 phones]({% link models/m02-phone-network.md %}) where speed matters more than unit quality.
3. **Phase 2:** [M10 hybrid cueing]({% link models/m10-hybrid-cueing.md %}) — add passive RF and camera confirmation at key sites.
4. **R&D bet:** [M6 perch-and-listen]({% link models/m06-perch-and-listen.md %}) and [M7 drone-deployed nodes]({% link models/m07-drone-deployed-nodes.md %}) for fast placement in contested areas.
