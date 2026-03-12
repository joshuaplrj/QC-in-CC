"""Quantum Supply Chain
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class SupplyChain(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Supply Chain", n_qubits=10, max_bond_dim=16, classical_time_target=1.0)
        self._seed = 25200


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = SupplyChain()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
