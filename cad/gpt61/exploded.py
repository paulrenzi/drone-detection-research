"""Presentation transforms only. The original CadQuery B-reps stay unchanged.

Coordinates and translations here are mm, Z up, as in build.py. Staged rigid
translations explain disassembly; they do not simulate flexures, wiring, screw
rotation, cutting ties, heat setting, or the commanded rotor release sequence.
"""
from dataclasses import dataclass
from pathlib import Path
import json
import numpy as np
from geometry import compound, overlap, xyz_bounds
from build import load_cache, dart_rows, harness_rows
from parameters import ROTOR_TOP, HEAD_BOTTOM
import printed

ROOT = Path(__file__).resolve().parent
DURATION = 8.0


@dataclass
class Part:
    name: str
    rows: list
    facts: dict
    family: str

    @property
    def shape(self):
        return compound(s for _, s, _ in self.rows)


def facts(display, kind, source, function, mass=None, basis=None, group=None,
          uncertainties=()):
    return dict(display_name=display, printed_or_bought=kind,
                geometry_source=source, function=function, mass_g=mass,
                mass_basis=basis or 'Unmeasured; no separate mass in the existing report.',
                mass_measured=False, mass_group=group,
                uncertainties=list(uncertainties))


def make_parts(p):
    mass = json.loads((ROOT/'out/mass_properties.json').read_text())
    dm = {r['name']: r for r in mass['dart']}
    hm = {r['name']: r for r in mass['harness']}
    dart = []

    def add(name, rows, display, kind, source, function, mass_key=None, **kw):
        r = dm.get(mass_key or name)
        dart.append(Part(name, rows, facts(display, kind, source, function,
                         mass=r['mass_g'] if r else None,
                         basis=r['basis'] if r else None, **kw), 'dart'))

    raw = {n: (n, s, c) for n, s, c in dart_rows(p)}
    for n in raw:
        if not n.startswith('tail_'):continue
        add(n,[raw[n]],n.replace('_',' ').capitalize(),'bought' if n=='tail_bond' else 'printed',
            {'type':'modelled','reference':'tail_fins.py; DESIGN.md'},
            'Bonds the keyed fins and collars to the rod.' if n=='tail_bond' else 'Adds tail side area for the estimated restoring moment.' if n.startswith('tail_fin') else 'Locates four keyed fin tabs around the rod.',
            uncertainties=['Prototype bond strength, fin stiffness and fall response are untested; weigh actual parts and cured adhesive.'])
    for n, desc, function in (
        ('body', 'Printed body with integral cell snaps and hanger', 'Supports the cell and rod and transfers the carried load through its integral hanger.'),
        ('pod_shell', 'Printed electronics tray', 'Holds the electronics and provides the rod socket and microphone cavity.'),
        ('pod_lid', 'Printed service lid and FPC backer', 'Closes the pod and supports the external kit FPC antenna.'),
        ('usb_cap','Printed USB and button service cap','Covers the removable USB and pin access opening.')):
        add(n, [raw[n]], desc, 'printed', {'type':'modelled', 'reference':'printed.py; DESIGN.md'}, function,
            uncertainties=['PETG density and printed fit are unmeasured.',
                           'Snaps, ribs, channels and hanger are integral geometry, not separate parts.'])
    add('rod', [raw['rod']], 'Solid fibreglass rod', 'bought',
        {'type':'modelled', 'reference':'Specified 6 x 500 mm stock; purchased.py; S1 does not specify this rod.'},
        'Provides the continuous spine and sharpened soil insertion end.', 'fibreglass_rod',
        uncertainties=['Composite density and incoming rod diameter are unmeasured.'])
    add('cell_18650', [raw[n] for n in ('cell_wrap','positive_terminal','positive_insulator')],
        'Samsung INR18650-25R flat-top cell', 'bought',
        {'type':'datasheet', 'reference':'S5; purchased.py cell(); terminal and insulator details reconstructed'},
        'Supplies electrical energy to the listener.', 'Samsung25R_cell',
        uncertainties=['45 g is the datasheet maximum, not a measured cell mass.', 'Terminal and insulator details are MEASURE envelopes.'])
    for prefix,name,label,key in [('xiao_','xiao_esp32s3','Seeed XIAO ESP32S3','XIAO_ESP32S3'),('wio_','wio_sx1262','Seeed Wio-SX1262 extension','Wio_SX1262')]:
        add(name,[r for r in p['board'] if r[0].startswith(prefix)],label,'bought',
            {'type':'manufacturer STEP and modelled mate','reference':'S4; sources/xiao-manifest.json; native unscaled Seeed OEM solids'},
            'Provides the listener processor and battery charger.' if prefix=='xiao_' else 'Provides the SX1262 LoRa radio through the kit board-to-board connector.',key,
            uncertainties=['Populated mass is MEASURE; stack mating spacing and missing XIAO mating connector require measurement.','No display or firmware status window; source CAD can retain inactive component bodies.'])
    add('inmp441', p['mic'], 'INMP441 microphone breakout', 'bought',
        {'type':'datasheet and modelled', 'reference':'S6 bare IC outline; generic breakout reconstructed in purchased.py'},
        'Senses sound through the side-facing bottom-port acoustic cavity.', 'INMP441_breakout',
        uncertainties=['Breakout outline, port, thickness and 1 g mass are unmeasured.', 'Five short mic wires are modelled; solder-pad labels and wire dress require verification.'])
    for names,name,label,key in [(('lora_FPC','RF_pigtail'),'antenna','Kit LoRa FPC and U.FL coax','LoRa_FPC_and_coax'),(('wifi_FPC','wifi_coax'),'wifi_antenna','Kit WiFi/BLE FPC and coax','WiFi_FPC_and_coax')]:
        add(name,[raw[n] for n in names],label,'bought',
            {'type':'modelled; kit identity from manufacturer','reference':'S4 kit product page identifies included FPC; dimensions unsourced MEASURE'},
            'Radiates LoRa from the top backer.' if name=='antenna' else 'Connects the XIAO WiFi/BLE U.FL to its separate wall-mounted FPC.',key,
            uncertainties=['Exact supplied antenna geometry and mass must be measured.','Cable unplugging and deformation are not simulated.'])
    for n, s, c in p['hardware']:
        if n in ('lora_FPC','RF_pigtail','wifi_FPC','wifi_coax'):
            continue
        source = {'type':'modelled', 'reference':'purchased.py; DESIGN.md BOM'}
        u = ['Material-density mass estimate; actual item has not been weighed.']
        if n.startswith('pod_insert'):
            display, fun = 'Ruthex M2 heat-set insert '+n[-1], 'Provides a metal thread for a pod lid screw.'
            source = {'type':'manufacturer STEP', 'reference':'S9; ruthex-m2x4.step'}
            u += ['Shown lifted for identification; heat-set inserts are installed with heat, not routinely pulled out.']
        elif n.startswith('pod_M2'):
            display, fun = 'M2 x 6 pod lid screw '+n[-1], 'Clamps the service lid onto the pod sealing land.'
            u += ['Threads use major-diameter envelopes; unscrewing is represented by axial translation.']
        elif n.startswith('board_retention'):
            display, fun = 'PCB edge foam pad '+n.split('foam_')[1], 'Cushions the board against a lid retention finger.'
        elif n.startswith('nickel'):
            display, fun = 'Factory-welded cell tab '+n.split('_')[-1], 'Provides a welded electrical connection at a cell terminal.'
            u += ['Offset for identification only; removing a factory weld is not routine service.']
        elif n.startswith('mic_wire'):
            display, fun = n.replace('_',' '), 'Connects INMP441 to the named XIAO I2S or supply pad with a short wire.'
            u += ['Wire dress and solder-pad positions require verification.']
        elif n.startswith('power_wire'):
            display, fun = 'Insulated power wire '+n[-1], 'Routes one battery connection through the protected gutters to the pod.'
            u += ['Rigid displayed route; unplugging, soldering and flexible extraction are not simulated.']
        elif 'tie' in n:
            display, fun = n.replace('_',' ').capitalize(), 'Retains the wiring against the rod or provides body strain relief.'
            source = {'type':'datasheet and modelled', 'reference':'S7 T18R dimensions; fitted closed loop'}
            u += ['Cut the disposable tie before removal; the intact loop is displaced only for identification.']
        else:
            display = {'perimeter_silicone_seal':'Perimeter silicone cord seal',
                       'mic_waterproof_film':'Prototype microphone silicone film',
                       'mic_silicone_cavity_seal':'Microphone cavity silicone seal'}[n]
            fun = {'perimeter_silicone_seal':'Compresses around the service lid perimeter.',
                   'mic_waterproof_film':'Covers the acoustic opening with a prototype soft film.',
                   'mic_silicone_cavity_seal':'Spaces and seals the microphone board around its acoustic cavity.'}[n]
            u += ['Soft-material fit, acoustic response and water sealing are untested; no waterproof rating is claimed.']
            if n.startswith('mic_'): source['reference'] = 'S6a sealing guidance; design-assumption dimensions in purchased.py'
        add(n, [(n,s,c)], display, 'bought', source, fun, uncertainties=u)

    harness = []
    for n, s, c in harness_rows(p):
        canonical = {'harness_plate':'plate', 'release_rotor':'rotor', 'SG90_case_tabs':'sg90',
                     'SG90_stock_double_horn':'sg90_stock_double_horn'}.get(n,n)
        if n == 'SG90_output_spline': continue
        rows = [(n,s,c)]
        group = None
        r = hm.get(canonical) or hm.get(n)
        src = {'type':'modelled', 'reference':'purchased.py; DESIGN.md BOM'}
        kind = 'bought'
        u = ['Material-density mass estimate; actual item has not been weighed.']
        if canonical in ('plate','rotor'):
            kind = 'printed'; src = {'type':'modelled', 'reference':'printed.py; DESIGN.md'}
            display = 'Printed harness plate' if canonical=='plate' else 'Printed release rotor'
            fun = 'Transfers the four dart loads to the aircraft payload rails.' if canonical=='plate' else 'Supports the dart heads and uncovers their release slots as it turns.'
            u = ['PETG density and printed fits are unmeasured.']
        elif canonical in ('sg90','sg90_stock_double_horn'):
            src = {'type':'datasheet and modelled', 'reference':'S3 manufacturer drawing/photo; MEASURE spline and horn'}
            group = 'SG90_with_stock_horn'
            display = 'TowerPro SG90 servo with output spline' if canonical=='sg90' else 'Supplied SG90 double horn'
            fun = 'Rotates the release mechanism through its output spline.' if canonical=='sg90' else 'Transmits servo rotation to the two drive studs.'
            if canonical=='sg90': rows += [r for r in p['servo'] if r[0]=='SG90_output_spline']
            u = ['9 g catalog mass is shared by servo and stock horn; separate masses are unmeasured.', 'Exact servo variant, spline and horn dimensions require measurement.']
        elif 'keeper_spacer' in n:
            display, fun = 'Rotor keeper spacer', 'Sets the loose axial keeper stack above the stock horn.'
        elif 'keeper_washer' in n:
            display, fun = 'Rotor keeper washer', 'Limits rotor lift while leaving a nominal axial running gap.'
        elif 'spline_screw' in n:
            display, fun = 'Replacement output spline screw', 'Fastens the axial keeper stack to the measured servo output thread.'
            u += ['Actual servo thread must be measured; nominal M1.6 is an assumption.']
        elif 'lower_nut' in n or 'upper_nut' in n:
            display, fun = n.replace('_',' ').capitalize(), 'Locks one drive stud against the stock horn.'
            src['reference'] = 'S10 M2 nut envelope; purchased.py'
        elif 'drive_pin' in n:
            display, fun = n.replace('_',' ').capitalize(), 'Engages an axial clearance hole in the release rotor.'
        elif 'mount_nut' in n:
            display, fun = n.replace('_',' ').capitalize(), 'Provides a captive thread for one servo tab fastener.'
        elif 'servo_M2' in n:
            display, fun = n.replace('_',' '), 'Clamps one servo mounting tab under the harness plate.'
        elif 'servo_lead' in n:
            display, fun = n.replace('_',' ').capitalize(), 'Represents one conductor of the servo supply and signal cable.'
            u += ['Flexible cable unplugging and routing are not simulated.']
        elif 'JR_plug' in n:
            display, fun = 'Servo JR connector envelope', 'Represents the removable servo cable connector.'
        elif 'rail_zip' in n:
            display, fun = n.replace('_',' ').capitalize(), 'Secures one printed saddle to an aircraft payload rail.'
            src = {'type':'datasheet and modelled', 'reference':'S7 T18R dimensions; fitted closed loop'}
            u += ['Cut before removal; the rigid closed-loop depiction does not open.']
        elif n=='PTFE_bearing_film':
            display, fun = 'PTFE bearing film', 'Provides the assumed low-friction surface on the plate bearing ridge.'
            src = {'type':'datasheet and modelled', 'reference':'S8 3M 5490 thickness; modelled annular cut strip'}
            u += ['Actual breakaway friction is unmeasured.']
        else: raise ValueError(n)
        harness.append(Part(canonical, rows, facts(display,kind,src,fun,
                            r['mass_g'] if r else None,r['basis'] if r else None,group,u), 'harness'))
    drone=[]
    for n,s,c in p['drone']:
        proxy = n.startswith('prop_swept')
        f=facts(n.replace('_',' ').capitalize(),'bought',
                {'type':'modelled' if proxy else 'manufacturer STEP',
                 'reference':'S2 swept envelope, not a propeller blade model' if proxy else 'S1 Holybro x500v2-frame.step; original solid index retained'},
                'Shows the assumed propeller swept clearance volume.' if proxy else 'Represents one retained stock X500 airframe, rail, landing gear, motor or hardware component.',
                uncertainties=['No aircraft-part masses are available in the mass properties report.'] +
                              (['Swept slab thickness and fitted propeller plane are unmeasured; this is a clearance proxy.'] if proxy else ['Installed aircraft equipment and hardware may differ from the source CAD.']))
        f['is_clearance_proxy']=proxy
        drone.append(Part(n,[(n,s,c)],f,'drone'))
    return dart,harness,drone,mass


