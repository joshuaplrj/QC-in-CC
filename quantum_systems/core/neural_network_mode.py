"""Neural-mode compatibility layer."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class TensorNetworkGraph:
    node_count: int

class NeuralNetworkMode:
    def __init__(self, n_qubits: int = 8, bond_dim: int = 16): self.n_qubits = n_qubits; self.bond_dim = bond_dim; self.graph = TensorNetworkGraph(node_count=n_qubits)
    def setup_figure(self, fig):
        if fig is None: return
        fig.clear(); ax = fig.add_subplot(1,1,1); ax.text(0.5,0.5,"Tensor Network View",ha="center",va="center"); ax.axis("off")
    def update_visualization(self, active_nodes, active_messages):
        return {"active_nodes": list(active_nodes), "active_messages": list(active_messages), "node_count": self.graph.node_count}
