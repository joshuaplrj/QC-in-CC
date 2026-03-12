# Adding Modules: Extension Guide

Step-by-step guide for adding new simulation modules to the QC in CC framework for both classical and quantum systems.

---

## Overview

Adding a module involves:
1. Creating a Python class inheriting from the appropriate base (`SimulationBase` or `BaseQuantumSystem`)
2. Implementing required methods (setup, solve, visualize, etc.)
3. Registering in the module launcher
4. Testing and benchmarking

**Time Required**: 2-4 hours per module (classical + quantum)

---

## Part 1: Adding a Classical Module

### Step 1: Create Module File

**Location**: `classical_systems/[discipline]/[module_name].py`

**File Naming**: Use lowercase with underscores
- ✓ Good: `power_flow.py`, `circuit_simulator.py`
- ✗ Bad: `PowerFlow.py`, `power-flow.py`

### Step 2: Implement Module Class

```python
# File: classical_systems/electrical/my_power_flow.py

from classical_systems.core import SimulationBase, SimulationConfig
import numpy as np
import matplotlib.pyplot as plt
import time

class MyPowerFlow(SimulationBase):
    """Analyze electrical power flow in a grid network.
    
    Solves the power flow equations to find node voltages and
    line flows given loads and generation at each bus.
    
    Problem Type: Linear System (Ax = b)
    Complexity: O(n³) for n buses
    """
    
    def __init__(self, config: SimulationConfig = None):
        """Initialize power flow simulator.
        
        Args:
            config: SimulationConfig with problem_size, seed, scale
        """
        super().__init__(config or SimulationConfig(
            problem_size=30,  # Number of buses
            seed=42,
            scale=1.0
        ))
        
        # Initialize module-specific attributes
        self.admittance_matrix = None
        self.test_loads = None
        self.test_generation = None
        self._last_output = None
    
    def setup(self):
        """Initialize power grid data and algorithm structures."""
        n = self.config.problem_size
        
        # Create test data using seed for reproducibility
        self.test_loads = self.generate_series(n)
        self.test_generation = self.generate_series(n)
        
        # Create admittance matrix (sparse for realism)
        # Simplified: tridiagonal network
        diag = 4.0 * np.ones(n)
        off_diag = -1.0 * np.ones(n - 1)
        self.admittance_matrix = (
            np.diag(diag) + 
            np.diag(off_diag, 1) + 
            np.diag(off_diag, -1)
        )
        
        # Ensure configuration is marked as setup complete
        self.config.status = 'ready'
    
    def solve(self) -> dict:
        """Execute power flow algorithm.
        
        Returns:
            dict with 'output', 'metrics', 'status', 'computation_time'
        """
        start_time = time.time()
        
        try:
            self.config.status = 'running'
            
            # Prepare right-hand side (loads - generation)
            rhs = self.test_loads - self.test_generation
            rhs = rhs * self.config.scale
            
            # Solve linear system Ax = V (voltages)
            voltages = np.linalg.solve(self.admittance_matrix, rhs)
            
            # Output is the voltage magnitudes (per-unit)
            output = np.abs(voltages).tolist()
            self._last_output = output
            
            elapsed = time.time() - start_time
            self.config.computation_time = elapsed
            self.config.iteration_count = len(output)
            self.config.status = 'completed'
            
            return {
                'output': output,
                'metrics': {
                    'mean': np.mean(output),
                    'min': np.min(output),
                    'max': np.max(output),
                    'std_dev': np.std(output)
                },
                'status': 'completed',
                'computation_time': elapsed
            }
        
        except Exception as e:
            self.config.status = 'error'
            elapsed = time.time() - start_time
            return {
                'output': [],
                'metrics': {},
                'status': f'error: {str(e)}',
                'computation_time': elapsed
            }
    
    def visualize(self):
        """Display power flow results with matplotlib."""
        if not hasattr(self, '_last_output') or not self._last_output:
            print("No results to visualize. Run solve() first.")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot 1: Voltage profile
        voltages = self._last_output
        buses = np.arange(len(voltages))
        ax1.bar(buses, voltages, color='steelblue', alpha=0.7)
        ax1.axhline(y=1.0, color='red', linestyle='--', label='Nominal (1.0 pu)')
        ax1.set_xlabel('Bus Number')
        ax1.set_ylabel('Voltage (per-unit)')
        ax1.set_title('Power Flow - Voltage Profile')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Spectrum
        spectrum = self.discrete_spectrum(voltages)
        freqs = np.arange(len(spectrum))
        ax2.plot(freqs, np.abs(spectrum), 'o-', color='darkgreen', alpha=0.7)
        ax2.set_xlabel('Frequency')
        ax2.set_ylabel('Magnitude')
        ax2.set_title('Voltage Spectrum')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def get_metrics(self) -> dict:
        """Calculate detailed metrics from last solve()."""
        if not self._last_output:
            return {}
        
        output = np.array(self._last_output)
        spectrum = self.discrete_spectrum(self._last_output)
        
        return {
            'mean': float(np.mean(output)),
            'min': float(np.min(output)),
            'max': float(np.max(output)),
            'std_dev': float(np.std(output)),
            'spectrum_peaks': np.argsort(np.abs(spectrum))[-3:].tolist(),
            'spectrum_energy': float(np.sum(np.abs(spectrum) ** 2))
        }


# Function to run module directly
def main():
    """Demonstration of module execution."""
    config = SimulationConfig(problem_size=50, seed=42)
    module = MyPowerFlow(config)
    
    print("Setting up power flow solver...")
    module.setup()
    
    print("Running power flow analysis...")
    result = module.solve()
    
    print(f"✓ Completed in {result['computation_time']:.4f}s")
    print(f"  Mean voltage: {result['metrics']['mean']:.4f} pu")
    print(f"  Voltage range: {result['metrics']['min']:.4f} - {result['metrics']['max']:.4f}")
    
    print("Generating visualization...")
    module.visualize()
    
    return result


if __name__ == "__main__":
    main()
```

