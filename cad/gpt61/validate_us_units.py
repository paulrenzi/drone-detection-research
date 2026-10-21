"""Validate US presentation against the current, deliberately revised model.

The prior revision's immutable-geometry comparisons are archived in tmp;
the tail-fin revision is expected to change geometry, masses and machine data.
"""
from pathlib import Path
import datetime,hashlib,json,re
from PIL import Image
R=Path(__file__).resolve().parent
def read(n):return json.loads((R/n).read_text(encoding='utf-8'))
checks=read('out/checks.json');assert not checks['failed']
ex=read('out/export_validation.json');assert len(ex['printed'])==14 and all(r['passed'] for r in ex['printed'])
pngs=sorted((R/'renders').glob('*.png'))
records={p.stem:json.loads(p.read_text(encoding='utf-8')) for p in (R/'tmp/us-caption-records').glob('*.json')}
assert len(pngs)==38 and {p.stem for p in pngs}<=set(records)
results=[]
for p in pngs:
    rec=records[p.stem];assert rec['text_fits']
    with Image.open(p) as im:assert list(im.size)==rec['size']
    strings=[rec['title'],rec['subtitle']]+[r['text'] for r in rec['labels']]
    for s in strings:
        allowed=s.replace('0.4 mm nozzle (0.016 in)','').replace('0.20 mm layers (0.008 in)','')
        assert not re.search(r'\b(?:mm|cm|kg|MPa)\b|\d\s*(?:g|N|°C)\b',allowed),(p.name,s)
        assert '\ufffd' not in s
    for i,a in enumerate(rec['text_boxes']):
        assert a[0]>=0 and a[1]>=0 and a[2]<rec['size'][0] and a[3]<rec['size'][1]
        for b in rec['text_boxes'][i+1:]:
            assert min(a[2],b[2])<=max(a[0],b[0]) or min(a[3],b[3])<=max(a[1],b[1]),(p.name,'label overlap',a,b)
    results.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size=rec['size'],text_fits=True,labels_do_not_overlap=True))
m=read('out/mass_properties.json');a=read('out/tail_analysis.json')
assert f"{m['dummy']['ballast_total_g']/28.349523125:.2f} oz" in records['dummy_ballast_detail']['subtitle']
assert f"{m['dart_cg_mm'][0]/25.4:.3f} in" in json.dumps(records['dart_balance'])
assert f"{a['after']['minimum']['cp_x_mm']/25.4:.3f} in" in json.dumps(records['dart_balance'])
for row in read('out/print_manifest.json'):
    dims=[v/25.4 for v in row['print_bbox_mm']]
    expected=' x '.join(f'{v:.{3 if abs(v)<.1 else 2}f}' for v in dims)+' in'
    assert records['print_'+row['part']]['subtitle'].startswith(expected),(row['part'],expected)
docs={n:(R/n).read_text(encoding='utf-8') for n in ('DESIGN.md','README.md','web/README.md','REVIEW.html','out/checks.md')}
for name,s in docs.items():
    assert '\ufffd' not in s,name
    if name=='DESIGN.md':
        s=s[:s.index('## Primary source register')]+s[s.index('## Pod, wiring and service'):]
        s=re.sub(r'\([\d.]+ g/cm³\)','',s)
    s=s.replace('0.4 mm nozzle (0.016 in)','').replace('0.20 mm layers (0.008 in)','')
    if name=='out/checks.md':s=s.replace('3g','three times gravity')
    assert not re.search(r'\d\s*(?:mm|cm|kg|g|N|MPa|°C)\b',s),(name,'unconverted measurement')
    assert not re.search(r'\b(?:mic|hanger|same|nominal|to|The|the|PETG)[0-9]',s),(name,'joined number')
report=dict(pass_=True,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),geometry_checks=len(checks['checks']),printed_export_checks=14,
    render_count=len(pngs),documents=list(docs),renders=results,
    scope='Current finned model: US captions/documents, caption bounds and overlap, model-linked balance/pressure/ballast/print dimensions. SI machine field names and units retained; numeric values recomputed for changed geometry. Human inspection is separately attested in visual_review.json.')
(R/'out/us_units_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:',len(pngs),'current US render/layout records;',len(checks['checks']),'geometry checks; 14 print exports; five human documents.')
