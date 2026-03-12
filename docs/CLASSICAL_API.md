# Classical Systems API Reference

Complete API documentation for the classical simulation framework, including `SimulationBase`, `SimulationConfig`, and utility functions.

---

## Overview

The classical systems API provides a unified interface for deterministic simulations across all engineering disciplines. All classical modules inherit from `SimulationBase` and use `SimulationConfig` for parameter management.

**Key Principle**: All modules follow the same lifecycle pattern (setup → solve → visualize) with consistent return types and error handling.

---

## SimulationConfig Dataclass

Configuration object used by all classical modules.

**Location**: `classical_systems/core/__init__.py`

### Definition

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class SimulationConfig:
    """Configuration for simulation parameters."""
    
    problem_size: int = 50
    """Problem dimension (scales algorithm complexity). Range: 10-1000."""
    
    seed: int = 42
    """Random seed for reproducibility. Use 0 for no seeding."""
    
    scale: float = 1.0
    """Output scaling factor. Applied to results for unit conversion."""
    
    # Internal state (auto-populated by framework)
    iteration_count: int = 0
    """Total iterations executed (populated after solve)."""
    
    computation_time: float = 0.0
    """Execution duration in seconds (populated after solve)."""
    
    status: str = 'pending'
    """Current execution status: 'pending', 'running', 'completed', 'error'."""
    
    status_history: List[str] = field(default_factory=list)
    """Timeline of status changes during execution."""
```

### Usage Examples

**Default Configuration:**
```python
from classical_systems.core import SimulationConfig

config = SimulationConfig()
# problem_size=50, seed=42, scale=1.0
```

**Custom Configuration:**
```python
config = SimulationConfig(
    problem_size=200,
    seed=123,
    scale=2.5
)
```

**Accessing Configuration:**
```python
print(config.problem_size)      # 200
print(config.seed)              # 123
print(config.scale)             # 2.5
print(config.computation_time)  # Updated after solve()
```

---

## SimulationBase Abstract Class

Base class for all classical simulation modules. Defines the standard interface and lifecycle.

**Location**: `classical_systems/core/__init__.py`

### Class Definition

```python
class SimulationBase:
    """Base class for all classical simulation modules."""
    
    def __init__(self, config: SimulationConfig = None):
        """Initialize simulation with configuration."""
        
    def setup(self) -> None:
        """Prepare simulation data and structures.
        
        Called once before solve(). Should:
        - Generate test data
        - Initialize algorithm structures
        - Verify configuration validity
        """
        
    def solve(self) -> Dict[str, Any]:
        """Execute the core simulation algorithm.
        
        Returns:
            dict with keys:
                'output': List or array of results
                'metrics': Dict with statistics
                'status': str, 'completed' or error description
                'computation_time': float, seconds elapsed
        """
        
    def visualize(self) -> None:
        """Display results using matplotlib.
        
        Creates figure(s) showing:
        - Primary results
        - Metrics/statistics
        - Algorithm traces (if applicable)
        """
        
    def get_metrics(self) -> Dict[str, float]:
        """Calculate and return execution metrics.
        
        Returns:
            dict with keys:
                'mean': float, mean of output
                'min': float, minimum value
                'max': float, maximum value
                'std_dev': float, standard deviation
                'spectrum_peaks': List[float], frequency domain peaks
        """
        
    # Utility methods
    
    def generate_series(self, length: int) -> List[float]:
        """Generate a test data series for the module."""
        
    def discrete_spectrum(self, signal: List[float]) -> List[float]:
        """Compute discrete Fourier spectrum of signal."""
```

### Methods in Detail

#### `__init__(config: SimulationConfig = None)`

Initialize the simulation module.

```python
from classical_systems.electrical.power_flow import PowerFlow
from classical_systems.core import SimulationConfig

# With default config
sim = PowerFlow()

