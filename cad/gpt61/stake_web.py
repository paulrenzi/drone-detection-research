"""Additional web scene retaining the exact same reusable pod on a garden stake."""
import numpy as np
from exploded import Part,facts,interpolate,ramp
from variants import stake_rows
from build import mass_item
from parameters import M

def make_stake_scene(p,dart,mass):
    rows=stake_rows(p);byname={n:(n,s,c) for n,s,c in rows}
    parts=[];used=set()
    # Reuse source facts and grouped physical bought parts after standing transform.
    for part in dart:
        available=[byname[n] for n,s,c in part.rows if n in byname]
        if not available:continue
        if part.name in ('body','rod'):continue
        parts.append(Part('stake_'+part.name,available,dict(part.facts),'stake'))
        used.update(n for n,s,c in available)
    for n,s,c in rows:
        if n in used:continue
        kind='printed' if n in ('stake_adapter','stake_cell_holder') else 'bought'
        if n in ('cell_wrap','positive_terminal','positive_insulator'):continue
        rho=M.petg_density if kind=='printed' else M.rod_density if n in ('garden_stake','pod_socket_rod_offcut') else 1.45 if 'wire' in n else 1.14
        r=mass_item(n,s,rho,basis='MEASURE nominal density; 100% infill for printed parts')
        f=facts(n.replace('_',' ').capitalize(),kind,{'type':'modelled','reference':'variants.py; printed.py; stake OD and stock properties MEASURE'},
                'Clamps the reusable listener pod or its battery to the hand-placed stake.' if kind=='printed' else 'Provides stake support, retention or battery wiring.',r['mass_g'],r['basis'],uncertainties=['No physical installation or mass measurement.'])
        parts.append(Part(n,[(n,s,c)],f,'stake'))
    inst=[]
    head_names={n for part in dart if part.name not in ('body','rod','cell_18650') for n,s,c in part.rows}
    for part in parts:
        head=any(n in head_names for n,s,c in part.rows)
        # One retained pod subassembly withdraws upward from its offcut socket;
        # remaining stake hardware is a retained assembly, not dismantled here.
        def move(t,head=head):return np.array([0.,0.,100*interpolate(ramp(1,5),t)]) if head else np.zeros(3)
        inst.append(dict(part=part,name=part.name,base=np.zeros(3),motion=move,group='dart_stake_pod' if head else 'airframe'))
    return parts,inst
