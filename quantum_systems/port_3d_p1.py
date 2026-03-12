import sys
import re
import os

path = r'c:\Users\John Jacob\Desktop\Desktop\QC in CC\QB in CC\quantum_systems\custom_animations.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace cryptography
crypto_new = """@register_animation("cryptography")
def draw_cryptography(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    engine = Renderer3D(canvas, width, height, palette)
    
    # 3D Grid floor
    for i in range(-5, 6):
        engine.add_line((i*40, 100, -200), (i*40, 100, 200), palette["grid"])
        engine.add_line((-200, 100, i*40), (200, 100, i*40), palette["grid"])
        
    # Floating 3D Cubes (Data Blocks)
    for i in range(5):
        cx = -150 + i*75
        cy = -50 + math.sin(phase*2 + i)*30
        cz = math.cos(phase + i)*50
        rot = phase + i
        color = palette["accent"] if i == 2 else palette["secondary"]
        engine.draw_cube(cx, cy, cz, 40, rot, rot*0.5, 0, color)
        
    # Central Lock Mechanism (Cylinder approx with planes)
    open_offset = max(0.0, math.sin(phase)*50)
    for i in range(8):
        ang = i * math.pi/4
        # draw arc for the lock loop
        px = math.cos(ang)*30
        py = -50 - open_offset - math.sin(ang)*30
        if py < -50:
             cx, cy, cz = px, py, 0
             engine.draw_cube(cx, cy, cz, 10, 0, phase, 0, palette["primary"])
             
    engine.draw_cube(0, 0, 0, 80, 0, phase*0.2, 0, "#0a1520") # lock body
    
    engine.render()"""

# We look for @register_animation("cryptography") up to the next @register
content = re.sub(r'@register_animation\("cryptography"\).*?(?=@register_animation)', crypto_new + '\n\n', content, flags=re.DOTALL)

# Replace molecular_dynamics
md_new = """@register_animation("molecular_dynamics")
def draw_molecular_dynamics(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    engine = Renderer3D(canvas, width, height, palette)
    
    temp = 0.5 + 0.5*math.sin(phase*0.5)
    
    # 3D Lattice
    spacing = 80
    atoms = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                dx = math.sin(phase*5 + x*7 + y*11 + z*3) * 20 * temp
                dy = math.cos(phase*4 + x*13 + y*5 + z*7) * 20 * temp
                dz = math.sin(phase*3 + x*2 + y*17 + z*5) * 20 * temp
                
                ax, ay, az = x*spacing + dx, y*spacing + dy, z*spacing + dz
                atoms.append((ax, ay, az))
                
    # Rotate entire lattice
    rot_x, rot_y = phase*0.3, phase*0.7
    proj_atoms = []
    for ax, ay, az in atoms:
        rx, ry, rz = engine._rotate_3d(ax, ay, az, rot_x, rot_y, 0)
        proj_atoms.append((rx, ry, rz))
        
    # Draw bonds (lines instead of polys for speed)
    for i in range(len(proj_atoms)):
        for j in range(i+1, len(proj_atoms)):
            d = math.hypot(proj_atoms[i][0]-proj_atoms[j][0], math.hypot(proj_atoms[i][1]-proj_atoms[j][1], proj_atoms[i][2]-proj_atoms[j][2]))
            if d < spacing * 1.5:
                strain = abs(d - spacing) / spacing
                col = palette["danger"] if strain > 0.2 else palette["primary"]
                engine.add_line(proj_atoms[i], proj_atoms[j], col, 2)
                
    for ax, ay, az in proj_atoms:
        col = palette["accent"] if temp > 0.8 else palette["primary"]
        engine.draw_cube(ax, ay, az, 15, rot_x, rot_y, phase, col)
        
    engine.render()"""

content = re.sub(r'@register_animation\("molecular_dynamics"\).*?(?=@register_animation)', md_new + '\n\n', content, flags=re.DOTALL)

# Replace reactor_design
reac_new = """@register_animation("reactor_design")
def draw_reactor_design(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    engine = Renderer3D(canvas, width, height, palette)
    
    # 3D CSTR Tank Wireframe
    h, r = 150, 80
    for i in range(12):
        ang = i * math.pi/6
        ax = math.cos(ang)*r
        az = math.sin(ang)*r
        # rotate tank slightly
        rx, ry, rz = engine._rotate_3d(ax, -h/2, az, 0.2, phase*0.2, 0)
        rx2, ry2, rz2 = engine._rotate_3d(ax, h/2, az, 0.2, phase*0.2, 0)
        engine.add_line((rx, ry, rz), (rx2, ry2, rz2), palette["grid"])
        
    # Impeller (rotating planes)
    engine.draw_plane(0, 0, 0, 100, 20, 0.2, phase*5, 0, palette["secondary"])
    engine.draw_plane(0, 0, 0, 20, 100, 0.2 + math.pi/2, phase*5, 0, palette["secondary"])
    
    # 3D Particles A+B -> C
    import random
    random.seed(42) # structure it deterministically per tick implicitly based on loop
    for i in range(40):
        px = (i*37 % (r*1.6)) - r*0.8
        py = (i*13 % (h*0.8)) - h*0.4
        pz = (i*29 % (r*1.6)) - r*0.8
        
        # Swirl
        ang = math.atan2(pz, px) + phase*2 + (py/h)*phase*5
        dist = math.hypot(px, pz)
        px2 = math.cos(ang)*dist
        pz2 = math.sin(ang)*dist
        
        rx, ry, rz = engine._rotate_3d(px2, py, pz2, 0.2, phase*0.2, 0)
        
        progress = (math.sin(phase + i) + 1)/2
        if progress < 0.3: col = palette["primary"]
        elif progress < 0.6: col = palette["danger"]
        else: col = palette["accent"]
        
        engine.draw_cube(rx, ry, rz, 8 if progress > 0.6 else 5, phase, phase, 0, col)
        
    engine.render()"""
    
