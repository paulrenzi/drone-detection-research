"""Run with the CadQuery Python listed in BRIEF.md. Writes only in this folder.

  python build.py               build, export, validate and render everything
  python build.py --no-render   geometry, exports and automated checks only
  python build.py --render-only load cached generated B-reps and render

The single source of geometry is printed.py/purchased.py, never edited meshes.
"""
from pathlib import Path
import sys, json, math, argparse, time, csv
sys.dont_write_bytecode=True
import cadquery as cq
import printed as pr
import purchased as buy
from parameters import *
from geometry import *

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out'; RENDERS=ROOT/'renders'; CACHE=ROOT/'cache'
for p in (OUT,RENDERS,CACHE):p.mkdir(exist_ok=True)

def log(*args):print(*args,flush=True)

def moment(shape,mass):return dict(mass_g=mass,centroid_mm=list(shape.Center().toTuple()))

def mass_item(name,shape,density=None,mass=None,basis=''):
    m=shape.Volume()/1000*density if mass is None else mass
    return dict(name=name,volume_mm3=shape.Volume(),density_g_cm3=density,**moment(shape,m),basis=basis)

def mass_dart(body,parts):
    rows=[mass_item('body',body,M.petg_density,basis='100% infill, 4 walls, solid PETG')]
    for name in ('pod_shell','pod_lid'):
        rows.append(mass_item(name,parts[name],M.petg_density,basis='100% infill, thin walls solid'))
    rows.append(mass_item('fibreglass_rod',buy.rod(),M.rod_density,basis='MEASURE composite density'))
    cs=compound(s for _,s,_ in buy.cell())
    rows.append(mass_item('Samsung25R_cell',cs,mass=M.cell_mass,basis='Samsung max45g, MEASURE actual'))
    hs=compound(s for _,s,_ in parts['board'])
    rows.append(mass_item('Heltec_with_OLED',hs,mass=M.board_mass,basis='MEASURE9g; OEM CAD spatial distribution proxy'))
    mic=compound(s for _,s,_ in parts['mic'])
    rows.append(mass_item('INMP441_breakout',mic,mass=M.mic_mass,basis='MEASURE1g; geometric centroid'))
    for n,s,c in parts['hardware']:
        if n in ('whip','whip_boot','RF_pigtail'):continue
        rho=8.5 if 'insert' in n else 7.85 if 'M2' in n else 8.9 if 'nickel' in n else .15 if 'foam' in n else 1.10 if 'seal' in n or 'film' in n else 1.45 if 'power_wire' in n else 1.14
        rows.append(mass_item(n,s,rho,basis='material-density model; wire1.45 composite, foam.15, silicone1.10'))
    whip=compound(s for n,s,c in parts['hardware'] if n in ('whip','whip_boot','RF_pigtail'))
    rows.append(mass_item('whip_and_pigtail',whip,mass=M.whip_mass,basis='MEASURE1.2g; envelope centroid'))
    return rows

def resultant(rows):
    m=sum(x['mass_g'] for x in rows)
    return m,[sum(x['mass_g']*x['centroid_mm'][j] for x in rows)/m for j in range(3)]

def make_model():
    parts={}
    for n,f in (('pod_shell',pr.pod_shell),('pod_lid',pr.pod_lid),('plate',pr.plate),('rotor',pr.rotor),('fit_coupon',pr.fit_coupon)):
        log('model',n);parts[n]=f()
    parts['board']=buy.heltec();parts['mic']=buy.microphone();parts['hardware']=buy.dart_hardware()
    # Fixed point: moving the integral hanger also moves its mass and sleeve.
    h=267.;hy=6.
    iterations=[]
    for k in range(12):
        b=pr.body(h,hy);rows=mass_dart(b,parts);m,cg=resultant(rows)
        iterations.append(dict(hanger=[h,hy],cg=cg[:2],mass=m))
        log('balance',k,round(h,3),round(cg[0],3),round(m,3))
        if max(abs(cg[0]-h),abs(cg[1]-hy))<.015:break
        h,hy=cg[:2]
    parts['body']=b;parts['hanger']=h;parts['hanger_y']=hy;parts['hanger_xy']=[h,hy,cg[2]];parts['dart_mass']=m;parts['dart_cg']=cg;parts['mass_rows']=rows;parts['balance_iterations']=iterations
    parts['servo']=buy.sg90()
    film=cyl(BEARING_RO-.3,BEARING_FILM_T,(0,0,BEARING_Z-BEARING_FILM_T)).cut(cyl(BEARING_RI+.3,BEARING_FILM_T+1,(0,0,BEARING_Z-BEARING_FILM_T-.1)))
    parts['bearing_film']=[('PTFE_bearing_film',film,'white')]
    log('import drone')
    # Individual B-reps are a faster lossless cache of the immutable OEM asset.
    meta=CACHE/'model.json'
    if meta.exists():
        old=json.loads(meta.read_text())
        parts['drone']=[(n,cq.Shape.importBrep(str(CACHE/f)),c) for n,f,c in old['drone']['parts']]
        parts['vendor_duplicates_removed']=old['vendor_duplicates_removed']
    else:parts['drone'],parts['vendor_duplicates_removed']=buy.drone()
    parts['rail_ties']=[]
    for x in SADDLE_X:
        for y in (-30,30):parts['rail_ties']+=buy.zip_tie_x(x,y,RAIL_AXIS+.5,14.8,14.4,name=f'rail_zip_{x}_{y}')
    return parts

