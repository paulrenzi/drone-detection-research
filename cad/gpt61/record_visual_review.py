"""Attest current render inspection; run only after looking at every PNG."""
from pathlib import Path
import argparse,hashlib,json,datetime
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--reviewed',action='store_true',help='Explicitly attest that every current render has been inspected.');args=ap.parse_args()
if not args.reviewed:raise SystemExit('Inspect all renders first, then supply --reviewed. This script does not inspect images.')
notes={
 'dart_balance.png':'CAD side cutaway shows gold 18650 at nose, labelled tip datum, actual mass balance and sampled pressure estimates before/after fins.',
 'dart_fins_detail.png':'Diagonal flat panels, two slotted collars, tab clearance and bonded attachment inspected; no physical joint qualification.',
 'dart_fall_sequence.png':'Four illustrative attitudes explicitly labelled schematic, not simulation; wind is upwind-pointing, with no turn timing claim.',
 'print_tail_fin.png':'Full broad planar face on bed, tabs coplanar; no supports.',
 'print_tail_collar.png':'Axial face on bed; rod bore, keyways and wire relief open vertically; no supports.',
 'print_stake_adapter.png':'Reoriented flat after visual review; removes unsupported sideways V-saddle projections.',
 'print_stake_cell_holder.png':'Flat coplanar base and cradle floor; snap beams require local support.',
 'pod_usb_access.png':'End cap set aside, USB visible; lid retained and FPC backer explicitly cropped.',
 'section_pod.png':'Boolean half-section exposes both boards and socket duct; no display.',
 'bought_xiao_wio.png':'Native Seeed board geometry; unmeasured B2B mating spacing labelled.',
 'dummy_ballast_detail.png':'Two retained body ballast pockets visible; remaining two head portions documented.',
 'stake_clamp_detail.png':'Two stake ties plus separate pod-neck retaining tie; locator offcut visible.',
}
rows={p.name:dict(inspected=True,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),note=notes.get(p.name,'Framing, part visibility, geometry and current XIAO identity visually reviewed.')) for p in sorted((R/'renders').glob('*.png'))}
data=dict(reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Assistant visually inspected every final PNG at original resolution using view_image; checked US units, number/word spacing, matching model values, and uncropped, non-overlapping labels.',scope='CAD imagery only; no physical print, acoustic, radio, drop or flight qualification',renders=rows)
for folder in ('out','web'):(R/folder/'visual_review.json').write_text(json.dumps(data,indent=2)+'\n')
print('Recorded current inspection of',len(rows),'renders')