### Step 3: Test Locally

```bash
# Run module directly
python classical_systems/electrical/my_power_flow.py

# Test with different problem sizes
python -c "
from classical_systems.electrical.my_power_flow import MyPowerFlow
from classical_systems.core import SimulationConfig

for size in [10, 50, 100]:
    config = SimulationConfig(problem_size=size)
    module = MyPowerFlow(config)
    module.setup()
    result = module.solve()
    print(f'Size {size}: {result[\"computation_time\"]:.4f}s')
"
```

### Step 4: Register in Launcher

Edit `classical_systems/launcher.py`:

```python
# Find the MODULE_REGISTRY dict

MODULE_REGISTRY = {
    'electrical': {
        'power_flow': PowerFlow,
        'circuit_simulator': CircuitSimulator,
        'my_power_flow': MyPowerFlow,  # Add this line
        ...
    },
    ...
}
```

### Step 5: Test in Launcher

```bash
# Launch the GUI
python classical_systems/launcher.py

# Select: Electrical → my_power_flow
# Configure problem size, run, verify visualization
```

---

## Part 2: Adding a Quantum Module

### Step 1: Create Quantum Module File

**Location**: `quantum_systems/[discipline]/[module_name].py`

### Step 2: Implement Quantum Module Class

```python
# File: quantum_systems/electrical/my_power_flow.py

from quantum_systems.base_template import BaseQuantumSystem
from quantum_systems.core import HHLAlgorithm, CTMP_Engine
from classical_systems.core import SimulationConfig
import numpy as np
import matplotlib.pyplot as plt
import time

class MyPowerFlow(BaseQuantumSystem):
    """Quantum-accelerated power flow analysis.
    
    Uses HHL algorithm to solve linear power flow equations.
    Includes built-in classical baseline for accuracy comparison.
    """
    
    # Declare algorithm type (auto-selects HHL)
    algorithm_type = 'linear_system'
    
    def __init__(self, config: SimulationConfig = None):
        """Initialize quantum power flow module.
        
        Args:
            config: SimulationConfig with problem_size, seed, scale
        """
        super().__init__(config or SimulationConfig(
            problem_size=30,
            seed=42,
            scale=1.0
        ))
        
        # Initialize quantum components
        self.algorithm = HHLAlgorithm()
        
        # Store results for fidelity comparison
        self._classical_output = None
        self._quantum_output = None
        self._classical_time = None
        self._quantum_time = None
        
        # Initialize grids
        self.admittance_matrix = None
        self.test_loads = None
    
    def execute_classical(self) -> dict:
        """Run classical power flow solver (baseline).
        
        Returns:
            dict with 'output', 'time', 'metrics'
        """
        start = time.time()
        
        # Generate test data (identical seed for comparison)
        n = self.config.problem_size
        self.test_loads = self.generate_series(n)
        
        # Create admittance matrix
        diag = 4.0 * np.ones(n)
        off_diag = -1.0 * np.ones(n - 1)
        self.admittance_matrix = (
            np.diag(diag) + 
            np.diag(off_diag, 1) + 
            np.diag(off_diag, -1)
        )
        
        # Classical solve: Ax = b
        rhs = self.test_loads * self.config.scale
        voltages = np.linalg.solve(self.admittance_matrix, rhs)
        output = np.abs(voltages).tolist()
        
        elapsed = time.time() - start
        self._classical_output = output
        self._classical_time = elapsed
        
        return {
            'output': output,
            'time': elapsed,
            'metrics': {
                'mean': np.mean(output),
                'std_dev': np.std(output)
            }
        }
    
    def execute_quantum(self) -> dict:
        """Run quantum-accelerated power flow solver.
        
        Uses HHL algorithm for linear system solution.
        
        Returns:
            dict with 'output', 'time', 'metrics', 'circuit_trace'
        """
        start = time.time()
        
        # Use admittance matrix from classical execution
        # (if not run, initialize it)
        if self.admittance_matrix is None:
            n = self.config.problem_size
            diag = 4.0 * np.ones(n)
            off_diag = -1.0 * np.ones(n - 1)
            self.admittance_matrix = (
                np.diag(diag) + 
                np.diag(off_diag, 1) + 
                np.diag(off_diag, -1)
            )
        
        if self.test_loads is None:
            self.test_loads = self.generate_series(self.config.problem_size)
        
        # Quantum solve using HHL
        rhs = self.test_loads * self.config.scale
        
        # HHL algorithm
        voltages = self.algorithm.solve(self.admittance_matrix, rhs)
        output = np.abs(voltages).tolist()
        
        elapsed = time.time() - start
        self._quantum_output = output
        self._quantum_time = elapsed
        
        # Build circuit trace for display
        circuit_trace = [
            {'gate': 'Hadamard', 'qubits': [0, 1, 2, 3]},
            {'gate': 'QPE_Init', 'qubits': [0, 1]},
            {'gate': 'Controlled-e^iAt', 'qubits': [0, 1]},
            {'gate': 'QPE_Measure', 'qubits': [0, 1]},
            {'gate': 'Controlled_Rotation', 'qubits': [2, 3]},
            {'gate': 'Uncompute', 'qubits': [0, 1]}
        ]
        
        return {
            'output': output,
            'time': elapsed,
            'metrics': {
                'mean': np.mean(output),
                'std_dev': np.std(output)
            },
            'circuit_trace': circuit_trace
        }
    
    def get_fidelity_metrics(self) -> dict:
        """Calculate accuracy metrics comparing quantum vs classical.
        
        Returns:
            dict with RMSE, MAPE, R², confidence intervals
        """
        if self._classical_output is None or self._quantum_output is None:
            return {}
        
        c = np.array(self._classical_output)
        q = np.array(self._quantum_output)
        
        # RMSE
        rmse = np.sqrt(np.mean((q - c) ** 2))
        
        # MAPE
        mape = np.mean(np.abs((q - c) / (np.abs(c) + 1e-10))) * 100
        
        # R²
        ss_res = np.sum((q - c) ** 2)
        ss_tot = np.sum((c - np.mean(c)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 1.0
        
        # 95% Confidence Interval
        errors = np.abs(q - c)
        mean_err = np.mean(errors)
        std_err = np.std(errors)
        ci_lower = max(0, mean_err - 1.96 * std_err)
        ci_upper = mean_err + 1.96 * std_err
        
        # Speedup
        speedup = self._classical_time / self._quantum_time if self._quantum_time > 0 else 0
        
        return {
            'rmse': rmse,
            'mape': mape,
            'r2': r2,
            'confidence_95': (ci_lower, ci_upper),
            'speedup': speedup,
            'correlation': np.corrcoef(c, q)[0, 1] if len(c) > 1 else 1.0
        }
    
    def visualize(self):
        """Display results with runtime and fidelity charts."""
        if not self._classical_output or not self._quantum_output:
            print("No results to visualize. Run both execute_* methods first.")
            return
        
        fig = plt.figure(figsize=(15, 5))
        
        # Chart 1: Runtime Comparison
        ax1 = fig.add_subplot(131)
        times = [self._classical_time, self._quantum_time]
        bars = ax1.bar(['Classical', 'Quantum'], times, color=['steelblue', 'darkgreen'])
        ax1.set_ylabel('Time (seconds)')
        ax1.set_title('Runtime Comparison')
        # Add speedup label
        speedup = self._classical_time / self._quantum_time
        ax1.text(0.5, max(times) * 0.8, f'{speedup:.2f}x', 
                ha='center', fontsize=12, fontweight='bold')
        
        # Chart 2: Fidelity Metrics
        ax2 = fig.add_subplot(132)
        fidelity = self.get_fidelity_metrics()
        metrics = ['RMSE', 'MAPE', 'R²']
        values = [
            fidelity['rmse'] * 100,  # Scale for visibility
            fidelity['mape'],
            fidelity['r2'] * 100
        ]
        bars = ax2.bar(metrics, values, color=['coral', 'orange', 'green'])
        ax2.set_ylabel('Value')
        ax2.set_title('Fidelity Metrics')
        
        # Chart 3: Output Comparison
        ax3 = fig.add_subplot(133)
        c = self._classical_output
        q = self._quantum_output
        x = np.arange(len(c))
        ax3.plot(x, c, 'o-', label='Classical', alpha=0.7)
        ax3.plot(x, q, 's--', label='Quantum', alpha=0.7)
        ax3.set_xlabel('Bus')
        ax3.set_ylabel('Voltage (pu)')
        ax3.set_title('Output Comparison')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


def main():
    """Demonstration of quantum power flow module."""
    config = SimulationConfig(problem_size=30, seed=42)
    module = MyPowerFlow(config)
    
    print("Running classical baseline...")
    classical = module.execute_classical()
    print(f"✓ Classical: {classical['time']:.4f}s")
    
    print("Running quantum solver...")
    quantum = module.execute_quantum()
    print(f"✓ Quantum: {quantum['time']:.4f}s")
    
    print("Calculating fidelity metrics...")
    fidelity = module.get_fidelity_metrics()
    print(f"  RMSE: {fidelity['rmse']:.6f}")
    print(f"  MAPE: {fidelity['mape']:.2f}%")
    print(f"  R²: {fidelity['r2']:.4f}")
    print(f"  Speedup: {fidelity['speedup']:.2f}x")
    
    print("Generating visualization...")
    module.visualize()


if __name__ == "__main__":
    main()
```

