# QC in CC: Quantum Computing in Classical Computers

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

An advanced framework to execute quantum computing algorithms within classical computing systems, with comprehensive implementations across 14+ engineering and scientific domains.

## Overview

QC in CC bridges the gap between quantum and classical computing by implementing quantum algorithms that can run on classical hardware. The framework includes parallel implementations of both classical and quantum simulations for comparative analysis, performance benchmarking, and real-world engineering applications.

## Key Features

- **Dual Computing Paradigm**: Side-by-side classical and quantum algorithm implementations
- **14+ Engineering Domains**: Aerospace, agricultural, biomedical, chemical, civil, computer science, electrical, environmental, industrial, marine, materials science, mechanical, nuclear, and petroleum
- **79+ Simulation Modules**: Each with deterministic outputs and comprehensive benchmarking
- **Interactive GUI**: User-friendly interfaces for both classical and quantum systems
- **Performance Analysis**: Built-in metrics (RMSE, MAPE, R², confidence intervals)
- **Live Visualization**: Real-time simulation visuals with runtime and fidelity charts
- **Comprehensive Benchmarking**: Cross-branch performance comparison framework

## Project Structure

```
QC-in-CC/
├── classical_systems/          # Classical algorithm implementations (79 modules)
│   ├── aerospace/
│   ├── agricultural/
│   ├── biomedical/
│   ├── chemical/
│   ├── civil/
│   ├── computer_science/
│   ├── electrical/
│   ├── environmental/
│   ├── industrial/
│   ├── marine/
│   ├── materials_science/
│   ├── mechanical/
│   ├── nuclear/
│   ├── petroleum/
│   ├── core/                   # Base simulation framework
│   ├── launcher.py             # Classical systems GUI launcher
│   └── ui_utils.py             # UI utilities
├── quantum_systems/            # Quantum algorithm implementations (78 modules)
│   ├── [same domain structure as classical_systems]
│   ├── core/                   # Quantum engine implementations
│   │   ├── ctmp_engine.py      # Circuit template matching processor
│   │   ├── quantum_algorithms.py
│   │   ├── comparison_engine.py
│   │   ├── memristor_emulator.py
│   │   ├── circuit_visualizer.py
│   │   └── neural_network_mode.py
│   ├── launcher_quantum.py     # Quantum systems GUI launcher
│   └── base_template.py        # Common runtime contract
├── docs/                       # Comprehensive documentation
│   ├── GETTING_STARTED.md      # Installation & setup guide
│   ├── ARCHITECTURE.md         # System architecture overview
│   ├── CLASSICAL_API.md        # Classical systems API reference
│   ├── QUANTUM_API.md          # Quantum systems API reference
│   ├── QUANTUM_THEORY.md       # Theoretical foundations
│   ├── BENCHMARKING.md         # Performance analysis guide
│   ├── MODULES.md              # Module reference
│   └── TROUBLESHOOTING.md      # Common issues and solutions
└── [Benchmarking & Testing Scripts]
    ├── branch_benchmark.py
    ├── three_way_benchmark.py
    ├── verify_quality.py
    └── benchmark_results/
```

## Installation

### Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 2GB minimum (4GB+ recommended for benchmarks)
- **Disk Space**: ~500MB

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/joshuaplrj/QC-in-CC.git
   cd QC-in-CC
   ```

2. **Create a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install numpy scipy matplotlib networkx customtkinter pytest
   ```

## Quick Start

### Classical Systems

Launch the interactive GUI for classical simulations:
```bash
python classical_systems/launcher.py
```

Run a specific classical module:
```bash
python classical_systems/aerospace/aircraft_weight.py
python classical_systems/electrical/power_flow.py
```

### Quantum Systems

Launch the interactive GUI for quantum simulations:
```bash
python quantum_systems/launcher_quantum.py
```

Run a specific quantum module:
```bash
python quantum_systems/aerospace/aircraft_weight.py
python quantum_systems/electrical/power_flow.py
```

### Benchmarking

Compare performance across branches:
```bash
python branch_benchmark.py
python three_way_benchmark.py
```

Run quality verification:
```bash
python verify_quality.py
```

## Module Coverage

### Available Domains

| Domain | Classical | Quantum | Notes |
|--------|-----------|---------|-------|
| Aerospace | ✓ | ✓ | Aircraft, orbital, hypersonic analyses |
| Agricultural | ✓ | ✓ | Crop models, irrigation, drying |
| Biomedical | ✓ | ✓ | Biomechanics, imaging, pharmacokinetics |
| Chemical | ✓ | ✓ | Reactors, distillation, adsorption |
| Civil | ✓ | ✓ | Structural, seismic, traffic analysis |
| Computer Science | ✓ | ✓ | Algorithms, cryptography, databases |
| Electrical | ✓ | ✓ | Circuits, power systems, signals |
| Environmental | ✓ | ✓ | Modeling and analysis |
| Industrial | ✓ | ✓ | Process optimization |
| Marine | ✓ | ✓ | Hydrodynamics, navigation |
| Materials Science | ✓ | ✓ | Material properties, simulations |
| Mechanical | ✓ | ✓ | Dynamics, thermal analysis |
| Nuclear | ✓ | ✓ | Reactor simulation, safety |
| Petroleum | ✓ | ✓ | Reservoir simulation, processing |

**Total Modules**: 157 (79 classical + 78 quantum)

## Architecture

### Classical Systems
- Deterministic, seeded outputs
- Lightweight runtime contract
- Direct numerical simulations
- Baseline performance reference

### Quantum Systems
- Quantum algorithm implementations
- Classical emulation of quantum circuits
- Fidelity metrics vs. classical baseline
- Live visualization with performance charts

### Core Components
- `SimulationConfig`: Configuration management
- `SimulationBase`: Base simulation class
- `InteractiveGUI`: Unified GUI framework
- Circuit visualization and analysis tools

## Performance Metrics

Each simulation produces:
- **RMSE**: Root Mean Squared Error
- **MAPE**: Mean Absolute Percentage Error
- **R²**: Coefficient of determination
- **Confidence Intervals**: Statistical bounds on results
- **Runtime**: Execution time benchmarking

## Documentation

- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Classical API Reference](docs/CLASSICAL_API.md)
- [Quantum API Reference](docs/QUANTUM_API.md)
- [Quantum Theory Foundations](docs/QUANTUM_THEORY.md)
- [Benchmarking Guide](docs/BENCHMARKING.md)
- [Modules Reference](docs/MODULES.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## Testing & Verification

All modules are verified for:
- ✓ Import correctness
- ✓ Execution integrity
- ✓ Output determinism
- ✓ Cross-branch compatibility
- ✓ Fidelity metrics

Run tests:
```bash
python -m pytest quantum_systems/core/tests/test_core.py -q
python verify_quality.py
```

## Contributing

Contributions are welcome! Please ensure:
1. Code follows the existing module template
2. Deterministic outputs (use seeded randomization)
3. Comprehensive docstrings
4. Test coverage

## License

MIT License - see LICENSE file for details

## Citation

If you use QC in CC in research, please cite:
```
@software{qcincc2026,
  title={QC in CC: Quantum Computing in Classical Computers},
  author={Joshua P.},
  year={2026},
  url={https://github.com/joshuaplrj/QC-in-CC}
}
```

## Support

For issues, questions, or suggestions:
- Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- Review [GETTING_STARTED.md](docs/GETTING_STARTED.md)
- Submit an issue on GitHub

---

**Last Updated**: March 2026