# With custom config
config = SimulationConfig(problem_size=100, seed=42)
sim = PowerFlow(config)
```

#### `setup() -> None`

Prepare data structures and test data. Always called before `solve()`.

```python
class PowerFlow(SimulationBase):
    def setup(self):
        # Generate power grid structure
        self.nodes = self.config.problem_size
        self.edges = []
        
        # Initialize solver
        self.admittance_matrix = np.zeros((self.nodes, self.nodes))
        
        # Generate test data
        self.test_voltages = self.generate_series(self.nodes)
        self.test_loads = self.generate_series(self.nodes)
```

**Calling:**
```python
sim = PowerFlow()
sim.setup()  # Prepare internal structures
```

#### `solve() -> Dict[str, Any]`

Execute the core algorithm. Must be called after `setup()`.

**Return Format:**
```python
{
    'output': [1.0, 0.98, 0.95, ...],  # Main results
    'metrics': {                         # Statistics
        'mean': 0.975,
        'min': 0.92,
        'max': 1.02,
        'iteration_count': 142
    },
    'status': 'completed',               # Execution status
    'computation_time': 0.042            # Elapsed seconds
}
```

**Usage:**
```python
sim = PowerFlow(SimulationConfig(problem_size=100))
sim.setup()
result = sim.solve()

print(result['output'])         # Voltage results
print(result['metrics']['mean']) # Average voltage
print(result['computation_time']) # 0.042 seconds
```

#### `visualize() -> None`

Display results using matplotlib. Call after `solve()`.

```python
sim = PowerFlow()
sim.setup()
sim.solve()
sim.visualize()  # Opens matplotlib figure
```

#### `get_metrics() -> Dict[str, float]`

Calculate detailed metrics from last `solve()`.

**Return Format:**
```python
{
    'mean': 0.975,
    'min': 0.92,
    'max': 1.02,
    'std_dev': 0.032,
    'spectrum_peaks': [0.15, 0.42, 0.89],  # Frequency domain peaks
    'spectrum_energy': 42.3  # Total spectrum energy
}
```

**Usage:**
```python
sim = PowerFlow()
sim.setup()
sim.solve()

metrics = sim.get_metrics()
print(f"Mean: {metrics['mean']:.4f}")
print(f"Std Dev: {metrics['std_dev']:.4f}")
print(f"Spectrum: {metrics['spectrum_peaks']}")
```

#### `generate_series(length: int) -> List[float]`

Generate a test data series of specified length.

```python
sim = PowerFlow()
series = sim.generate_series(100)
# Returns list of 100 random floats (seeded by config.seed)
```

#### `discrete_spectrum(signal: List[float]) -> List[float]`

Compute frequency domain spectrum using FFT.

```python
signal = [1.0, 0.5, 0.3, 0.1, 0.2]
spectrum = sim.discrete_spectrum(signal)
# Returns magnitude spectrum in frequency domain
```

---

## Complete Usage Example

**Example: Power Flow Analysis Module**

```python
from classical_systems.electrical.power_flow import PowerFlow
from classical_systems.core import SimulationConfig

# Create configuration
config = SimulationConfig(
    problem_size=50,      # 50-node power grid
    seed=42,              # Reproducible randomness
    scale=1.0             # Results scaling (for per-unit analysis)
)

# Instantiate module
sim = PowerFlow(config)

# Phase 1: Setup
print("Setting up simulation...")
sim.setup()
print(f"Initialized {sim.config.problem_size}-node power grid")

# Phase 2: Solve
print("Running power flow solver...")
result = sim.solve()
print(f"✓ Completed in {result['computation_time']:.4f}s")
print(f"✓ Mean voltage: {result['metrics']['mean']:.4f} pu")

# Phase 3: Analyze
metrics = sim.get_metrics()
print(f"Standard deviation: {metrics['std_dev']:.4f}")
print(f"Voltage range: {metrics['min']:.4f} - {metrics['max']:.4f}")
print(f"Frequency peaks: {metrics['spectrum_peaks']}")

