"""Refresh the optional stake wiring without changing flight/printed geometry."""
import sys,json
sys.dont_write_bytecode=True
from build import load_cache,mass_report,assembly,OUT
from variants import stake_rows,stake_local_rows,render_variants
from geometry import overlap
p=load_cache();rows=stake_local_rows(p);raw={n:s for n,s,c in rows}
checks=json.loads((OUT/'checks.json').read_text())
new=[]
for n in ('stake_power_wire_0','stake_power_wire_1'):
 for target in ('stake_adapter','stake_cell_holder','pod_shell','pod_lid'):
  v=overlap(raw[n],raw[target]);new.append(dict(check=n+'_to_'+target,pass_=v<.02,interference_mm3=v));print(new[-1],flush=True)
v=overlap(raw['stake_power_wire_0'],raw['stake_power_wire_1']);new.append(dict(check='stake_separate_power_wires',pass_=v<.02,interference_mm3=v));print(new[-1],flush=True)
assert all(r['pass_'] for r in new)
names={r['check'] for r in new};checks['checks']=[r for r in checks['checks'] if r['check'] not in names]+new
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(OUT/'checks.md').write_text('# Generated geometry checks\n\n'+'\n'.join(f'- {"PASS" if r["pass_"] else "FAIL"}: {r["check"]} - '+json.dumps({k:v for k,v in r.items() if k not in ('check','pass_')}) for r in checks['checks'])+'\n')
mass_report(p);assembly(stake_rows(p),'Stake_listener',OUT/'stake_assembled.step');render_variants(p)
print('Stake wiring refreshed; existing verified geometric parts unchanged.',flush=True)
