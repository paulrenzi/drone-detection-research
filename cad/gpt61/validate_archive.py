"""Check that the final print archive contains the current validated parts."""
from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parent;O=R/'out';path=O/'print-kit.zip'
pm=json.loads((O/'print_manifest.json').read_text())
with zipfile.ZipFile(path) as z:
 assert z.testzip() is None
 for row in pm:
  for ext in ('step','stl'):assert z.read(row[ext])==(O/row[ext]).read_bytes(),row[ext]
 assert z.read('DESIGN.md')==(R/'DESIGN.md').read_bytes()
 assert z.read('kits.json')==(O/'kits.json').read_bytes()
 count=len(z.namelist())
report=dict(pass_=True,file=path.name,size_bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),entries=count,printed_STEP_STL_pairs=len(pm),scope='Archive CRC and byte-for-byte comparison with current validated parts, DESIGN.md and kit quantities')
(O/'archive_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
