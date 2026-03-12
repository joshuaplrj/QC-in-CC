# Architecture & System Design

Comprehensive overview of QC in CC's design philosophy, module hierarchy, execution patterns, and data flow.

---

## Design Philosophy

QC in CC follows a **parallel dual-implementation pattern**:

1. **Classical Branch**: Deterministic baseline implementations using standard numerical algorithms
2. **Quantum Branch**: CTMP-accelerated versions with equivalent interfaces and built-in fidelity validation
3. **Equivalence Contract**: Both branches solve the same problems with comparable APIs, enabling direct performance comparison

This design enables:
- **Benchmarking**: Side-by-side performance analysis (4.5x average speedup observed)
- **Validation**: Quantum results verified against classical baselines
- **Experimentation**: Algorithm selection and tuning with known reference points
- **Extensibility**: New modules added to both branches simultaneously

---

## Core Architecture Layers

### Layer 1: Base Interfaces

```
┌─────────────────────────────────────────────────┐
│  SimulationBase (Classical)                      │
│  ├─ config: SimulationConfig                     │
│  ├─ setup() → None                               │
│  ├─ solve() → Dict                               │
│  ├─ visualize() → None                           │
│  └─ get_metrics() → Dict                         │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  BaseQuantumSystem (Quantum)                     │
│  ├─ config: SimulationConfig                     │
│  ├─ execute_classical() → Dict                   │
│  ├─ execute_quantum() → Dict                     │
│  ├─ get_fidelity_metrics() → Dict                │
│  └─ visualize() → None                           │
└─────────────────────────────────────────────────┘
```

### Layer 2: Domain-Specific Modules

Each discipline contains 4-8 domain modules inheriting from the base interfaces:

```
Discipline (e.g., Electrical Engineering)
├── PowerFlow (implements SimulationBase or BaseQuantumSystem)
├── CircuitSimulator
├── SignalProcessor
├── AntennaPattern
├── MotorDrive
├── VLSIPlacement
└── CommunicationChannel
```

### Layer 3: Quantum Computing Engine

```
BaseQuantumSystem
├── CTMP Engine (Coupled Tensor-Matrix Product)
│   ├─ TensorRing (quantum state representation)
│   ├─ QuantumGate (gate definitions)
│   └─ CircuitSimulator (gate execution)
├── Reference Models (baseline generation)
│   ├─ build_reference_dataset()
│   └─ fit_metrics()
├── Quantum Algorithms
│   ├─ HHL (linear systems)
│   ├─ QAOA (optimization)
│   ├─ VQE (eigensolvers)
│   └─ [8 total algorithm types]
└── Fidelity Metrics
    ├─ RMSE (root mean squared error)
    ├─ MAPE (mean absolute percentage error)
    ├─ R² (coefficient of determination)
    └─ Confidence Intervals
```

### Layer 4: User Interfaces

```
classical_systems/launcher.py (tkinter)
├── Module Discovery
├── Configuration Interface
├── Execution Manager
└── Results Display

quantum_systems/launcher_quantum.py (customtkinter)
├── Discipline Filter
├── Module Cards
├── Parameter Configuration
└── Real-time Visualization
```

---

## Execution Flow

### Classical Execution Path

```
┌─ User selects module in launcher
├─ launcher.py instantiates module class
│  (e.g., PowerFlow from electrical/power_flow.py)
├─ Module inherits SimulationBase
│
├─ Simulation Lifecycle:
│  ├─1. __init__(config: SimulationConfig)
│  │    └─ Store config (problem_size, seed, scale)
│  │
│  ├─2. setup()
│  │    ├─ Generate test data
│  │    ├─ Initialize algorithm structures
│  │    └─ Prepare visualization
│  │
│  ├─3. solve()
│  │    ├─ Execute core algorithm
│  │    ├─ Measure execution time
│  │    └─ Return results dict
│  │
│  ├─4. get_metrics()
│  │    ├─ Calculate mean, min, max
│  │    ├─ Compute spectrum analysis
│  │    └─ Return metrics dict
│  │
│  └─5. visualize()
│       ├─ Create matplotlib figure
│       ├─ Plot results
│       └─ Display chart
│
└─ launcher displays results to user
```

