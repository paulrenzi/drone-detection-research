"""Reproducible broadside silhouette estimate, wind arithmetic and CAD figures.

Uniform pressure on a projected silhouette is a deliberately simple estimate,
not a small-angle aerodynamic derivative or a time-domain fall simulation.
"""
from pathlib import Path
import json,math
import numpy as np
import cadquery as cq
from PIL import Image,ImageDraw,ImageFont
from parameters import *
from geometry import *
from display_units import length,mass,inch
R=Path(__file__).resolve().parent

def solve_unfinned(p):
    from build import mass_dart,resultant
    import printed
    h,hy=254.,7.
    for _ in range(20):
        body=printed.body(h,hy)
        rows=[r for r in mass_dart(body,p) if not r['name'].startswith('tail_')]
        m,cg=resultant(rows)
        if max(abs(h-cg[0]),abs(hy-cg[1]))<.001:break
        h,hy=cg[:2]
    return body,m,cg

def groups(p,body,tail=False):
    import purchased
    pod=compound(p[n] for n in ('pod_shell','pod_lid','usb_cap'))
    cutter=box(250,150,200,at=(FPC_X0+125,0,-70))
    g=[('body_and_cell',compound([body]+[s for n,s,c in purchased.cell()])),
       ('pod',pod.cut(cutter)),
       ('antenna_strip_and_backer',compound([pod.intersect(cutter)]+[s for n,s,c in p['hardware'] if n=='lora_FPC']))]
    if tail:
        from tail_fins import rows
        g.append(('fins_and_collars',compound(s for n,s,c in rows(p) if n!='tail_bond')))
    g.append(('exposed_rod',purchased.rod()))
    return g

def meshes(group):
    out=[]
    for n,s in group:
        vs,fs=s.tessellate(.12,.16)
        out.append((n,np.array([v.toTuple() for v in vs]),np.array(fs)))
    return out

def silhouette(group,roll,step=.25):
    # Orthographic projection onto X and transverse direction q. The union
    # removes hidden rod and overlapping fin panels. Group priority changes
    # component bookkeeping only, never total area or centroid.
    x0=-2.;q0=-90.;width=int(692/step)+1;height=int(180/step)+1
    occupied=np.zeros((height,width),dtype=bool);records=[]
    a=math.radians(roll);coord=x0+(np.arange(width)+.5)*step
    for n,vs,fs in group:
        im=Image.new('1',(width,height));d=ImageDraw.Draw(im)
        pts=np.column_stack(((vs[:,0]-x0)/step,(vs[:,1]*math.cos(a)+(vs[:,2]-ROD_Z)*math.sin(a)-q0)/step))
        for face in fs:
            tri=pts[face]
            ab=tri[1]-tri[0];ac=tri[2]-tri[0]
            if abs(ab[0]*ac[1]-ab[1]*ac[0])<1e-6:continue
            d.polygon([tuple(t) for t in tri],fill=1)
        mask=np.asarray(im,dtype=bool)&~occupied;occupied |= np.asarray(im,dtype=bool)
        area=float(mask.sum()*step**2)
        cx=float(np.dot(mask.sum(axis=0),coord)/mask.sum()) if mask.any() else 0.
        records.append(dict(component=n,projected_area_mm2=area,centroid_x_mm=cx))
    area=sum(r['projected_area_mm2'] for r in records)
    cp=sum(r['projected_area_mm2']*r['centroid_x_mm'] for r in records)/area
    return dict(roll_deg=roll,projected_area_mm2=area,cp_x_mm=cp,components=records)

