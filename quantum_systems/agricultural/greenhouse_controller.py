"""Quantum Greenhouse Controller
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class GreenhouseController(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Greenhouse Controller", n_qubits=9, max_bond_dim=20, classical_time_target=1.0)
        self._seed = 70937


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = GreenhouseController()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
