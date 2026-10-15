"""Headless shaded renders of CadQuery shapes to PNG, via VTK (ships with cadquery-ocp)."""
import math
import vtk
import cadquery as cq

PALETTE = {
    "print": (0.93, 0.55, 0.16),   # printed PETG
    "print2": (0.30, 0.55, 0.85),
    "board": (0.10, 0.45, 0.25),
    "cell": (0.35, 0.35, 0.40),
    "steel": (0.70, 0.72, 0.75),
    "pole": (0.85, 0.85, 0.70),
    "fur": (0.45, 0.40, 0.35),
    "servo": (0.15, 0.30, 0.75),
    "carbon": (0.18, 0.18, 0.20),
    "ghost": (0.80, 0.80, 0.82),
}


def _poly(shape, tol=0.2):
    if isinstance(shape, cq.Workplane):
        shape = cq.Compound.makeCompound([o for o in shape.vals() if isinstance(o, cq.Shape)])
    verts, tris = shape.tessellate(tol, 0.3)
    pts = vtk.vtkPoints()
    for v in verts:
        pts.InsertNextPoint(v.x, v.y, v.z)
    cells = vtk.vtkCellArray()
    for t in tris:
        cells.InsertNextCell(3)
        for i in t:
            cells.InsertCellPoint(i)
    pd = vtk.vtkPolyData()
    pd.SetPoints(pts)
    pd.SetPolys(cells)
    return pd


def render(parts, path, elev=20, azim=-60, size=(1200, 900), zoom=1.0, edges=True, opacity=None):
    """parts: list of (shape, colour-name-or-rgb). Writes a PNG with a white background."""
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    for i, (shape, col) in enumerate(parts):
        pd = _poly(shape)
        nrm = vtk.vtkPolyDataNormals()
        nrm.SetInputData(pd)
        nrm.SetFeatureAngle(35)
        nrm.SplittingOn()
        m = vtk.vtkPolyDataMapper()
        m.SetInputConnection(nrm.GetOutputPort())
        a = vtk.vtkActor()
        a.SetMapper(m)
        rgb = PALETTE.get(col, col) if isinstance(col, str) else col
        a.GetProperty().SetColor(*rgb)
        a.GetProperty().SetSpecular(0.25)
        a.GetProperty().SetSpecularPower(20)
        if col == "ghost":
            a.GetProperty().SetOpacity(0.35)
        ren.AddActor(a)
        if edges and col not in ("fur", "ghost"):
            fe = vtk.vtkFeatureEdges()
            fe.SetInputData(pd)
            fe.BoundaryEdgesOn()
            fe.FeatureEdgesOn()
            fe.SetFeatureAngle(35)
            fe.ManifoldEdgesOff()
            fe.NonManifoldEdgesOff()
            em = vtk.vtkPolyDataMapper()
            em.SetInputConnection(fe.GetOutputPort())
            em.ScalarVisibilityOff()
            ea = vtk.vtkActor()
            ea.SetMapper(em)
            ea.GetProperty().SetColor(0.1, 0.1, 0.1)
            ea.GetProperty().SetLineWidth(1.2)
            ren.AddActor(ea)
    cam = ren.GetActiveCamera()
    cam.SetViewUp(0, 0, 1)
    cam.SetPosition(math.cos(math.radians(azim)) * math.cos(math.radians(elev)),
                    math.sin(math.radians(azim)) * math.cos(math.radians(elev)),
                    math.sin(math.radians(elev)))
    cam.SetFocalPoint(0, 0, 0)
    ren.ResetCamera()
    cam.Zoom(zoom)
    light = vtk.vtkLight()
    light.SetLightTypeToCameraLight()
    light.SetPosition(-0.4, 0.6, 1)
    ren.AddLight(light)
    win = vtk.vtkRenderWindow()
    win.SetOffScreenRendering(1)
    win.SetMultiSamples(8)
    win.AddRenderer(ren)
    win.SetSize(*size)
    win.Render()
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(win)
    w2i.Update()
    wr = vtk.vtkPNGWriter()
    wr.SetFileName(str(path))
    wr.SetInputConnection(w2i.GetOutputPort())
    wr.Write()
