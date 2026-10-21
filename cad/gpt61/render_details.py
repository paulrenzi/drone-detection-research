"""Close service view, using the same exact B-reps as all other exports."""
from build import load_cache,RENDERS
from geometry import box
from render_local import render

def service_detail(p):
    clip=box(53,48,30,at=(558.5,0,-2))
    rows=[(p['pod_shell'].intersect(clip),'pod'),(p['pod_lid'].intersect(clip),'lid')]
    rows += [(s,c) for n,s,c in p['board']+p['mic']]
    rows += [(s,c) for n,s,c in p['hardware'] if n.startswith(('mic_wire','pod_M2','pod_insert'))]
    rows.append((p['usb_cap'].translate((25,33,0)),'lid'))
    render(rows,RENDERS/'pod_usb_access.png','USB-C and BOOT/RESET service access',
           'Cap withdrawn then set aside | lid retained | FPC backer cropped for this detail | pin reaches either button from end opening',az=-24,el=26,size=(1600,1100))

if __name__=='__main__':service_detail(load_cache())
