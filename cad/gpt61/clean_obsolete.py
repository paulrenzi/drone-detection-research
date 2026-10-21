"""Prune only obsolete generated artifacts inside this exact package."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
def remove(p):
 p=p.resolve();assert R in p.parents and p.is_file();p.unlink();print('Removed',p.relative_to(R))
for rel in ('out/bought_heltec_v3.step','renders/bought_heltec.png'):
 p=R/rel
 if p.exists():remove(p)
d=json.loads((R/'cache/model.json').read_text());used={'model.json'}
for v in d.values():
 if isinstance(v,dict) and 'shape' in v:used.add(v['shape'])
 if isinstance(v,dict) and 'parts' in v:used.update(row[1] for row in v['parts'])
for p in (R/'cache').glob('*.brep'):
 if p.name not in used:remove(p)
