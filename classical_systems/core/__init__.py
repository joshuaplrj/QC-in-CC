"""
Stable core primitives for the rebuilt classical systems package.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import math
import time
from pathlib import Path
from typing import Any


@dataclass
class SimulationConfig:
    """Configuration for a classical simulation."""

    name: str
    parameters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class SimulationBase:
    """Small, deterministic base class used by every classical module."""

    def __init__(self, config: SimulationConfig | None = None) -> None:
        self.config = config or SimulationConfig(name=self.__class__.__name__)
        self.parameters = dict(self.config.parameters)
        self.results: dict[str, Any] = {}
        self.iteration_count = 0
        self.computation_time = 0.0
        self.status_history: list[str] = []

    def setup(self) -> None:
        """Prepare internal state before solve()."""

    def solve(self) -> None:
        raise NotImplementedError("solve() must be implemented by subclasses")

    def visualize(self, ax: Any = None) -> Any:
        return self.results

    def run(self) -> dict[str, Any]:
        self.setup()
        start = time.perf_counter()
        self.solve()
        self.computation_time = max(time.perf_counter() - start, 0.0)
        self.results.setdefault("computation_time", self.computation_time)
        return self.results

    def reset(self) -> None:
        self.results = {}
        self.iteration_count = 0
        self.computation_time = 0.0
        self.status_history.clear()

    def log_status(self, message: str) -> None:
        self.status_history.append(message)

    @staticmethod
    def generate_series(length: int, seed: int, scale: float = 1.0) -> list[float]:
        """Generate deterministic pseudo-random waveform data."""
        if length <= 0:
            return []

        state = seed & 0x7FFFFFFF
        if state == 0:
            state = 1

        values: list[float] = []
        for idx in range(length):
            state = (1103515245 * state + 12345) & 0x7FFFFFFF
            unit = state / 0x7FFFFFFF
            wave = math.sin(idx * 0.173) + math.cos(idx * 0.071)
            values.append(scale * (0.65 * wave + (unit - 0.5)))

        return values

    @staticmethod
    def discrete_spectrum(data: list[float], bins: int = 32) -> list[float]:
        """Compute a compact DFT magnitude spectrum without external dependencies."""
        if not data:
            return [0.0]

        n = len(data)
        k_max = max(1, min(int(bins), n))
        spec: list[float] = []

        for k in range(k_max):
            real = 0.0
            imag = 0.0
            for i, value in enumerate(data):
                angle = 2.0 * math.pi * k * i / n
                real += value * math.cos(angle)
                imag -= value * math.sin(angle)
            spec.append((real * real + imag * imag) ** 0.5 / n)

        return spec

    def export_results(self, path: str | Path) -> None:
        payload = {
            "name": self.config.name,
            "parameters": self.parameters,
            "results": self.results,
            "metrics": {
                "iteration_count": self.iteration_count,
                "computation_time": self.computation_time,
            },
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


class InteractiveGUI:
    """Compatibility shim for legacy imports."""

    def __init__(self, simulation: SimulationBase, title: str = "Classical Simulation") -> None:
        self.simulation = simulation
        self.title = title

    def run(self) -> dict[str, Any]:
        return self.simulation.run()


__all__ = ["SimulationBase", "SimulationConfig", "InteractiveGUI"]