# Phase 4: Visualize
print("Generating visualization...")
sim.visualize()
```

---

## Module Implementation Template

To create a new classical module:

**File: `classical_systems/[discipline]/[module_name].py`**

```python
from classical_systems.core import SimulationBase, SimulationConfig
import numpy as np
import matplotlib.pyplot as plt

class MyModule(SimulationBase):
    """Description of what this module simulates."""
    
    def __init__(self, config: SimulationConfig = None):
        super().__init__(config or SimulationConfig())
        # Initialize module-specific attributes
        self.algorithm_state = None
    
    def setup(self):
        """Generate test data and initialize algorithm."""
        # Generate problem data
        self.data = self.generate_series(self.config.problem_size)
        
        # Initialize algorithm-specific structures
        self.algorithm_state = np.zeros((self.config.problem_size, 1))
    
    def solve(self) -> dict:
        """Run the core algorithm."""
        import time
        start_time = time.time()
        
        try:
            # Execute algorithm
            self.config.status = 'running'
            
            output = []
            iteration = 0
            while iteration < self.config.problem_size:
                # Simulation logic
                step_result = self._algorithm_step(self.data[iteration])
                output.append(step_result)
                iteration += 1
                self.config.iteration_count = iteration
            
            # Scale results
            output = [x * self.config.scale for x in output]
            
            elapsed = time.time() - start_time
            self.config.computation_time = elapsed
            self.config.status = 'completed'
            
            return {
                'output': output,
                'metrics': {'mean': np.mean(output), 'std_dev': np.std(output)},
                'status': 'completed',
                'computation_time': elapsed
            }
        
        except Exception as e:
            self.config.status = 'error'
            return {
                'output': [],
                'metrics': {},
                'status': f'error: {str(e)}',
                'computation_time': time.time() - start_time
            }
    
    def visualize(self):
        """Plot results."""
        if not hasattr(self, '_last_output'):
            print("No results to visualize. Run solve() first.")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot 1: Results vs data
        ax1.plot(self.data, label='Input')
        ax1.plot(self._last_output, label='Output')
        ax1.set_xlabel('Index')
        ax1.set_ylabel('Value')
        ax1.legend()
        ax1.set_title('Input vs Output')
        
        # Plot 2: Spectrum
        spectrum = self.discrete_spectrum(self._last_output)
        ax2.plot(np.abs(spectrum))
        ax2.set_xlabel('Frequency')
        ax2.set_ylabel('Magnitude')
        ax2.set_title('Frequency Spectrum')
        
        plt.tight_layout()
        plt.show()
    
    def _algorithm_step(self, data_point):
        """Execute one step of algorithm."""
        # Module-specific algorithm logic
        return data_point * 1.1  # Placeholder

# For running module directly
def main():
    config = SimulationConfig(problem_size=50, seed=42)
    module = MyModule(config)
    module.setup()
    result = module.solve()
    module.visualize()
    return result

if __name__ == "__main__":
    main()
```

---

## Error Handling

Classical modules use a uniform error handling pattern:

```python
def solve(self) -> dict:
    """Solve with error handling."""
    try:
        # Algorithm execution
        output = self._run_algorithm()
        return {
            'output': output,
            'metrics': self.get_metrics(),
            'status': 'completed',
            'computation_time': elapsed_time
        }
    except ValueError as e:
        return {
            'output': [],
            'metrics': {},
            'status': f'parameter_error: {str(e)}',
            'computation_time': elapsed_time
        }
    except RuntimeError as e:
        return {
            'output': [],
            'metrics': {},
            'status': f'computation_error: {str(e)}',
            'computation_time': elapsed_time
        }
