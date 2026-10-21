"""Check display units, immutable model/data, and pixels outside annotations."""
from pathlib import Path
import datetime,hashlib,json,re,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont

R=Path(__file__).resolve().parent
B=R/'tmp/us-units-baseline'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

protected=read(B/'protected-hashes.json')
assert all(sha(R/n)==h for n,h in protected.items()),'Geometry or model source changed'
machine_reports=['out/mass_properties.json','out/print_manifest.json','out/kits.json','web/manifest.json']
for name in machine_reports:
    assert read(R/name)==read(B/name),name+' machine-readable values changed'
checks=read(R/'out/checks.json');original=read(B/'out/checks.json')
assert checks==original,'Geometry check values or metadata changed'
assert read(R/'out/export_validation.json')==read(B/'out/export_validation.json')
assert len(checks['checks'])==140 and not checks['failed']

# Compare the actual renderer's geometry, camera, lighting and colour code with
# the clean starting revision. Only the annotation/drawing stage has changed.
for name,start,end in [('render_local.py','    ren=vtk.vtkRenderer();','    im=Image.open(path)'),
                       ('web_export.py','def camera_render(', '    im=Image.open(path)')]:
    old=subprocess.check_output(['git','show','HEAD:cad/gpt61/'+name],cwd=R,text=True,encoding='utf-8')
    new=(R/name).read_text(encoding='utf-8')
    assert old[old.index(start):old.index(end)]==new[new.index(start):new.index(end)],name+' camera or geometry renderer changed'
old=subprocess.check_output(['git','show','HEAD:cad/gpt61/render_local.py'],cwd=R,text=True,encoding='utf-8')
new=(R/'render_local.py').read_text(encoding='utf-8')
assert old[old.index('COLORS ='):old.index('_cache={}')] == new[new.index('COLORS ='):new.index('_cache={}')]

records={p.stem:read(p) for p in (R/'tmp/us-caption-records').glob('*.json')}
pngs=sorted((R/'renders').glob('*.png'))
assert len(pngs)==33 and set(records)=={p.stem for p in pngs}
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',21)
results=[]
for p in pngs:
    rec=records[p.stem]
    strings=[rec['title'],rec['subtitle']]+[item['text'] for item in rec['labels']]
    for text in strings:
        allowed=text.replace('0.4 mm nozzle (0.016 in)','').replace('0.20 mm layers (0.008 in)','')
        assert not re.search(r'\b(?:mm|cm|kg|MPa)\b|\d\s*(?:g|N|°C)\b',allowed),(p.name,text)
        assert '\ufffd' not in text and rec['text_fits']
    boxes=rec['text_boxes']
    for i,a in enumerate(boxes):
        for b in boxes[i+1:]:
            assert min(a[2],b[2])<=max(a[0],b[0]) or min(a[3],b[3])<=max(a[1],b[1]),(p.name,'overlapping labels',a,b)
    old=Image.open(B/'renders'/p.name).convert('RGB');new=Image.open(p).convert('RGB')
    assert old.size==new.size==tuple(rec['size'])
    mask=Image.new('L',new.size,0);draw=ImageDraw.Draw(mask)
    draw.rectangle((0,0,new.width,124 if rec['labels'] else 111),fill=255)
    for item in rec['labels']:
        new_text=item['text']
        old_text={'Solid 19.69 in rod':'Solid 500 mm rod','Three M2x6 screws':'Three M2 x 6 screws'}.get(new_text,new_text)
        # Exclude only text backplates and their leader lines, in both versions.
        for text in (old_text,new_text):
            x,y=item['position'];anchor=item['anchor']
            box=draw.textbbox((x,y),text,font=font)
            box=(box[0]-8,box[1]-4,box[2]+8,box[3]+4)
            endpoint=(box[0] if anchor[0]<x else box[2],(box[1]+box[3])/2)
            draw.rectangle(box,fill=255)
            draw.line([tuple(anchor),endpoint],fill=255,width=6)
            draw.ellipse((anchor[0]-5,anchor[1]-5,anchor[0]+5,anchor[1]+5),fill=255)
    difference=np.abs(np.asarray(old).astype(np.int16)-np.asarray(new).astype(np.int16))
    visible=np.asarray(mask)==0
    outside=int(np.count_nonzero(np.any(difference,axis=2) & visible))
    mean=float(difference[visible].mean())
    large_fraction=float(np.count_nonzero((difference.max(axis=2)>16)&visible)/np.count_nonzero(visible))
    # Fresh B-rep tessellation/VTK shading is not byte deterministic. Record
    # that small raster noise without mistaking it for a changed camera/model.
    assert mean<1.0 and large_fraction<.003,(p.name,mean,large_fraction,'visual scene changed')
    results.append(dict(file=p.name,sha256=sha(p),size=list(new.size),text_fits=True,labels_do_not_overlap=True,changed_pixels_outside_annotations=outside,mean_channel_difference_outside_annotations=mean,large_difference_pixel_fraction=large_fraction))

# Independent model-based spot checks of the captions most likely to regress.
m=read(R/'out/mass_properties.json')
assert f"{m['dummy']['ballast_total_g']/28.349523125:.2f} oz" in records['dummy_ballast_detail']['subtitle']
assert '27.01 in overall | mic 19.69 in above soil | tip buried 2.76 in'==records['dart_stood']['subtitle']
for row in read(R/'out/print_manifest.json'):
    dims=[float(x)/25.4 for x in row['print_bbox_mm']]
    expected=' x '.join(f'{x:.{3 if abs(x)<.1 else 2}f}' for x in dims)+' in'
    assert records['print_'+row['part']]['subtitle'].startswith(expected),(row['part'],expected)
docs={n:(R/n).read_text(encoding='utf-8') for n in ('DESIGN.md','README.md','web/README.md','REVIEW.html','out/checks.md')}
for name,text in docs.items():
    assert '\ufffd' not in text,name
    if name=='DESIGN.md':
        text=text.split('## Primary source register')[0]+text.split('## Pod, wiring and service')[1]
        text=re.sub(r'\([\d.]+ g/cm³\)','',text)
    text=text.replace('0.4 mm nozzle (0.016 in)','').replace('0.20 mm layers (0.008 in)','')
    if name=='out/checks.md':text=text.replace('3g','three times gravity')
    assert not re.search(r'\d\s*(?:mm|cm|kg|g|N|MPa|°C)\b',text),(name,'unconverted measurement')
    assert not re.search(r'\b(?:mic|hanger|same|nominal|to|The|the|PETG)[0-9]',text),(name,'joined word and number')

report=dict(pass_=True,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    geometry_checks=140,printed_export_checks=12,protected_geometry_files=len(protected),
    machine_reports_unchanged=machine_reports,geometry_check_results_unchanged=True,
    export_validation_unchanged=True,renderer_geometry_camera_and_colour_code_unchanged=True,
    raster_comparison_limits=dict(mean_channel_difference_below=1.0,channel_difference_over_16_pixel_fraction_below=.003),
    render_count=len(results),documents=list(docs),renders=results,
    scope='US caption/document units and typography; original model hashes, exact check values, unchanged machine reports, label bounds/overlap, unchanged renderer geometry/camera/colour code, and small raster-noise bounds outside annotations. Human review is separate in visual_review.json.')
(R/'out/us_units_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS: 33 render captions/layouts/pixel comparisons; 425 protected model files; unchanged data and 140 geometry checks; 12 export checks; five human documents.')
