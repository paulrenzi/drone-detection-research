"""Regenerate regular presentation PNGs from the current verified B-rep cache.

The five web/exploded PNGs are generated separately by web_export.py.
"""
import sys
sys.dont_write_bytecode=True
from build import load_cache,render_all,print_transform,RENDERS
from geometry import box
from render_local import render

p=load_cache()
render_all(p)
# These two final images were last produced by refresh_stake_prints.py, whose
# orange material and flat-base caption differ from build.py's defaults. Repeat
# those exact scenes, without running the geometry/export refresh script.
for n in ('stake_adapter','stake_cell_holder'):
    s=print_transform(n,p[n]);b=s.BoundingBox()
    render([(s,'body'),(box(b.xlen+12,b.ylen+12,.6,at=(0,0,-.6)),'white')],
           RENDERS/f'print_{n}.png',f'Print orientation - {n.replace("_"," ")}',
           f'{b.xlen:.1f} x {b.ylen:.1f} x {b.zlen:.1f} mm | PETG, 0.4 mm nozzle, 0.20 mm layers, 100% infill | flat base down'+(' | local support: snap beams' if n=='stake_cell_holder' else ' | no supports'),
           az=-65,el=30,size=(1600,1000))
