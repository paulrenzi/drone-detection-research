"""Regenerate exploded PNGs, animated GLBs, manifest and verification reports.

From the repository root:
  C:\\Users\\paulm\\.venvs\\cad\\Scripts\\python.exe cad/gpt61/web_export.py

Uses the existing B-rep cache and mass report. Never invokes build/export_all,
never changes source geometry, and never writes to out/. All temporary files,
including npm's cache if the validator needs installing, stay in this folder.
"""
from pathlib import Path
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import math
import shutil
import struct
import subprocess
import time
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
import trimesh
from exploded import (ROOT, DURATION, make_parts, instances, verify_exploded,
                      load_cache)
from render_local import COLORS

WEB=ROOT/'web'
TMP=ROOT/'tmp'
MESH_CACHE=TMP/'web-meshes'
TIMES=np.array(sorted(set([0.,DURATION]+[round(i*.1,3) for i in range(81)])),dtype='<f4')
VERSION='web-xiao-2'


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()


def protected_snapshot():
    paths=list((ROOT/'out').glob('*'))
    paths += [ROOT/n for n in ('build.py','printed.py','purchased.py','parameters.py','geometry.py')]
    paths += list((ROOT/'cache').glob('*'))
    return {str(f.relative_to(ROOT)).replace('\\','/'):dict(bytes=f.stat().st_size,sha256=sha(f))
            for f in paths if f.is_file()}


def polydata(vertices,faces):
    p=vtk.vtkPolyData();pts=vtk.vtkPoints()
    pts.SetData(numpy_to_vtk(np.asarray(vertices,dtype=np.float64),deep=True));p.SetPoints(pts)
    cells=vtk.vtkCellArray()
    offsets=(np.arange(len(faces)+1)*3).astype(np.int64)
    connectivity=np.asarray(faces,dtype=np.int64).ravel()
    cells.SetData(vtk.util.numpy_support.numpy_to_vtkIdTypeArray(offsets,deep=True),
                  vtk.util.numpy_support.numpy_to_vtkIdTypeArray(connectivity,deep=True))
    p.SetPolys(cells)
    return p


