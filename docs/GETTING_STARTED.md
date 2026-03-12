# Getting Started with QC in CC

A step-by-step guide to install, configure, and run QC in CC simulations.

---

## System Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 2GB minimum (4GB+ recommended for benchmarks)
- **Disk Space**: ~500MB for installation and dependencies

---

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "QB in CC"
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install numpy scipy matplotlib networkx customtkinter
```

**Optional** (for benchmarking and testing):
```bash
pip install pytest
```

### Step 4: Verify Installation

```bash
python -c "import numpy, scipy, matplotlib, networkx, customtkinter; print('✓ All dependencies installed')"
```

Test importing the frameworks:
```bash
python -c "from classical_systems.core import SimulationBase, SimulationConfig; print('✓ Classical systems ready')"
python -c "from quantum_systems.base_template import BaseQuantumSystem; print('✓ Quantum systems ready')"
```

If all tests pass, installation is complete! 🎉

---

## Running Classical Simulations

### Option 1: GUI Launcher (Recommended)

Launch the interactive GUI:
```bash
python classical_systems/launcher.py
```

**Usage:**
1. Window opens showing all 14 disciplines
2. Click a discipline to expand and see available modules
3. Select a module
4. Configure parameters (problem size, random seed, scale) or use defaults
5. Click "Run" to execute
6. View results in real-time (status, metrics, visualization)
7. Export or save results if desired

### Option 2: Run Single Module (Python)

```python
from classical_systems.electrical.power_flow import main

result = main()
# result contains: output, metrics, status
print(result)
```

### Option 3: Programmatic Usage

```python
from classical_systems.electrical.power_flow import PowerFlow
from classical_systems.core import SimulationConfig

# Configure
config = SimulationConfig(problem_size=100, seed=42, scale=1.0)
sim = PowerFlow(config)

# Run
sim.setup()
sim.solve()
metrics = sim.get_metrics()

# Visualize
sim.visualize()
```

---

## Running Quantum Simulations

### Option 1: GUI Launcher (Recommended)

Launch the modern quantum UI:
```bash
python quantum_systems/launcher_quantum.py
```

**Features:**
- Dark mode with blue theme
- Discipline-based filtering
- Algorithm display for each module
- Real-time execution tracking
- Fidelity metrics visualization

**Usage:**
1. Select a discipline from the left panel
2. Choose a module from the card grid
3. Configure quantum parameters (problem size, shots, optimization rounds)
4. Click "Execute"
5. Monitor progress with runtime and fidelity charts
6. View results showing classical vs quantum outputs

### Option 2: Run Single Module (Python)

```python
from quantum_systems.electrical.power_flow import PowerFlow

app = PowerFlow()
app.run()  # Opens results window with visualizations
```

### Option 3: Programmatic Usage

```python
from quantum_systems.electrical.power_flow import PowerFlow
from classical_systems.core import SimulationConfig

config = SimulationConfig(problem_size=100, seed=42, scale=1.0)
app = PowerFlow(config)

# Execute both classical and quantum
classical_result = app.execute_classical()
quantum_result = app.execute_quantum()

# Get metrics
fidelity = app.get_fidelity_metrics()
print(f"RMSE: {fidelity['rmse']}, R²: {fidelity['r2']}")
```

---

## Running Benchmarks

### Benchmark Types

**1. Classical vs Quantum Comparison** (all 78+ modules)
```bash
python branch_benchmark.py
```

Output: Performance comparison, speedup metrics, JSON export

**2. Three-Way Analysis** (detailed metrics)
```bash
python three_way_benchmark.py
```

Output: Comprehensive timing, accuracy, and scaling analysis

### Understanding Benchmark Output

```
Benchmarking Quantum Systems (78 modules)...

✓ aerospace/panel_method ... 0.0008s (classical: 0.0032s, speedup: 4.12x)
✓ electrical/power_flow ... 0.0007s (classical: 0.0034s, speedup: 4.85x)
...
✓ 78/78 modules passed

Overall Statistics:
  Avg Quantum Time: 0.0007s
  Avg Classical Time: 0.0034s
  Average Speedup: 4.5x
  Success Rate: 100%
