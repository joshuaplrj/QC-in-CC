"""
Classical Systems Launcher
Unified launcher for all classical system simulations.
"""

import os
import sys
import inspect
import json
import math
import tkinter as tk
from tkinter import ttk, messagebox
try:
    from classical_systems.ui_utils import configure_window_geometry
except ModuleNotFoundError:
    import os
    import sys

    current_dir = os.path.dirname(os.path.abspath(__file__))
    for candidate in (current_dir, os.path.dirname(current_dir)):
        if candidate not in sys.path:
            sys.path.insert(0, candidate)

    from ui_utils import configure_window_geometry


class ClassicalSystemsLauncher:
    """Main launcher for the classical systems library."""

    def __init__(self, root):
        self.root = root
        self.root.title("Classical Systems Simulation Library - Launcher")
        configure_window_geometry(self.root, width=1100, height=760)
        self.root.minsize(920, 600)
        self.root.configure(bg="#1e1e1e")

        self.simulations = self._build_simulations()

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        self.status_var = tk.StringVar(
            value=f"Ready to launch {self.total_simulations} classical systems"
        )
        self.setup_ui()

    @property
    def total_simulations(self):
        """Return total number of simulations available."""
        return sum(len(systems) for systems in self.simulations.values())

    def _build_simulations(self):
        """Define all available classical simulations."""
        return {
            "Computer Science": [
                ("Algorithm Visualizer", "computer_science.algorithm_viz", "Sorting and graph algorithm demos"),
                ("Network Flow", "computer_science.network_flow", "Max-flow and min-cut analysis"),
                ("Cryptography", "computer_science.cryptography", "RSA and AES workflow demonstration"),
                ("Cryptography Workbench", "computer_science.cryptography_workbench", "Interactive crypto sandbox"),
                ("Database Optimizer", "computer_science.database_optimizer", "Query planning and optimization"),
                ("Compiler Optimizer", "computer_science.compiler_optimizer", "Code optimization techniques"),
                ("Blockchain Simulator", "computer_science.blockchain_simulator", "Consensus and ledger simulation"),
            ],
            "Electrical Engineering": [
                ("Power Flow", "electrical.power_flow", "Grid analysis on benchmark networks"),
                ("Circuit Simulator", "electrical.circuit_simulator", "SPICE-like transient and AC analysis"),
                ("Signal Processor", "electrical.signal_processor", "DSP and filtering pipeline"),
                ("Antenna Pattern", "electrical.antenna_pattern", "3D radiation pattern modeling"),
                ("Motor Drive", "electrical.motor_drive", "Vector control and drive response"),
                ("VLSI Placement", "electrical.vlsi_placement", "Chip placement optimization"),
                ("Communication Channel", "electrical.communication_channel", "BER and channel behavior"),
            ],
            "Mechanical Engineering": [
                ("CFD Solver", "mechanical.cfd_solver", "Navier-Stokes flow simulation"),
                ("FEA Solver", "mechanical.fea_solver", "Finite element stress analysis"),
                ("Robot Kinematics", "mechanical.robot_kinematics", "Multi-DOF robotic arm modeling"),
                ("Heat Engine", "mechanical.heat_engine", "Thermodynamic cycle analysis"),
                ("Vibration Analysis", "mechanical.vibration", "Modal and time-domain response"),
                ("Manufacturing", "mechanical.manufacturing", "CNC process optimization"),
                ("Turbomachinery", "mechanical.turbomachinery", "Compressor and turbine analysis"),
                ("Combined Cycle", "mechanical.combined_cycle", "Power plant integration model"),
            ],
            "Civil Engineering": [
                ("Bridge Analysis", "civil.bridge_analysis", "3D truss and frame evaluation"),
                ("Traffic Flow", "civil.traffic_flow", "Macroscopic traffic dynamics"),
                ("Water Network", "civil.water_network", "Hydraulic distribution simulation"),
                ("Seismic Analysis", "civil.seismic_analysis", "Response spectrum evaluation"),
                ("Construction", "civil.construction", "CPM and PERT scheduling"),
                ("Urban Planning", "civil.urban_planning", "Growth and zoning scenario modeling"),
            ],
            "Chemical Engineering": [
                ("Process Flow", "chemical.process_flow", "Steady-state process simulation"),
                ("Reactor Design", "chemical.reactor_design", "CSTR and PFR behavior"),
                ("Distillation", "chemical.distillation", "Column operation and separation"),
                ("Heat Exchanger", "chemical.heat_exchanger", "Network synthesis and sizing"),
                ("Adsorption", "chemical.adsorption", "Breakthrough and loading curves"),
                ("Polymerization", "chemical.polymerization", "Kinetics and conversion tracking"),
            ],
            "Aerospace Engineering": [
                ("Panel Method", "aerospace.panel_method", "Potential flow aerodynamics"),
                ("Turbojet", "aerospace.turbojet", "Engine performance cycle analysis"),
                ("Aircraft Weight", "aerospace.aircraft_weight", "Weight and balance estimation"),
                ("Trajectory", "aerospace.trajectory", "Mission path optimization"),
                ("Composite", "aerospace.composite", "Laminate structural analysis"),
                ("Orbital", "aerospace.orbital", "Two-body and transfer mechanics"),
                ("Hypersonic", "aerospace.hypersonic", "Shock and high-speed flow modeling"),
            ],
            "Biomedical Engineering": [
                ("Medical Imaging", "biomedical.medical_imaging", "CT and MRI reconstruction"),
                ("Biomechanics", "biomedical.biomechanics", "Joint and motion mechanics"),
                ("Pharmacokinetics", "biomedical.pharmacokinetics", "Drug concentration over time"),
                ("EKG Analyzer", "biomedical.ekg_analyzer", "Cardiac signal processing"),
                ("DNA Aligner", "biomedical.dna_aligner", "Sequence alignment analysis"),
            ],
            "Environmental Engineering": [
                ("Atmospheric Model", "environmental.atmospheric", "Pollutant dispersion modeling"),
                ("River Quality", "environmental.river_quality", "Water quality and contaminant transport"),
                ("Wind Farm", "environmental.wind_farm", "Turbine placement optimization"),
                ("Groundwater Flow", "environmental.groundwater_flow", "Aquifer behavior simulation"),
                ("Carbon Cycle", "environmental.carbon_cycle", "Climate carbon balance model"),
            ],
            "Materials Science": [
                ("Molecular Dynamics", "materials_science.molecular_dynamics", "Atomistic system simulation"),
                ("Phase Diagram", "materials_science.phase_diagram", "Phase equilibrium prediction"),
                ("Crystallography", "materials_science.crystallography", "Crystal structure visualization"),
                ("Corrosion Predictor", "materials_science.corrosion_predictor", "Degradation rate forecasting"),
                ("Composite Micromechanics", "materials_science.composite_micromechanics", "Constituent-level properties"),
                ("Heat Treatment", "materials_science.heat_treatment", "TTT and CCT process behavior"),
            ],
            "Industrial Engineering": [
                ("Job Shop", "industrial.job_shop", "Constraint-driven scheduling"),
                ("Supply Chain", "industrial.supply_chain", "Network planning and logistics"),
                ("Assembly Line", "industrial.assembly_line", "Line balancing and throughput"),
                ("Queuing Network", "industrial.queuing_network", "Service and waiting-time analysis"),
                ("Statistical Control", "industrial.statistical_control", "Process quality monitoring"),
                ("Facility Location", "industrial.facility_location", "Site selection optimization"),
            ],
            "Nuclear Engineering": [
                ("Reactor Kinetics", "nuclear.reactor_kinetics", "Point-reactor dynamic model"),
                ("Monte Carlo", "nuclear.monte_carlo", "Particle transport and shielding"),
                ("Fuel Burnup", "nuclear.fuel_burnup", "Depletion and isotope tracking"),
                ("Thermal Hydraulics", "nuclear.thermal_hydraulics", "Two-phase thermal flow"),
            ],
            "Petroleum Engineering": [
                ("Reservoir", "petroleum.reservoir", "Reservoir pressure and production"),
                ("Well Test", "petroleum.well_test", "Pressure transient interpretation"),
                ("Hydraulic Fracturing", "petroleum.hydraulic_fracturing", "Fracture propagation simulation"),
                ("Enhanced Recovery", "petroleum.enhanced_recovery", "EOR strategy analysis"),
            ],
            "Marine Engineering": [
                ("Ship Resistance", "marine.ship_resistance", "Hull drag and propulsion load"),
                ("Propeller", "marine.propeller", "Propeller performance design"),
                ("Mooring Analysis", "marine.mooring_analysis", "Line tension and station keeping"),
                ("Offshore Platform", "marine.offshore_platform", "Platform stability modeling"),
            ],
            "Agricultural Engineering": [
                ("Crop Growth", "agricultural.crop_growth", "Crop development simulation"),
                ("Irrigation", "agricultural.irrigation", "Field irrigation planning"),
                ("Grain Drying", "agricultural.grain_drying", "Moisture reduction modeling"),
                ("Greenhouse Controller", "agricultural.greenhouse_controller", "Climate control optimization"),
            ],
        }

    def setup_ui(self):
        """Build launcher UI with a quantum-style layout (without top readme text)."""
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        title_label = tk.Label(
            self.root,
            text="Classical Systems Simulation Library",
            font=("Helvetica", 24, "bold"),
            bg="#1e1e1e",
            fg="cyan",
        )
        title_label.pack(pady=(20, 6))

        subtitle = tk.Label(
            self.root,
            text="Unified launcher for full-spectrum classical engineering simulations",
            font=("Helvetica", 12),
            bg="#1e1e1e",
            fg="white",
        )
        subtitle.pack(pady=(0, 12))

        systems_frame = tk.LabelFrame(
            self.root,
            text="Available Classical Systems",
            bg="#1e1e1e",
            fg="white",
            font=("Helvetica", 12, "bold"),
            labelanchor="n",
        )
        systems_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(6, 16))

        canvas = tk.Canvas(systems_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(systems_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

        scrollable_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(window_id, width=event.width),
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame.grid_columnconfigure(0, weight=4)
        scrollable_frame.grid_columnconfigure(1, weight=3)
        scrollable_frame.grid_columnconfigure(2, weight=0)

        row = 0
        for discipline, systems in self.simulations.items():
            discipline_label = tk.Label(
                scrollable_frame,
                text=discipline,
                font=("Helvetica", 11, "bold"),
                bg="#1e1e1e",
                fg="yellow",
            )
            discipline_label.grid(row=row, column=0, columnspan=3, sticky="w", pady=(14, 4), padx=8)
            row += 1

            for name, module, description in systems:
                name_label = tk.Label(
                    scrollable_frame,
                    text=f"  - {name}",
                    font=("Helvetica", 10),
                    bg="#1e1e1e",
                    fg="white",
                    anchor="w",
                )
                name_label.grid(row=row, column=0, sticky="w", padx=(20, 8), pady=2)

                desc_label = tk.Label(
                    scrollable_frame,
                    text=description,
                    font=("Helvetica", 9, "italic"),
                    bg="#1e1e1e",
                    fg="#4ecdc4",
                    anchor="w",
                )
                desc_label.grid(row=row, column=1, sticky="w", padx=8)

                launch_btn = tk.Button(
                    scrollable_frame,
                    text="Launch",
                    command=lambda m=module, n=name: self.launch_simulation(m, n),
                    bg="#4ecdc4",
                    fg="black",
                    font=("Helvetica", 9, "bold"),
                    width=10,
                    relief=tk.FLAT,
                    activebackground="#6fe3da",
                )
                launch_btn.grid(row=row, column=2, padx=(8, 10), pady=2)

                row += 1

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=(0, 16))

        tk.Button(
            button_frame,
            text="View Statistics",
            command=self.show_statistics,
            bg="#ff6b6b",
            fg="white",
            font=("Helvetica", 11, "bold"),
            width=18,
            relief=tk.FLAT,
            activebackground="#ff8787",
        ).pack(side=tk.LEFT, padx=8)

        tk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit,
            bg="#ffeaa7",
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=10,
            relief=tk.FLAT,
            activebackground="#fff0c4",
        ).pack(side=tk.LEFT, padx=8)

        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#2d2d2d",
            fg="white",
            padx=8,
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _resolve_simulation_class(self, module):
        """Resolve a SimulationBase subclass from a module."""
        try:
            from classical_systems.core import SimulationBase
        except ModuleNotFoundError:
            from core import SimulationBase

        module_classes = [
            cls
            for _, cls in inspect.getmembers(module, inspect.isclass)
            if cls.__module__ == module.__name__
            and issubclass(cls, SimulationBase)
            and cls is not SimulationBase
        ]

        if not module_classes:
            return None

        expected = "".join(
            part.capitalize() for part in module.__name__.split(".")[-1].split("_")
        ) + "Simulation"

        for cls in module_classes:
            if cls.__name__.lower() == expected.lower():
                return cls

        return module_classes[0]

    @staticmethod
    def _humanize_metric_name(name):
        """Convert nested metric keys into compact labels."""
        parts = [part for part in str(name).split(".") if part]
        if not parts:
            label = "Metric"
        elif len(parts) == 1:
            label = parts[0].replace("_", " ").strip().title()
        else:
            label = f"{parts[-2]}.{parts[-1]}".replace("_", " ").strip().title()
        return (label[:28] + "...") if len(label) > 28 else label

    @staticmethod
    def _format_metric_value(value):
        """Format numbers for card and chart labels."""
        abs_value = abs(value)
        if abs_value >= 1000:
            return f"{value:,.2f}"
        if abs_value >= 1:
            return f"{value:.4f}"
        return f"{value:.6f}"

    def _extract_numeric_metrics(self, payload):
        """Extract scalar metrics from nested simulation results without deriving new values."""
        metrics = []

        def record(name, value):
            if isinstance(value, bool):
                return
            if isinstance(value, (int, float)):
                numeric = float(value)
                if math.isfinite(numeric):
                    metrics.append((name, numeric))

        def walk(node, prefix=""):
            if isinstance(node, dict):
                for key, value in node.items():
                    next_prefix = f"{prefix}.{key}" if prefix else str(key)
                    walk(value, next_prefix)
                return

            if isinstance(node, (list, tuple)):
                # Skip list aggregation to avoid synthetic metrics that are not shown in text.
                return

            record(prefix or "value", node)

        walk(payload)

        if not metrics:
            return []

        unique_metrics = []
        seen_paths = set()
        for name, value in metrics:
            if name in seen_paths:
                continue
            seen_paths.add(name)
            label = self._humanize_metric_name(name)
            unique_metrics.append((label, value))
            if len(unique_metrics) >= 8:
                break
        return unique_metrics

    def _draw_visual_dashboard(self, window, bar_canvas, gauge_canvas, metrics):
        """Render metric-faithful charts with decorative animation overlays."""
        palette = ["#4ecdc4", "#ff6b6b", "#ffe66d", "#7dd3fc", "#c084fc", "#a3e635"]
        state = {"tick": 0}
        values = [value for _, value in metrics]
        v_min = min(values) if values else 0.0
        v_max = max(values) if values else 1.0
        if math.isclose(v_min, v_max):
            pad = 1.0 if math.isclose(v_max, 0.0) else abs(v_max) * 0.15
            v_min -= pad
            v_max += pad

        def animate():
            try:
                if not window.winfo_exists():
                    return
            except tk.TclError:
                return

            state["tick"] += 1
            t = state["tick"]

            bar_canvas.delete("all")
            width = max(bar_canvas.winfo_width(), 480)
            height = max(bar_canvas.winfo_height(), 220)
            left_pad = 14
            right_pad = 10
            top_pad = 30
            bottom = height - 32
            available_height = max(40.0, float(bottom - top_pad))
            value_span = max(v_max - v_min, 1e-9)

            def value_to_y(value):
                frac = (value - v_min) / value_span
                return bottom - (frac * available_height)

            zero_y = value_to_y(0.0)

            bar_canvas.create_text(
                left_pad,
                10,
                text="Metric Values (exact data values)",
                fill="#8de9ff",
                anchor="nw",
                font=("Helvetica", 10, "bold"),
            )
            bar_canvas.create_line(left_pad, zero_y, width - right_pad, zero_y, fill="#466287", width=1)
            bar_canvas.create_text(
                width - right_pad,
                zero_y - 8,
                text="0",
                anchor="e",
                fill="#7fa7c8",
                font=("Consolas", 8),
            )

            count = max(len(metrics), 1)
            slot_width = max(30.0, (width - left_pad - right_pad) / count)
            for idx, (label, value) in enumerate(metrics):
                x0 = left_pad + idx * slot_width + 6
                x1 = left_pad + (idx + 1) * slot_width - 6
                y_value = value_to_y(value)
                y0 = min(zero_y, y_value)
                y1 = max(zero_y, y_value)

                color = palette[idx % len(palette)]
                bar_canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
                bar_canvas.create_text(
                    (x0 + x1) / 2,
                    y0 - 9 if value >= 0 else y1 + 9,
                    text=self._format_metric_value(value),
                    fill="#f3fdff",
                    font=("Consolas", 8),
                )
                bar_canvas.create_text(
                    (x0 + x1) / 2,
                    bottom + 12,
                    text=label,
                    fill="#d7ebff",
                    font=("Helvetica", 8),
                )

            # Decorative scan line: animation only, does not alter data geometry.
            scan_x = left_pad + (t * 6 % max(1.0, width - left_pad - right_pad))
            bar_canvas.create_line(scan_x, top_pad, scan_x, bottom, fill="#4ecdc4", width=1, stipple="gray50")

            gauge_canvas.delete("all")
            gauge_w = max(gauge_canvas.winfo_width(), 250)
            gauge_h = max(gauge_canvas.winfo_height(), 220)
            center_x = gauge_w / 2
            center_y = gauge_h * 0.52
            radius = min(gauge_w, gauge_h) * 0.26
            magnitudes = [abs(value) for _, value in metrics]
            total_mag = sum(magnitudes)

            gauge_canvas.create_text(
                center_x,
                18,
                text="Metric Share Donut (from exact values)",
                fill="#8de9ff",
                font=("Helvetica", 10, "bold"),
            )
            gauge_canvas.create_oval(
                center_x - radius - 16,
                center_y - radius - 16,
                center_x + radius + 16,
                center_y + radius + 16,
                outline="#253a58",
                width=2,
            )
            start = 120.0
            dominant_label = "-"
            dominant_value = 0.0
            for idx, (label, value) in enumerate(metrics):
                share = (abs(value) / total_mag) if total_mag > 0 else (1.0 / max(len(metrics), 1))
                extent = max(1.0, 300.0 * share)
                color = palette[idx % len(palette)]
                gauge_canvas.create_arc(
                    center_x - radius - 16,
                    center_y - radius - 16,
                    center_x + radius + 16,
                    center_y + radius + 16,
                    start=start,
                    extent=extent,
                    style=tk.ARC,
                    width=10,
                    outline=color,
                )
                start += extent
                if abs(value) >= abs(dominant_value):
                    dominant_label = label
                    dominant_value = value

            gauge_canvas.create_text(
                center_x,
                center_y - 4,
                text=dominant_label,
                fill="#effdff",
                font=("Helvetica", 9, "bold"),
            )
            gauge_canvas.create_text(
                center_x,
                center_y + 16,
                text=self._format_metric_value(dominant_value),
                fill="#d6f5ff",
                font=("Consolas", 10, "bold"),
            )
            gauge_canvas.create_text(
                center_x,
                center_y + 34,
                text="largest absolute metric",
                fill="#aacfe6",
                font=("Helvetica", 8),
            )

            for idx in range(4):
                angle = (t * 0.085) + (idx * (math.pi / 2.0))
                orbit = radius + 22 + idx * 7
                px = center_x + math.cos(angle) * orbit
                py = center_y + math.sin(angle) * orbit * 0.65
                color = palette[idx % len(palette)]
                gauge_canvas.create_oval(px - 3, py - 3, px + 3, py + 3, fill=color, width=0)

            sparkline = []
            trend_y = gauge_h - 26
            for idx, (_, value) in enumerate(metrics):
                x = 20 + idx * (gauge_w - 40) / max(1, len(metrics) - 1)
                normalized = (value - v_min) / value_span
                y = trend_y - normalized * 44
                sparkline.extend([x, y])
            if len(sparkline) >= 4:
                gauge_canvas.create_line(*sparkline, fill="#7dd3fc", width=2, smooth=True)

            try:
                window.after(55, animate)
            except tk.TclError:
                return

        animate()

    def _show_result_window(self, display_name, module_name, result):
        """Show simulation results in a dedicated launcher window."""
        window = tk.Toplevel(self.root)
        window.title(f"{display_name} - Results")
        configure_window_geometry(window, width=1040, height=760)
        window.minsize(700, 450)
        window.configure(bg="#1e1e1e")

        tk.Label(
            window,
            text=display_name,
            font=("Helvetica", 18, "bold"),
            bg="#1e1e1e",
            fg="cyan",
        ).pack(anchor="w", padx=16, pady=(12, 4))

        tk.Label(
            window,
            text=f"Module: classical_systems.{module_name}",
            font=("Helvetica", 10),
            bg="#1e1e1e",
            fg="#bdbdbd",
        ).pack(anchor="w", padx=16, pady=(0, 10))

        metrics = self._extract_numeric_metrics(result)
        if metrics:
            visual_frame = tk.LabelFrame(
                window,
                text="Visual Analytics",
                bg="#1e1e1e",
                fg="#8de9ff",
                font=("Helvetica", 10, "bold"),
            )
            visual_frame.pack(fill=tk.X, padx=16, pady=(0, 10))

            cards_frame = tk.Frame(visual_frame, bg="#1e1e1e")
            cards_frame.pack(fill=tk.X, padx=8, pady=(6, 4))

            for idx, (label, value) in enumerate(metrics[:4]):
                cards_frame.grid_columnconfigure(idx, weight=1)
                card = tk.Frame(
                    cards_frame,
                    bg="#243148",
                    highlightbackground="#3e5478",
                    highlightthickness=1,
                    padx=8,
                    pady=6,
                )
                card.grid(row=0, column=idx, sticky="ew", padx=4)
                tk.Label(
                    card,
                    text=label,
                    font=("Helvetica", 8, "bold"),
                    bg="#243148",
                    fg="#8de9ff",
                    anchor="w",
                ).pack(anchor="w")
                tk.Label(
                    card,
                    text=self._format_metric_value(value),
                    font=("Consolas", 10, "bold"),
                    bg="#243148",
                    fg="#f3fdff",
                    anchor="w",
                ).pack(anchor="w", pady=(2, 0))

            chart_row = tk.Frame(visual_frame, bg="#1e1e1e")
            chart_row.pack(fill=tk.BOTH, expand=True, padx=8, pady=(2, 8))

            bar_canvas = tk.Canvas(
                chart_row,
                height=230,
                bg="#0f1624",
                highlightthickness=1,
                highlightbackground="#2b3c5a",
            )
            bar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

            gauge_canvas = tk.Canvas(
                chart_row,
                width=300,
                height=230,
                bg="#0b141d",
                highlightthickness=1,
                highlightbackground="#2b3c5a",
            )
            gauge_canvas.pack(side=tk.LEFT, fill=tk.Y)

            self._draw_visual_dashboard(window, bar_canvas, gauge_canvas, metrics[:6])

        frame = tk.Frame(window, bg="#1e1e1e")
        frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 12))

        text = tk.Text(
            frame,
            wrap=tk.NONE,
            bg="#111111",
            fg="#d7ffd7",
            insertbackground="#d7ffd7",
            font=("Consolas", 10),
        )
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=text.xview)
        text.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        text.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        formatted = (
            json.dumps(result, indent=2, default=str)
            if isinstance(result, dict)
            else str(result)
        )
        text.insert("1.0", formatted)
        text.configure(state=tk.DISABLED)

        tk.Button(
            window,
            text="Close",
            command=window.destroy,
            bg="#4ecdc4",
            fg="black",
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            activebackground="#6fe3da",
            width=12,
        ).pack(pady=(0, 12))

    def launch_simulation(self, module_name, display_name):
        """Launch a selected classical simulation module."""
        full_module_path = f"classical_systems.{module_name}"
        self.status_var.set(f"Launching {display_name}...")
        self.root.update_idletasks()

        try:
            module = __import__(full_module_path, fromlist=["main"])
            result = None
            launched = False

            if hasattr(module, "main"):
                launched = True
                result = module.main()
            else:
                sim_class = self._resolve_simulation_class(module)
                if sim_class is not None:
                    launched = True
                    simulation = sim_class()
                    if hasattr(simulation, "run") and callable(simulation.run):
                        result = simulation.run()

            if not launched:
                messagebox.showerror(
                    "Launch Error",
                    f"{module_name} is missing both main() and a runnable SimulationBase class.",
                )
                self.status_var.set(f"Launch failed: {display_name}")
                return

            if isinstance(result, dict):
                self._show_result_window(display_name, module_name, result)

            self.status_var.set(f"Launched {display_name}")
        except ImportError as exc:
            messagebox.showerror(
                "Import Error",
                f"Could not import {module_name}.\n\n{exc}",
            )
            self.status_var.set(f"Import failed: {display_name}")
        except Exception as exc:
            messagebox.showerror(
                "Launch Error",
                f"Failed to launch {display_name}:\n{exc}",
            )
            self.status_var.set(f"Error launching {display_name}")

    def show_statistics(self):
        """Show summary statistics for the classical systems library."""
        lines = ["Classical Systems Statistics", "=" * 32, ""]
        for discipline, systems in self.simulations.items():
            lines.append(f"{discipline}: {len(systems)} systems")

        lines.extend(
            [
                "",
                f"Total systems: {self.total_simulations}",
                f"Disciplines: {len(self.simulations)}",
            ]
        )

        messagebox.showinfo("Statistics", "\n".join(lines))
        self.status_var.set("Statistics loaded")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = ClassicalSystemsLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