def mesh_part(part):
    sources=''.join(sha(ROOT/n) for n in ('parameters.py','printed.py','purchased.py','variants.py','stake_web.py'))
    fingerprint=hashlib.sha256((VERSION+part.name+(':oem3000' if part.family=='drone' else '')+sha(ROOT/'cache/model.json')+sources).encode()).hexdigest()[:20]
    path=MESH_CACHE/(fingerprint+'.npz')
    if path.exists():
        z=np.load(path);count=int(z['count'])
        return dict(center=z['center'],primitives=[dict(vertices=z[f'v{i}'],normals=z[f'n{i}'],faces=z[f'f{i}'],color=tuple(z[f'c{i}'])) for i in range(count)],
                    source_triangles=int(z['source_triangles']),web_triangles=int(z['web_triangles']))
    buckets={};source_count=0
    printed=part.facts['printed_or_bought']=='printed'
    tol,ang=(.10,.18) if printed else (.40,.65) if part.family=='drone' else (.20,.40)
    for n,s,c in part.rows:
        col=tuple(COLORS.get(c,c)) if isinstance(c,str) else tuple(c)
        vs,fs=s.tessellate(tol,ang)
        if not fs:continue
        v=np.array([q.toTuple() for q in vs],dtype=float);f=np.asarray(fs,dtype=np.int64)
        source_count+=len(f)
        bucket=buckets.setdefault(col,[]);bucket.append((v,f))
    b=part.shape.BoundingBox()
    center=np.array([(b.xmin+b.xmax)/2,(b.ymin+b.ymax)/2,(b.zmin+b.zmax)/2])
    primitives=[]
    for col,chunks in buckets.items():
        vs=[];fs=[];offset=0
        for v,f in chunks:vs.append(v);fs.append(f+offset);offset+=len(v)
        v=np.vstack(vs);f=np.vstack(fs)
        # Remove only zero-area tessellation artefacts; original CAD is intact.
        ok=np.linalg.norm(np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]),axis=1)>1e-12
        # Tessellation can leave unused vertices after degenerate faces are
        # removed. They have no surface normal and must not enter a glTF mesh.
        used,remap=np.unique(f[ok].ravel(),return_inverse=True)
        pd=polydata(v[used],remap.reshape(-1,3))
        # Manufacturer detail can dwarf the frame silhouette. VTK is already
        # installed in the CAD environment; no geometry replacement is used.
        cap=3000 if part.family=='drone' else 14000 if part.name in ('xiao_esp32s3','wio_sx1262') else None
        if cap and pd.GetNumberOfCells()>cap:
            dec=vtk.vtkQuadricDecimation();dec.SetInputData(pd)
            dec.SetTargetReduction(1-cap/pd.GetNumberOfCells());dec.VolumePreservationOn();dec.Update();pd=dec.GetOutput()
        pv=vtk_to_numpy(pd.GetPoints().GetData())
        pf=vtk_to_numpy(pd.GetPolys().GetConnectivityArray()).reshape(-1,3)
        good=np.linalg.norm(np.cross(pv[pf[:,1]]-pv[pf[:,0]],pv[pf[:,2]]-pv[pf[:,0]]),axis=1)>1e-12
        used,remap=np.unique(pf[good].ravel(),return_inverse=True)
        pd=polydata(pv[used],remap.reshape(-1,3))
        normal=vtk.vtkPolyDataNormals();normal.SetInputData(pd);normal.SetFeatureAngle(40)
        normal.SplittingOn();normal.ConsistencyOn();normal.ComputePointNormalsOn();normal.ComputeCellNormalsOff();normal.Update()
        result=normal.GetOutput()
        v=vtk_to_numpy(result.GetPoints().GetData()).astype(float)
        f=vtk_to_numpy(result.GetPolys().GetConnectivityArray()).reshape(-1,3).copy()
        n=vtk_to_numpy(result.GetPointData().GetNormals()).astype(float)
        assert np.all(np.linalg.norm(n,axis=1)>1e-8),('Zero web normal',part.name)
        n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-20)
        primitives.append(dict(vertices=(v-center).astype('<f4'),normals=n.astype('<f4'),faces=f.astype('<u4'),color=col))
    total=sum(len(c['faces']) for c in primitives)
    data=dict(count=len(primitives),center=center,source_triangles=source_count,web_triangles=total)
    for i,c in enumerate(primitives):data.update({f'v{i}':c['vertices'],f'n{i}':c['normals'],f'f{i}':c['faces'],f'c{i}':c['color']})
    np.savez_compressed(path,**data)
    print('MESH',part.name,source_count,'->',total,flush=True)
    return dict(center=center,primitives=primitives,source_triangles=source_count,web_triangles=total)


def y_up(v,scale=True):
    a=np.asarray(v)
    return a[..., [0,2,1]]*np.array([1,1,-1])/(1000 if scale else 1)