def dart_rows(parts):
    return [('body',parts['body'],'body'),('pod_shell',parts['pod_shell'],'pod'),('pod_lid',parts['pod_lid'],'lid'),('rod',buy.rod(),'rod')]+buy.cell()+parts['board']+parts['mic']+parts['hardware']

def carried_transform(s,i,hanger,drop=0,pitch=0):
    h,hy,cz=hanger
    x,y,_=pr.head_positions()[i]
    shift=ROTOR_TOP-HEAD_BOTTOM
    if pitch:
        # Pitch about CG only after initial vertical translation has cleared
        # the plate. This is a prescribed clearance trajectory, not dynamics.
        s=s.rotate((h,hy,cz),(h,hy+1,cz),-pitch)
    return s.translate((x-h,y-hy,shift-drop))

def stood_transform(s):
    # Dart longitudinal +X becomes world +Z; its nose stop is at soil Z0.
    return s.rotate((0,0,0),(0,1,0),-90).translate((-ROD_Z,0,-BODY_X0))

def harness_rows(parts,angle=0):
    out=[('harness_plate',parts['plate'],'plate'),('release_rotor',parts['rotor'].rotate((0,0,0),(0,0,1),angle),'rotor')]
    for n,s,c in parts['servo']:
        if any(t in n for t in ('horn','spline_screw','drive_pin')):s=s.rotate((0,0,0),(0,0,1),angle)
        out.append((n,s,c))
    return out+parts['rail_ties']+parts['bearing_film']

def scene(parts,state='carried'):
    phi=16 if state=='mid_release' else 0
    rows=parts['drone']+harness_rows(parts,phi)
    for i in range(4):
        for n,s,c in dart_rows(parts):
            d=70 if state=='mid_release' and i==0 else 0
            rows.append((f'dart{i+1}_{n}',carried_transform(s,i,parts['hanger_xy'],d),c))
    return rows

def stood_scene(parts):
    # Full aircraft parked on its stock skids, with one listener in soil beside
    # it and three still carried. A geometric end state, not a landing sequence.
    rows=parts['drone']+harness_rows(parts,16)
    for i in (1,2,3):
        rows += [(f'dart{i+1}_{n}',carried_transform(s,i,parts['hanger_xy']),c) for n,s,c in dart_rows(parts)]
    rows=[(n,s.moved(cq.Location(cq.Vector(0,0,-GROUND_Z))),c) for n,s,c in rows]
    rows += [(f'stood_{n}',stood_transform(s).translate((650,0,0)),c) for n,s,c in dart_rows(parts)]
    rows.append(('soil_plane',box(1260,900,90,at=(250,0,-90)),'soil'))
    return rows

def print_transform(n,s):
    if n=='pod_lid':s=s.rotate((0,0,0),(1,0,0),180)
    elif n=='rotor':s=s.rotate((0,0,0),(1,0,0),180)
    b=s.BoundingBox()
    return s.translate((-(b.xmin+b.xmax)/2,-(b.ymin+b.ymax)/2,-b.zmin))

PRINT_NAMES=('body','pod_shell','pod_lid','plate','rotor','fit_coupon')

def cache(parts):
    serial={}
    for key,val in parts.items():
        if isinstance(val,cq.Shape):
            val.exportBrep(str(CACHE/(key+'.brep')));serial[key]={'shape':key+'.brep'}
        elif isinstance(val,list) and val and isinstance(val[0],tuple) and len(val[0])==3 and isinstance(val[0][1],cq.Shape):
            packed=[]
            for j,(n,s,c) in enumerate(val):
                filename=f'{key}_{j:03}.brep';s.exportBrep(str(CACHE/filename));packed.append([n,filename,c])
            serial[key]={'parts':packed}
        else:serial[key]=val
    (CACHE/'model.json').write_text(json.dumps(serial,indent=2))

