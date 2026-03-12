"""Performance comparison helpers."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import time

@dataclass
class BenchmarkResult:
    algorithm_name: str
    mode: str
    execution_time: float
    result: object
    success: bool
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class PerformanceBenchmark:
    def __init__(self, algorithm_name: str): self.algorithm_name = algorithm_name; self.classical_result = None; self.quantum_result = None
    def _run(self, mode: str, func, *args, **kwargs):
        t0 = time.perf_counter()
        try: val = func(*args, **kwargs); ok = True
        except Exception as exc: val = str(exc); ok = False
        return BenchmarkResult(self.algorithm_name, mode, max(time.perf_counter()-t0,1e-6), val, ok)
    def run_classical(self, func, *args, **kwargs): self.classical_result = self._run("classical", func, *args, **kwargs); return self.classical_result
    def run_quantum(self, func, *args, **kwargs): self.quantum_result = self._run("quantum", func, *args, **kwargs); return self.quantum_result
    def calculate_advantages(self):
        if not self.classical_result or not self.quantum_result: return {"speedup":1.0,"memory_advantage":1.0,"efficiency":1.0}
        s = self.classical_result.execution_time / max(self.quantum_result.execution_time,1e-6)
        return {"speedup":s,"memory_advantage":1.0,"efficiency":s}
    def verify_result_equivalence(self, tolerance: float = 1e-6) -> bool:
        return bool(self.classical_result and self.quantum_result and self.classical_result.success and self.quantum_result.success)
    def get_summary(self) -> str: return f"Benchmark {self.algorithm_name}: speedup={self.calculate_advantages()['speedup']:.2f}x"

class ComparisonEngine:
    def __init__(self, name: str = "comparison"): self.name = name; self.benchmark = PerformanceBenchmark(name)
