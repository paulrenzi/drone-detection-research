"""Stake installation and inert drop dummy, derived from the same cached model."""
from pathlib import Path
import json,math
import numpy as np
from parameters import *
from geometry import *
import purchased as buy
R=Path(__file__).resolve().parent

def write_kit_manifest():
    kits={'four_flying_darts_and_harness':dict(body=4,pod_shell=4,pod_lid=4,usb_cap=4,plate=1,rotor=1,tail_fin=16,tail_collar=8),
          'one_stake_listener':dict(stake_adapter=1,stake_cell_holder=1,pod_shell=1,pod_lid=1,usb_cap=1),
          'one_inert_dummy':dict(dummy_body=1,dummy_lid=1,dummy_head_insert=1,pod_shell=1,pod_lid=1,usb_cap=1,tail_fin=4,tail_collar=2),
          'fit_tool':dict(fit_coupon=1)}
    (R/'out/kits.json').write_text(json.dumps(dict(printed_kits=kits,notes=['All printed parts intentionally100% infill; STLs onZ0 for Vyper.','Stake and dummy are alternatives; do not add their parts to flight payload.','See DESIGN.md for bought hardware, ballast centres and assembly.']),indent=2)+'\n')

def dummy_baseline(p):
    rows=[('dummy_body',p['dummy_body'],'body'),('dummy_lid',p['dummy_lid'],'lid'),
          ('dummy_head_insert',p['dummy_head_insert'],'body'),('rod',buy.rod(),'rod')]
    rows += [(n,p[n],'pod' if n=='pod_shell' else 'lid') for n in ('pod_shell','pod_lid','usb_cap')]
    from tail_fins import rows as tail_rows
    rows += tail_rows(p)
    rows += [r for r in p['hardware'] if r[0].startswith(('pod_insert','pod_M2','perimeter'))]
    for x in (77,145):
        nut=__import__('cadquery').Workplane('XY').workplane(offset=16.4).center(x,CELL_Y).polygon(6,M2_NUT_CIRC).extrude(1.6).val().cut(cyl(.85,2,(x,CELL_Y,16.3)))
        rows += [(f'dummy_nut_{x}',nut,'metal'),(f'dummy_M2x8_{x}',buy.screw(2,8,(x,CELL_Y,14),head=3.8,head_h=2),'metal')]
    return rows

def dummy_report(p):
    from build import mass_item,resultant
    rows=[]
    for n,s,c in dummy_baseline(p):
        rho=M.rod_density if n=='rod' else 8.5 if 'insert' in n and n!='dummy_head_insert' else 7.85 if 'M2' in n or 'nut_' in n else 1.10 if 'seal' in n else M.petg_density
        rows.append(mass_item(n,s,rho if n!='tail_bond' else None,mass=M.fin_adhesive_mass if n=='tail_bond' else None,basis='Inert dummy nominal material-density model, solid PETG; same tail bonds'))
    base_m,base_c=resultant(rows)
    needed=p['dart_mass']-base_m
    # Preserve approximately the real head/body mass split, then solve exact
    # total mass and longitudinal moment using the two body ballast pockets.
    real_head=sum(r['mass_g'] for r in p['mass_rows'] if r['centroid_mm'][0]>450)
    empty_head=sum(r['mass_g'] for r in rows if r['centroid_mm'][0]>450)
    head=max(0,real_head-empty_head+.5)
    body=needed-head
    target=np.array(p['dart_cg'])*p['dart_mass']
    moment=np.array(base_c)*base_m
    head_moment=head*np.array([560.,0.,7.])
    rear=((target-moment-head_moment)[0]-body*92)/38
    front=body-rear
    yz=(target-moment-head_moment)[1:]/body
    ballast=[]
    for name,mass,x,y,z,L,W,bottom,top in [
        ('body_front',front,92,yz[0],yz[1],20,12,3.6,20),
        ('body_rear',rear,130,yz[0],yz[1],20,12,3.6,20),
        ('head_front',head/2,554,0,7,6.5,13,4.2,10),
        ('head_rear',head/2,566,0,7,6.5,13,4.2,10)]:
        H=mass/(L*W)*1000/M.ballast_density
        fits=mass>=0 and z-H/2>=bottom and z+H/2<=top and (abs(y-CELL_Y)<=1.5 if name.startswith('body') else True)
        ballast.append(dict(name=name,mass_g=mass,centroid_mm=[x,float(y),float(z)],equivalent_solid_steel_bbox_mm=[L,W,H],fits_pocket=bool(fits)))
    total=base_m+sum(b['mass_g'] for b in ballast)
    cg=(moment+sum((np.array(b['centroid_mm'])*b['mass_g'] for b in ballast),start=np.zeros(3)))/total
    return dict(target_mass_g=p['dart_mass'],baseline_mass_g=base_m,ballast_total_g=needed,
                ballast=ballast,total_g=total,cg_mm=cg.tolist(),cg_error_mm=(cg-np.array(p['dart_cg'])).tolist(),
                baseline_parts=rows,all_pockets_fit=all(b['fits_pocket'] for b in ballast),
                method='Four weighed steel ballast portions; continuous equivalent steel blocks model mass and all three moments. Fix at listed centres with foam/adhesive; include adhesive in weighed portion. No battery or electronics.',
                limitation='Match the actual built real dart before comparative tests; CAD targets depend on unmeasured stock and slicer mass. No passive nose-down or sticking claim.')

