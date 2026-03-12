"""Quantum Mooring Analysis
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class MooringAnalysis(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Mooring Analysis", n_qubits=9, max_bond_dim=13, classical_time_target=1.0)
        self._seed = 93073


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = MooringAnalysis()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
