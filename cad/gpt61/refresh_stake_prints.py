"""Rebuild only optional stake parts; preserve the verified flight geometry."""
import sys,json
sys.dont_write_bytecode=True
import cadquery as cq
import printed as pr
from build import load_cache,cache,mass_report,print_transform,assembly,OUT,RENDERS
from parameters import *
from geometry import box
from variants import stake_rows,render_variants
from render_local import render
from verify import verify
p=load_cache();p['stake_cell_holder']=pr.stake_cell_holder()
cache(p);mass_report(p);verify(p)
manifest=json.loads((OUT/'print_manifest.json').read_text())
for n in ('stake_adapter','stake_cell_holder'):
 s=p[n];ps=print_transform(n,s);b=ps.BoundingBox()
 cq.exporters.export(s,str(OUT/(n+'.step')),tolerance=.05,angularTolerance=.12)
 cq.exporters.export(ps,str(OUT/(n+'.stl')),tolerance=.05,angularTolerance=.12)
 row=next(r for r in manifest if r['part']==n);row['print_bbox_mm']=[b.xlen,b.ylen,b.zlen]
 render([(ps,'body'),(box(b.xlen+12,b.ylen+12,.6,at=(0,0,-.6)),'white')],RENDERS/f'print_{n}.png',f'Print orientation - {n.replace("_"," ")}',
        f'{b.xlen:.1f} x {b.ylen:.1f} x {b.zlen:.1f} mm | PETG,0.4 mm nozzle,0.2 mm layers,100% infill | flat base down'+(' | local support: snap beams' if n=='stake_cell_holder' else ' | no supports'),az=-65,el=30,size=(1600,1000))
(OUT/'print_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
assembly(stake_rows(p),'Stake_listener',OUT/'stake_assembled.step')
render_variants(p)
print('Optional stake parts and reports refreshed; flight parts unchanged.',flush=True)
