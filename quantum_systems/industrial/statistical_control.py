"""Quantum Statistical Control
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class StatisticalControl(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Statistical Control", n_qubits=8, max_bond_dim=18, classical_time_target=1.0)
        self._seed = 3498


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = StatisticalControl()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