class GLB:
    def __init__(self):
        self.bin=bytearray()
        self.doc=dict(asset=dict(version='2.0',generator='gpt61/web_export.py; original CAD in millimetres, web in metres'),
                      scene=0,scenes=[dict(name='Carried mechanical prototype',nodes=[])],
                      nodes=[],meshes=[],materials=[],accessors=[],bufferViews=[],buffers=[])
        self.materials={};self.meshes={}

    def accessor(self,array,kind,target=None):
        a=np.ascontiguousarray(array)
        while len(self.bin)%4:self.bin.append(0)
        view=dict(buffer=0,byteOffset=len(self.bin),byteLength=a.nbytes)
        if target:view['target']=target
        vi=len(self.doc['bufferViews']);self.doc['bufferViews'].append(view);self.bin.extend(a.tobytes())
        dtype={np.dtype('<f4'):5126,np.dtype('<u4'):5125,np.dtype('<u2'):5123}[a.dtype]
        acc=dict(bufferView=vi,componentType=dtype,count=len(a),type=kind)
        if kind=='SCALAR':acc.update(min=[float(a.min())],max=[float(a.max())])
        elif kind=='VEC3':acc.update(min=a.min(axis=0).astype(float).tolist(),max=a.max(axis=0).astype(float).tolist())
        ai=len(self.doc['accessors']);self.doc['accessors'].append(acc)
        return ai

    def material(self,color,part):
        alpha=.14 if part.facts.get('is_clearance_proxy') else 1.
        metal=.7 if color==COLORS['metal'] else .65 if color==COLORS['gold'] else 0.
        rough=.38 if metal else .72
        key=(*color,alpha,metal,rough)
        if key not in self.materials:
            name=next((k for k,c in COLORS.items() if tuple(c)==tuple(color)),'custom')
            m=dict(name=name+('_clearance' if alpha<1 else ''),pbrMetallicRoughness=dict(baseColorFactor=[*color,alpha],metallicFactor=metal,roughnessFactor=rough),doubleSided=False)
            if alpha<1:m['alphaMode']='BLEND';m['doubleSided']=True
            self.materials[key]=len(self.doc['materials']);self.doc['materials'].append(m)
        return self.materials[key]

    def mesh(self,part,mesh):
        key=part.family+':'+part.name
        if key in self.meshes:return self.meshes[key]
        prim=[]
        for c in mesh['primitives']:
            v=y_up(c['vertices']).astype('<f4');n=y_up(c['normals'],False).astype('<f4')
            # Re-normalize after float32 conversion for strict glTF validation.
            lengths=np.linalg.norm(n,axis=1,keepdims=True)
            assert np.all(lengths>1e-8),('Zero glTF normal',part.name)
            n/=lengths
            idx=c['faces'].astype('<u2' if len(v)<=65535 else '<u4').ravel()
            prim.append(dict(attributes=dict(POSITION=self.accessor(v,'VEC3',34962),NORMAL=self.accessor(n,'VEC3',34962)),indices=self.accessor(idx,'SCALAR',34963),material=self.material(c['color'],part),mode=4))
        mi=len(self.doc['meshes']);self.doc['meshes'].append(dict(name=part.name,primitives=prim));self.meshes[key]=mi
        return mi

    def save(self,path):
        self.doc['buffers']=[dict(byteLength=len(self.bin))]
        data=json.dumps(self.doc,separators=(',',':'),ensure_ascii=True).encode()
        data+=b' '*((-len(data))%4);self.bin+=b'\0'*((-len(self.bin))%4)
        with path.open('wb') as f:
            f.write(struct.pack('<4sII',b'glTF',2,12+8+len(data)+8+len(self.bin)))
            f.write(struct.pack('<I4s',len(data),b'JSON'));f.write(data)
            f.write(struct.pack('<I4s',len(self.bin),b'BIN\0'));f.write(self.bin)


def export_glb(name,inst,meshes,origin):
    glb=GLB();time_accessor=glb.accessor(TIMES,'SCALAR')
    anim=dict(name='explode',samplers=[],channels=[],extras=dict(duration_seconds=DURATION,description='Staged rigid presentation translations; see manifest motion limitations.'))
    part_facts=[];triangles=0
    for i,item in enumerate(inst):
        part=item['part'];m=meshes[part.family+':'+part.name]
        pos=m['center']+item['base']-origin
        node=dict(name=item['name'],mesh=glb.mesh(part,m),translation=y_up(pos).tolist(),
                  extras=dict(part_name=part.name,display_name=part.facts['display_name'],group=item['group'],printed_or_bought=part.facts['printed_or_bought']))
        glb.doc['nodes'].append(node);glb.doc['scenes'][0]['nodes'].append(i)
        samples=np.array([y_up(pos+item['motion'](float(t))) for t in TIMES],dtype='<f4')
        # Static airframe nodes need no animation channel; all moving part nodes
        # receive translations, without matrices or geometry morphs.
        if np.max(np.abs(samples-samples[0]))>1e-8:
            sampler=len(anim['samplers']);anim['samplers'].append(dict(input=time_accessor,output=glb.accessor(samples,'VEC3'),interpolation='LINEAR'))
            anim['channels'].append(dict(sampler=sampler,target=dict(node=i,path='translation')))
        tris=sum(len(c['faces']) for c in m['primitives']);triangles+=tris
        f=dict(node_name=item['name'],part_name=part.name,**part.facts,
               triangle_count=tris,material_colours=[dict(name=glb.doc['materials'][glb.material(c['color'],part)]['name'],**glb.doc['materials'][glb.material(c['color'],part)]['pbrMetallicRoughness']) for c in m['primitives']],
               assembled_translation_m=y_up(pos).tolist(),exploded_translation_m=y_up(pos+item['motion'](DURATION)).tolist(),
               explode_offset_mm_z_up=item['motion'](DURATION).tolist())
        part_facts.append(f)
    glb.doc['animations']=[anim]
    glb.doc['extras']=dict(units='metres',up_axis='Y',origin_in_original_cad_mm=origin.tolist(),
                          prototype_only=True,motion_is_physical_simulation=False)
    path=WEB/(name+'.glb');glb.save(path)
    unique_triangles=sum(sum(len(c['faces']) for c in meshes[k]['primitives']) for k in glb.meshes)
    return dict(file=path.name,size_bytes=path.stat().st_size,sha256=sha(path),triangle_count=triangles,
                unique_mesh_triangle_count=unique_triangles,node_count=len(inst),mesh_count=len(glb.doc['meshes']),
                has_explode_animation=True,animation_name='explode',animation_duration_seconds=DURATION,
                animated_node_count=len(anim['channels']),orientation='Dart long axis +X, carried horizontal; glTF +Y is up.',
                origin_cad_mm_z_up=origin.tolist(),parts=part_facts)