def dummy_rows(p):
    rows=dummy_baseline(p)
    for b in dummy_report(p)['ballast']:
        L,W,H=b['equivalent_solid_steel_bbox_mm'];x,y,z=b['centroid_mm']
        rows.append(('ballast_'+b['name'],box(L,W,H,at=(x,y,z-H/2)),'metal'))
    return rows

def stake_local_rows(p):
    from build import dart_rows
    rows=[r for r in dart_rows(p) if r[0] in ('pod_shell','pod_lid','usb_cap')]
    rows+=p['board']+p['mic']+[r for r in p['hardware'] if not r[0].startswith(('power_wire','rod_tie','body_strain','nickel'))]
    rows += [('stake_adapter',p['stake_adapter'],'body'),('stake_cell_holder',p['stake_cell_holder'].translate((200,-30,0)),'body')]
    rows += [(n,s.translate((200,-30,0)),c) for n,s,c in buy.cell()]
    z=5+M.stake_d/math.sqrt(2)
    rows += [('garden_stake',cyl(M.stake_d/2,1219.2,(-M.stake_burial+BODY_X0,26,z),(1,0,0)),'rod'),
             ('pod_socket_rod_offcut',cyl(2.9,40,(460,0,ROD_Z),(1,0,0)),'rod')]
    for x in (457,483):rows+=buy.zip_tie_x(x,26,(z+M.stake_d/2-2)/2,22,z+M.stake_d/2+4,name=f'stake_clamp_tie_{x}')
    for x in (284,336):rows+=buy.zip_tie_x(x,26,(z+M.stake_d/2+1.8)/2,22,z+M.stake_d/2+.2,name=f'stake_cell_tie_{x}')
    rows+=buy.zip_tie_x(490,13,(z+M.stake_d/2)/2,42,z+M.stake_d/2+2,name='stake_pod_retaining_tie')
    for i in range(2):
        tail=[pt for pt in power_wire_paths()[i] if pt[0]>=480]
        lead=[(x+200,y-30,z0) for x,y,z0 in power_wire_paths()[i][:3 if i==0 else 4]]
        if i:lead.append((352,-1,4.6))
        path=lead+[(355-i,12+i*2,10),(450,12+i*2,10),(478,4.3+i*1.4,4.8)]+tail
        rows.append((f'stake_power_wire_{i}',pipe_path(path,M.wire_od/2),'red' if i==0 else 'wire'))
    return rows

def stake_rows(p):
    from build import stood_transform
    return [(n,stood_transform(s),c) for n,s,c in stake_local_rows(p)]

