import sys
import re

path = r'c:\Users\John Jacob\Desktop\Desktop\QC in CC\QB in CC\quantum_systems\custom_animations.py'
with open(path, 'r', encoding='utf-8') as f:
    orig = f.read()

# 1. Remove Renderer3D block entirely
engine_pattern = r'class Renderer3D:.*?# --- Primitives ---.*?def draw_sphere\(.*?\):.*?self\.add_poly\(trans_poly, color\)'
orig = re.sub(engine_pattern, '', orig, flags=re.DOTALL)

# Clean up import math/tkinter duplicates if they were added right before it.
orig = re.sub(r'import math\nimport tkinter as tk\n\n\n@register_animation', '\n@register_animation', orig, flags=re.DOTALL)

# 2. Revert 5 specific animations
reverts = {
    "cryptography": '''@register_animation("cryptography")
def draw_cryptography(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    cx, cy = width / 2, height / 2
    phase = tick * 0.05 * flow_factor
    
    # 2D Data streams
    for i in range(8):
        y = cy - 100 + i * 25
        x = width * 0.1 + ((phase * 150 + i * 40) % (width * 0.8))
        val = hex(int(tick + i) % 16)[2:].upper()
        canvas.create_text(x, y, text=val, fill=palette["primary"], font=("Consolas", 12))
        canvas.create_line(x - 20, y, x + 20, y, fill=palette["secondary"], width=2, dash=(2, 4))
        
    # 2D Padlock
    lock_y = cy + 50
    open_offset = max(0.0, math.sin(phase) * 20)
    canvas.create_arc(cx - 30, lock_y - 70 - open_offset, cx + 30, lock_y - 10 - open_offset, start=0, extent=180, outline=palette["primary"], width=8, style=tk.ARC)
    canvas.create_rectangle(cx - 40, lock_y - 30, cx + 40, lock_y + 40, fill="#0d1b2a", outline=palette["accent"], width=3)
    canvas.create_oval(cx - 10, lock_y - 5, cx + 10, lock_y + 15, fill="#121e2b", outline=palette["danger"], width=2)
''',

    "molecular_dynamics": '''@register_animation("molecular_dynamics")
def draw_molecular_dynamics(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    cx, cy = width / 2, height / 2
    phase = tick * 0.05 * flow_factor
    temp = 0.5 + 0.5 * math.sin(phase * 0.5)
    
    spacing = 60
    atoms = []
    for r in range(-1, 2):
        for c in range(-1, 2):
            dx = math.sin(phase*4 + r*5 + c*7) * 15 * temp
            dy = math.cos(phase*3 + r*2 + c*11) * 15 * temp
            atoms.append((cx + c*spacing + dx, cy + r*spacing + dy))
            
    for i, p1 in enumerate(atoms):
        for j, p2 in enumerate(atoms[i+1:]):
            dist = math.hypot(p1[0]-p2[0], p1[1]-p2[1])
            if dist < spacing * 1.5:
                strain = abs(dist - spacing) / spacing
                col = palette["danger"] if strain > 0.2 else palette["primary"]
                canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=col, width=2)
                
    for ax, ay in atoms:
        col = palette["accent"] if temp > 0.8 else palette["primary"]
        canvas.create_oval(ax-8, ay-8, ax+8, ay+8, fill="#0d1b2a", outline=col, width=2)
        canvas.create_oval(ax-2, ay-2, ax+2, ay+2, fill=col, outline="")
''',

    "reactor_design": '''@register_animation("reactor_design")
def draw_reactor_design(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    cx, cy = width / 2, height / 2
    phase = tick * 0.05 * flow_factor
    
    # Tank
    canvas.create_rectangle(cx - 80, cy - 100, cx + 80, cy + 100, fill="#0d1b2a", outline=palette["primary"], width=3)
    
    # Impeller
    canvas.create_line(cx, cy - 100, cx, cy + 80, fill=palette["secondary"], width=4)
    angle = phase * 5
    canvas.create_line(cx - math.cos(angle)*40, cy + 80 + math.sin(angle)*10, cx + math.cos(angle)*40, cy + 80 - math.sin(angle)*10, fill=palette["secondary"], width=6)
    
    # Particles
    import random
    random.seed(42)
    for i in range(40):
        px = cx - 70 + (i*13 % 140)
        py = cy - 90 + (i*17 % 180)
        
        # swirl
        dx = math.sin(phase*3 + py*0.05) * 20
        px += dx
        
        progress = (math.sin(phase + i) + 1)/2
        col = palette["primary"] if progress < 0.4 else palette["danger"] if progress < 0.8 else palette["accent"]
        
        canvas.create_oval(px-4, py-4, px+4, py+4, fill=col, outline="")
''',

    "cfd_solver": '''@register_animation("cfd_solver")
def draw_cfd_solver(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    cx, cy = width / 2, height / 2
    phase = tick * 0.05 * flow_factor
    
    obs_r = 40
    canvas.create_oval(cx - obs_r, cy - obs_r, cx + obs_r, cy + obs_r, fill="#121e2b", outline=palette["accent"], width=3)
    
    for i in range(15):
        y_start = cy - 100 + i * 15
        pts = []
        for x in range(int(width*0.1), int(width*0.9), 10):
            dist = math.hypot(x - cx, y_start - cy)
            y = y_start
            
            if dist < obs_r * 2.5:
                deflection = (obs_r * 40) / max(dist, 1)
                y += (y_start - cy) / abs(y_start - cy + 0.001) * deflection
                
            if x > cx and dist < obs_r * 3:
                y += math.sin(x*0.05 - phase*5) * 10 # wake turbulence
                
            pts.extend([x, y])
            
        color = palette["danger"] if abs(y_start - cy) < obs_r else palette["primary"]
        canvas.create_line(*pts, fill=color, smooth=True, width=2)
''',

    "robot_kinematics": '''@register_animation("robot_kinematics")
def draw_robot_kinematics(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    cx, cy = width / 2, height / 2
    phase = tick * 0.05 * flow_factor
    
    # Target
    tx = cx + 80 + math.sin(phase * 1.5) * 60
    ty = cy + 40 + math.cos(phase * 2) * 50
    canvas.create_oval(tx - 8, ty - 8, tx + 8, ty + 8, outline=palette["danger"], width=2, dash=(2, 2))
    canvas.create_line(tx-12, ty, tx+12, ty, fill=palette["danger"])
    canvas.create_line(tx, ty-12, tx, ty+12, fill=palette["danger"])
    
    # Base
    bx, by = cx - 100, cy + 80
    canvas.create_rectangle(bx - 30, by, bx + 30, by + 20, fill="#121e2b", outline=palette["secondary"], width=3)
    
    # 2D IK
    l1, l2 = 120, 100
    dist = min(math.hypot(tx - bx, ty - by), l1 + l2 - 1)
    
    angle_target = math.atan2(ty - by, tx - bx)
    
    cos_angle_2 = (dist*dist - l1*l1 - l2*l2) / (2 * l1 * l2)
    cos_angle_2 = max(-1, min(1, cos_angle_2))
    angle_2 = math.acos(cos_angle_2)
    
    cos_angle_1 = (dist*dist + l1*l1 - l2*l2) / (2 * dist * l1)
    cos_angle_1 = max(-1, min(1, cos_angle_1))
    angle_1 = math.acos(cos_angle_1)
    
    j1x = bx + math.cos(angle_target - angle_1) * l1
    j1y = by + math.sin(angle_target - angle_1) * l1
    
    # Links
    canvas.create_line(bx, by, j1x, j1y, fill=palette["primary"], width=12, capstyle=tk.ROUND)
    canvas.create_line(bx, by, j1x, j1y, fill="#121e2b", width=6, capstyle=tk.ROUND)
    
    canvas.create_line(j1x, j1y, tx, ty, fill=palette["accent"], width=8, capstyle=tk.ROUND)
    canvas.create_line(j1x, j1y, tx, ty, fill="#121e2b", width=4, capstyle=tk.ROUND)
    
    # Joints
    for jx, jy in [(bx, by), (j1x, j1y)]:
        canvas.create_oval(jx - 10, jy - 10, jx + 10, jy + 10, fill=palette["secondary"], outline="")
        canvas.create_oval(jx - 4, jy - 4, jx + 4, jy + 4, fill="#0d1b2a", outline="")
'''
}

for key, content in reverts.items():
    # Find block starting with @register_animation("key") and ending at the next @register_animation or end of file
    pattern = r'@register_animation\("' + key + r'"\).*?(?=@register_animation|\Z)'
    orig = re.sub(pattern, content + '\n\n', orig, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(orig)

print("Reverted 5 animations successfully")
