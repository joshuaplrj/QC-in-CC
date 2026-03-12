"""Quantum Reactor Design
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class ReactorDesign(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Reactor Design", n_qubits=12, max_bond_dim=18, classical_time_target=1.0)
        self._seed = 1533


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = ReactorDesign()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
