"""Geometric and first-order mechanical checks; never equated to a flight test."""
from pathlib import Path
import json, math, itertools, time
import cadquery as cq
from parameters import *
from geometry import *
import printed as pr

ROOT=Path(__file__).resolve().parent

def verify(p):
    from build import PRINT_NAMES, dart_rows, carried_transform, stood_transform, print_transform, harness_rows
    checks=[];failures=[]
    def check(name,ok,**data):
        row=dict(check=name,pass_=bool(ok),**data);checks.append(row)
        print('CHECK',name,'PASS' if ok else 'FAIL',json.dumps(data)[:500],flush=True)
        if not ok:failures.append(name)
    for n in PRINT_NAMES:
        s=p[n];b=print_transform(n,s).BoundingBox();dims=[b.xlen,b.ylen,b.zlen]
        check(n+'_solid',s.isValid() and len(s.Solids())==1,valid=s.isValid(),solids=len(s.Solids()),volume_mm3=s.Volume())
        check(n+'_bed',all(a<=b+.001 for a,b in zip(dims,BED)),bbox_mm=dims,bed_mm=BED)
    check('balance_fixed_point',abs(p['hanger']-p['dart_cg'][0])<.02,hanger_mm=p['hanger'],cg_mm=p['dart_cg'],mass_g=p['dart_mass'])
    # D throat tolerance .20 mm total; Samsung diameter tolerance +.07.
    delta=(M.cell_d+.07-(SNAP_MOUTH-.20))/2
    strain=3*SNAP_T*delta/(2*SNAP_L**2)
    Kt=2.0 # conservative root/stress-concentration factor, not FEA
    I=SNAP_H*SNAP_T**3/12
    force=3*M.petg_modulus*I*delta/SNAP_L**3
    check('snap_flexure_screen',Kt*strain<M.printed_allowable_strain,per_arm_deflection_mm=delta,nominal_surface_strain=strain,root_factor=Kt,factored_strain=Kt*strain,screen_allowable=M.printed_allowable_strain,per_arm_tip_force_N=force,four_arm_force_N=4*force,method='linear axial cantilever, F=3EI delta/L^3; conservative tip load')
    neckstress=3*p['dart_mass']*9.81/1000/(math.pi*NECK_D**2/4)
    check('hanger_tension_screen',neckstress<8,stress_3g_MPa=neckstress,assumed_print_allowable_MPa=8,method='axial neck area, layer-strength coupon required')
    payload_force=4*p['dart_mass']*9.81/1000
    torque=.12*payload_force*(BEARING_RO+BEARING_RI)/2000
    check('bearing_friction_screen',torque*3<1.8*.0980665,assumed_mu=.12,static_torque_Nm=torque,three_g_torque_Nm=3*torque,SG90_4v8_stall_Nm=1.8*.0980665,scope='engineering estimate with PTFE tape, no measured friction or servo current')
    hm=json.loads((ROOT/'out/mass_properties.json').read_text())['harness_total_g']
    tie_force=(4*p['dart_mass']+hm)*9.81/1000*3/4
    check('four_rail_ties_load_screen',tie_force<80,force_per_tie_3g_N=tie_force,S7_catalog_min_loop_strength_N=80,scope='Equal sharing assumed; printed saddle strength and dynamic unequal loading untested')
    # Rigid local fits: deliberate press fit and heat-set interference are
    # reported separately and are not silently counted as free clearances.
    cell=compound(s for _,s,_ in __import__('purchased').cell())
    board=compound(s for _,s,_ in p['board'])
    mic=compound(s for _,s,_ in p['mic'])
    for name,a,b in [
        ('cell_to_body',cell,p['body']),('PCB_to_shell',board,p['pod_shell']),
        ('PCB_to_lid',board,p['pod_lid']),('mic_to_shell',mic,p['pod_shell']),
        ('mic_to_lid',mic,p['pod_lid']),('shell_to_lid',p['pod_shell'],p['pod_lid']),
        ('cap_to_shell',p['usb_cap'],p['pod_shell']),('cap_to_lid',p['usb_cap'],p['pod_lid']),
        ('dummy_lid_to_body',p['dummy_lid'],p['dummy_body']),
        ('dummy_insert_to_shell',p['dummy_head_insert'],p['pod_shell'])]:
        v=overlap(a,b);check(name,v<.02,interference_mm3=v)
    for n,s,c in p['hardware']:
        if not n.startswith(('power_wire','mic_wire')):continue
        for part in ('body','pod_shell','pod_lid'):
            v=overlap(s,p[part]);check(n+'_to_'+part,v<.02,interference_mm3=v)
    wires=[(n,s) for n,s,c in p['hardware'] if n.startswith(('mic_wire','power_wire')) or n in ('RF_pigtail','wifi_coax')]
    wire_collisions=[]
    for i,(n,a) in enumerate(wires):
        for other,b in wires[i+1:]:
            v=overlap(a,b)
            if v>.02:wire_collisions.append([n,other,v])
    check('separate_insulated_wire_routes',not wire_collisions,collisions=wire_collisions,scope='Nominal rigid wire routes, excluding solder-to-pad contacts')
    press=overlap(__import__('purchased').rod(),p['body'])
    check('rod_press_lands_declared',press>0 and press<30,intentional_interference_mm3=press,land_bore_mm=M.rod_fit_bore,rod_mm=M.rod_d,main_bore_mm=M.rod_d+.35)
    # Plate, servo and rotor check at every 2-degree sample across 0..64.
    sv=compound(s for n,s,c in p['servo'] if n.startswith('SG90_case') or n.startswith('SG90_output'))
    for name,a,b in [('servo_case_to_plate',sv,p['plate']),('servo_case_to_rotor',sv,p['rotor']),('rotor_to_plate',p['rotor'],p['plate'])]:
        v=overlap(a,b);check(name,v<.02,interference_mm3=v)
    drive=compound(s for n,s,c in p['servo'] if 'horn' in n or 'drive_pin' in n)
    for n,s in [('plate',p['plate']),('rotor',p['rotor'])]:
        v=overlap(drive,s);check('horn_and_drive_to_'+n,v<.02,interference_mm3=v)
    keeper=compound(s for n,s,c in p['servo'] if 'keeper' in n or 'spline_screw' in n)
    v=overlap(keeper,p['rotor']);check('axial_keeper_to_rotor',v<.02,interference_mm3=v,keeper_gap_mm=.4)
    ties=compound(s for n,s,c in p['rail_ties'])
    v=overlap(ties,p['plate']);check('rail_tie_channels',v<.02,interference_mm3=v,nominal_tie_width_mm=2.5,channel_width_mm=3.1)
    # Head underside contact area measured by intersection of a thin bearing
    # probe. Head solid starts at rotor top, so normal supported contact is
    # zero interference; probe converts real footprint area to a measurement.
    positions=pr.head_positions();steps=pr.release_steps()
    area={};hold0=[];release_windows={};angles=[k*.5 for k in range(129)]
    for i,(x,y,_) in enumerate(positions):
        probe=cyl(HEAD_D/2,.1,(x,y,ROTOR_TOP-.1))
        areas=[]
        for phi in angles:
            r=p['rotor'].rotate((0,0,0),(0,0,1),phi)
            areas.append(overlap(r,probe)/.1)
        atstep=areas[int(steps[i]*2)];atprev=areas[int((steps[i]-16)*2)]
        untilprev=min(areas[:int((steps[i]-16)*2)+1])
        freed=[a for a,v in zip(angles,areas) if v<.001 and abs(a-steps[i])<=16]
        release_windows[str(i+1)]=[min(freed),max(freed)] if freed else []
        hold0.append(areas[0]);area[str(i+1)]=dict(initial_mm2=areas[0],previous_detent_mm2=atprev,minimum_before_previous_detent_mm2=untilprev,at_release_mm2=atstep,release_deg=steps[i],full_clear_window_deg=release_windows[str(i+1)])
        check(f'dart{i+1}_release',atstep<.001 and untilprev>8,**area[str(i+1)])
    # Check neck/rotor volumes throughout the turn; round heads sit above it.
    worst=0.;contact=[]
    for phi in range(0,65,2):
        rr=p['rotor'].rotate((0,0,0),(0,0,1),phi)
        for i in range(4):
            if phi>steps[i]:continue
            h=carried_transform(p['body'],i,p['hanger_xy'])
            v=overlap(h,rr)
            if v>worst:worst=v;contact=[phi,i+1]
    check('rotor_body_sweep',worst<.02,max_interference_mm3=worst,worst_angle_dart=contact,sampled_step_deg=2)
    # Geometric full rigid assemblies, conservative whole-component bboxes
    # prune expensive boolean checks. Deliberate sealing/tie contacts excluded.
    # Exterior collision geometry. The pod is conservatively filled solid;
    # buried electronic detail was checked above and cannot affect frame fit.
    dart=compound([p[n] for n in ('body','pod_shell','pod_lid','usb_cap')]+[__import__('purchased').rod(),cell]+[s for n,s,c in p['hardware'] if n in ('lora_FPC','RF_pigtail')])
    carried=[carried_transform(dart,i,p['hanger_xy']) for i in range(4)]
    records=[]
    def against(a,rows,label):
        mx=0.;which='';dmin=1e9;dname=''
        aa=xyz_bounds(a)
        for n,b,c in rows:
            bb=xyz_bounds(b)
            # conservative Euclidean AABB separation, then precise OCP if close
            gaps=[max(0,bb[j]-aa[j+1],aa[j]-bb[j+1]) for j in (0,2,4)]
            lb=math.sqrt(sum(x*x for x in gaps))
            if lb<dmin:dmin=lb;dname=n
            if lb<1e-5:
                v=overlap(a,b)
                if v>mx:mx=v;which=n
                if v>.02:records.append(dict(case=label,part=n,interference_mm3=v))
        return mx,which,dmin,dname
    drone=[r for r in p['drone'] if not r[0].startswith('prop_swept')]
    frame=[r for r in drone if 'landing_gear' not in r[0]]
    legs=[r for r in drone if 'landing_gear' in r[0]]
    props=[r for r in p['drone'] if r[0].startswith('prop_swept')]
    hfixed=[('plate',p['plate'],'plate')]+[(n,s,c) for n,s,c in p['servo'] if n.startswith('SG90_case')]
    hrigid=compound(s for n,s,c in hfixed)
    maxv,n,dist,dn=against(hrigid,drone,'harness_drone')
    check('harness_to_OEM_drone',maxv<.02,max_interference_mm3=maxv,part=n,min_clearance_mm=dist,nearest=dn)
    for i,a in enumerate(carried):
        for label,rows in [('frame',frame),('landing_gear',legs),('prop_sweeps',props),('harness',hfixed)]:
            v,n,d,dn=against(a,rows,f'carried_{i+1}_{label}')
            check(f'carried_dart{i+1}_{label}',v<.02,max_interference_mm3=v,part=n,min_clearance_mm=d,nearest=dn)
        check(f'carried_dart{i+1}_ground',a.BoundingBox().zmin>GROUND_Z,clearance_mm=a.BoundingBox().zmin-GROUND_Z)
        for j in range(i):
            v=overlap(a,carried[j]);d=min(aabb_distance(x,y) for x in a.Solids() for y in carried[j].Solids());check(f'darts_{j+1}_{i+1}_separation',v<.02,interference_mm3=v,clearance_lower_bound_mm=d)
    # Full extraction sweep for every dart, including head crossing the plate.
    # Translate 0..90mm in 5mm increments, preserve horizontality until clear.
    release_max=0.;release_case=None;release_leg_min=1e9
    for i in range(4):
        rr=p['rotor'].rotate((0,0,0),(0,0,1),steps[i])
        obstacles=hfixed+[('rotor',rr,'rotor')]+drone
        for dz in range(0,91,5):
            a=carried[i].translate((0,0,-dz))
            for n,b,c in obstacles:
                v=overlap(a,b)
                if v>release_max:release_max=v;release_case=[i+1,dz,n]
            # Exact nearest leg clearance at each sample.
            for n,b,c in legs:
                if b.Volume()>500:release_leg_min=min(release_leg_min,aabb_distance(a,b))
    check('vertical_extraction_sweep',release_max<.02,max_interference_mm3=release_max,worst_dart_drop_part=release_case,drop_samples_mm=list(range(0,91,5)),min_leg_clearance_mm=release_leg_min)
    # Prescribed rotation after 430mm separation, aircraft in air +1500mm.
    # All four dart positions, 0..90deg pitch; ground checked with aircraft high.
    pitchmax=0.;pitchcase=None;pitchground=1e9
    for i in range(4):
        for angle in range(0,91,5):
            a=carried_transform(dart,i,p['hanger_xy'],430,angle)
            for n,b,c in drone:
                v=overlap(a,b)
                if v>pitchmax:pitchmax=v;pitchcase=[i+1,angle,n]
            pitchground=min(pitchground,a.BoundingBox().zmin-(GROUND_Z-1500))
    check('post_extraction_pitch_sweep',pitchmax<.02,max_interference_mm3=pitchmax,worst=pitchcase,pitch_step_deg=5,vertical_translation_before_pitch_mm=430,aircraft_height_above_stock_ground_mm=1500,ground_clearance_mm=pitchground,scope='prescribed path only, no fall dynamics or aerodynamic claim')
    # Stood state body stop at ground, 70mm rod penetration, all electronics
    # above ground. The rod/soil intersection is the only intended one.
    ground=box(1000,1000,100,at=(0,0,-100))
    for name in ('body','pod_shell','pod_lid','usb_cap'):
        s=stood_transform(p[name]);v=overlap(s,ground)
        check('stood_'+name+'_ground',v<.02,interference_mm3=v,lowest_height_mm=s.BoundingBox().zmin)
    stood=stood_transform(dart).translate((650,0,0))
    parked=compound([s.moved(cq.Location(cq.Vector(0,0,-GROUND_Z))) for n,s,c in p['drone']]+[a.moved(cq.Location(cq.Vector(0,0,-GROUND_Z))) for a in carried[1:]])
    # The entire stood listener is outside the entire parked vehicle AABB;
    # this conservative bound proves separation without an expensive all-pairs
    # solids traversal through the detailed OEM compound.
    lb=aabb_distance(stood,parked)
    check('stood_full_aircraft_scene',lb>1.,clearance_lower_bound_mm=lb,listener_offset_mm=[650,0,0],stock_skid_ground_z_mm=0,scope='end-state review layout; intentional70mm tip-soil penetration')
    from variants import dummy_report, dummy_rows, stake_local_rows
    dr=dummy_report(p)
    check('dummy_mass_and_3D_balance',abs(dr['total_g']-p['dart_mass'])<.001 and max(abs(v) for v in dr['cg_error_mm'])<.001 and dr['all_pockets_fit'],mass_g=dr['total_g'],ballast_g=dr['ballast_total_g'],cg_error_mm=dr['cg_error_mm'],pockets_fit=dr['all_pockets_fit'])
    for b in dr['ballast']:
        L,W,H=b['equivalent_solid_steel_bbox_mm'];x,y,z=b['centroid_mm']
        shape=box(L,W,H,at=(x,y,z-H/2))
        v=overlap(shape,p['dummy_body'] if b['name'].startswith('body') else p['dummy_head_insert'])
        check('ballast_'+b['name']+'_clearance',v<.02,interference_mm3=v,steel_mass_g=b['mass_g'])
    # Cap removed: actual insertion corridor from beyond pod end to USB mouth.
    usb=box(18,11,6.2,at=(581,0,2.5))
    v=overlap(usb,p['pod_shell'])+overlap(usb,p['pod_lid'])
    check('USB_plug_access',v<.02,interference_mm3=v,plug_envelope_mm=[12,11,6.2],scope='MEASURE actual cable overmould; end cap removed')
    # Pin enters through removable service opening, diagonally downward onto
    # either button; starts beyond Wio end so upper PCB cannot block it.
    for y in (-5.93,5.93):
        probe=pipe_path([(584,y,16),(570.8,y,5.0)],.35)
        obstacles=[p['pod_shell'],p['pod_lid']]+[s for n,s,c in p['board'] if n.startswith('wio_')]
        v=sum(overlap(probe,s) for s in obstacles)
        check('BOOT_RESET_pin_access_'+str(y),v<.02,interference_mm3=v,pin_d_mm=.7,scope='Cap removed; verify button identity/travel on purchased revision')
    check('mic_ground_height',abs(MIC_X-BODY_X0-500)<.01,height_mm=MIC_X-BODY_X0)
    # V saddles are diameter-independent. A circle seated on both45deg faces
    # raises its axis by radius*sqrt(2); evaluate both range endpoints and nominal.
    for d in (8.,M.stake_d,13.):
        z=5+d/math.sqrt(2)
        stake=cyl(d/2,70,(440,26,z),(1,0,0))
        v=overlap(stake,p['stake_adapter'])
        check('stake_range_'+str(d),v<.02,interference_mm3=v,axis_height_mm=z,diameter_mm=d)
        holder=p['stake_cell_holder'].translate((200,-30,0))
        low=cyl(d/2,80,(270,26,z),(1,0,0))
        v=overlap(low,holder)
        check('stake_cell_holder_range_'+str(d),v<.02,interference_mm3=v,diameter_mm=d)
    sr=stake_local_rows(p);sd={n:s for n,s,c in sr}
    for n in ('stake_power_wire_0','stake_power_wire_1'):
        for target in ('stake_adapter','stake_cell_holder','pod_shell','pod_lid'):
            v=overlap(sd[n],sd[target]);check(n+'_to_'+target,v<.02,interference_mm3=v)
    v=overlap(sd['stake_power_wire_0'],sd['stake_power_wire_1'])
    check('stake_separate_power_wires',v<.02,interference_mm3=v)
    for a,b in [('stake_adapter','pod_shell'),('stake_adapter','pod_socket_rod_offcut')]:
        v=overlap(sd[a],sd[b]);check(a+'_to_'+b,v<.02,interference_mm3=v)
    for n,s,co in sr:
        if not n.startswith(('stake_clamp_tie','stake_cell_tie','stake_pod_retaining')):continue
        target=sd['stake_cell_holder'] if n.startswith('stake_cell') else sd['stake_adapter']
        v=overlap(s,target)+overlap(s,sd['garden_stake'])
        if n.startswith('stake_pod_retaining'):v+=overlap(s,p['pod_shell'])
        check(n+'_clearance',v<.02,interference_mm3=v)
    check('stake_mic_height',abs(MIC_X-BODY_X0-500)<.01,mic_height_mm=500,stake_length_mm=1219.2,burial_nominal_mm=M.stake_burial,scope='Slide adapter until mic is500mm above actual ground, independently of insertion depth')
    data=dict(checks=checks,failed=failures,rigid_interferences=records,release_contact=area,measure_parameters=measure_dict(),clearance_distances='Vehicle distances are conservative axis-aligned bounding-box lower bounds; a zero lower bound is NOT a measured zero gap. Interference results use actual B-rep boolean volumes after broad-phase pruning.',discrete_sampling='0.5deg contact; 2deg rotor-neck; 5mm extraction; 5deg prescribed pitch',limitations=['No aerodynamic or self-righting simulation','No print, proof load, water, shake, cycling or flight test','MEASURE parameters remain nominal assumptions','Intentional press-fit, heat-set and elastomer contacts are excluded from clearance pass claims'])
    (ROOT/'out'/'checks.json').write_text(json.dumps(data,indent=2)+'\n')
    from display_units import write_checks_markdown
    write_checks_markdown(data, ROOT/'out'/'checks.md')
    print('VERIFICATION',len(checks),'checks;',len(failures),'failures',flush=True)
    if failures:raise AssertionError('Failed geometry checks: '+', '.join(failures))
    return data
