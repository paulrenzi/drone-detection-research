"""CadQuery construction helpers. All coordinates in mm."""
import math
import cadquery as cq

def box(x,y,z,at=(0,0,0)):
    return cq.Workplane('XY').box(x,y,z,centered=(True,True,False)).translate(at).val()

def cyl(r,h,p=(0,0,0),d=(0,0,1)):
    return cq.Solid.makeCylinder(r,h,cq.Vector(*p),cq.Vector(*d))

def cone(r1,r2,h,p=(0,0,0),d=(0,0,1)):
    return cq.Solid.makeCone(r1,r2,h,cq.Vector(*p),cq.Vector(*d))

def rounded(x,y,z,r=2,at=(0,0,0)):
    return cq.Workplane('XY').box(x,y,z,centered=(True,True,False)).edges('|Z').fillet(r).translate(at).val()

def union(*items):
    s=items[0]
    for item in items[1:]:s=s.fuse(item)
    return s.clean()

def compound(parts):return cq.Compound.makeCompound(list(parts))

def sector(ri,ro,angle,span,z,h):
    # Exact circle arcs (not a polygonal gear approximation).
    a=math.radians(angle-span/2); b=math.radians(angle+span/2);m=(a+b)/2
    p=lambda r,t:(r*math.cos(t),r*math.sin(t))
    w=cq.Workplane('XY').workplane(offset=z).moveTo(*p(ri,a)).lineTo(*p(ro,a))
    w=w.threePointArc(p(ro,m),p(ro,b)).lineTo(*p(ri,b)).threePointArc(p(ri,m),p(ri,a)).close()
    return w.extrude(h).val()

def bar(a,b,width,z,h):
    dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy)
    return rounded(L+width,width,h,min(width/2-.01,2),at=(0,0,z)).rotate((0,0,0),(0,0,1),math.degrees(math.atan2(dy,dx))).translate(((a[0]+b[0])/2,(a[1]+b[1])/2,0))

def pipe_path(points,r):
    items=[]
    for a,b in zip(points,points[1:]):
        d=cq.Vector(*b)-cq.Vector(*a)
        items.append(cyl(r,d.Length,a,d.normalized().toTuple()))
    for p in points[1:-1]:items.append(cq.Solid.makeSphere(r,cq.Vector(*p)))
    return union(*items)

def teardrop_x(x0,L,r,y,z):
    # 45 degree roof above round bore: avoids horizontal-bore support material.
    a=r/math.sqrt(2)
    w=cq.Workplane('YZ',origin=(x0,0,0)).moveTo(y-a,z+a)
    w=w.threePointArc((y-r,z),(y,z-r)).threePointArc((y+r,z),(y+a,z+a))
    return w.lineTo(y,z+r*math.sqrt(2)).close().extrude(L).val()

def chamfer(shape,selector,amount):
    return cq.Workplane().add(shape).edges(selector).chamfer(amount).val()

def fillet(shape,selector,amount):
    return cq.Workplane().add(shape).edges(selector).fillet(amount).val()

_BOUND_CACHE={}
def xyz_bounds(s):
    key=s.wrapped
    if key in _BOUND_CACHE:return _BOUND_CACHE[key]
    b=s.BoundingBox()
    result=[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]
    _BOUND_CACHE[key]=result
    return result

def overlap(a,b):
    aa=xyz_bounds(a);bb=xyz_bounds(b)
    if any(min(aa[j+1],bb[j+1])-max(aa[j],bb[j]) < 1e-5 for j in (0,2,4)):return 0.
    # Individual-solid broad phase prevents OCCT from building expensive
    # compound/compound boolean graphs for buried board detail or long darts.
    sa=a.Solids();sb=b.Solids()
    if len(sa)>1 or len(sb)>1:
        return sum(overlap(x,y) for x in sa for y in sb)
    return a.intersect(b).Volume()

def aabb_distance(a,b):
    aa=xyz_bounds(a);bb=xyz_bounds(b)
    return math.sqrt(sum(max(0,bb[j]-aa[j+1],aa[j]-bb[j+1])**2 for j in (0,2,4)))
