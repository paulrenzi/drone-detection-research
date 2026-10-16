from pathlib import Path
import sys, urllib.request, re
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'vendor'))
import pymupdf as pdf
for file,page in [('heltec-v3-datasheet.pdf',13),('inmp441.pdf',18)]:
    doc=pdf.open(ROOT/'sources'/file)
    print(file,len(doc),'pages',flush=True)
    doc[page].get_pixmap(matrix=pdf.Matrix(1.6,1.6)).save(ROOT/'sources'/(file+'-drawing.png'))
url='https://towerpro.com.tw/product/sg90-7/'
html=urllib.request.urlopen(url).read().decode('utf-8')
(ROOT/'sources'/'towerpro-page.html').write_text(html,encoding='utf-8')
links=list(dict.fromkeys(re.findall(r'(?:src|href)=["\']([^"\']+)',html)))
for link in links:
    if ('sg90' in link.lower() or 'configure' in link.lower()) and any(link.lower().endswith(x) for x in ('.jpg','.png','.jpeg','.pdf')):
        print(link,flush=True)
        name=link.split('/')[-1]
        data=urllib.request.urlopen(link).read()
        (ROOT/'sources'/name).write_bytes(data)