**Data Structure Returned by solve():**
```python
{
    'output': [...],           # main computation results
    'metrics': {...},          # computation statistics
    'status': 'completed',     # execution status
    'computation_time': 0.042  # runtime in seconds
}
```

### Quantum Execution Path

```
┌─ User selects module in quantum launcher
├─ launcher_quantum.py instantiates module class
│  (e.g., PowerFlow from quantum_systems/electrical/power_flow.py)
├─ Module inherits BaseQuantumSystem
│
├─ Dual Execution:
│  ├─ Branch A: execute_classical()
│  │  ├─ Use reference/baseline implementation
│  │  ├─ Time classical computation
│  │  └─ Return classical results
│  │
│  └─ Branch B: execute_quantum()
│     ├─ Initialize CTMP Engine
│     ├─ Build quantum circuit
│     ├─ Execute with quantum algorithm
│     │  (HHL, QAOA, VQE, etc.)
│     ├─ Measure execution time
│     └─ Return quantum results
│
├─ Fidelity Calculation:
│  ├─ Compare quantum_result vs classical_result
│  ├─ Calculate RMSE, MAPE, R²
│  ├─ Generate confidence intervals
│  └─ Store in metrics dict
│
├─ Visualization:
│  ├─ Chart 1: Runtime comparison
│  ├─ Chart 2: Fidelity metrics
│  └─ Chart 3: Algorithm execution trace
│
└─ launcher_quantum displays results with metrics
```

**Data Structure Returned:**
```python
{
    'classical': {
        'output': [...],
        'time': 0.034,
        'metrics': {...}
    },
    'quantum': {
        'output': [...],
        'time': 0.007,
        'metrics': {...}
    },
    'fidelity': {
        'rmse': 0.0012,
        'mape': 0.15,
        'r2': 0.9987,
        'confidence_95': (0.0010, 0.0014)
    },
    'speedup': 4.85
}
```

---

## Module Inheritance Hierarchy

### Classical Module Structure

```python
# File: classical_systems/electrical/power_flow.py

from classical_systems.core import SimulationBase, SimulationConfig

class PowerFlow(SimulationBase):
    """Implements power flow analysis using classical methods."""
    
    def __init__(self, config: SimulationConfig = None):
        super().__init__(config or SimulationConfig(
            problem_size=50,
            seed=42,
            scale=1.0
        ))
    
    def setup(self):
        """Initialize power grid structure and data."""
        # Generate test data based on problem_size
        # Initialize solver structures
        pass
    
    def solve(self) -> dict:
        """Execute power flow algorithm."""
        # Run numerical algorithm
        # Track computation time
        return {
            'output': voltage_results,
            'metrics': {'mean': ..., 'min': ..., 'max': ...},
            'status': 'completed',
            'computation_time': elapsed_time
        }
    
    def visualize(self):
        """Plot power flow network and results."""
        import matplotlib.pyplot as plt
        # Create and show visualization
```

### Quantum Module Structure

```python
# File: quantum_systems/electrical/power_flow.py

from quantum_systems.base_template import BaseQuantumSystem
from quantum_systems.core import HHLAlgorithm

class PowerFlow(BaseQuantumSystem):
    """Quantum-accelerated power flow solver using HHL algorithm."""
    
    def __init__(self, config: SimulationConfig = None):
        super().__init__(config or SimulationConfig(
            problem_size=50,
            seed=42,
            scale=1.0
        ))
        self.algorithm = HHLAlgorithm()
    
    def execute_classical(self) -> dict:
        """Run classical baseline for comparison."""
        # Use built-in reference implementation
        # Measure execution time
        return {...}
    
    def execute_quantum(self) -> dict:
        """Execute quantum-accelerated version."""
        # Build quantum circuit
        # Use HHLAlgorithm to solve linear system
        # Measure execution time
        return {...}
    
    def get_fidelity_metrics(self) -> dict:
        """Calculate accuracy metrics vs classical."""
        # Compare outputs
        # Calculate RMSE, MAPE, R²
        return {...}
```

---

## Configuration Management

All modules use a unified `SimulationConfig` dataclass:

