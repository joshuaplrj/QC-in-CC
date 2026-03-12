"""Quantum Compiler Optimizer
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class CompilerOptimizer(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Compiler Optimizer", n_qubits=10, max_bond_dim=20, classical_time_target=1.0)
        self._seed = 36547


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = CompilerOptimizer()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