# (time, final-offset fraction). Different parts are removed in service order.
def ramp(start,end): return [(0.,0.),(start,0.),(end,1.),(DURATION,1.)]


def dart_offset(n):
    # Pod first withdraws from the square rod end on +X; body withdraws toward
    # the tip on -X. Cell opens +Z; mic assembly opens toward the cavity on -Y.
    if n=='rod': return (0,0,0),ramp(0,1)
    if n.startswith('tail_fin'):
        from parameters import FIN_ANGLES
        import math
        a=math.radians(FIN_ANGLES[int(n[-1])-1])
        return (0,65*math.cos(a),65*math.sin(a)),ramp(1.1,2.0)
    if n.startswith('tail_collar'):return (180 if n.endswith('2') else 150,0,-60),ramp(2,3.3)
    if n=='tail_bond':return (0,-85,-65),ramp(2,3.3)
    if n=='body': return (-300,0,0),ramp(2.0,3.3)
    if n=='cell_18650': return (-300,0,85),None
    if n.startswith('nickel_tab'): return (-318 if n.endswith('77.82') else -282,0,85),None
    x=65
    if n=='pod_shell':return (x,0,0),ramp(2,3.3)
    if n=='pod_lid':return (x,0,125),None
    if n=='xiao_esp32s3':return (x,0,49),None
    if n=='wio_sx1262':return (x,0,72),None
    if n=='usb_cap':return (x+45,0,0),ramp(1,1.9)
    if n=='wifi_antenna':return (x,55,20),None
    if n.startswith('mic_wire'):return (x,-100,32+16*['D3_BCLK','D4_WS','D5_SD','3V3','GND'].index(n[9:])),ramp(3.4,5.0)
    if n=='inmp441':return (x,-70,0),None
    if n=='antenna':return (210,0,0),ramp(1,1.9)
    if n.startswith('pod_M2'):return (x,0,160),None
    if n.startswith('pod_insert'):return (x,0,30),None
    if n=='perimeter_silicone_seal':return (x,0,97),None
    if n=='mic_waterproof_film':return (x,-24,0),None
    if n=='mic_silicone_cavity_seal':return (x,-46,0),None
    if n.startswith('board_retention'):return (x,0,78),None
    if n.startswith('power_wire'):return (0,90 if n.endswith('0') else 104,0),ramp(.6,1.7)
    if 'tie' in n:return (0,47,0),ramp(.1,.6)
    raise ValueError(n)


