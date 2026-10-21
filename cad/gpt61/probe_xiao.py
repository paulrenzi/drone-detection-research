from pathlib import Path
import sys,json,re,html
sys.dont_write_bytecode=True
import cadquery as cq
R=Path(__file__).resolve().parent
for stem,file in [('xiao','xiao-oem/XIAO-ESP32S3 v2.step'),('wio','wio-oem/Wio-SX1262_for_XIAO_3D_file.step')]:
 s=cq.importers.importStep(str(R/'sources'/file)).val()
 rows=[]
 for i,a in enumerate(s.Solids()):
  b=a.BoundingBox();rows.append(dict(i=i,v=round(a.Volume(),3),bounds=[round(x,4) for x in (b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax)]))
 print(stem,'solids',len(rows),'bounds',s.BoundingBox().__dict__,'largest',sorted(rows,key=lambda r:-r['v'])[:15])
 (R/'sources'/f'{stem}-cad-inspection.json').write_text(json.dumps(rows,indent=2))
 s.exportBrep(str(R/'sources'/f'{stem}-oem.brep'))
txt=(R/'sources/xiao-kit-page.html').read_text(encoding='utf-8')
for match in re.finditer(r"<input[^>]+value='(.*?)'",txt,re.S):
 try:obj=json.loads(html.unescape(match[1]))
 except Exception:continue
 if 'product_feature_description' in obj:
  text='\n'.join(str(v) for v in obj.values());text=html.unescape(re.sub('<[^>]+>',' ',text))
  (R/'sources/xiao-kit-description.txt').write_text(text,encoding='utf-8')
  for line in text.splitlines():
   if re.search('antenna|FPC|mm',line,re.I):print(line[:2000])
