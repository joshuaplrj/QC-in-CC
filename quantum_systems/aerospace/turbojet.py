"""Quantum Turbojet
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class Turbojet(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Turbojet", n_qubits=12, max_bond_dim=17, classical_time_target=1.0)
        self._seed = 9776


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = Turbojet()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