### Step 3: Register in Quantum Launcher

Edit `quantum_systems/launcher_quantum.py`:

```python
# Find MODULE_REGISTRY

MODULE_REGISTRY = {
    'electrical': {
        'power_flow': PowerFlow,
        'circuit_simulator': CircuitSimulator,
        'my_power_flow': MyPowerFlow,  # Add this line
        ...
    },
    ...
}
```

### Step 4: Test in Quantum Launcher

```bash
# Launch quantum GUI
python quantum_systems/launcher_quantum.py

# Select: Electrical → my_power_flow
# Configure, execute, verify metrics
```

---

## Step 5: Benchmarking Your Module

```bash
# Run benchmarks to see your module's performance
python branch_benchmark.py

# Check results
grep "my_power_flow" benchmark_summary.md

# Or parse JSON
python -c "
import json
with open('benchmark_results.json') as f:
    results = json.load(f)
    if 'electrical' in results['modules']:
        module = results['modules']['electrical'].get('my_power_flow', {})
        if module:
            print(f'Speedup: {module.get(\"speedup\", \"N/A\")}x')
"
```

---

## Testing Best Practices

### Unit Test Template

```python
# test_my_module.py
import pytest
from classical_systems.electrical.my_power_flow import MyPowerFlow
from quantum_systems.electrical.my_power_flow import MyPowerFlow as MyPowerFlowQuantum
from classical_systems.core import SimulationConfig

def test_classical_module_basic():
    """Test basic classical module functionality."""
    config = SimulationConfig(problem_size=10, seed=42)
    module = MyPowerFlow(config)
    
    module.setup()
    assert module.admittance_matrix is not None
    assert module.test_loads is not None

def test_classical_solve():
    """Test solve execution."""
    config = SimulationConfig(problem_size=10, seed=42)
    module = MyPowerFlow(config)
    module.setup()
    
    result = module.solve()
    assert result['status'] == 'completed'
    assert len(result['output']) > 0
    assert result['computation_time'] > 0

def test_reproducibility():
    """Same seed produces same results."""
    config1 = SimulationConfig(problem_size=10, seed=42)
    config2 = SimulationConfig(problem_size=10, seed=42)
    
    m1 = MyPowerFlow(config1)
    m2 = MyPowerFlow(config2)
    
    m1.setup()
    m1.solve()
    m2.setup()
    m2.solve()
    
    assert m1._last_output == m2._last_output

def test_quantum_module_dual_execution():
    """Test quantum module classical and quantum branches."""
    config = SimulationConfig(problem_size=10, seed=42)
    module = MyPowerFlowQuantum(config)
    
    classical = module.execute_classical()
    quantum = module.execute_quantum()
    fidelity = module.get_fidelity_metrics()
    
    assert classical['time'] > 0
    assert quantum['time'] > 0
    assert fidelity['r2'] > 0.99

# Run tests
# pytest test_my_module.py -v
```

