"""Millimetre heightfield solids for enlarged teaching models, not process geometry.

Each XY cell is solid from z=0 to its saved top. Extract only external voxel
faces; never concatenate intersecting component meshes. NumPy + stdlib only.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import struct

import numpy as np


# Five columns, seven rows; top row first. English uppercase and schematic signs.
FONT = {
    'A': ['01110','10001','10001','11111','10001','10001','10001'],
    'B': ['11110','10001','10001','11110','10001','10001','11110'],
    'C': ['01111','10000','10000','10000','10000','10000','01111'],
    'D': ['11110','10001','10001','10001','10001','10001','11110'],
    'E': ['11111','10000','10000','11110','10000','10000','11111'],
    'F': ['11111','10000','10000','11110','10000','10000','10000'],
    'G': ['01111','10000','10000','10111','10001','10001','01111'],
    'H': ['10001','10001','10001','11111','10001','10001','10001'],
    'I': ['11111','00100','00100','00100','00100','00100','11111'],
    'J': ['00111','00010','00010','00010','10010','10010','01100'],
    'K': ['10001','10010','10100','11000','10100','10010','10001'],
    'L': ['10000','10000','10000','10000','10000','10000','11111'],
    'M': ['10001','11011','10101','10101','10001','10001','10001'],
    'N': ['10001','11001','10101','10011','10001','10001','10001'],
    'O': ['01110','10001','10001','10001','10001','10001','01110'],
    'P': ['11110','10001','10001','11110','10000','10000','10000'],
    'Q': ['01110','10001','10001','10001','10101','10010','01101'],
    'R': ['11110','10001','10001','11110','10100','10010','10001'],
    'S': ['01111','10000','10000','01110','00001','00001','11110'],
    'T': ['11111','00100','00100','00100','00100','00100','00100'],
    'U': ['10001','10001','10001','10001','10001','10001','01110'],
    'V': ['10001','10001','10001','10001','10001','01010','00100'],
    'W': ['10001','10001','10001','10101','10101','10101','01010'],
    'X': ['10001','10001','01010','00100','01010','10001','10001'],
    'Y': ['10001','10001','01010','00100','00100','00100','00100'],
    'Z': ['11111','00001','00010','00100','01000','10000','11111'],
    '0': ['01110','10001','10011','10101','11001','10001','01110'],
    '1': ['00100','01100','00100','00100','00100','00100','01110'],
    '2': ['01110','10001','00001','00010','00100','01000','11111'],
    '3': ['11110','00001','00001','01110','00001','00001','11110'],
    '4': ['00010','00110','01010','10010','11111','00010','00010'],
    '5': ['11111','10000','10000','11110','00001','00001','11110'],
    '6': ['01110','10000','10000','11110','10001','10001','01110'],
    '7': ['11111','00001','00010','00100','01000','01000','01000'],
    '8': ['01110','10001','10001','01110','10001','10001','01110'],
    '9': ['01110','10001','10001','01111','00001','00001','01110'],
    '+': ['00000','00100','00100','11111','00100','00100','00000'],
    '-': ['00000','00000','00000','11111','00000','00000','00000'],
    '.': ['00000','00000','00000','00000','00000','00110','00110'],
    '/': ['00001','00001','00010','00100','01000','10000','10000'],
    ':': ['00000','00110','00110','00000','00110','00110','00000'],
    ' ': ['00000'] * 7,
}


class HeightModel:
    """Coordinates and absolute top_mm are millimetres; cell array is (y, x).

    Main geometric feature widths must be >=1.2 mm. Text pixels are a declared
    >=0.8 mm exception. These are construction constraints, not a universal
    minimum-wall-thickness measurement for arbitrary meshes.
    """
    def __init__(self, width_mm=60, depth_mm=42, pitch_mm=0.4, base_mm=2.4,
                 max_height_mm=25, min_feature_mm=1.2):
        values = np.asarray([width_mm, depth_mm, pitch_mm, base_mm, max_height_mm, min_feature_mm], float)
        if not np.all(np.isfinite(values)) or np.any(values <= 0):
            raise ValueError('Dimensions must be finite and positive')
        if base_mm < 2.4 - 1e-9 or min_feature_mm < 1.2 - 1e-9:
            raise ValueError('Base must be >=2.4 mm and main feature width >=1.2 mm')
        self.width_mm, self.depth_mm, self.pitch_mm = map(float, (width_mm, depth_mm, pitch_mm))
        self.base_mm, self.max_height_mm, self.min_feature_mm = map(float, (base_mm, max_height_mm, min_feature_mm))
        nx, ny = round(width_mm / pitch_mm), round(depth_mm / pitch_mm)
        if abs(nx * pitch_mm - width_mm) > 1e-8 or abs(ny * pitch_mm - depth_mm) > 1e-8:
            raise ValueError('Width and depth must be exact pitch multiples')
        self.base_steps = int(np.ceil(base_mm / pitch_mm - 1e-9))
        self.max_steps = int(np.floor(max_height_mm / pitch_mm + 1e-9))
        if self.max_steps < self.base_steps:
            raise ValueError('Maximum height is below the base')
        self._h = np.full((ny, nx), self.base_steps, dtype=np.int32)
        self.features = []
        self.repair_report = None
        self._x, self._y = np.meshgrid((np.arange(nx) + 0.5) * pitch_mm,
                                       (np.arange(ny) + 0.5) * pitch_mm)

    @property
    def heightfield(self):
        return self._h.astype(np.float64) * self.pitch_mm

    @property
    def heights_mm(self):
        return self.heightfield

    @property
    def heights(self):
        return self.heightfield

    def _height(self, value):
        value = float(value)
        if not np.isfinite(value) or value < self.base_mm - 1e-9 or value > self.max_height_mm + 1e-9:
            raise ValueError(f'Top height must lie between {self.base_mm} and {self.max_height_mm} mm')
        return min(self.max_steps, max(self.base_steps, int(np.floor(value / self.pitch_mm + 0.5))))

    def _bounds(self, x0, y0, x1, y1, minimum=None):
        values = np.asarray([x0, y0, x1, y1], float)
        if not np.all(np.isfinite(values)) or x1 <= x0 or y1 <= y0:
            raise ValueError('Invalid XY bounds')
        if x0 < -1e-9 or y0 < -1e-9 or x1 > self.width_mm + 1e-9 or y1 > self.depth_mm + 1e-9:
            raise ValueError(f'Feature outside {self.width_mm} x {self.depth_mm} mm plate: {values.tolist()}')
        if minimum is not None and min(x1 - x0, y1 - y0) < minimum - 1e-9:
            raise ValueError(f'Feature narrower than {minimum} mm')
        return (self._x >= x0 - 1e-9) & (self._x < x1 - 1e-9) & (self._y >= y0 - 1e-9) & (self._y < y1 - 1e-9)

    def rect(self, x0, y0, x1, y1, top_mm):
        mask = self._bounds(x0, y0, x1, y1, self.min_feature_mm)
        self._h[mask] = np.maximum(self._h[mask], self._height(top_mm))
        self.features.append({'kind': 'rect', 'nominal_width_mm': min(x1-x0, y1-y0), 'top_mm': top_mm})
        return self

    def groove(self, x0, y0, x1, y1, top_mm):
        mask = self._bounds(x0, y0, x1, y1, self.min_feature_mm)
        self._h[mask] = np.minimum(self._h[mask], self._height(top_mm))
        self.features.append({'kind': 'groove', 'nominal_width_mm': min(x1-x0, y1-y0), 'top_mm': top_mm})
        return self

    def ellipse(self, cx, cy, rx, ry, top_mm):
        self._bounds(cx-rx, cy-ry, cx+rx, cy+ry, self.min_feature_mm)
        mask = ((self._x-cx)/rx)**2 + ((self._y-cy)/ry)**2 <= 1 + 1e-12
        self._h[mask] = np.maximum(self._h[mask], self._height(top_mm))
        self.features.append({'kind': 'ellipse', 'nominal_width_mm': 2*min(rx, ry), 'top_mm': top_mm})
        return self

    def line(self, points, width_mm, top_mm):
        points = np.asarray(points, dtype=float)
        if points.ndim != 2 or points.shape[1] != 2 or len(points) < 2 or not np.all(np.isfinite(points)):
            raise ValueError('line needs at least two finite XY points')
        if not np.isfinite(width_mm) or width_mm < self.min_feature_mm - 1e-9:
            raise ValueError('Line width is below the main-feature limit')
        radius = width_mm/2
        self._bounds(points[:,0].min()-radius, points[:,1].min()-radius,
                     points[:,0].max()+radius, points[:,1].max()+radius)
        mask = np.zeros_like(self._h, dtype=bool)
        for a, b in zip(points[:-1], points[1:]):
            d = b-a
            length2 = float(d @ d)
            t = np.zeros_like(self._x) if length2 == 0 else np.clip(((self._x-a[0])*d[0] + (self._y-a[1])*d[1])/length2, 0, 1)
            mask |= (self._x-a[0]-t*d[0])**2 + (self._y-a[1]-t*d[1])**2 <= radius**2 + 1e-12
        self._h[mask] = np.maximum(self._h[mask], self._height(top_mm))
        self.features.append({'kind': 'line', 'nominal_width_mm': float(width_mm), 'top_mm': top_mm})
        return self

    path = line

    def text(self, text, x, y, pixel_mm=0.8, raise_mm=0.8):
        text = str(text).upper()
        if not text or any(c not in FONT for c in text):
            raise ValueError('Text supports A-Z, 0-9, space, + - . / :')
        if not np.isfinite(pixel_mm) or pixel_mm < 0.8 - 1e-9 or not np.isfinite(raise_mm) or raise_mm < 0.4 - 1e-9:
            raise ValueError('Text pixel must be >=0.8 mm and raised height >=0.4 mm')
        cells = int(np.ceil(pixel_mm/self.pitch_mm-1e-9))
        pixel = cells*self.pitch_mm
        start_x = int(np.floor(x/self.pitch_mm+0.5))
        start_y = int(np.floor(y/self.pitch_mm+0.5))
        self._bounds(start_x*self.pitch_mm, start_y*self.pitch_mm,
                     (start_x+(6*len(text)-1)*cells)*self.pitch_mm, (start_y+7*cells)*self.pitch_mm)
        lift = max(1, int(np.ceil(raise_mm/self.pitch_mm-1e-9)))
        for index, char in enumerate(text):
            if char == ' ':
                continue
            x0, y0 = start_x+index*6*cells, start_y
            existing = int(self._h[y0:y0+7*cells, x0:x0+5*cells].max())
            target = existing+lift
            if target > self.max_steps:
                raise ValueError('Text would exceed maximum height')
            for row, bits in enumerate(FONT[char]):
                for col, bit in enumerate(bits):
                    if bit == '1':
                        yy = y0+(6-row)*cells
                        xx = x0+col*cells
                        self._h[yy:yy+cells, xx:xx+cells] = target
        self.features.append({'kind': 'text', 'text': text, 'nominal_width_mm': pixel,
                              'raise_mm': lift*self.pitch_mm})
        return self

    def repair_corners(self):
        """Remove diagonal-only high-column contacts by monotone local filling."""
        before = self._h.copy()
        ny, nx = self._h.shape
        iterations = 0
        examples = []
        while True:
            a, b = self._h[:-1,:-1], self._h[:-1,1:]
            c, d = self._h[1:,:-1], self._h[1:,1:]
            ad = np.minimum(a,d) > np.maximum(b,c)
            bc = np.minimum(b,c) > np.maximum(a,d)
            if not ad.any() and not bc.any():
                break
            targets, heights = [], []
            for mask, first in ((ad, True), (bc, False)):
                y, x = np.nonzero(mask)
                if first:
                    choose = b[y,x] >= c[y,x]
                    yy, xx = np.where(choose,y,y+1), np.where(choose,x+1,x)
                    hh = np.minimum(a[y,x],d[y,x])
                else:
                    choose = a[y,x] >= d[y,x]
                    yy, xx = np.where(choose,y,y+1), np.where(choose,x,x+1)
                    hh = np.minimum(b[y,x],c[y,x])
                targets.append(yy*nx+xx)
                heights.append(hh.copy())
            indices, values = np.concatenate(targets), np.concatenate(heights)
            for index, target in zip(indices[:max(0, 12-len(examples))], values):
                yy, xx = divmod(int(index), nx)
                examples.append({'cell_yx': [yy,xx], 'old_mm': float(self._h[yy,xx]*self.pitch_mm),
                                 'new_mm': float(target*self.pitch_mm)})
            np.maximum.at(self._h.ravel(), indices, values)
            iterations += 1
            if iterations > nx*ny*self.max_steps:
                raise RuntimeError('Monotone corner repair failed to converge')
        delta = self._h-before
        report = {'iterations': iterations, 'changed_cells': int(np.count_nonzero(delta)),
                  'added_volume_mm3': float(delta.sum()*self.pitch_mm**3),
                  'maximum_raise_mm': float(delta.max()*self.pitch_mm), 'examples': examples,
                  'method': 'Fill the higher low corner to the lower opposing high height; no cells lowered.'}
        self.repair_report = report
        return report

    def mesh(self):
        self.repair_corners()
        h = self._h
        occupied = np.arange(int(h.max()))[:,None,None] < h[None,:,:]
        templates = [
            (2, 1, [[1,0,0],[1,1,0],[1,1,1],[1,0,1]]),
            (2,-1, [[0,0,0],[0,0,1],[0,1,1],[0,1,0]]),
            (1, 1, [[0,1,0],[0,1,1],[1,1,1],[1,1,0]]),
            (1,-1, [[0,0,0],[1,0,0],[1,0,1],[0,0,1]]),
            (0, 1, [[0,0,1],[1,0,1],[1,1,1],[0,1,1]]),
            (0,-1, [[0,0,0],[0,1,0],[1,1,0],[1,0,0]]),
        ]
        quads = []
        for axis, sign, offsets in templates:
            neighbor = np.zeros_like(occupied)
            destination, source = [slice(None)]*3, [slice(None)]*3
            destination[axis] = slice(None,-1) if sign > 0 else slice(1,None)
            source[axis] = slice(1,None) if sign > 0 else slice(None,-1)
            neighbor[tuple(destination)] = occupied[tuple(source)]
            z,y,x = np.nonzero(occupied & ~neighbor)
            origins = np.column_stack((x,y,z)).astype(np.int32)
            quads.append(origins[:,None,:]+np.asarray(offsets,np.int32)[None,:,:])
        corners = np.concatenate(quads)
        vertices, inverse = np.unique(corners.reshape(-1,3), axis=0, return_inverse=True)
        q = inverse.reshape(-1,4)
        faces = np.concatenate((q[:,[0,1,2]], q[:,[0,2,3]]))
        return vertices.astype(np.float64)*self.pitch_mm, faces.astype(np.int32)

    @staticmethod
    def binary_stl(vertices, faces):
        triangles = np.asarray(vertices, float)[faces]
        normals = np.cross(triangles[:,1]-triangles[:,0], triangles[:,2]-triangles[:,0])
        normals /= np.linalg.norm(normals, axis=1)[:,None]
        dtype = np.dtype([('normal','<f4',(3,)),('vertices','<f4',(3,3)),('attribute','<u2')])
        data = np.zeros(len(faces),dtype=dtype)
        data['normal'],data['vertices'] = normals,triangles
        header = b'EDUCATIONAL HEIGHTFIELD; coordinates in mm; enlarged nonphysical device geometry'
        return header[:80].ljust(80,b' ')+struct.pack('<I',len(faces))+data.tobytes()

    def export(self, stl_path, heightfield_path):
        stl_path, heightfield_path = Path(stl_path), Path(heightfield_path)
        if heightfield_path.suffix.lower() != '.npy':
            raise ValueError('heightfield_path must end in .npy')
        vertices, faces = self.mesh()
        payload = self.binary_stl(vertices,faces)
        validator_path = Path(__file__).parent/'validation'/'validate_meshes.py'
        spec = importlib.util.spec_from_file_location('_teaching_mesh_validator',validator_path)
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        rv,rf,rn = validator.read_binary_stl(payload)
        report = validator.validate_mesh(rv,rf,self.heightfield,self.pitch_mm,self.base_mm,
                                         [self.width_mm,self.depth_mm],self.max_height_mm,rn)
        if report['status'] != 'PASS':
            raise ValueError('STL validation failed: '+str(report['errors']))
        stl_path.parent.mkdir(parents=True,exist_ok=True)
        heightfield_path.parent.mkdir(parents=True,exist_ok=True)
        stl_path.write_bytes(payload)
        np.save(heightfield_path,self.heightfield,allow_pickle=False)
        report.update(stl_path=str(stl_path),heightfield_path=str(heightfield_path),
                      stl_sha256=hashlib.sha256(payload).hexdigest(),
                      heightfield_sha256=hashlib.sha256(heightfield_path.read_bytes()).hexdigest(),
                      corner_repair=self.repair_report,features=self.features,
                      minimum_declared_main_feature_mm=min((f['nominal_width_mm'] for f in self.features if f['kind']!='text'),default=None),
                      minimum_declared_text_stroke_mm=min((f['nominal_width_mm'] for f in self.features if f['kind']=='text'),default=None),
                      feature_width_scope='Declared construction widths; not a universal medial-axis wall-thickness test.',
                      physical_print_tested=False)
        return report