```

---

## Performance Characteristics

| Aspect | Notes |
|--------|-------|
| **Memory** | O(problem_size²) for matrix operations |
| **Time** | O(n³) typical for linear algebra, O(n log n) for FFT |
| **Scaling** | problem_size parameter controls computational load |
| **Reproducibility** | Controlled by seed parameter (default 42) |
| **Parallelization** | NumPy/SciPy use thread pools automatically |

---

## Common Patterns

### Pattern 1: Linear System Solvers

```python
class LinearSystemModule(SimulationBase):
    def solve(self) -> dict:
        # Build system matrix A and vector b
        A = self._build_system_matrix()
        b = self._build_rhs_vector()
        
        # Solve Ax = b
        x = np.linalg.solve(A, b)
        
        return {
            'output': x,
            'metrics': self._compute_metrics(x),
            'status': 'completed',
            'computation_time': elapsed_time
        }
```

### Pattern 2: Iterative Algorithms

```python
class IterativeModule(SimulationBase):
    def solve(self) -> dict:
        output = []
        state = self._initialize_state()
        
        for iteration in range(self.config.problem_size):
            state = self._update_step(state)
            output.append(state)
            self.config.iteration_count = iteration + 1
        
        return {...}
```

### Pattern 3: Data Processing Pipelines

```python
class DataProcessingModule(SimulationBase):
    def solve(self) -> dict:
        # Process input data through stages
        stage1 = self._preprocess(self.data)
        stage2 = self._transform(stage1)
        output = self._postprocess(stage2)
        
        return {...}
```

---

## Inheritance Hierarchy

```
SimulationBase (abstract)
├── Aerospace Modules
│   ├── PanelMethod
│   ├── Turbojet
│   └── ...
├── Electrical Modules
│   ├── PowerFlow
│   ├── CircuitSimulator
│   └── ...
└── [12 other disciplines]
```

Each module inherits `SimulationBase` and implements the 5 required methods.

---

## Testing Your Module

```python
# test_my_module.py
from classical_systems.electrical.my_module import MyModule
from classical_systems.core import SimulationConfig

def test_module_lifecycle():
    """Test basic setup, solve, visualize flow."""
    config = SimulationConfig(problem_size=10, seed=42)
    module = MyModule(config)
    
    # Setup
    module.setup()
    assert hasattr(module, 'data')
    
    # Solve
    result = module.solve()
    assert result['status'] == 'completed'
    assert len(result['output']) > 0
    
    # Metrics
    metrics = module.get_metrics()
    assert 'mean' in metrics
    assert 'std_dev' in metrics

def test_reproducibility():
    """Same seed = same results."""
    config1 = SimulationConfig(problem_size=50, seed=42)
    config2 = SimulationConfig(problem_size=50, seed=42)
    
    m1 = MyModule(config1)
    m2 = MyModule(config2)
    
    m1.setup()
    m1.solve()
    m2.setup()
    m2.solve()
    
    # Results should be identical
    assert np.allclose(m1._last_output, m2._last_output)
```

Run with:
```bash
pytest test_my_module.py -v
```

---

## Integration with Launcher

To register a new module in the classical launcher:

**In `classical_systems/launcher.py`:**

```python
MODULE_REGISTRY = {
    'electrical': {
        'power_flow': PowerFlow,
        'circuit_simulator': CircuitSimulator,
        'my_module': MyModule,  # Add new module here
        ...
    },
    ...
}
```

---

## Utilities

### generate_series(length: int) -> List[float]

Generates reproducible random series using configured seed.

```python
sim = PowerFlow(SimulationConfig(seed=42))
series = sim.generate_series(100)
# Each call with seed=42 produces identical series
```

### discrete_spectrum(signal: List[float]) -> List[float]

Computes FFT magnitude spectrum.

```python
signal = [1, 0.5, 0.3, 0.1]
spectrum = sim.discrete_spectrum(signal)
# Returns magnitude spectrum (normalized)
```

---

## Next Steps

- **Implementation**: See [ADDING_MODULES.md](./ADDING_MODULES.md) for step-by-step guide
- **Architecture**: Review [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- **Modules**: Browse [MODULES.md](./MODULES.md) for existing examples
- **Comparison**: Study [QUANTUM_API.md](./QUANTUM_API.md) for quantum equivalents

---

**Last Updated**: March 2026  
**API Version**: 1.0  
**Stability**: Stable