def harness_offset(n):
    if n=='plate':return (0,0,0),ramp(0,1)
    if n=='rotor':return (0,0,105),ramp(2.1,3.1)
    if n=='sg90':return (0,0,-70),ramp(4.1,5.2)
    if n=='sg90_stock_double_horn':return (0,0,40),ramp(3.1,4.0)
    if 'spline_screw' in n:return (0,0,192),ramp(.2,.8)
    if 'keeper_washer' in n:return (0,0,165),ramp(.8,1.4)
    if 'keeper_spacer' in n:return (0,0,150),ramp(1.4,2.1)
    if 'lower_nut' in n:return (0,0,32),ramp(3.1,4)
    if 'upper_nut' in n:return (0,0,76),ramp(3.1,4)
    if 'drive_pin' in n:return (0,0,50),ramp(3.1,4)
    if 'mount_nut' in n:return (0,0,26),ramp(4.1,5.2)
    if 'servo_M2' in n:return (0,0,-40),ramp(3.3,4.1)
    if 'servo_lead' in n:return (0,-30-5*int(n[-1]),-70),ramp(.2,1.2)
    if 'JR_plug' in n:return (0,-45,-70),ramp(.2,1.2)
    if 'rail_zip' in n:return (0,0,125),ramp(.2,1.2)
    if n=='PTFE_bearing_film':return (0,0,70),ramp(3.1,4)
    raise ValueError(n)


