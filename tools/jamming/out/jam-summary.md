# Jamming: how far a jammer blinds our radio, and what that does to the nets

Assumed: jammer power spread over 860-940 MHz, SF9, 125 kHz, 5 dB link margin, always on. Near the ground: the jammer's signal fades as our darts' does (the main estimate for a jammer near the ground). Clear path: plain two-ray over open ground while our hops stay as short as planned (the worst case; nearer the truth for a jammer up high).

## Reach: inside this distance the radio cannot receive
| Jammer | a dart | a post (whip on a stake) | the position's raised receiver |
|---|---|---|---|
| Trench jammer, 20 W, 5 ft up | 390 ft to 1.1 mi | 480 ft to 1.4 mi | 1030 ft to 3.0 mi |
| Vehicle jammer, 100 W, 8 ft up | 740 ft to 2.2 mi | 910 ft to 2.7 mi | 1950 ft to 5.7 mi |
| Jammer on a mast, 50 W, 33 ft up | 1260 ft to 3.7 mi | 1560 ft to 4.5 mi | 0.6 mi to 9.7 mi |
| A LoRa hunter, 20 W all in our channel, 5 ft up | 1970 ft to 5.7 mi | 2420 ft to 7.1 mi | 1.0 mi to 15.2 mi |

## The position net (the lay model's sector), every jammer on
| Case | Path | Darts jammed | Receiver jammed | Darts that reach the unit | Worst warning |
|---|---|---|---|---|---|
| Enemy trench jammers along their edge | near the ground | 0 | no | 16 of 16 | 60 s |
| Enemy trench jammers along their edge | clear | 16 | no | 2 of 16 | none |
| LoRa hunters along their edge | near the ground | 7 | no | 11 of 16 | none |
| LoRa hunters along their edge | clear | 16 | no | 2 of 16 | none |
| Our trench jammers at the positions | near the ground | 0 | no | 16 of 16 | 60 s |
| Our trench jammers at the positions | clear | 16 | no | 2 of 16 | none |
| All of them | near the ground | 0 | no | 16 of 16 | 60 s |
| All of them | clear | 16 | no | 2 of 16 | none |
| Last plan (radio trunks to a receiver at P2), our trench jammers | near the ground | 0 | yes | 0 of 25 | none |
| Last plan (radio trunks to a receiver at P2), our trench jammers | clear | 25 | yes | 0 of 25 | none |
| Last plan, enemy trench jammers | near the ground | 0 | no | 25 of 25 | 60 s |
| Last plan, enemy trench jammers | clear | 25 | yes | 0 of 25 | none |

## The road guard: share of strike tracks with a minute (55 s)
| Road | Case | Near the ground | Clear path |
|---|---|---|---|
| a road running along the front | Our and the enemy's trench jammers on | 100% | 100% |
| a road running along the front | The truck's own jammer on, radio guard | 0% | 0% |
| a road running along the front | The truck's own jammer on, posts on a wire with lamps | 100% | 2% |
| a road running along the front | All of them, posts on a wire with lamps | 100% | 2% |
| a road running toward the front | Our and the enemy's trench jammers on | 100% | 89% |
| a road running toward the front | The truck's own jammer on, radio guard | 0% | 0% |
| a road running toward the front | The truck's own jammer on, posts on a wire with lamps | 100% | 22% |
| a road running toward the front | All of them, posts on a wire with lamps | 100% | 21% |
