"""Stable CTMP engine primitives."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import math
import time
from typing import Any
import numpy as np

class QuantumGate(Enum):
    H="hadamard"; X="pauli_x"; Y="pauli_y"; Z="pauli_z"; CNOT="cnot"; CZ="cz"; CPHASE="cphase"; RX="rx"; RY="ry"; RZ="rz"; PHASE="phase"; T="t"; SWAP="swap"; TOFFOLI="toffoli"; MEASURE="measure"

@dataclass
class GateOperation:
    gate: QuantumGate
    target: int
    control: int | None = None
    params: dict[str, Any] | None = None

class TensorRing:
    def __init__(self, n_qubits: int, bond_dim: int = 16) -> None:
        self.n_qubits = n_qubits
        self.bond_dim = max(2, bond_dim)
        self.cores = []
        for _ in range(n_qubits):
            c = np.zeros((self.bond_dim, 2, self.bond_dim), dtype=complex)
            c[0, 0, 0] = 1.0
            self.cores.append(c)
    def get_memory_usage(self) -> int: return sum(c.nbytes for c in self.cores)
    def get_classical_memory(self) -> int: return max(1, 2**self.n_qubits) * 16
    def get_compression_ratio(self) -> float: return self.get_classical_memory() / max(1, self.get_memory_usage())

class CTMP_Engine:
    def __init__(self, n_qubits: int = 8, max_bond_dim: int = 16) -> None:
        self.n_qubits = n_qubits
        self.max_bond_dim = max(2, min(max_bond_dim, 64))
        self.state = TensorRing(n_qubits, self.max_bond_dim)
        self.gate_history = []
        self._metric_refresh_interval = 4
        self.metrics = {"gate_count":0,"svd_count":0,"execution_time":0.0,"memory_peak":float(self.state.get_memory_usage()),"compression_ratio":float(self.state.get_compression_ratio())}

    def reset(self) -> None:
        self.state = TensorRing(self.n_qubits, self.max_bond_dim)
        self.gate_history = []
        self.metrics.update({"gate_count":0,"svd_count":0,"execution_time":0.0,"memory_peak":float(self.state.get_memory_usage()),"compression_ratio":float(self.state.get_compression_ratio())})

    def _single(self, g: QuantumGate, p: dict[str, Any] | None = None) -> np.ndarray:
        p = p or {}
        if g == QuantumGate.H: return np.array([[1,1],[1,-1]],dtype=complex)/math.sqrt(2)
        if g == QuantumGate.X: return np.array([[0,1],[1,0]],dtype=complex)
        if g == QuantumGate.Y: return np.array([[0,-1j],[1j,0]],dtype=complex)
        if g == QuantumGate.Z: return np.array([[1,0],[0,-1]],dtype=complex)
        if g == QuantumGate.PHASE: return np.array([[1,0],[0,np.exp(1j*float(p.get("theta",math.pi/4)))]],dtype=complex)
        if g == QuantumGate.T: return np.array([[1,0],[0,np.exp(1j*math.pi/4)]],dtype=complex)
        if g == QuantumGate.RX:
            t = float(p.get("theta",0.0)); return np.array([[math.cos(t/2),-1j*math.sin(t/2)],[-1j*math.sin(t/2),math.cos(t/2)]],dtype=complex)
        if g == QuantumGate.RY:
            t = float(p.get("theta",0.0)); return np.array([[math.cos(t/2),-math.sin(t/2)],[math.sin(t/2),math.cos(t/2)]],dtype=complex)
        if g == QuantumGate.RZ:
            t = float(p.get("theta",0.0)); return np.array([[np.exp(-1j*t/2),0],[0,np.exp(1j*t/2)]],dtype=complex)
        return np.eye(2,dtype=complex)

    def _two(self, g: QuantumGate, p: dict[str, Any] | None = None) -> np.ndarray:
        if g == QuantumGate.CNOT: return np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)
        if g == QuantumGate.CZ: return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,-1]],dtype=complex)
        if g == QuantumGate.CPHASE:
            t = float((p or {}).get("theta",math.pi/2)); return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,np.exp(1j*t)]],dtype=complex)
        if g == QuantumGate.SWAP: return np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)
        return np.eye(4,dtype=complex)

    def apply_gate(self, gate: QuantumGate, target: int, control: int | None = None, params: dict[str, Any] | None = None) -> None:
        t0 = time.perf_counter()
        target = int(target) % self.n_qubits
        control = None if control is None else int(control) % self.n_qubits
        if control is None: self._apply_single_qubit_gate(self._single(gate, params), target)
        else: self._apply_two_qubit_gate(self._two(gate, params), target, control)
        self.gate_history.append(GateOperation(gate,target,control,params))
        gate_count = int(self.metrics["gate_count"]) + 1
        self.metrics["gate_count"] = gate_count
        self.metrics["execution_time"] = float(self.metrics["execution_time"]) + (time.perf_counter() - t0)

        if gate_count % self._metric_refresh_interval == 0:
            mem = float(self.state.get_memory_usage())
            self.metrics["memory_peak"] = float(max(float(self.metrics["memory_peak"]), mem))
            self.metrics["compression_ratio"] = float(self.state.get_classical_memory() / max(1.0, mem))

    def _apply_single_qubit_gate(self, gate_matrix: np.ndarray, target: int) -> None:
        c = self.state.cores[target]
        self.state.cores[target] = np.einsum("ab,ibj->iaj", gate_matrix, c)

    def _apply_two_qubit_gate(self, gate_matrix: np.ndarray, target: int, control: int) -> None:
        """Apply a two-qubit gate using the CTMP merge-apply-SVD-truncate protocol.

        Per the CTMP framework design:
        1. Merge two adjacent cores into a joint tensor
        2. Apply the 4×4 gate on physical indices
        3. SVD decompose back into two cores
        4. Truncate to max_bond_dim to maintain O(n·χ²) memory
        """
        target = int(target) % self.n_qubits
        control = int(control) % self.n_qubits
        if target == control:
            return

        gate = np.asarray(gate_matrix, dtype=complex)
        if gate.shape == (2, 2):
            gate = np.array(
                [[1, 0, 0, 0], [0, 1, 0, 0],
                 [0, 0, gate[0, 0], gate[0, 1]],
                 [0, 0, gate[1, 0], gate[1, 1]]],
                dtype=complex,
            )
        elif gate.shape != (4, 4):
            return

        # Reshape gate to (i', j', i, j) for contraction
        U_gate = gate.reshape(2, 2, 2, 2)

        core_t = self.state.cores[target]   # shape: (χ_L, 2, χ_M)
        core_c = self.state.cores[control]  # shape: (χ_M', 2, χ_R)

        # 1. Merge: M[α, i, j, β] = Σ_γ core_t[α, i, γ] * core_c[γ, j, β]
        #    Note: for non-adjacent qubits we use direct contraction
        #    which is an approximation but preserves the tensor ring structure.
        merged = np.einsum("aig,gjb->aijb", core_t, core_c)
        # merged shape: (χ_L, 2, 2, χ_R)

        # 2. Apply gate: M'[α, i', j', β] = Σ_{i,j} U[i',j',i,j] * M[α,i,j,β]
        merged = np.einsum("klij,aijb->aklb", U_gate, merged)
        # merged shape: (χ_L, 2, 2, χ_R)

        chi_L = merged.shape[0]
        chi_R = merged.shape[3]

        # 3. Reshape for SVD: (χ_L * 2) × (2 * χ_R)
        M_matrix = merged.reshape(chi_L * 2, 2 * chi_R)

        # SVD decomposition
        U_svd, S, Vh = np.linalg.svd(M_matrix, full_matrices=False)

        # 4. Truncate to max_bond_dim
        chi_new = min(len(S), self.max_bond_dim)
        U_svd = U_svd[:, :chi_new]
        S = S[:chi_new]
        Vh = Vh[:chi_new, :]

        # Absorb singular values into U (left-canonical form)
        U_svd = U_svd * S[np.newaxis, :]

        # Reshape back into tensor cores
        # new_core_t: (χ_L, 2, χ_new)
        new_core_t = U_svd.reshape(chi_L, 2, chi_new)
        # new_core_c: (χ_new, 2, χ_R)
        new_core_c = Vh.reshape(chi_new, 2, chi_R)

        self.state.cores[target] = new_core_t
        self.state.cores[control] = new_core_c
        self.metrics["svd_count"] = int(self.metrics["svd_count"]) + 1

    def measure(self, qubit: int) -> int:
        c = self.state.cores[int(qubit)%self.n_qubits]
        p0 = float(np.sum(np.abs(c[:,0,:])**2)); p1 = float(np.sum(np.abs(c[:,1,:])**2)); t = p0+p1
        if t <= 0: return 0
        return 0 if (p0/t) >= 0.5 else 1

    def get_expectation_value(self, observable: np.ndarray, qubit: int) -> float:
        c = self.state.cores[int(qubit)%self.n_qubits]
        temp = np.einsum("ab,ibj->iaj", observable, c)
        return float(np.real(np.einsum("ibj,iaj->", c.conj(), temp)))

    def metrics_snapshot(self) -> dict[str, float | int]:
        mem = float(self.state.get_memory_usage())
        self.metrics["memory_peak"] = float(max(float(self.metrics["memory_peak"]), mem))
        self.metrics["compression_ratio"] = float(self.state.get_classical_memory() / max(1.0, mem))
        return dict(self.metrics)
