"""Stable quantum algorithm stubs."""
from __future__ import annotations
import math
import random
import numpy as np
from .ctmp_engine import CTMP_Engine, QuantumGate

class HHLAlgorithm:
    def __init__(self, matrix_size: int = 8): self.matrix_size=max(2,matrix_size); self.n_qubits=int(math.ceil(math.log2(self.matrix_size))); self.engine=CTMP_Engine(n_qubits=max(2,self.n_qubits+1),max_bond_dim=16)
    def solve(self, A: np.ndarray, b: np.ndarray, shots: int = 64) -> np.ndarray:
        self.engine.reset(); [self.engine.apply_gate(QuantumGate.H,q) for q in range(min(self.engine.n_qubits,4))]
        n = np.linalg.norm(b)
        return np.zeros_like(b) if n <= 0 else b / n

class QAOAOptimizer:
    def __init__(self, n_qubits: int = 8, depth: int = 2): self.n_qubits=max(2,n_qubits); self.depth=max(1,depth); self.engine=CTMP_Engine(n_qubits=self.n_qubits,max_bond_dim=16); self.cost_terms=[]
    def set_problem(self, cost_terms): self.cost_terms=list(cost_terms)
    def _cost(self, bits):
        if not self.cost_terms: return float(sum(bits))
        v = 0.0
        for i,j,c in self.cost_terms:
            bi = bits[i % len(bits)]; bj = bits[j % len(bits)]; v += c * (1 if bi == bj else -1)
        return v
    def optimize(self, n_iterations: int = 32):
        rng = random.Random(42+self.n_qubits+self.depth); best=None; bc=float("inf")
        for _ in range(max(1,n_iterations)):
            bits=[rng.randint(0,1) for _ in range(self.n_qubits)]; c=self._cost(bits)
            if c < bc: best=bits; bc=c
        return (best or [0]*self.n_qubits), float(bc)

class VQESolver:
    def __init__(self, n_qubits: int = 6, n_electrons: int = 2): self.n_qubits=max(2,n_qubits); self.n_electrons=max(1,n_electrons); self.engine=CTMP_Engine(n_qubits=self.n_qubits,max_bond_dim=16)
    def solve_ground_state(self, iterations: int = 32): return -1.0 - 0.01*self.n_qubits, [0.1*(i+1) for i in range(min(8,self.n_qubits))]

class GroverSearch:
    def __init__(self, n_qubits: int = 6): self.n_qubits=max(2,n_qubits); self.marked={0}; self.engine=CTMP_Engine(n_qubits=self.n_qubits,max_bond_dim=8)
    def set_oracle(self, marked_items): self.marked={int(i) for i in marked_items} or {0}
    def search(self, shots: int = 64): return min(self.marked)

class QuantumFourierTransform:
    def __init__(self, n_qubits: int = 6): self.n_qubits=max(2,n_qubits); self.engine=CTMP_Engine(n_qubits=self.n_qubits,max_bond_dim=8)
    def apply_qft(self):
        self.engine.reset()
        for q in range(self.n_qubits):
            self.engine.apply_gate(QuantumGate.H, q)
            if q+1 < self.n_qubits: self.engine.apply_gate(QuantumGate.CPHASE, q+1, q, params={"theta": math.pi/(q+2)})

class QuantumWalk:
    def __init__(self, n_nodes: int = 8): self.n_nodes=max(2,n_nodes); self.position=0
    def step(self): self.position=(self.position+1)%self.n_nodes; return self.position
    def run(self, steps: int = 10): return [self.step() for _ in range(max(1,steps))]

class ShorAlgorithm:
    def __init__(self, n_qubits: int = 8): self.n_qubits=max(2,n_qubits)
    def factor(self, n: int):
        n = int(n)
        if n <= 3: return 1, n
        for i in range(2, int(math.sqrt(n))+1):
            if n % i == 0: return i, n//i
        return 1, n