```

See **[BENCHMARKING.md](./BENCHMARKING.md)** for detailed analysis.

---

## Verification Scripts

After installation, run these verification scripts to confirm everything works:

### Import Verification

```bash
# Check all classical modules are importable
python -c "from classical_systems.launcher import get_all_modules; print(len(get_all_modules()), 'modules loaded')"

# Check all quantum modules are importable
python -c "from quantum_systems.launcher_quantum import get_all_modules; print(len(get_all_modules()), 'modules loaded')"
```

### Scale Verification

```bash
python verify_scale.py
```

Verifies that modules handle different problem sizes correctly.

### Overflow Verification

```bash
python verify_overflow.py
```

Ensures numerical stability across different scales.

### Quality Verification

```bash
python verify_quality.py
```

Validates quantum module accuracy and fidelity metrics.

---

## Common First Steps

### 1. Explore Available Modules

```python
# List all disciplines and modules
from classical_systems.launcher import get_all_modules

for discipline, modules in get_all_modules().items():
    print(f"{discipline}: {len(modules)} modules")
    for module_name in modules:
        print(f"  - {module_name}")
```

### 2. Run a Quick Test

Start with a simple discipline like **Electrical Engineering**:

```bash
python classical_systems/launcher.py
# Select: Electrical → Power Flow → Run with defaults
```

Then compare with quantum:

```bash
python quantum_systems/launcher_quantum.py
# Select: Electrical → Power Flow → Execute
# Compare runtimes and fidelity metrics
```

### 3. Run a Benchmark

```bash
# Compare classical vs quantum on all modules
python branch_benchmark.py

# Review results in benchmark_results.json
```

See **[MODULES.md](./MODULES.md)** for a complete listing of all 157 available simulations.

---

## Troubleshooting Installation

### Issue: ImportError for customtkinter

**Solution:**
```bash
pip install --upgrade customtkinter
```

If still failing, the quantum launcher requires customtkinter. Classical launcher uses built-in tkinter and should always work.

### Issue: ModuleNotFoundError (numpy, scipy, matplotlib)

**Solution:**
```bash
pip install --upgrade numpy scipy matplotlib
```

### Issue: Python version too old

**Solution:**
```bash
# Check Python version
python --version

# If < 3.7, update Python from python.org
# Then reinstall virtual environment with new Python version
```

### Issue: Permission denied on launcher.py (macOS/Linux)

**Solution:**
```bash
chmod +x classical_systems/launcher.py
chmod +x quantum_systems/launcher_quantum.py
```

### Issue: tkinter not found (Linux)

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Then reactivate virtual environment
source venv/bin/activate
```

See **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** for more help.

---

## Environment Variables (Optional)

Configure behavior with optional environment variables:

```bash
# Disable GPU acceleration (if using CUDA-accelerated systems)
export QC_FORCE_CPU=1

# Set number of threads
export OMP_NUM_THREADS=4

# Enable debug logging
export QC_DEBUG=1
```

---

## Next Steps

Once installation is complete:

1. **Understand the System**: Read [ARCHITECTURE.md](./ARCHITECTURE.md) for system design overview
2. **Explore APIs**: Study [CLASSICAL_API.md](./CLASSICAL_API.md) and [QUANTUM_API.md](./QUANTUM_API.md)
3. **Browse Modules**: Check [MODULES.md](./MODULES.md) for discipline-specific simulations
4. **Learn Algorithms**: Explore [QUANTUM_ALGORITHMS.md](./QUANTUM_ALGORITHMS.md) for algorithm details
5. **Create Extensions**: Read [ADDING_MODULES.md](./ADDING_MODULES.md) to build custom modules
6. **Benchmark**: Run [BENCHMARKING.md](./BENCHMARKING.md) analysis on your system

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Run classical GUI | `python classical_systems/launcher.py` |
| Run quantum GUI | `python quantum_systems/launcher_quantum.py` |
| Benchmark all modules | `python branch_benchmark.py` |
| Run tests | `pytest quantum_systems/core/tests/` |
| Check module imports | `python -c "from classical_systems import launcher"` |
| List all modules | See [MODULES.md](./MODULES.md) |

---

**Last Updated**: March 2026  
**Tested on**: Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
