Completed entirely inside `cad/gpt61/`, with no commit or push.

| Model | File size |
|---|---:|
| `web/dart.glb` | 3.64 MB |
| `web/harness.glb` | 4.51 MB |
| `web/aircraft.glb` | 19.34 MB |

Each contains an eight-second `explode` animation, named part nodes, PBR colours, metres and Y-up coordinates. The dart is horizontal.

Also delivered five inspected PNGs, the complete [manifest](C:/Users/paulm/drone-detection-research/cad/gpt61/web/manifest.json), updated documentation, and [web_export.py](C:/Users/paulm/drone-detection-research/cad/gpt61/web_export.py) to regenerate everything.

All read-back and exploded-overlap checks pass. Khronos reports **0 errors and 0 warnings** for every GLB. Original geometry and `out/` files remain unchanged.

Unmeasured properties remain flagged; the rigid animation illustrates assembly without simulating flexible parts or unscrewing.