"""Read binary STL and certify a closed boundary of a saved MM heightfield.

NumPy + stdlib. The source geometry is deliberately restricted to grid-aligned,
solid vertical columns. Certification checks every surface square against the
independent heightfield occupancy rule, plus completeness and manifold topology.
It is not a general self-intersection solver or a physical print qualification.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import struct
import sys

import numpy as np


def read_binary_stl(source):
    raw = source if isinstance(source, bytes) else Path(source).read_bytes()
    if len(raw) < 84:
        raise ValueError('Binary STL header is truncated')
    count = struct.unpack_from('<I',raw,80)[0]
    if count == 0 or len(raw) != 84+50*count:
        raise ValueError('Binary STL byte length does not match facet count')
    dtype = np.dtype([('normal','<f4',(3,)),('vertices','<f4',(3,3)),('attribute','<u2')])
    records = np.frombuffer(raw,dtype=dtype,count=count,offset=84)
    triangles = records['vertices'].astype(np.float64)
    vertices,inverse = np.unique(triangles.reshape(-1,3),axis=0,return_inverse=True)
    return vertices,inverse.reshape(-1,3).astype(np.int32),records['normal'].astype(np.float64)


def validate_mesh(vertices,faces,heightfield,pitch_mm=0.4,base_mm=2.4,
                  expected_xy_mm=(60,42),max_height_mm=25,stored_normals=None):
    vertices,faces,h = np.asarray(vertices,float),np.asarray(faces),np.asarray(heightfield,float)
    checks,errors,metrics = [],[],{}
    def check(name,condition,detail=''):
        checks.append({'check':name,'status':'PASS' if condition else 'FAIL'})
        if not condition:
            errors.append(name+(': '+detail if detail else ''))
        return bool(condition)
    def result():
        return {'status':'FAIL' if errors else 'PASS','checks':checks,'errors':errors,
                **metrics,'pitch_mm':float(pitch_mm),'base_mm':float(base_mm),
                'coordinate_units':'mm by generator/manifest convention; STL has no standard units field',
                'physical_print_tested':False,
                'scope':'Digital topology and restricted heightfield boundary certification. No printer/material/slicer qualification or arbitrary-mesh wall-thickness assertion.'}
    shape_ok = vertices.ndim==2 and vertices.shape[1]==3 and faces.ndim==2 and faces.shape[1]==3 and h.ndim==2 and min(h.shape)>0
    if not check('array_shapes',shape_ok):
        return result()
    if not check('finite_values',np.isfinite(vertices).all() and np.isfinite(h).all() and np.isfinite(pitch_mm) and pitch_mm>0):
        return result()
    if not check('valid_face_indices',np.issubdtype(faces.dtype,np.integer) and faces.size>0 and faces.min()>=0 and faces.max()<len(vertices)):
        return result()
    triangles = vertices[faces]
    cross = np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0])
    doubled_areas = np.linalg.norm(cross,axis=1)
    if not check('nonzero_triangle_areas',bool(np.all(doubled_areas>pitch_mm**2*1e-8))):
        return result()
    normals = cross/doubled_areas[:,None]
    if stored_normals is not None:
        sn = np.asarray(stored_normals,float)
        check('stored_normals_consistent',sn.shape==normals.shape and np.isfinite(sn).all() and np.allclose(sn,normals,atol=1e-5,rtol=1e-5))
    lower,upper = vertices.min(axis=0),vertices.max(axis=0)
    size = upper-lower
    tol = max(1e-5,float(pitch_mm)*1e-4)
    check('millimetre_dimensions',np.allclose(size[:2],expected_xy_mm,atol=tol,rtol=0) and upper[2]<=max_height_mm+tol and np.allclose(lower,0,atol=tol,rtol=0))
    check('heightfield_dimensions',np.allclose([h.shape[1]*pitch_mm,h.shape[0]*pitch_mm],expected_xy_mm,atol=tol,rtol=0))
    check('base_at_least_2_4_mm',base_mm>=2.4-1e-9 and h.min()>=base_mm-tol)
    check('heightfield_bounds',h.min()>0 and h.max()<=max_height_mm+tol and abs(h.max()-upper[2])<=tol)
    check('flat_bottom_no_downward_overhang',np.all(np.abs(triangles[normals[:,2]<-0.5,:,2])<=tol))
    canonical_faces = np.sort(faces,axis=1)
    check('no_duplicate_triangles',len(np.unique(canonical_faces,axis=0))==len(faces))
    edges = np.concatenate((faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]))
    edge_keys,inverse,counts = np.unique(np.sort(edges,axis=1),axis=0,return_inverse=True,return_counts=True)
    manifold_edges = check('every_edge_has_two_faces',bool(np.all(counts==2)),f'{int(np.count_nonzero(counts!=2))} invalid edges')
    directions = np.where(edges[:,0]<edges[:,1],1,-1)
    check('consistent_directed_edge_winding',bool(np.all(np.bincount(inverse,weights=directions,minlength=len(counts))==0)))
    euler = len(vertices)-len(edge_keys)+len(faces)
    check('euler_characteristic_two',euler==2,str(euler))
    components = None
    bad_vertices = None
    if manifold_edges:
        owners = np.tile(np.arange(len(faces)),3)
        face_pairs = owners[np.argsort(inverse,kind='stable')].reshape(-1,2)
        parent = np.arange(len(faces))
        def find(x):
            while parent[x]!=x:
                parent[x]=parent[parent[x]]
                x=int(parent[x])
            return int(x)
        for a,b in face_pairs:
            a,b=find(int(a)),find(int(b))
            if a!=b:
                parent[b]=a
        components=len({find(i) for i in range(len(faces))})
        check('one_connected_surface',components==1,str(components))
        links=[[] for _ in vertices]
        for a,b,c in faces.tolist():
            links[a].append((b,c));links[b].append((c,a));links[c].append((a,b))
        bad_vertices=0
        for link in links:
            adjacency=defaultdict(list)
            for a,b in link:
                adjacency[a].append(b);adjacency[b].append(a)
            if not adjacency or any(len(n)!=2 for n in adjacency.values()):
                bad_vertices+=1
                continue
            visited=set();pending=[next(iter(adjacency))]
            while pending:
                node=pending.pop()
                if node not in visited:
                    visited.add(node);pending.extend(x for x in adjacency[node] if x not in visited)
            if len(visited)!=len(adjacency):
                bad_vertices+=1
        check('every_vertex_link_is_one_cycle',bad_vertices==0,str(bad_vertices))
    else:
        check('one_connected_surface',False,'Cannot certify with nonmanifold edges')
        check('every_vertex_link_is_one_cycle',False,'Cannot certify with nonmanifold edges')
    volume=float(np.einsum('ij,ij->i',triangles[:,0],np.cross(triangles[:,1],triangles[:,2])).sum()/6)
    expected_volume=float(h.sum()*pitch_mm**2)
    check('positive_signed_volume',volume>0)
    check('volume_matches_heightfield',abs(volume-expected_volume)<=max(0.01,expected_volume*2e-6))
    lattice=np.rint(vertices/pitch_mm).astype(np.int64)
    steps=np.rint(h/pitch_mm).astype(np.int64)
    on_grid=check('vertices_and_heights_on_saved_lattice',np.allclose(vertices,lattice*pitch_mm,atol=tol,rtol=0) and np.allclose(h,steps*pitch_mm,atol=tol,rtol=0))
    boundary_verified=False
    quads=None
    if on_grid:
        xyz=lattice[faces]
        mn,mx=xyz.min(axis=1),xyz.max(axis=1)
        spans=mx-mn
        axis=np.argmin(spans,axis=1)
        unit_triangles=np.all(np.sort(spans,axis=1)==np.array([0,1,1]),axis=1)
        if check('triangles_are_unit_grid_square_halves',bool(unit_triangles.all())):
            keys=np.column_stack((axis,mn))
            unique_keys,qinv,qcounts=np.unique(keys,axis=0,return_inverse=True,return_counts=True)
            quads=len(unique_keys)
            pairs_ok=check('two_triangles_per_boundary_square',bool(np.all(qcounts==2)))
            if pairs_ok:
                pairs=np.argsort(qinv,kind='stable').reshape(-1,2)
                diagonal_ok=True
                for first,second in pairs:
                    a=set(faces[first]);b=set(faces[second]);common=list(a&b)
                    if len(a|b)!=4 or len(common)!=2 or np.abs(lattice[common[0]]-lattice[common[1]]).sum()!=2:
                        diagonal_ok=False;break
                check('square_halves_cover_without_overlap',diagonal_ok)
            else:
                diagonal_ok=False
            low=mn.copy();low[np.arange(len(mn)),axis]-=1
            high=mn
            def occupied(cells):
                x,y,z=cells.T
                valid=(x>=0)&(x<steps.shape[1])&(y>=0)&(y<steps.shape[0])&(z>=0)
                out=np.zeros(len(cells),bool)
                ix=np.nonzero(valid)[0]
                out[ix]=z[ix]<steps[y[ix],x[ix]]
                return out
            low_full,high_full=occupied(low),occupied(high)
            expected_sign=np.where(low_full,1,-1)
            actual_sign=np.sign(normals[np.arange(len(normals)),axis])
            boundary_ok=check('each_facet_separates_solid_and_air',bool(np.all(low_full!=high_full) and np.all(actual_sign==expected_sign)))
            expected_quads=int(2*steps.size+np.abs(np.diff(steps,axis=0)).sum()+np.abs(np.diff(steps,axis=1)).sum()+steps[0,:].sum()+steps[-1,:].sum()+steps[:,0].sum()+steps[:,-1].sum())
            complete=check('all_heightfield_boundary_squares_present',quads==expected_quads,f'{quads} versus {expected_quads}')
            boundary_verified=bool(pairs_ok and diagonal_ok and boundary_ok and complete)
    check('restricted_geometry_no_self_intersections',boundary_verified and manifold_edges and bad_vertices==0,
          'Certified only by complete, nonoverlapping lattice boundary plus manifold tests')
    metrics.update(vertices=int(len(vertices)),triangles=int(len(faces)),edges=int(len(edge_keys)),
                   euler_characteristic=int(euler),connected_components=components,
                   nonmanifold_vertices=bad_vertices,boundary_squares=quads,
                   size_mm=[float(x) for x in size],bounding_box_mm=[lower.tolist(),upper.tolist()],
                   signed_volume_mm3=volume,expected_volume_mm3=expected_volume,
                   volume_absolute_error_mm3=abs(volume-expected_volume),
                   saved_heightfield_minimum_mm=float(h.min()),
                   no_self_intersection_scope='Complete grid boundary certification, not arbitrary triangle-pair testing',
                   no_overhang_scope='Every column solid from z=0; no downward-facing surface above build plate')
    return result()


def validate_file(stl_path,heightfield_path,pitch_mm=0.4,base_mm=2.4,expected_xy_mm=(60,42),max_height_mm=25):
    stl_path,heightfield_path=Path(stl_path),Path(heightfield_path)
    raw=stl_path.read_bytes()
    vertices,faces,normals=read_binary_stl(raw)
    field=np.load(heightfield_path,allow_pickle=False)
    report=validate_mesh(vertices,faces,field,pitch_mm,base_mm,expected_xy_mm,max_height_mm,normals)
    report.update(stl_sha256=hashlib.sha256(raw).hexdigest(),
                  heightfield_sha256=hashlib.sha256(heightfield_path.read_bytes()).hexdigest())
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stl')
    parser.add_argument('--heightfield')
    parser.add_argument('--manifest',default=str(Path(__file__).resolve().parent.parent/'generated_manifest.json'),
                        help='JSON list, {records:[...]} or {models:[...]}; paths relative to the manifest')
    parser.add_argument('--output',help='Save the complete validation JSON; stdout remains a compact summary')
    parser.add_argument('--pitch',type=float,default=0.4)
    parser.add_argument('--base',type=float,default=2.4)
    parser.add_argument('--size',type=float,nargs=2,default=(60,42))
    parser.add_argument('--max-height',type=float,default=25)
    args=parser.parse_args()
    try:
        if args.stl or args.heightfield:
            if not args.stl or not args.heightfield:
                raise ValueError('--stl and --heightfield must be supplied together')
            report=validate_file(args.stl,args.heightfield,args.pitch,args.base,args.size,args.max_height)
            output={'status':report['status'],'models':[report]}
        else:
            path=Path(args.manifest)
            payload=json.loads(path.read_text(encoding='utf-8'))
            items=payload if isinstance(payload,list) else payload.get('records',payload.get('models'))
            if not isinstance(items,list) or not items:
                raise ValueError('Manifest requires a nonempty records/models list')
            reports=[]
            for item in items:
                stl=item.get('stl',item.get('stl_path'))
                height=item.get('heightfield',item.get('heightfield_path'))
                generated=item.get('geometry_report',{})
                report=validate_file(path.parent/stl,path.parent/height,
                                     item.get('pitch_mm',generated.get('pitch_mm',args.pitch)),
                                     item.get('base_mm',generated.get('base_mm',args.base)),
                                     item.get('size_mm',generated.get('size_mm',args.size))[:2],
                                     item.get('max_height_mm',args.max_height))
                for key in ('stl_sha256','heightfield_sha256'):
                    expected=item.get(key,generated.get(key))
                    if expected is not None:
                        matched=report[key]==expected
                        report['checks'].append({'check':'manifest_'+key,'status':'PASS' if matched else 'FAIL'})
                        if not matched:
                            report['status']='FAIL';report['errors'].append('Manifest checksum mismatch: '+key)
                report['print_id']=item.get('print_id',item.get('id'))
                reports.append(report)
            output={'status':'PASS' if reports and all(r['status']=='PASS' for r in reports) else 'FAIL','models':reports}
    except Exception as exc:
        output={'status':'FAIL','errors':[f'{type(exc).__name__}: {exc}']}
    if args.output:
        try:
            destination=Path(args.output)
            destination.parent.mkdir(parents=True,exist_ok=True)
            destination.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        except OSError as exc:
            output['status']='FAIL';output.setdefault('errors',[]).append('Cannot save report: '+str(exc))
    reports=output.get('models',[])
    summary={'status':output['status'],'models_checked':len(reports),
             'models_passed':sum(r['status']=='PASS' for r in reports),
             'checks_run':sum(len(r.get('checks',[])) for r in reports),
             'failed_models':[{'print_id':r.get('print_id'),'errors':r.get('errors',[])[:12]}
                              for r in reports if r['status']!='PASS'],
             'errors':output.get('errors',[]),'physical_print_tested':False}
    if args.output:
        summary['full_report']=args.output
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0 if output['status']=='PASS' else 1


if __name__=='__main__':
    sys.exit(main())
