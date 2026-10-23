# a road running along the front: 4.00 mi of road

## Plan
posts 21 (one every 1055 ft), fence 6.2 mi in 1 run(s): 35 fence darts, 5 trunks with 25 relays; 60 air-dropped darts in all
per mile of road: 5.3 posts, 15.0 darts; longest route to a post 10 hops; nodes cut off in the plan: 0

## Strike tracks (drone flying in at 60 mph within 60 degrees of the enemy direction, 1000 tracks)
| Guard | Darts | Worst warning | 10th pct | Median | Tracks with a minute (55 s) | 30 s | 10 s |
|---|---|---|---|---|---|---|---|
| Posts only | 21 | 0 s | 2 s | 4 s | 0% | 0% | 3% |
| Posts and fence | 81 | 58 s | 61 s | 71 s | 100% | 100% | 100% |

## Landings within 300 ft of the road (480 spots)
heard by a post 100%, by two or more 13%; distance to the loudest post: median 350 ft, 90th pct 525 ft
landings 600-1,500 ft off the road: heard by a post 10% (the rest only as a drone in, none out)

## One dead node, on the plan
worst single loss leaves 98% of tracks with a minute; 0 of 81 nodes cost more than 2 points

## Holes between repairs (each dart lost 0.5% a day, each post 1.0%, found and fixed within 1 day)
dead at a time: mean 0.6; tracks with a minute: mean 99%, worst day 88%; landings heard: mean 99%

## Laying the fence
planned: 60 darts in 17 sorties; 6.2 h with 6 packs and 2 charger channels, 3.3 h with 12 packs and 4
simulated, GPS jammed, confirm, 200 lays: darts 76.8 (9 in 10 within 83), sorties 22.6, 8.8 h (6 packs) / 3.8 h (12 packs), drones lost 0.47, points left for repair 0.25
tracks with a minute after the lay: mean 100%, lays with at least 97%: 99%

## Costs, ours, small batch (est.)
package: 90 air-dropped darts, 25 posts, 14 receivers, outfitted drone with 12 packs and 4 channels: $5900 ($1477 a mile)
one re-lay of the fence: $2634 (77 darts, 0.47 drones, pack wear)
| Dart cell life | Fence re-lays a year | Fence | Posts | Repairs between re-lays | A year | A mile a year |
|---|---|---|---|---|---|---|
| 2 weeks | 26.0 | $68485 | $6142 | $7098 | $81726 | $20454 |
| 4 weeks | 13.0 | $34243 | $3071 | $7098 | $44412 | $11115 |
| 12 weeks | 4.3 | $11414 | $1024 | $7098 | $19536 | $4889 |

## If the planning numbers are wrong (50 lays each)
| Case | Posts | Air-dropped darts | Per mile | Tracks with a minute, plan | Darts used a lay | Sorties |
|---|---|---|---|---|---|---|
| Plan | 21 | 60 | 20.3 | 100% | 77.7 | 22.9 |
| Drones come within 45 degrees, not 60 | 21 | 52 | 18.3 | 100% | 66.9 | 20.4 |
| Drones come within 75 degrees | 21 | 63 | 21.0 | 100% | 81.0 | 23.8 |
| Radio hop 800 ft, not 980 | 21 | 72 | 23.3 | 100% | 94.6 | 27.1 |
| Hearing 500 ft, not 656 | 31 | 66 | 24.3 | 100% | 81.6 | 24.1 |
| A trunk every 3 mi, not 2 | 21 | 55 | 19.0 | 100% | 69.8 | 21.0 |
| Landings 95% upright, not 85% | 21 | 60 | 20.3 | 100% | 69.0 | 20.6 |