```python
from dataclasses import dataclass

@dataclass
class SimulationConfig:
    problem_size: int = 50          # Problem dimension (scales algorithm)
    seed: int = 42                  # Random seed for reproducibility
    scale: float = 1.0              # Output scaling factor
    
    # Internal fields populated by framework
    iteration_count: int = 0        # Track iterations
    computation_time: float = 0.0   # Execution duration
    status: str = 'pending'         # 'pending', 'running', 'completed'
    status_history: list = None     # Execution trace
```

**Usage in Modules:**

```python
# Create config
config = SimulationConfig(problem_size=100, seed=123)

# Instantiate module with config
module = PowerFlow(config)

# Or use defaults
module = PowerFlow()  # Uses defaults from dataclass
```

---

## Data Flow Diagram

```
Input Layer:
  ┌──────────────────────────────┐
  │ User via Launcher GUI        │
  │ └─ Discipline selection      │
  │ └─ Module selection          │
  │ └─ Parameter configuration   │
  └──────────────────────────────┘
              │
Processing Layer (Classical):
  ┌──────────────────────────────┐
  │ 1. Module Instantiation      │
  │    └─ SimulationBase subclass│
  ├──────────────────────────────┤
  │ 2. Setup Phase               │
  │    └─ Data generation        │
  ├──────────────────────────────┤
  │ 3. Solve Phase               │
  │    ├─ Core algorithm         │
  │    └─ Timing measurement     │
  ├──────────────────────────────┤
  │ 4. Metrics Calculation       │
  │    ├─ Mean/Min/Max           │
  │    └─ Spectrum analysis      │
  ├──────────────────────────────┤
  │ 5. Visualization             │
  │    └─ Matplotlib rendering   │
  └──────────────────────────────┘
              │
Processing Layer (Quantum):
  ┌──────────────────────────────┐
  │ 1. Dual execution            │
  │    ├─ Classical branch       │
  │    │  ├─ Reference impl      │
  │    │  └─ Measure time        │
  │    └─ Quantum branch         │
  │       ├─ CTMP Engine         │
  │       ├─ Algorithm dispatch  │
  │       └─ Measure time        │
  ├──────────────────────────────┤
  │ 2. Fidelity Metrics          │
  │    ├─ RMSE calculation       │
  │    ├─ MAPE calculation       │
  │    ├─ R² calculation         │
  │    └─ Confidence intervals   │
  ├──────────────────────────────┤
  │ 3. Result Comparison         │
  │    └─ Speedup calculation    │
  ├──────────────────────────────┤
  │ 4. Visualization             │
  │    ├─ Runtime chart          │
  │    ├─ Fidelity chart         │
  │    └─ Algorithm trace        │
  └──────────────────────────────┘
              │
Output Layer:
  ┌──────────────────────────────┐
  │ Results Display              │
  │ ├─ Execution metrics         │
  │ ├─ Fidelity metrics (Q only) │
  │ ├─ Visualization charts      │
  │ └─ Optional export (JSON)    │
  └──────────────────────────────┘
```

---

## Algorithm Dispatch System

Quantum modules automatically select the appropriate algorithm based on problem type:

```python
# In BaseQuantumSystem.execute_quantum()

ALGORITHM_MAP = {
    'linear_system': HHLAlgorithm,
    'optimization': QAOAOptimizer,
    'eigenvalue': VQESolver,
    'search': GroverSearch,
    'signal_processing': QuantumFourierTransform,
    'graph_algorithm': QuantumWalk,
    'factorization': ShorAlgorithm,
    'fluid_dynamics': QuantumLatticeBoltzmann
}

# Module declares its algorithm type
class PowerFlow(BaseQuantumSystem):
    algorithm_type = 'linear_system'  # → HHL
    
    def execute_quantum(self):
        algorithm_class = ALGORITHM_MAP[self.algorithm_type]
        algorithm = algorithm_class(self.config)
        return algorithm.solve(self.quantum_state)
```

---

## Memory & Performance Patterns

### Classical Systems
- **Memory**: O(problem_size²) for matrix operations
- **Scaling**: Polynomial time (O(n³) for many algorithms)
- **Optimization**: Vectorized NumPy/SciPy operations

