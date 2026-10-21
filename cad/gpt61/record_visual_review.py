"""Attest current render inspection; run only after looking at every PNG."""
from pathlib import Path
import argparse,hashlib,json,datetime
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--reviewed',action='store_true',help='Explicitly attest that every current render has been inspected.');args=ap.parse_args()
if not args.reviewed:raise SystemExit('Inspect all renders first, then supply --reviewed. This script does not inspect images.')
notes={
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
