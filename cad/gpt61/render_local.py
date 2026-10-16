"""Deterministic CAD-only VTK renderer. No generated/painted geometry."""
from pathlib import Path
import math
import vtk
import cadquery as cq
from PIL import Image, ImageDraw, ImageFont

COLORS = dict(body=(0.94,.42,.10), pod=(.09,.44,.56), lid=(.16,.62,.69),
    plate=(.92,.53,.13), rotor=(.18,.28,.38), carbon=(.15,.18,.22),
    metal=(.65,.70,.74), gold=(.82,.63,.23), board=(.11,.38,.29),
    oled=(.05,.09,.14), cell=(.16,.60,.47), wire=(.22,.23,.27),
    servo=(.16,.37,.72), horn=(.90,.91,.85), rod=(.84,.80,.62),
    gasket=(.34,.30,.29), soil=(.69,.63,.50), prop=(.58,.69,.75),
    white=(.91,.93,.91), red=(.72,.10,.07))

_cache={}
def poly(s,tol=.18):
    key=(s.hashCode(),tol)
    if key in _cache:return _cache[key]
    vs,ts=s.tessellate(tol,.22)
    pts=vtk.vtkPoints()
    for v in vs:pts.InsertNextPoint(*v.toTuple())
    cells=vtk.vtkCellArray()
    for t in ts:
        cells.InsertNextCell(3)
        for i in t:cells.InsertCellPoint(i)
    pd=vtk.vtkPolyData();pd.SetPoints(pts);pd.SetPolys(cells)
    _cache[key]=pd
    return pd

def render(parts,path,title,subtitle='',az=-56,el=26,size=(1600,1050),scale=None,target=None,edges=False):
    """parts: (shape, color key [,opacity]); orthographic, fitted then explicit scale."""
    ren=vtk.vtkRenderer();ren.SetBackground(.957,.966,.972)
    # Reserve header space instead of painting text over the model (whip tip
    # in a tall view otherwise disappears beneath the annotation band).
    ren.SetViewport(0,0,1,1-112/size[1])
    ren.SetUseDepthPeeling(1);ren.SetMaximumNumberOfPeels(80);ren.SetOcclusionRatio(.05)
    corners=[]
    for row in parts:
        s,col,*op=row
        if isinstance(s,cq.Workplane):s=s.val()
        if s.Volume()<1e-8:continue
        bb=s.BoundingBox()
        corners += [(x,y,z) for x in (bb.xmin,bb.xmax) for y in (bb.ymin,bb.ymax) for z in (bb.zmin,bb.zmax)]
        n=vtk.vtkPolyDataNormals();n.SetInputData(poly(s));n.SetFeatureAngle(45);n.SplittingOn()
        m=vtk.vtkPolyDataMapper();m.SetInputConnection(n.GetOutputPort())
        a=vtk.vtkActor();a.SetMapper(m);p=a.GetProperty()
        p.SetColor(*COLORS.get(col,col));p.SetInterpolationToPhong()
        p.SetAmbient(.28);p.SetDiffuse(.72);p.SetSpecular(.16);p.SetSpecularPower(28)
        p.SetOpacity(op[0] if op else 1.)
        if edges:p.SetEdgeVisibility(1);p.SetEdgeColor(.14,.17,.20);p.SetLineWidth(.6)
        ren.AddActor(a)
    cam=ren.GetActiveCamera();cam.ParallelProjectionOn();cam.SetViewUp(0,0,1)
    d=(math.cos(math.radians(az))*math.cos(math.radians(el)),math.sin(math.radians(az))*math.cos(math.radians(el)),math.sin(math.radians(el)))
    cam.SetPosition(*(v*2000 for v in d));cam.SetFocalPoint(0,0,0)
    ren.ResetCamera()
    horizontal=math.hypot(d[0],d[1])
    right=(-d[1]/horizontal,d[0]/horizontal,0)
    up=(-d[0]*d[2]/horizontal,-d[1]*d[2]/horizontal,horizontal)
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    rb=[dot(p,right) for p in corners];ub=[dot(p,up) for p in corners];db=[dot(p,d) for p in corners]
    rc=(min(rb)+max(rb))/2;uc=(min(ub)+max(ub))/2;dc=(min(db)+max(db))/2
    focal=target if target is not None else tuple(right[i]*rc+up[i]*uc+d[i]*dc for i in range(3))
    cam.SetFocalPoint(*focal);cam.SetPosition(*(focal[i]+d[i]*2000 for i in range(3)))
    aspect=size[0]/(size[1]-112)
    fitted=max((max(ub)-min(ub))/2,(max(rb)-min(rb))/(2*aspect))*1.09
    cam.SetParallelScale(scale if scale else fitted)
    ren.ResetCameraClippingRange()
    for pos,intensity in [((-.6,-.5,1),.8),((.5,.7,.6),.5)]:
        light=vtk.vtkLight();light.SetLightTypeToCameraLight();light.SetPosition(*pos);light.SetIntensity(intensity);ren.AddLight(light)
    win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetMultiSamples(0);win.SetAlphaBitPlanes(1)
    win.AddRenderer(ren);win.SetSize(*size);win.Render()
    snap=vtk.vtkWindowToImageFilter();snap.SetInput(win);snap.Update()
    out=vtk.vtkPNGWriter();out.SetFileName(str(path));out.SetInputConnection(snap.GetOutputPort());out.Write();win.Finalize()
    im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im)
    try:
        f=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',30)
        sf=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',19)
    except OSError:f=sf=ImageFont.load_default()
    draw.rectangle((0,0,size[0],111), fill=(244,247,249))
    draw.text((35,18),title,fill=(28,48,61),font=f)
    lines=[];line=''
    for word in subtitle.split():
        test=(line+' '+word).strip()
        if line and draw.textlength(test,font=sf)>size[0]-72:lines.append(line);line=word
        else:line=test
    if line:lines.append(line)
    for i,line in enumerate(lines[:2]):draw.text((36,62+i*24),line,fill=(67,83,93),font=sf)
    im.save(path)
    print('render',Path(path).name,flush=True)