def read_glb(path):
    data=path.read_bytes();magic,version,length=struct.unpack_from('<4sII',data)
    assert magic==b'glTF' and version==2 and length==len(data)
    jlen,kind=struct.unpack_from('<I4s',data,12);assert kind==b'JSON'
    doc=json.loads(data[20:20+jlen]);off=20+jlen
    blen,kind=struct.unpack_from('<I4s',data,off);assert kind==b'BIN\0'
    return doc,data[off+8:off+8+blen]


def decode(doc,blob,index):
    a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']]
    width={'SCALAR':1,'VEC3':3}[a['type']]
    dtype={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']]
    out=np.frombuffer(blob,dtype=dtype,count=a['count']*width,offset=v.get('byteOffset',0)+a.get('byteOffset',0))
    return out.reshape(a['count'],width) if width>1 else out


def validate_readback(name,info,inst,meshes):
    path=WEB/info['file'];doc,blob=read_glb(path)
    budget=20_000_000 if name=='aircraft' else 8_000_000
    assert path.stat().st_size<=budget,(name,path.stat().st_size,budget)
    assert len(doc['nodes'])==len(inst)
    assert len(set(n['name'] for n in doc['nodes']))==len(inst)
    a=doc['animations'];assert len(a)==1 and a[0]['name']=='explode'
    origin=np.array(info['origin_cad_mm_z_up'])
    channels={c['target']['node']:c for c in a[0]['channels']}
    endpoint_error=0.;triangle_count=0;state_bounds={k:[] for k in ('assembled','exploded')}
    for i,(node,item) in enumerate(zip(doc['nodes'],inst)):
        assert node['name']==item['name']
        m=meshes[item['part'].family+':'+item['part'].name]
        start=y_up(m['center']+item['base']-origin)
        end=start+y_up(item['motion'](DURATION))
        actual_start=np.array(node['translation']);actual_end=actual_start
        if i in channels:
            c=channels[i];s=a[0]['samplers'][c['sampler']]
            t=decode(doc,blob,s['input']);samples=decode(doc,blob,s['output'])
            assert float(t[0])==0 and float(t[-1])==DURATION and np.all(np.diff(t)>0)
            actual_start=samples[0];actual_end=samples[-1]
            # Compare EVERY animation sample with the source transforms.
            expect=np.array([start+y_up(item['motion'](float(q))) for q in t])
            endpoint_error=max(endpoint_error,float(np.abs(samples-expect).max()))
        endpoint_error=max(endpoint_error,float(np.abs(actual_start-start).max()),float(np.abs(actual_end-end).max()))
        for pr in doc['meshes'][node['mesh']]['primitives']:
            v=decode(doc,blob,pr['attributes']['POSITION']);n=decode(doc,blob,pr['attributes']['NORMAL']);idx=decode(doc,blob,pr['indices'])
            assert np.isfinite(v).all() and np.isfinite(n).all() and idx.max()<len(v) and len(idx)%3==0
            assert np.max(np.abs(np.linalg.norm(n,axis=1)-1))<1e-5
            triangle_count+=len(idx)//3
            for key,tr in (('assembled',actual_start),('exploded',actual_end)):
                state_bounds[key]+=[(v+tr).min(axis=0),(v+tr).max(axis=0)]
    assert endpoint_error<2e-6,endpoint_error
    assert triangle_count==info['triangle_count']
    scene=trimesh.load(path,force='scene',process=False)
    assert isinstance(scene,trimesh.Scene) and len(scene.geometry)>0
    states={k:dict(min_m=np.min(v,axis=0).tolist(),max_m=np.max(v,axis=0).tolist()) for k,v in state_bounds.items()}
    return dict(pass_=True,readers=['GLB binary + accessor round-trip','trimesh.Scene'],
                size_budget_bytes=budget,node_count=len(doc['nodes']),triangle_count=triangle_count,
                unique_mesh_count=len(doc['meshes']),animation_samples=len(TIMES),
                max_animation_translation_error_m=endpoint_error,bounds=states)


def khronos_validate(skip_install=False):
    js=ROOT/'validate_web.cjs'
    dependency=TMP/'web-validator/node_modules/gltf-validator'
    if not dependency.exists() and not skip_install:
        npm=shutil.which('npm.cmd') or shutil.which('npm')
        if npm:
            subprocess.run([npm,'install','--prefix',str(TMP/'web-validator'),'--cache',str(TMP/'npm-cache'),'--no-audit','--no-fund','gltf-validator@2.0.0-dev.3.10'],check=True,cwd=ROOT)
    node=shutil.which('node')
    if node and dependency.exists():
        subprocess.run([node,str(js)],check=True,cwd=ROOT)
        return json.loads((WEB/'validation-khronos.json').read_text())
    result=dict(available=False,reason='Node/npm or gltf-validator unavailable; binary and trimesh read-back still required.')
    (WEB/'validation-khronos.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def camera_render(inst,meshes,path,title,subtitle,az=-65,el=28,size=(2000,1200),
                  selected=None,labels=(),crop_heads=False):
    """Render the exact web tessellation. Original CAD shapes are never edited."""
    from PIL import Image,ImageDraw,ImageFont
    ren=vtk.vtkRenderer();ren.SetBackground(.957,.966,.972)
    ren.SetViewport(0,0,1,1-125/size[1]);ren.SetUseDepthPeeling(1);ren.SetMaximumNumberOfPeels(100)
    anchors={};allpts=[]
    datum=json.loads((ROOT/'cache/model.json').read_text())
    for item in inst:
        if selected and not selected(item):continue
        part=item['part'];m=meshes[part.family+':'+part.name]
        delta=m['center']+item['base']+item['motion'](DURATION)
        anchors[item['name']]=delta
        # Leader lines terminate on actual material, rather than the empty
        # centre of an annulus or the centre of a tall part's bounding box.
        anchor_points={'plate':(0,-49.5,5), 'rotor':(46,0,15.2),
                       'body':(datum['hanger'],datum['hanger_y'],35),
                       'pod_lid':(558,0,18.5),'pod_shell':(558,-15.2,5),
                       'perimeter_silicone_seal':(536.9,0,16.55),
                       'PTFE_bearing_film':(0,-49.5,11.96),
                       'power_wire_1':(300,5.7,4.8)}
        if part.name in anchor_points:
            anchors[item['name']]=np.array(anchor_points[part.name])+item['base']+item['motion'](DURATION)
        for c in m['primitives']:
            v=c['vertices']+delta;f=c['faces']
            if crop_heads and item['group'].startswith('dart'):
                if part.name!='body':continue
                # Display-only section around the hanger; GLB keeps full darts.
                head=printed_head(item,delta-m['center'])
                vf=v[f]
                keep=np.all((np.abs(vf[:,:,0]-head[0])<22)&(vf[:,:,2]>head[2]-40),axis=1)
                f=f[keep]
                if not len(f):continue
                allpts.append(v[np.unique(f)].copy())
                anchors[item['name']]=head
            else:allpts.append(v.copy())
            pd=polydata(v,f);pd.GetPointData().SetNormals(numpy_to_vtk(c['normals'],deep=True))
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(pd)
            actor=vtk.vtkActor();actor.SetMapper(mapper);prop=actor.GetProperty();prop.SetColor(*c['color'])
            prop.SetInterpolationToPhong();prop.SetAmbient(.28);prop.SetDiffuse(.72);prop.SetSpecular(.16);prop.SetSpecularPower(28)
            if part.facts.get('is_clearance_proxy'):prop.SetOpacity(.12)
            ren.AddActor(actor)
    cam=ren.GetActiveCamera();cam.ParallelProjectionOn();cam.SetViewUp(0,0,1)
    az=math.radians(az);el=math.radians(el);d=np.array([math.cos(az)*math.cos(el),math.sin(az)*math.cos(el),math.sin(el)])
    right=np.array([-math.sin(az),math.cos(az),0]);up=np.cross(d,right)
    vertices=np.vstack(allpts);projected=np.column_stack([vertices@right,vertices@up,vertices@d])
    lo=projected.min(axis=0);hi=projected.max(axis=0);mid=(lo+hi)/2
    focal=right*mid[0]+up*mid[1]+d*mid[2]
    cam.SetFocalPoint(*focal);cam.SetPosition(*(focal+3000*d))
    aspect=size[0]/(size[1]-125);cam.SetParallelScale(max((hi[1]-lo[1])/2,(hi[0]-lo[0])/(2*aspect))*1.22)
    ren.ResetCameraClippingRange()
    for pos,intensity in [((-.6,-.5,1),.8),((.5,.7,.6),.5)]:
        light=vtk.vtkLight();light.SetLightTypeToCameraLight();light.SetPosition(*pos);light.SetIntensity(intensity);ren.AddLight(light)
    win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetMultiSamples(0);win.SetAlphaBitPlanes(1);win.AddRenderer(ren);win.SetSize(*size);win.Render()
    projected_anchors={}
    for n,p in anchors.items():
        ren.SetWorldPoint(*p,1);ren.WorldToDisplay();x,y,_=ren.GetDisplayPoint();projected_anchors[n]=(x,size[1]-y)
    snap=vtk.vtkWindowToImageFilter();snap.SetInput(win);snap.Update();out=vtk.vtkPNGWriter();out.SetFileName(str(path));out.SetInputConnection(snap.GetOutputPort());out.Write();win.Finalize()
    im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im)
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',21);bold=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',31)
    draw.rectangle((0,0,size[0],124),fill=(244,247,249));draw.text((35,18),title,font=bold,fill=(28,48,61))
    draw.text((35,66),subtitle,font=font,fill=(67,83,93))
    for name,text,xy in labels:
        if name not in projected_anchors:continue
        x,y=xy[0]*size[0],xy[1]*size[1];anchor=projected_anchors[name]
        box=draw.textbbox((x,y),text,font=font);box=(box[0]-8,box[1]-4,box[2]+8,box[3]+4)
        endpoint=(box[0] if anchor[0]<x else box[2],(box[1]+box[3])/2)
        draw.line([anchor,endpoint],fill=(104,120,132),width=2);draw.ellipse((anchor[0]-3,anchor[1]-3,anchor[0]+3,anchor[1]+3),fill=(56,75,88))
        draw.rectangle(box,fill=(244,247,249));draw.text((x,y),text,font=font,fill=(28,48,61))
    im.save(path);print('RENDER',path.name,flush=True)


