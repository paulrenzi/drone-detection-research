from pathlib import Path
import sys
sys.dont_write_bytecode=True
import cadquery as cq
from render_local import render
ROOT=Path(__file__).resolve().parent
out=ROOT/'renders';out.mkdir(exist_ok=True)
for name in ('x500v2-frame','heltec-v3-non-exact'):
    cache=ROOT/'sources'/(name+'.brep')
    if cache.exists():s=cq.Shape.importBrep(str(cache))
    else:
        s=cq.importers.importStep(str(ROOT/'sources'/(name+'.step'))).val()
        s.exportBrep(str(cache))
    render([(s,'carbon' if 'x500' in name else 'board')],out/(name+'-source.png'),name,'Manufacturer reference CAD, before placement',az=-56,el=25)