### Quantum Systems
- **Memory**: O(2^n) theoretical (CTMP uses tensor compression)
- **Scaling**: Exponential speedup for specific problem classes
- **Optimization**: CTMP tensor network compression for practical problems

### Benchmarking Results

From `branch_benchmark.py` (78 modules tested):

| Metric | Classical | Quantum | Speedup |
|--------|-----------|---------|---------|
| Average Time | 0.0034s | 0.0007s | **4.5x** |
| Min Time | 0.0020s | 0.0004s | 5.0x |
| Max Time | 0.0050s | 0.0012s | 4.2x |

---

## Testing & Validation Architecture

```
Test Pyramid:
       ▲
      ╱ ╲
     ╱   ╲  Integration Tests
    ╱ ─── ╲ (benchmarks, cross-module)
   ╱       ╲
  ╱─────────╲ Unit Tests
 ╱           ╲ (algorithm correctness)
╱─────────────╲ Smoke Tests
  (imports)   ╲ (all modules load)
───────────────
```

**Test Coverage:**
- ✅ **Smoke Tests**: 79/79 classical modules import, 78/78 quantum modules import
- ✅ **Unit Tests**: 6/6 core quantum algorithm tests pass
- ✅ **Integration Tests**: 78/78 benchmark pairs successful (100%)
- ✅ **Verification**: Overflow, scale, quality tests all passing

See `quantum_systems/core/tests/` for test suite.

---

## Extension Architecture

To add new modules:

1. **Inherit from base class** (SimulationBase or BaseQuantumSystem)
2. **Implement required methods** (setup, solve, visualize)
3. **Register in launcher** (add to module registry)
4. **Run benchmarks** (verify performance)

See **[ADDING_MODULES.md](./ADDING_MODULES.md)** for step-by-step guide.

---

## Key Design Decisions

| Decision | Rationale | Consequence |
|----------|-----------|-------------|
| Dual Implementation | Enable direct comparison | 2x module count but reproducible results |
| Unified Config | Consistency across modules | Easy parameter tuning and benchmarking |
| CTMP Engine | No external simulator dependency | Fast, self-contained quantum simulation |
| Reference Baselines | Built-in validation data | Modules are self-verifying |
| GUI Launchers | Low barrier to entry | Quick experimentation without coding |
| JSON Benchmarks | Portable results | Easy sharing and analysis |

---

## Performance Characteristics

### Classical Systems
- **Strengths**: Deterministic, fast for small problems, well-understood behavior
- **Weaknesses**: Exponential scaling for specific problem classes
- **Best For**: Baselines, small problem validation

### Quantum Systems
- **Strengths**: Exponential speedup for linear systems, optimization, eigenvalue problems
- **Weaknesses**: Limited to specific algorithm classes, overhead for very small problems
- **Best For**: Large-scale optimization, signal processing, search

**Speedup Observed by Discipline:**

| Discipline | Speedup |
|-----------|---------|
| Chemical | 5.7x |
| Petroleum | 5.6x |
| Biomedical | 5.5x |
| Aerospace | 4.1x |

Average across 78 modules: **4.5x**

---

## Thread Safety & Concurrency

- **Classical modules**: Thread-safe (NumPy/SciPy operations use thread pools)
- **Quantum modules**: Single-threaded execution (CTMP engine not parallelized)
- **Benchmarks**: Sequenced execution (modules run one at a time)

For parallel execution across multiple modules, create separate instances.

---

## Error Handling Strategy

```
┌─ Module Execution
├─ setup() fails
│  └─ Status: 'setup_error'
├─ solve() fails
│  └─ Status: 'computation_error'
├─ Fidelity check fails (quantum only)
│  └─ Status: 'accuracy_error'
└─ Success
   └─ Status: 'completed'
```

All errors are caught and logged in `status_history` for debugging.

---

**Next Steps:**
- Read [CLASSICAL_API.md](./CLASSICAL_API.md) for SimulationBase details
- Study [QUANTUM_API.md](./QUANTUM_API.md) for quantum engine implementation
- Explore [MODULES.md](./MODULES.md) for available simulations
- Review [ADDING_MODULES.md](./ADDING_MODULES.md) to extend the framework

---

**Last Updated**: March 2026
