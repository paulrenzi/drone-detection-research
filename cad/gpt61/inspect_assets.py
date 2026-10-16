from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
import cadquery as cq
ROOT = Path(__file__).resolve().parent
for f in ('x500v2-frame.step','heltec-v3-non-exact.step'):
    print('IMPORT', f, flush=True)
    s=cq.importers.importStep(str(ROOT/'sources'/f)).val()
    rows=[]
    for i,so in enumerate(s.Solids()):
        b=so.BoundingBox(); c=so.Center()
        rows.append(dict(i=i,volume=round(so.Volume(),3),bbox=[round(v,3) for v in (b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax)],center=[round(v,3) for v in c.toTuple()]))
    (ROOT/'sources'/(f+'.solids.json')).write_text(json.dumps(rows,indent=2))
    print('solids',len(rows),'bounds',s.BoundingBox().__dict__,flush=True)
    for row in rows:
        if row['volume']>500 or f.startswith('heltec'): print(row,flush=True)
