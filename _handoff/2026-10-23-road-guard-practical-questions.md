# Handoff: practical questions about guarding a supply road against fibre-optic drones

Written 2026-10-23 at tripwire HEAD 097fc68 (this handoff is the next commit). Supersedes
`2026-10-21-simplify-the-test-ui.md` as the place to start **for road work**; the test-UI job
in that file is still open and separate. The playbook (`docs/PLAYBOOK-DRONE-DETECTION.md`) is
the authority for the software; this file is history.

## State at this commit
- **Everything is pushed and live** at https://paulrenzi.github.io/tripwire. The only thing
  not committed is `_scratch_ui/`, which is never committed (patch scripts, render checks,
  the video recorder `lay_video.py`).
- **Last three commits:**
  - `db1be49` adds the road page, the route model and the jamming model.
  - `c9f9582` compares fibre and ±60° as options.
  - `097fc68` makes fibre home at ±60° the position-net plan, with the animations and every
    page updated.

## Where the road work lives
| What | File |
|---|---|
| Page | `models/route-guard.md` ("Guarding a road"), with the animation in `assets/js/route.js` and data in `assets/data/route-demo.json` |
| Model | `tools/routemodel/route_model.py`, on the lay model (`tools/laymodel/lay_model.py`). Roads: `road-lateral.json` (along the front, 2.3 mi back) and `road-radial.json` (toward it, 1.7–5.7 mi back), both invented, 4 mi each |
| Jamming | `tools/jamming/jam_model.py` (it has road rows; these did not change in 097fc68) |
| Costs | `costs.md#guarding-a-road` |
| Tests | `research/open-questions.md`: T20 = hear a landing beside a road; T21 = the fibre tip dart (position net) |

## What the road model says today (all unmeasured)
- **Two parts:**
  - Posts placed by hand every ≤1,100 ft, 40 ft off the road.
  - A fence of air-dropped darts 5,316 ft out within ±60° of the enemy, joined to the road
    by radio relay trunks every 2 mi.
- **Darts:** 21 posts and 60–93 darts for 4 mi, about 20–28 a mile.
- **Warning:** with the fence, every track gets at least 58 s, against 4–9 s with posts
  alone.
- **Landings:** every landing within 300 ft of the road is heard. Only 10–13% of landings
  600–1,500 ft out are.
- **Jamming:** the trucks' own jammers are the threat. The proposed answer is posts on
  twisted pair along the verge, plus hooded lamps facing the road, for about $200 a mile
  more.
  - In the worst case the truck's jammer reaches the fence too. The page says "jammer off on
    a hot stretch, or fibre trunks".
- **Cost:** a package of about $5,900–7,100, then $44–64k a year at four-week cells,
  $11–16k a mile.

## Known loose end, made sharper by 097fc68
**The road fence still comes home by radio trunks.** The position net just switched to
fibre home (tip darts plus a base box, about 1.2 mi of FPV fibre each, light one way only,
a 10 s heartbeat). That removed relay trunks and the jamming exposure there.
- **To decide:** whether the road fence should use the same design.
  - **For it:** tip darts at the fence, with fibre paid out to a base box on the road, or
    straight onto the verge cable.
  - **Against it:** the fence is 1 mi out, and roads run 4 mi, so it needs several fibres.
    Today's trunks are every 2 mi.
- **Not done:** `route_model.py` has no fibre option yet, and the road page and costs have
  not been touched since db1be49.

## Practical questions Paul wants to think through (next session)
Paul's framing: "practical questions about guarding a supply road against fiber optic
drones". He has not given the list yet. **Ask him for his questions first**; don't build
anything until he has. Likely candidates, from the gaps table on the page:
- **Who does it:** who lays and maintains posts on mined verges, and how often.
- **Drivers:** what a driver actually does on a "hot" alert or a "waiting" alert, and who
  clears a waiting drone.
- **Landings far out:** waiting drones that land more than 600 ft out. Would a second row
  of posts, or posts on both sides, help?
- **Traffic noise:** convoy noise masking a landing (T20).
- **Friendly drones:** our own drone crews crossing the fence all day (T15).
- **Nets:** fit with existing net tunnels, where waiting drones hide under the nets.
- **Fibre-cut repair:** if fibre trunks are adopted, how cut fibres get repaired.

## How to verify (standing)
- **Pages:** render them with Playwright and a `?cb=<n>` query; never trust an HTTP 200.
  Use `python tools/render_check.py https://paulrenzi.github.io/tripwire`; for a page-specific
  check, see the pattern in `_scratch_ui/live_fibre.py`.
- **Animations:** the lay video is recorded from `assets/js/lay.js` by
  `_scratch_ui/lay_video.py`.

## Standing rules
- US units only (in/ft/yd/mi, oz/lb, mph, °F) on every page.
- Run Python with `py`.
- Commit your own files by explicit path, never `git add -A`. Never commit `_scratch_ui`.
- Commit with `git commit -F -` and a quoted heredoc. Never write a backslash through a
  bash heredoc.
- Write a `.new` file, then `os.replace`.
- Do the research yourself. Never fan out subagents.
- Never use the paid Anthropic API.
- Answer what Paul asked, deliverable first.