def load_cache():
    data=json.loads((CACHE/'model.json').read_text())
    for k,v in list(data.items()):
        if isinstance(v,dict) and 'shape' in v:data[k]=cq.Shape.importBrep(str(CACHE/v['shape']))
        elif isinstance(v,dict) and 'parts' in v:data[k]=[(n,cq.Shape.importBrep(str(CACHE/f)),tuple(c) if isinstance(c,list) else c) for n,f,c in v['parts']]
    return data

def assembly(rows,name,path):
    from render_local import COLORS
    assy=cq.Assembly(name=name)
    for n,s,c in rows:
        rgb=COLORS.get(c,c) if isinstance(c,str) else c
        alpha=.17 if n.startswith('prop_swept') else 1
        assy.add(s,name=n,color=cq.Color(*rgb,alpha))
    assy.export(str(path),exportType='STEP')

def system_assembly(parts,state,path):
    # Shared dart subassembly with placement locations preserves CAD instances
    # instead of serializing four independently transformed electronic boards.
    from render_local import COLORS
    def group(rows,name):
        a=cq.Assembly(name=name)
        for n,s,c in rows:
            rgb=COLORS.get(c,c) if isinstance(c,str) else c
            a.add(s,name=n,color=cq.Color(*rgb,.17 if n.startswith('prop_swept') else 1))
        return a
    root=cq.Assembly(name='Tripwire_'+state)
    air_z=-GROUND_Z if state=='stood' else 0.
    phi=16 if state in ('stood','mid_release') else 0.
    craft=group(parts['drone']+harness_rows(parts,phi),'carrier')
    root.add(craft,name='X500_harness',loc=cq.Location(cq.Vector(0,0,air_z)))
    base=group(dart_rows(parts),'listener')
    for i,(x,y,t) in enumerate(pr.head_positions()):
        if state=='stood' and i==0:
            loc=cq.Location(cq.Vector(650-ROD_Z,0,-BODY_X0),cq.Vector(0,1,0),-90)
        else:
            drop=70 if state=='mid_release' and i==0 else 0
            loc=cq.Location(cq.Vector(x-parts['hanger'],y-parts['hanger_y'],ROTOR_TOP-HEAD_BOTTOM-drop+air_z))
        root.add(base,name=f'listener_{i+1}',loc=loc)
    if state=='stood':root.add(box(1260,900,90,at=(250,0,-90)),name='soil',color=cq.Color(*COLORS['soil']))
    root.export(str(path),exportType='STEP')

