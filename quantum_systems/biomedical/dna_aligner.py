"""Quantum Dna Aligner
Data-calibrated simulation module."""
from __future__ import annotations

try:
    from quantum_systems.base_template import BaseQuantumSystem
except ModuleNotFoundError:
    from base_template import BaseQuantumSystem


class DnaAligner(BaseQuantumSystem):
    def __init__(self) -> None:
        super().__init__(name="Dna Aligner", n_qubits=12, max_bond_dim=16, classical_time_target=1.0)
        self._seed = 47938


def main() -> None:
    import tkinter as tk
    root = tk.Tk()
    app = DnaAligner()
    app.setup_gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
