import os

code = '''
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
'''

with open('c:\\Users\\John Jacob\\Desktop\\Desktop\\QC in CC\\QB in CC\\quantum_systems\\custom_animations.py', 'a') as f:
    f.write(code)
