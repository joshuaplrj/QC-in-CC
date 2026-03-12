"""Quantum Trajectory
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class Trajectory(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Trajectory", n_qubits=11, max_bond_dim=15, classical_time_target=1.0)
        self._seed = 25598


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = Trajectory()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
