"""Memristor compatibility layer."""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass
class DiodeBridge:
    voltage: float = 0.0
    current: float = 0.0
    resistance: float = 120.0
    def step(self, Vin: float) -> float:
        self.voltage = float(Vin)
        drift = 0.05 * math.tanh(self.voltage/5.0)
        self.resistance = max(20.0, min(500.0, self.resistance - drift*10.0))
        self.current = self.voltage / max(self.resistance, 1e-6)
        return self.current
    def get_resistance(self) -> float: return float(self.resistance)
    def get_hysteresis_loop(self) -> tuple[list[float], list[float]]:
        vs = [math.sin(i*0.1)*5.0 for i in range(100)]
        ds = DiodeBridge(resistance=self.resistance)
        return vs, [ds.step(v) for v in vs]

class MemristorEmulator:
    def __init__(self, n_memristors: int = 8) -> None:
        self.n_memristors = n_memristors
        self.memristors = [DiodeBridge() for _ in range(n_memristors)]
        self.enabled = True
    def reset(self) -> None: self.memristors = [DiodeBridge() for _ in range(self.n_memristors)]
    def apply_signal(self, index: int, voltage: float) -> float:
        if not self.enabled: return 0.0
        return self.memristors[int(index)%self.n_memristors].step(voltage)
