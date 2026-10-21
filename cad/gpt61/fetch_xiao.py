"""Fetch primary Seeed mechanical references, confined to this package."""
from pathlib import Path
import urllib.request, json, hashlib, zipfile, subprocess
ROOT=Path(__file__).resolve().parent
S=ROOT/'sources'; S.mkdir(exist_ok=True)
URLS={
 'xiao-3d.zip':'https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/seeed-studio-xiao-esp32s3-3d_model.zip',
 'wio-xiao-3d.rar':'https://files.seeedstudio.com/products/SenseCAP/Wio_SX1262/Wio-SX1262_for_XIAO_3D_file.rar',
 'xiao-dimensions.dxf':'https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_v1.1_Dimensioning.dxf',
 'wio-schematic.pdf':'https://files.seeedstudio.com/products/SenseCAP/Wio_SX1262/Schematic_Diagram_Wio-SX1262_for_XIAO.pdf',
 'wio-datasheet.pdf':'https://files.seeedstudio.com/products/SenseCAP/Wio_SX1262/Wio-SX1262_Module_Datasheet.pdf',
 'xiao-schematic.pdf':'https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_SCH_v1.2.pdf',
 'xiao-kit-page.html':'https://www.seeedstudio.com/Wio-SX1262-with-XIAO-ESP32S3-p-5982.html',
}
def main():
    rows=[]
    for name,url in URLS.items():
        p=S/name
        if not p.exists():
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=90) as r:p.write_bytes(r.read())
        rows.append(dict(file=name,url=url,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
        print(name,p.stat().st_size,flush=True)
    (S/'xiao-manifest.json').write_text(json.dumps(rows,indent=2))
    d=S/'xiao-oem';d.mkdir(exist_ok=True)
    with zipfile.ZipFile(S/'xiao-3d.zip') as z:z.extractall(d)
    d=S/'wio-oem';d.mkdir(exist_ok=True)
    subprocess.run(['tar','-xf',str(S/'wio-xiao-3d.rar'),'-C',str(d)],check=True)
    import cadquery as cq
    for stem,file in [('xiao','xiao-oem/XIAO-ESP32S3 v2.step'),('wio','wio-oem/Wio-SX1262_for_XIAO_3D_file.step')]:
        cq.importers.importStep(str(S/file)).val().exportBrep(str(S/f'{stem}-oem.brep'))
if __name__=='__main__':main()