def carriage(p):
    from build import mass_dart,resultant
    import printed
    cases=[]
    for offset in (-5.,0.,5.):
        h=p['hanger']+offset;hy=p['hanger_y']
        for _ in range(16):
            b=printed.body(h,hy);m,cg=resultant(mass_dart(b,p))
            if max(abs(h-cg[0]-offset),abs(hy-cg[1]))<.003:break
            h,hy=cg[0]+offset,cg[1]
        tilt=math.degrees(math.atan2(h-cg[0],HEAD_BOTTOM-cg[2]))
        collisions=[];ground=1e9
        from tail_fins import rows
        import purchased
        shape=compound([b,p['pod_shell'],p['pod_lid'],p['usb_cap'],purchased.rod()]+[s for n,s,c in purchased.cell()]+[s for n,s,c in rows(p)])
        shapes=[]
        for i,(x,y,_) in enumerate(printed.head_positions()):
            a=shape.rotate((h,hy,HEAD_BOTTOM),(h,hy+1,HEAD_BOTTOM),-tilt).translate((x-h,y-hy,ROTOR_TOP-HEAD_BOTTOM))
            shapes.append(a);ground=min(ground,a.BoundingBox().zmin-GROUND_Z)
            for n,ob in [('plate',p['plate']),('rotor',p['rotor'])]:
                v=overlap(a,ob)
                if v>.02:collisions.append(dict(dart=i+1,part=n,interference_mm3=v))
        cases.append(dict(hanger_offset_from_cg_mm=offset,equilibrium_nose_down_deg=tilt,
                          hanger_x_mm=h,cg_mm=cg,mass_g=m,ground_clearance_mm=ground,
                          seating_collisions=collisions,selected=offset==0,
                          scope='Static gravity equilibrium about head bearing point; rigid head/plate/rotor seating check. Tilted options rejected here, not release-qualified.'))
    return cases

def report(p):
    before_body,bm,bc=solve_unfinned(p)
    width=before_body.BoundingBox().ylen
    samples={}
    convergence={}
    for label,b,cg,tail in [('before',before_body,bc,False),('after',p['body'],p['dart_cg'],True)]:
        mesh=meshes(groups(p,b,tail));rows=[]
        for roll in range(0,180,15):
            r=silhouette(mesh,roll)
            r.update(cg_x_mm=cg[0],static_margin_mm=r['cp_x_mm']-cg[0],static_margin_body_widths=(r['cp_x_mm']-cg[0])/width)
            rows.append(r)
        worst=min(rows,key=lambda r:r['static_margin_mm'])
        fine=silhouette(mesh,worst['roll_deg'],.125)
        convergence[label]=dict(coarse_step_mm=.25,fine_step_mm=.125,roll_deg=worst['roll_deg'],cp_delta_mm=fine['cp_x_mm']-worst['cp_x_mm'])
        samples[label]=dict(mass_g=bm if label=='before' else p['dart_mass'],cg_mm=cg,
                            minimum=worst,maximum=max(rows,key=lambda r:r['static_margin_mm']),roll_samples=rows)
    wind=[]
    for height in (16.,33.,49.):
        v=math.sqrt(2*32.17404856*height)
        wind.append(dict(drop_height_ft=height,impact_speed_ft_s=v,impact_speed_mph=v/1.4666666667,
                         tilt_deg={str(w):math.degrees(math.atan((w*1.4666666667)/v)) for w in (5,10,15)}))
    data=dict(method='Uniform pressure on the union of orthographically projected CAD side silhouettes (cardboard-cutout estimate); CP=sum(area*x)/sum(area). 0.010 in raster, 15 degree roll samples. Parts are not double-counted.',
              source_urls=['https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/generalized-center-of-pressure/','https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/conditions-for-rocket-stability/','https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/falling-object-with-air-resistance/'],
              body_width_mm=width,target_minimum_body_widths=2.,before=samples['before'],after=samples['after'],raster_convergence=convergence,
              carriage=carriage(p),wind=wind,
              limitations=['Estimate only; nothing printed, dropped or flown.','Uniform broadside pressure is not a validated small-angle CP; real force coefficients, wake shielding, fin flexibility, inertia, damping, propwash and rotation timing are unknown.','Roll sampling is discrete; the minimum reported is the sampled minimum.','Wind arithmetic assumes release from rest, zero horizontal ground speed, constant wind, no drag and perfect alignment with relative air; it is not a landing prediction.','Vertical drag alone reduces impact speed and increases this tilt at fixed relative crosswind; horizontal entrainment reduces relative crosswind, so the net change requires coupled dynamics.','A positive static margin does not establish self-righting from a flat release or completion of a turn within the available drop height. Controlled dummy drop tests must determine that.'])
    (R/'out/tail_analysis.json').write_text(json.dumps(data,indent=2)+'\n')
    return data

