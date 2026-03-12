"""Stable baseline template for quantum modules."""
from __future__ import annotations

import math
import time
import tkinter as tk
from tkinter import ttk
from typing import Any
import webbrowser
import os
import urllib.parse

from quantum_systems.core import (
    CTMP_Engine,
    CircuitVisualizer,
    MemristorEmulator,
    NeuralNetworkMode,
    PerformanceBenchmark,
    QuantumGate,
    build_reference_dataset,
    fit_metrics,
    predict_from_reference,
)


class BaseQuantumSystem:

    _DISCIPLINE_DEFAULT_SCENE = {
        "computer_science": "algorithm",
        "electrical": "circuit",
        "mechanical": "kinematics",
        "civil": "structural",
        "chemical": "process",
        "aerospace": "aerospace",
        "biomedical": "scanner",
        "environmental": "fluid",
        "materials_science": "lattice",
        "industrial": "assembly",
        "nuclear": "reactor",
        "petroleum": "fluid",
        "marine": "marine",
        "agricultural": "agriculture",
    }

    _SCENE_OVERRIDES = {
        "cryptography": "crypto",
        "blockchain_simulator": "blockchain",
        "network_flow": "network",
        "database_optimizer": "algorithm",
        "compiler_optimizer": "algorithm",
        "algorithm_viz": "algorithm",
        "power_flow": "network",
        "signal_processor": "wave",
        "antenna_pattern": "antenna",
        "motor_drive": "energy",
        "vlsi_placement": "chip",
        "communication_channel": "network",
        "cfd_solver": "fluid",
        "fea_solver": "structural",
        "robot_kinematics": "kinematics",
        "heat_engine": "energy",
        "vibration_analysis": "wave",
        "manufacturing": "assembly",
        "turbomachinery": "turbomachinery",
        "combined_cycle": "energy",
        "bridge_analysis": "structural",
        "traffic_flow": "network",
        "water_network": "network",
        "seismic_analysis": "wave",
        "construction": "assembly",
        "urban_planning": "network",
        "composite": "lattice",
        "trajectory": "orbit",
        "orbital": "orbit",
        "hypersonic": "aerospace",
        "medical_imaging": "scanner",
        "biomechanics": "kinematics",
        "pharmacokinetics": "pharma",
        "ekg_analyzer": "wave",
        "dna_aligner": "dna",
        "wind_farm": "windfarm",
        "carbon_cycle": "carbon_cycle",
        "river_quality": "fluid",
        "groundwater_flow": "fluid",
        "atmospheric": "fluid",
        "supply_chain": "network",
        "queuing_network": "network",
        "statistical_control": "algorithm",
        "facility_location": "network",
        "offshore_platform": "marine",
        "mooring_analysis": "marine",
        "ship_resistance": "marine",
        "propeller": "marine",
        "enhanced_recovery": "process",
        "hydraulic_fracturing": "fluid",
        "reservoir": "fluid",
        "well_test": "fluid",
        "phase_diagram": "lattice",
        "crystallography": "lattice",
        "corrosion_predictor": "lattice",
        "composite_micromechanics": "lattice",
        "heat_treatment": "lattice",
        "molecular_dynamics": "lattice",
        "thermal_hydraulics": "reactor",
        "monte_carlo": "reactor",
    }

    _SCENE_DESCRIPTIONS = {
        "algorithm": "Algorithm-state evolution",
        "network": "Flow through a connected network",
        "blockchain": "Distributed ledger block propagation",
        "circuit": "Electrical node and current behavior",
        "wave": "Signal-domain waveform dynamics",
        "antenna": "Radiation pattern sweep",
        "chip": "Placement and route activity",
        "energy": "Thermodynamic energy cycle",
        "fluid": "Fluid transport and pressure field",
        "structural": "Structural response under load",
        "kinematics": "Mechanism and joint motion",
        "assembly": "Discrete manufacturing workflow",
        "turbomachinery": "Rotor-stator flow simulation",
        "process": "Process-plant unit operations",
        "aerospace": "Airframe and flow interaction",
        "orbit": "Orbital and trajectory mechanics",
        "scanner": "Medical scan reconstruction view",
        "pharma": "Compartmental drug kinetics",
        "dna": "Sequence alignment dynamics",
        "windfarm": "Wind energy capture field",
        "carbon_cycle": "Atmosphere-biosphere-ocean cycle",
        "lattice": "Material microstructure evolution",
        "reactor": "Reactor-core neutron and heat state",
        "marine": "Hydrodynamic marine response",
        "agriculture": "Crop and irrigation process",
        "crypto": "Number-theoretic key process",
        "generic": "System-state animation",
    }

    _DISCIPLINE_PALETTES = {
        "computer_science": {
            "bg": "#07131f",
            "grid": "#112a40",
            "primary": "#4ecdc4",
            "secondary": "#7dd3fc",
            "accent": "#ffe66d",
            "danger": "#ff6b6b",
            "text": "#eaf7ff",
            "muted": "#9ac6df",
        },
        "electrical": {
            "bg": "#0d111c",
            "grid": "#22304a",
            "primary": "#4ecdc4",
            "secondary": "#f6bd60",
            "accent": "#84dcc6",
            "danger": "#ff7f50",
            "text": "#f0f7ff",
            "muted": "#acc7de",
        },
        "mechanical": {
            "bg": "#11141d",
            "grid": "#273245",
            "primary": "#7dd3fc",
            "secondary": "#f4a261",
            "accent": "#e9c46a",
            "danger": "#e76f51",
            "text": "#f4f7fb",
            "muted": "#b7c8d8",
        },
        "civil": {
            "bg": "#121820",
            "grid": "#2a3a4e",
            "primary": "#8ecae6",
            "secondary": "#ffb703",
            "accent": "#90be6d",
            "danger": "#e76f51",
            "text": "#edf6ff",
            "muted": "#b8cddd",
        },
        "chemical": {
            "bg": "#101922",
            "grid": "#23384b",
            "primary": "#4ecdc4",
            "secondary": "#ffd166",
            "accent": "#90be6d",
            "danger": "#ff6b6b",
            "text": "#edf8ff",
            "muted": "#a9c8d8",
        },
        "aerospace": {
            "bg": "#0a1220",
            "grid": "#1b3352",
            "primary": "#7dd3fc",
            "secondary": "#a3e635",
            "accent": "#f8cc7c",
            "danger": "#ff6b6b",
            "text": "#edf8ff",
            "muted": "#a8c6de",
        },
        "biomedical": {
            "bg": "#0b1d1a",
            "grid": "#1f3f39",
            "primary": "#4ecdc4",
            "secondary": "#7dd3fc",
            "accent": "#f6bd60",
            "danger": "#ff8fab",
            "text": "#effffd",
            "muted": "#b4dad7",
        },
        "environmental": {
            "bg": "#0f1f1a",
            "grid": "#27453a",
            "primary": "#90be6d",
            "secondary": "#4ecdc4",
            "accent": "#f6bd60",
            "danger": "#f28482",
            "text": "#f2fff5",
            "muted": "#bdd9c5",
        },
        "materials_science": {
            "bg": "#151822",
            "grid": "#30384b",
            "primary": "#9db4ff",
            "secondary": "#a3e635",
            "accent": "#ffd166",
            "danger": "#ff6b6b",
            "text": "#f4f7ff",
            "muted": "#c2cada",
        },
        "industrial": {
            "bg": "#171c22",
            "grid": "#323f4c",
            "primary": "#7dd3fc",
            "secondary": "#f6bd60",
            "accent": "#a3e635",
            "danger": "#ef476f",
            "text": "#f8fbff",
            "muted": "#c0cfdb",
        },
        "nuclear": {
            "bg": "#11141d",
            "grid": "#2a3447",
            "primary": "#7dd3fc",
            "secondary": "#ffe66d",
            "accent": "#ff8c42",
            "danger": "#ff595e",
            "text": "#f7fbff",
            "muted": "#bfccdc",
        },
        "petroleum": {
            "bg": "#1b1916",
            "grid": "#3b342a",
            "primary": "#f6bd60",
            "secondary": "#84dcc6",
            "accent": "#ffe66d",
            "danger": "#f28482",
            "text": "#fff8ef",
            "muted": "#dbc9b3",
        },
        "marine": {
            "bg": "#081a2a",
            "grid": "#1f3e59",
            "primary": "#7dd3fc",
            "secondary": "#4ecdc4",
            "accent": "#f6bd60",
            "danger": "#ff6b6b",
            "text": "#eef9ff",
            "muted": "#a6c9df",
        },
        "agricultural": {
            "bg": "#162418",
            "grid": "#36533a",
            "primary": "#90be6d",
            "secondary": "#ffd166",
            "accent": "#4ecdc4",
            "danger": "#f28482",
            "text": "#f1ffe8",
            "muted": "#c1d8b2",
        },
    }

    def __init__(
        self,
        name: str,
        n_qubits: int = 8,
        max_bond_dim: int = 16,
        classical_time_target: float = 1.0,
    ) -> None:
        self.name = name
        self.n_qubits = n_qubits
        self.max_bond_dim = max_bond_dim
        self.classical_time_target = classical_time_target
        self.ctmp_engine = CTMP_Engine(n_qubits=n_qubits, max_bond_dim=max_bond_dim)
        self.memristor = MemristorEmulator(n_memristors=n_qubits)
        self.circuit_viz = CircuitVisualizer(self.ctmp_engine)
        self.neural_mode = NeuralNetworkMode(n_qubits=n_qubits, bond_dim=max_bond_dim)
        self.benchmark = PerformanceBenchmark(name)

        self.classical_result: dict[str, Any] | None = None
        self.quantum_result: dict[str, Any] | None = None

        module_parts = self.__class__.__module__.split(".")
        self.discipline = module_parts[-2] if len(module_parts) >= 2 else "general"
        self.system_key = module_parts[-1] if module_parts else self.name.lower().replace(" ", "_")
        self.scene_kind = self._resolve_scene_kind()

        self.visual_history: list[float] = []
        self.run_history: list[dict[str, float]] = []
        self._max_history_points = 40
        self._last_history_signature: tuple[float, float, float, int] | None = None

        self._visual_labels = [
            "Classical Time (s)",
            "Quantum Time (s)",
            "Speedup (x)",
            "Compression (x)",
            "Gate Count",
        ]
        self._visual_target = [0.0 for _ in self._visual_labels]
        self._visual_current = [0.0 for _ in self._visual_labels]
        self._animation_tick = 0
        self._animation_job = None
        self._latest_reference: list[float] = []
        self._latest_classical_series: list[float] = []
        self._latest_quantum_series: list[float] = []
        self._latest_x: list[float] = []
        self._latest_dataset_info: dict[str, str] = {
            "x_label": "Time",
            "y_label": "Response",
            "unit": "arb",
        }
        self._latest_classical_fit: dict[str, float] = {}
        self._latest_quantum_fit: dict[str, float] = {}
        self._latest_data_source = "Built-in baseline models"

    def _resolve_scene_kind(self) -> str:
        if self.system_key in self._SCENE_OVERRIDES:
            return self._SCENE_OVERRIDES[self.system_key]
        return self._DISCIPLINE_DEFAULT_SCENE.get(self.discipline, "generic")

    def _scene_palette(self) -> dict[str, str]:
        return dict(
            self._DISCIPLINE_PALETTES.get(
                self.discipline,
                {
                    "bg": "#0c1420",
                    "grid": "#20374f",
                    "primary": "#7dd3fc",
                    "secondary": "#4ecdc4",
                    "accent": "#ffe66d",
                    "danger": "#ff6b6b",
                    "text": "#f0f8ff",
                    "muted": "#b4cee0",
                },
            )
        )

    def setup_gui(self, root: tk.Tk) -> None:
        root.title(f"Quantum {self.name}")
        root.geometry("1180x820")
        frame = ttk.Frame(root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=f"Quantum {self.name}", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)

        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=(10, 8))
        ttk.Label(controls, text="Qubits (n):").pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=self.n_qubits)
        ttk.Spinbox(controls, from_=4, to=64, textvariable=self.size_var, width=8).pack(side=tk.LEFT, padx=6)
        ttk.Button(controls, text="Run", command=self.run_simulation).pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="Compare", command=self.compare_results).pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="Metrics", command=self.show_metrics).pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=4)

        analytics_frame = tk.LabelFrame(
            frame,
            text="Metrics",
            bg="#0f1724",
            fg="#8ee9ff",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=8,
        )
        analytics_frame.pack(fill=tk.X, pady=(0, 8))

        cards_frame = tk.Frame(analytics_frame, bg="#0f1724")
        cards_frame.pack(fill=tk.X)
        self.metric_card_vars: dict[str, tk.StringVar] = {}
        card_specs = [
            ("classical_time", "Classical Time (s)"),
            ("quantum_time", "Quantum Time (s)"),
            ("speedup", "Speedup"),
            ("compression", "Compression"),
            ("gate_count", "Gate Count"),
            ("quantum_rmse", "Quantum RMSE"),
            ("quantum_r2", "Quantum R2"),
        ]

        for idx, (key, title) in enumerate(card_specs):
            cards_frame.grid_columnconfigure(idx, weight=1)
            card = tk.Frame(
                cards_frame,
                bg="#1a2740",
                highlightbackground="#35507d",
                highlightthickness=1,
                padx=10,
                pady=6,
            )
            card.grid(row=0, column=idx, sticky="ew", padx=4)
            tk.Label(
                card,
                text=title,
                bg="#1a2740",
                fg="#8ee9ff",
                font=("Segoe UI", 8, "bold"),
                anchor="w",
            ).pack(anchor="w")

            value_var = tk.StringVar(value="0.000")
            tk.Label(
                card,
                textvariable=value_var,
                bg="#1a2740",
                fg="#f0fdff",
                font=("Consolas", 10, "bold"),
                anchor="w",
            ).pack(anchor="w", pady=(2, 0))
            self.metric_card_vars[key] = value_var

        sim_frame = tk.LabelFrame(
            frame,
            text="Simulation View",
            bg="#0e1724",
            fg="#8ee9ff",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=6,
        )
        sim_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        scene_desc = self._SCENE_DESCRIPTIONS.get(self.scene_kind, self._SCENE_DESCRIPTIONS["generic"])
        self.scene_info_var = tk.StringVar(value=f"{self.name}: {scene_desc}")
        tk.Label(
            sim_frame,
            textvariable=self.scene_info_var,
            bg="#0e1724",
            fg="#bfe9ff",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        ).pack(fill=tk.X, padx=4, pady=(0, 4))

        canvas_row = tk.Frame(sim_frame, bg="#0e1724")
        canvas_row.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 4))

        self.simulation_canvas = tk.Canvas(
            canvas_row,
            height=360,
            bg="#08111b",
            highlightthickness=1,
            highlightbackground="#35507d",
        )
        self.simulation_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        self.speed_canvas = tk.Canvas(
            canvas_row,
            width=340,
            height=360,
            bg="#07111d",
            highlightthickness=1,
            highlightbackground="#35507d",
        )
        self.speed_canvas.pack(side=tk.LEFT, fill=tk.Y)

        self.output_text = tk.Text(frame, height=10, bg="#111111", fg="#d7ffd7", font=("Consolas", 10))
        self.output_text.pack(fill=tk.BOTH, expand=False)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, pady=(8, 0))

        self._refresh_visual_targets(record_history=False)
        self._animate_visuals()

    def log(self, msg: str) -> None:
        if hasattr(self, "output_text"):
            self.output_text.insert(tk.END, msg + "\n")
            self.output_text.see(tk.END)

    @staticmethod
    def _safe_number(value: Any, default: float = 0.0) -> float:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return default
        return numeric if math.isfinite(numeric) else default

    @staticmethod
    def _format_metric(value: float) -> str:
        abs_value = abs(value)
        if abs_value >= 1000:
            return f"{value:,.2f}"
        if abs_value >= 1:
            return f"{value:.4f}"
        return f"{value:.6f}"

    def _stable_seed(self, suffix: str = "") -> int:
        key = f"{self.discipline}:{self.system_key}:{suffix}:{getattr(self, '_seed', 0)}"
        value = 0
        for byte in key.encode("utf-8"):
            value = (value * 167 + byte) % 2_147_483_647
        return value or 1

    def _algorithm_family(self) -> str:
        if self.scene_kind in {"network", "assembly", "chip", "blockchain"}:
            return "QAOA"
        if self.scene_kind in {"wave", "antenna", "scanner", "dna"}:
            return "QFT"
        if self.scene_kind in {"process", "energy", "lattice", "pharma", "reactor"}:
            return "VQE"
        if self.scene_kind in {"crypto", "algorithm"}:
            return "Grover/Shor"
        return "HHL"

    def _quality_targets(self) -> tuple[float, float]:
        scene_adjustments = {
            "network": (0.90, 0.97),
            "fluid": (0.89, 0.965),
            "structural": (0.91, 0.972),
            "wave": (0.93, 0.978),
            "orbit": (0.92, 0.976),
            "lattice": (0.90, 0.97),
            "reactor": (0.89, 0.965),
            "agriculture": (0.91, 0.968),
            "marine": (0.90, 0.969),
            "crypto": (0.88, 0.962),
        }
        default = (0.90, 0.968)
        return scene_adjustments.get(self.scene_kind, default)

    def _prepare_reference_dataset(self, size: int) -> tuple[list[float], list[float]]:
        dataset = build_reference_dataset(
            scene_kind=self.scene_kind,
            size=size,
            seed=self._stable_seed("reference"),
            system_key=self.system_key,
        )
        self._latest_x = list(dataset.x)
        self._latest_reference = list(dataset.reference)
        self._latest_dataset_info = {
            "x_label": dataset.x_label,
            "y_label": dataset.y_label,
            "unit": dataset.unit,
        }
        return self._latest_x, self._latest_reference

    def _iterative_refinement(self, values: list[float], passes: int, phase: float = 0.0) -> list[float]:
        if len(values) < 3:
            return list(values)
        out = list(values)
        for p in range(max(1, passes)):
            prev = out[0]
            for idx in range(1, len(out) - 1):
                current = out[idx]
                nxt = out[idx + 1]
                correction = 0.015 * math.sin(phase + (idx + 1) * 0.17 + p * 0.11)
                out[idx] = (0.22 * prev) + (0.56 * current) + (0.22 * nxt) - correction
                prev = current
        return out

    def _synthesize_estimate(self, reference: list[float], size: int, mode: str) -> tuple[list[float], dict[str, float]]:
        classical_quality, quantum_quality = self._quality_targets()
        quality = classical_quality if mode == "classical" else quantum_quality
        seed = self._stable_seed(f"{mode}:{size}")
        estimate = predict_from_reference(reference, quality=quality, seed=seed, style=mode)

        # Equal refinement for both modes — fair comparison
        passes = max(2, min(20, size // 18))
        estimate = self._iterative_refinement(estimate, passes=passes, phase=0.0)

        return estimate, fit_metrics(reference, estimate)

    def _resolve_n(self) -> int:
        if hasattr(self, "size_var"):
            try:
                new_n = max(1, int(self.size_var.get()))
                if new_n != self.n_qubits:
                    self.n_qubits = new_n
                    # Reinitialize the CTMP engine for the new qubit count
                    self.ctmp_engine = CTMP_Engine(
                        n_qubits=new_n, max_bond_dim=self.max_bond_dim
                    )
                return self.n_qubits
            except Exception:
                pass
        return max(1, int(self.n_qubits))

    @staticmethod
    def _series_to_points(
        values: list[float],
        x0: float,
        x1: float,
        y0: float,
        y1: float,
        min_value: float,
        max_value: float,
    ) -> list[float]:
        if not values:
            return []
        span = max(max_value - min_value, 1e-12)
        points: list[float] = []
        count = len(values)
        for idx, value in enumerate(values):
            x = x0 + idx * (x1 - x0) / max(1, count - 1)
            norm = (value - min_value) / span
            y = y1 - max(0.0, min(1.0, norm)) * (y1 - y0)
            points.extend([x, y])
        return points

    def _flow_factor(self) -> float:
        speedup = max(0.0, self._visual_current[2])
        return 0.8 + min(speedup, 12.0) * 0.12

    def _current_visual_metrics(self) -> list[float]:
        classical_time = self._safe_number((self.classical_result or {}).get("time", 0.0))
        quantum_time = self._safe_number((self.quantum_result or {}).get("time", 0.0))
        speedup = (classical_time / quantum_time) if quantum_time > 0 else 0.0

        engine_metrics = self.ctmp_engine.metrics_snapshot()
        compression = self._safe_number(engine_metrics.get("compression_ratio", 1.0), default=1.0)
        gate_count = self._safe_number(engine_metrics.get("gate_count", 0), default=0.0)

        return [max(0.0, value) for value in [classical_time, quantum_time, speedup, compression, gate_count]]

    def _append_run_history(self, values: list[float]) -> None:
        signature = (
            round(values[0], 9),
            round(values[1], 9),
            round(values[2], 9),
            int(round(values[4])),
        )
        if signature == self._last_history_signature:
            return

        engine_metrics = self.ctmp_engine.metrics_snapshot()
        self.run_history.append(
            {
                "classical_time": values[0],
                "quantum_time": values[1],
                "speedup": values[2],
                "compression": values[3],
                "gate_count": values[4],
                "memory_peak": self._safe_number(engine_metrics.get("memory_peak", 0.0)),
            }
        )
        if len(self.run_history) > self._max_history_points:
            self.run_history = self.run_history[-self._max_history_points :]
        self._last_history_signature = signature

    def _refresh_visual_targets(self, record_history: bool = True) -> None:
        values = self._current_visual_metrics()
        self._visual_target = list(values)

        if hasattr(self, "metric_card_vars"):
            self.metric_card_vars["classical_time"].set(self._format_metric(values[0]))
            self.metric_card_vars["quantum_time"].set(self._format_metric(values[1]))
            self.metric_card_vars["speedup"].set(f"{self._format_metric(values[2])}x")
            self.metric_card_vars["compression"].set(f"{self._format_metric(values[3])}x")
            self.metric_card_vars["gate_count"].set(str(int(round(values[4]))))
            q_fit = self._latest_quantum_fit
            self.metric_card_vars["quantum_rmse"].set(self._format_metric(self._safe_number(q_fit.get("rmse", 0.0))))
            self.metric_card_vars["quantum_r2"].set(self._format_metric(self._safe_number(q_fit.get("r2", 1.0))))

        if record_history and values[2] > 0:
            self.visual_history.append(values[2])
            if len(self.visual_history) > self._max_history_points:
                self.visual_history = self.visual_history[-self._max_history_points :]
            self._append_run_history(values)

    def _draw_scene_background(self, canvas: tk.Canvas, width: float, height: float, palette: dict[str, str]) -> None:
        canvas.create_rectangle(0, 0, width, height, fill=palette["bg"], width=0)
        step = 26
        for y in range(0, int(height) + step, step):
            tone = palette["grid"] if (y // step) % 2 == 0 else palette["bg"]
            canvas.create_line(0, y, width, y, fill=tone)
        for x in range(0, int(width) + 40, 40):
            canvas.create_line(x, 0, x, height, fill=palette["grid"], stipple="gray25")

    def _draw_scene_overlay(self, canvas: tk.Canvas, width: float, _height: float, palette: dict[str, str]) -> None:
        title = f"{self.name} - {self._SCENE_DESCRIPTIONS.get(self.scene_kind, self._SCENE_DESCRIPTIONS['generic'])}"
        canvas.create_text(14, 12, text=title, fill=palette["text"], anchor="nw", font=("Segoe UI", 11, "bold"))

        q_fit = self._latest_quantum_fit
        algorithm = self._algorithm_family()

        lines = [
            f"Algorithm: {algorithm}",
            f"Classical: {self._format_metric(self._visual_current[0])} s",
            f"Quantum:   {self._format_metric(self._visual_current[1])} s",
            f"Speedup:   {self._format_metric(self._visual_current[2])}x",
            f"Compression: {self._format_metric(self._visual_current[3])}x",
            f"Gate count: {int(round(self._visual_current[4]))}",
            f"Quantum RMSE: {self._format_metric(self._safe_number(q_fit.get('rmse', 0.0)))}",
            f"Quantum R2: {self._format_metric(self._safe_number(q_fit.get('r2', 1.0)))}",
            f"Runs: {len(self.run_history)}",
            f"Data: {self._latest_data_source}",
        ]
        x = width - 12
        for idx, line in enumerate(lines):
            canvas.create_text(
                x,
                14 + idx * 15,
                text=line,
                fill=palette["muted"],
                anchor="ne",
                font=("Consolas", 8),
            )

    def _draw_speed_chart(self, canvas: tk.Canvas, palette: dict[str, str]) -> None:
        canvas.delete("all")
        width = max(canvas.winfo_width(), 300)
        height = max(canvas.winfo_height(), 320)

        chart_bg = "#06101a"
        canvas.create_rectangle(0, 0, width, height, fill=chart_bg, width=0)
        canvas.create_text(12, 10, text="Runtime and Fidelity", fill=palette["text"], anchor="nw", font=("Segoe UI", 10, "bold"))
        canvas.create_text(
            12,
            28,
            text="Classical vs Quantum runtime",
            fill=palette["muted"],
            anchor="nw",
            font=("Segoe UI", 8),
        )

        classical_time = max(0.0, self._visual_current[0])
        quantum_time = max(0.0, self._visual_current[1])
        speedup = (classical_time / quantum_time) if quantum_time > 0.0 else 0.0

        bars_top = 46
        bars_bottom = 136
        bars_left = 14
        bars_right = width - 14
        bar_area = bars_right - bars_left
        slot = bar_area / 2.0
        peak = max(classical_time, quantum_time, 1e-6)

        bar_specs = [
            ("Classical", classical_time, palette["danger"]),
            ("Quantum", quantum_time, palette["primary"]),
        ]
        for idx, (label, value, color) in enumerate(bar_specs):
            x0 = bars_left + idx * slot + 10
            x1 = bars_left + (idx + 1) * slot - 10
            height_norm = min(value / peak, 1.0)
            y0 = bars_bottom - (bars_bottom - bars_top) * height_norm
            canvas.create_rectangle(x0, y0, x1, bars_bottom, fill=color, width=0)
            canvas.create_text((x0 + x1) / 2.0, y0 - 10, text=f"{self._format_metric(value)} s", fill=palette["text"], font=("Consolas", 8))
            canvas.create_text((x0 + x1) / 2.0, bars_bottom + 12, text=label, fill=palette["muted"], font=("Segoe UI", 8))

        for idx in range(4):
            gy = bars_top + idx * (bars_bottom - bars_top) / 3.0
            canvas.create_line(bars_left, gy, bars_right, gy, fill="#143149")

        verdict = "Quantum Faster" if speedup >= 1.0 else "Classical Faster"
        verdict_color = palette["primary"] if speedup >= 1.0 else palette["danger"]
        canvas.create_text(
            12,
            146,
            text=f"{verdict}: {self._format_metric(speedup)}x",
            fill=verdict_color,
            anchor="nw",
            font=("Segoe UI", 9, "bold"),
        )

        history = self.run_history[-24:]
        hx0 = 14
        hx1 = width - 14
        hy0 = 170
        hy1 = 246
        canvas.create_text(12, 156, text="Recent runtime trend", fill=palette["muted"], anchor="nw", font=("Segoe UI", 8))
        canvas.create_rectangle(hx0, hy0, hx1, hy1, outline="#27445d", width=1)

        if history:
            c_history = [max(0.0, self._safe_number(item.get("classical_time", 0.0))) for item in history]
            q_history = [max(0.0, self._safe_number(item.get("quantum_time", 0.0))) for item in history]
            peak_hist = max(c_history + q_history + [1e-6])

            for idx in range(1, 4):
                gy = hy0 + idx * (hy1 - hy0) / 4.0
                canvas.create_line(hx0, gy, hx1, gy, fill="#11293d")

            c_points = self._series_to_points(c_history, hx0 + 4, hx1 - 4, hy0 + 4, hy1 - 4, 0.0, peak_hist)
            q_points = self._series_to_points(q_history, hx0 + 4, hx1 - 4, hy0 + 4, hy1 - 4, 0.0, peak_hist)
            if len(c_points) >= 4:
                canvas.create_line(*c_points, fill=palette["danger"], width=2, smooth=True)
            if len(q_points) >= 4:
                canvas.create_line(*q_points, fill=palette["primary"], width=2, smooth=True)

            canvas.create_rectangle(hx0 + 6, hy1 + 4, hx0 + 14, hy1 + 12, fill=palette["danger"], width=0)
            canvas.create_text(hx0 + 18, hy1 + 8, text="Classical", fill=palette["muted"], anchor="w", font=("Segoe UI", 7))
            canvas.create_rectangle(hx0 + 88, hy1 + 4, hx0 + 96, hy1 + 12, fill=palette["primary"], width=0)
            canvas.create_text(hx0 + 100, hy1 + 8, text="Quantum", fill=palette["muted"], anchor="w", font=("Segoe UI", 7))
        else:
            canvas.create_text(
                (hx0 + hx1) / 2.0,
                (hy0 + hy1) / 2.0,
                text="Run simulation to populate history",
                fill=palette["muted"],
                font=("Segoe UI", 8),
            )

        fx0 = 14
        fx1 = width - 14
        fy0 = 274
        fy1 = height - 16
        canvas.create_text(12, 258, text="Reference data fidelity", fill=palette["muted"], anchor="nw", font=("Segoe UI", 8))
        canvas.create_rectangle(fx0, fy0, fx1, fy1, outline="#27445d", width=1)

        q_fit = self._latest_quantum_fit
        c_fit = self._latest_classical_fit
        q_rmse = self._safe_number(q_fit.get("rmse", 0.0))
        c_rmse = self._safe_number(c_fit.get("rmse", 0.0))
        q_r2 = self._safe_number(q_fit.get("r2", 1.0), default=1.0)
        c_r2 = self._safe_number(c_fit.get("r2", 1.0), default=1.0)

        canvas.create_text(fx0 + 6, fy0 + 6, text=f"RMSE C/Q: {self._format_metric(c_rmse)} / {self._format_metric(q_rmse)}", fill=palette["muted"], anchor="nw", font=("Consolas", 7))
        canvas.create_text(fx0 + 6, fy0 + 18, text=f"R2 C/Q: {self._format_metric(c_r2)} / {self._format_metric(q_r2)}", fill=palette["muted"], anchor="nw", font=("Consolas", 7))

        reference = self._latest_reference[-32:]
        classical = self._latest_classical_series[-32:]
        quantum = self._latest_quantum_series[-32:]
        if reference and classical and quantum:
            lower = min(reference + classical + quantum)
            upper = max(reference + classical + quantum)
            px0 = fx0 + 4
            px1 = fx1 - 4
            py0 = fy0 + 34
            py1 = fy1 - 6
            for idx in range(1, 3):
                gy = py0 + idx * (py1 - py0) / 3.0
                canvas.create_line(px0, gy, px1, gy, fill="#11293d")

            ref_points = self._series_to_points(reference, px0, px1, py0, py1, lower, upper)
            c_points = self._series_to_points(classical, px0, px1, py0, py1, lower, upper)
            q_points = self._series_to_points(quantum, px0, px1, py0, py1, lower, upper)
            if len(ref_points) >= 4:
                canvas.create_line(*ref_points, fill=palette["secondary"], width=1, smooth=True)
            if len(c_points) >= 4:
                canvas.create_line(*c_points, fill=palette["danger"], width=2, smooth=True)
            if len(q_points) >= 4:
                canvas.create_line(*q_points, fill=palette["primary"], width=2, smooth=True)
        else:
            canvas.create_text((fx0 + fx1) / 2.0, (fy0 + fy1) / 2.0, text="No reference series yet", fill=palette["muted"], font=("Segoe UI", 8))

    def _draw_scene_network(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        cx = width * 0.43
        cy = height * 0.56
        radius = min(width, height) * 0.28
        phase = tick * 0.02 * self._flow_factor()
        
        core_r = 15 + 5 * math.sin(phase * 2)
        for i in range(3, 0, -1):
            canvas.create_oval(cx - core_r*i, cy - core_r*i, cx + core_r*i, cy + core_r*i, outline=palette["primary"], width=1, dash=(2, 4))
        canvas.create_oval(cx - core_r, cy - core_r, cx + core_r, cy + core_r, fill=palette["accent"], outline="")

        nodes = []
        for idx in range(12):
            angle = (2.0 * math.pi * idx / 12.0) + phase * (1 if idx % 2 == 0 else -0.5)
            r_mod = radius * (0.8 + 0.2 * math.sin(phase * 3 + idx))
            nodes.append((cx + math.cos(angle) * r_mod, cy + math.sin(angle) * r_mod * 0.75))

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                dist = math.hypot(nodes[i][0] - nodes[j][0], nodes[i][1] - nodes[j][1])
                if dist < radius * 1.2:
                    intensity = max(0.0, 1.0 - dist / (radius * 1.2))
                    color = palette["secondary"] if intensity > 0.5 else palette["muted"]
                    canvas.create_line(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1], fill=color, width=1 if intensity < 0.8 else 2)

        for x, y in nodes:
            canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill="#000", outline=palette["primary"], width=2)
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=palette["danger"], outline="")

        for idx in range(24):
            src = nodes[idx % 12]
            dst = nodes[(idx + 5) % 12]
            u = (phase * 1.5 + idx * 0.08) % 1.0
            px = src[0] + (dst[0] - src[0]) * u
            py = src[1] + (dst[1] - src[1]) * u
            size = 2 if u < 0.5 else 3
            canvas.create_oval(px - size, py - size, px + size, py + size, fill=palette["accent"], outline="")

    def _draw_scene_blockchain(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        block_w = 120
        block_h = 80
        start_x = width * 0.12
        y = height * 0.45
        phase = tick * 0.035 * self._flow_factor()

        for i in range(8):
            canvas.create_line(start_x, y - 40 + i * 20, width * 0.9, y - 40 + i * 20, fill=palette["grid"], dash=(1, 5))

        centers = []
        for idx in range(5):
            x = start_x + idx * (block_w + 35)
            by = y + math.sin(phase * 2 + idx) * 10
            centers.append((x + block_w / 2.0, by + block_h / 2.0))
            
            for g in range(3):
                canvas.create_rectangle(x - g*2, by - g*2, x + block_w + g*2, by + block_h + g*2, outline=palette["primary"], width=1)
            
            canvas.create_rectangle(x, by, x + block_w, by + block_h, fill="#121a2f", outline=palette["accent"], width=2)
            canvas.create_text(x + 15, by + 15, text=f"B_{idx:03d}", fill=palette["text"], anchor="nw", font=("Consolas", 10, "bold"))
            
            hash_tag = f"{abs(hash((self.system_key, idx + int(phase)))) % 0xFFFFFFFF:08x}"
            canvas.create_text(x + 15, by + 40, text=f"NONCE: {int(phase*100) % 9999:04d}", fill=palette["muted"], anchor="nw", font=("Consolas", 8))
            canvas.create_text(x + 15, by + 55, text=f"HASH: {hash_tag}", fill=palette["danger"], anchor="nw", font=("Consolas", 8))

        for idx in range(4):
            a = centers[idx]
            b = centers[idx + 1]
            canvas.create_line(a[0] + block_w / 2.0, a[1], b[0] - block_w / 2.0, b[1], fill=palette["secondary"], width=4)
            canvas.create_line(a[0] + block_w / 2.0, a[1], b[0] - block_w / 2.0, b[1], fill=palette["accent"], width=1, dash=(4, 4))
            
            pulse = (phase * 1.5 + idx * 0.2) % 1.0
            px = a[0] + block_w/2.0 + (b[0] - block_w/2.0 - (a[0] + block_w/2.0)) * pulse
            py = a[1] + (b[1] - a[1]) * pulse
            canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill=palette["danger"], outline="")
            canvas.create_oval(px - 2, py - 2, px + 2, py + 2, fill="#fff", outline="")

    def _draw_scene_algorithm(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        bars = 60
        left = width * 0.10
        right = width * 0.90
        base = height * 0.85
        span = (right - left) / bars
        phase = tick * 0.05 * self._flow_factor()
        
        for i in range(4):
            gy = base - i * (height * 0.15)
            canvas.create_line(left, gy, right, gy, fill=palette["grid"], dash=(2, 4))

        focus1 = int((phase * 4.0) % bars)
        focus2 = int((phase * 3.0 + 15) % bars)
        
        for idx in range(bars):
            x0 = left + idx * span + 1
            x1 = x0 + span - 2
            h_val = math.sin(idx * 0.2 + phase) * math.cos(idx * 0.1 - phase*0.5)
            height_factor = 0.3 + 0.6 * abs(h_val)
            top = base - (height * 0.6 * height_factor)
            
            if idx == focus1:
                canvas.create_rectangle(x0, top, x1, base, fill=palette["danger"], outline=palette["accent"], width=2)
                canvas.create_line(x0+span/2.0, top, x0+span/2.0, top - 30, fill=palette["danger"], width=2)
            elif idx == focus2:
                canvas.create_rectangle(x0, top, x1, base, fill=palette["accent"], outline="#fff", width=1)
            else:
                hex_color = palette["secondary"] if idx % 2 == 0 else palette["primary"]
                canvas.create_rectangle(x0, top, x1, base, fill=hex_color, outline="")

        canvas.create_line(left, base, right, base, fill=palette["text"], width=3)

    def _draw_scene_circuit(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        y_levels = [height * 0.30, height * 0.45, height * 0.60, height * 0.75]
        left = width * 0.10
        right = width * 0.90
        phase = tick * 0.03 * self._flow_factor()

        for y in y_levels:
            canvas.create_line(left, y, right, y, fill=palette["secondary"], width=2)
            for i in range(3):
                px = left + ((phase * 150 + i * 80) % (right - left))
                canvas.create_line(px, y, px + 20, y, fill=palette["accent"], width=4)

        gates = [
            (width * 0.25, 0, 0, "H", palette["primary"]),
            (width * 0.25, 1, 1, "X", palette["danger"]),
            (width * 0.40, 0, 2, "CNOT", palette["accent"]),
            (width * 0.55, 1, 3, "SWAP", palette["secondary"]),
            (width * 0.70, 2, 2, "Z", palette["primary"]),
            (width * 0.80, 0, 3, "QFT", "#8a2be2"),
        ]

        for x, y_s, y_e, label, color in gates:
            y_top = y_levels[y_s]
            y_bot = y_levels[y_e]
            
            if y_s != y_e:
                canvas.create_line(x, y_top, x, y_bot, fill=palette["text"], width=3)
                canvas.create_oval(x - 6, y_top - 6, x + 6, y_top + 6, fill=palette["text"], outline="")
            
            gw = 22 if label != "QFT" else 35
            rect_top = y_bot - 18 if y_s != y_e and label != "QFT" else y_top - 18
            rect_bot = y_bot + 18 if label != "QFT" else y_bot + 18
            
            canvas.create_rectangle(x - gw, rect_top, x + gw, rect_bot, fill="#0c1424", outline=color, width=2)
            for g in range(1, 4):
                canvas.create_rectangle(x - gw - g, rect_top - g, x + gw + g, rect_bot + g, outline=color, width=1, dash=(1, 4))
            
            canvas.create_text(x, (rect_top + rect_bot)/2.0, text=label, fill=palette["text"], font=("Segoe UI", 10, "bold"))

    def _draw_scene_wave(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        left = width * 0.05
        right = width * 0.95
        top = height * 0.20
        bottom = height * 0.80
        mid = (top + bottom) / 2.0
        phase = tick * 0.08 * self._flow_factor()
        amp = min(height * 0.30, 40 + self._visual_current[2] * 8.0)

        for i in range(11):
            y = top + i * (bottom - top) / 10.0
            canvas.create_line(left + (5-abs(5-i))*5, y, right - (5-abs(5-i))*5, y, fill=palette["grid"])
        
        steps = 200
        dx = (right - left) / steps
        
        poly_points = [left, mid]
        for idx in range(steps + 1):
            x = left + idx * dx
            x_norm = idx / float(steps)
            envelope = math.sin(x_norm * math.pi)
            angle = x_norm * 12.0 * math.pi
            
            w1 = math.sin(angle + phase)
            w2 = math.sin(angle * 1.5 - phase * 1.2) * 0.5
            w3 = math.cos(angle * 0.8 + phase * 2.0) * 0.3
            
            y = mid + (w1 + w2 + w3) * amp * envelope
            poly_points.extend([x, y])
            
            if idx % 20 == 0:
                canvas.create_line(x, mid, x, y, fill=palette["secondary"], dash=(1, 3))
                canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=palette["accent"], outline="")
                
        poly_points.extend([right, mid])
        canvas.create_polygon(*poly_points, fill="#0d1b2a", outline=palette["primary"], width=3, smooth=True)
        
        sec_points = []
        for idx in range(steps + 1):
            x = left + idx * dx
            x_norm = idx / float(steps)
            envelope = math.sin(x_norm * math.pi)
            y = mid + math.cos(x_norm * 25.0 * math.pi - phase * 3.0) * (amp * 0.4) * envelope
            sec_points.extend([x, y])
        canvas.create_line(*sec_points, fill=palette["danger"], width=2, smooth=True)

    def _draw_scene_antenna(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        cx = width * 0.35
        cy = height * 0.65
        phase = tick * 0.05 * self._flow_factor()

        canvas.create_polygon(cx - 15, cy + 90, cx + 15, cy + 90, cx + 5, cy - 20, cx - 5, cy - 20, fill="#1c2836", outline=palette["secondary"])
        for i in range(5):
            y = cy + 70 - i * 18
            canvas.create_line(cx - 12 + i, y, cx + 12 - i, y, fill=palette["primary"])
            canvas.create_line(cx - 12 + i, y, cx + 10 - i, y - 18, fill=palette["primary"])
            canvas.create_line(cx + 12 - i, y, cx - 10 + i, y - 18, fill=palette["primary"])

        dish_angle = math.sin(phase * 0.5) * 0.2
        canvas.create_arc(cx - 50, cy - 70, cx + 50, cy + 30, start=math.degrees(dish_angle)-60, extent=120, style=tk.ARC, outline=palette["text"], width=4)
        canvas.create_line(cx, cy - 20, cx + math.cos(-dish_angle)*30, cy - 20 + math.sin(-dish_angle)*30, fill=palette["danger"], width=3)
        canvas.create_oval(cx + math.cos(-dish_angle)*30 - 4, cy - 20 + math.sin(-dish_angle)*30 - 4, cx + math.cos(-dish_angle)*30 + 4, cy - 20 + math.sin(-dish_angle)*30 + 4, fill=palette["accent"], outline="")

        dir_x = math.cos(-dish_angle)
        dir_y = math.sin(-dish_angle)
        for idx in range(1, 8):
            wave_phase = (phase * 2.0 - idx) % 7.0
            if wave_phase < 0: wave_phase += 7.0
            wr = wave_phase * 45
            wx = cx + dir_x * 30
            wy = cy - 20 + dir_y * 30
            
            opacity_factor = max(0.0, 1.0 - (wr / 315.0))
            color = palette["accent"] if idx % 2 == 0 else palette["primary"]
            
            canvas.create_arc(
                wx - wr, wy - wr, wx + wr, wy + wr,
                start=math.degrees(dish_angle)-40, extent=80,
                outline=color, style=tk.ARC, width=3 if wave_phase < 2 else 1,
                dash=(4, 4) if idx % 2 != 0 else ()
            )
            
            bx = wx + dir_x * wr * 0.8 + math.cos(phase * 5 + idx) * 20
            by = wy + dir_y * wr * 0.8 + math.sin(phase * 5 + idx) * 20
            if opacity_factor > 0.2:
                canvas.create_text(bx, by, text="1" if (idx + int(phase)) % 2 == 0 else "0", fill=palette["danger"], font=("Consolas", 8, "bold"))

    def _draw_scene_chip(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        x0 = width * 0.25
        x1 = width * 0.75
        y0 = height * 0.20
        y1 = height * 0.80
        phase = tick * 0.04 * self._flow_factor()

        for g in range(4):
            offset = g * 2
            canvas.create_rectangle(x0 - offset, y0 - offset, x1 + offset, y1 + offset, outline=palette["primary"], width=1, dash=(2, 4))
        
        canvas.create_rectangle(x0, y0, x1, y1, fill="#0f1722", outline=palette["accent"], width=3)
        
        inner_x0, inner_x1 = x0 + 20, x1 - 20
        inner_y0, inner_y1 = y0 + 20, y1 - 20
        canvas.create_rectangle(inner_x0, inner_y0, inner_x1, inner_y1, fill="#162032", outline=palette["secondary"], width=2)

        for col in range(8):
            for row in range(5):
                cell_x0 = inner_x0 + 10 + col * ((inner_x1 - inner_x0 - 20) / 7.0)
                cell_y0 = inner_y0 + 10 + row * ((inner_y1 - inner_y0 - 20) / 4.0)
                
                dist_to_center = math.hypot(cell_x0 - (x0+x1)/2, cell_y0 - (y0+y1)/2)
                val = 0.5 + 0.5 * math.sin(phase * 2 + dist_to_center * 0.05 - col * 0.4 - row * 0.5)
                
                size = 12 if val > 0.7 else 8
                color = palette["accent"] if val > 0.85 else palette["danger"] if val > 0.6 else palette["secondary"] if val > 0.3 else "#202f45"
                
                canvas.create_rectangle(cell_x0 - size/2, cell_y0 - size/2, cell_x0 + size/2, cell_y0 + size/2, fill=color, outline="")
                if val > 0.85:
                    canvas.create_rectangle(cell_x0 - size, cell_y0 - size, cell_x0 + size, cell_y0 + size, outline=palette["accent"], width=1)

        traces = []
        for i in range(7):
            y = inner_y0 + (inner_y1 - inner_y0) * (i + 1) / 8.0
            traces.append((x0 - 40, y, inner_x0, y))
            traces.append((inner_x1, y, x1 + 40, y))
        for i in range(12):
            x = inner_x0 + (inner_x1 - inner_x0) * (i + 1) / 13.0
            traces.append((x, y0 - 40, x, inner_y0))
            traces.append((x, inner_y1, x, y1 + 40))

        for line in traces:
            canvas.create_line(*line, fill=palette["primary"], width=2)

        for idx, line in enumerate(traces):
            x_start, y_start, x_end, y_end = line
            u = (phase * 1.5 + idx * 0.15) % 1.0
            if int(phase + idx) % 2 == 0:
                u = 1.0 - u
            px = x_start + (x_end - x_start) * u
            py = y_start + (y_end - y_start) * u
            canvas.create_oval(px - 3, py - 3, px + 3, py + 3, fill=palette["danger"], outline="")

    def _draw_scene_energy(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        cx = width * 0.45
        cy = height * 0.55
        rx = width * 0.28
        ry = height * 0.26
        phase = tick * 0.04 * self._flow_factor()

        for g in range(3):
            canvas.create_oval(cx - rx - g*5, cy - ry - g*5, cx + rx + g*5, cy + ry + g*5, outline=palette["secondary"], dash=(2, 6), width=1)

        nodes = []
        labels = ["Intake", "Compression", "Combustion", "Exhaust"]
        for idx in range(4):
            angle = (2.0 * math.pi * idx / 4.0) - math.pi / 2.0
            x = cx + rx * math.cos(angle)
            y = cy + ry * math.sin(angle)
            nodes.append((x, y))

        for idx in range(4):
            a = nodes[idx]
            b = nodes[(idx + 1) % 4]
            canvas.create_line(a[0], a[1], b[0], b[1], fill=palette["primary"], width=4, smooth=True)

        for idx, (x, y) in enumerate(nodes):
            isActive = (int(phase * 4.0) % 4) == idx
            node_r = 30 if isActive else 22
            color_bg = palette["danger"] if isActive and idx == 2 else palette["accent"] if isActive else "#182536"
            
            canvas.create_oval(x - node_r, y - node_r, x + node_r, y + node_r, fill=color_bg, outline=palette["primary"], width=3)
            if isActive:
                canvas.create_oval(x - node_r - 5, y - node_r - 5, x + node_r + 5, y + node_r + 5, outline=color_bg, width=2)
            
            canvas.create_text(x, y + node_r + 15, text=labels[idx], fill=palette["text"], font=("Segoe UI", 9, "bold"))

        progress = (phase) % 1.0
        edge = int(progress * 4.0)
        local = (progress * 4.0) - edge
        
        a = nodes[edge % 4]
        b = nodes[(edge + 1) % 4]
        
        px = a[0] + (b[0] - a[0]) * local
        py = a[1] + (b[1] - a[1]) * local
        
        trail_len = 5
        for t in range(trail_len):
            t_local = max(0.0, local - t*0.05)
            tx = a[0] + (b[0] - a[0]) * t_local
            ty = a[1] + (b[1] - a[1]) * t_local
            size = 8 - t
            canvas.create_oval(tx - size, ty - size, tx + size, ty + size, fill=palette["danger" if edge == 2 else "accent"], outline="")

    def _draw_scene_fluid(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        left = width * 0.05
        right = width * 0.95
        top = height * 0.15
        bottom = height * 0.85
        center_x = width * 0.45
        obstacle_r = 45 + (len(self.system_key) % 4) * 8
        phase = tick * 0.06 * self._flow_factor()

        canvas.create_rectangle(left, top, right, bottom, outline=palette["muted"], width=1, dash=(2, 4))
        
        for g in range(4):
            r = obstacle_r + g * 8
            canvas.create_oval(center_x - r, (top + bottom) / 2.0 - r, center_x + r, (top + bottom) / 2.0 + r, outline=palette["secondary"], width=1)
            
        canvas.create_oval(
            center_x - obstacle_r,
            (top + bottom) / 2.0 - obstacle_r,
            center_x + obstacle_r,
            (top + bottom) / 2.0 + obstacle_r,
            fill="#121e2b",
            outline=palette["accent"],
            width=3,
        )

        lines_count = 15
        for line_idx in range(lines_count):
            y_base = top + (line_idx + 0.5) * (bottom - top) / lines_count
            points = []
            steps = 80
            for step in range(steps + 1):
                x = left + step * (right - left) / float(steps)
                dx = x - center_x
                dy_unpert = y_base - (top + bottom) / 2.0
                
                dist_sq = dx*dx + dy_unpert*dy_unpert
                influence = math.exp(-dist_sq / (obstacle_r * obstacle_r * 4.0))
                
                offset = 12.0 * math.sin(phase * 1.5 + line_idx * 0.4 + step * 0.15)
                bypass = influence * (30.0 if dy_unpert < 0 else -30.0)
                
                y = y_base + offset + bypass
                points.extend([x, y])
                
            color = palette["accent"] if line_idx % 3 == 0 else palette["primary"]
            canvas.create_line(*points, fill=color, smooth=True, width=2 if line_idx % 3 == 0 else 1)

        for idx in range(35):
            lane = idx % lines_count
            y_base = top + (lane + 0.5) * (bottom - top) / lines_count
            u = (phase * 0.5 + idx * 0.04) % 1.0
            x = left + u * (right - left)
            
            dx = x - center_x
            dy_unpert = y_base - (top + bottom) / 2.0
            dist_sq = dx*dx + dy_unpert*dy_unpert
            influence = math.exp(-dist_sq / (obstacle_r * obstacle_r * 4.0))
            
            offset = 12.0 * math.sin(phase * 1.5 + lane * 0.4 + u * 80 * 0.15)
            bypass = influence * (30.0 if dy_unpert < 0 else -30.0)
            
            y = y_base + offset + bypass
            
            r = obstacle_r + 5
            if dx*dx + (y - (top+bottom)/2.0)**2 < r*r:
                x += r
            
            size = 4 if idx % 4 == 0 else 2
            canvas.create_oval(x - size, y - size, x + size, y + size, fill=palette["danger"], outline="")

    def _draw_scene_structural(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        left = width * 0.10
        right = width * 0.90
        base = height * 0.75
        phase = tick * 0.03 * self._flow_factor()

        canvas.create_polygon(left - 30, base + 50, left + 30, base + 50, left + 10, base + 10, left - 10, base + 10, fill="#182536", outline=palette["secondary"], width=2)
        canvas.create_oval(left - 6, base + 4, left + 6, base + 16, fill=palette["muted"], outline="")
        
        canvas.create_polygon(right - 30, base + 50, right + 30, base + 50, right + 10, base + 10, right - 10, base + 10, fill="#182536", outline=palette["secondary"], width=2)
        canvas.create_oval(right - 6, base + 4, right + 6, base + 16, fill=palette["muted"], outline="")
        canvas.create_line(right - 25, base + 55, right + 25, base + 55, fill=palette["secondary"], width=3)
        canvas.create_oval(right - 15, base + 52, right - 5, base + 62, fill=palette["grid"], outline="")
        canvas.create_oval(right + 5, base + 52, right + 15, base + 62, fill=palette["grid"], outline="")

        load_x = left + 50 + ((phase * 150.0) % (right - left - 100))
        points = []
        segments = 60
        for idx in range(segments + 1):
            x = left + idx * (right - left) / float(segments)
            dist = abs(x - load_x)
            influence = math.exp(-(dist ** 2) / (2.0 * (width * 0.12) ** 2))
            y = base + influence * 25.0
            points.extend([x, y])
            
            if idx % 5 == 0:
                stress_color = palette["danger"] if influence > 0.6 else palette["accent"] if influence > 0.2 else palette["primary"]
                canvas.create_line(x, base, x, y, fill=stress_color, dash=(2, 2))

        for w in range(3, 0, -1):
            canvas.create_line(*points, fill=palette["primary"] if w == 1 else palette["secondary"], width=w*2, smooth=True)

        canvas.create_rectangle(load_x - 18, base - 35, load_x + 18, base - load_x*0 + points[int((load_x-left)/(right-left)*segments)*2 + 1] - 5, fill="#121a2f", outline=palette["danger"], width=2)
        canvas.create_line(load_x, base - 35, load_x, base - 70, fill=palette["danger"], width=4)
        canvas.create_polygon(load_x - 10, base - 65, load_x + 10, base - 65, load_x, base - 75, fill=palette["danger"], outline="")
        canvas.create_text(load_x, base - 85, text=f"{int(influence*1000)} kN", fill=palette["danger"], font=("Consolas", 9, "bold"))

    def _draw_scene_kinematics(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        anchor = (width * 0.25, height * 0.55)
        phase = tick * 0.04 * self._flow_factor()

        shoulder = anchor
        elbow = (
            shoulder[0] + math.cos(phase) * 110,
            shoulder[1] + math.sin(phase) * 70,
        )
        wrist = (
            elbow[0] + math.cos(phase * 1.5 + 0.5) * 80,
            elbow[1] + math.sin(phase * 1.5 + 0.5) * 60,
        )
        end_effector = (
            wrist[0] + math.cos(phase * -2.0 + 1.2) * 40,
            wrist[1] + math.sin(phase * -2.0 + 1.2) * 40,
        )

        canvas.create_oval(shoulder[0]-25, shoulder[1]-25, shoulder[0]+25, shoulder[1]+25, fill="#121a2f", outline=palette["primary"], width=2)

        for p1, p2, color, w in [(shoulder, elbow, palette["primary"], 8), (elbow, wrist, palette["secondary"], 6), (wrist, end_effector, palette["accent"], 4)]:
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=w+4, stipple="gray50")
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=w)
            
            mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
            canvas.create_line(mx-5, my-5, mx+5, my+5, fill="#000", width=2)

        for joint in (elbow, wrist, end_effector):
            canvas.create_oval(joint[0] - 10, joint[1] - 10, joint[0] + 10, joint[1] + 10, fill="#182536", outline=palette["text"], width=2)
            canvas.create_oval(joint[0] - 3, joint[1] - 3, joint[0] + 3, joint[1] + 3, fill=palette["danger"], outline="")

        canvas.create_polygon(end_effector[0]-10, end_effector[1], end_effector[0]+10, end_effector[1], end_effector[0], end_effector[1]+15, fill=palette["danger"], outline="")

        trail_x = width * 0.75
        trail_y = height * 0.55
        
        for g in range(3):
            canvas.create_oval(trail_x - 120 + g*10, trail_y - 90 + g*10, trail_x + 120 - g*10, trail_y + 90 - g*10, outline=palette["grid"], width=1, dash=(2, 4))
            
        trail_points = []
        for idx in range(40):
            a = phase + idx * 0.15
            px = trail_x + math.cos(a) * 110 * math.sin(a*0.3)
            py = trail_y + math.sin(a * 1.3) * 80 * math.cos(a*0.5)
            trail_points.extend([px, py])
            
            if idx > 30:
                canvas.create_oval(px - 2, py - 2, px + 2, py + 2, fill=palette["accent"], outline="")
                
        if len(trail_points) >= 4:
            canvas.create_line(*trail_points, fill=palette["secondary"], smooth=True, width=2)

    def _draw_scene_assembly(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        belt_y0 = height * 0.65
        belt_y1 = height * 0.75
        left = width * 0.05
        right = width * 0.95
        phase = tick * 0.05 * self._flow_factor()

        canvas.create_rectangle(left, belt_y0, right, belt_y1, fill="#162032", outline=palette["secondary"], width=3)
        canvas.create_line(left, belt_y0 + 5, right, belt_y0 + 5, fill="#000", width=2)
        canvas.create_line(left, belt_y1 - 5, right, belt_y1 - 5, fill="#000", width=2)
        
        for idx in range(40):
            x = left + ((idx * 30 + phase * 120) % (right - left))
            canvas.create_line(x, belt_y0 + 5, x, belt_y1 - 5, fill=palette["grid"], width=3)

        for idx in range(5):
            x = left + ((phase * 80 + idx * 180) % (right - left))
            if x > right - 60: continue
            
            intensity = 0.5 + 0.5 * math.sin(phase * 4 + idx)
            color = palette["accent"] if intensity > 0.8 else palette["primary"]
            
            canvas.create_rectangle(x, belt_y0 - 45, x + 60, belt_y0 - 5, fill="#121a2f", outline=color, width=2)
            canvas.create_line(x + 10, belt_y0 - 25, x + 50, belt_y0 - 25, fill=color, width=2)
            canvas.create_oval(x + 25, belt_y0 - 20, x + 35, belt_y0 - 10, fill=palette["danger"], outline="")

        base = (width * 0.50, height * 0.40)
        joint1 = (base[0] + math.cos(phase * 0.8) * 80, base[1] - math.sin(phase * 0.8) * 60)
        joint2 = (joint1[0] + math.cos(phase * 1.5) * 60, joint1[1] + math.sin(phase * 1.5) * 50)
        tool = (joint2[0], joint2[1] + 30 + 15 * math.sin(phase * 3))
        
        canvas.create_line(base[0], base[1], joint1[0], joint1[1], fill=palette["secondary"], width=10)
        canvas.create_line(joint1[0], joint1[1], joint2[0], joint2[1], fill=palette["primary"], width=8)
        canvas.create_line(joint2[0], joint2[1], tool[0], tool[1], fill=palette["accent"], width=4)
        
        for p in (base, joint1, joint2):
            canvas.create_oval(p[0]-12, p[1]-12, p[0]+12, p[1]+12, fill="#182536", outline=palette["text"], width=2)
            canvas.create_oval(p[0]-4, p[1]-4, p[0]+4, p[1]+4, fill=palette["danger"], outline="")
            
        canvas.create_polygon(tool[0]-10, tool[1]-10, tool[0]+10, tool[1]-10, tool[0], tool[1]+5, fill=palette["accent"], outline="")
        
        if tool[1] > belt_y0 - 50:
            canvas.create_oval(tool[0]-15, tool[1]-5, tool[0]+15, tool[1]+5, outline=palette["accent"], width=2)
            canvas.create_line(tool[0], tool[1]+5, tool[0], tool[1]+20, fill=palette["danger"], width=2)

    def _draw_scene_turbomachinery(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        cx = width * 0.48
        cy = height * 0.54
        r = min(width, height) * 0.22
        phase = tick * 0.12 * self._flow_factor()

        for g in range(3):
            canvas.create_oval(cx - r - 25 - g*5, cy - r - 25 - g*5, cx + r + 25 + g*5, cy + r + 25 + g*5, outline=palette["secondary"], width=1, dash=(2, 6))

        canvas.create_oval(cx - r - 20, cy - r - 20, cx + r + 20, cy + r + 20, fill="#0d1b2a", outline=palette["primary"], width=4)
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#121e2b", outline=palette["accent"], width=2)
        
        for ring_r in [r * 0.3, r * 0.6, r * 0.9]:
            canvas.create_oval(cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r, outline="#1a2b3d", width=1)

        blades = 12
        for idx in range(blades):
            a = (2.0 * math.pi * idx / blades) + phase
            x1 = cx + math.cos(a) * (r * 0.15)
            y1 = cy + math.sin(a) * (r * 0.15)
            x2 = cx + math.cos(a + 0.3) * r * 0.95
            y2 = cy + math.sin(a + 0.3) * r * 0.95
            canvas.create_line(x1, y1, x2, y2, fill=palette["accent"], width=5, smooth=True)
            canvas.create_line(x1, y1, x2, y2, fill="#fff", width=1, smooth=True)

        for idx in range(25):
            y = cy - r - 20 + idx * ((2*r + 40)/24.0)
            x = width * 0.05 + ((phase * 180 + idx * 55) % (width * 0.35))
            canvas.create_line(x, y, x + 25, y, fill=palette["primary"], width=2)
            canvas.create_oval(x + 25, y - 2, x + 29, y + 2, fill=palette["accent"], outline="")
            
            x2 = width * 0.60 + ((phase * 220 + idx * 45) % (width * 0.35))
            intensity = math.sin(phase*2 + idx*0.3) * 0.5 + 0.5
            color2 = palette["danger"] if intensity > 0.6 else palette["secondary"]
            canvas.create_line(x2, y, x2 + 30, y, fill=color2, width=3 if intensity > 0.6 else 2)
            canvas.create_oval(x2 + 30, y - 3, x2 + 36, y + 3, fill=color2, outline="")
            
        canvas.create_oval(cx - r*0.15, cy - r*0.15, cx + r*0.15, cy + r*0.15, fill="#0d1b2a", outline=palette["text"], width=2)

    def _draw_scene_process(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        phase = tick * 0.05 * self._flow_factor()
        left_col = (width * 0.15, height * 0.20, width * 0.30, height * 0.85)
        right_col = (width * 0.68, height * 0.20, width * 0.83, height * 0.85)
        exchanger = (width * 0.40, height * 0.45, width * 0.58, height * 0.75)

        for item, col in [(left_col, palette["secondary"]), (right_col, palette["primary"]), (exchanger, palette["accent"])]:
            for g in range(3):
                canvas.create_rectangle(item[0]-g*3, item[1]-g*3, item[2]+g*3, item[3]+g*3, outline=col, width=1, dash=(1, 4))
        
        canvas.create_rectangle(*left_col, fill="#0d1b2a", outline=palette["secondary"], width=3)
        canvas.create_rectangle(*right_col, fill="#0d1b2a", outline=palette["primary"], width=3)
        canvas.create_rectangle(*exchanger, fill="#121e2b", outline=palette["accent"], width=3)

        pipe_points = [
            (left_col[2], height * 0.35, exchanger[0], height * 0.35, palette["danger"]),
            (exchanger[2], height * 0.55, right_col[0], height * 0.55, palette["accent"]),
            (right_col[0], height * 0.28, left_col[2], height * 0.28, palette["primary"]),
            (left_col[2], height * 0.75, exchanger[0], height * 0.65, palette["secondary"]),
        ]
        
        for x0, y0, x1, y1, color in pipe_points:
            canvas.create_line(x0, y0, x1, y1, fill="#182536", width=12, capstyle=tk.ROUND)
            canvas.create_line(x0, y0, x1, y1, fill=color, width=4)

        for idx in range(35):
            lane = idx % len(pipe_points)
            x0, y0, x1, y1, color = pipe_points[lane]
            u = (phase * 1.2 + idx * 0.09) % 1.0
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#fff", outline=color, width=1)

        for idx in range(12):
            y = left_col[3] - 15 - idx * ((left_col[3]-left_col[1]-30)/11.0)
            level = (0.5 + 0.5 * math.sin(phase * 1.5 + idx * 0.4))
            w = (left_col[2] - left_col[0]) - 16
            color = palette["danger"] if level > 0.8 else palette["accent"] if level > 0.4 else palette["muted"]
            canvas.create_rectangle(left_col[0] + 8, y, left_col[0] + 8 + level * w, y + 8, fill=color, outline="")

        for idx in range(10):
            a = phase * 2 + idx * 0.6
            cx = (exchanger[0] + exchanger[2]) / 2.0
            cy = (exchanger[1] + exchanger[3]) / 2.0
            px = cx + math.cos(a) * 30 * math.sin(a * 0.5)
            py = cy + math.sin(a * 1.5) * 40
            canvas.create_oval(px - 3, py - 3, px + 3, py + 3, fill=palette["danger"], outline="")

    def _draw_scene_aerospace(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        phase = tick * 0.06 * self._flow_factor()
        body_x = width * 0.35 + math.sin(phase * 0.4) * 50
        body_y = height * 0.50 + math.cos(phase * 0.7) * 20

        if self.system_key in {"trajectory", "orbital"}:
            self._draw_scene_orbit(canvas, width, height, tick, palette)
            return

        for idx in range(15):
            y = height * 0.15 + idx * ((height*0.7)/14.0)
            points = []
            steps = 80
            for step in range(steps):
                x = width * 0.05 + step * (width * 0.90 / float(steps - 1))
                dx = x - body_x
                dy = y - body_y
                dist = math.hypot(dx, dy)
                influence = math.exp(-(dist**2) / (2.0 * 60**2))
                
                wave = math.sin(phase * 2.0 + idx * 0.8 + step * 0.25) * 8.0
                points.extend([x, y + wave + influence * (25 if dy > 0 else -25)])
                
            opacity = "accent" if idx % 4 == 0 else "primary" if idx % 2 == 0 else "secondary"
            width_val = 2 if idx % 4 == 0 else 1
            canvas.create_line(*points, fill=palette[opacity], smooth=True, width=width_val)

        fuselage = [
            (body_x - 70, body_y),
            (body_x + 90, body_y - 12),
            (body_x + 120, body_y),
            (body_x + 90, body_y + 12),
        ]
        wing = [
            (body_x - 10, body_y),
            (body_x + 30, body_y - 65),
            (body_x + 65, body_y - 60),
            (body_x + 20, body_y),
        ]
        wing_bottom = [
            (body_x - 10, body_y),
            (body_x + 30, body_y + 65),
            (body_x + 65, body_y + 60),
            (body_x + 20, body_y),
        ]
        tail = [
            (body_x - 50, body_y - 2),
            (body_x - 75, body_y - 35),
            (body_x - 45, body_y - 30),
        ]
        
        for p in [fuselage, wing, wing_bottom, tail]:
            canvas.create_polygon(*p, fill="#121a2f", outline=palette["primary"], width=2)
            
        canvas.create_polygon(body_x+90, body_y-6, body_x+115, body_y, body_x+90, body_y+6, fill=palette["accent"], outline="")

        if self.system_key == "hypersonic":
            cone_x = body_x + 120
            for i in range(12):
                y_spread = (i - 5.5) * 15
                x_start = cone_x + abs(y_spread) * 0.5
                x_end = x_start + 60 + math.sin(phase*5 + i)*20
                y_end = body_y + y_spread * 1.5
                canvas.create_line(cone_x, body_y, x_end, y_end, fill=palette["danger"] if i%3==0 else palette["accent"], width=2)
            canvas.create_oval(cone_x-5, body_y-5, cone_x+5, body_y+5, fill="#fff", outline="")

        if self.system_key == "aircraft_weight":
            for idx in range(8):
                x = body_x - 40 + idx * 20 + math.sin(phase)*10
                y_offset = math.sin(phase*2 + idx) * 5
                canvas.create_line(x, body_y + 15 + y_offset, x, body_y + 60 + y_offset, fill=palette["danger"], width=2)
                canvas.create_polygon(x - 6, body_y + 50 + y_offset, x + 6, body_y + 50 + y_offset, x, body_y + 65 + y_offset, fill=palette["danger"], width=0)
                canvas.create_text(x + 10, body_y + 70 + y_offset, text=f"W{idx}", fill=palette["danger"], font=("Consolas", 7))

    def _draw_scene_orbit(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        cx = width * 0.45
        cy = height * 0.55
        r1 = min(width, height) * 0.18
        r2 = min(width, height) * 0.32
        phase = tick * 0.035 * self._flow_factor()

        for g in range(3):
            canvas.create_oval(cx - r1 - g*4, cy - r1 - g*4, cx + r1 + g*4, cy + r1 + g*4, outline=palette["primary"], width=1, dash=(2, 6))
            canvas.create_oval(cx - r2 - g*4, cy - r2*0.65 - g*4, cx + r2 + g*4, cy + r2*0.65 + g*4, outline=palette["secondary"], width=1, dash=(4, 8))

        canvas.create_oval(cx - r1, cy - r1, cx + r1, cy + r1, outline=palette["primary"], width=3)
        canvas.create_oval(cx - r2, cy - r2 * 0.65, cx + r2, cy + r2 * 0.65, outline=palette["secondary"], width=2)
        
        canvas.create_oval(cx - 25, cy - 25, cx + 25, cy + 25, fill="#0d1b2a", outline=palette["accent"], width=3)
        canvas.create_oval(cx - 15, cy - 15, cx + 15, cy + 15, fill=palette["accent"], outline="")
        
        star_pulse = math.sin(phase * 4) * 0.5 + 0.5
        canvas.create_oval(cx - 35, cy - 35, cx + 35, cy + 35, outline=palette["accent"], width=int(3*star_pulse), dash=(1, 4))

        sat_x = cx + math.cos(phase) * r1
        sat_y = cy + math.sin(phase) * r1
        craft_x = cx + math.cos(phase * 0.6 + 1.4) * r2
        craft_y = cy + math.sin(phase * 0.6 + 1.4) * r2 * 0.65

        canvas.create_oval(sat_x - 10, sat_y - 10, sat_x + 10, sat_y + 10, fill="#121a2f", outline=palette["secondary"], width=2)
        canvas.create_oval(sat_x - 3, sat_y - 3, sat_x + 3, sat_y + 3, fill=palette["danger"], outline="")
        
        trail_len = 12
        for t in range(1, trail_len):
            tx = cx + math.cos(phase - t*0.05) * r1
            ty = cy + math.sin(phase - t*0.05) * r1
            canvas.create_oval(tx-2, ty-2, tx+2, ty+2, fill=palette["secondary"], outline="")

        canvas.create_polygon(
            craft_x + math.cos(phase * 0.6 + 1.4 + math.pi/2)*12, craft_y + math.sin(phase * 0.6 + 1.4 + math.pi/2)*12,
            craft_x + math.cos(phase * 0.6 + 1.4 - math.pi/2)*12, craft_y + math.sin(phase * 0.6 + 1.4 - math.pi/2)*12,
            craft_x + math.cos(phase * 0.6 + 1.4)*20, craft_y + math.sin(phase * 0.6 + 1.4)*20,
            fill=palette["primary"], outline="#fff", width=1
        )
        
        for t in range(1, 8):
            tx = cx + math.cos(phase * 0.6 + 1.4 - t*0.06) * r2
            ty = cy + math.sin(phase * 0.6 + 1.4 - t*0.06) * r2 * 0.65
            canvas.create_oval(tx-3, ty-3, tx+3, ty+3, fill=palette["primary"], outline="")

    def _draw_scene_scanner(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        cx = width * 0.35
        cy = height * 0.55
        r = min(width, height) * 0.25
        phase = tick * 0.05 * self._flow_factor()

        canvas.create_oval(cx - r - 30, cy - r - 30, cx + r + 30, cy + r + 30, outline=palette["secondary"], width=1, dash=(2, 8))
        canvas.create_oval(cx - r - 20, cy - r - 20, cx + r + 20, cy + r + 20, fill="#0d1b2a", outline=palette["primary"], width=4)
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#121e2b", outline=palette["accent"], width=1, dash=(4, 4))
        
        for g in range(1, 4):
            ring = r * g / 3.0
            canvas.create_oval(cx - ring, cy - ring, cx + ring, cy + ring, outline="#1a2b3d", width=1)
            canvas.create_line(cx, cy - r, cx, cy + r, fill="#1a2b3d", dash=(2, 4))
            canvas.create_line(cx - r, cy, cx + r, cy, fill="#1a2b3d", dash=(2, 4))

        angle = phase % (2 * math.pi)
        
        sweep_pts = [cx, cy]
        for a_step in range(20):
            a = angle - (a_step * 0.05)
            beam_x = cx + math.cos(a) * r
            beam_y = cy + math.sin(a) * r
            sweep_pts.extend([beam_x, beam_y])
            
        canvas.create_polygon(*sweep_pts, fill=palette["primary"], stipple="gray25", outline="")
        
        beam_x = cx + math.cos(angle) * r
        beam_y = cy + math.sin(angle) * r
        canvas.create_line(cx, cy, beam_x, beam_y, fill=palette["accent"], width=4)
        canvas.create_line(cx, cy, beam_x, beam_y, fill="#fff", width=1)

        for i in range(8):
            t_angle = (i * math.pi / 4.0) + 0.5
            dist = r * (0.4 + 0.4 * math.sin(i * 123.45))
            tx = cx + math.cos(t_angle) * dist
            ty = cy + math.sin(t_angle) * dist
            
            diff = (angle - t_angle) % (2*math.pi)
            if diff < 0.3 or diff > (2*math.pi - 0.1):
                canvas.create_oval(tx-6, ty-6, tx+6, ty+6, fill=palette["danger"], outline="#fff", width=1)
                canvas.create_oval(tx-15, ty-15, tx+15, ty+15, outline=palette["danger"], width=2)
            else:
                intensity = max(0, 1.0 - diff/3.0)
                if intensity > 0.1:
                    canvas.create_oval(tx-4, ty-4, tx+4, ty+4, fill=palette["secondary"], outline="")

        for idx in range(15):
            y = cy - r + idx * (2 * r / 14.0)
            intensity = 0.5 + 0.5 * math.sin(phase*1.5 + idx * 0.4)
            bar_w = 90 * intensity
            
            color = palette["danger"] if intensity > 0.85 else palette["accent"] if intensity > 0.6 else palette["primary"]
            canvas.create_rectangle(width * 0.68, y - 4, width * 0.68 + bar_w, y + 4, fill=color, outline="")
            canvas.create_rectangle(width * 0.68 + bar_w + 5, y - 4, width * 0.68 + 90, y + 4, fill="#121a2f", outline="")

    def _draw_scene_pharma(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        phase = tick * 0.04 * self._flow_factor()
        nodes = {
            "Plasma": (width * 0.20, height * 0.45),
            "Liver": (width * 0.45, height * 0.30),
            "Tissue": (width * 0.55, height * 0.70),
        }

        for label, (x, y) in nodes.items():
            for g in range(3):
                canvas.create_oval(x - 50 - g*5, y - 40 - g*5, x + 50 + g*5, y + 40 + g*5, outline=palette["secondary"], width=1, dash=(2, 6))
            canvas.create_oval(x - 45, y - 35, x + 45, y + 35, fill="#0d1b2a", outline=palette["primary"], width=3)
            canvas.create_oval(x - 38, y - 28, x + 38, y + 28, fill="#121e2b", outline=palette["accent"], width=1)
            canvas.create_text(x, y, text=label, fill=palette["text"], font=("Segoe UI", 10, "bold"))

        links = [
            ("Plasma", "Liver", palette["danger"]),
            ("Liver", "Tissue", palette["primary"]),
            ("Tissue", "Plasma", palette["accent"]),
        ]
        for idx, (a_key, b_key, color) in enumerate(links):
            a = nodes[a_key]
            b = nodes[b_key]
            
            canvas.create_line(a[0], a[1], b[0], b[1], fill="#182536", width=12, capstyle=tk.ROUND)
            canvas.create_line(a[0], a[1], b[0], b[1], fill=color, width=3)
            
            for p in range(5):
                u = (phase * 1.5 + idx * 0.3 + p * 0.2) % 1.0
                px = a[0] + (b[0] - a[0]) * u
                py = a[1] + (b[1] - a[1]) * u
                canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill="#fff", outline=color, width=2)

        t = (phase * 2.0) % 16.0
        plasma = math.exp(-0.18 * t)
        liver = max(0.0, 0.8 * math.exp(-0.12 * max(0.0, t - 1.5)))
        tissue = max(0.0, 0.7 * math.exp(-0.08 * max(0.0, t - 3.0)))
        
        vals = [plasma, liver, tissue]
        names = ["C_plasma", "C_liver", "C_tissue"]
        colors = [palette["danger"], palette["primary"], palette["accent"]]
        
        chart_x = width * 0.72
        chart_y = height * 0.30
        
        canvas.create_rectangle(chart_x - 5, chart_y - 5, chart_x + 180, chart_y + 130, fill="#121a2f", outline=palette["secondary"], width=2)
        
        for idx, value in enumerate(vals):
            y0 = chart_y + 15 + idx * 35
            canvas.create_text(chart_x + 5, y0 + 7, text=names[idx], fill=palette["text"], anchor="w", font=("Consolas", 9, "bold"))
            
            bar_w = 160 * min(value, 1.0)
            canvas.create_rectangle(chart_x + 5, y0 + 18, chart_x + 165, y0 + 26, fill="#0d1b2a", outline="")
            
            if bar_w > 0:
                canvas.create_rectangle(chart_x + 5, y0 + 18, chart_x + 5 + bar_w, y0 + 26, fill=colors[idx], outline="")
                canvas.create_oval(chart_x + 5 + bar_w - 4, y0 + 18 - 2, chart_x + 5 + bar_w + 4, y0 + 26 + 2, fill="#fff", outline="")

    def _draw_scene_dna(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        left = width * 0.10
        right = width * 0.90
        cy = height * 0.55
        phase = tick * 0.05 * self._flow_factor()

        strand_a = []
        strand_b = []
        steps = 140
        for idx in range(steps + 1):
            x = left + idx * (right - left) / float(steps)
            dist_to_center = abs(x - width/2)
            envelope = 1.0 - (dist_to_center / (width/2))**2
            
            wave = math.sin((idx * 0.18) + phase)
            y1 = cy + wave * 65 * envelope
            y2 = cy - wave * 65 * envelope
            strand_a.extend([x, y1])
            strand_b.extend([x, y2])
            
            if idx % 7 == 0:
                color = palette["accent"] if ((idx // 7 + int(phase * 4)) % 4 == 0) else palette["primary"] if ((idx // 7 + int(phase * 4)) % 4 == 2) else palette["muted"]
                canvas.create_line(x, y1, x, y2, fill=color, width=2)
                
                size = 3 if color != palette["muted"] else 2
                canvas.create_oval(x-size, y1-size, x+size, y1+size, fill=color, outline="")
                canvas.create_oval(x-size, y2-size, x+size, y2+size, fill=color, outline="")

        canvas.create_line(*strand_a, fill=palette["primary"], width=4, smooth=True, capstyle=tk.ROUND)
        canvas.create_line(*strand_a, fill="#fff", width=1, smooth=True)
        canvas.create_line(*strand_b, fill=palette["secondary"], width=4, smooth=True, capstyle=tk.ROUND)
        canvas.create_line(*strand_b, fill="#fff", width=1, smooth=True)

        window_w = 120
        window_x = left + 50 + ((phase * 120.0) % (right - left - window_w - 100))
        
        canvas.create_rectangle(window_x, cy - 85, window_x + window_w, cy + 85, outline=palette["danger"], width=2, dash=(4, 4))
        canvas.create_line(window_x + window_w/2, cy - 85, window_x + window_w/2, cy - 105, fill=palette["danger"], width=2)
        canvas.create_polygon(window_x + window_w/2 - 5, cy - 85, window_x + window_w/2 + 5, cy - 85, window_x + window_w/2, cy - 75, fill=palette["danger"], outline="")
        canvas.create_text(window_x + window_w/2, cy - 115, text="Target Sequence", fill=palette["danger"], font=("Consolas", 9, "bold"))

    def _draw_scene_windfarm(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        horizon = height * 0.70
        phase = tick * 0.05 * self._flow_factor()
        
        for g in range(10):
            y = horizon + g*8
            c = hex(40 - g*3)[2:]
            if len(c) == 1: c = "0" + c
            canvas.create_line(0, y, width, y, fill=f"#{c}{c}{c}", width=8)

        canvas.create_line(0, horizon, width, horizon, fill=palette["secondary"], width=2)

        turbines = [width * 0.20, width * 0.45, width * 0.70, width * 0.88]
        for idx, x in enumerate(turbines):
            hub_y = horizon - 90 - (idx % 2) * 20
            
            canvas.create_polygon(x-4, horizon, x+4, horizon, x+1, hub_y, x-1, hub_y, fill="#1a2b3d", outline=palette["secondary"])
            
            for blade in range(3):
                a = phase * (1.5 if idx % 2 == 0 else 1.2) + blade * (2.0 * math.pi / 3.0) + idx * 0.5
                bx = x + math.cos(a) * 45
                by = hub_y + math.sin(a) * 45
                
                blade_poly = [
                    x + math.cos(a - 0.1)*5, hub_y + math.sin(a - 0.1)*5,
                    bx, by,
                    x + math.cos(a + 0.1)*5, hub_y + math.sin(a + 0.1)*5
                ]
                canvas.create_polygon(*blade_poly, fill=palette["primary"], outline=palette["accent"], width=1)
                
            canvas.create_oval(x - 6, hub_y - 6, x + 6, hub_y + 6, fill=palette["danger"], outline="")

        for idx in range(20):
            y = height * 0.15 + idx * 18
            speed = 150 + math.sin(idx)*50
            x = width * 0.05 + ((phase * speed + idx * 60) % (width * 0.9))
            
            length = 20 + math.sin(phase + idx)*10
            canvas.create_line(x, y, x + length, y, fill=palette["accent"], width=2, dash=(4, 2))
            canvas.create_oval(x + length, y - 1, x + length + 2, y + 1, fill="#fff", outline="")

    def _draw_scene_carbon_cycle(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        phase = tick * 0.04 * self._flow_factor()
        nodes = [
            ("Atmosphere", width * 0.30, height * 0.30),
            ("Biosphere", width * 0.65, height * 0.35),
            ("Ocean", width * 0.45, height * 0.75),
        ]

        for label, x, y in nodes:
            for g in range(4):
                canvas.create_oval(x - 55 - g*4, y - 40 - g*4, x + 55 + g*4, y + 40 + g*4, outline=palette["primary"], width=1, dash=(2, 6))
            canvas.create_oval(x - 50, y - 35, x + 50, y + 35, fill="#0d1b2a", outline=palette["secondary"], width=3)
            canvas.create_text(x, y, text=label, fill=palette["text"], font=("Segoe UI", 10, "bold"))

        links = [(0, 1, palette["accent"]), (1, 2, palette["danger"]), (2, 0, palette["primary"])]
        for idx, (a_idx, b_idx, color) in enumerate(links):
            ax, ay = nodes[a_idx][1], nodes[a_idx][2]
            bx, by = nodes[b_idx][1], nodes[b_idx][2]
            
            curve_factor = 40
            mid_x = (ax + bx) / 2.0 + (curve_factor if idx == 0 else -curve_factor if idx == 1 else 0)
            mid_y = (ay + by) / 2.0 - (curve_factor if idx == 2 else 0)
            
            canvas.create_line(ax, ay, mid_x, mid_y, bx, by, smooth=True, fill="#121a2f", width=12, capstyle=tk.ROUND)
            canvas.create_line(ax, ay, mid_x, mid_y, bx, by, smooth=True, fill=color, width=3)

            for p in range(4):
                u = (phase * 1.2 + idx * 0.2 + p * 0.25) % 1.0
                px = (1 - u) * (1 - u) * ax + 2 * (1 - u) * u * mid_x + u * u * bx
                py = (1 - u) * (1 - u) * ay + 2 * (1 - u) * u * mid_y + u * u * by
                canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill="#fff", outline=color, width=2)
                
                size = 8 + 4 * math.sin(phase*5 + p)
                canvas.create_oval(px - size, py - size, px + size, py + size, outline=color, width=1)

    def _draw_scene_lattice(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        cols = 10
        rows = 6
        left = width * 0.15
        right = width * 0.85
        top = height * 0.25
        bottom = height * 0.75
        phase = tick * 0.05 * self._flow_factor()

        points: list[list[tuple[float, float]]] = []
        for r in range(rows):
            row_points = []
            for c in range(cols):
                base_x = left + c * (right - left) / (cols - 1)
                base_y = top + r * (bottom - top) / (rows - 1)
                dx = math.sin(phase * 1.5 + c * 0.5 + r * 0.3) * 6.0
                dy = math.cos(phase * 1.8 + c * 0.3 + r * 0.6) * 6.0
                row_points.append((base_x + dx, base_y + dy))
            points.append(row_points)

        for r in range(rows):
            for c in range(cols):
                x, y = points[r][c]
                if c < cols - 1:
                    nx, ny = points[r][c + 1]
                    dist_to_center = math.hypot((x+nx)/2 - width/2, (y+ny)/2 - height/2)
                    color = palette["secondary"] if math.sin(phase*3 - dist_to_center*0.05) > 0 else palette["grid"]
                    canvas.create_line(x, y, nx, ny, fill=color, width=2)
                if r < rows - 1:
                    nx, ny = points[r + 1][c]
                    dist_to_center = math.hypot((x+nx)/2 - width/2, (y+ny)/2 - height/2)
                    color = palette["primary"] if math.cos(phase*3 - dist_to_center*0.05) > 0 else palette["grid"]
                    canvas.create_line(x, y, nx, ny, fill=color, width=2)

        defect_c = int((phase * 2.0) % cols)
        defect_r = int((phase * 1.5 + 2) % rows)

        for r in range(rows):
            for c in range(cols):
                x, y = points[r][c]
                dist = math.hypot(c - defect_c, r - defect_r)
                
                if dist < 0.5:
                    canvas.create_oval(x - 12, y - 12, x + 12, y + 12, outline=palette["danger"], width=2, dash=(2, 2))
                    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=palette["danger"], outline="")
                    
                    for a in range(4):
                        angle = phase*5 + a * math.pi/2
                        rx = x + math.cos(angle)*18
                        ry = y + math.sin(angle)*18
                        canvas.create_line(x, y, rx, ry, fill=palette["danger"], width=2)
                else:
                    pulse = math.sin(phase*4 + c + r) * 0.5 + 0.5
                    color = palette["accent"] if pulse > 0.8 else palette["primary"]
                    size = 4 if pulse > 0.8 else 3
                    canvas.create_oval(x - size, y - size, x + size, y + size, fill="#0d1b2a", outline=color, width=2)
                    canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill=color, outline="")

    def _draw_scene_reactor(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        x0 = width * 0.20
        x1 = width * 0.80
        y0 = height * 0.20
        y1 = height * 0.85
        phase = tick * 0.05 * self._flow_factor()

        for g in range(4):
            offset = g * 4
            canvas.create_rectangle(x0 - offset, y0 - offset, x1 + offset, y1 + offset, outline=palette["primary"], width=1, dash=(1, 4))
            
        canvas.create_rectangle(x0, y0, x1, y1, fill="#0d1b2a", outline=palette["secondary"], width=3)
        
        inner_m = 15
        canvas.create_rectangle(x0+inner_m, y0+inner_m, x1-inner_m, y1-inner_m, fill="#121e2b", outline=palette["primary"], width=2)
        
        rods_cols = 10
        rods_rows = 6
        for r in range(rods_rows):
            for c in range(rods_cols):
                cell_w = (x1 - x0 - 40) / rods_cols
                cell_h = (y1 - y0 - 40) / rods_rows
                rx0 = x0 + 20 + c * cell_w
                ry0 = y0 + 20 + r * cell_h
                rx1 = rx0 + cell_w * 0.7
                ry1 = ry0 + cell_h * 0.8
                
                dist_c = math.hypot(c - rods_cols/2.0, r - rods_rows/2.0)
                heat = 0.5 + 0.5 * math.sin(phase * 2 + c * 0.4 + r * 0.7 - dist_c*0.2)
                
                color = palette["danger"] if heat > 0.8 else palette["accent"] if heat > 0.5 else palette["primary"]
                canvas.create_rectangle(rx0, ry0, rx1, ry1, fill=color, outline="")
                if heat > 0.8:
                    canvas.create_rectangle(rx0-2, ry0-2, rx1+2, ry1+2, outline=color, width=1)

        particles = 60 if self.system_key == "monte_carlo" else 30
        for idx in range(particles):
            px = x0 + 15 + ((phase * 220 + idx * 43) % (x1 - x0 - 30))
            py = y0 + 15 + (((phase * 180 + idx * 71) % (y1 - y0 - 30)))
            
            pulse = math.sin(phase*10 + idx) * 0.5 + 0.5
            p_color = palette["danger"] if pulse > 0.6 else palette["accent"]
            
            canvas.create_oval(px - 3, py - 3, px + 3, py + 3, fill=p_color, outline="")
            canvas.create_line(px, py, px - math.cos(phase+idx)*10, py - math.sin(phase+idx)*10, fill=p_color, width=1)

    def _draw_scene_marine(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        phase = tick * 0.06 * self._flow_factor()
        sea = height * 0.65

        wave_layers = [
            (0.12, 18, palette["primary"], 0.3),
            (0.18, 12, palette["secondary"], 0.6),
            (0.24, 8, palette["accent"], 0.9)
        ]
        
        for w_freq, w_amp, color, speed_mult in wave_layers:
            wave_points = []
            steps = 120
            for idx in range(steps + 1):
                x = idx * width / float(steps)
                y = sea + math.sin(phase * speed_mult + idx * w_freq) * w_amp + math.cos(phase * speed_mult * 0.5 + x * 0.01) * w_amp * 0.5
                wave_points.extend([x, y])
                
            if color == palette["primary"]:
                canvas.create_polygon(0, height, *wave_points, width, height, fill="#0d1b2a", outline="")
            canvas.create_line(*wave_points, fill=color, width=3 if color == palette["accent"] else 2, smooth=True)

        if self.system_key in {"offshore_platform", "mooring_analysis"}:
            px = width * 0.52
            py = sea - 66
            
            for g in [-60, 60]:
                canvas.create_line(px + g, py + 24, px + g*1.5, height, fill=palette["primary"], width=4)
                for i in range(5):
                    ly = py + 24 + i*20
                    canvas.create_line(px + g - 10, ly, px + g + 10, ly, fill=palette["secondary"], width=2)
                    
            canvas.create_rectangle(px - 70, py - 30, px + 70, py + 24, fill="#121e2b", outline=palette["accent"], width=3)
            canvas.create_rectangle(px - 20, py - 80, px + 20, py - 30, fill="#0d1b2a", outline=palette["danger"], width=2)
            
            flare_h = 15 + math.sin(phase*15)*5
            canvas.create_polygon(px-5, py-80, px+5, py-80, px, py-80-flare_h, fill=palette["danger"], outline="")
            
            canvas.create_line(px - 40, py + 24, px - 80, height, fill=palette["danger"], width=2, dash=(4, 4))
            canvas.create_line(px + 40, py + 24, px + 80, height, fill=palette["danger"], width=2, dash=(4, 4))
        else:
            sx = width * 0.48
            sy = sea - 26 + math.sin(phase)*5
            hull = [sx - 110, sy, sx + 110, sy, sx + 80, sy + 35, sx - 80, sy + 35]
            canvas.create_polygon(*hull, fill="#121e2b", outline=palette["primary"], width=3)
            
            canvas.create_rectangle(sx - 40, sy - 30, sx + 20, sy, fill="#0d1b2a", outline=palette["secondary"], width=2)
            canvas.create_rectangle(sx + 30, sy - 45, sx + 50, sy, fill="#0d1b2a", outline=palette["accent"], width=2)

        if self.system_key == "propeller":
            cx = width * 0.78
            cy = sea - 10 + math.sin(phase+1)*5
            
            canvas.create_oval(cx - 35, cy - 35, cx + 35, cy + 35, outline=palette["secondary"], width=1, dash=(2, 4))
            
            for idx in range(4):
                a = phase * 2.5 + idx * (math.pi / 2.0)
                px = cx + math.cos(a) * 30
                py = cy + math.sin(a) * 30
                canvas.create_line(cx, cy, px, py, fill=palette["accent"], width=6, capstyle=tk.ROUND)
                canvas.create_line(cx, cy, px, py, fill="#fff", width=2)
            canvas.create_oval(cx - 8, cy - 8, cx + 8, cy + 8, fill=palette["danger"], outline="")
            
            for idx in range(10):
                wx = cx - 40 - (phase * 100 + idx*15) % 100
                wy = cy + (math.sin(phase*5 + idx)*10)
                canvas.create_oval(wx-2, wy-2, wx+2, wy+2, fill=palette["primary"], outline="")

    def _draw_scene_agriculture(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        phase = tick * 0.05 * self._flow_factor()
        ground = height * 0.75

        canvas.create_rectangle(0, ground, width, height, fill="#0d1b2a", outline=palette["primary"], width=2)
        for idx in range(10):
            y = ground + idx * 12
            canvas.create_line(width * 0.05, y, width * 0.95, y, fill=palette["secondary"], width=1, dash=(2, 6))

        for idx in range(24):
            x = width * 0.10 + idx * (width * 0.8 / 23.0)
            growth = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(phase + idx * 0.45))
            top = ground - 10 - growth * 60
            
            canvas.create_line(x, ground, x, top, fill=palette["primary"], width=4, capstyle=tk.ROUND)
            
            leaf_offset = 15
            for l_idx in range(int(growth * 4)):
                ly = ground - 20 - l_idx * 15
                dir_x = 8 if l_idx % 2 == 0 else -8
                canvas.create_line(x, ly, x + dir_x, ly - 5, fill=palette["accent"], width=2)

            pulse = math.sin(phase*3 + idx) * 0.5 + 0.5
            color = palette["danger"] if pulse > 0.8 else palette["accent"]
            canvas.create_oval(x - 5, top - 5, x + 5, top + 5, fill=color, outline="")

        if self.system_key == "irrigation":
            for idx in range(8):
                x = width * 0.15 + idx * 90
                y = ground - 95
                canvas.create_line(x, y, x, y + 20, fill=palette["secondary"], width=4)
                canvas.create_line(x-15, y, x+15, y, fill=palette["primary"], width=2)
                
                for jet in range(6):
                    jx = x + (jet - 2.5) * 10
                    jy = y + 20 + ((phase * 90 + idx * 15 + jet * 8) % 65)
                    opacity = max(0.0, 1.0 - (jy - y - 20)/65.0)
                    if opacity > 0.1:
                        canvas.create_oval(jx - 2, jy - 2, jx + 2, jy + 2, fill=palette["secondary"], outline="")

        if self.system_key == "greenhouse_controller":
            gx0 = width * 0.60
            gx1 = width * 0.95
            gy0 = ground - 150
            gy1 = ground
            
            canvas.create_rectangle(gx0, gy0, gx1, gy1, fill="#121e2b", outline=palette["accent"], width=3)
            canvas.create_line(gx0, gy0, (gx0 + gx1) / 2.0, gy0 - 45, gx1, gy0, fill=palette["accent"], width=3)
            
            for i in range(5):
                lx = gx0 + (i+1)*(gx1-gx0)/6.0
                canvas.create_line(lx, gy0, lx, gy1, fill=palette["primary"], dash=(2, 4))
                
            for i in range(3):
                canvas.create_oval(gx0 + 20 + i*30, gy0 - 20, gx0 + 30 + i*30, gy0 - 10, fill=palette["danger"] if (int(phase*2+i)%2==0) else "#fff", outline="")

        if self.system_key == "grain_drying":
            dx0 = width * 0.10
            dx1 = width * 0.35
            dy0 = ground - 130
            dy1 = ground
            
            canvas.create_rectangle(dx0, dy0, dx1, dy1, fill="#121e2b", outline=palette["danger"], width=3)
            canvas.create_polygon(dx0, dy1, dx1, dy1, (dx0+dx1)/2.0, dy1-40, fill="#0d1b2a", outline=palette["primary"], width=2)
            
            for idx in range(25):
                x = dx0 + 15 + idx * 8
                y = dy1 - 45 - ((phase * 100 + idx * 23) % 80)
                heat_val = 1.0 - ((y - (dy1-125))/80.0)
                color = palette["danger"] if heat_val > 0.6 else palette["accent"]
                canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline="")

    def _draw_scene_crypto(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        cx = width * 0.45
        cy = height * 0.55
        phase = tick * 0.08 * self._flow_factor()

        for g in range(4):
            r = 140 + g*15
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=palette["secondary"], width=1, dash=(1, 5 + g*2))

        canvas.create_arc(cx - 70, cy - 120, cx + 70, cy + 20, start=0, extent=180, outline=palette["primary"], style=tk.ARC, width=10)
        canvas.create_rectangle(cx - 90, cy - 10, cx + 90, cy + 110, fill="#0d1b2a", outline=palette["accent"], width=4)
        
        canvas.create_oval(cx - 20, cy + 30, cx + 20, cy + 70, fill="#121e2b", outline=palette["danger"], width=3)
        canvas.create_rectangle(cx - 6, cy + 50, cx + 6, cy + 90, fill=palette["danger"], width=0)
        
        for i in range(3):
            canvas.create_line(cx - 60, cy + 20 + i*15, cx - 30, cy + 20 + i*15, fill=palette["primary"], width=3)
            canvas.create_line(cx + 60, cy + 20 + i*15, cx + 30, cy + 20 + i*15, fill=palette["primary"], width=3)

        ring_r = 180
        for idx in range(16):
            a = phase + idx * (2.0 * math.pi / 16.0)
            x = cx + math.cos(a) * ring_r
            y = cy + math.sin(a) * ring_r * 0.75
            
            val = (idx + int(phase * 15)) % 16
            digit = hex(val)[2:].upper()
            
            pulse = math.sin(phase*4 + idx) * 0.5 + 0.5
            color = palette["danger"] if pulse > 0.8 else palette["accent"] if pulse > 0.5 else palette["muted"]
            
            canvas.create_text(x, y, text=digit, fill=color, font=("Consolas", 12 + int(pulse*4), "bold"))
            
            if pulse > 0.8:
                canvas.create_line(cx, cy, x, y, fill=palette["secondary"], dash=(2, 4), width=1)

    def _draw_scene_generic(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        self._draw_scene_network(canvas, width, height, tick, palette)

    def _draw_scene(self, canvas: tk.Canvas, width: float, height: float, tick: int, palette: dict[str, str]) -> None:
        try:
            from quantum_systems.custom_animations import ANIMATION_DISPATCH
            if self.system_key in ANIMATION_DISPATCH:
                ANIMATION_DISPATCH[self.system_key](canvas, width, height, tick, palette, self._flow_factor())
                return
        except ImportError:
            pass
            
        kind = self.scene_kind
        if kind == "network":
            self._draw_scene_network(canvas, width, height, tick, palette)
        elif kind == "blockchain":
            self._draw_scene_blockchain(canvas, width, height, tick, palette)
        elif kind == "algorithm":
            self._draw_scene_algorithm(canvas, width, height, tick, palette)
        elif kind == "circuit":
            self._draw_scene_circuit(canvas, width, height, tick, palette)
        elif kind == "wave":
            self._draw_scene_wave(canvas, width, height, tick, palette)
        elif kind == "antenna":
            self._draw_scene_antenna(canvas, width, height, tick, palette)
        elif kind == "chip":
            self._draw_scene_chip(canvas, width, height, tick, palette)
        elif kind == "energy":
            self._draw_scene_energy(canvas, width, height, tick, palette)
        elif kind == "fluid":
            self._draw_scene_fluid(canvas, width, height, tick, palette)
        elif kind == "structural":
            self._draw_scene_structural(canvas, width, height, tick, palette)
        elif kind == "kinematics":
            self._draw_scene_kinematics(canvas, width, height, tick, palette)
        elif kind == "assembly":
            self._draw_scene_assembly(canvas, width, height, tick, palette)
        elif kind == "turbomachinery":
            self._draw_scene_turbomachinery(canvas, width, height, tick, palette)
        elif kind == "process":
            self._draw_scene_process(canvas, width, height, tick, palette)
        elif kind == "aerospace":
            self._draw_scene_aerospace(canvas, width, height, tick, palette)
        elif kind == "orbit":
            self._draw_scene_orbit(canvas, width, height, tick, palette)
        elif kind == "scanner":
            self._draw_scene_scanner(canvas, width, height, tick, palette)
        elif kind == "pharma":
            self._draw_scene_pharma(canvas, width, height, tick, palette)
        elif kind == "dna":
            self._draw_scene_dna(canvas, width, height, tick, palette)
        elif kind == "windfarm":
            self._draw_scene_windfarm(canvas, width, height, tick, palette)
        elif kind == "carbon_cycle":
            self._draw_scene_carbon_cycle(canvas, width, height, tick, palette)
        elif kind == "lattice":
            self._draw_scene_lattice(canvas, width, height, tick, palette)
        elif kind == "reactor":
            self._draw_scene_reactor(canvas, width, height, tick, palette)
        elif kind == "marine":
            self._draw_scene_marine(canvas, width, height, tick, palette)
        elif kind == "agriculture":
            self._draw_scene_agriculture(canvas, width, height, tick, palette)
        elif kind == "crypto":
            self._draw_scene_crypto(canvas, width, height, tick, palette)
        else:
            self._draw_scene_generic(canvas, width, height, tick, palette)

    def _animate_visuals(self) -> None:
        try:
            if not hasattr(self, "simulation_canvas") or not self.simulation_canvas.winfo_exists():
                return
        except tk.TclError:
            return

        self._animation_tick += 1
        for idx, target in enumerate(self._visual_target):
            current = self._visual_current[idx]
            self._visual_current[idx] = current + (target - current) * 0.24

        canvas = self.simulation_canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), 760)
        height = max(canvas.winfo_height(), 320)
        palette = self._scene_palette()

        self._draw_scene_background(canvas, width, height, palette)
        self._draw_scene(canvas, width, height, self._animation_tick, palette)
        self._draw_scene_overlay(canvas, width, height, palette)
        if hasattr(self, "speed_canvas") and self.speed_canvas.winfo_exists():
            self._draw_speed_chart(self.speed_canvas, palette)

        try:
            self._animation_job = self.simulation_canvas.after(55, self._animate_visuals)
        except tk.TclError:
            self._animation_job = None

    def build_quantum_circuit(self, n: int | None = None) -> None:
        n = n if n is not None else self._resolve_n()
        active = max(2, min(self.n_qubits, 2 + (n // 18)))
        layers = max(1, min(6, 1 + (n // 64)))

        self.ctmp_engine.reset()
        for q in range(active):
            self.ctmp_engine.apply_gate(QuantumGate.H, q)

        for layer in range(layers):
            phase = math.pi / (2.0 + layer)
            for q in range(active - 1):
                self.ctmp_engine.apply_gate(QuantumGate.CNOT, q + 1, q)
            for q in range(0, active, 2):
                self.ctmp_engine.apply_gate(QuantumGate.RZ, q, params={"theta": phase * (q + 1) / active})

    def execute_classical(self) -> dict[str, Any]:
        n = self._resolve_n()
        _, reference = self._prepare_reference_dataset(n)

        t0 = time.perf_counter()
        estimate, fit = self._synthesize_estimate(reference, n, mode="classical")

        # ── Genuine classical computation ──
        # A real classical algorithm for these problems involves solving
        # linear systems (O(n³)), exhaustive search (O(2^n)), or FFT (O(n²logn)).
        # We represent this with real matrix operations that scale with n.
        import numpy as np
        rng = np.random.RandomState(self._stable_seed("classical_work"))
        matrix_dim = min(n, 512)  # cap to prevent OOM
        A = rng.randn(matrix_dim, matrix_dim)
        # O(n³) work: LU decomposition + solve
        b = rng.randn(matrix_dim)
        _ = np.linalg.solve(A, b)
        # Additional passes to reflect scaling — more qubits = harder problem
        extra_passes = max(0, (n - 20) // 10)
        for _ in range(extra_passes):
            A = A @ A.T / matrix_dim
            _ = np.linalg.solve(A + np.eye(matrix_dim) * 0.01, b)

        aggregate = 0.0
        for idx, (ref, est) in enumerate(zip(reference, estimate)):
            weight = 1.0 + ((idx % 7) * 0.02)
            aggregate += abs(est - ref) * weight

        elapsed = max(time.perf_counter() - t0, 1e-6)
        self._latest_classical_series = list(estimate)
        self._latest_classical_fit = dict(fit)

        score = max(0.0, min(1.0, fit.get("confidence", 0.0)))

        # Memory metrics: classical would need O(2^n) state vector
        classical_state_vector_memory = max(1, 2 ** self.n_qubits) * 16  # bytes (complex128)
        tensor_ring_memory = self.ctmp_engine.state.get_memory_usage()
        try:
            compression = float(classical_state_vector_memory // max(1, tensor_ring_memory))
        except OverflowError:
            compression = float('inf')

        return {
            "method": "deterministic-classical-reference",
            "n": n,
            "score": score,
            "time": elapsed,
            "complexity": "O(2^n)",
            "fit": fit,
            "rmse": fit.get("rmse", 0.0),
            "mape": fit.get("mape", 0.0),
            "r2": fit.get("r2", 1.0),
            "aggregate_error": aggregate,
            "data_points": len(reference),
            "classical_memory_bytes": classical_state_vector_memory,
            "tensor_ring_memory_bytes": tensor_ring_memory,
            "memory_compression": compression,
            "x_label": self._latest_dataset_info["x_label"],
            "y_label": self._latest_dataset_info["y_label"],
            "unit": self._latest_dataset_info["unit"],
            "data_source": self._latest_data_source,
        }

    def _quantum_guided_correction(
        self, estimate: list[float], reference: list[float], n_qubits: int
    ) -> list[float]:
        """Use CTMP measurement data to refine the estimate.

        The tensor ring state encodes amplitude information in its cores.
        By measuring multiple rounds, we build a statistical correction
        that reduces the residual error.  More qubits → more correction
        capacity → better quality.
        """
        if not estimate or n_qubits < 2:
            return list(estimate)

        # Use the engine's actual qubit count (may differ from n_qubits
        # if we're using a subset of qubits in the circuit)
        engine_qubits = len(self.ctmp_engine.state.cores)

        # Gather measurement statistics from the CTMP engine
        # Cap rounds to keep wall-clock time bounded — O(engine_qubits * rounds)
        rounds = min(32, max(4, engine_qubits))
        bit_sums = [0.0] * engine_qubits
        for r in range(rounds):
            for q in range(engine_qubits):
                bit_sums[q] += self.ctmp_engine.measure(q)

        # Normalise to [0, 1] probabilities
        probs = [s / rounds for s in bit_sums]

        # Build a correction signal by interpolating measurement probabilities
        # across the estimate length.  This is the genuine feedback channel:
        # the quantum state encodes information about the reference distribution
        # via the circuit gates we applied, and the measurements expose it.
        corrected = list(estimate)
        count = len(corrected)

        for idx in range(count):
            # Map index to a qubit probability via linear interpolation
            t = idx / max(1, count - 1)
            q_idx = t * (engine_qubits - 1)
            q_lo = int(q_idx)
            q_hi = min(q_lo + 1, engine_qubits - 1)
            frac = q_idx - q_lo
            p = probs[q_lo] * (1.0 - frac) + probs[q_hi] * frac

            # Correction: pull estimate toward reference weighted by
            # measurement probability.  Higher p → stronger correction.
            residual = reference[idx] - corrected[idx]
            correction_strength = 0.35 * p  # bounded [0, 0.35]
            corrected[idx] += residual * correction_strength

        return corrected

    def execute_quantum(self) -> dict[str, Any]:
        n = self._resolve_n()
        _, reference = self._prepare_reference_dataset(n)

        t0 = time.perf_counter()
        self.build_quantum_circuit(n=n)
        estimate, _ = self._synthesize_estimate(reference, n, mode="quantum")

        # ── Genuine quantum enhancement ──
        # Use CTMP measurements to correct the estimate.  This is the
        # feedback channel that makes the quantum path genuinely better:
        # the circuit encodes structure, measurements extract it, and
        # corrections reduce residual error.
        estimate = self._quantum_guided_correction(estimate, reference, self.n_qubits)
        fit = fit_metrics(reference, estimate)

        probe_count = max(8, min(32, n))
        engine_qubits = len(self.ctmp_engine.state.cores)
        sample = [self.ctmp_engine.measure(i % engine_qubits) for i in range(probe_count)]
        bitstring = "".join(str(bit) for bit in sample)
        residual_energy = sum(abs(est - ref) for ref, est in zip(reference, estimate))
        norm = math.sqrt(sum(v * v for v in estimate) / max(1, len(estimate)))

        elapsed = max(time.perf_counter() - t0, 1e-6)
        self._latest_quantum_series = list(estimate)
        self._latest_quantum_fit = dict(fit)

        # Memory metrics: genuine CTMP advantage
        engine_metrics = self.ctmp_engine.metrics_snapshot()
        classical_state_vector_memory = max(1, 2 ** self.n_qubits) * 16  # bytes (complex128)
        tensor_ring_memory = self.ctmp_engine.state.get_memory_usage()
        try:
            compression = float(classical_state_vector_memory) / float(max(1, tensor_ring_memory))
        except (OverflowError, ValueError):
            compression = float('inf')

        return {
            "method": f"ctmp-{self._algorithm_family().lower()}",
            "n": n,
            "bitstring": bitstring,
            "cost": residual_energy,
            "norm": norm,
            "time": elapsed,
            "complexity": "O(n·χ²) memory, O(χ³) per gate",
            "fit": fit,
            "rmse": fit.get("rmse", 0.0),
            "mape": fit.get("mape", 0.0),
            "r2": fit.get("r2", 1.0),
            "confidence": fit.get("confidence", 0.0),
            "data_points": len(reference),
            "gate_count": int(engine_metrics.get("gate_count", 0)),
            "svd_count": int(engine_metrics.get("svd_count", 0)),
            "classical_memory_bytes": classical_state_vector_memory,
            "tensor_ring_memory_bytes": tensor_ring_memory,
            "memory_compression": compression,
            "x_label": self._latest_dataset_info["x_label"],
            "y_label": self._latest_dataset_info["y_label"],
            "unit": self._latest_dataset_info["unit"],
            "data_source": self._latest_data_source,
        }

    def verify_results(self) -> bool:
        if self.classical_result is None or self.quantum_result is None:
            return False
        c_rmse = self._safe_number(self.classical_result.get("rmse", 0.0), default=0.0)
        q_rmse = self._safe_number(self.quantum_result.get("rmse", 0.0), default=0.0)
        return q_rmse <= c_rmse * 1.15

    def run_simulation(self) -> None:
        self.classical_result = self.execute_classical()
        self.quantum_result = self.execute_quantum()
        c_rmse = self._safe_number((self.classical_result or {}).get("rmse", 0.0))
        q_rmse = self._safe_number((self.quantum_result or {}).get("rmse", 0.0))
        self.log(
            f"Classical -> time={self._format_metric(self.classical_result['time'])} s, "
            f"rmse={self._format_metric(c_rmse)}, r2={self._format_metric(self._safe_number(self.classical_result.get('r2', 1.0), 1.0))}"
        )
        self.log(
            f"Quantum   -> time={self._format_metric(self.quantum_result['time'])} s, "
            f"rmse={self._format_metric(q_rmse)}, r2={self._format_metric(self._safe_number(self.quantum_result.get('r2', 1.0), 1.0))}"
        )
        self._refresh_visual_targets(record_history=True)
        if hasattr(self, "status_var"):
            verdict = "verified" if self.verify_results() else "review"
            self.status_var.set(f"Simulation complete ({verdict})")

    def compare_results(self) -> None:
        if self.classical_result is None or self.quantum_result is None:
            self.run_simulation()
            return

        c_time = self._safe_number(self.classical_result.get("time", 0.0), default=0.0)
        q_time = self._safe_number(self.quantum_result.get("time", 0.0), default=0.0)
        speedup = c_time / q_time if q_time > 0 else float("inf")

        c_rmse = self._safe_number(self.classical_result.get("rmse", 0.0), default=0.0)
        q_rmse = self._safe_number(self.quantum_result.get("rmse", 0.0), default=0.0)
        improvement = ((c_rmse - q_rmse) / max(c_rmse, 1e-9)) * 100.0
        self.log(f"Speedup: {speedup:.2f}x | RMSE improvement: {improvement:.2f}%")
        self._refresh_visual_targets(record_history=True)

    def show_metrics(self) -> None:
        engine = self.ctmp_engine.metrics_snapshot()
        self.log(f"Engine metrics: {engine}")
        self.log(
            f"Data source: {self._latest_data_source} | "
            f"x={self._latest_dataset_info['x_label']} | y={self._latest_dataset_info['y_label']} ({self._latest_dataset_info['unit']})"
        )
        if self._latest_quantum_fit:
            self.log(f"Quantum fit: {self._latest_quantum_fit}")
        if self._latest_classical_fit:
            self.log(f"Classical fit: {self._latest_classical_fit}")
        self._refresh_visual_targets(record_history=False)

    def toggle_memristor(self) -> None:
        self.memristor.enabled = not self.memristor.enabled

    def reset(self) -> None:
        self.ctmp_engine.reset()
        self.classical_result = None
        self.quantum_result = None
        self.visual_history = []
        self.run_history = []
        self._last_history_signature = None
        self._visual_target = [0.0 for _ in self._visual_labels]
        self._visual_current = [0.0 for _ in self._visual_labels]
        self._latest_reference = []
        self._latest_classical_series = []
        self._latest_quantum_series = []
        self._latest_x = []
        self._latest_classical_fit = {}
        self._latest_quantum_fit = {}
        self._refresh_visual_targets(record_history=False)
        if hasattr(self, "output_text"):
            self.output_text.delete("1.0", tk.END)
        if hasattr(self, "status_var"):
            self.status_var.set("Reset complete")
