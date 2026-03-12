"""Quantum Turbomachinery
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class Turbomachinery(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Turbomachinery", n_qubits=12, max_bond_dim=12, classical_time_target=1.0)
        self._seed = 5702


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = Turbomachinery()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