def interpolate(keys,t):
    return float(np.interp(t,[k[0] for k in keys],[k[1] for k in keys]))


def dart_motion(n,t):
    delta,keys=dart_offset(n)
    if keys is not None:return np.asarray(delta)*interpolate(keys,t)
    d=np.asarray(delta,dtype=float)
    # Move the populated pod as one subassembly before opening it, and the
    # cell with its body before lifting the cell out of the integral snaps.
    xstage=ramp(2,3.3)
    zstage=ramp(3.4,5.0)
    if n=='pod_lid':zstage=ramp(3.4,4.2)
    elif n.startswith('pod_M2'):zstage=ramp(3.3,3.7)
    elif n in ('xiao_esp32s3','wio_sx1262'):zstage=ramp(4.4,5.4)
    elif n.startswith('board_retention') or n=='perimeter_silicone_seal':zstage=ramp(4.2,4.7)
    elif n.startswith('pod_insert'):zstage=ramp(5.4,6.3)
    elif n=='cell_18650' or n.startswith('nickel_tab'):zstage=ramp(3.4,4.4)
    elif n=='inmp441':zstage=ramp(4.2,5.1)
    elif n.startswith('mic_'):zstage=ramp(5.1,6.1)
    d[0]*=interpolate(xstage,t)
    d[1:]*=interpolate(zstage,t)
    return d


