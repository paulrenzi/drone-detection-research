"""Four flat PETG feathers and two keyed, bonded end-printed collars.

All model dimensions in mm. The attachment is a prototype bonded joint;
strength, creep, impact retention and aerodynamic response remain untested.
"""
import math
import cadquery as cq
from parameters import *
from geometry import *

def orient(s,angle):
    return s.rotate((0,0,0),(1,0,0),angle).translate((0,0,ROD_Z))

def fin_flat():
    # Canonical panel lies on XY, including both keyed root tabs. Convex
    # corners are small chamfers in plan, so the full bottom face is on bed.
    pts=[(FIN_X0,FIN_ROOT_R),(FIN_TIP_X0,FIN_TIP_R),
         (FIN_TIP_X1,FIN_TIP_R),(FIN_X1,FIN_ROOT_R)]
    s=cq.Workplane('XY').polyline(pts).close().extrude(FIN_T).val()
    for x in FIN_COLLARS:
        tab=box(FIN_COLLAR_L-.4,FIN_ROOT_R-FIN_TAB_R+.1,FIN_T,
                at=(x+FIN_COLLAR_L/2,(FIN_TAB_R+FIN_ROOT_R+.1)/2,0))
        s=s.fuse(tab)
    return s.clean()

def fin(angle):
    return orient(fin_flat().translate((0,0,-FIN_T/2)),angle)

def collar(x):
    s=cyl(FIN_COLLAR_R,FIN_COLLAR_L,(x,0,ROD_Z),(1,0,0))
    s=s.cut(cyl(FIN_BORE_D/2,FIN_COLLAR_L+2,(x-1,0,ROD_Z),(1,0,0)))
    for a in FIN_ANGLES:
        slot=box(FIN_COLLAR_L+2,6.,FIN_SLOT_T,
                 at=(x+FIN_COLLAR_L/2,7.3,-FIN_SLOT_T/2))
        s=s.cut(orient(slot,a))
    # Open axial wire relief bypasses both insulated cell leads; it is clear
    # of all four diagonal keyways. No adhesive in this relief.
    s=s.cut(box(FIN_COLLAR_L+2,8,2.6,at=(x+4,7.4,3.5)))
    return s.clean()

def bond_geometry():
    # Representative cured annular films under the two collars. The weighed
    # total includes fillets in the fin keyways; its mass is a MEASURE input.
    films=[]
    for x in FIN_COLLARS:
        s=cyl(FIN_BORE_D/2,FIN_COLLAR_L,(x,0,ROD_Z),(1,0,0))
        s=s.cut(cyl(M.rod_d/2,FIN_COLLAR_L+2,(x-1,0,ROD_Z),(1,0,0)))
        films.append(s)
    return compound(films)

def printed_shapes():
    return dict(tail_fin=fin(FIN_ANGLES[0]),tail_collar=collar(FIN_COLLARS[0]))

def rows(p):
    return [(f'tail_fin_{i+1}',p['tail_fin'].rotate((0,0,ROD_Z),(1,0,ROD_Z),a-FIN_ANGLES[0]),'fin')
            for i,a in enumerate(FIN_ANGLES)]+[
            (f'tail_collar_{i+1}',p['tail_collar'].translate((x-FIN_COLLARS[0],0,0)),'pod')
            for i,x in enumerate(FIN_COLLARS)]+[('tail_bond',bond_geometry(),'gasket')]

def print_shape(name,s):
    if name=='tail_fin':
        return s.translate((0,0,-ROD_Z)).rotate((0,0,0),(1,0,0),-FIN_ANGLES[0])
    if name=='tail_collar':
        return s.rotate((0,0,0),(0,1,0),-90)
    return s
