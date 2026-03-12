"""Quantum Hypersonic
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class Hypersonic(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Hypersonic", n_qubits=12, max_bond_dim=12, classical_time_target=1.0)
        self._seed = 24114


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = Hypersonic()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
