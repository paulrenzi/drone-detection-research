"""Refresh derived mass tables/kit quantities from an already verified cache."""
import sys,json
sys.dont_write_bytecode=True
from build import load_cache,mass_report,OUT
p=load_cache();m=mass_report(p)
kits={
 'four_flying_darts_and_harness':dict(body=4,pod_shell=4,pod_lid=4,usb_cap=4,plate=1,rotor=1),
 'one_stake_listener':dict(stake_adapter=1,stake_cell_holder=1,pod_shell=1,pod_lid=1,usb_cap=1),
 'one_inert_dummy':dict(dummy_body=1,dummy_lid=1,dummy_head_insert=1,pod_shell=1,pod_lid=1,usb_cap=1),
 'fit_tool':dict(fit_coupon=1),
}
(OUT/'kits.json').write_text(json.dumps(dict(printed_kits=kits,notes=['All printed parts intentionally100% infill; STLs onZ0 for Vyper.','Stake and dummy are alternatives; do not add their parts to flight payload.','See DESIGN.md for bought hardware, ballast centres and assembly.']),indent=2)+'\n')
print('Mass reports refreshed; dart',m['dart_total_g'],'stake',m['stake']['total_g'],'g')
