"""
Classical Carbon Cycle
Rebuilt stable simulation module.
"""

from __future__ import annotations

import statistics
from typing import Any

try:
    from core import SimulationBase, SimulationConfig
except ModuleNotFoundError:
    from classical_systems.core import SimulationBase, SimulationConfig


class CarbonCycleSimulation(SimulationBase):
    """Deterministic classical simulation for Carbon Cycle."""

    def __init__(self, config: SimulationConfig | None = None) -> None:
        config = config or SimulationConfig(
            name="Carbon Cycle",
            parameters={"problem_size": 128, "seed": 16137, "scale": 1.0},
        )
        super().__init__(config)

    def setup(self) -> None:
        self.problem_size = max(8, int(self.parameters.get("problem_size", 128)))
        self.seed = int(self.parameters.get("seed", 16137))
        self.scale = float(self.parameters.get("scale", 1.0))

    def solve(self) -> None:
        series = self.generate_series(self.problem_size, self.seed, self.scale)
        spectrum = self.discrete_spectrum(series)

        self.results = {
            "simulation": self.config.name,
            "sample_count": len(series),
            "mean": float(statistics.fmean(series)),
            "minimum": float(min(series)),
            "maximum": float(max(series)),
            "spectrum_peak": float(max(spectrum)),
        }
        self.iteration_count = self.problem_size


def main() -> dict[str, Any]:
    simulation = CarbonCycleSimulation()
    return simulation.run()


if __name__ == "__main__":
    output = main()
    print("CarbonCycleSimulation complete:", output)
