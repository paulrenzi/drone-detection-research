# a road running toward the front: 4.03 mi of road

## Plan
posts 21 (one every 1064 ft), fence 10.2 mi in 1 run(s): 58 fence darts, 7 trunks with 35 relays; 93 air-dropped darts in all
per mile of road: 5.2 posts, 23.1 darts; longest route to a post 11 hops; nodes cut off in the plan: 0

## Strike tracks (drone flying in at 60 mph within 60 degrees of the enemy direction, 1025 tracks)
| Guard | Darts | Worst warning | 10th pct | Median | Tracks with a minute (55 s) | 30 s | 10 s |
|---|---|---|---|---|---|---|---|
| Posts only | 21 | 2 s | 4 s | 9 s | 9% | 16% | 43% |
| Posts and fence | 114 | 59 s | 68 s | 100 s | 100% | 100% | 100% |

## Landings within 300 ft of the road (486 spots)
heard by a post 100%, by two or more 24%; distance to the loudest post: median 340 ft, 90th pct 584 ft
landings 600-1,500 ft off the road: heard by a post 13% (the rest only as a drone in, none out)

## One dead node, on the plan
worst single loss leaves 99% of tracks with a minute; 0 of 114 nodes cost more than 2 points

## Holes between repairs (each dart lost 0.5% a day, each post 1.0%, found and fixed within 1 day)
dead at a time: mean 0.8; tracks with a minute: mean 100%, worst day 96%; landings heard: mean 99%

## Laying the fence
planned: 93 darts in 29 sorties; 12.2 h with 6 packs and 2 charger channels, 5.6 h with 12 packs and 4
simulated, GPS jammed, confirm, 200 lays: darts 118.7 (9 in 10 within 126), sorties 34.5, 14.7 h (6 packs) / 6.4 h (12 packs), drones lost 0.67, points left for repair 0.26
tracks with a minute after the lay: mean 100%, lays with at least 97%: 100%

## Costs, ours, small batch (est.)
package: 130 air-dropped darts, 25 posts, 14 receivers, outfitted drone with 12 packs and 4 channels: $7060 ($1751 a mile)
one re-lay of the fence: $4022 (119 darts, 0.67 drones, pack wear)
| Dart cell life | Fence re-lays a year | Fence | Posts | Repairs between re-lays | A year | A mile a year |
|---|---|---|---|---|---|---|
| 2 weeks | 26.0 | $104572 | $6142 | $9105 | $119820 | $29724 |
| 4 weeks | 13.0 | $52286 | $3071 | $9105 | $64463 | $15991 |
| 12 weeks | 4.3 | $17429 | $1024 | $9105 | $27558 | $6836 |

## If the planning numbers are wrong (50 lays each)
| Case | Posts | Air-dropped darts | Per mile | Tracks with a minute, plan | Darts used a lay | Sorties |
|---|---|---|---|---|---|---|
| Plan | 21 | 93 | 28.3 | 100% | 120.4 | 34.9 |
| Drones come within 45 degrees, not 60 | 21 | 83 | 25.8 | 100% | 107.2 | 31.2 |
| Drones come within 75 degrees | 21 | 96 | 29.0 | 100% | 124.0 | 36.3 |
| Radio hop 800 ft, not 980 | 21 | 111 | 32.7 | 100% | 143.6 | 40.6 |
| Hearing 500 ft, not 656 | 31 | 101 | 32.7 | 100% | 125.6 | 36.1 |
| A trunk every 3 mi, not 2 | 21 | 83 | 25.8 | 100% | 107.1 | 31.1 |
| Landings 95% upright, not 85% | 21 | 93 | 28.3 | 100% | 106.3 | 31.8 |
