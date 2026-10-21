"""Cross-file consistency checks in addition to CAD/STL and Khronos validators."""
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parent
def read(rel):return json.loads((R/rel).read_text(encoding='utf-8'))
m=read('out/mass_properties.json');w=read('web/manifest.json');checks=read('out/checks.json');ex=read('out/export_validation.json')
assert not checks['failed']
assert len(ex['printed'])==14 and all(x['passed'] for x in ex['printed'])
assert abs(sum(r['mass_g'] for r in m['dart'])-m['dart_total_g'])<1e-6
assert abs(sum(r['mass_g'] for r in m['harness'])-m['harness_total_g'])<1e-6
assert abs(4*m['dart_total_g']+m['harness_total_g']-m['carried_payload_g'])<1e-6
assert max(abs(m['dart_cg_mm'][i]-m['hanger_'+('x' if i==0 else 'y')+'_mm']) for i in (0,1))<.02
assert m['dummy']['all_pockets_fit'] and max(abs(v) for v in m['dummy']['cg_error_mm'])<.001
assert set(w['models'])=={'dart','harness','aircraft','stake'}
assert {'schema_version','units','up_axis','animation','models','mass_groups','modelled_mass_totals_g','mass_report','source_register','source_download_register','limitations','web_tessellation','validation','renders'}<=set(w)
assert w['units']=='metres' and w['up_axis']=='Y'
model_masses={}
for name,model in w['models'].items():
 assert model['has_explode_animation'] and model['animation_duration_seconds']==8
 assert (R/'web'/model['file']).stat().st_size==model['size_bytes']
 assert hashlib.sha256((R/'web'/model['file']).read_bytes()).hexdigest()==model['sha256']
 text=json.dumps(model).lower();assert 'heltec' not in text and 'oled' not in text
 known=sum(p['mass_g'] for p in model['parts'] if p['mass_g'] is not None)
 assert all({'node_name','part_name','display_name','printed_or_bought','geometry_source','function','mass_g','mass_basis','mass_measured','mass_group','uncertainties','triangle_count','material_colours'}<=set(p) for p in model['parts'])
 groups={p['mass_group'] for p in model['parts'] if p['mass_g'] is None and p.get('mass_group')}
 known+=sum(w['mass_groups'][g]['mass_g'] for g in groups)
 expected=m['dart_total_g'] if name=='dart' else m['stake']['total_g'] if name=='stake' else m['carried_payload_g']
 assert abs(known-expected)<1e-5,(name,known,expected)
 model_masses[name]=known
rv=read('out/visual_review.json')
pngs={p.name for p in (R/'renders').glob('*.png')}
assert set(rv['renders'])==pngs
for n,row in rv['renders'].items():
 assert row['inspected'] and hashlib.sha256((R/'renders'/n).read_bytes()).hexdigest()==row['sha256']
assert all(v['pass_'] for v in read('web/validation-readback.json').values())
assert all(v['pass_'] for v in read('web/exploded_checks.json').values())
kh=read('web/validation-khronos.json');assert kh['available']
assert all(v['issues']['numErrors']==0 and v['issues']['numWarnings']==0 for v in kh['models'].values())
for r in read('out/print_manifest.json'):
 assert (R/'out'/r['step']).is_file() and (R/'out'/r['stl']).is_file()
assert not (R/'out/bought_heltec_v3.step').exists() and not (R/'renders/bought_heltec.png').exists()
tail=read('out/tail_analysis.json')
assert tail['after']['minimum']['static_margin_body_widths']>=2
assert abs(tail['after']['mass_g']-m['dart_total_g'])<1e-6
assert {'dart_balance.png','dart_fins_detail.png','dart_fall_sequence.png','print_tail_fin.png','print_tail_collar.png'}<=pngs
kit=read('out/kits.json')['printed_kits']['four_flying_darts_and_harness']
assert kit['tail_fin']==16 and kit['tail_collar']==8
for name in ('dart','harness','aircraft'):
 nodes=[p['node_name'] for p in w['models'][name]['parts']]
 assert sum('tail_fin_' in n for n in nodes)==(4 if name=='dart' else 16)
 assert sum('tail_collar_' in n for n in nodes)==(2 if name=='dart' else 8)
result=dict(pass_=True,geometry_checks=len(checks['checks']),printed_parts=14,models=model_masses,render_count=len(pngs),scope='Current report consistency, output identities, GLB mass accounting, tail nodes and kit quantities, all visual-review hashes and validator summaries')
(R/'out/package_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