---

## Checklist for New Module

- [ ] Class inherits from correct base (SimulationBase or BaseQuantumSystem)
- [ ] `__init__` calls `super().__init__()` with default config
- [ ] `setup()` initializes all data structures
- [ ] `solve()` returns dict with 'output', 'metrics', 'status', 'computation_time'
- [ ] `visualize()` creates matplotlib figure (classical) or multi-chart display (quantum)
- [ ] `get_metrics()` returns dict with at least 'mean', 'min', 'max', 'std_dev'
- [ ] Module has `main()` function for direct execution
- [ ] Module works with different `problem_size` values
- [ ] Results are reproducible with same seed
- [ ] Module registered in appropriate launcher
- [ ] Module appears in launcher GUI and functions correctly
- [ ] Benchmarks run successfully
- [ ] Speedup is in expected range (3.5-5.7x for quantum)
- [ ] Accuracy metrics are excellent (RMSE < 0.01, R² > 0.99)
- [ ] Unit tests pass
- [ ] Code has docstrings for class and methods
- [ ] File is in correct directory structure

---

## Common Mistakes to Avoid

1. **Not calling `super().__init__()`**: Module won't inherit base functionality
2. **Forgetting to scale results**: Output doesn't use `self.config.scale`
3. **Not tracking `computation_time`**: Can't measure performance
4. **Non-deterministic results**: Different seeds don't produce consistent results
5. **Missing error handling**: Exceptions crash without informative messages
6. **Not testing visualization**: Charts fail to display at runtime
7. **Quantum without classical**: Can't calculate fidelity metrics
8. **Wrong return type**: `solve()` must return dict, not just numpy array
9. **Hardcoded problem size**: Module doesn't scale with `config.problem_size`
10. **Not registering in launcher**: Module exists but not accessible via GUI

---

## Tips for Better Modules

- Use **meaningful variable names**: `admittance_matrix` instead of `A`
- **Add type hints**: `def solve(self) -> dict:`
- **Write docstrings**: Explain problem, algorithm, parameters
- **Validate inputs**: Check that matrices are invertible, vectors are right size
- **Handle edge cases**: problem_size=1, negative loads, singular matrices
- **Add progress tracking**: Update `self.config.iteration_count` in loops
- **Test with varied sizes**: problem_size = [5, 10, 50, 100, 200]
- **Compare results**: Classical vs numerical library (numpy.linalg)
- **Profile performance**: Use `timeit` to find bottlenecks
- **Optimize hot paths**: Inner loops benefit from vectorization

---

**Last Updated**: March 2026  
**Template Version**: 1.0  
**Example Modules**: 157 total implemented
