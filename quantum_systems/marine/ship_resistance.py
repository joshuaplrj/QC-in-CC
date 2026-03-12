"""Quantum Ship Resistance
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class ShipResistance(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Ship Resistance", n_qubits=11, max_bond_dim=18, classical_time_target=1.0)
        self._seed = 41457


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = ShipResistance()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
