"""Quantum Monte Carlo
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class MonteCarlo(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Monte Carlo", n_qubits=9, max_bond_dim=20, classical_time_target=1.0)
        self._seed = 90667


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = MonteCarlo()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
