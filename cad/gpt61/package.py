"""Make a compact printing handoff and a final local receipt."""
from pathlib import Path
import json, hashlib, zipfile, datetime
ROOT=Path(__file__).resolve().parent
out=ROOT/'out'
paths=list(out.glob('*.stl'))+[out/'print_manifest.json',ROOT/'DESIGN.md',out/'mass_properties.csv',out/'checks.md']
with zipfile.ZipFile(out/'print-kit.zip','w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for p in paths:z.write(p,p.name)
records=[]
for p in sorted(ROOT.glob('*.py'))+sorted((ROOT/'renders').glob('*.png'))+list(out.glob('*.stl')):
    records.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
checks=json.loads((out/'checks.json').read_text())
mass=json.loads((out/'mass_properties.json').read_text())
receipt=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),cadquery='2.8.0',vtk='9.6.2',geometry_checks=len(checks['checks']),failed=checks['failed'],printed_exports_verified=json.loads((out/'export_validation.json').read_text())['printed'],dart_g=mass['dart_total_g'],harness_g=mass['harness_total_g'],scope='cad/gpt61 only; no commit/push; no physical qualification',files=records)
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('print-kit.zip', (out/'print-kit.zip').stat().st_size,'bytes; receipt.json written')