def instances(model,dart,harness,drone,p):
    """Each instance holds one physical part node, including all loaded darts."""
    rows=[]
    if model=='dart':
        for part in dart:rows.append(dict(part=part,name=part.name,base=np.zeros(3),motion=lambda t,n=part.name:dart_motion(n,t),group='dart'))
        return rows
    if model=='aircraft':
        for part in drone:rows.append(dict(part=part,name=part.name,base=np.zeros(3),motion=lambda t:np.zeros(3),group='airframe'))
    # In aircraft view the entire loaded harness is first removed downwards;
    # only then is its rotor lifted relative to the now separated plate.
    def lower(t):return np.array([0.,0.,-400*interpolate(ramp(.2,2.2),t)]) if model=='aircraft' else np.zeros(3)
    def service_time(t):return max(0.,t-2.2)*DURATION/(DURATION-2.2) if model=='aircraft' else t
    for part in harness:
        delta,keys=harness_offset(part.name)
        def movement(t,delta=delta,keys=keys):return lower(t)+np.asarray(delta)*interpolate(keys,service_time(t))
        rows.append(dict(part=part,name=part.name,base=np.zeros(3),motion=movement,group='harness'))
    for i,(x,y,_) in enumerate(printed.head_positions()):
        base=np.array([x-p['hanger'],y-p['hanger_y'],ROTOR_TOP-HEAD_BOTTOM])
        # Full darts stay rigid; no hidden electronics are discarded.
        drop=145 if i%2==0 else 215
        for part in dart:
            def movement(t,drop=drop):return lower(t)+np.array([0.,0.,-drop*interpolate(ramp(5.3,7.5),service_time(t))])
            rows.append(dict(part=part,name=f'dart{i+1}_{part.name}',base=base,motion=movement,group=f'dart{i+1}'))
    return rows


def verify_exploded(model,inst):
    """Same exact-solid intersection and .02 mm3 threshold as verify.py.

    Populated boards/cells, stock aircraft and the four complete loaded darts
    are retained subassemblies. Their original internal contacts are not new
    exploded collisions. All independently exploded parts are checked against
    one another, with AABB pruning before exact OCP booleans.
    """
    groups={}
    for item in inst:
        group=item['group']
        key=group if group.startswith('dart') and model!='dart' or group=='airframe' else item['name']
        for _,s,_ in item['part'].rows:
            moved=s.translate(tuple(item['base']+item['motion'](DURATION)))
            groups.setdefault(key,[]).append(moved)
    shapes={n:compound(s) for n,s in groups.items()}
    collisions=[];candidates=0;tested=0
    names=list(shapes)
    for i,n in enumerate(names):
        a=shapes[n];aa=xyz_bounds(a)
        for m in names[i+1:]:
            tested+=1;b=shapes[m];bb=xyz_bounds(b)
            if any(min(aa[j+1],bb[j+1])-max(aa[j],bb[j])<1e-5 for j in (0,2,4)):continue
            candidates+=1
            v=overlap(a,b)
            if v>=.02:collisions.append(dict(parts=[n,m],interference_mm3=v))
    result=dict(pass_=not collisions,threshold_mm3=.02,groups=len(shapes),pairs=tested,
                exact_boolean_candidates=candidates,collisions=collisions,
                scope='Final exploded endpoint, exact original B-reps, AABB pruning; retained subassembly internal contacts excluded.',
                motion_scope='Staged presentation, not a continuous collision-free service path or dynamic release simulation.')
    print('EXPLODED',model,json.dumps(result),flush=True)
    return result