def printed_head(item,translation):
    # original hanger head centre in dart coordinates
    meta=json.loads((ROOT/'cache/model.json').read_text())
    return np.array([meta['hanger'],meta['hanger_y'],51.6])+translation


def render_all(scenes,meshes):
    render=ROOT/'renders'
    camera_render(scenes['dart'],meshes,render/'dart_exploded.png',
                  'Exploded listener - complete modelled parts',
                  'Body withdraws toward tip; pod withdraws from rod end; cell and lid open upward. Integral snaps stay on body.',
                  az=-80,el=27,size=(2200,1200),labels=[('body','Body + integral snaps / hanger',(.025,.77)),('rod','Solid 500 mm rod',(.35,.80)),('cell_18650','18650 cell',(.04,.31)),('pod_shell','Pod tray',(.66,.78)),('antenna','Kit LoRa FPC + U.FL lead',(.81,.57)),('power_wire_1','Both power wires',(.37,.29))])
    camera_render(scenes['dart'],meshes,render/'dart_exploded_pod.png',
                  'Exploded pod - electronics, seal and fasteners',
                  'Seeed XIAO + Wio stack; generic INMP441; USB service cap. Antenna envelope, stack fit and masses remain MEASURE.',
                  selected=lambda i:(i['part'].name.startswith(('pod_','mic_','board_retention','perimeter')) and not i['part'].name.startswith('mic_wire')) or i['part'].name in ('xiao_esp32s3','wio_sx1262','inmp441','usb_cap'),
                  az=-58,el=25,size=(1700,1500),labels=[('pod_M2x6_0','Three M2 x 6 screws',(.02,.16)),('pod_lid','Service lid + pressure fingers',(.40,.25)),('perimeter_silicone_seal','Silicone perimeter cord',(.67,.39)),('board_retention_foam_565_8.3','Four foam pads',(.68,.49)),('wio_sx1262','Wio-SX1262 extension',(.65,.54)),('xiao_esp32s3','XIAO ESP32S3',(.65,.64)),('pod_insert_2','Three heat-set inserts',(.66,.68)),('pod_shell','Tray + ribs / channels',(.65,.83)),('inmp441','INMP441 breakout',(.02,.70)),('mic_waterproof_film','Soft film',(.06,.83)),('mic_silicone_cavity_seal','Cavity seal',(.02,.77))])
    camera_render(scenes['harness'],meshes,render/'harness_exploded.png',
                  'Exploded harness - four complete listeners',
                  'Keeper lifts first, then rotor / horn; darts move down after the retained head support is removed.',
                  az=-65,el=23,size=(2200,1500),labels=[('rotor','Release rotor',(.54,.27)),('plate','Plate + four rail saddles',(.73,.48)),('sg90','SG90 servo',(.70,.60)),('dart1_body','Dart 1 / 3: first tier',(.02,.65)),('dart2_body','Dart 2 / 4: second tier',(.03,.83)),('SG90_spline_screw','Keeper screw',(.65,.16))])
    camera_render(scenes['harness'],meshes,render/'harness_exploded_detail.png',
                  'Harness stack detail - heads sectioned for clarity',
                  'Complete darts remain in the GLB. Ties, wires, hardware and keeper are displaced; the plate geometry is unchanged.',
                  az=-58,el=22,size=(1700,1700),crop_heads=True,
                  labels=[('SG90_spline_screw','Keeper screw',(.64,.15)),('rotor_keeper_washer','Keeper washer',(.64,.21)),('rotor_keeper_spacer','Keeper spacer',(.64,.28)),('rotor','Rotor',(.69,.36)),('PTFE_bearing_film','PTFE film',(.02,.43)),('sg90_stock_double_horn','Stock horn + drive studs / nuts',(.62,.48)),('plate','Printed plate + saddles',(.68,.57)),('sg90','SG90 + output spline',(.65,.70)),('dart1_body','Hanger on complete dart',(.64,.86))])
    camera_render(scenes['aircraft'],meshes,render/'aircraft_exploded.png',
                  'Exploded carried assembly - Holybro X500 V2',
                  'Payload first lowers 400 mm clear of the airframe; harness then opens and the four rigid darts lower into two tiers.',
                  az=-56,el=16,size=(2100,2100),labels=[('x500_frame_000','Manufacturer X500 frame',(.05,.15)),('plate','Harness plate',(.69,.59)),('rotor','Lifted release rotor',(.69,.49)),('dart1_body','Four complete carried darts',(.03,.81))])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--no-render',action='store_true');ap.add_argument('--no-install',action='store_true');ap.add_argument('--render-only',action='store_true');args=ap.parse_args()
    for p in (WEB,TMP,MESH_CACHE):p.mkdir(parents=True,exist_ok=True)
    start=time.time();before=protected_snapshot();print('Loading original B-reps',flush=True)
    p=load_cache();dart,harness,drone,mass=make_parts(p)
    scenes={name:instances(name,dart,harness,drone,p) for name in ('dart','harness','aircraft')}
    from stake_web import make_stake_scene
    stake, scenes['stake']=make_stake_scene(p,dart,mass)
    if args.render_only:
        meshes={part.family+':'+part.name:mesh_part(part) for part in dart+harness+drone+stake}
        render_all(scenes,meshes);assert before==protected_snapshot();return
    checks={name:verify_exploded(name,inst) for name,inst in scenes.items()}
    (WEB/'exploded_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    assert all(c['pass_'] for c in checks.values()),'Exploded endpoint overlap; inspect web/exploded_checks.json'
    meshes={part.family+':'+part.name:mesh_part(part) for part in dart+harness+drone+stake}
    models={};readback={}
    for name,inst in scenes.items():
        # Sensible shared harness datum; dart origin at the middle of its length.
        origin=np.array([322.,0.,5.2]) if name=='dart' else np.zeros(3)
        models[name]=export_glb(name,inst,meshes,origin)
        readback[name]=validate_readback(name,models[name],inst,meshes)
        print('WEB',name,models[name]['size_bytes'],'bytes',models[name]['triangle_count'],'instanced triangles',flush=True)
    (WEB/'validation-readback.json').write_text(json.dumps(readback,indent=2)+'\n')
    validator=khronos_validate(args.no_install)
    if not args.no_render:render_all(scenes,meshes)
    after=protected_snapshot();assert before==after,'Protected CAD input/output changed'
    (WEB/'provenance.json').write_text(json.dumps(dict(unchanged=True,files=before),indent=2)+'\n')
    manifest=dict(schema_version=1,units='metres',up_axis='Y',animation=dict(name='explode',duration_seconds=DURATION,interpolation='LINEAR',use='Clamp and scrub the clip; do not loop if the final exploded view should remain visible.'),
                  models=models,mass_groups=dict(antenna=dict(mass_g=.8,basis='MEASURE kit LoRa FPC and coax.'),SG90_with_stock_horn=dict(mass_g=9.0,basis='S3 catalog mass; individual servo/horn masses unmeasured.')),
                  modelled_mass_totals_g=dict(dart=mass['dart_total_g'],harness_without_darts=mass['harness_total_g'],four_dart_payload=mass['carried_payload_g'],stake=mass['stake']['total_g'],aircraft=None),
                  mass_report='../out/mass_properties.json',source_register='../DESIGN.md',source_download_register='../sources/manifest.json',
                  limitations=['XIAO revision: geometry and mass reports regenerated before this web export.',
                               'All masses are model estimates or catalog figures; no physical parts were weighed.',
                               'Per-part mass is null where only a purchased-assembly mass is available; never infer a mass from tessellated volume.',
                               'Dart nodes retain the original physical parts; populated board components and cell terminal details are grouped as purchased assemblies.',
                               'Aircraft source solids retain vendor indices; precise stock fastener identities and masses have not been established.',
                               'Propeller swept slabs are translucent clearance proxies, not actual propeller blade geometry or mass.',
                               'Rigid presentation translations show assembly axes and service order, not thread rotation, flexible deformation, a collision-free continuous path or a flight release.',
                               'Closed ties must be cut, soldered/welded connections disconnected as appropriate, and heat-set inserts heated; their displaced depictions are identification layouts.',
                               'Integral snap fingers, ribs and channels belong to their printed part; five short INMP441 wires are included. RTV, solder and final wire dress remain assembly allowances.',
                               'Factory-welded nickel tabs stay attached in actual service; lateral tab offsets only distinguish the depicted items.',
                               'No physical print, drop, acoustic, waterproofing, radio or flight qualification is implied.'],
                  web_tessellation=dict(printed_linear_tolerance_mm=.10,printed_angular_tolerance_rad=.18,other_linear_tolerance_mm=.20,other_angular_tolerance_rad=.40,oem_aircraft_linear_tolerance_mm=.40,oem_aircraft_angular_tolerance_rad=.65,
                                        electronics_max_triangles_per_colour=14000,aircraft_max_triangles_per_source_solid=3000,method='Original B-rep tessellation; VTK quadric decimation only when OEM cap exceeded; shared dart meshes; no textures or compression extensions.'),
                  validation=dict(readback='validation-readback.json',khronos='validation-khronos.json',exploded='exploded_checks.json',protected_files='provenance.json'),
                  renders=['../renders/'+n for n in ('dart_exploded.png','dart_exploded_pod.png','harness_exploded.png','harness_exploded_detail.png','aircraft_exploded.png')])
    (WEB/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('DONE',round(time.time()-start,1),'seconds; full-resolution inputs and outputs unchanged.',flush=True)


if __name__=='__main__':main()
