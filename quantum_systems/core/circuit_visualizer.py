"""Circuit visualization compatibility layer."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class QuantumCircuitRenderer:
    gate_count: int = 0
    def render_text(self) -> str: return f"Circuit gates: {self.gate_count}"

class CircuitVisualizer:
    def __init__(self, engine): self.engine = engine; self.renderer = QuantumCircuitRenderer()
    def setup_figure(self, fig):
        if fig is None: return
        fig.clear(); ax = fig.add_subplot(1,1,1); ax.text(0.5,0.5,"Circuit View",ha="center",va="center"); ax.axis("off")
    def animate_execution(self, fig, canvas, delay: float = 0.0):
        self.renderer.gate_count = len(getattr(self.engine, "gate_history", []))
        self.setup_figure(fig)
        if canvas is not None and hasattr(canvas, "draw"): canvas.draw()
