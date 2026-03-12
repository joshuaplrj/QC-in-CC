"""
Quantum Systems Launcher
Unified launcher for all quantum system simulations with a modern, engaging UI.
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os
import inspect
import importlib
import statistics
from PIL import Image

# Ensure both project root and quantum_systems package are importable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
for candidate in (PROJECT_ROOT, CURRENT_DIR):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class QuantumLauncher(ctk.CTk):
    """Modern dashboard launcher for quantum systems library"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Quantum Systems Simulation Library")
        self.geometry("1100x700")
        
        # Grid layout 1x2 (Sidebar and Main Frame)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Registry and Filter State
        self.disciplines = self._get_disciplines()
        self.all_systems = [
            {"discipline": d, "name": n, "module": m, "algo": a}
            for d, systems in self.disciplines.items()
            for n, m, a in systems
        ]
        self.current_filter = "All Systems"
        self.system_cards = []

        self.setup_ui()
        
    def _get_disciplines(self):
        return {
            "Computer Science": [
                ("Cryptography", "computer_science.cryptography", "Shor's + Grover's"),
                ("Database Optimizer", "computer_science.database_optimizer", "Grover's search"),
                ("Compiler Optimizer", "computer_science.compiler_optimizer", "QAOA"),
                ("Blockchain Simulator", "computer_science.blockchain_simulator", "Post-quantum"),
                ("Network Flow", "computer_science.network_flow", "QAOA"),
                ("Algorithm Visualizer", "computer_science.algorithm_viz", "Multi-algorithm"),
            ],
            "Electrical Engineering": [
                ("Power Flow", "electrical.power_flow", "HHL"),
                ("Circuit Simulator", "electrical.circuit_simulator", "HHL"),
                ("Signal Processor", "electrical.signal_processor", "QFT"),
                ("Antenna Pattern", "electrical.antenna_pattern", "HHL"),
                ("Motor Drive", "electrical.motor_drive", "QAOA"),
                ("VLSI Placement", "electrical.vlsi_placement", "QAOA"),
                ("Communication Channel", "electrical.communication_channel", "Grover's"),
            ],
            "Mechanical Engineering": [
                ("CFD Solver", "mechanical.cfd_solver", "Quantum Lattice Boltzmann"),
                ("FEA Solver", "mechanical.fea_solver", "HHL"),
                ("Robot Kinematics", "mechanical.robot_kinematics", "QAOA"),
                ("Heat Engine", "mechanical.heat_engine", "VQE"),
                ("Vibration Analysis", "mechanical.vibration_analysis", "QFT"),
                ("Manufacturing", "mechanical.manufacturing", "QAOA"),
                ("Turbomachinery", "mechanical.turbomachinery", "HHL"),
                ("Combined Cycle", "mechanical.combined_cycle", "QAOA"),
            ],
            "Civil Engineering": [
                ("Bridge Analysis", "civil.bridge_analysis", "HHL"),
                ("Traffic Flow", "civil.traffic_flow", "QAOA"),
                ("Water Network", "civil.water_network", "HHL"),
                ("Seismic Analysis", "civil.seismic_analysis", "QFT"),
                ("Construction", "civil.construction", "QAOA"),
                ("Urban Planning", "civil.urban_planning", "QAOA"),
            ],
            "Chemical Engineering": [
                ("Process Flow", "chemical.process_flow", "HHL"),
                ("Reactor Design", "chemical.reactor_design", "VQE"),
                ("Distillation", "chemical.distillation", "QAOA"),
                ("Heat Exchanger", "chemical.heat_exchanger", "HHL"),
                ("Adsorption", "chemical.adsorption", "VQE"),
                ("Polymerization", "chemical.polymerization", "VQE"),
            ],
            "Aerospace Engineering": [
                ("Panel Method", "aerospace.panel_method", "HHL"),
                ("Turbojet", "aerospace.turbojet", "QAOA"),
                ("Aircraft Weight", "aerospace.aircraft_weight", "QAOA"),
                ("Trajectory", "aerospace.trajectory", "Grover's"),
                ("Composite Materials", "aerospace.composite", "VQE"),
                ("Orbital Mechanics", "aerospace.orbital", "HHL"),
                ("Hypersonic Flow", "aerospace.hypersonic", "Quantum Walk"),
            ],
            "Biomedical Engineering": [
                ("Medical Imaging", "biomedical.medical_imaging", "QFT"),
                ("Biomechanics", "biomedical.biomechanics", "HHL"),
                ("Pharmacokinetics", "biomedical.pharmacokinetics", "VQE"),
                ("EKG Analyzer", "biomedical.ekg_analyzer", "QFT"),
                ("DNA Aligner", "biomedical.dna_aligner", "Grover's"),
            ],
            "Environmental Engineering": [
                ("Wind Farm", "environmental.wind_farm", "QAOA"),
                ("Atmospheric Model", "environmental.atmospheric", "Quantum Walk"),
                ("River Quality", "environmental.river_quality", "HHL"),
                ("Groundwater Flow", "environmental.groundwater_flow", "HHL"),
                ("Carbon Cycle", "environmental.carbon_cycle", "VQE"),
            ],
            "Materials Science": [
                ("Molecular Dynamics", "materials_science.molecular_dynamics", "VQE"),
                ("Phase Diagram", "materials_science.phase_diagram", "VQE"),
                ("Crystallography", "materials_science.crystallography", "QFT"),
                ("Corrosion Predictor", "materials_science.corrosion_predictor", "VQE"),
                ("Composite Micromechanics", "materials_science.composite_micromechanics", "HHL"),
                ("Heat Treatment", "materials_science.heat_treatment", "VQE"),
            ],
            "Industrial Engineering": [
                ("Job Shop", "industrial.job_shop", "QAOA"),
                ("Supply Chain", "industrial.supply_chain", "QAOA"),
                ("Assembly Line", "industrial.assembly_line", "QAOA"),
                ("Queuing Network", "industrial.queuing_network", "HHL"),
                ("Statistical Control", "industrial.statistical_control", "QAOA"),
                ("Facility Location", "industrial.facility_location", "QAOA"),
            ],
            "Nuclear Engineering": [
                ("Reactor Kinetics", "nuclear.reactor_kinetics", "HHL"),
                ("Monte Carlo", "nuclear.monte_carlo", "Quantum Walk"),
                ("Fuel Burnup", "nuclear.fuel_burnup", "VQE"),
                ("Thermal Hydraulics", "nuclear.thermal_hydraulics", "HHL"),
            ],
            "Petroleum Engineering": [
                ("Reservoir", "petroleum.reservoir", "HHL"),
                ("Well Test", "petroleum.well_test", "HHL"),
                ("Hydraulic Fracturing", "petroleum.hydraulic_fracturing", "QAOA"),
                ("Enhanced Recovery", "petroleum.enhanced_recovery", "QAOA"),
            ],
            "Marine Engineering": [
                ("Ship Resistance", "marine.ship_resistance", "HHL"),
                ("Propeller", "marine.propeller", "QAOA"),
                ("Mooring Analysis", "marine.mooring_analysis", "HHL"),
                ("Offshore Platform", "marine.offshore_platform", "HHL"),
            ],
            "Agricultural Engineering": [
                ("Crop Growth", "agricultural.crop_growth", "VQE"),
                ("Irrigation", "agricultural.irrigation", "QAOA"),
                ("Grain Drying", "agricultural.grain_drying", "HHL"),
                ("Greenhouse Controller", "agricultural.greenhouse_controller", "QAOA"),
            ],
        }

    def setup_ui(self):
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1) # The scrollable area expands

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="QUANTUM", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        self.sub_logo_label = ctk.CTkLabel(self.sidebar_frame, text="Simulation Library", font=ctk.CTkFont(size=12))
        self.sub_logo_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        # Scrollable Discipline Area
        self.navigation_frame = ctk.CTkScrollableFrame(self.sidebar_frame, fg_color="transparent", corner_radius=0)
        self.navigation_frame.grid(row=2, column=0, sticky="nsew", padx=5)
        self.navigation_frame.grid_columnconfigure(0, weight=1)

        self.sidebar_buttons = []
        
        # All Systems Button
        all_btn = ctk.CTkButton(self.navigation_frame, text="All Systems", 
                                 fg_color="transparent", text_color=("gray10", "gray90"),
                                 hover_color=("gray70", "gray30"),
                                 anchor="w", command=lambda: self.select_discipline("All Systems"))
        all_btn.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.sidebar_buttons.append(all_btn)

        # Department Buttons
        for i, disc in enumerate(self.disciplines.keys(), start=1):
            btn = ctk.CTkButton(self.navigation_frame, text=disc, 
                                 fg_color="transparent", text_color=("gray10", "gray90"),
                                 hover_color=("gray70", "gray30"),
                                 anchor="w", command=lambda d=disc: self.select_discipline(d))
            btn.grid(row=i, column=0, padx=10, pady=2, sticky="ew")
            self.sidebar_buttons.append(btn)

        # Footer Actions
        self.footer_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.footer_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.benchmark_btn = ctk.CTkButton(self.footer_frame, text="Benchmarks", 
                                           fg_color="#ff8b5c", hover_color="#e67e51",
                                           command=self.run_benchmarks)
        self.benchmark_btn.grid(row=0, column=0, pady=(0, 5), sticky="ew")
        
        self.test_btn = ctk.CTkButton(self.footer_frame, text="Run Tests", 
                                     fg_color="#3fbf7f", hover_color="#34a36b",
                                     command=self.run_tests)
        self.test_btn.grid(row=1, column=0, sticky="ew")

        # Main Content Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.header_frame, text="Available Systems", font=ctk.CTkFont(size=30, weight="bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.search_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Search systems...", width=300)
        self.search_entry.grid(row=0, column=1, padx=(20, 0))
        self.search_entry.bind("<KeyRelease>", self.filter_systems)

        # Scrollable Grid
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Status Bar
        self.status_bar = ctk.CTkLabel(self, text=f"Ready to launch {len(self.all_systems)} systems", anchor="w", padx=10)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.select_discipline("All Systems")

    def select_discipline(self, discipline):
        self.current_filter = discipline
        self.title_label.configure(text=discipline)
        
        for btn in self.sidebar_buttons:
            if btn.cget("text") == discipline:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")
        
        self.refresh_grid()

    def filter_systems(self, event=None):
        self.refresh_grid()

    def refresh_grid(self):
        for child in self.scrollable_frame.winfo_children():
            child.destroy()
        self.system_cards = []

        search_query = self.search_entry.get().lower()
        
        # Group by discipline for headers
        disciplines_to_show = []
        if self.current_filter == "All Systems":
            disciplines_to_show = list(self.disciplines.keys())
        else:
            disciplines_to_show = [self.current_filter]

        current_row = 0
        total_shown = 0

        for disc in disciplines_to_show:
            # Filter systems for this discipline
            filtered = [
                s for s in self.all_systems 
                if s["discipline"] == disc
                and (search_query in s["name"].lower() or search_query in s["algo"].lower())
            ]
            
            if not filtered:
                continue

            # Add Discipline Header
            header = ctk.CTkLabel(self.scrollable_frame, text=disc, 
                                  font=ctk.CTkFont(size=20, weight="bold"), 
                                  text_color=("#0a2a66", "#4fa1ff"))
            header.grid(row=current_row, column=0, columnspan=3, sticky="w", padx=10, pady=(15, 10))
            current_row += 1

            # Add System Cards in grid
            for i, s in enumerate(filtered):
                card = ctk.CTkFrame(self.scrollable_frame, width=280, height=160, corner_radius=15, border_width=1)
                card.grid(row=current_row + (i // 3), column=i % 3, padx=10, pady=10, sticky="nsew")
                card.grid_propagate(False)
                
                name_lbl = ctk.CTkLabel(card, text=s["name"], font=ctk.CTkFont(size=16, weight="bold"), wraplength=240)
                name_lbl.pack(pady=(15, 5), padx=10)
                
                algo_lbl = ctk.CTkLabel(card, text=s["algo"], font=ctk.CTkFont(size=12, slant="italic"), text_color="gray")
                algo_lbl.pack(pady=0, padx=10)
                
                launch_btn = ctk.CTkButton(card, text="Launch", width=120, corner_radius=20,
                                           command=lambda m=s["module"]: self.launch_system(m))
                launch_btn.pack(side="bottom", pady=15)
                
                self.system_cards.append(card)
            
            current_row += (len(filtered) + 2) // 3
            total_shown += len(filtered)

        self.status_bar.configure(text=f"Showing {total_shown} systems")

    def launch_system(self, module_name):
        self.status_bar.configure(text=f"Launching {module_name}...")
        self.update_idletasks()
        
        try:
            full_module_name = f"quantum_systems.{module_name}"
            module = importlib.import_module(full_module_name)

            app_class = self._resolve_system_class(module, module_name)
            if app_class is None:
                raise AttributeError(f"No compatible GUI class found in {full_module_name}.")

            new_root = ctk.CTkToplevel(self)
            new_root.title(f"Quantum {module_name.split('.')[-1].replace('_', ' ').title()}")
            new_root.after(100, lambda: new_root.focus()) # Ensure it comes to front

            app = app_class()
            app.setup_gui(new_root)
            self.status_bar.configure(text=f"Launched {module_name}")
                
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch {module_name}:\n{str(e)}")
            self.status_bar.configure(text=f"Error launching {module_name}")

    def _expected_class_name(self, module_name):
        return ''.join(word.capitalize() for word in module_name.split('.')[-1].split('_'))

    def _resolve_system_class(self, module, module_name):
        expected_name = self._expected_class_name(module_name)
        candidates = [
            cls for _, cls in inspect.getmembers(module, inspect.isclass)
            if cls.__module__ == module.__name__ and callable(getattr(cls, 'setup_gui', None))
        ]
        for preferred_name in (expected_name, f"Quantum{expected_name}"):
            for candidate in candidates:
                if candidate.__name__ == preferred_name:
                    return candidate
        return candidates[0] if candidates else None

    def run_benchmarks(self):
        self.status_bar.configure(text="Running benchmarks...")
        self.update_idletasks()

        records = []
        failures = []
        total = len(self.all_systems)

        for idx, sys_info in enumerate(self.all_systems, start=1):
            display_name = sys_info["name"]
            module_name = sys_info["module"]
            algorithm = sys_info["algo"]
            
            if idx == 1 or idx % 10 == 0:
                self.status_bar.configure(text=f"Benchmarking {idx}/{total}: {display_name}")
                self.update_idletasks()

            try:
                full_module_name = f"quantum_systems.{module_name}"
                module = importlib.import_module(full_module_name)
                app_class = self._resolve_system_class(module, module_name)
                if app_class is None:
                    failures.append((module_name, "no compatible class"))
                    continue

                app = app_class()
                app.n_qubits = 16
                quantum_result = app.execute_quantum()
                classical_result = app.execute_classical()

                c_time = float(classical_result.get("time", 0.0) or 0.0)
                q_time = float(quantum_result.get("time", 0.0) or 0.0)
                speedup = (c_time / q_time) if q_time > 0.0 else 0.0

                c_rmse = float(classical_result.get("rmse", 0.0) or 0.0)
                q_rmse = float(quantum_result.get("rmse", 0.0) or 0.0)
                rmse_gain = ((c_rmse - q_rmse) / max(c_rmse, 1e-9)) * 100.0

                # Genuine memory advantage
                compression = float(quantum_result.get("memory_compression", 1.0) or 1.0)

                records.append({
                    "name": display_name, "module": module_name, "algorithm": algorithm,
                    "speedup": speedup, "classical_time": c_time, "quantum_time": q_time,
                    "rmse_gain": rmse_gain, "quantum_r2": float(quantum_result.get("r2", 0.0) or 0.0),
                    "memory_compression": compression,
                })
            except Exception as exc:
                failures.append((module_name, str(exc)))

        if not records:
            messagebox.showerror("Benchmark Results", "No benchmark results were produced.")
            self.status_bar.configure(text="Benchmarks failed")
            return

        avg_speedup = statistics.fmean(item["speedup"] for item in records)
        median_speedup = statistics.median(item["speedup"] for item in records)
        avg_rmse_gain = statistics.fmean(item["rmse_gain"] for item in records)
        avg_q_r2 = statistics.fmean(item["quantum_r2"] for item in records)
        avg_compression = statistics.fmean(item["memory_compression"] for item in records)

        top_speed = sorted(records, key=lambda item: item["speedup"], reverse=True)[:3]
        top_compression = sorted(records, key=lambda item: item["memory_compression"], reverse=True)[:3]

        lines = [
            "Quantum Systems Benchmark Summary",
            "=================================",
            "",
            f"Systems evaluated: {len(records)} / {total}",
            f"Average time ratio: {avg_speedup:.4f}x",
            f"Average memory compression: {avg_compression:.1f}x (CTMP advantage)",
            f"Average RMSE improvement: {avg_rmse_gain:.2f}%",
            f"Average quantum R2: {avg_q_r2:.4f}",
            "",
            "Top Memory Compression (genuine CTMP advantage):",
        ]
        for idx, item in enumerate(top_compression, start=1):
            lines.append(
                f"{idx}. {item['name']} ({item['algorithm']}) - {item['memory_compression']:.1f}x compression"
            )

        lines.append("")
        lines.append("Timing (honest measured):")
        for idx, item in enumerate(top_speed, start=1):
            lines.append(
                f"{idx}. {item['name']} ({item['algorithm']}) - "
                f"[C: {item['classical_time']:.4f}s | Q: {item['quantum_time']:.4f}s]"
            )

        if failures:
            lines.append("")
            lines.append(f"Failed modules: {len(failures)}")
            for module_name, reason in failures[:5]:
                lines.append(f"- {module_name}: {reason}")

        messagebox.showinfo("Benchmark Results", "\n".join(lines))
        self.status_bar.configure(text="Benchmarks complete")
    
    def run_tests(self):
        """Run unit tests"""
        self.status_bar.configure(text="Running tests...")
        self.update_idletasks()
        
        try:
            import subprocess
            tests_path = os.path.join(CURRENT_DIR, 'core', 'tests')
            result = subprocess.run([sys.executable, '-m', 'pytest', tests_path, '-v'],
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                messagebox.showinfo("Tests", "All tests passed!")
            else:
                messagebox.showerror("Tests", f"Some tests failed:\n{result.stdout}")
                
        except Exception as e:
            messagebox.showinfo("Tests", f"Test execution:\n{str(e)}")
        
        self.status_bar.configure(text="Tests complete")

if __name__ == "__main__":
    app = QuantumLauncher()
    app.mainloop()