def export_all(parts):
    manifest=[]
    for n in PRINT_NAMES:
        s=parts[n]
        log('export',n)
        for ext in ('step','stl'):
            # STEP retains assembly datum, STL is already in print orientation.
            obj=s if ext=='step' else print_transform(n,s)
            cq.exporters.export(obj,str(OUT/(n+'.'+ext)),tolerance=.05,angularTolerance=.12)
        manifest.append(dict(part=n,quantity=4 if n in ('body','pod_shell','pod_lid') else 1,step=n+'.step',stl=n+'.stl',print_bbox_mm=[print_transform(n,s).BoundingBox().xlen,print_transform(n,s).BoundingBox().ylen,print_transform(n,s).BoundingBox().zlen]))
    log('export bought parts')
    assembly(parts['board'],'Heltec_V3_reference',OUT/'bought_heltec_v3.step')
    assembly(parts['mic'],'INMP441_breakout',OUT/'bought_inmp441.step')
    assembly(parts['servo'],'SG90_with_horn',OUT/'bought_SG90.step')
    assembly(buy.cell(),'Samsung25R',OUT/'bought_18650.step')
    cq.exporters.export(buy.rod(),str(OUT/'bought_rod.step'))
    assembly(parts['drone'],'Holybro_X500_V2',OUT/'bought_x500.step')
    log('export full carried assembly')
    system_assembly(parts,'carried',OUT/'assembly_carried.step')
    log('export mid-release assembly')
    system_assembly(parts,'mid_release',OUT/'assembly_mid_release.step')
    stand=[(n,stood_transform(s),c) for n,s,c in dart_rows(parts)]
    assembly(stand,'Dart_in_soil',OUT/'dart_stood.step')
    system_assembly(parts,'stood',OUT/'assembly_stood.step')
    (OUT/'print_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

def mass_report(parts):
    rows=parts['mass_rows']
    harness=[mass_item(n,parts[n],M.petg_density,basis='100% infill PETG') for n in ('plate','rotor')]
    stock_names=('SG90_case_tabs','SG90_output_spline','SG90_stock_double_horn')
    sc=compound(s for n,s,c in parts['servo'] if n in stock_names)
    harness.append(mass_item('SG90_with_stock_horn',sc,mass=9.0,basis='S3 rated9g; model external centroid'))
    for n,s,c in parts['servo']+parts['rail_ties']+parts['bearing_film']:
        if n in stock_names:continue
        harness.append(mass_item(n,s,2.2 if 'PTFE' in n else 1.14 if n.startswith('rail_zip') else 1.45 if 'lead' in n else 1.2 if 'plug' in n else 7.85,basis='modeled hardware density'))
    hm,hc=resultant(harness)
    data=dict(dart=rows,dart_total_g=parts['dart_mass'],dart_cg_mm=parts['dart_cg'],hanger_x_mm=parts['hanger'],hanger_y_mm=parts['hanger_y'],balance_residual_mm=parts['dart_cg'][0]-parts['hanger'],harness=harness,harness_total_g=hm,harness_cg_mm=hc,carried_payload_g=hm+4*parts['dart_mass'],infill='100% in all prototype parts; four 0.4mm walls and six top/bottom layers; no global density multiplier',balance_iterations=parts['balance_iterations'])
    (OUT/'mass_properties.json').write_text(json.dumps(data,indent=2)+'\n')
    with (OUT/'mass_properties.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['assembly','part','mass_g','centroid_x_mm','centroid_y_mm','centroid_z_mm','CAD_volume_mm3','basis'])
        for group,it in [('dart',rows),('harness',harness)]:
            for r in it:writer.writerow([group,r['name'],r['mass_g'],*r['centroid_mm'],r['volume_mm3'],r['basis']])
    return data

def render_all(parts):
    from render_local import render
    def rend(rows,name,title,subtitle='',**kw):
        # Opaque pod exteriors hide electronics in the full-aircraft views.
        # Skipping buried objects changes no visible surfaces and keeps QA fast.
        if name.startswith('assembly_') or name=='dart_stood.png':
            hidden=('heltec','oled','header_pad','mic_pcb','INMP441','mic_pad','pod_insert','pod_M2','perimeter','mic_water','mic_silicone','retention_foam','RF_pigtail')
            rows=[r for r in rows if not any(k in r[0] for k in hidden)]
        render([(s,c,.16) if n.startswith('prop_swept') else (s,c) for n,s,c in rows],RENDERS/name,title,subtitle,**kw)
    rend(scene(parts),'assembly_carried.png','Four listeners on the Holybro X500 V2','Manufacturer frame CAD | 260 mm prop sweeps | carried state',az=-56,el=17,size=(1800,1200))
    rend(scene(parts,'mid_release'),'assembly_mid_release.png','Release 1 of 4 - rotor at 16 degrees','First dart translated 70 mm down; three still carried | geometric state, not flight simulation',az=-56,el=12,size=(1800,1200))
    rend(stood_scene(parts),'assembly_stood.png','One listener in soil, three on the carrier','Full stood state | stock skids on ground | listener placed beside aircraft for clearance review',az=-58,el=17,size=(1900,1200))
    close=harness_rows(parts,16)
    for i in range(4):
        for n in ('body',):
            sh=carried_transform(parts[n],i,parts['hanger_xy'],25 if i==0 else 0)
            # Crop body at the hanger to make load path and open gap visible.
            x,y,_=pr.head_positions()[i]
            sh=sh.intersect(box(48,30,85,at=(x,y,-50)))
            close.append((f'hanger_{i}',sh,'body'))
    rend(close,'release_detail.png','Rim, heads, bearing ridge and SG90 drive','The four heads pass through clearance slots; the inner bearing ring carries the vertical load',az=-62,el=55,size=(1500,1100))
    stand=[(n,stood_transform(s),c) for n,s,c in dart_rows(parts)]
    soil=box(155,155,12,at=(0,0,-12))
    rend(stand+[('ground',soil,'soil')],'dart_stood.png','Listener seated to its soil stop',f'{POD_X1+M.whip_l:.0f} mm overall | mic {MIC_X-BODY_X0:.0f} mm above soil | tip buried 70 mm',az=-135,el=8,size=(850,1600))
    # A real half-space boolean section along cell/rod length, with the cell
    # omitted in one view so that the floor/wall/press-fit features are legible.
    bodyrows=[('body',parts['body'],'body'),('rod',buy.rod(),'rod')]+buy.cell()
    crop=box(250,50,90,at=((70+parts['hanger']+25)/2,4,-2))
    cut=box(300,60,100,at=(180,CELL_Y-30,-10))
    sec=[(n,s.intersect(crop).intersect(cut),c) for n,s,c in bodyrows if n in ('body','rod')]
    rend(sec,'section_body.png','Body longitudinal cutaway - cell omitted','Cut through the cell axis | thin saddle, relieved snap fingers, end stops and rod sleeve',az=70,el=25,size=(1600,900))
    # Transverse section of the cell at the flexible latch's free end.
    slab=box(3.0,45,30,at=(104.5,12,-2))
    rend([(n,s.intersect(slab),c) for n,s,c in bodyrows],'section_body_snap.png','Cell retention - transverse detail','16.8 mm throat | 18 mm cantilever | lead-in ramp and undercut | cell rests in a 1.6 mm saddle',az=-12,el=12,size=(1200,950))
    # Pod section across the front side, retaining the board and membrane.
    podrows=[('pod_shell',parts['pod_shell'],'pod'),('pod_lid',parts['pod_lid'],'lid')]+parts['board']+parts['mic']+[r for r in parts['hardware'] if 'pod_' in r[0] or 'mic_' in r[0] or 'perimeter' in r[0]]
    half=box(100,40,40,at=(520,-20,-10))
    rend([(n,s.intersect(half),c) for n,s,c in podrows],'section_pod.png','Pod longitudinal section - serviceable electronics','Silicone cord seal, heat-set bosses, edge supports, OLED and side-facing bottom-port microphone',az=70,el=22,size=(1600,1100))
    # Exploded service assembly exposes the features hidden in the section.
    exploded=[('pod_shell',parts['pod_shell'],'pod')]+parts['board']+parts['mic']
    exploded.append(('pod_lid',parts['pod_lid'].translate((0,0,32)),'lid'))
    rend(exploded,'pod_exploded.png','Pod service assembly','Four M2x6 screws and heat-set inserts | lid pads retain PCB | weather membrane behind rain hood',az=-60,el=32,size=(1600,1150))
    for n in PRINT_NAMES:
        s=print_transform(n,parts[n]);bb=s.BoundingBox();bed=box(bb.xlen+12,bb.ylen+12,.6,at=(0,0,-.6))
        sub=f'{bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm | PETG, 0.4 mm nozzle, 0.2 mm layers, 100% infill'
        if n=='body':sub+=' | local support: hanger flange + 4 snap beams'
        elif n=='pod_shell':sub+=' | local support: hood, socket lip, mic-guide ledges'
        else:sub+=' | no supports'
        rend([(n,s,'body' if n in ('body','fit_coupon') else 'pod' if 'pod' in n else 'plate' if n=='plate' else 'rotor'),('build_surface',bed,'white')],f'print_{n}.png',f'Print orientation - {n.replace("_"," ")}',sub,az=-65,el=30,size=(1600,1000))
    # Bought-part board detail is colored to expose real vendor components.
    rend(parts['board'],'bought_heltec.png','Heltec WiFi LoRa 32 V3 - mechanical reference','Official V3.7 populated PCB + OLED stack | two 18-way header pad rows left unpopulated',az=-58,el=35,size=(1500,1000))
    rend(parts['servo'],'bought_servo.png','TowerPro SG90 and supplied double horn','Case, tabs, grooves on the output spline, fixing nuts and two axial sliding drive pins',az=-65,el=28,size=(1300,1100))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--no-render',action='store_true');ap.add_argument('--render-only',action='store_true');ap.add_argument('--geometry-only',action='store_true');ap.add_argument('--exports-only',action='store_true');ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    start=time.time()
    parts=load_cache() if args.render_only or args.exports_only or args.verify_only else make_model()
    if args.exports_only:export_all(parts);return
    if args.verify_only:
        from verify import verify
        verify(parts);return
    if not args.render_only:
        cache(parts);mass_report(parts)
        if not args.geometry_only:export_all(parts)
        from verify import verify
        verify(parts)
    if not args.no_render:render_all(parts)
    log('DONE',round(time.time()-start,1),'seconds; dart',round(parts['dart_mass'],2),'g; hanger',round(parts['hanger'],2),'mm')

if __name__=='__main__':main()