def stake_mass_report(p):
    from build import mass_item,resultant
    raw={n:(n,s,c) for n,s,c in stake_local_rows(p)};used=set();rows=[]
    groups=[('XIAO_ESP32S3',[n for n in raw if n.startswith('xiao_')],M.xiao_mass),
            ('Wio_SX1262',[n for n in raw if n.startswith('wio_')],M.wio_mass),
            ('INMP441_breakout',[n for n,s,c in p['mic']],M.mic_mass),
            ('Samsung25R_cell',['cell_wrap','positive_terminal','positive_insulator'],M.cell_mass),
            ('LoRa_FPC_and_coax',['lora_FPC','RF_pigtail'],M.fpc_mass),
            ('WiFi_FPC_and_coax',['wifi_FPC','wifi_coax'],M.wifi_mass)]
    for label,names,grams in groups:
        used.update(names)
        rows.append(mass_item(label,compound(raw[n][1] for n in names),mass=grams,basis='Same sourced maximum/MEASURE mass as flying dart'))
    for n,(nn,s,c) in raw.items():
        if n in used:continue
        rho=M.petg_density if n in ('pod_shell','pod_lid','usb_cap','stake_adapter','stake_cell_holder') else M.rod_density if n in ('garden_stake','pod_socket_rod_offcut') else 8.5 if 'insert' in n else 7.85 if 'M2' in n else .15 if 'foam' in n else 1.10 if 'seal' in n or 'film' in n else 1.45 if 'wire' in n else 1.14
        rows.append(mass_item(n,s,rho,basis='Nominal model density; 100% infill for printed pieces; stock MEASURE'))
    total,cg=resultant(rows)
    return dict(parts=rows,total_g=total,cg_local_mm=cg,datum='Original dart X/Y/Z datum before stood_transform; includes full1219.2mm stake and cell; not flight payload')

def render_variants(p):
    from build import stood_transform,RENDERS
    from render_local import render
    def rend(rows,file,title,sub,**kw):render([(s,c) for n,s,c in rows],RENDERS/file,title,sub,**kw)
    soil=('soil',box(160,180,15,at=(0,12,-15)),'soil')
    rend(stake_rows(p)+[soil],'stake_assembled.png','Hand-placed stake listener','48 in stake | nominal10 mm OD, clamp8-13 mm | mic500 mm above actual soil | same18650 in separate holder',az=-132,el=8,size=(950,1800))
    local=stake_local_rows(p)
    # Expose the clamp without burying it behind the opaque pod.
    close=[r for r in local if r[0] in ('stake_adapter','pod_socket_rod_offcut','stake_pod_retaining_tie') or r[0].startswith('stake_clamp')]
    z=5+M.stake_d/math.sqrt(2)
    close.append(('stake_cut',cyl(M.stake_d/2,85,(435,26,z),(1,0,0)),'rod'))
    close.append(('pod_neck',p['pod_shell'].intersect(box(56,22,25,at=(508,0,-2))),'pod'))
    rend(close,'stake_clamp_detail.png','Reusable pod on adjustable V saddle','Two ties clamp an8-13 mm stake | 5.8 mm fibreglass offcut joins original pod socket',az=-58,el=32,size=(1500,1000))
    rows=dummy_rows(p)
    rend([(n,stood_transform(s),c) for n,s,c in rows]+[soil],'dummy_assembled.png','Inert full-mass drop-test dart','Same rod, hanger, pod exterior and antenna backer | four weighed ballast portions | no cell or electronics',az=-135,el=8,size=(850,1600))
    show=[r for r in rows if r[0] in ('dummy_body','dummy_lid','dummy_nut_77','dummy_nut_145') or r[0].startswith('ballast_body')]
    show=[(n,s.translate((0,0,24 if n=='dummy_lid' else 0)),c) for n,s,c in show]
    d=dummy_report(p)
    rend(show,'dummy_ballast_detail.png','Dummy body and retained ballast pockets',f"{d['ballast_total_g']:.2f} g total steel ballast across body and head | body lid uses two M2x8 screws and captive nuts",az=-65,el=35,size=(1600,1000))
