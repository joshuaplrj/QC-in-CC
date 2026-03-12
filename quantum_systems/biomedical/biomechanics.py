"""Quantum Biomechanics
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class Biomechanics(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Biomechanics", n_qubits=8, max_bond_dim=18, classical_time_target=1.0)
        self._seed = 42431


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = Biomechanics()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
