"""Quantum Carbon Cycle
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class CarbonCycle(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Carbon Cycle", n_qubits=8, max_bond_dim=12, classical_time_target=1.0)
        self._seed = 16137


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = CarbonCycle()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
