"""Download the original reference assets; writes only beside this script."""
from pathlib import Path
import urllib.request, hashlib, json

ROOT = Path(__file__).resolve().parent
FILES = {
    'inmp441.pdf': 'https://arduino.ua/files/INMP441.PDF',
    'ruthex-m2x4.step': 'https://cdn.shopify.com/s/files/1/0567/7019/9760/files/ruthex_RX-M2x4.step?v=1621264078',
    '3m5490.pdf': 'https://multimedia.3m.com/mws/media/2522949O/3m-ptfe-extruded-film-tape-5490.pdf?fn=3M-PTFE-Extruded-Film-Tape-5490.pdf',
    'x500v2-frame.step': 'https://2367252986-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FLIgtGDAvVGkCKGOJb1bR%2Fuploads%2F8i7OGwxNrtr6nOP4BgQ0%2Fx500v2-frame.step?alt=media&token=c06776fd-bd31-40e5-aaa3-9fb56c6ccf5a',
    'X500MotorSpec.png': 'https://cdn.shopify.com/s/files/1/0604/5905/7341/files/X500MotorSpec.png?v=1678791632',
    'X500-assembly.pdf': 'https://cdn.shopifycdn.net/s/files/1/0604/5905/7341/files/X500_V2_Assembly_Guide_en.pdf?v=1720853913',
    'samsung-25r.pdf': 'https://files.dcpower.eu/datasheets/samsung/INR18650-25R-datasheet.pdf',
}

def main():
    dest = ROOT/'sources'
    dest.mkdir(exist_ok=True)
    manifest = []
    for name, url in FILES.items():
        p = dest/name
        if not p.exists():
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=90) as response:
                p.write_bytes(response.read())
        blob = p.read_bytes()
        manifest.append(dict(file=name,url=url,bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest()))
        print(name, len(blob), flush=True)
    (dest/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')

if __name__ == '__main__': main()
