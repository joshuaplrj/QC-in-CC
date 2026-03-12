import math
import tkinter as tk

class Renderer3D:
    def __init__(self, canvas: tk.Canvas, width: float, height: float, palette: dict):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.cx = width / 2
        self.cy = height / 2
        self.palette = palette
        self.fov = min(width, height) * 0.8
        self.faces = [] # Store (z_avg, face_pts, color_hex, outline_color)

    def _project(self, x, y, z):
        # Prevent division by zero or flipping if object goes behind camera
        # Assumes camera is at z = -self.fov roughly
        z_eff = z + self.fov
        if z_eff < 0.1: z_eff = 0.1
        
        f = self.fov / z_eff
        px = self.cx + x * f
        py = self.cy + y * f
        return px, py

    def _rotate_3d(self, x, y, z, ax, ay, az):
        # X axis
        y1 = y * math.cos(ax) - z * math.sin(ax)
        z1 = z * math.cos(ax) + y * math.sin(ax)
        # Y axis
        x2 = x * math.cos(ay) - z1 * math.sin(ay)
        z2 = z1 * math.cos(ay) + x * math.sin(ay)
        # Z axis
        x3 = x2 * math.cos(az) - y1 * math.sin(az)
        y3 = y1 * math.cos(az) + x2 * math.sin(az)
        return x3, y3, z2

    def add_poly(self, vertices, color, outline=""):
        # vertices = [(x,y,z), ...]
        
        # Calculate normal for backface culling and basic lighting
        if len(vertices) >= 3:
            v0, v1, v2 = vertices[0], vertices[1], vertices[len(vertices)-1]
            # Vectors v0->v1 and v0->v2
            dx1, dy1, dz1 = v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2]
            dx2, dy2, dz2 = v2[0]-v0[0], v2[1]-v0[1], v2[2]-v0[2]
            
            # Cross product
            nx = dy1*dz2 - dz1*dy2
            ny = dz1*dx2 - dx1*dz2
            nz = dx1*dy2 - dy1*dx2
            
            # Backface culling (if dot product of normal and camera vector is positive, it's facing away)
            # Camera vector is roughly (0,0,-1) towards the screen from the object
            if nz > 0.01:
                return # cull

            # Normalize normal
            length = math.hypot(nx, math.hypot(ny, nz))
            if length > 0.001:
                nx, ny, nz = nx/length, ny/length, nz/length
            else:
                nx, ny, nz = 0, 0, -1

            # Simple directional lighting from top-left (dx=0.5, dy=-0.5, dz=-0.7)
            ldx, ldy, ldz = 0.5, -0.5, -0.7
            ll = math.hypot(ldx, math.hypot(ldy, ldz))
            ldx, ldy, ldz = ldx/ll, ldy/ll, ldz/ll
            
            dot = -(nx*ldx + ny*ldy + nz*ldz)
            dot = max(0.0, min(1.0, dot))
            
            # Simple shading logic
            try:
                # parse hex colors
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                
                # Ambient + diffuse
                ambient = 0.3
                diffuse = 0.7 * dot
                intensity = ambient + diffuse
                
                r = min(255, int(r * intensity))
                g = min(255, int(g * intensity))
                b = min(255, int(b * intensity))
                shaded_color = f"#{r:02x}{g:02x}{b:02x}"
            except:
                shaded_color = color
        else:
            shaded_color = color
            
        # Z-sorting avg
        z_avg = sum(v[2] for v in vertices) / len(vertices)
        
        # Project poly to 2D
        pts_2d = []
        for v in vertices:
            px, py = self._project(*v)
            pts_2d.extend([px, py])
            
        self.faces.append((z_avg, pts_2d, shaded_color, outline))

    def add_line(self, v1, v2, color, width=1):
        z_avg = (v1[2] + v2[2]) / 2.0
        p1 = self._project(*v1)
        p2 = self._project(*v2)
        # Store as a "line" type by injecting width instead of color in index 3
        # Use a special tag in index 2 to denote it's a line
        self.faces.append((z_avg, [p1[0], p1[1], p2[0], p2[1]], "LINE:"+color, width))

    def render(self):
        # Sort back to front (highest z is furthest away)
        self.faces.sort(key=lambda item: item[0], reverse=True)
        for _, pts, fill, outline in self.faces:
            if fill.startswith("LINE:"):
                col = fill.split("LINE:")[1]
                w = outline
                self.canvas.create_line(*pts, fill=col, width=w)
            else:
                self.canvas.create_polygon(*pts, fill=fill, outline=outline, width=1)

    # --- Primitives ---
    
    def draw_cube(self, cx, cy, cz, size, rot_x, rot_y, rot_z, color):
        s = size / 2.0
        # 8 vertices
        vertices = [
            (-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s), # Front
            (-s, -s, s),  (s, -s, s),  (s, s, s),  (-s, s, s)   # Back
        ]
        
        # Rotate and translate
        trans_v = []
        for x, y, z in vertices:
            rx, ry, rz = self._rotate_3d(x, y, z, rot_x, rot_y, rot_z)
            trans_v.append((rx + cx, ry + cy, rz + cz))
            
        # 6 faces
        faces_idx = [
            (0, 1, 2, 3), # Front
            (1, 5, 6, 2), # Right
            (5, 4, 7, 6), # Back
            (4, 0, 3, 7), # Left
            (3, 2, 6, 7), # Top
            (4, 5, 1, 0)  # Bottom
        ]
        
        for f in faces_idx:
            poly = [trans_v[i] for i in f]
            self.add_poly(poly, color, outline=self.palette["grid"])

    def draw_plane(self, cx, cy, cz, w, h, rot_x, rot_y, rot_z, color, wireframe=False):
        hw, hh = w/2, h/2
        vertices = [
            (-hw, 0, -hh), (hw, 0, -hh), (hw, 0, hh), (-hw, 0, hh)
        ]
        trans_v = []
        for x, y, z in vertices:
            rx, ry, rz = self._rotate_3d(x, y, z, rot_x, rot_y, rot_z)
            trans_v.append((rx + cx, ry + cy, rz + cz))
            
        if wireframe:
            self.add_line(trans_v[0], trans_v[1], color, 1)
            self.add_line(trans_v[1], trans_v[2], color, 1)
            self.add_line(trans_v[2], trans_v[3], color, 1)
            self.add_line(trans_v[3], trans_v[0], color, 1)
        else:
            self.add_poly(trans_v, color, outline=self.palette["grid"])

    def draw_sphere(self, cx, cy, cz, r, rot_x, rot_y, rot_z, color, segments=12):
        # Lat/Lon UV mapping
        for i in range(segments):
            lat0 = math.pi * (-0.5 + (i - 1) / segments)
            z0 = math.sin(lat0)
            zr0 = math.cos(lat0)
            
            lat1 = math.pi * (-0.5 + i / segments)
            z1 = math.sin(lat1)
            zr1 = math.cos(lat1)
            
            for j in range(segments):
                lng = 2 * math.pi * (j - 1) / segments
                x0 = math.cos(lng) * zr0
                y0 = math.sin(lng) * zr0
                x1 = math.cos(lng) * zr1
                y1 = math.sin(lng) * zr1
                
                lng_next = 2 * math.pi * j / segments
                x2 = math.cos(lng_next) * zr1
                y2 = math.sin(lng_next) * zr1
                x3 = math.cos(lng_next) * zr0
                y3 = math.sin(lng_next) * zr0
                
                # vertices
                v0 = (x0*r, y0*r, z0*r)
                v1 = (x1*r, y1*r, z1*r)
                v2 = (x2*r, y2*r, z2*r)
                v3 = (x3*r, y3*r, z3*r)
                
                poly = [v0, v1, v2, v3]
                trans_poly = []
                for px, py, pz in poly:
                    rx, ry, rz = self._rotate_3d(px, py, pz, rot_x, rot_y, rot_z)
                    trans_poly.append((rx+cx, ry+cy, rz+cz))
                    
                self.add_poly(trans_poly, color)