content = re.sub(r'@register_animation\("reactor_design"\).*?(?=@register_animation)', reac_new + '\n\n', content, flags=re.DOTALL)

# Replace cfd_solver
cfd_new = """@register_animation("cfd_solver")
def draw_cfd_solver(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    engine = Renderer3D(canvas, width, height, palette)
    
    # 3D Obstacle (Sphere)
    obs_r = 50
    engine.draw_sphere(-50, 0, 0, obs_r, phase*0.5, phase*0.7, 0, "#121e2b", segments=8)
    
    # Flow Field Particles passing through in 3D
    for i in range(60):
        # Initial positions far left
        px = -250 + (phase*200 + i*40) % 500
        py = -100 + (i*17) % 200
        pz = -100 + (i*29) % 200
        
        # Deflection from sphere
        dist = math.hypot(px - (-50), math.hypot(py, pz))
        if dist < obs_r * 2:
            mag = (obs_r*1.5) / max(dist, 1)
            py += (py/dist) * mag * 20
            pz += (pz/dist) * mag * 20
        
        # Wake turbulence
        if px > -50 and dist < obs_r * 3:
            py += math.sin(px*0.05 - phase*5)*10
            pz += math.cos(px*0.05 - phase*4)*10
            
        color = palette["danger"] if dist < obs_r * 1.5 else palette["accent"] if dist < obs_r * 2.5 else palette["primary"]
        rx, ry, rz = engine._rotate_3d(px, py, pz, 0.2, phase*0.1, 0)
        
        # Draw particle as a small moving cube
        engine.draw_cube(rx, ry, rz, 4, phase, phase, phase, color)
        
    engine.render()"""

content = re.sub(r'@register_animation\("cfd_solver"\).*?(?=@register_animation)', cfd_new + '\n\n', content, flags=re.DOTALL)

# Replace robot_kinematics
robot_new = """@register_animation("robot_kinematics")
def draw_robot_kinematics(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    engine = Renderer3D(canvas, width, height, palette)
    
    # Base
    engine.draw_cube(0, 150, 0, 60, 0, phase*0.5, 0, "#121e2b")
    
    # 3D Arm logic
    l1, l2, l3 = 80, 70, 50
    
    # Inverse targets mapping to 3D space
    tx = math.sin(phase)*100
    ty = -50 + math.sin(phase*2)*50
    tz = math.cos(phase)*80
    
    engine.draw_sphere(tx, ty, tz, 10, phase, phase, 0, palette["danger"], segments=6) # Target
    
    # Simplified angles
    base_rot = math.atan2(tz, tx)
    # Planar inverse
    plane_d = math.hypot(tx, tz)
    dist = min(math.hypot(plane_d, ty - 150), l1+l2+l3 - 1)
    
    ang_elev = math.atan2(ty - 150, plane_d)
    
    # Transform forward keeping joints inside engine rotation hierarchy
    j0x, j0y, j0z = 0, 150, 0
    # Joint 1
    j1x = math.cos(base_rot)*math.cos(ang_elev + 0.5)*l1
    j1y = 150 + math.sin(ang_elev + 0.5)*l1
    j1z = math.sin(base_rot)*math.cos(ang_elev + 0.5)*l1
    # Joint 2
    j2x = j1x + math.cos(base_rot)*math.cos(ang_elev - 0.5)*l2
    j2y = j1y + math.sin(ang_elev - 0.5)*l2
    j2z = j1z + math.sin(base_rot)*math.cos(ang_elev - 0.5)*l2
    
    # Links
    engine.add_line((j0x, j0y, j0z), (j1x, j1y, j1z), palette["primary"], 8)
    engine.add_line((j1x, j1y, j1z), (j2x, j2y, j2z), palette["primary"], 6)
    engine.add_line((j2x, j2y, j2z), (tx, ty, tz), palette["accent"], 4)
    
    # Joints as cubes
    for jx, jy, jz in [(j0x, j0y, j0z), (j1x, j1y, j1z), (j2x, j2y, j2z)]:
         engine.draw_cube(jx, jy, jz, 15, phase, phase, 0, palette["secondary"])
         
    engine.render()"""

content = re.sub(r'@register_animation\("robot_kinematics"\).*?(?=@register_animation)', robot_new + '\n\n', content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS writing 5 3D animations")