def fonts(size=24,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/segoeui'+('b' if bold else '')+'.ttf',size)

def render_tail_views(p):
    from build import dart_rows
    from render_local import render,caption_record
    from tail_fins import rows as tail_rows
    data=json.loads((R/'out/tail_analysis.json').read_text())
    # True CAD side cutaway; projected guide positions share one X datum.
    cut=box(300,90,100,at=(175,CELL_Y-45,-20))
    show=[]
    for n,s,c in dart_rows(p):
        if n=='body':s=s.intersect(cut)
        if n in ('cell_wrap','positive_terminal','positive_insulator'):c='gold'
        if n.startswith(('xiao','wio','mic_','INMP','power_wire','pod_M2','pod_insert','board_retention','nickel','perimeter')):continue
        show.append((s,c))
    path=R/'renders/dart_balance.png'
    # Fixed orthographic side projection makes the callouts geometrically exact.
    render(show,path,'Mass near the point; projected pressure farther aft',
           'CAD side cutaway | gold: 18650 cell | pressure marks: sampled silhouette estimate',
           az=-90,el=0,size=(2000,1000),target=(343,0,8),scale=165)
    im=Image.open(path).convert('RGB');d=ImageDraw.Draw(im)
    # render_local uses an 888 px model viewport: 330 mm vertical span.
    k=888/330;xp=lambda x:1000+(x-343)*k
    labels=[];boxes=[]
    def label(text,pos,anchor,color):
        box_=d.textbbox(pos,text,font=fonts(23));d.line([anchor,(pos[0]+10,pos[1]-8)],fill=color,width=2)
        d.rectangle((box_[0]-6,box_[1]-3,box_[2]+6,box_[3]+3),fill='#f4f7f9')
        d.text(pos,text,font=fonts(23),fill=color)
        boxes.append(box_);labels.append(dict(text=text,position=list(pos),anchor=list(anchor)))
    cy=556
    for name,x,lx,color in [('Balance point',p['dart_cg'][0],100,'#12384d'),('CP before fins',data['before']['minimum']['cp_x_mm'],750,'#7a7788'),('CP with fins',data['after']['minimum']['cp_x_mm'],1400,'#9b2859')]:
        xx=xp(x);d.line([(xx,470),(xx,cy+38)],fill=color,width=3)
        d.ellipse((xx-7,cy-7,xx+7,cy+7),fill=color)
        label(f'{name}: {length(x,3)} from tip',(lx,755),(xx,cy+38),color)
    cellx=CELL_X0+M.cell_l/2
    label(f'18650 centre: {length(cellx,3)} from tip | {mass(M.cell_mass)}',(75,325),(xp(cellx),cy),'#735712')
    label('Tip: 0.00 in',(75,610),(xp(0),cy),'#12384d')
    caption_record(path,im.size,'Mass near the point; projected pressure farther aft','CAD side cutaway | gold: 18650 cell | pressure marks: sampled silhouette estimate',boxes,labels)
    im.save(path)
    local=tail_rows(p)+[('rod_segment',__import__('purchased').rod().intersect(box(180,80,100,at=(450,0,-40))),'rod'),
                       ('pod_neck',p['pod_shell'].intersect(box(56,30,60,at=(508,0,-20))),'pod')]
    local=[(n,s.translate((0,35,35)) if n=='tail_fin_1' else s,c) for n,s,c in local]
    render([(s,c) for n,s,c in local],R/'renders/dart_fins_detail.png','Tail attachment - one fin lifted to show keyed tabs',
           f'Root chord {length(FIN_X1-FIN_X0)} | exposed radial span {length(FIN_TIP_R-FIN_ROOT_R)} | {length(FIN_T)} PETG | debond before removal',az=-60,el=24,size=(1800,1100))
    # Label attachment separately in the lower part of the detail image.
    path=R/'renders/dart_fins_detail.png';base=Image.open(path).convert('RGB')
    im=Image.new('RGB',(base.width,base.height+75),'#f4f7f9');im.paste(base,(0,0));d=ImageDraw.Draw(im)
    text=f'Two {length(FIN_COLLAR_L)} collars; {length(FIN_SLOT_T-FIN_T,3)} total tab clearance; bond tabs + rod; keep wire relief dry'
    d.text((35,1120),text,font=fonts(23),fill='#193443');im.save(path)
    rec=json.loads((R/'tmp/us-caption-records/dart_fins_detail.json').read_text());rec['labels'].append(dict(text=text,position=[35,1120],anchor=[35,1120]));rec['text_boxes'].append(list(d.textbbox((35,1120),text,font=fonts(23))));caption_record(path,im.size,rec['title'],rec['subtitle'],rec['text_boxes'],rec['labels'])
    fall_schematic(data)

def fall_schematic(data):
    from render_local import caption_record
    path=R/'renders/dart_fall_sequence.png';im=Image.new('RGB',(2000,1050),'#f4f7f9');d=ImageDraw.Draw(im)
    title='Four fall attitudes - schematic, not a simulation'
    sub='Illustrative poses only; turn time, rotation path and impact attitude require controlled dummy drops'
    boxes=[];labels=[]
    def text(s,xy,size=24,bold=False):
        f=fonts(size,bold);d.text(xy,s,font=f,fill='#193443');boxes.append(list(d.textbbox(xy,s,font=f)));labels.append(dict(text=s,position=list(xy),anchor=list(xy)))
    text(title,(35,24),34,True);text(sub,(35,80),24)
    tilt=data['wind'][1]['tilt_deg']['10'];centres=[(270,450),(760,470),(1240,470),(1730,470)]
    descriptions=[('1. Leaves flat','At the balance point'),('2. Begins turning','Restoring moment estimate'),('3. Nose-down pose','Still-air illustration'),('4. Points into the wind',f'10 mph / 33 ft estimate: {tilt:.1f} deg')]
    for centre,angle,(heading,desc) in zip(centres,(0.,45.,90.,90.-tilt),descriptions):
        x,y=centre;a=math.radians(angle);u=np.array([math.cos(a),-math.sin(a)]);v=np.array([math.sin(a),math.cos(a)])
        # +u points toward tail; point at -u is the low end at nose-down poses.
        pt=lambda axial,rad=0:tuple(np.array([x,y])+u*axial+v*rad)
        d.line([pt(-160),pt(160)],fill='#9b9678',width=7)
        d.polygon([pt(-160),pt(-137,-7),pt(-137,7)],fill='#193443')
        d.line([pt(-112),pt(-50)],fill='#e88939',width=25)
        d.line([pt(-103),pt(-62)],fill='#e1b441',width=14)
        d.line([pt(95),pt(125)],fill='#16778d',width=24)
        d.polygon([pt(46,0),pt(68,-27),pt(91,-27),pt(105,0),pt(91,27),pt(68,27)],fill='#a43b6b')
        d.line([pt(125),pt(168)],fill='#2697a5',width=9)
        d.ellipse((x-7,y-7,x+7,y+7),fill='#193443')
        text(heading,(x-212,735),24,True);text(desc,(x-212,778),22)
    # Wind toward the right, so the nose leans left/upwind in the last pose.
    d.line([(1540,230),(1860,230)],fill='#387b9a',width=4);d.polygon([(1860,230),(1842,221),(1842,239)],fill='#387b9a')
    text('Wind: 10 mph',(1580,175),24)
    text('Pose spacing is not elapsed time or distance. No landing, self-righting or survival result is claimed.',(65,910),26)
    caption_record(path,im.size,title,sub,boxes,labels);im.save(path)

if __name__=='__main__':
    from build import load_cache
    p=load_cache();a=report(p);render_tail_views(p)
    print(json.dumps({k:{n:a[k][n] for n in ('mass_g','cg_mm','minimum','maximum')} for k in ('before','after')},indent=2))
