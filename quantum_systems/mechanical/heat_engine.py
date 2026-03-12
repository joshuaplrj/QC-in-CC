"""Quantum Heat Engine
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class HeatEngine(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Heat Engine", n_qubits=9, max_bond_dim=16, classical_time_target=1.0)
        self._seed = 47821


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = HeatEngine()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
