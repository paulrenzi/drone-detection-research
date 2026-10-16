"""Independent STEP round-trip and STL topology/volume checks for print files."""
from pathlib import Path
import json, sys, hashlib
sys.dont_write_bytecode=True
import cadquery as cq
import vtk
from geometry import xyz_bounds
ROOT=Path(__file__).resolve().parent
results=[]
for row in json.loads((ROOT/'out'/'print_manifest.json').read_text()):
    n=row['part'];step=ROOT/'out'/row['step'];stl=ROOT/'out'/row['stl']
    solid=cq.importers.importStep(str(step)).val()
    reader=vtk.vtkSTLReader();reader.SetFileName(str(stl));reader.MergingOn();reader.Update()
    poly=reader.GetOutput()
    edge=vtk.vtkFeatureEdges();edge.SetInputData(poly);edge.BoundaryEdgesOn();edge.NonManifoldEdgesOn();edge.FeatureEdgesOff();edge.ManifoldEdgesOff();edge.Update()
    mass=vtk.vtkMassProperties();mass.SetInputData(poly);mass.Update()
    err=abs(mass.GetVolume()-solid.Volume())/solid.Volume()
    passed=solid.isValid() and len(solid.Solids())==1 and edge.GetOutput().GetNumberOfCells()==0 and err<.005
    result=dict(part=n,passed=passed,step_valid=solid.isValid(),step_solids=len(solid.Solids()),stl_triangles=poly.GetNumberOfCells(),boundary_or_nonmanifold_edges=edge.GetOutput().GetNumberOfCells(),cad_volume_mm3=solid.Volume(),stl_volume_mm3=mass.GetVolume(),relative_volume_error=err,stl_bounds=poly.GetBounds())
    results.append(result);print(n,result,flush=True)
files=[]
for path in sorted((ROOT/'out').iterdir()):
    if path.suffix.lower() in ('.stl','.step'):
        data=path.read_bytes();files.append(dict(file=path.name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
(ROOT/'out'/'export_validation.json').write_text(json.dumps(dict(printed=results,files=files),indent=2)+'\n')
if not all(x['passed'] for x in results):raise SystemExit('Export validation failed')
print('All printed STEP round-trips and STL topology/volume checks passed.',flush=True)
