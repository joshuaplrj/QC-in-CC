"""
Custom Animations Dispatcher
Maps specific system keys to their unique animation functions.
"""
import math
import tkinter as tk

ANIMATION_DISPATCH = {}

def register_animation(system_key: str):
    def decorator(func):
        ANIMATION_DISPATCH[system_key] = func
        return func
    return decorator

# ==========================================
# AEROSPACE SYSTEMS
# ==========================================



import math
import tkinter as tk




@register_animation("aircraft_weight")
def draw_aircraft_weight(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Draw aircraft silhouette
    body_w, body_h = width * 0.4, height * 0.1
    wing_span, wing_root = width * 0.7, height * 0.25
    
    points = [
        cx - body_w, cy, 
        cx - body_w*0.8, cy - body_h,
        cx + body_w*0.6, cy - body_h*0.8,
        cx + body_w, cy,
        cx + body_w*0.6, cy + body_h*0.8,
        cx - body_w*0.8, cy + body_h,
    ]
    canvas.create_polygon(*points, fill="#0d1b2a", outline=palette["primary"], width=2)
    
    wings = [
        cx - body_w*0.2, cy,
        cx + body_w*0.2, cy - wing_span*0.5,
        cx + body_w*0.4, cy - wing_span*0.4,
        cx + body_w*0.2, cy,
        cx + body_w*0.4, cy + wing_span*0.4,
        cx + body_w*0.2, cy + wing_span*0.5,
        cx - body_w*0.2, cy,
    ]
    canvas.create_polygon(*wings, fill="#121e2b", outline=palette["secondary"], width=2)
    
    # Draw dynamic load vectors
    num_loads = 8
    for i in range(num_loads):
        x = cx - body_w*0.6 + i * (body_w*1.2) / (num_loads-1)
        load_mag = 40 + math.sin(phase*2 + i)*20
        y_start = cy - body_h*1.5 - load_mag
        
        color = palette["danger"] if load_mag > 50 else palette["accent"]
        canvas.create_line(x, y_start, x, cy - body_h*0.5, fill=color, width=3, arrow=tk.LAST)
        
        canvas.create_text(x, y_start - 10, text=f"{int(load_mag)}kN", fill=color, font=("Consolas", 8, "bold"))
        
        # Stress internal indicators
        stress_r = load_mag * 0.15
        canvas.create_oval(x - stress_r, cy - stress_r, x + stress_r, cy + stress_r, fill=color, stipple="gray50", outline="")

@register_animation("turbojet")
def draw_turbojet(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.08 * flow_factor
    cx, cy = width * 0.4, height * 0.5
    r_core, r_outer = height * 0.15, height * 0.3
    
    # Engine housing
    canvas.create_arc(cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer, start=90, extent=270, outline=palette["secondary"], style=tk.ARC, width=3)
    canvas.create_oval(cx - r_core, cy - r_core, cx + r_core, cy + r_core, fill="#0d1b2a", outline=palette["primary"], width=2)
    
    # Rotating turbine blades
    num_blades = 16
    for i in range(num_blades):
        angle = phase*2 + i * (2*math.pi / num_blades)
        x_inner = cx + math.cos(angle) * r_core
        y_inner = cy + math.sin(angle) * r_core
        x_outer = cx + math.cos(angle + 0.2) * r_outer * 0.95
        y_outer = cy + math.sin(angle + 0.2) * r_outer * 0.95
        
        blade_color = palette["accent"] if i % 2 == 0 else palette["primary"]
        canvas.create_line(x_inner, y_inner, x_outer, y_outer, fill=blade_color, width=4)
        canvas.create_line(x_inner, y_inner, x_outer, y_outer, fill="#fff", width=1)
        
    # Combustor glow and exhaust
    for flame in range(12):
        fx = cx + r_outer + flame*15
        f_amp = 30 + math.sin(phase*5 + flame)*15
        fy_top = cy - f_amp
        fy_bot = cy + f_amp
        
        f_color = palette["danger"] if flame < 5 else palette["accent"] if flame < 9 else palette["primary"]
        dash_pat = (4, 4) if flame > 6 else None
        canvas.create_line(fx, fy_top, fx + 15, cy, fx, fy_bot, fill=f_color, width=3, smooth=True, dash=dash_pat)
        
        canvas.create_oval(fx-4, cy + math.sin(phase*8 + flame)*20 - 4, fx+4, cy + math.sin(phase*8 + flame)*20 + 4, fill="#fff", outline="")

@register_animation("panel_method")
def draw_panel_method(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.04 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Draw airfoil shape
    c_len = width * 0.6
    airfoil_pts = []
    num_panels = 30
    for i in range(num_panels):
        t = i / (num_panels-1)
        x = cx - c_len/2 + t*c_len
        # NACA 0012 approx
        yt = 5 * 0.12 * c_len * (0.2969*math.sqrt(t) - 0.126*t - 0.3516*(t**2) + 0.2843*(t**3) - 0.1015*(t**4))
        airfoil_pts.extend([x, cy - yt])
    for i in range(num_panels-1, -1, -1):
        t = i / (num_panels-1)
        x = cx - c_len/2 + t*c_len
        yt = 5 * 0.12 * c_len * (0.2969*math.sqrt(t) - 0.126*t - 0.3516*(t**2) + 0.2843*(t**3) - 0.1015*(t**4))
        airfoil_pts.extend([x, cy + yt])
        
    canvas.create_polygon(*airfoil_pts, fill="#121e2b", outline=palette["primary"], width=2)
    
    # Draw flow vectors and panel normals
    for i in range(0, len(airfoil_pts), 4):
        px, py = airfoil_pts[i], airfoil_pts[i+1]
        nx = 0 # simple normal approx for visual
        ny = -1 if py < cy else 1
        
        # Pulsing panels
        pulse = math.sin(phase*3 + px*0.01) * 0.5 + 0.5
        color = palette["danger"] if pulse > 0.8 else palette["accent"]
        
        canvas.create_oval(px-3, py-3, px+3, py+3, fill=color, outline="")
        canvas.create_line(px, py, px, py + ny*20*pulse, fill=color, width=2, arrow=tk.LAST)
        
    # Flow lines
    for line in range(-5, 6):
        flow_pts = []
        y_start = cy + line * 30
        for x_step in range(0, int(width), 20):
            # Deflect near airfoil
            dist = math.hypot(x_step - cx, y_start - cy)
            deflect = 0
            if dist < c_len/2:
                deflect = math.exp(-dist/50) * 40 * (-1 if line < 0 else 1)
                
            x_anim = x_step + (phase * 100) % 20
            flow_pts.extend([x_anim, y_start + deflect + math.sin(phase + x_step*0.05)*5])
            
        color_flow = palette["secondary"] if abs(line) > 2 else palette["primary"]
        canvas.create_line(*flow_pts, fill=color_flow, smooth=True, width=1)

@register_animation("composite")
def draw_composite(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.03 * flow_factor
    layers = 5
    layer_h = height * 0.8 / layers
    
    for l in range(layers):
        y_center = height * 0.1 + l * layer_h + layer_h/2
        
        # alternating fiber angles
        angle_deg = 45 if l % 2 == 0 else -45
        if l == layers//2: angle_deg = 0
        
        color = palette["secondary"] if l % 2 == 0 else palette["primary"]
        if l == layers//2: color = palette["accent"]
        
        # Layer boundary
        canvas.create_rectangle(width*0.1, y_center - layer_h*0.4, width*0.9, y_center + layer_h*0.4, fill="#0d1b2a", outline=color, width=2)
        
        # Draw fibers
        fiber_spacing = 20
        stress = math.sin(phase*2 + l) * 10 # shear stress visualization
        
        for fx in range(int(width*0.1), int(width*0.9), fiber_spacing):
            if angle_deg == 0:
                canvas.create_line(fx + stress, y_center - layer_h*0.3, fx + stress, y_center + layer_h*0.3, fill=color, width=3)
            else:
                x_off = layer_h*0.6 * math.tan(math.radians(angle_deg))
                canvas.create_line(fx - x_off + stress, y_center - layer_h*0.3, fx + x_off + stress, y_center + layer_h*0.3, fill=color, width=2)
                
            # Interlaminar defects/stress points
            if fx % 80 == 0:
                pulse = math.sin(phase*5 + fx + l) * 0.5 + 0.5
                if pulse > 0.7:
                    canvas.create_oval(fx - 4, y_center - layer_h*0.4 - 4, fx + 4, y_center - layer_h*0.4 + 4, fill=palette["danger"], outline="")

@register_animation("orbital")
def draw_orbital(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Central body (Earth/Planet)
    canvas.create_oval(cx - 40, cy - 40, cx + 40, cy + 40, fill="#121e2b", outline=palette["primary"], width=3)
    canvas.create_oval(cx - 50, cy - 50, cx + 50, cy + 50, outline=palette["secondary"], width=1, dash=(2, 4))
    
    orbits = [
        (width * 0.2, height * 0.15, 0.8, palette["primary"]),   # LEO
        (width * 0.35, height * 0.25, 0.4, palette["secondary"]),# MEO
        (width * 0.45, height * 0.35, 0.2, palette["accent"])    # HEO/GTO (elliptical)
    ]
    
    for idx, (a, b, speed, color) in enumerate(orbits):
        # Draw orbit path
        canvas.create_oval(cx - a, cy - b, cx + a, cy + b, outline=color, width=1, dash=(4, 4))
        
        # Draw satellite
        angle = phase * speed + idx * 2.0
        sat_x = cx + math.cos(angle) * a
        sat_y = cy + math.sin(angle) * b
        
        canvas.create_rectangle(sat_x - 6, sat_y - 6, sat_x + 6, sat_y + 6, fill="#0d1b2a", outline=color, width=2)
        canvas.create_line(sat_x - 12, sat_y, sat_x + 12, sat_y, fill=color, width=2) # solar panels
        
        # Sensor cone/beam directed to center
        beam_dist = 40
        beam_x = sat_x - math.cos(angle) * beam_dist
        beam_y = sat_y - math.sin(angle) * beam_dist
        canvas.create_polygon(sat_x, sat_y, sat_x - math.cos(angle - 0.2)*beam_dist, sat_y - math.sin(angle - 0.2)*beam_dist,
                              sat_x - math.cos(angle + 0.2)*beam_dist, sat_y - math.sin(angle + 0.2)*beam_dist,
                              fill=color, stipple="gray25", outline="")
                              
        # Data transmission pulses
        pulse_r = (phase * 100 + idx*50) % math.hypot(a, b)
        if pulse_r > 10 and pulse_r < a:
            pulse_x = sat_x - math.cos(angle) * pulse_r
            pulse_y = sat_y - math.sin(angle) * pulse_r
            canvas.create_oval(pulse_x-3, pulse_y-3, pulse_x+3, pulse_y+3, fill=palette["danger"], outline="")

@register_animation("hypersonic")
def draw_hypersonic(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.08 * flow_factor
    cx, cy = width * 0.3, height * 0.5
    
    # Hypersonic vehicle (waverider shape)
    v_len, v_width = 120, 40
    vehicle = [
        cx + v_len, cy,
        cx, cy - v_width,
        cx - 20, cy - v_width,
        cx + 20, cy,
        cx - 20, cy + v_width,
        cx, cy + v_width
    ]
    canvas.create_polygon(*vehicle, fill="#121e2b", outline=palette["primary"], width=2)
    
    # Bow shockwave
    shock_pts = []
    cone_angle = 0.3 + math.sin(phase)*0.05 # oscillating Mach cone
    for y in range(-int(height/2), int(height/2), 10):
        x = cx + v_len - abs(y) / math.tan(cone_angle)
        shock_pts.extend([x, cy + y])
    canvas.create_line(*shock_pts, fill=palette["danger"], width=4, smooth=True)
    canvas.create_line(*shock_pts, fill="#fff", width=1, smooth=True)
    
    # Secondary shockwaves / Plasma sheath
    for i in range(1, 4):
        offset = i * 20
        sheath_pts = []
        for y in range(-int(height/3), int(height/3), 15):
            x = cx + v_len - offset - abs(y) / math.tan(cone_angle + i*0.1)
            sheath_pts.extend([x, cy + y])
        canvas.create_line(*sheath_pts, fill=palette["accent"] if i==1 else palette["secondary"], width=2, dash=(4, 4), smooth=True)

    # High temp ablation particles
    for i in range(30):
        px = cx + v_len - (phase*200 + i*13) % (v_len*2)
        py = cy + (math.sin(phase*10 + i)*v_width*1.5)
        if px < cx + v_len: # behind nose
            p_color = palette["danger"] if px > cx else palette["accent"]
            canvas.create_oval(px-2, py-2, px+2, py+2, fill=p_color, outline="")
            
@register_animation("trajectory")
def draw_trajectory(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Launch pad and target
    pad_x, pad_y = width * 0.1, height * 0.8
    tar_x, tar_y = width * 0.9, height * 0.8
    
    canvas.create_rectangle(pad_x-10, pad_y, pad_x+10, height, fill="#1a2b3d", outline=palette["secondary"], width=2)
    canvas.create_polygon(tar_x-15, tar_y, tar_x+15, tar_y, tar_x, tar_y+20, fill=palette["danger"], outline="")
    
    # Optimal Trajectory (Parabola/Ballistic)
    peak_y = height * 0.2
    traj_pts = []
    steps = 50
    for i in range(steps):
        t = i / (steps-1)
        x = pad_x + t*(tar_x - pad_x)
        # Parabola y = 4h(t - t^2)
        y = pad_y - 4*(pad_y - peak_y)*(t - t**2)
        traj_pts.extend([x, y])
    canvas.create_line(*traj_pts, fill=palette["secondary"], width=2, dash=(4, 4), smooth=True)
    
    # Active vehicle integrating path
    curr_t = (phase * 0.5) % 1.0
    vx = pad_x + curr_t*(tar_x - pad_x)
    vy = pad_y - 4*(pad_y - peak_y)*(curr_t - curr_t**2)
    
    # Vehicle flame/trail
    trail_len = 10
    for t_step in range(1, trail_len):
        past_t = max(0.0, curr_t - t_step*0.01)
        tx = pad_x + past_t*(tar_x - pad_x)
        ty = pad_y - 4*(pad_y - peak_y)*(past_t - past_t**2)
        canvas.create_oval(tx-t_step, ty-t_step, tx+t_step, ty+t_step, fill=palette["danger"], outline="")
        
    canvas.create_oval(vx-6, vy-6, vx+6, vy+6, fill="#121e2b", outline=palette["primary"], width=2)
    
    # Targeting computer/telemetry lines
    canvas.create_line(vx, vy, vx, height, fill=palette["primary"], dash=(2, 6))
    canvas.create_line(vx, vy, pad_x, vy, fill=palette["primary"], dash=(2, 6))
    canvas.create_text(vx + 30, vy - 20, text=f"Alt: {int(height-vy)}m", fill=palette["accent"], font=("Consolas", 8))
    canvas.create_text(vx + 30, vy - 10, text=f"Rng: {int(vx-pad_x)}m", fill=palette["accent"], font=("Consolas", 8))


# ==========================================
# CIVIL SYSTEMS
# ==========================================

@register_animation("bridge_analysis")
def draw_bridge_analysis(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.04 * flow_factor
    ground = height * 0.75
    
    # River/Ground
    canvas.create_rectangle(0, ground, width, height, fill="#0a1520", outline="")
    canvas.create_line(0, ground, width, ground, fill=palette["primary"], width=2)
    
    # Truss Bridge Nodes
    nodes_x = [width * (0.15 + i*0.14) for i in range(6)]
    deck_y = height * 0.45
    arch_y = height * 0.25
    
    # Draw moving load
    load_pos = (phase * 150) % (width * 0.7) + width * 0.15
    canvas.create_rectangle(load_pos-20, deck_y-30, load_pos+20, deck_y, fill="#121e2b", outline=palette["accent"], width=2)
    canvas.create_line(load_pos, deck_y, load_pos, deck_y+40, fill=palette["danger"], width=4, arrow=tk.LAST)
    
    # Connecting members
    for i in range(len(nodes_x)-1):
        x1, x2 = nodes_x[i], nodes_x[i+1]
        
        # Calculate localized stress based on load proximity
        dist1 = abs((x1+x2)/2 - load_pos)
        stress1 = max(0, 1.0 - dist1/150.0)
        c_deck = palette["danger"] if stress1 > 0.6 else palette["accent"] if stress1 > 0.3 else palette["secondary"]
        c_arch = palette["danger"] if stress1 > 0.5 else palette["primary"]
        
        # Give displacement (deflection)
        deflect_y1 = deck_y + stress1*15
        deflect_y2 = deck_y + max(0, 1.0 - abs((nodes_x[min(i+2, len(nodes_x)-1)]+x2)/2 - load_pos)/150.0)*15
        
        # Deck
        canvas.create_line(x1, deflect_y1, x2, deflect_y2, fill=c_deck, width=4)
        # Top arch
        canvas.create_line(x1, arch_y, x2, arch_y, fill=c_arch, width=3)
        # Vertical
        canvas.create_line(x1, arch_y, x1, deflect_y1, fill=c_arch, width=2)
        # Diagonal
        canvas.create_line(x1, arch_y, x2, deflect_y2, fill=c_deck, width=2)
        
        # Node joints
        canvas.create_oval(x1-4, arch_y-4, x1+4, arch_y+4, fill="#0d1b2a", outline=palette["primary"], width=2)
        canvas.create_oval(x1-4, deflect_y1-4, x1+4, deflect_y1+4, fill="#0d1b2a", outline=palette["primary"], width=2)
        
    # Final rightmost nodes
    x_last = nodes_x[-1]
    canvas.create_line(x_last, arch_y, x_last, deck_y, fill=palette["primary"], width=2)
    canvas.create_oval(x_last-4, arch_y-4, x_last+4, arch_y+4, fill="#0d1b2a", outline=palette["primary"], width=2)
    canvas.create_oval(x_last-4, deck_y-4, x_last+4, deck_y+4, fill="#0d1b2a", outline=palette["primary"], width=2)

    # Piers
    canvas.create_rectangle(nodes_x[0]-15, deck_y, nodes_x[0]+15, ground, fill="#121e2b", outline=palette["secondary"], width=2)
    canvas.create_rectangle(nodes_x[-1]-15, deck_y, nodes_x[-1]+15, ground, fill="#121e2b", outline=palette["secondary"], width=2)

@register_animation("traffic_flow")
def draw_traffic_flow(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # City layout grid
    roads = [
        # Horizontal
        (height * 0.3, True), (height * 0.7, True),
        # Vertical
        (width * 0.3, False), (width * 0.7, False)
    ]
    
    for pos, is_horiz in roads:
        if is_horiz:
            canvas.create_line(0, pos-15, width, pos-15, fill=palette["grid"], width=1)
            canvas.create_line(0, pos+15, width, pos+15, fill=palette["grid"], width=1)
            canvas.create_line(0, pos, width, pos, fill=palette["secondary"], width=1, dash=(4, 4))
        else:
            canvas.create_line(pos-15, 0, pos-15, height, fill=palette["grid"], width=1)
            canvas.create_line(pos+15, 0, pos+15, height, fill=palette["grid"], width=1)
            canvas.create_line(pos, 0, pos, height, fill=palette["secondary"], width=1, dash=(4, 4))

    # Intersections (Traffic Lights)
    cycle = (phase * 0.5) % 2.0
    horiz_green = cycle < 1.0
    
    intersections = [(width*0.3, height*0.3), (width*0.7, height*0.3), 
                     (width*0.3, height*0.7), (width*0.7, height*0.7)]
                     
    for ix, iy in intersections:
        c_horiz = palette["accent"] if horiz_green else palette["danger"]
        c_vert = palette["danger"] if horiz_green else palette["accent"]
        
        canvas.create_oval(ix - 25, iy - 25, ix + 25, iy + 25, fill="#0d1b2a", outline=palette["primary"], width=1)
        # Horiz lights
        canvas.create_oval(ix - 20, iy - 6, ix - 14, iy + 6, fill=c_horiz, outline="")
        canvas.create_oval(ix + 14, iy - 6, ix + 20, iy + 6, fill=c_horiz, outline="")
        # Vert lights
        canvas.create_oval(ix - 6, iy - 20, ix + 6, iy - 14, fill=c_vert, outline="")
        canvas.create_oval(ix - 6, iy + 14, ix + 6, iy + 20, fill=c_vert, outline="")
        
    # Draw vehicles
    for i in range(12):
        # determine road
        road_idx = i % 4
        pos, is_horiz = roads[road_idx]
        
        speed = 100
        raw_dist = (phase * speed + i * 80) % (width if is_horiz else height)
        
        # Stop logic at intersections
        is_stopped = False
        if is_horiz and not horiz_green:
            if abs(raw_dist - (width*0.3 - 30)) < 15 or abs(raw_dist - (width*0.7 - 30)) < 15:
                is_stopped = True
        elif not is_horiz and horiz_green:
            if abs(raw_dist - (height*0.3 - 30)) < 15 or abs(raw_dist - (height*0.7 - 30)) < 15:
                is_stopped = True
                
        # Modulate distance if stopped (very basic visual approx)
        dist = raw_dist
        if is_stopped:
            # snap to stop line
            if abs(raw_dist - width*0.3) < 45: dist = width*0.3 - 30
            elif abs(raw_dist - width*0.7) < 45: dist = width*0.7 - 30
            elif abs(raw_dist - height*0.3) < 45: dist = height*0.3 - 30
            elif abs(raw_dist - height*0.7) < 45: dist = height*0.7 - 30
            
        lane_offset = 8 if i % 2 == 0 else -8
            
        if is_horiz:
            vx, vy = dist, pos + lane_offset
            car_poly = [vx-6, vy-4, vx+6, vy-4, vx+6, vy+4, vx-6, vy+4]
        else:
            vx, vy = pos + lane_offset, dist
            car_poly = [vx-4, vy-6, vx+4, vy-6, vx+4, vy+6, vx-4, vy+6]
            
        color = palette["danger"] if is_stopped else palette["primary"]
        canvas.create_polygon(*car_poly, fill=color, outline="#fff", width=1)

@register_animation("water_network")
def draw_water_network(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    nodes = {
        "Res": (width*0.1, height*0.2),
        "Pump": (width*0.3, height*0.4),
        "Tank": (width*0.5, height*0.2),
        "J1": (width*0.5, height*0.6),
        "J2": (width*0.7, height*0.4),
        "City": (width*0.9, height*0.8)
    }
    
    pipes = [
        ("Res", "Pump", 12),
        ("Pump", "Tank", 8),
        ("Pump", "J1", 10),
        ("Tank", "J2", 8),
        ("J1", "J2", 6),
        ("J2", "City", 14),
        ("J1", "City", 8)
    ]
    
    # Draw pipes and flow particles
    for a_key, b_key, diam in pipes:
        ax, ay = nodes[a_key]
        bx, by = nodes[b_key]
        
        # Pipe outline
        canvas.create_line(ax, ay, bx, by, fill=palette["grid"], width=diam+4, capstyle=tk.ROUND)
        canvas.create_line(ax, ay, bx, by, fill="#0d1b2a", width=diam, capstyle=tk.ROUND)
        
        # Water flow particles mapped by phase
        dist = math.hypot(bx-ax, by-ay)
        num_particles = int(dist / 20)
        for p in range(num_particles):
            u = (phase * 1.5 + p / num_particles) % 1.0
            px = ax + (bx - ax) * u
            py = ay + (by - ay) * u
            
            # Pressure gradient color
            p_color = palette["accent"] if u > 0.8 else palette["primary"]
            canvas.create_oval(px-diam/2+1, py-diam/2+1, px+diam/2-1, py+diam/2-1, fill=p_color, outline="")
            
    # Draw nodes
    for name, (x, y) in nodes.items():
        if name == "Res":
            canvas.create_polygon(x-20, y-10, x+20, y-10, x+15, y+15, x-15, y+15, fill=palette["primary"], outline="#fff", width=1)
        elif name == "Tank":
            water_lvl = 10 + math.sin(phase)*5
            canvas.create_rectangle(x-15, y-15, x+15, y+15, fill="#121e2b", outline=palette["secondary"], width=2)
            canvas.create_rectangle(x-13, y+13-water_lvl, x+13, y+13, fill=palette["secondary"], outline="")
        elif name == "City":
            for b in range(4):
                canvas.create_rectangle(x-20+b*10, y+15-b*8, x-12+b*10, y+15, fill=palette["accent"], outline="")
        elif name == "Pump":
            canvas.create_oval(x-12, y-12, x+12, y+12, fill=palette["danger"], outline="#fff", width=2)
            pulse = math.sin(phase*10)*3
            canvas.create_oval(x-12-pulse, y-12-pulse, x+12+pulse, y+12+pulse, outline=palette["danger"], width=1)
        else: # Junctions
            canvas.create_oval(x-6, y-6, x+6, y+6, fill="#0d1b2a", outline=palette["primary"], width=2)
            
        canvas.create_text(x, y-25, text=name, fill=palette["text"], font=("Segoe UI", 8))

@register_animation("seismic_analysis")
def draw_seismic_analysis(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.06 * flow_factor
    epicenter_x, epicenter_y = width * 0.3, height * 0.8
    
    # Draw ground layers
    for i in range(4):
        y = height * 0.3 + i * (height * 0.2)
        canvas.create_line(0, y, width, y, fill=palette["grid"], width=2)
        
    # Fault line
    canvas.create_line(width*0.2, height, width*0.5, height*0.3, fill=palette["danger"], width=3, dash=(8, 4))
    
    # Epicenter pulse
    for r in range(1, 4):
        radius = (phase * 50 + r * 40) % 250
        opacity = max(0, 1.0 - radius/250.0)
        if opacity > 0:
            color = palette["danger"] if r == 1 else palette["accent"]
            canvas.create_oval(epicenter_x-radius, epicenter_y-radius, epicenter_x+radius, epicenter_y+radius, 
                               outline=color, width=int(opacity*5), dash=(4, 6))
                               
    # Buildings responding to waves
    num_buildings = 5
    for i in range(num_buildings):
        bx = width * 0.3 + i * 100
        by = height * 0.3 # surface
        
        # Calculate wave arrival and sway
        dist = math.hypot(bx - epicenter_x, by - epicenter_y)
        sway = 0
        if dist < (phase * 50) % 250 + 50: # if wave reached
            sway = math.sin(phase*8 + dist*0.1) * (100 / (dist*0.05 + 1))
            
        # Draw building with sway
        b_width = 30
        b_height = 80 + i*20
        
        # Polygon with shear deformation
        b_poly = [
            bx - b_width/2, by,
            bx + b_width/2, by,
            bx + b_width/2 + sway, by - b_height,
            bx - b_width/2 + sway, by - b_height
        ]
        
        # Color based on stress (sway amt)
        b_color = palette["danger"] if abs(sway) > 10 else palette["secondary"] if abs(sway) > 5 else "#121e2b"
        canvas.create_polygon(*b_poly, fill=b_color, outline=palette["primary"], width=2)
        
        # Windows
        for wy in range(10, b_height, 20):
            wx = bx + (sway * (wy/b_height))
            canvas.create_rectangle(wx - b_width*0.3, by - wy - 5, wx + b_width*0.3, by - wy + 5, fill="#0d1b2a", outline="")

@register_animation("construction")
def draw_construction(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.04 * flow_factor
    ground = height * 0.8
    
    canvas.create_line(0, ground, width, ground, fill=palette["primary"], width=3)
    
    # Building Frame (Beam structure)
    cols, rows = 5, 4
    spacing_x, spacing_y = 60, 50
    start_x = width * 0.3
    
    for r in range(rows):
        y = ground - (r+1)*spacing_y
        # determine completion status
        progress_thresh = (r * cols) / (rows*cols)
        current_progress = (phase*0.2) % 1.2 # slightly over 1 to pause at end
        
        for c in range(cols):
            x = start_x + c*spacing_x
            
            item_progress = (r*cols + c) / (rows*cols)
            is_built = current_progress > item_progress
            is_active = item_progress <= current_progress < item_progress + 0.1
            
            color = palette["secondary"] if is_built else palette["grid"]
            if is_active: color = palette["accent"]
                
            # vertical beams
            canvas.create_line(x, y+spacing_y, x, y, fill=color, width=4)
            # horizontal beams
            if c < cols - 1:
                canvas.create_line(x, y, x+spacing_x, y, fill=color, width=4)
                
            if is_active:
                canvas.create_oval(x-10, y-10, x+10, y+10, outline=palette["danger"], width=2, dash=(2, 2))
                
    # Crane
    crane_base_x = start_x - 80
    canvas.create_line(crane_base_x, ground, crane_base_x, ground - rows*spacing_y - 80, fill=palette["accent"], width=6)
    canvas.create_line(crane_base_x-20, ground - rows*spacing_y - 60, crane_base_x + cols*spacing_x + 40, ground - rows*spacing_y - 60, fill=palette["accent"], width=4)
    
    # Crane trolley & hook
    trolley_x = crane_base_x + 20 + abs(math.sin(phase*2))*(cols*spacing_x)
    canvas.create_rectangle(trolley_x-10, ground - rows*spacing_y - 65, trolley_x+10, ground - rows*spacing_y - 55, fill="#121e2b", outline=palette["primary"], width=2)
    
    hook_len = 30 + abs(math.cos(phase*3))*50
    canvas.create_line(trolley_x, ground - rows*spacing_y - 55, trolley_x, ground - rows*spacing_y - 55 + hook_len, fill=palette["primary"], width=2)
    canvas.create_arc(trolley_x-5, ground - rows*spacing_y - 55 + hook_len, trolley_x+5, ground - rows*spacing_y - 55 + hook_len + 10, start=180, extent=-180, style=tk.ARC, outline=palette["danger"], width=2)

@register_animation("urban_planning")
def draw_urban_planning(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.03 * flow_factor
    
    # Isometric grid base
    cx, cy = width * 0.5, height * 0.7
    grid_size = 40
    rows, cols = 6, 6
    
    def to_iso(r, c, h=0):
        # Isometric projection simple math
        x = cx + (c - r) * grid_size * 0.866
        y = cy + (c + r) * grid_size * 0.5 - h
        return x, y
        
    for r in range(rows):
        for c in range(cols):
            # Base tile
            p1 = to_iso(r, c)
            p2 = to_iso(r, c+1)
            p3 = to_iso(r+1, c+1)
            p4 = to_iso(r+1, c)
            
            # Zoning color mapping
            zone_type = (r*3 + c*7) % 4
            colors = [palette["grid"], palette["primary"], palette["secondary"], palette["accent"]]
            base_col = colors[zone_type]
            
            canvas.create_polygon(*p1, *p2, *p3, *p4, fill="#0d1b2a", outline=base_col, width=1)
            
            # Draw building (height based on zone and optimization phase)
            target_h = ((r*13 + c*17) % 5) * 20
            if zone_type == 0: target_h = 0 # park/empty
            
            # Optimization growth animation
            current_h = target_h * (0.5 + 0.5*math.sin(phase*2 + r + c))
            
            if current_h > 5:
                # Top face
                t1, t2 = to_iso(r, c, current_h), to_iso(r, c+1, current_h)
                t3, t4 = to_iso(r+1, c+1, current_h), to_iso(r+1, c, current_h)
                canvas.create_polygon(*t1, *t2, *t3, *t4, fill=base_col, outline="#fff", width=1)
                
                # Left face
                canvas.create_polygon(*p1, *t1, *t4, *p4, fill="#121e2b", outline=base_col, width=1)
                
                # Right face
                canvas.create_polygon(*p4, *t4, *t3, *p3, fill="#1a2b3d", outline=base_col, width=1)
                
    # Optimization Scanner Plane
    scan_row = (phase * 3) % rows
    s1, s2 = to_iso(scan_row, 0, 100), to_iso(scan_row, cols, 100)
    s4, s3 = to_iso(scan_row+1, 0, 100), to_iso(scan_row+1, cols, 100)
    canvas.create_polygon(*s1, *s2, *s3, *s4, fill="", outline=palette["danger"], width=2, dash=(4, 4))

# ==========================================
# MORE ELECTRICAL & MECHANICAL
# ==========================================

@register_animation('signal_processor')
def draw_signal_processor(canvas, width, height, tick, palette, flow_factor):
    phase = tick * 0.1 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Time domain signal
    t_pts = []
    steps = int(width * 0.8)
    for x in range(steps):
        t = x * 0.05 + phase
        y = math.sin(t)*30 + math.cos(t*2.5)*15 + math.sin(t*5)*5
        t_pts.extend([width*0.1 + x, cy - 80 - y])
    canvas.create_line(*t_pts, fill=palette['secondary'], width=2)
    
    # FFT Process block
    canvas.create_rectangle(cx-40, cy-30, cx+40, cy+30, fill="#121e2b", outline=palette['primary'], width=2)
    canvas.create_text(cx, cy, text="FFT", fill=palette['text'], font=("Consolas", 12, "bold"))
    
    # Connecting arrows
    canvas.create_line(cx, cy-80, cx, cy-30, fill=palette['accent'], arrow=tk.LAST, dash=(4,2))
    canvas.create_line(cx, cy+30, cx, cy+80, fill=palette['accent'], arrow=tk.LAST, dash=(4,2))
    
    # Frequency domain spectrum
    freqs = [30, 0, 15, 0, 0, 5, 0, 0, 0, 0] # amplitudes of sin/cos combo above
    f_width = width * 0.8 / len(freqs)
    
    for i, amp in enumerate(freqs):
        bx = width*0.1 + i*f_width + f_width/2
        bh = amp * 2
        # pulse effect on peaks
        if amp > 0:
            bh += math.sin(phase*5 + i)*5
            col = palette['danger'] if i==0 else palette['primary']
            canvas.create_rectangle(bx-10, cy+80+100, bx+10, cy+80+100-bh, fill="#0d1b2a", outline=col, width=2)

@register_animation('communication_channel')
def draw_communication_channel(canvas, width, height, tick, palette, flow_factor):
    phase = tick * 0.08 * flow_factor
    
    tx, ty = width * 0.15, height * 0.5
    rx, ry = width * 0.85, height * 0.5
    
    # Transmitter / Receiver
    canvas.create_polygon(tx-20, ty-20, tx+20, ty, tx-20, ty+20, fill="#121e2b", outline=palette['primary'], width=2)
    canvas.create_polygon(rx+20, ry-20, rx-20, ry, rx+20, ry+20, fill="#121e2b", outline=palette['secondary'], width=2)
    
    # Carrier wave
    wave_pts = []
    dist = rx - tx - 40
    for x in range(int(dist)):
        px = tx + 20 + x
        
        # QPSK modulation simulation (phase shifts)
        t = (x - phase*50) * 0.05
        # Add a sudden phase shift every 40px
        symbol = int((px - phase*50) / 40) % 4
        phase_shift = symbol * (math.pi/2)
        
        # Noise
        noise = (math.sin(x*31.4)*math.cos(x*12.7)) * 10
        
        py = ty + math.sin(t + phase_shift)*20 + noise
        wave_pts.extend([px, py])
        
    canvas.create_line(*wave_pts, fill=palette['accent'], width=2)
    
    # Data packets
    for i in range(5):
        px = tx + 20 + ((phase*80 + i*60) % dist)
        canvas.create_oval(px-4, ty-4, px+4, ty+4, fill=palette['danger'], outline='')
        
        # Constellation diagram inset
        if abs(px - width/2) < 30:
            ix, iy = width*0.5, height*0.2
            canvas.create_oval(ix-30, iy-30, ix+30, iy+30, outline=palette['grid'])
            canvas.create_line(ix-35, iy, ix+35, iy, fill=palette['grid'])
            canvas.create_line(ix, iy-35, ix, iy+35, fill=palette['grid'])
            
            # plot current symbol
            symbol = int((px - phase*50) / 40) % 4
            sx = ix + math.cos(symbol*math.pi/2 + math.pi/4)*20
            sy = iy + math.sin(symbol*math.pi/2 + math.pi/4)*20
            canvas.create_oval(sx-4, sy-4, sx+4, sy+4, fill=palette['danger'], outline='')

@register_animation('manufacturing')
def draw_manufacturing(canvas, width, height, tick, palette, flow_factor):
    phase = tick * 0.05 * flow_factor
    cy = height * 0.6
    
    # Conveyor belt
    belt_y = cy + 20
    canvas.create_line(width*0.1, belt_y, width*0.9, belt_y, fill=palette['secondary'], width=4)
    for i in range(20):
        roller_x = width*0.1 + ((phase*50 + i*40) % (width*0.8))
        canvas.create_oval(roller_x-4, belt_y+2, roller_x+4, belt_y+10, outline=palette['primary'])
        
    # Robotic arms / Stations
    stations = [(width*0.3, "Weld"), (width*0.5, "Assemble"), (width*0.7, "Inspect")]
    for sx, name in stations:
        canvas.create_rectangle(sx-20, cy-80, sx+20, cy-60, fill="#1a2b3d", outline=palette['accent'])
        canvas.create_text(sx, cy-90, text=name, fill=palette['text'], font=("Segoe UI", 8))
        
        # Arm mechanism
        arm_len = 40 + math.sin(phase*3 + sx)*10
        canvas.create_line(sx, cy-60, sx, cy-60+arm_len, fill=palette['primary'], width=3)
        canvas.create_oval(sx-5, cy-60+arm_len, sx+5, cy-50+arm_len, fill=palette['danger'], outline='')
    
    # Products moving
    for i in range(5):
        px = width*0.1 + ((phase*60 + i*150) % (width*0.8))
        
        # Product evolution
        if px < width*0.3:
            canvas.create_rectangle(px-10, belt_y-20, px+10, belt_y, outline=palette['grid'], width=2) # raw
        elif px < width*0.5:
            canvas.create_rectangle(px-10, belt_y-20, px+10, belt_y, fill="#0d1b2a", outline=palette['primary'], width=2) # welded
        elif px < width*0.7:
            canvas.create_polygon(px-10, belt_y, px+10, belt_y, px, belt_y-25, fill="#121e2b", outline=palette['accent'], width=2) # assembled
        else:
            canvas.create_polygon(px-10, belt_y, px+10, belt_y, px, belt_y-25, fill=palette['danger'], outline='') # inspected/painted


# ==========================================
# NUCLEAR & PETROLEUM
# ==========================================

import math
import tkinter as tk

@register_animation('reactor_kinetics')
def draw_reactor_kinetics(canvas, width, height, tick, palette, flow_factor):
    phase = tick * 0.1 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Core vessel
    r = height * 0.3
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=palette['primary'], width=4)
    canvas.create_oval(cx-r+10, cy-r+10, cx+r-10, cy+r-10, fill="#0d1b2a", outline=palette['secondary'], width=2)
    
    # Fuel Rods & Control Rods
    for col in range(-2, 3):
        rx = cx + col * 30
        
        # Control rod insertion depth
        c_depth = math.sin(phase*0.5 + col)*30 + 30
        
        # Guide tube/Fuel
        canvas.create_line(rx, cy-r+20, rx, cy+r-20, fill=palette['accent'], width=8, capstyle=tk.ROUND)
        # Control Rod (absorber)
        canvas.create_line(rx, cy-r+15, rx, cy-r+15 + c_depth, fill=palette['danger'], width=6, capstyle=tk.ROUND)

    # Neutron population (Prompt and Delayed)
    num_neutrons = 50
    for i in range(num_neutrons):
        nx = cx - r + 20 + (i*17 % (2*r - 40))
        ny = cy - r + 20 + (i*23 % (2*r - 40))
        
        # Random walk
        dx = math.sin(phase*10 + i*5)*10
        dy = math.cos(phase*11 + i*3)*10
        
        # fission events
        if abs(dx) > 8 and abs(dy) > 8:
            canvas.create_oval(nx+dx-10, ny+dy-10, nx+dx+10, ny+dy+10, outline=palette['danger'])
            
        n_col = palette['primary'] if i % 5 != 0 else palette['secondary'] # fast vs thermal
        canvas.create_oval(nx+dx-2, ny+dy-2, nx+dx+2, ny+dy+2, fill=n_col, outline='')

@register_animation('reservoir')
def draw_reservoir(canvas, width, height, tick, palette, flow_factor):
    phase = tick * 0.05 * flow_factor
    
    # Geological strata
    canvas.create_rectangle(0, height*0.3, width, height*0.6, fill="#121e2b", outline='') # Cap rock
    canvas.create_rectangle(0, height*0.6, width, height, fill="#0a1520", outline='') # Reservoir rock
    
    # Oil/Water saturation field
    for x in range(0, int(width), 20):
        for y in range(int(height*0.6), int(height), 20):
            # Sweep efficiency front
            front_x = phase * 50
            dist_to_well = width*0.8 - x
            
            sat = 0
            if x < front_x + math.sin(y*0.05)*30: # Water replacing oil
                sat = 1.0 # water
            else:
                sat = 0.0 # oil
                
            color = palette['primary'] if sat == 1.0 else palette['accent']
            canvas.create_oval(x, y, x+10, y+10, fill=color, outline='', stipple="gray50" if sat==0.0 else "")

    # Injection Well (Water)
    ix = width * 0.2
    canvas.create_line(ix, 0, ix, height*0.9, fill=palette['primary'], width=8)
    canvas.create_line(ix, 0, ix, height*0.9, fill="#fff", width=2, dash=(4,4))
    
    # Production Well (Oil/Mix)
    px = width * 0.8
    canvas.create_line(px, 0, px, height*0.9, fill=palette['accent'], width=8)
    
    # Upward flow in production well
    for i in range(10):
        fy = height*0.9 - ((phase*100 + i*30) % (height*0.9))
        canvas.create_oval(px-3, fy-5, px+3, fy+5, fill="#fff", outline='')

# ==========================================
# COMPUTER SCIENCE SYSTEMS
# ==========================================

@register_animation("cryptography")
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


@register_animation("database_optimizer")
def draw_database_optimizer(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    rows, cols = 5, 8
    cell_w, cell_h = width * 0.6 / cols, height * 0.6 / rows
    start_x, start_y = width * 0.2, height * 0.2
    
    target_r, target_c = 2, 5
    
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * cell_w
            y = start_y + r * cell_h
            
            is_target = (r == target_r and c == target_c)
            base_prob = 1.0 / (rows*cols)
            if is_target:
                prob = base_prob + math.sin(phase)* (1.0 - base_prob) if math.sin(phase) > 0 else base_prob
            else:
                prob = base_prob - math.sin(phase)* (base_prob) if math.sin(phase) > 0 else base_prob
                
            color = palette["danger"] if is_target and prob > 0.5 else palette["primary"]
            fill_h = cell_h * max(0.1, prob*2)
            
            canvas.create_rectangle(x, y, x + cell_w, y + cell_h, outline=palette["grid"])
            canvas.create_rectangle(x + 2, y + cell_h - fill_h, x + cell_w - 2, y + cell_h, fill=color, outline="")

    # Query pointer
    px = start_x + target_c * cell_w + cell_w/2
    py = start_y + target_r * cell_h + cell_h/2
    if math.sin(phase) > 0.8:
        canvas.create_oval(px-cell_w, py-cell_h, px+cell_w, py+cell_h, outline=palette["accent"], width=2, dash=(4,4))

@register_animation("compiler_optimizer")
def draw_compiler_optimizer(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, 50
    
    levels = 4
    nodes = {}
    for l in range(levels):
        num_nodes = 2**l
        for n in range(num_nodes):
            x = width * (n + 0.5) / num_nodes
            y = cy + l * 60
            
            folded = False
            if l == 3 and (n % 3 == 0):
                folded = math.sin(phase + n) > 0
            elif l == 2 and n == 1:
                folded = math.sin(phase*0.5) > 0
                
            nodes[(l, n)] = (x, y, folded)
            
            if l > 0:
                px, py, p_folded = nodes[(l-1, n//2)]
                if not p_folded and not folded:
                    color = palette["secondary"] if l%2==0 else palette["primary"]
                    canvas.create_line(px, py, x, y, fill=color, width=2)
                    
    for (l, n), (x, y, folded) in nodes.items():
        if not folded:
            rad = 12 if l < 3 else 8
            color = palette["accent"] if (l*n + tick//10)%5 == 0 else "#121e2b"
            canvas.create_oval(x-rad, y-rad, x+rad, y+rad, fill=color, outline=palette["primary"], width=2)
            
    scan_y = cy + (phase*40 % (levels*60))
    canvas.create_line(0, scan_y, width, scan_y, fill=palette["danger"], dash=(2, 4))
    
@register_animation("blockchain_simulator")
def draw_blockchain_simulator(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    num_blocks = 4
    block_w, block_h = 60, 80
    spacing = width * 1.0 / (num_blocks+1)
    
    for i in range(num_blocks):
        bx = spacing * (i+1)
        by = cy + math.sin(phase*2 + i)*10
        
        if i > 0:
            prev_x = spacing * i
            prev_y = cy + math.sin(phase*2 + i - 1)*10
            canvas.create_line(prev_x + block_w/2, prev_y, bx - block_w/2, by, fill=palette["accent"], width=3, dash=(4,4))
            
            hx = prev_x + block_w/2 + (bx - prev_x - block_w) * ((phase*1.5)%1.0)
            hy = prev_y + (by - prev_y) * ((phase*1.5)%1.0)
            canvas.create_oval(hx-4, hy-4, hx+4, hy+4, fill=palette["danger"], outline="")
            
        canvas.create_rectangle(bx - block_w/2, by - block_h/2, bx + block_w/2, by + block_h/2, fill="#0d1b2a", outline=palette["primary"], width=2)
        
        for d in range(4):
            dx = bx - block_w/2 + 10
            dy = by - block_h/2 + 15 + d*12
            canvas.create_line(dx, dy, bx + block_w/2 - 10, dy, fill=palette["secondary"], width=2)
            
        if i == num_blocks - 1:
            nonce = hex(int(phase*1000 % 65535))[2:].zfill(4)
            canvas.create_text(bx, by + block_h/2 + 15, text=f"Nonce:{nonce}", fill=palette["danger"], font=("Consolas", 8))
            if math.sin(phase*5) > 0.8:
                canvas.create_rectangle(bx - block_w/2, by - block_h/2, bx + block_w/2, by + block_h/2, outline=palette["accent"], width=4)

@register_animation("network_flow")
def draw_network_flow(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    nodes = [
        (width*0.1, height*0.5),
        (width*0.3, height*0.2),
        (width*0.3, height*0.8),
        (width*0.7, height*0.3),
        (width*0.7, height*0.7),
        (width*0.9, height*0.5)
    ]
    
    edges = [
        (0, 1, 15), (0, 2, 10),
        (1, 2, 5), (1, 3, 12), (1, 4, 4),
        (2, 4, 14),
        (3, 5, 10), (4, 3, 7), (4, 5, 15)
    ]
    
    for u, v, cap in edges:
        ux, uy = nodes[u]
        vx, vy = nodes[v]
        
        canvas.create_line(ux, uy, vx, vy, fill=palette["grid"], width=cap)
        
        active_flow = cap * (0.5 + 0.5*math.sin(phase + u + v))
        flow_w = max(1, active_flow)
        color = palette["primary"] if active_flow < cap*0.8 else palette["danger"]
        
        num_particles = int((math.hypot(vx-ux, vy-uy) / 20))
        for p in range(num_particles):
            t = (phase * 1.5 + p / num_particles) % 1.0
            px = ux + (vx - ux) * t
            py = uy + (vy - uy) * t
            canvas.create_oval(px - flow_w/2, py - flow_w/2, px + flow_w/2, py + flow_w/2, fill=color, outline="")

    labels = ["S", "A", "B", "C", "D", "T"]
    for i, (nx, ny) in enumerate(nodes):
        canvas.create_oval(nx-15, ny-15, nx+15, ny+15, fill="#121e2b", outline=palette["accent"], width=2)
        canvas.create_text(nx, ny, text=labels[i], fill=palette["text"], font=("Segoe UI", 10, "bold"))

@register_animation("algorithm_viz")
def draw_algorithm_viz(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.08 * flow_factor
    
    num_elements = 20
    arr_w = width * 0.8
    bar_w = arr_w / num_elements
    start_x = width * 0.1
    start_y = height * 0.7
    
    for i in range(num_elements):
        x = start_x + i * bar_w
        
        for ghost in range(3):
            h = 20 + abs(math.sin(phase + i*0.2 + ghost)*80)
            color = palette["secondary"] if ghost == 0 else palette["grid"]
            dash = None if ghost == 0 else (2, 2)
            canvas.create_rectangle(x + 2, start_y - h, x + bar_w - 2, start_y, outline=color, dash=dash)
            
        if i == int(phase*5) % num_elements:
            h = 20 + abs(math.sin(phase + i*0.2)*80)
            canvas.create_rectangle(x + 2, start_y - h, x + bar_w - 2, start_y, fill=palette["danger"], outline="")
            
    cx, cy = width * 0.5, height * 0.2
    canvas.create_oval(cx-10, cy-10, cx+10, cy+10, outline=palette["primary"], width=2)
    canvas.create_line(cx, cy+10, cx-40, cy+40, fill=palette["primary"])
    canvas.create_line(cx, cy+10, cx+40, cy+40, fill=palette["primary"])
    canvas.create_oval(cx-50, cy+40, cx-30, cy+60, outline=palette["primary"], width=2)
    canvas.create_oval(cx+30, cy+40, cx+50, cy+60, outline=palette["primary"], width=2)
    
    focus_x = start_x + ((phase*2) % 1.0) * arr_w
    canvas.create_polygon(focus_x - 30, start_y + 30, focus_x + 30, start_y + 30, focus_x, start_y, fill=palette["accent"], stipple="gray25", outline="")

# ==========================================
# ELECTRICAL ENGINEERING SYSTEMS
# ==========================================

@register_animation("power_flow")
def draw_power_flow(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    buses = [
        (width*0.2, height*0.3, "G1"),
        (width*0.5, height*0.2, "B1"),
        (width*0.8, height*0.3, "L1"),
        (width*0.5, height*0.7, "B2"),
        (width*0.8, height*0.8, "L2")
    ]
    lines = [(0, 1), (1, 2), (1, 3), (3, 4), (0, 3)]
    
    for u, v in lines:
        ux, uy, _ = buses[u]
        vx, vy, _ = buses[v]
        
        target_cx = (ux + vx) / 2
        target_cy = (uy + vy) / 2
        
        dist = math.hypot(vx-ux, vy-uy)
        pts = []
        steps = int(dist/5)
        for i in range(steps):
            t = i / steps
            px = ux + (vx - ux) * t
            py = uy + (vy - uy) * t
            
            nx = -(vy - uy) / dist
            ny = (vx - ux) / dist
            
            wave = math.sin(phase*3 + i*0.4) * 10
            pts.extend([px + nx*wave, py + ny*wave])
            
        canvas.create_line(ux, uy, vx, vy, fill=palette["grid"], width=3)
        if len(pts) >= 4:
            canvas.create_line(*pts, fill=palette["primary"], width=1, smooth=True)
        
        if (tick//10) % len(lines) == lines.index((u,v)):
            canvas.create_oval(target_cx-8, target_cy-8, target_cx+8, target_cy+8, fill=palette["danger"], outline="")

    for nx, ny, label in buses:
        canvas.create_rectangle(nx-20, ny-5, nx+20, ny+5, fill="#121e2b", outline=palette["secondary"], width=2)
        if "G" in label:
            canvas.create_oval(nx-15, ny-35, nx+15, ny-5, fill="#0d1b2a", outline=palette["accent"], width=2)
            canvas.create_text(nx, ny-20, text="~", fill=palette["accent"], font=("Consolas", 14))
        elif "L" in label:
            canvas.create_polygon(nx, ny+5, nx-15, ny+30, nx+15, ny+30, fill="#1a2b3d", outline=palette["danger"])
        
        canvas.create_text(nx, ny-15, text=label, fill=palette["text"], font=("Segoe UI", 8))

    vmin, vmax = width*0.1, width*0.9
    canvas.create_line(vmin, height*0.9, vmax, height*0.9, fill=palette["grid"])
    profile_len = vmin + (vmax-vmin)*(0.8 + 0.2*math.sin(phase))
    canvas.create_line(vmin, height*0.9, profile_len, height*0.9, fill=palette["accent"], width=4)
    canvas.create_text(vmin, height*0.9 - 10, text="System Voltage Stability", fill=palette["text"], anchor="nw", font=("Segoe UI", 8))

@register_animation("circuit_simulator")
def draw_circuit_simulator(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    path = [
        (width*0.2, height*0.7),
        (width*0.2, height*0.3),
        (width*0.5, height*0.3),
        (width*0.8, height*0.3),
        (width*0.8, height*0.7),
        (width*0.5, height*0.7)
    ]
    
    for i in range(len(path)):
        p1 = path[i]
        p2 = path[(i+1)%len(path)]
        
        if i == 0:
            mid_y = (p1[1] + p2[1])/2
            canvas.create_line(p1[0], p1[1], p1[0], mid_y+10, fill=palette["primary"], width=2)
            canvas.create_line(p1[0], mid_y-10, p1[0], p2[1], fill=palette["primary"], width=2)
            canvas.create_oval(p1[0]-15, mid_y-15, p1[0]+15, mid_y+15, fill="#0d1b2a", outline=palette["accent"], width=2)
            canvas.create_text(p1[0], mid_y, text="+ -", fill=palette["accent"], font=("Consolas", 10))
        elif i == 2:
            pts = [p1[0], p1[1]]
            for zig in range(8):
                zx = p1[0] + (p2[0]-p1[0])*(zig/8.0) + 5
                zy = p1[1] + (10 if zig%2==0 else -10)
                pts.extend([zx, zy])
            pts.extend([p2[0], p2[1]])
            canvas.create_line(*pts, fill=palette["danger"], width=2)
        elif i == 4:
            mid_y = (p1[1] + p2[1])/2
            canvas.create_line(p1[0], p1[1], p1[0], mid_y-5, fill=palette["primary"], width=2)
            canvas.create_line(p1[0]-15, mid_y-5, p1[0]+15, mid_y-5, fill=palette["primary"], width=2)
            canvas.create_line(p1[0]-15, mid_y+5, p1[0]+15, mid_y+5, fill=palette["primary"], width=2)
            canvas.create_line(p1[0], mid_y+5, p1[0], p2[1], fill=palette["primary"], width=2)
        else:
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=palette["primary"], width=2)
            
    matrix_x, matrix_y = width * 0.5, height * 0.5
    for r in range(3):
        for c in range(3):
            val = abs(math.sin(phase + r*3 + c))
            color = palette["secondary"] if val > 0.5 else palette["grid"]
            canvas.create_rectangle(matrix_x - 30 + c*20, matrix_y - 30 + r*20, matrix_x - 10 + c*20, matrix_y - 10 + r*20, fill=color, outline="")
    canvas.create_text(matrix_x, matrix_y + 40, text="Ax = b (HHL)", fill=palette["text"], font=("Consolas", 10))
    
    e_path = width * 1.6 + height * 0.8
    current = (phase * 150) % e_path
    
    ex, ey = 0, 0
    if current < height*0.4: ex, ey = width*0.2, height*0.7 - current
    elif current < height*0.4 + width*0.6: ex, ey = width*0.2 + (current - height*0.4), height*0.3
    elif current < height*0.8 + width*0.6: ex, ey = width*0.8, height*0.3 + (current - height*0.4 - width*0.6)
    else: ex, ey = width*0.8 - (current - height*0.8 - width*0.6), height*0.7
    
    canvas.create_oval(ex-5, ey-5, ex+5, ey+5, fill=palette["accent"], outline="")

@register_animation("antenna_pattern")
def draw_antenna_pattern(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.8
    
    num_elements = 5
    spacing = 30
    start_x = cx - (num_elements-1)*spacing/2
    
    steer_angle = math.sin(phase * 0.5) * math.pi/4
    
    for i in range(num_elements):
        ex = start_x + i * spacing
        canvas.create_rectangle(ex-5, cy-10, ex+5, cy+10, fill="#121e2b", outline=palette["primary"])
        
        element_phase = i * spacing * math.sin(steer_angle) * 0.2
        for r in range(1, 6):
            radius = (phase*20 + r*20 + element_phase*20) % 150
            if radius > 10:
                opacity = max(0, 1.0 - radius/150.0)
                canvas.create_arc(ex - radius, cy - radius, ex + radius, cy + radius, start=0, extent=180, style=tk.ARC, outline=palette["grid"], width=1)
                
    lobe_pts = []
    for angle_deg in range(-90, 91, 2):
        rad = math.radians(angle_deg)
        val = 0
        for i in range(num_elements):
            p_shift = i * math.pi * (math.sin(rad) - math.sin(steer_angle))
            val += math.cos(p_shift)
        val = abs(val) / num_elements
        
        gain = val * 180
        px = cx + math.sin(rad) * gain
        py = cy - math.cos(rad) * gain
        lobe_pts.extend([px, py])
        
    lobe_pts.extend([cx, cy])
    if len(lobe_pts) >= 4:
        canvas.create_polygon(*lobe_pts, fill="", outline=palette["danger"], width=2, smooth=True)
        
    beam_x = cx + math.sin(steer_angle) * 200
    beam_y = cy - math.cos(steer_angle) * 200
    canvas.create_line(cx, cy, beam_x, beam_y, fill=palette["accent"], dash=(4, 4))
    
@register_animation("motor_drive")
def draw_motor_drive(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.1 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    r_outer = height * 0.35
    r_inner = height * 0.25
    canvas.create_oval(cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer, fill="#0a1520", outline=palette["secondary"], width=3)
    canvas.create_oval(cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner, fill="#121e2b", outline=palette["primary"], width=2)
    
    for i in range(6):
        angle = i * math.pi / 3
        cx_coil = cx + math.cos(angle) * (r_inner + 15)
        cy_coil = cy + math.sin(angle) * (r_inner + 15)
        
        phase_idx = i % 3
        p_val = math.sin(phase + phase_idx*2*math.pi/3)
        coil_color = palette["danger"] if p_val > 0.5 else palette["accent"] if p_val < -0.5 else palette["grid"]
        
        canvas.create_oval(cx_coil-10, cy_coil-10, cx_coil+10, cy_coil+10, fill=coil_color, outline="")
        
    rot_angle = phase * 2.0
    r_rotor = height * 0.22
    canvas.create_oval(cx - r_rotor, cy - r_rotor, cx + r_rotor, cy + r_rotor, fill="#1a2b3d", outline=palette["primary"])
    
    for i in range(12):
        bar_angle = rot_angle + i * math.pi / 6
        x1 = cx + math.cos(bar_angle)*r_rotor*0.5
        y1 = cy + math.sin(bar_angle)*r_rotor*0.5
        x2 = cx + math.cos(bar_angle)*r_rotor*0.9
        y2 = cy + math.sin(bar_angle)*r_rotor*0.9
        canvas.create_line(x1, y1, x2, y2, fill=palette["secondary"], width=3)
        
    fx = cx + math.cos(phase)*r_rotor*0.8
    fy = cy + math.sin(phase)*r_rotor*0.8
    canvas.create_line(cx, cy, fx, fy, fill=palette["danger"], width=4, arrow=tk.LAST)

@register_animation("vlsi_placement")
def draw_vlsi_placement(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    die_w, die_h = width * 0.6, height * 0.7
    cx, cy = width * 0.5, height * 0.5
    canvas.create_rectangle(cx - die_w/2, cy - die_h/2, cx + die_w/2, cy + die_h/2, fill="#0a121a", outline=palette["grid"], width=2)
    
    for x in range(int(cx - die_w/2), int(cx + die_w/2), 20):
        canvas.create_line(x, cy - die_h/2, x, cy + die_h/2, fill="#112233")
    for y in range(int(cy - die_h/2), int(cy + die_h/2), 20):
        canvas.create_line(cx - die_w/2, y, cx + die_w/2, y, fill="#112233")
        
    num_cells = 15
    cells = []
    for i in range(num_cells):
        tx = cx + math.cos(i*12.4)*die_w*0.3
        ty = cy + math.sin(i*7.1)*die_h*0.3
        
        ix = cx + math.cos(i)*die_w*0.4
        iy = cy + math.sin(i*3.1)*die_h*0.4
        
        opt_level = 0.5 + 0.5*math.sin(phase*0.5) 
        curr_x = ix + (tx - ix) * opt_level
        curr_y = iy + (ty - iy) * opt_level
        cells.append((curr_x, curr_y))
        
        canvas.create_rectangle(curr_x-8, curr_y-8, curr_x+8, curr_y+8, fill="#1a2b3d", outline=palette["primary"], width=2)
        
    for i in range(num_cells - 1):
        if i % 3 != 0:
            c1, c2 = cells[i], cells[i+1]
            canvas.create_line(c1[0], c1[1], c2[0], c1[1], fill=palette["secondary"], width=1)
            canvas.create_line(c2[0], c1[1], c2[0], c2[1], fill=palette["secondary"], width=1)
            
    wirelength = sum(abs(cells[i][0]-cells[i+1][0]) + abs(cells[i][1]-cells[i+1][1]) for i in range(num_cells-1))
    canvas.create_text(cx, cy + die_h/2 + 20, text=f"Total Wirelength: {int(wirelength)}", fill=palette["accent"], font=("Consolas", 10))


# ==========================================
# MECHANICAL ENGINEERING SYSTEMS
# ==========================================

@register_animation("cfd_solver")
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


@register_animation("fea_solver")
def draw_fea_solver(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Cantilever bracket simulation
    start_x, start_y = width * 0.2, height * 0.8
    bracket_len = width * 0.5
    bracket_h = height * 0.15
    
    # Deformation driven by phase
    load = math.sin(phase) * 60
    
    canvas.create_line(start_x-10, start_y+30, start_x-10, start_y-bracket_h-30, fill=palette["grid"], width=4) # Wall
    
    # Mesh elements
    num_x, num_y = 10, 3
    dx, dy = bracket_len / num_x, bracket_h / num_y
    
    for i in range(num_x):
        for j in range(num_y):
            # calculate node positions with deflection
            x0 = start_x + i*dx
            y0 = start_y - j*dy
            x1 = x0 + dx
            y1 = y0
            x2 = x0 + dx
            y2 = y0 - dy
            x3 = x0
            y3 = y0 - dy
            
            # Simple beam deflection equation y = (W*x^3)/(3EI) roughly quadratic/cubic
            def deflect(px):
                t = (px - start_x) / bracket_len
                return load * (t**2) * (3 - t) / 2
                
            pts = [
                x0, y0 + deflect(x0),
                x1, y1 + deflect(x1),
                x2, y2 + deflect(x2),
                x3, y3 + deflect(x3)
            ]
            
            # Stress color (higher stress near wall and top/bottom edges)
            stress = abs(load) * (1.0 - (i/num_x)*0.8) * (abs(j - num_y/2) / (num_y/2))
            fill_col = palette["danger"] if stress > 40 else palette["accent"] if stress > 15 else "#121e2b"
            
            canvas.create_polygon(*pts, fill=fill_col, outline=palette["primary"], width=1)
            
    # Load arrow
    tip_x = start_x + bracket_len
    tip_y = start_y - bracket_h/2 + deflect(tip_x)
    canvas.create_line(tip_x, tip_y - 40 * (1 if load > 0 else -1), tip_x, tip_y, fill=palette["danger"], width=4, arrow=tk.LAST)

@register_animation("robot_kinematics")
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


@register_animation("heat_engine")
def draw_heat_engine(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.08 * flow_factor
    
    # Piston Cylinder
    cyl_x, cyl_y = width * 0.25, height * 0.5
    cyl_w, cyl_h = 80, 150
    canvas.create_rectangle(cyl_x - cyl_w/2, cyl_y - cyl_h/2, cyl_x + cyl_w/2, cyl_y + cyl_h/2, outline=palette["primary"], width=3)
    
    # Stroke
    piston_y = cyl_y + math.sin(phase) * (cyl_h/2 - 20)
    canvas.create_rectangle(cyl_x - cyl_w/2 + 2, piston_y, cyl_x + cyl_w/2 - 2, piston_y + 20, fill="#121e2b", outline=palette["secondary"], width=2)
    canvas.create_line(cyl_x, piston_y + 20, cyl_x, cyl_y + cyl_h/2 + 50, fill=palette["secondary"], width=4) # rod
    
    # Gas particles changing color based on compression (temperature)
    vol = piston_y - (cyl_y - cyl_h/2)
    temp_norm = 1.0 - (vol / cyl_h) # higher temp when compressed
    gas_col = palette["danger"] if temp_norm > 0.6 else palette["accent"] if temp_norm > 0.3 else palette["primary"]
    
    for i in range(20):
        gx = cyl_x - cyl_w/2 + 10 + (i*17 + tick*5) % (cyl_w - 20)
        gy = cyl_y - cyl_h/2 + 10 + (i*23 + tick*2) % max(10, vol - 20)
        canvas.create_oval(gx-3, gy-3, gx+3, gy+3, fill=gas_col, outline="")

    # PV Diagram
    pv_x, pv_y = width * 0.7, height * 0.6
    pv_size = 100
    canvas.create_line(pv_x - pv_size, pv_y + pv_size, pv_x + pv_size, pv_y + pv_size, fill=palette["grid"]) # V axis
    canvas.create_line(pv_x - pv_size, pv_y + pv_size, pv_x - pv_size, pv_y - pv_size, fill=palette["grid"]) # P axis
    
    pv_pts = []
    for t in range(0, 50):
        p = t * math.pi * 2 / 50
        v = pv_x + math.cos(p) * 60
        # P ~ 1/V roughly, with offset
        pres = pv_y - (60 / (1.5 + math.cos(p))) * 40
        pv_pts.extend([v, pres])
    canvas.create_polygon(*pv_pts, fill="", outline=palette["accent"], width=2, smooth=True)
    
    # Current state
    curr_v = pv_x - math.sin(phase) * 60
    curr_p = pv_y - (60 / (1.5 - math.sin(phase))) * 40
    canvas.create_oval(curr_v-5, curr_p-5, curr_v+5, curr_p+5, fill=palette["danger"], outline="")

@register_animation("vibration_analysis")
def draw_vibration_analysis(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.1 * flow_factor
    
    # Beam modes
    for mode in range(1, 4):
        base_y = height * (0.2 + mode*0.2)
        canvas.create_line(width*0.1, base_y-20, width*0.1, base_y+20, fill=palette["grid"], width=4)
        
        pts = []
        for x in range(int(width*0.1), int(width*0.8), 5):
            t = (x - width*0.1) / (width*0.7)
            # Cantilever mode shapes approx
            freq = phase * mode * 2
            amp = math.sin(freq) * 30 * (1 - math.cos(t * math.pi/2 * (2*mode-1)))
            pts.extend([x, base_y + amp])
            
        color = palette["danger"] if mode == 1 else palette["accent"] if mode == 2 else palette["primary"]
        canvas.create_line(*pts, fill=color, width=3, smooth=True)
        
    # Spectrum chart
    chart_y = height * 0.9
    canvas.create_line(width*0.1, chart_y, width*0.9, chart_y, fill=palette["grid"])
    # Plot peaks identifying natural frequencies
    for i, mode in enumerate([1, 2, 3]):
        px = width*0.1 + mode * (width*0.2)
        ph = 40 if mode == 1 else 25 if mode == 2 else 15
        ph += math.sin(phase*10 + mode)*3
        color = palette["danger"] if mode == 1 else palette["accent"] if mode == 2 else palette["primary"]
        canvas.create_rectangle(px-10, chart_y, px+10, chart_y-ph, fill="#0d1b2a", outline=color, width=2)
        canvas.create_text(px, chart_y+10, text=f"w{mode}", fill=palette["muted"], font=("Consolas", 8))

@register_animation("turbomachinery")
def draw_turbomachinery(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.1 * flow_factor
    cx, cy = width * 0.3, height * 0.5
    r_hub, r_tip = height * 0.1, height * 0.35
    
    canvas.create_oval(cx - r_tip, cy - r_tip, cx + r_tip, cy + r_tip, outline=palette["grid"], width=2, dash=(4,4))
    
    num_blades = 12
    for i in range(num_blades):
        angle = phase + i * (2*math.pi / num_blades)
        x_in = cx + math.cos(angle)*r_hub
        y_in = cy + math.sin(angle)*r_hub
        # Blade twist curve
        ctrl_x = cx + math.cos(angle + 0.3)*r_tip*0.6
        ctrl_y = cy + math.sin(angle + 0.3)*r_tip*0.6
        x_out = cx + math.cos(angle + 0.1)*r_tip
        y_out = cy + math.sin(angle + 0.1)*r_tip
        
        canvas.create_line(x_in, y_in, ctrl_x, ctrl_y, fill=palette["primary"], width=6, smooth=True)
        canvas.create_line(ctrl_x, ctrl_y, x_out, y_out, fill=palette["primary"], width=3, smooth=True)
        
    canvas.create_oval(cx - r_hub, cy - r_hub, cx + r_hub, cy + r_hub, fill="#121e2b", outline=palette["secondary"], width=2)
    
    # Velocity triangles / Streamlines (Right side showing unwrapped cascade)
    cx_casc, cy_casc = width * 0.75, height * 0.5
    for i in range(5):
        y_c = cy_casc - 80 + i*40
        canvas.create_arc(cx_casc-30, y_c-20, cx_casc+30, y_c+20, start=30, extent=120, style=tk.ARC, outline=palette["secondary"], width=4)
        
        # flow vector
        fy = y_c - (phase*80 % 40)
        canvas.create_line(cx_casc - 50, fy, cx_casc, fy, fill=palette["danger"], width=2, arrow=tk.LAST)
        canvas.create_line(cx_casc + 10, fy+10, cx_casc + 60, fy-20, fill=palette["accent"], width=2, arrow=tk.LAST)

@register_animation("combined_cycle")
def draw_combined_cycle(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Gas Turbine (Left)
    gt_x, gt_y = width*0.2, height*0.5
    canvas.create_polygon(gt_x-40, gt_y-20, gt_x+40, gt_y-40, gt_x+40, gt_y+40, gt_x-40, gt_y+20, fill="#121e2b", outline=palette["primary"], width=2)
    canvas.create_text(gt_x, gt_y, text="GT", fill=palette["text"])
    
    # Heat Recovery Steam Generator (Center)
    hr_x, hr_y = width*0.5, height*0.5
    canvas.create_rectangle(hr_x-30, hr_y-60, hr_x+30, hr_y+60, fill="#0a1520", outline=palette["danger"], width=2)
    for i in range(5):
        y = hr_y - 40 + i*20
        canvas.create_line(hr_x-20, y, hr_x+20, y, fill=palette["danger"], width=3)
    canvas.create_text(hr_x, hr_y+75, text="HRSG", fill=palette["text"])
    
    # Steam Turbine (Right)
    st_x, st_y = width*0.8, height*0.5
    canvas.create_polygon(st_x-30, st_y-40, st_x+30, st_y-20, st_x+30, st_y+20, st_x-30, st_y+40, fill="#121e2b", outline=palette["secondary"], width=2)
    canvas.create_text(st_x, st_y, text="ST", fill=palette["text"])
    
    # Connectors with flows
    # GT exhaust to HRSG (Hot)
    for i in range(3):
        p = (phase*1.5 + i/3.0) % 1.0
        x = gt_x + 40 + p*(hr_x - 30 - gt_x - 40)
        canvas.create_oval(x-3, gt_y-3 + math.sin(phase*5+i)*5, x+3, gt_y+3 + math.sin(phase*5+i)*5, fill=palette["danger"], outline="")
        
    # HRSG Steam to ST (High Pressure)
    for i in range(3):
        p = (phase*1.5 + i/3.0) % 1.0
        x = hr_x + 30 + p*(st_x - 30 - hr_x - 30)
        canvas.create_oval(x-3, st_y-20-3, x+3, st_y-20+3, fill=palette["primary"], outline="")
        
    # Condenser return (Cold)
    canvas.create_line(st_x, st_y+40, st_x, st_y+80, hr_x, st_y+80, hr_x, hr_y+60, fill=palette["grid"], width=2)
    for i in range(5):
        p = (phase*1.5 + i/5.0) % 1.0
        # simplified box path logic
        c_path = p * 300
        dx, dy = st_x, st_y+40
        if c_path < 40: dy += c_path
        elif c_path < 40 + (st_x-hr_x): dy += 40; dx -= (c_path-40)
        else: dx = hr_x; dy = st_y+80 - (c_path - 40 - (st_x-hr_x))
        if dy >= hr_y+60:
            canvas.create_oval(dx-3, dy-3, dx+3, dy+3, fill=palette["secondary"], outline="")

# ==========================================
# CHEMICAL ENGINEERING SYSTEMS
# ==========================================

@register_animation("process_flow")
def draw_process_flow(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # P&ID Diagram components
    t1_x, t1_y = width*0.2, height*0.4
    pump_x, pump_y = width*0.4, height*0.7
    hx_x, hx_y = width*0.6, height*0.4
    t2_x, t2_y = width*0.8, height*0.6
    
    # Piping
    canvas.create_line(t1_x, t1_y+40, t1_x, pump_y, pump_x-20, pump_y, fill=palette["grid"], width=4)
    canvas.create_line(pump_x+20, pump_y, hx_x, pump_y, hx_x, hx_y+30, fill=palette["grid"], width=4)
    canvas.create_line(hx_x, hx_y-30, hx_x, t1_y-20, t2_x, t1_y-20, t2_x, t2_y-40, fill=palette["grid"], width=4)
    
    # Fluid animation in pipes
    flow1 = (phase*50) % (pump_y - (t1_y+40) + pump_x-20 - t1_x)
    if flow1 < pump_y - (t1_y+40): fx, fy = t1_x, t1_y+40 + flow1
    else: fx, fy = t1_x + (flow1 - (pump_y - (t1_y+40))), pump_y
    canvas.create_oval(fx-4, fy-4, fx+4, fy+4, fill=palette["primary"], outline="")
    
    # Tank 1
    lvl1 = 20 + math.sin(phase)*10
    canvas.create_rectangle(t1_x-30, t1_y-40, t1_x+30, t1_y+40, fill="#121e2b", outline=palette["primary"], width=2)
    canvas.create_rectangle(t1_x-28, t1_y+38-lvl1, t1_x+28, t1_y+38, fill=palette["primary"], outline="")
    
    # Pump
    canvas.create_oval(pump_x-20, pump_y-20, pump_x+20, pump_y+20, fill="#1a2b3d", outline=palette["accent"], width=2)
    canvas.create_arc(pump_x-15, pump_y-15, pump_x+15, pump_y+15, start=phase*200%360, extent=90, fill=palette["accent"])
    
    # Heat Exchanger
    canvas.create_oval(hx_x-30, hx_y-30, hx_x+30, hx_y+30, fill="#121e2b", outline=palette["danger"], width=2)
    canvas.create_line(hx_x-20, hx_y-10, hx_x+20, hx_y+10, fill=palette["danger"], width=2)
    canvas.create_line(hx_x-20, hx_y+10, hx_x+20, hx_y-10, fill=palette["danger"], width=2)
    
    # Tank 2
    lvl2 = 30 - math.sin(phase)*10
    canvas.create_rectangle(t2_x-20, t2_y-40, t2_x+20, t2_y+40, fill="#121e2b", outline=palette["secondary"], width=2)
    canvas.create_rectangle(t2_x-18, t2_y+38-lvl2, t2_x+18, t2_y+38, fill=palette["secondary"], outline="")

@register_animation("reactor_design")
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


@register_animation("distillation")
def draw_distillation(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx = width * 0.4
    
    # Column
    col_w, col_h = 60, height * 0.8
    bot_y, top_y = height * 0.9, height * 0.1
    canvas.create_rectangle(cx - col_w/2, top_y, cx + col_w/2, bot_y, fill="#0a121a", outline=palette["secondary"], width=2)
    
    # Trays
    num_trays = 8
    spacing = col_h / (num_trays + 1)
    
    for i in range(num_trays):
        y = bot_y - (i+1)*spacing
        canvas.create_line(cx - col_w/2, y, cx + col_w/2 - 10, y, fill=palette["grid"], width=2)
        
        # Vapor rising (bubbles)
        bx = cx - 15 + (phase*50 + i*10) % 30
        by = y + 10 - (phase*30 + i*5) % 20
        canvas.create_oval(bx-2, by-2, bx+2, by+2, fill=palette["danger"], outline="")
        
        # Liquid falling
        lx = cx + col_w/2 - 5
        ly = y + (phase*40 + i*15) % spacing
        canvas.create_line(lx, ly, lx, ly+5, fill=palette["primary"], width=2)
        
    # QAOA Composition graph
    chart_x = cx + col_w/2 + 50
    canvas.create_line(chart_x, bot_y, chart_x, top_y, fill=palette["grid"])
    canvas.create_text(chart_x, top_y-15, text="Light Key %", fill=palette["text"], font=("Segoe UI", 8))
    
    comp_pts = []
    for i in range(num_trays+2):
        y = bot_y - i*spacing
        # S-curve for composition
        t = i / (num_trays+1)
        val = 1.0 / (1.0 + math.exp(-10*(t - 0.5)))
        # QAOA fluctuation
        val += math.sin(phase*2 + i)*0.05
        comp_pts.extend([chart_x + val*80, y])
    canvas.create_line(*comp_pts, fill=palette["accent"], width=3, smooth=True)

@register_animation("heat_exchanger")
def draw_heat_exchanger(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Shell
    shell_w, shell_h = width * 0.6, 120
    canvas.create_rectangle(cx - shell_w/2, cy - shell_h/2, cx + shell_w/2, cy + shell_h/2, fill="#0d1b2a", outline=palette["grid"], width=2)
    
    # Tubes (Counter-flow)
    num_tubes = 4
    tube_spacing = shell_h / (num_tubes + 1)
    
    for i in range(num_tubes):
        y = cy - shell_h/2 + (i+1)*tube_spacing
        
        # Tube visual
        canvas.create_line(cx - shell_w/2 - 20, y, cx + shell_w/2 + 20, y, fill="#121e2b", width=8)
        
        # Hot fluid inside tubes transferring heat to Cold fluid in shell
        # Draw gradient manually with dashes
        for x_step in range(0, int(shell_w), 10):
            tx = cx - shell_w/2 + x_step
            # Hot fluid cools down from Left to Right
            temp_ratio = 1.0 - (x_step / shell_w)
            color = palette["danger"] if temp_ratio > 0.6 else palette["accent"] if temp_ratio > 0.3 else palette["primary"]
            
            # flow animation
            if (x_step + tick*3) % 20 < 10:
                canvas.create_line(tx, y, tx+10, y, fill=color, width=4)
                
    # Shell side flow (Cold fluid heating up from Right to Left)
    for p in range(40):
        # Baffle simulation
        py = cy - shell_h/2 + 10 + (p*13 + phase*20) % (shell_h - 20)
        px = cx + shell_w/2 - 10 - (p*37 + phase*40) % (shell_w - 20)
        
        # Heating up Right to Left
        temp_ratio = 1.0 - ((px - (cx - shell_w/2)) / shell_w)
        color = palette["danger"] if temp_ratio > 0.7 else palette["secondary"] if temp_ratio > 0.4 else palette["primary"]
        
        canvas.create_oval(px-3, py-3, px+3, py+3, fill=color, outline="")
        
    # Baffles
    for b in range(1, 6):
        bx = cx - shell_w/2 + b * shell_w/6
        if b % 2 != 0:
            canvas.create_line(bx, cy - shell_h/2, bx, cy + shell_h/2 - 30, fill=palette["grid"], width=4)
        else:
            canvas.create_line(bx, cy - shell_h/2 + 30, bx, cy + shell_h/2, fill=palette["grid"], width=4)

@register_animation("adsorption")
def draw_adsorption(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.6
    
    # Substrate lattice
    rows, cols = 3, 10
    spacing = 40
    start_x = cx - (cols-1)*spacing/2
    
    active_sites = []
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * spacing
            y = cy + r * spacing
            canvas.create_oval(x-10, y-10, x+10, y+10, fill="#121e2b", outline=palette["grid"], width=2)
            if r == 0:
                active_sites.append((x, y - 10))
                
    # VQE Coverage optimization
    coverage_target = 0.5 + 0.4 * math.sin(phase*0.2)
    
    for i, (sx, sy) in enumerate(active_sites):
        # Determine if site is occupied based on coverage and phase
        is_occupied = (math.sin(i*13.7 + phase) + 1)/2 < coverage_target
        
        if is_occupied:
            canvas.create_oval(sx-6, sy-12, sx+6, sy, fill=palette["accent"], outline="")
            canvas.create_line(sx, sy, sx, sy+10, fill=palette["primary"], dash=(2, 2)) # Van der Waals
        else:
            # Molecule falling/hovering
            hx = sx + math.sin(phase*3 + i)*15
            hy = sy - 40 + math.cos(phase*2 + i)*10
            canvas.create_oval(hx-6, hy-6, hx+6, hy+6, fill=palette["danger"], outline="")
            
    # Coverage metric
    canvas.create_text(cx, cy + rows*spacing + 20, text=f"Surface Coverage (theta): {int(coverage_target*100)}%", fill=palette["text"], font=("Consolas", 12))

@register_animation("polymerization")
def draw_polymerization(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    chain_len = 15
    base_r = 12
    
    # Main growing chain
    pts = []
    for i in range(chain_len):
        # Chain wiggle mechanics
        angle = math.sin(phase*0.5 + i*0.3) * 0.5
        x = cx - 150 + i * 25 * math.cos(angle)
        y = cy + math.sin(phase + i*0.5)*15 + i * 25 * math.sin(angle)
        pts.append((x, y))
        
    # Draw bonds
    for i in range(len(pts)-1):
        canvas.create_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], fill=palette["grid"], width=4)
        
    # Draw monomers in main chain
    for i, (x, y) in enumerate(pts):
        color = palette["primary"] if i % 2 == 0 else palette["secondary"]
        # Active growth center at the end
        if i == chain_len - 1:
            color = palette["danger"]
            r = base_r + math.sin(phase*5)*3
        else:
            r = base_r
        canvas.create_oval(x-r, y-r, x+r, y+r, fill="#0d1b2a", outline=color, width=2)
        
    # Free floating monomers
    for i in range(8):
        fx = cx + 50 + math.sin(phase*1.2 + i)*80
        fy = cy - 60 + math.cos(phase*.8 + i)*60
        f_color = palette["primary"] if i % 2 == 0 else palette["secondary"]
        canvas.create_oval(fx-8, fy-8, fx+8, fy+8, fill="#121e2b", outline=f_color, width=2)
        
    # VQE energy level indicator
    energy = -100 + math.sin(phase)*20
    canvas.create_text(cx, height*0.2, text=f"System Energy: {int(energy)} kJ/mol", fill=palette["accent"], font=("Consolas", 10))


# ==========================================
# BIOMEDICAL ENGINEERING SYSTEMS
# ==========================================

@register_animation("medical_imaging")
def draw_medical_imaging(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.4, height * 0.5
    
    # MRI Bore
    bore_r = height * 0.4
    canvas.create_oval(cx - bore_r, cy - bore_r, cx + bore_r, cy + bore_r, fill="#0a121a", outline=palette["secondary"], width=4)
    canvas.create_oval(cx - bore_r + 20, cy - bore_r + 20, cx + bore_r - 20, cy + bore_r - 20, outline=palette["grid"], width=1)
    
    # Patient body cross-section (simplified)
    body_w, body_h = bore_r * 0.6, bore_r * 0.4
    canvas.create_oval(cx - body_w, cy - body_h, cx + body_w, cy + body_h, fill="#121e2b", outline=palette["primary"], width=2)
    canvas.create_oval(cx - body_w*0.3, cy - body_h*0.3, cx + body_w*0.3, cy + body_h*0.3, fill="#1a2b3d", outline="") # Organ
    
    # RF pulses / Magnetic field sweep
    scan_angle = phase * 2.0
    sx1 = cx + math.cos(scan_angle)*bore_r
    sy1 = cy + math.sin(scan_angle)*bore_r
    sx2 = cx + math.cos(scan_angle + math.pi)*bore_r
    sy2 = cy + math.sin(scan_angle + math.pi)*bore_r
    canvas.create_line(sx1, sy1, sx2, sy2, fill=palette["danger"], width=2, dash=(4, 4))
    
    # QFT K-Space reconstruction (Right side)
    kx, ky = width * 0.85, height * 0.3
    k_size = height * 0.2
    canvas.create_rectangle(kx - k_size, ky - k_size, kx + k_size, ky + k_size, fill="#0a121a", outline=palette["grid"])
    canvas.create_text(kx, ky - k_size - 10, text="k-Space (QFT)", fill=palette["text"], font=("Segoe UI", 8))
    
    # Reconstructing details
    for i in range(20):
        px = kx + math.sin(phase*13 + i*7)*k_size*0.8
        py = ky + math.cos(phase*11 + i*5)*k_size*0.8
        intensity = (math.sin(phase*3 + i) + 1.0)/2.0
        color = palette["accent"] if intensity > 0.8 else palette["primary"] if intensity > 0.4 else palette["secondary"]
        rad = 1 + intensity*2
        canvas.create_oval(px-rad, py-rad, px+rad, py+rad, fill=color, outline="")

@register_animation("biomechanics")
def draw_biomechanics(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Knee joint simulation
    femur_len, tibia_len = 120, 120
    
    angle = math.pi/2 + math.sin(phase)*math.pi/6 # flexing
    
    hip_x, hip_y = cx, cy - femur_len + 20
    knee_x, knee_y = cx, cy + 20
    ankle_x, ankle_y = knee_x + math.sin(angle)*tibia_len, knee_y + math.cos(angle)*tibia_len
    
    # Bones
    canvas.create_line(hip_x, hip_y, knee_x, knee_y, fill=palette["primary"], width=15, capstyle=tk.ROUND)
    canvas.create_line(knee_x, knee_y, ankle_x, ankle_y, fill=palette["primary"], width=12, capstyle=tk.ROUND)
    
    # Cartilage
    canvas.create_arc(knee_x-10, knee_y-10, knee_x+10, knee_y+10, start=180, extent=180, outline=palette["accent"], width=4)
    
    # Muscle/Tendon actuating (Quadriceps)
    muscle_x = cx - 15
    muscle_attach = knee_y - 15
    canvas.create_line(hip_x - 10, hip_y + 20, muscle_x, muscle_attach, fill=palette["danger"], width=4, dash=(4, 2))
    canvas.create_line(muscle_x, muscle_attach, knee_x + math.sin(angle)*20, knee_y + math.cos(angle)*20, fill="#f4a261", width=3) # Tendon
    
    # Stress Vectors at joint
    stress_mag = abs(math.sin(phase)) * 40
    color_stress = palette["danger"] if stress_mag > 25 else palette["secondary"]
    canvas.create_line(knee_x, knee_y, knee_x, knee_y - stress_mag, fill=color_stress, width=3, arrow=tk.LAST)
    canvas.create_text(knee_x + 30, knee_y - stress_mag/2, text=f"Load: {int(stress_mag*10)}N", fill=color_stress, font=("Consolas", 8))

@register_animation("pharmacokinetics")
def draw_pharmacokinetics(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # 3-Compartment Model
    c_y = height * 0.4
    c_gut = (width*0.2, c_y, "Absorption (GI)")
    c_plas = (width*0.5, c_y, "Central (Plasma)")
    c_tiss = (width*0.8, c_y, "Peripheral (Tissue)")
    
    # Draw compartments
    r = 40
    for cx, cy, label in [c_gut, c_plas, c_tiss]:
        canvas.create_rectangle(cx-r, cy-r, cx+r, cy+r, fill="#0a121a", outline=palette["primary"], width=2)
        canvas.create_text(cx, cy - r - 15, text=label, fill=palette["text"], font=("Segoe UI", 8))
        
    # Flow arrows
    canvas.create_line(c_gut[0]+r, c_y, c_plas[0]-r, c_y, fill=palette["secondary"], width=2, arrow=tk.LAST)
    canvas.create_line(c_plas[0]+r, c_y-10, c_tiss[0]-r, c_y-10, fill=palette["secondary"], width=2, arrow=tk.LAST)
    canvas.create_line(c_tiss[0]-r, c_y+10, c_plas[0]+r, c_y+10, fill=palette["secondary"], width=2, arrow=tk.LAST)
    
    # Elimination
    elim_y = c_y + r + 30
    canvas.create_line(c_plas[0], c_y+r, c_plas[0], elim_y, fill=palette["danger"], width=2, arrow=tk.LAST)
    canvas.create_text(c_plas[0], elim_y + 10, text="Clearance", fill=palette["danger"], font=("Segoe UI", 8))
    
    # Simulate concentration over time (pulse representing repeated dosing)
    dose_phase = (phase * 0.5) % 1.0
    # simple math models for visual
    gut_conc = math.exp(-dose_phase*5)
    plas_conc = 2 * (math.exp(-dose_phase*2) - math.exp(-dose_phase*5))
    tiss_conc = 1 * (math.exp(-dose_phase*0.5) - math.exp(-dose_phase*2))
    
    canvas.create_rectangle(c_gut[0]-r+2, c_y+r-2 - gut_conc*2*r, c_gut[0]+r-2, c_y+r-2, fill=palette["accent"], outline="")
    canvas.create_rectangle(c_plas[0]-r+2, c_y+r-2 - plas_conc*r, c_plas[0]+r-2, c_y+r-2, fill=palette["danger"], outline="")
    canvas.create_rectangle(c_tiss[0]-r+2, c_y+r-2 - tiss_conc*2*r, c_tiss[0]+r-2, c_y+r-2, fill=palette["primary"], outline="")
    
    # Graph below
    g_y = height * 0.85
    canvas.create_line(width*0.1, g_y, width*0.9, g_y, fill=palette["grid"])
    canvas.create_text(width*0.1, g_y-30, text="Plasma Conc.", fill=palette["text"], anchor="w", font=("Segoe UI", 8))
    
    pts = []
    for x in range(int(width*0.1), int(width*0.9), 5):
        t = (x - width*0.1) / (width*0.8)
        # multi-dose superposition visual
        t_eff = (t - phase*0.2) % 0.3
        val = 2 * (math.exp(-t_eff*10) - math.exp(-t_eff*20))
        pts.extend([x, g_y - val*40])
    canvas.create_line(*pts, fill=palette["danger"], width=2, smooth=True)

@register_animation("ekg_analyzer")
def draw_ekg_analyzer(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.1 * flow_factor
    cx, cy = width * 0.5, height * 0.4
    
    # EKG Grid
    for y in range(int(cy-60), int(cy+60), 20):
        canvas.create_line(width*0.1, y, width*0.9, y, fill="#1c2a38", width=1)
    for x in range(int(width*0.1), int(width*0.9), 20):
        canvas.create_line(x, cy-60, x, cy+60, fill="#1c2a38", width=1)
        
    # Standard PQRST math approximation
    pts = []
    for x in range(int(width*0.1), int(width*0.9), 2):
        t = (x - width*0.1 - phase*100) % 200
        val = 0
        if 20 < t < 40: val = math.sin((t-20)/20 * math.pi) * 10 # P
        elif 60 < t < 70: val = -math.sin((t-60)/10 * math.pi) * 15 # Q
        elif 70 < t < 80: val = math.sin((t-70)/10 * math.pi) * 60 # R
        elif 80 < t < 90: val = -math.sin((t-80)/10 * math.pi) * 20 # S
        elif 120 < t < 160: val = math.sin((t-120)/40 * math.pi) * 15 # T
        
        pts.extend([x, cy - val])
        
    canvas.create_line(*pts, fill=palette["primary"], width=2)
    
    # QFT Frequency extraction showing arrhythmia detection
    f_y = height * 0.8
    canvas.create_line(width*0.1, f_y, width*0.9, f_y, fill=palette["grid"])
    canvas.create_text(width*0.1, f_y-50, text="QFT Spectrogram", fill=palette["text"], anchor="w", font=("Segoe UI", 8))
    
    noise = math.sin(phase*3 + tick)*5
    for i in range(1, 10):
        fx = width*0.1 + i*30
        h = 40 if i == 2 else 15 if i == 5 else 5
        h += noise if i > 5 else 0
        color = palette["danger"] if i == 2 else palette["accent"]
        canvas.create_rectangle(fx-10, f_y, fx+10, f_y-h, fill="#0d1b2a", outline=color, width=2)

@register_animation("dna_aligner")
def draw_dna_aligner(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Helices
    num_bases = 15
    spacing = width * 0.8 / num_bases
    start_x = width * 0.1
    
    strand1_y, strand2_y = height * 0.3, height * 0.7
    
    bases = ["A", "T", "C", "G"]
    colors = {"A": palette["primary"], "T": palette["danger"], "C": palette["accent"], "G": palette["secondary"]}
    
    # Sequence 1 (Reference)
    seq1 = [bases[(i*7 + 3) % 4] for i in range(num_bases)]
    # Sequence 2 (Target) moving left/right to align
    offset = math.sin(phase*0.5) * 3 # sweeping 3 positions
    
    for i in range(num_bases):
        x = start_x + i * spacing
        
        # Strand 1
        b1 = seq1[i]
        canvas.create_rectangle(x-10, strand1_y-15, x+10, strand1_y+15, fill="#121e2b", outline=colors[b1], width=2)
        canvas.create_text(x, strand1_y, text=b1, fill=colors[b1], font=("Consolas", 10, "bold"))
        
        # Strand 2 (continuous sweep)
        x_shift = start_x + (i + offset) * spacing
        b2_idx = (i*7 + 3 + int(round(offset))) % 4
        # to simulate finding a match at center offset
        if abs(offset) < 0.2:
            match_val = {"A":"T", "T":"A", "C":"G", "G":"C"}[b1] 
            b2 = match_val
        else:
            b2 = bases[(i*11 + tick//10) % 4] # random looking when not aligned
            
        if width*0.1 <= x_shift <= width*0.9:
            canvas.create_rectangle(x_shift-10, strand2_y-15, x_shift+10, strand2_y+15, fill="#121e2b", outline=colors[b2], width=2)
            canvas.create_text(x_shift, strand2_y, text=b2, fill=colors[b2], font=("Consolas", 10, "bold"))
            
            # Match beams
            dist = abs(x - x_shift)
            if dist < spacing*0.5:
                # Grover's amplitude high
                is_match = (b1=="A" and b2=="T") or (b1=="T" and b2=="A") or (b1=="C" and b2=="G") or (b1=="G" and b2=="C")
                l_col = palette["accent"] if is_match else palette["muted"]
                canvas.create_line(x, strand1_y+15, x_shift, strand2_y-15, fill=l_col, dash=(2,2), width=2 if is_match else 1)

# ==========================================
# ENVIRONMENTAL ENGINEERING SYSTEMS
# ==========================================

@register_animation("wind_farm")
def draw_wind_farm(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Ground
    ground_y = height * 0.8
    canvas.create_line(0, ground_y, width, ground_y, fill=palette["primary"], width=3)
    
    turbines = [
        (width*0.2, ground_y, 0.8),  # x, y, size_scale
        (width*0.5, ground_y, 1.0),
        (width*0.8, ground_y, 0.6)
    ]
    
    # Wind particles
    for i in range(40):
        wx = (phase * 80 + i * 30) % width
        wy = ground_y - 30 - (i * 17) % (height * 0.5)
        
        # adjust velocity if behind turbine (wake effect)
        speed = 1.0
        for tx, ty, scale in turbines:
            if tx < wx < tx + 100 and ty - 120*scale < wy < ty:
                speed = 0.5 # slower in wake
                
        canvas.create_line(wx, wy, wx + 10*speed, wy, fill=palette["grid"], width=1)
        
    # Draw Turbines
    for i, (tx, ty, scale) in enumerate(turbines):
        # Mast
        mast_h = 100 * scale
        canvas.create_polygon(tx-4*scale, ty, tx+4*scale, ty, tx+2*scale, ty-mast_h, tx-2*scale, ty-mast_h, fill="#121e2b", outline=palette["secondary"])
        
        # Hub
        hub_y = ty - mast_h
        rot_speed = phase * 2.0 * (1.2 if i == 0 else 0.8 if i == 2 else 1.0) # QAOA optimization variations
        
        # Blades
        blade_len = 45 * scale
        for b in range(3):
            angle = rot_speed + b * (2*math.pi / 3)
            bx = tx + math.cos(angle)*blade_len
            by = hub_y + math.sin(angle)*blade_len
            canvas.create_line(tx, hub_y, bx, by, fill=palette["primary"], width=max(2, int(4*scale)))
            
        canvas.create_oval(tx-3, hub_y-3, tx+3, hub_y+3, fill=palette["accent"], outline="")
        
        # QAOA efficiency metric bubble
        eff = 95 - i*15 + math.sin(phase + i)*5
        canvas.create_text(tx, ty + 15, text=f"{int(eff)}%", fill=palette["accent"], font=("Consolas", 8))

@register_animation("atmospheric")
def draw_atmospheric(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Earth globe outline
    r_globe = height * 0.35
    canvas.create_oval(cx - r_globe, cy - r_globe, cx + r_globe, cy + r_globe, outline=palette["primary"], width=2)
    
    # Latitude bands
    for lat in [-45, -20, 0, 20, 45]:
        rad = math.radians(lat)
        y_off = math.sin(rad) * r_globe
        w_off = math.cos(rad) * r_globe
        canvas.create_oval(cx - w_off, cy - y_off - 10, cx + w_off, cy - y_off + 10, outline=palette["grid"], style=tk.ARC, start=180, extent=180)
        
    # Flow vectors (Jet streams)
    for band in range(3):
        y = cy - r_globe*0.5 + band*r_globe*0.4
        w_band = math.sqrt(r_globe**2 - (y-cy)**2)
        
        for i in range(12):
            t = (phase*0.2 + i/12.0) % 1.0
            if band % 2 == 1: t = 1.0 - t # opposing flows
            
            x = cx - w_band + t * 2 * w_band
            # Wrap around depth perception (simulating front of globe)
            if 0.1 < t < 0.9: 
                v = 15
                dir_m = 1 if band % 2 == 0 else -1
                canvas.create_line(x, y + math.sin(t*math.pi)*10, x + v*dir_m, y + math.sin((t+0.1)*math.pi)*10, fill=palette["secondary"], arrow=tk.LAST)
                
    # Pollutant dispersion plume
    source_x, source_y = cx - r_globe*0.6, cy + r_globe*0.2
    canvas.create_oval(source_x-4, source_y-4, source_x+4, source_y+4, fill=palette["danger"], outline="")
    
    for i in range(20):
        p_t = (phase + i*0.1) % 1.0
        px = source_x + p_t * r_globe * 0.8
        py = source_y - p_t * r_globe * 0.4 + math.sin(phase*3 + i)*p_t*30
        
        opacity = max(0, 1.0 - p_t)
        if opacity > 0.1:
            rad = 2 + p_t*10
            col = palette["danger"] if p_t < 0.3 else palette["accent"]
            canvas.create_oval(px-rad, py-rad, px+rad, py+rad, outline=col, dash=(2, 2))

@register_animation("river_quality")
def draw_river_quality(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # River path (Sine wave)
    river_pts = []
    for x in range(0, int(width), 10):
        y = height * 0.5 + math.sin(x*0.01)*50
        river_pts.extend([x, y])
        
    canvas.create_line(*river_pts, fill=palette["primary"], width=40, smooth=True, capstyle=tk.ROUND)
    canvas.create_line(*river_pts, fill="#0a121a", width=36, smooth=True, capstyle=tk.ROUND) # inner water
    
    canvas.create_text(width*0.1, height*0.2, text="Contaminant Transport", fill=palette["text"], font=("Segoe UI", 10, "bold"))
    
    # Industrial source
    source_x = width * 0.2
    source_y = height * 0.5 + math.sin(source_x*0.01)*50 - 25
    canvas.create_rectangle(source_x-15, source_y-20, source_x+15, source_y, fill="#121e2b", outline=palette["secondary"], width=2)
    canvas.create_line(source_x, source_y, source_x, source_y+20, fill=palette["danger"], width=3) # outfall
    
    # Pollutant concentration (HHL Solving PDE)
    for i in range(30):
        p_x = source_x + (phase*40 + i*15) % (width - source_x)
        p_y = height * 0.5 + math.sin(p_x*0.01)*50
        
        # Diffuse and decay
        dist = p_x - source_x
        spread = 5 + dist * 0.05
        decay = math.exp(-dist * 0.005)
        
        if decay > 0.1:
            y_offset = math.sin(phase*3 + i) * spread
            p_y += y_offset
            color = palette["danger"] if decay > 0.6 else palette["accent"] if decay > 0.3 else palette["secondary"]
            rad = max(1, 3 * decay)
            canvas.create_oval(p_x-rad, p_y-rad, p_x+rad, p_y+rad, fill=color, outline="")
            
@register_animation("groundwater_flow")
def draw_groundwater_flow(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    surface_y = height * 0.2
    canvas.create_line(0, surface_y, width, surface_y, fill=palette["accent"], width=2)
    
    # Pumping Well
    well_x = width * 0.5
    well_bottom = height * 0.8
    canvas.create_rectangle(well_x-5, surface_y-10, well_x+5, well_bottom, fill="#1a2b3d", outline=palette["secondary"])
    
    # Cone of depression / Water table
    table_pts = [0, height*0.4]
    for x in range(0, int(width), 20):
        dist = abs(x - well_x)
        # log shape approximation for drawdown
        drawdown = 80 * math.exp(-dist/100)
        table_pts.extend([x, height*0.4 + drawdown])
    table_pts.extend([width, height*0.4])
    canvas.create_line(*table_pts, fill=palette["primary"], width=3, smooth=True)
    
    # Darcy's Law flow vectors into well
    for r in range(4):
        y = height*0.5 + r*40
        for side in [-1, 1]:
            x_start = well_x + side * (100 + r*20)
            x_end = x_start - side * 40
            
            # pulsing flow
            p = (phase*2 + r) % 1.0
            vx = x_start + (x_end - x_start)*p
            canvas.create_line(vx, y, vx - side*10, y, fill=palette["primary"], arrow=tk.LAST)
            
@register_animation("carbon_cycle")
def draw_carbon_cycle(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Pools
    p_atm = (width*0.5, height*0.2, "Atmosphere")
    p_lan = (width*0.3, height*0.6, "Biosphere")
    p_ocn = (width*0.7, height*0.6, "Oceans")
    
    for x, y, label in [p_atm, p_lan, p_ocn]:
        canvas.create_oval(x-40, y-30, x+40, y+30, fill="#0a121a", outline=palette["primary"], width=2)
        canvas.create_text(x, y, text=label, fill=palette["text"])
        
    # Fluxes balancing (VQE solved)
    fluxes = [
        (p_lan, p_atm, palette["danger"]), # Respiration/Emissions
        (p_atm, p_lan, palette["accent"]), # Photosynthesis
        (p_ocn, p_atm, palette["danger"]), # Outgassing
        (p_atm, p_ocn, palette["secondary"]), # Dissolution
    ]
    
    for (src, dst, col) in fluxes:
        ux, uy = src[0], src[1]
        vx, vy = dst[0], dst[1]
        
        # Arced paths
        mx, my = (ux+vx)/2, (uy+vy)/2
        dx, dy = vx-ux, vy-uy
        dist = math.hypot(dx, dy)
        nx, ny = -dy/dist*30, dx/dist*30
        
        # Animate particles along arc
        pts = []
        for t_step in range(11):
            t = t_step / 10.0
            # Quadratic bezier
            px = (1-t)**2*ux + 2*(1-t)*t*(mx+nx) + t**2*vx
            py = (1-t)**2*uy + 2*(1-t)*t*(my+ny) + t**2*vy
            pts.extend([px, py])
            
        canvas.create_line(*pts, fill=palette["grid"], smooth=True, dash=(2,4))
        
        # Moving flux packet
        t_p = (phase*0.8 + fluxes.index((src,dst))*0.25) % 1.0
        packet_x = (1-t_p)**2*ux + 2*(1-t_p)*t_p*(mx+nx) + t_p**2*vx
        packet_y = (1-t_p)**2*uy + 2*(1-t_p)*t_p*(my+ny) + t_p**2*vy
        
        canvas.create_oval(packet_x-5, packet_y-5, packet_x+5, packet_y+5, fill=col, outline="")


# ==========================================
# MATERIALS SCIENCE SYSTEMS
# ==========================================

@register_animation("molecular_dynamics")
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


@register_animation("phase_diagram")
def draw_phase_diagram(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.4, height * 0.6
    
    # Axes
    canvas.create_line(cx-100, cy+80, cx+150, cy+80, fill=palette["primary"], arrow=tk.LAST) # T
    canvas.create_text(cx+160, cy+80, text="T", fill=palette["primary"])
    canvas.create_line(cx-100, cy+80, cx-100, cy-120, fill=palette["primary"], arrow=tk.LAST) # P
    canvas.create_text(cx-100, cy-130, text="P", fill=palette["primary"])
    
    # Phase Boundaries (Triple point approx)
    triple_x, triple_y = cx, cy
    
    # Solid-Gas (Sublimation)
    pts_sg = [cx-100, cy+60, triple_x, triple_y]
    canvas.create_line(*pts_sg, fill=palette["grid"], width=3)
    
    # Solid-Liquid (Melting) - slightly negative slope for water, positive for general
    pts_sl = [triple_x, triple_y, cx-20, cy-100]
    canvas.create_line(*pts_sl, fill=palette["grid"], width=3)
    
    # Liquid-Gas (Boiling)
    critical_x, critical_y = cx+100, cy-60
    pts_lg = []
    for x in range(int(triple_x), int(critical_x)):
        t = (x - triple_x) / (critical_x - triple_x)
        y = triple_y - (triple_y - critical_y) * (1 - (1-t)**2)
        pts_lg.extend([x, y])
    canvas.create_line(*pts_lg, fill=palette["grid"], width=3)
    
    # Critical point
    canvas.create_oval(critical_x-3, critical_y-3, critical_x+3, critical_y+3, outline=palette["danger"])
    
    # Regions
    canvas.create_text(cx-60, cy-30, text="Solid", fill=palette["text"])
    canvas.create_text(cx+20, cy-60, text="Liquid", fill=palette["text"])
    canvas.create_text(cx+60, cy+20, text="Gas", fill=palette["text"])
    
    # State path (Quantum walk exploring phase space)
    state_x = cx - 50 + math.sin(phase)*120
    state_y = cy + 20 - math.cos(phase*.7)*100
    
    canvas.create_line(cx-100, state_y, state_x, state_y, fill=palette["accent"], dash=(2, 4))
    canvas.create_line(state_x, cy+80, state_x, state_y, fill=palette["accent"], dash=(2, 4))
    canvas.create_oval(state_x-6, state_y-6, state_x+6, state_y+6, fill=palette["danger"], outline="")

@register_animation("crystallography")
def draw_crystallography(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.3, height * 0.5
    size = 60
    
    # Rotating 3D lattice
    nodes = [
        (-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1),
        (-1,-1,1),  (1,-1,1),  (1,1,1),  (-1,1,1),
        (0,0,0) # Body centered
    ]
    edges = [
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7)
    ]
    
    ax = phase * 0.7
    ay = phase * 0.4
    
    proj_nodes = []
    for x, y, z in nodes:
        # Rotate Y
        x1 = x * math.cos(ay) - z * math.sin(ay)
        z1 = z * math.cos(ay) + x * math.sin(ay)
        # Rotate X
        y2 = y * math.cos(ax) - z1 * math.sin(ax)
        z2 = z1 * math.cos(ax) + y * math.sin(ax)
        
        scale = size / (2.0 + z2*0.3)
        px = cx + x1 * scale * 2
        py = cy + y2 * scale * 2
        proj_nodes.append((px, py, z2))
        
    for u, v in edges:
        p1, p2 = proj_nodes[u], proj_nodes[v]
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=palette["grid"], width=2)
        
    # Draw nodes
    for i, (px, py, z2) in enumerate(proj_nodes):
        r = 6 - z2*1.5
        col = palette["danger"] if i == 8 else palette["primary"]
        canvas.create_oval(px-r, py-r, px+r, py+r, fill="#121e2b", outline=col, width=2)
        
    # Diffraction Pattern (Right side)
    dx, dy = width * 0.75, height * 0.5
    canvas.create_oval(dx-80, dy-80, dx+80, dy+80, outline=palette["grid"])
    canvas.create_oval(dx-40, dy-40, dx+40, dy+40, outline=palette["grid"])
    
    # QFT peak intensity
    for i in range(12):
        angle = i * (math.pi/6) + phase*0.1
        for dist in [40, 80]:
            px = dx + math.cos(angle)*dist
            py = dy + math.sin(angle)*dist
            intensity = math.sin(phase*3 + i*dist)*0.5 + 0.5
            rad = 2 + intensity*4
            col = palette["accent"] if intensity > 0.8 else palette["secondary"]
            canvas.create_oval(px-rad, py-rad, px+rad, py+rad, fill=col, outline="")

@register_animation("corrosion_predictor")
def draw_corrosion_predictor(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Metal surface
    surf_y = height * 0.6
    canvas.create_rectangle(width*0.1, surf_y, width*0.9, height, fill="#1c2a38", outline=palette["grid"], width=2)
    
    for i in range(15):
        bx = width*0.15 + i*width*0.05
        # Corrosive pitting depth
        pit = abs(math.sin(phase*0.2 + i*4.1)) * 30
        
        # Oxide layer
        canvas.create_rectangle(bx-10, surf_y + pit, bx+10, surf_y + pit - 15, fill="#1a2b3d", outline=palette["danger"])
        
        # Ions diffusing away
        for ion in range(3):
            ix = bx + math.sin(phase*2 + ion + i)*15
            iy = surf_y + pit - 20 - (phase*30 + ion*20 + i*13) % 80
            canvas.create_oval(ix-3, iy-3, ix+3, iy+3, fill=palette["secondary"], outline="")
            
    # Electrochemical cell voltage
    cx, cy = width * 0.8, height * 0.3
    canvas.create_oval(cx-25, cy-25, cx+25, cy+25, fill="#0a121a", outline=palette["primary"], width=2)
    volts = 0.44 + math.sin(phase*5)*0.02 # Iron standard potential approx
    canvas.create_text(cx, cy, text=f"{volts:.2f}V", fill=palette["primary"], font=("Consolas", 10))

@register_animation("composite_micromechanics")
def draw_composite_micromechanics(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Matrix body
    canvas.create_rectangle(width*0.2, height*0.2, width*0.8, height*0.8, fill="#0d1b2a", outline=palette["grid"])
    
    # Fibers (Cross section)
    fibers = [
        (width*0.35, height*0.35), (width*0.65, height*0.35),
        (width*0.5, height*0.5),
        (width*0.35, height*0.65), (width*0.65, height*0.65)
    ]
    
    fiber_r = height * 0.08
    
    for fx, fy in fibers:
        # Fiber
        canvas.create_oval(fx-fiber_r, fy-fiber_r, fx+fiber_r, fy+fiber_r, fill="#1a2b3d", outline=palette["secondary"], width=3)
        
        # Interfacial stress (HHL strain field)
        stress_r = fiber_r + 5 + math.sin(phase*3 + fx)*5
        canvas.create_oval(fx-stress_r, fy-stress_r, fx+stress_r, fy+stress_r, outline=palette["danger"], dash=(2, 4))
        
    # Stress flow lines wrapping around fibers
    for y_start in range(int(height*0.25), int(height*0.8), 20):
        pts = []
        for x in range(int(width*0.2), int(width*0.8), 10):
            y = y_start
            # deflect around nearest fiber
            min_d = float('inf')
            near_fy = y
            for fx, fy in fibers:
                d = math.hypot(x - fx, y - fy)
                if d < min_d:
                    min_d = d
                    near_fy = fy
                    
            if min_d < fiber_r * 2:
                deflect = (fiber_r * 2 - min_d) * (1 if y > near_fy else -1)
                y += deflect * 0.5
            
            # Global shear
            y += math.sin(phase + x*0.01)*5
            pts.extend([x, y])
            
        canvas.create_line(*pts, fill=palette["primary"], smooth=True, width=1)

@register_animation("heat_treatment")
def draw_heat_treatment(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Metal Piece
    piece_x, piece_y = width*0.3, height*0.5
    piece_w, piece_h = 100, 150
    
    # Temperature cycle (Heating -> Quenching -> Tempering)
    cycle = phase % (2 * math.pi)
    if cycle < math.pi * 0.4:
        temp = cycle / (math.pi * 0.4) # Heat
    elif cycle < math.pi * 0.6:
        temp = 1.0 - (cycle - math.pi * 0.4)/(math.pi*0.2) # Quench
    else:
        temp = 0.3 * (1 - (cycle - math.pi*0.6)/(math.pi*1.4)) # Temper
        
    # RGB color mapped from blue (cool) to red/yellow (hot)
    def rgb_to_hex(r, g, b): return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
    r_c = min(255, 50 + temp*400)
    g_c = min(255, 30 + temp*200)
    b_c = min(255, 50 + (1-temp)*150)
    piece_color = rgb_to_hex(r_c, g_c, b_c)
    
    canvas.create_rectangle(piece_x-piece_w/2, piece_y-piece_h/2, piece_x+piece_w/2, piece_y+piece_h/2, fill=piece_color, outline=palette["grid"], width=3)
    
    # Microstructure inset (VQE simulating grain growth/martensite formation)
    inset_x, inset_y = width*0.75, height*0.5
    inset_r = 70
    canvas.create_oval(inset_x-inset_r, inset_y-inset_r, inset_x+inset_r, inset_y+inset_r, fill="#0a121a", outline=palette["primary"], width=2)
    
    # Voronoi/Grain approximation using intersecting lines
    num_grains = int(10 + temp*30) # Grains grow with temp
    for i in range(15):
        ang = i * math.pi/7 + phase*0.1
        lx = inset_x + math.cos(ang)*inset_r
        ly = inset_y + math.sin(ang)*inset_r
        lx2 = inset_x - math.cos(ang + temp)*inset_r
        ly2 = inset_y - math.sin(ang + temp)*inset_r
        
        # Quench forms needle-like martensite (red lines)
        if cycle > math.pi*0.4 and cycle < math.pi*0.6:
            canvas.create_line(inset_x, inset_y, lx2, ly2, fill=palette["danger"], width=2)
        else:
            canvas.create_line(lx, ly, lx2, ly2, fill=palette["secondary"], width=1)
            
    # TTT Diagram (Time-Temperature-Transformation) tracking
    chart_y = height * 0.85
    canvas.create_line(piece_x - 60 + (cycle/(2*math.pi))*120, chart_y, piece_x - 60 + (cycle/(2*math.pi))*120, chart_y-40, fill=palette["accent"])
    canvas.create_text(piece_x, chart_y+15, text=f"T: {int(temp*1000)} C", fill=palette["text"], font=("Consolas", 10))

# ==========================================
# INDUSTRIAL ENGINEERING SYSTEMS
# ==========================================

@register_animation("job_shop")
def draw_job_shop(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Machines
    machines = [(width*0.2, height*0.3, "M1"), (width*0.5, height*0.3, "M2"), (width*0.8, height*0.3, "M3")]
    for mx, my, m_label in machines:
        canvas.create_rectangle(mx-30, my-30, mx+30, my+30, fill="#1a2b3d", outline=palette["primary"], width=2)
        canvas.create_text(mx, my, text=m_label, fill=palette["text"], font=("Segoe UI", 12, "bold"))
        
    # Jobs processing
    jobs = [
        {"color": palette["danger"], "path": [(0, 1), (1, 2)], "offset": 0},
        {"color": palette["secondary"], "path": [(1, 0), (0, 2)], "offset": 0.3},
        {"color": palette["accent"], "path": [(2, 1), (1, 0)], "offset": 0.6}
    ]
    
    for job in jobs:
        progress = (phase*0.5 + job["offset"]) % 2.0
        step = int(progress)
        sub_p = progress - step
        
        if step < len(job["path"]):
            m_start = job["path"][step][0]
            m_end = job["path"][step][1]
            sx, sy, _ = machines[m_start]
            ex, ey, _ = machines[m_end]
            
            # Wait at machine, then move
            if sub_p < 0.5:
                # Processing
                bx, by = sx, sy - 45
                canvas.create_oval(sx-10, sy+15, sx+10, sy+25, outline=job["color"]) # machine active ring
            else:
                # Moving
                t = (sub_p - 0.5) * 2.0
                bx = sx + (ex - sx)*t
                by = (sy - 45) + (ey - sy)*t - math.sin(t*math.pi)*30 # arc hop
                
            canvas.create_rectangle(bx-10, by-10, bx+10, by+10, fill=job["color"], outline="")
            
    # Gantt Chart (QAOA Schedule)
    g_y = height * 0.75
    canvas.create_line(width*0.1, g_y, width*0.1, g_y+60, fill=palette["grid"])
    canvas.create_line(width*0.1, g_y+60, width*0.9, g_y+60, fill=palette["grid"])
    
    for m in range(3):
        canvas.create_text(width*0.08, g_y + 10 + m*20, text=f"M{m+1}", fill=palette["text"])
        # Blocks
        for b in range(4):
            # Optimized scheduling block arrangements
            b_start = width*0.1 + (m*30 + b*50 + phase*10) % (width*0.7)
            b_w = 20 + math.sin(m+b)*10
            color = [palette["danger"], palette["secondary"], palette["accent"]][(m+b)%3]
            canvas.create_rectangle(b_start, g_y + 2 + m*20, b_start+b_w, g_y + 18 + m*20, fill=color, outline="")

@register_animation("supply_chain")
def draw_supply_chain(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    nodes = {
        "Supplier": (width*0.15, height*0.3),
        "Factory": (width*0.45, height*0.3),
        "Warehouse": (width*0.75, height*0.3),
        "Retail A": (width*0.65, height*0.7),
        "Retail B": (width*0.85, height*0.7)
    }
    
    links = [("Supplier", "Factory"), ("Factory", "Warehouse"), ("Warehouse", "Retail A"), ("Warehouse", "Retail B")]
    
    for u, v in links:
        ux, uy = nodes[u]
        vx, vy = nodes[v]
        canvas.create_line(ux, uy, vx, vy, fill=palette["grid"], width=3)
        
        # Trucks moving
        t = (phase*0.5 + links.index((u,v))*0.3) % 1.0
        tx = ux + (vx - ux)*t
        ty = uy + (vy - uy)*t
        
        canvas.create_rectangle(tx-10, ty-5, tx+10, ty+5, fill=palette["secondary"], outline=palette["primary"])
        
    for name, (x, y) in nodes.items():
        canvas.create_oval(x-20, y-20, x+20, y+20, fill="#121e2b", outline=palette["accent"], width=2)
        canvas.create_text(x, y-30, text=name, fill=palette["text"], font=("Segoe UI", 9))
        
        # Inventory levels
        inv_max = 30
        inv = 15 + math.sin(phase*2 + x)*12
        color = palette["danger"] if inv < 5 else palette["primary"]
        canvas.create_rectangle(x+25, y+20, x+30, y+20-inv_max, fill="#0a121a", outline=palette["grid"])
        canvas.create_rectangle(x+25, y+20, x+30, y+20-inv, fill=color, outline="")

@register_animation("assembly_line")
def draw_assembly_line(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cy = height * 0.6
    
    # Conveyor
    canvas.create_line(width*0.1, cy, width*0.9, cy, fill=palette["secondary"], width=6)
    for i in range(15):
        rx = width*0.1 + (phase*40 + i*50) % (width*0.8)
        canvas.create_oval(rx-4, cy+3, rx+4, cy+11, fill="#121e2b", outline=palette["primary"])
        
    # Stations
    px = width*0.1 + (phase*40) % (width*0.8) # Base product
    
    stations = [(width*0.3, "Weld", palette["danger"]), (width*0.5, "Part", palette["accent"]), (width*0.7, "Paint", palette["primary"])]
    
    for sx, name, col in stations:
        # Station frame
        canvas.create_rectangle(sx-25, cy-80, sx+25, cy-50, fill="#1a2b3d", outline=col, width=2)
        canvas.create_text(sx, cy-90, text=name, fill=palette["text"], font=("Consolas", 10))
        
        # Arm / Action
        if abs(px - sx) < 20: # Active
            canvas.create_line(sx, cy-50, px, cy-20, fill=col, width=4)
            canvas.create_oval(px-15, cy-35, px+15, cy-5, outline=col, width=2)
        else: # Idle
            canvas.create_line(sx, cy-50, sx, cy-30, fill=palette["grid"], width=3)
            
    # Draw product assembling
    if px > width*0.1: canvas.create_rectangle(px-15, cy-20, px+15, cy-5, fill="#121e2b", outline="#fff") # base
    if px > width*0.3: canvas.create_oval(px-5, cy-15, px+5, cy-5, fill=palette["danger"], outline="") # weld
    if px > width*0.5: canvas.create_rectangle(px-5, cy-30, px+5, cy-20, fill=palette["accent"], outline="") # part
    if px > width*0.7: canvas.create_rectangle(px-15, cy-20, px+15, cy-5, fill=palette["primary"], outline="") # painted

@register_animation("queuing_network")
def draw_queuing_network(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    servers = [(width*0.4, height*0.3), (width*0.4, height*0.7), (width*0.8, height*0.5)]
    
    for i, (sx, sy) in enumerate(servers):
        # Server box
        canvas.create_rectangle(sx-20, sy-30, sx+20, sy+30, fill="#1a2b3d", outline=palette["primary"], width=2)
        canvas.create_text(sx, sy, text=f"S{i+1}", fill=palette["text"])
        
        # Service indicator line
        canvas.create_arc(sx-10, sy-10, sx+10, sy+10, start=90, extent=-(phase*300 % 360), style=tk.ARC, outline=palette["accent"], width=3)
        
        # Queues (Waiting lines)
        queue_len = int(5 + math.sin(phase*0.5 + i*3)*4)
        for q in range(queue_len):
            qx = sx - 40 - q*20
            color = palette["danger"] if queue_len > 7 else palette["secondary"]
            canvas.create_oval(qx-6, sy-6, qx+6, sy+6, fill=color, outline="")
            
    # Routing
    canvas.create_line(width*0.4+20, height*0.3, width*0.8-40, height*0.5, fill=palette["grid"], width=2, arrow=tk.LAST)
    canvas.create_line(width*0.4+20, height*0.7, width*0.8-40, height*0.5, fill=palette["grid"], width=2, arrow=tk.LAST)
    
    # Entity traversing
    tx = width*0.4 + 20 + (phase*50) % (width*0.4 - 60)
    ty = height*0.3 + (height*0.2) * ((tx - (width*0.4+20)) / (width*0.4 - 60))
    canvas.create_oval(tx-5, ty-5, tx+5, ty+5, fill=palette["accent"], outline="")

@register_animation("statistical_control")
def draw_statistical_control(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Control Chart
    chart_y = height * 0.5
    chart_h = height * 0.6
    
    # Limits
    ucl = chart_y - chart_h/2 * 0.8
    lcl = chart_y + chart_h/2 * 0.8
    canvas.create_line(width*0.1, ucl, width*0.9, ucl, fill=palette["danger"], dash=(4, 4))
    canvas.create_line(width*0.1, lcl, width*0.9, lcl, fill=palette["danger"], dash=(4, 4))
    canvas.create_line(width*0.1, chart_y, width*0.9, chart_y, fill=palette["grid"]) # Center line
    
    canvas.create_text(width*0.92, ucl, text="UCL", fill=palette["danger"])
    canvas.create_text(width*0.92, chart_y, text="CL", fill=palette["grid"])
    canvas.create_text(width*0.92, lcl, text="LCL", fill=palette["danger"])
    
    # QAOA optimized anomaly detection
    pts = []
    num_pts = 30
    for i in range(num_pts):
        x = width*0.1 + i * (width*0.8 / num_pts)
        
        # Variation
        noise = math.sin(x*0.1 + phase*2) * 20 + math.cos(x*0.05 + phase*3) * 15
        
        # Simulate an out-of-control point
        if abs((i*3 - int(phase*5)) % num_pts) < 1:
            noise = 60 * (1 if math.sin(phase) > 0 else -1)
            
        y = chart_y + noise
        pts.extend([x, y])
        
        # Point styling
        color = palette["danger"] if y < ucl or y > lcl else palette["primary"]
        rad = 4 if color == palette["danger"] else 2
        canvas.create_oval(x-rad, y-rad, x+rad, y+rad, fill=color, outline="")
        
        if color == palette["danger"]: # highlight out of control
            canvas.create_oval(x-10, y-10, x+10, y+10, outline=palette["danger"], dash=(2, 2))
            
    canvas.create_line(*pts, fill=palette["secondary"], width=1, smooth=True)

@register_animation("facility_location")
def draw_facility_location(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Demand points (Cities)
    cities = []
    for i in range(15):
        cx = width*0.2 + (i*83 % (width*0.6))
        cy = height*0.2 + (i*47 % (height*0.6))
        weight = 2 + (i%3)*2
        cities.append((cx, cy, weight))
        canvas.create_oval(cx-weight, cy-weight, cx+weight, cy+weight, fill="#121e2b", outline=palette["secondary"])
        
    # Candidate Facility Locations (Optimization moving them to centers of mass)
    facs = [
        (width*0.3 + math.sin(phase)*50, height*0.3 + math.cos(phase)*30),
        (width*0.7 + math.cos(phase*1.2)*60, height*0.6 + math.sin(phase*0.8)*40)
    ]
    
    for fx, fy in facs:
        canvas.create_polygon(fx-10, fy-10, fx+10, fy-10, fx+10, fy+10, fx-10, fy+10, fill=palette["accent"], outline="")
        canvas.create_text(fx, fy, text="F", fill="#000", font=("Segoe UI", 8, "bold"))
        
        # Connect to nearest cluster
        for cx, cy, w in cities:
            if math.hypot(cx-fx, cy-fy) < width*0.35: # simplified assignment
                canvas.create_line(fx, fy, cx, cy, fill=palette["primary"], width=1, dash=(2, 4))
                
                # Flow moving to demand
                t = (phase*2 + (cx+cy)*0.01) % 1.0
                px = fx + (cx - fx)*t
                py = fy + (cy - fy)*t
                canvas.create_oval(px-2, py-2, px+2, py+2, fill=palette["primary"], outline="")
                
    # Center of gravity overlay
    canvas.create_text(width*0.5, height*0.9, text="QAOA Facility Optimization", fill=palette["text"], font=("Segoe UI", 10))


# ==========================================
# NUCLEAR ENGINEERING SYSTEMS
# ==========================================

@register_animation("monte_carlo")
def draw_monte_carlo(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Shielding material block
    canvas.create_rectangle(width*0.3, height*0.1, width*0.7, height*0.9, fill="#121e2b", outline=palette["primary"], width=2)
    canvas.create_text(width*0.5, height*0.05, text="Radiation Shielding", fill=palette["text"])
    
    # Neutron particles (Random walk simulation)
    num_particles = 15
    for i in range(num_particles):
        # Deterministic pseudo-random path for visual stability
        seed = i * 137
        life = (phase*10 + seed) % 100
        
        # Start left
        px, py = width*0.1, height*0.2 + (seed % 60)* height*0.01
        
        # Path trace
        path_pts = [px, py]
        active = True
        for step in range(int(life)):
            # "random" angle
            angle = (math.sin(seed + step*1.3) * math.pi/4) if px < width*0.3 else (math.sin(seed + step*2.7) * math.pi)
            step_len = 10 + math.cos(seed)*5
            
            px += math.cos(angle)*step_len
            py += math.sin(angle)*step_len
            path_pts.extend([px, py])
            
            # Absorption check
            if width*0.3 < px < width*0.7:
                prob_absorb = 0.05
                if math.sin(seed + step*3.1) < -1 + prob_absorb*2: # absorbed
                    active = False
                    canvas.create_oval(px-4, py-4, px+4, py+4, fill=palette["danger"], outline="")
                    break
                    
        if len(path_pts) >= 4:
            canvas.create_line(*path_pts, fill=palette["secondary"], width=1, dash=(2, 2))
            if active:
                canvas.create_oval(px-3, py-3, px+3, py+3, fill=palette["accent"], outline="")

@register_animation("fuel_burnup")
def draw_fuel_burnup(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Core grid
    rows, cols = 5, 5
    cell_s = 40
    start_x = cx - (cols)*cell_s/2
    start_y = cy - (rows)*cell_s/2
    
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * cell_s
            y = start_y + r * cell_s
            
            # Distance from center drives flux and therefore burnup
            dist = math.hypot(c - 2, r - 2)
            
            # Burnup fraction over time (phase)
            burn_rate = 1.0 / (1.0 + dist*0.5)
            burn_level = (phase*0.2 * burn_rate) % 1.0
            
            # Color gradient: fresh (primary) -> depleted (danger/dark)
            border = palette["primary"] if burn_level < 0.5 else palette["danger"]
            fill_c = "#0d1b2a" if burn_level > 0.8 else "#1a2b3d"
            
            canvas.create_rectangle(x+2, y+2, x+cell_s-2, y+cell_s-2, fill=fill_c, outline=border, width=2)
            
            # Pellet stack inside
            pellet_h = (cell_s-8) / 4
            for p in range(4):
                if burn_level < 0.2 + p*0.2:
                    canvas.create_rectangle(x+8, y+4+p*pellet_h, x+cell_s-8, y+2+(p+1)*pellet_h, fill=palette["accent"], outline="")
                    
    # VQE Flux Distribution curve below
    flux_y = height * 0.85
    canvas.create_line(width*0.2, flux_y, width*0.8, flux_y, fill=palette["grid"])
    canvas.create_text(width*0.5, flux_y + 20, text="Neutron Flux Profile", fill=palette["text"])
    
    flux_pts = []
    for fx in range(int(width*0.2), int(width*0.8), 5):
        t = (fx - cx) / (width*0.3)
        val = math.exp(-t**2 * 2) * 30 * (1.0 - 0.2*math.sin(phase)) # flattens as it burns
        flux_pts.extend([fx, flux_y - val])
    canvas.create_line(*flux_pts, fill=palette["danger"], width=2, smooth=True)

@register_animation("thermal_hydraulics")
def draw_thermal_hydraulics(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Primary Coolant Loop
    r_x, r_y = width*0.3, height*0.6 # Reactor
    sg_x, sg_y = width*0.7, height*0.4 # Steam Gen
    
    # Reactor vessel
    canvas.create_path = [
        r_x-30, r_y-60, r_x+30, r_y-60, 
        r_x+30, r_y+60, r_x-30, r_y+60
    ]
    canvas.create_polygon(*canvas.create_path, fill="#0a121a", outline=palette["primary"], width=3)
    
    # Core heating
    core_temp = math.sin(phase)*10
    canvas.create_rectangle(r_x-20, r_y, r_x+20, r_y+50, fill=palette["danger"], outline="")
    for i in range(5):
        canvas.create_line(r_x-15+i*7, r_y, r_x-15+i*7, r_y+50, fill="#fff")
        
    # Coolant pipes
    canvas.create_line(r_x, r_y-60, r_x, r_y-80, sg_x, r_y-80, sg_x, sg_y+40, fill=palette["danger"], width=6, capstyle=tk.ROUND) # Hot leg
    canvas.create_line(sg_x, sg_y+40, sg_x, r_y+80, r_x, r_y+80, r_x, r_y+60, fill=palette["primary"], width=6, capstyle=tk.ROUND) # Cold leg
    
    # Coolant flow bits
    p_len = r_y-80 + sg_x-r_x + sg_y+40 - (r_y-80)
    flow_t = (phase*60) % 200
    if flow_t < 40: canvas.create_oval(r_x-4, r_y-60-flow_t-4, r_x+4, r_y-60-flow_t+4, fill="#fff", outline="")
    elif flow_t < 140: canvas.create_oval(r_x+(flow_t-40)-4, r_y-80-4, r_x+(flow_t-40)+4, r_y-80+4, fill="#fff", outline="")
    
    # Steam Generator
    canvas.create_oval(sg_x-40, sg_y-60, sg_x+40, sg_y+60, fill="#121e2b", outline=palette["secondary"], width=2)
    
    # Boiling bubbles in SG
    for i in range(20):
        bx = sg_x - 30 + (i*17 + phase*10) % 60
        by = sg_y + 50 - (i*23 + phase*40) % 100
        rad = 1 + (sg_y + 50 - by)*0.05
        canvas.create_oval(bx-rad, by-rad, bx+rad, by+rad, fill="", outline=palette["secondary"])

# ==========================================
# PETROLEUM ENGINEERING SYSTEMS
# ==========================================

@register_animation("well_test")
def draw_well_test(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.3
    
    # Reservoir cross section
    canvas.create_rectangle(width*0.2, cy, width*0.8, cy+100, fill="#1c1611", outline=palette["grid"], width=2)
    # Wellbore
    canvas.create_rectangle(cx-8, cy-50, cx+8, cy+80, fill="#111", outline=palette["secondary"])
    
    # Pressure drawdown cone
    drawdown_pts = [width*0.2, cy]
    for x in range(int(width*0.2), int(width*0.8), 10):
        dist = abs(x - cx)
        if dist > 8:
            # log approximation
            p_drop = 40 * math.exp(-dist/50) * (0.5 + 0.5*math.sin(phase*0.2)) # transient building
            drawdown_pts.extend([x, cy + p_drop])
    drawdown_pts.extend([width*0.8, cy])
    canvas.create_line(*drawdown_pts, fill=palette["primary"], width=2, smooth=True)
    
    # Fluid flowing to well
    for i in range(30):
        dist = 20 + (i*15 - phase*20) % 150
        side = 1 if i % 2 == 0 else -1
        fx = cx + side * dist
        fy = cy + 20 + (i*7 % 60)
        
        if width*0.2 < fx < width*0.8:
            canvas.create_line(fx, fy, fx - side*10, fy, fill=palette["danger"], width=1, arrow=tk.LAST)
            
    # Semi-log diagnostic plot
    px, py = width*0.3, height*0.9
    canvas.create_line(px, py, px+250, py, fill=palette["grid"]) # log t
    canvas.create_line(px, py, px, py-100, fill=palette["grid"]) # dP
    canvas.create_text(px+125, py+15, text="Log Time ->", fill=palette["text"], font=("Segoe UI", 8))
    
    plot_pts = []
    for t in range(5, 200, 5):
        # radial flow derivative stabilizing
        dp = 100 * (1 - math.exp(-t/20))
        plot_pts.extend([px + t, py - dp + math.sin(phase*5 + t)*2]) # noise
    if len(plot_pts) > 4: canvas.create_line(*plot_pts, fill=palette["accent"], smooth=True, width=2)

@register_animation("hydraulic_fracturing")
def draw_hydraulic_fracturing(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Rock layers
    for i in range(4):
        y = cy - 60 + i*40
        canvas.create_line(width*0.1, y, width*0.9, y, fill=palette["grid"])
        
    # Horizontal well
    canvas.create_line(width*0.2, cy-100, width*0.2, cy, width*0.8, cy, fill="#555", width=6, capstyle=tk.ROUND)
    canvas.create_line(width*0.2, cy-100, width*0.2, cy, width*0.8, cy, fill=palette["secondary"], width=2, capstyle=tk.ROUND)
    
    # Fractures growing
    num_stages = 4
    for s in range(num_stages):
        stage_x = width*0.8 - s*(width*0.6/num_stages) - 20
        
        # QAOA optimizes frac spacing/length
        max_len = 40 + math.sin(s*2.1)*10
        growth = max(0, min(1.0, (phase*0.5 - s*0.2))) # sequential fracturing
        curr_len = max_len * growth
        
        if curr_len > 0:
            # Main cracks
            canvas.create_line(stage_x, cy, stage_x+10, cy-curr_len, fill=palette["danger"], width=2)
            canvas.create_line(stage_x, cy, stage_x-15, cy+curr_len, fill=palette["danger"], width=2)
            
            # Branching (complexity)
            if curr_len > 20:
                canvas.create_line(stage_x+5, cy-curr_len/2, stage_x+20, cy-curr_len*0.8, fill=palette["accent"], width=1)
                
            # Proppant
            canvas.create_oval(stage_x-3, cy-3, stage_x+3, cy+3, fill=palette["primary"], outline="")

@register_animation("enhanced_recovery")
def draw_enhanced_recovery(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Injector and Producer
    inj_x, prod_x = width * 0.2, width * 0.8
    res_y_top, res_y_bot = height * 0.4, height * 0.7
    
    canvas.create_rectangle(inj_x-6, height*0.2, inj_x+6, res_y_bot, fill="#1c2a38", outline=palette["primary"])
    canvas.create_rectangle(prod_x-6, height*0.2, prod_x+6, res_y_bot, fill="#1c2a38", outline=palette["danger"])
    
    # Reservoir
    canvas.create_rectangle(inj_x, res_y_top, prod_x, res_y_bot, outline=palette["grid"], width=2)
    
    # Sweep efficiency (QAOA profile)
    # CO2/Water front advancing
    sweep_pts = [inj_x, res_y_top]
    front_progress = width*0.2 + (phase*20) % (width*0.6)
    
    for y in range(int(res_y_top), int(res_y_bot)+1, 10):
        # Viscous fingering effect
        finger = math.sin(y*0.2 - phase*2) * 20
        # Gravity override (fluid rises or sinks)
        grav = (y - res_y_top) * 0.3
        
        fx = front_progress + finger - grav
        fx = min(max(inj_x, fx), prod_x)
        sweep_pts.extend([fx, y])
        
    sweep_pts.extend([inj_x, res_y_bot])
    
    # Fill swept area with injectant color
    if len(sweep_pts) > 4: canvas.create_polygon(*sweep_pts, fill="#0d1b2a", outline=palette["primary"], width=2)
    
    # Oil drops being pushed
    for i in range(15):
        oy = res_y_top + 10 + (i*23 % (res_y_bot - res_y_top - 20))
        finger_at_y = front_progress + math.sin(oy*0.2 - phase*2)*20 - (oy-res_y_top)*0.3
        
        ox = finger_at_y + 10 + (i*11 % 40)
        if ox < prod_x:
            canvas.create_oval(ox-4, oy-4, ox+4, oy+4, fill="#111", outline=palette["accent"])
            
    canvas.create_text(inj_x, height*0.15, text="Injector", fill=palette["primary"])
    canvas.create_text(prod_x, height*0.15, text="Producer", fill=palette["danger"])

# ==========================================
# MARINE ENGINEERING SYSTEMS
# ==========================================

@register_animation("ship_resistance")
def draw_ship_resistance(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.4, height * 0.5
    
    # Water surface (HHL Wave profile)
    wave_pts = []
    for x in range(0, int(width), 5):
        # Bow wave generated at cx
        amp = 0
        if x > cx:
            dist = x - cx
            amp = 20 * math.exp(-dist/100) * math.sin(dist*0.1 - phase*5)
        wave_pts.extend([x, cy + amp])
    canvas.create_line(*wave_pts, fill=palette["primary"], width=2)
    
    # Ship hull
    hull_l, hull_d = 120, 30
    hull_pts = [
        cx - hull_l*0.2, cy - 20, # stern top
        cx + hull_l*0.8, cy - 20, # bow top
        cx + hull_l*0.8, cy,      # bow waterline
        cx + hull_l*0.5, cy + hull_d, # bottom curve
        cx - hull_l*0.2, cy + hull_d*0.8 # stern curve
    ]
    canvas.create_polygon(*hull_pts, fill="#121e2b", outline=palette["accent"], width=2)
    
    # Pressure distribution on hull
    for i in range(10):
        t = i/9.0
        px = cx - hull_l*0.2 + t*hull_l
        
        # simplify pressure profile
        pressure = (1.0 if px > cx+hull_l*0.4 else -0.5 if px < cx else 0) * 15
        
        py = cy + hull_d # approx bottom
        canvas.create_line(px, py, px, py + pressure, fill=palette["danger"] if pressure>0 else palette["secondary"], arrow=tk.LAST)
        
    # Flow streamlines below hull
    for y in range(int(cy + hull_d + 10), int(height), 20):
        s_pts = []
        for x in range(0, int(width), 20):
            deflect = 0
            if cx - hull_l*0.2 < x < cx + hull_l*0.8:
                deflect = 10 * math.exp(-(y - cy - hull_d)/20)
            s_pts.extend([x - (phase*20)%20, y + deflect])
        canvas.create_line(*s_pts, fill=palette["grid"], smooth=True)

@register_animation("propeller")
def draw_propeller(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.1 * flow_factor
    cx, cy = width * 0.3, height * 0.5
    r_prop = height * 0.3
    
    # Side view of propeller rotating using 3D projection
    num_blades = 4
    for b in range(num_blades):
        angle = phase + b * (math.pi/2)
        
        # Blade twist and projection
        x_tip = cx + math.sin(angle) * 15 # pitches forward/back
        y_tip = cy + math.cos(angle) * r_prop
        
        # Only draw if "in front" for depth, or draw back ones darker
        is_front = math.sin(angle) > 0
        color = palette["secondary"] if is_front else palette["grid"]
        
        canvas.create_polygon(cx, cy-5, cx, cy+5, x_tip+10, y_tip, x_tip-10, y_tip, fill="#1a2b3d", outline=color, width=2)
        
    # Hub
    canvas.create_oval(cx-10, cy-15, cx+20, cy+15, fill="#121e2b", outline=palette["primary"])
    
    # Helical tip vortices (wake)
    for b in range(num_blades):
        v_pts = []
        angle_offset = b * (math.pi/2)
        for t in range(30):
            # traveling downstream (to the right)
            vx = cx + t*10
            # rotating
            vy = cy + math.cos(phase - t*0.5 + angle_offset) * r_prop * 0.9
            v_pts.extend([vx, vy])
            
        if len(v_pts) > 4: canvas.create_line(*v_pts, fill=palette["danger"], width=1, smooth=True, dash=(2, 4))
        
    # Thrust vector
    thrust_mag = 40 + math.sin(phase*4)*5
    canvas.create_line(cx+20, cy, cx+20+thrust_mag, cy, fill=palette["accent"], width=4, arrow=tk.LAST)

@register_animation("mooring_analysis")
def draw_mooring_analysis(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx = width * 0.5
    
    surface = height * 0.3
    seabed = height * 0.9
    canvas.create_line(0, seabed, width, seabed, fill=palette["primary"], width=4)
    
    # Waves (Drift forces)
    wave_pts = []
    for x in range(0, int(width), 10):
        wave_pts.extend([x, surface + math.sin(x*0.05 - phase*3)*15 + math.sin(x*0.02 - phase)*5])
    canvas.create_line(*wave_pts, fill=palette["primary"], width=2, smooth=True)
    
    # Floater response (Heave, Pitch, Surge)
    surge = math.sin(phase*1.5)*30
    heave = math.sin(phase*1.5 + math.pi/4)*10
    pitch = math.sin(phase*1.5 + math.pi/2)*0.1
    
    fx, fy = cx + surge, surface + heave
    
    # Platform
    p_w, p_h = 100, 20
    # rotate corners
    c1x = fx + math.cos(pitch)*(-p_w/2) - math.sin(pitch)*(-p_h)
    c1y = fy + math.sin(pitch)*(-p_w/2) + math.cos(pitch)*(-p_h)
    c2x = fx + math.cos(pitch)*(p_w/2) - math.sin(pitch)*(-p_h)
    c2y = fy + math.sin(pitch)*(p_w/2) + math.cos(pitch)*(-p_h)
    c4x = fx + math.cos(pitch)*(-p_w/2) - math.sin(pitch)*(p_h)
    c4y = fy + math.sin(pitch)*(-p_w/2) + math.cos(pitch)*(p_h)
    c3x = fx + math.cos(pitch)*(p_w/2) - math.sin(pitch)*(p_h)
    c3y = fy + math.sin(pitch)*(p_w/2) + math.cos(pitch)*(p_h)
    
    canvas.create_polygon(c1x, c1y, c2x, c2y, c3x, c3y, c4x, c4y, fill="#1a2b3d", outline=palette["secondary"], width=2)
    
    # Mooring lines (Catenary curve approximation)
    anchors = [(width*0.1, seabed), (width*0.9, seabed)]
    fairleads = [(c4x, c4y), (c3x, c3y)]
    
    for i in range(2):
        ax, ay = anchors[i]
        flx, fly = fairleads[i]
        
        # tension color
        dist = math.hypot(ax-flx, ay-fly)
        color = palette["danger"] if dist > math.hypot(width*0.4, seabed-surface) + 10 else palette["grid"]
        
        pts = []
        for t in range(11):
            p = t/10.0
            x = ax + (flx - ax)*p
            # catenary sag
            sag = 40 * math.sin(p * math.pi) * (1 - (dist / (height*0.8)))
            y = ay + (fly - ay)*p + max(0, sag)
            pts.extend([x, y])
            
        canvas.create_line(*pts, fill=color, width=2, smooth=True)

@register_animation("offshore_platform")
def draw_offshore_platform(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx = width * 0.5
    seabed = height * 0.9
    surface = height * 0.4
    
    canvas.create_line(0, seabed, width, seabed, fill=palette["primary"], width=4)
    canvas.create_line(0, surface, width, surface, fill=palette["secondary"], dash=(4,4))
    
    # Jacket structure
    top_y = height * 0.2
    base_w, top_w = 120, 80
    
    # Environmental load (wind + wave)
    load = math.sin(phase*2)*15
    
    # Nodes
    levels = 4
    left_legs, right_legs = [], []
    for l in range(levels+1):
        t = l/levels
        y = seabed - t*(seabed - top_y)
        w = base_w - t*(base_w - top_w)
        
        # Deflection profile (cantilever-like, squared)
        deflec = load * (t**2)
        
        left_legs.append((cx - w/2 + deflec, y))
        right_legs.append((cx + w/2 + deflec, y))
        
    # Draw members
    for l in range(levels):
        # horizontal
        canvas.create_line(left_legs[l][0], left_legs[l][1], right_legs[l][0], right_legs[l][1], fill=palette["grid"], width=3)
        # diagonal cross bracing
        canvas.create_line(left_legs[l][0], left_legs[l][1], right_legs[l+1][0], right_legs[l+1][1], fill=palette["accent"], width=2)
        canvas.create_line(right_legs[l][0], right_legs[l][1], left_legs[l+1][0], left_legs[l+1][1], fill=palette["accent"], width=2)
        
    # Main legs
    canvas.create_line(*[c for p in left_legs for c in p], fill=palette["primary"], width=4)
    canvas.create_line(*[c for p in right_legs for c in p], fill=palette["primary"], width=4)
    
    # Topside Deck
    d_x, d_y = cx + load, top_y
    canvas.create_rectangle(d_x - top_w/2 - 20, d_y-30, d_x + top_w/2 + 20, d_y, fill="#1a2b3d", outline=palette["danger"], width=2)
    canvas.create_text(d_x, d_y-15, text="Topside", fill=palette["text"])
    
    # Wave hitting
    wave_x = width*0.2 + (phase*80 % (width*0.8))
    canvas.create_oval(wave_x-20, surface-10, wave_x+20, surface+10, outline=palette["danger"])

# ==========================================
# AGRICULTURAL ENGINEERING SYSTEMS
# ==========================================

@register_animation("crop_growth")
def draw_crop_growth(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    ground_y = height * 0.7
    canvas.create_line(0, ground_y, width, ground_y, fill="#4a3b2c", width=10) # Soil
    
    # Sun / Photosynthesis
    sun_x, sun_y = width*0.8, height*0.2
    canvas.create_oval(sun_x-20, sun_y-20, sun_x+20, sun_y+20, fill="", outline=palette["accent"], width=3)
    for i in range(8):
        ang = phase + i*math.pi/4
        rx, ry = sun_x + math.cos(ang)*25, sun_y + math.sin(ang)*25
        canvas.create_line(sun_x, sun_y, rx, ry, fill=palette["accent"])
        
    # Plants
    num_plants = 4
    for p in range(num_plants):
        px = width * 0.2 + p * (width*0.5/num_plants)
        
        # VQE optimized growth parameter
        growth = 0.3 + 0.7 * (0.5 + 0.5*math.sin(phase*0.2 + p))
        
        stem_h = 100 * growth
        # Stem
        canvas.create_line(px, ground_y, px, ground_y - stem_h, fill=palette["primary"], width=4)
        
        # Leaves
        num_leaves = int(4 * growth)
        for l in range(num_leaves):
            ly = ground_y - 20 - l*20
            side = 1 if l%2==0 else -1
            canvas.create_oval(px, ly, px + side*30*growth, ly - 10, fill=palette["accent"], outline="")
            
        # Roots
        for r in range(3):
            canvas.create_line(px, ground_y, px + (r-1)*15*growth, ground_y + 40*growth, fill="#7b5e40", width=2)
            
        # Water uptake
        if math.sin(phase*5 + p) > 0:
            canvas.create_oval(px-3, ground_y+10, px+3, ground_y+16, fill=palette["secondary"], outline="")
            
@register_animation("irrigation")
def draw_irrigation(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    
    # Top-down view of Center Pivot
    cx, cy = width * 0.5, height * 0.5
    field_r = height * 0.4
    
    # Dry field background
    canvas.create_oval(cx - field_r, cy - field_r, cx + field_r, cy + field_r, fill="#2a2211", outline=palette["grid"])
    
    # QAOA optimized wetness map (simulated as concentric rings intersecting with pivot)
    arm_angle = phase * 0.5
    
    ax = cx + math.cos(arm_angle)*field_r
    ay = cy + math.sin(arm_angle)*field_r
    
    # Draw wetted area behind arm
    canvas.create_arc(cx - field_r, cy - field_r, cx + field_r, cy + field_r, start=-math.degrees(arm_angle), extent=45, fill="#1a3b2a", outline="")
    
    # Pivot Arm
    canvas.create_line(cx, cy, ax, ay, fill=palette["primary"], width=4)
    canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill=palette["danger"], outline="")
    
    # Sprinklers
    for s in range(5):
        rad = (s+1) * field_r/5
        sx = cx + math.cos(arm_angle)*rad
        sy = cy + math.sin(arm_angle)*rad
        
        canvas.create_oval(sx-3, sy-3, sx+3, sy+3, fill=palette["accent"], outline="")
        
        # Water spray
        spray_r = 15 + math.sin(phase*10 + s)*5
        canvas.create_oval(sx-spray_r, sy-spray_r, sx+spray_r, sy+spray_r, outline=palette["secondary"], dash=(2,2))
        
    canvas.create_text(width*0.15, height*0.1, text="Soil Moisture Cov.", fill=palette["text"], font=("Segoe UI", 10))

@register_animation("grain_drying")
def draw_grain_drying(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.5, height * 0.5
    
    # Silo
    silo_w, silo_h = 100, height * 0.6
    canvas.create_rectangle(cx - silo_w/2, cy - silo_h/2, cx + silo_w/2, cy + silo_h/2, outline=palette["grid"], width=3)
    canvas.create_polygon(cx - silo_w/2, cy - silo_h/2, cx + silo_w/2, cy - silo_h/2, cx, cy - silo_h/2 - 40, outline=palette["grid"], width=3, fill="")
    
    # Grain bed
    grain_lvl = cy + silo_h/2 - silo_h*0.7 # 70% full
    canvas.create_rectangle(cx - silo_w/2 + 2, grain_lvl, cx + silo_w/2 - 2, cy + silo_h/2 - 2, fill="#2a2211", outline="")
    
    # Particles/Moisture
    for i in range(30):
        # grain particles
        gx = cx - silo_w/2 + 10 + (i*13 % (silo_w-20))
        gy = grain_lvl + 10 + (i*29 % (cy + silo_h/2 - grain_lvl - 20))
        
        canvas.create_oval(gx-2, gy-2, gx+2, gy+2, fill=palette["accent"], outline="")
        
        # hot air rising
        hx = cx - silo_w/2 + 10 + (i*7 % (silo_w-20))
        hy = cy + silo_h/2 - (phase*60 + i*15) % silo_h
        
        # air cools and picks up moisture
        air_t = 1.0 - (cy + silo_h/2 - hy) / silo_h
        col = palette["danger"] if air_t > 0.6 else palette["secondary"]
        if hy > grain_lvl - 20:
            canvas.create_line(hx, hy, hx, hy-10, fill=col, width=2)
            
    # HHL Heat Transfer profile
    px, py = width*0.8, cy + silo_h/2
    canvas.create_line(px, py, px, py - silo_h, fill=palette["grid"])
    canvas.create_text(px, py-silo_h-15, text="Moisture %", fill=palette["text"])
    
    m_pts = []
    for y in range(int(py - silo_h*0.7), int(py), 5):
        t = (py - y) / (silo_h*0.7)
        # exponential drying profile
        m = 20 * math.exp(-t*3) * (0.8 + 0.2*math.sin(phase))
        m_pts.extend([px + m, y])
    if len(m_pts) > 4: canvas.create_line(*m_pts, fill=palette["primary"], width=2, smooth=True)

@register_animation("greenhouse_controller")
def draw_greenhouse_controller(canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str], flow_factor: float) -> None:
    phase = tick * 0.05 * flow_factor
    cx, cy = width * 0.4, height * 0.6
    
    # Greenhouse structure
    gw, gh = 160, 100
    pts = [
        cx - gw/2, cy + gh/2,
        cx + gw/2, cy + gh/2,
        cx + gw/2, cy - gh/4,
        cx, cy - gh/2,
        cx - gw/2, cy - gh/4
    ]
    canvas.create_polygon(*pts, fill="#0a121a", outline=palette["primary"], width=3)
    
    # Vents (QAOA optimized opening)
    vent_open = 10 + math.sin(phase)*10
    canvas.create_line(cx, cy - gh/2, cx + 30, cy - gh/2 - vent_open, fill=palette["accent"], width=3)
    
    # Internal Climate Variables
    # Temp
    canvas.create_text(cx - 40, cy, text="T:", fill=palette["danger"])
    t_val = 22 + math.sin(phase)*3
    canvas.create_rectangle(cx - 20, cy - 5, cx - 20 + t_val, cy + 5, fill=palette["danger"], outline="")
    
    # Humidity
    canvas.create_text(cx - 40, cy + 20, text="RH:", fill=palette["secondary"])
    h_val = 60 + math.cos(phase)*10
    canvas.create_rectangle(cx - 20, cy + 15, cx - 20 + h_val*0.5, cy + 25, fill=palette["secondary"], outline="")
    
    # CO2
    canvas.create_text(cx - 40, cy + 40, text="CO2:", fill=palette["grid"])
    co2_val = 400 + math.sin(phase*0.5)*100
    canvas.create_rectangle(cx - 20, cy + 35, cx - 20 + co2_val*0.1, cy + 45, fill=palette["grid"], outline="")
    
    # Fan
    fx, fy = cx + gw/2 - 20, cy - 10
    canvas.create_oval(fx-10, fy-10, fx+10, fy+10, outline=palette["primary"])
    canvas.create_line(fx-8, fy, fx+8, fy, fill=palette["primary"])
    canvas.create_line(fx, fy-8, fx, fy+8, fill=palette["primary"])
    # Fan breeze
    if t_val > 23:
        for i in range(3):
            bx = fx - 20 - (phase*20 + i*10) % 30
            canvas.create_line(bx, fy-5+i*5, bx-10, fy-5+i*5, fill=palette["muted"])

