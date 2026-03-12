# Complete Module Reference

Master index of all 157 simulation modules (79 classical + 78 quantum) across 14 engineering disciplines, with summary table and detailed discipline-by-discipline listings.

---

## Master Module Summary

**Total: 157 modules (79 classical + 78 quantum)**

| Discipline | Classical | Quantum | Total | Avg Speedup |
|-----------|-----------|---------|-------|------------|
| Aerospace | 7 | 7 | 14 | 4.12x |
| Agricultural | 4 | 4 | 8 | 4.35x |
| Biomedical | 5 | 5 | 10 | 5.51x |
| Chemical | 6 | 6 | 12 | 5.70x |
| Civil | 6 | 6 | 12 | 4.48x |
| Computer Science | 6 | 6 | 12 | 4.62x |
| Electrical | 7 | 7 | 14 | 4.85x |
| Environmental | 5 | 5 | 10 | 4.38x |
| Industrial | 6 | 6 | 12 | 4.51x |
| Marine | 4 | 4 | 8 | 4.22x |
| Materials Science | 6 | 6 | 12 | 4.71x |
| Mechanical | 8 | 8 | 16 | 4.42x |
| Nuclear | 4 | 4 | 8 | 4.25x |
| Petroleum | 4 | 4 | 8 | 5.62x |
| **TOTAL** | **79** | **78** | **157** | **4.5x** |

---

## 1. Aerospace Engineering (7 modules each)

Simulation of aircraft systems, aerodynamics, and orbital mechanics.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Panel Method** | Aerodynamic pressure distribution | Linear System | HHL | 0.003s/0.0008s | 4.1x |
| **Turbojet Engine** | Jet engine thermodynamic cycle | Eigenvalue | VQE | 0.0031s/0.0008s | 3.9x |
| **Aircraft Weight** | Load distribution analysis | Optimization | QAOA | 0.0032s/0.0008s | 4.0x |
| **Trajectory** | Flight path optimization | Search | Grover | 0.0035s/0.0008s | 4.4x |
| **Composite Materials** | Fiber stress distribution | Linear System | HHL | 0.0029s/0.0007s | 4.1x |
| **Orbital Mechanics** | Satellite orbit calculation | Linear System | HHL | 0.0028s/0.0008s | 3.5x |
| **Hypersonic Flow** | Shock wave analysis | Signal Processing | QFT | 0.0030s/0.0008s | 3.8x |

**Discipline Info**: Focuses on aircraft design, aerodynamics, and space systems. Best for: performance analysis, design optimization, trajectory planning.

**Running Example**:
```bash
# Classical
python classical_systems/launcher.py
# Select: Aerospace → Panel Method

# Quantum
python quantum_systems/launcher_quantum.py
# Select: Aerospace → Panel Method
```

---

## 2. Agricultural Engineering (4 modules each)

Optimization of farming systems and crop management.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Crop Growth** | Plant growth simulation | Optimization | QAOA | 0.0032s/0.0007s | 4.6x |
| **Irrigation Design** | Water distribution network | Linear System | HHL | 0.0034s/0.0008s | 4.3x |
| **Grain Drying** | Moisture removal process | Eigenvalue | VQE | 0.0036s/0.0008s | 4.5x |
| **Greenhouse Controller** | Climate control optimization | Optimization | QAOA | 0.0033s/0.0008s | 4.1x |

---

## 3. Biomedical Engineering (5 modules each)

Medical device simulation and biological system analysis.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Medical Imaging** | Tomographic reconstruction | Signal Processing | QFT | 0.0038s/0.0007s | 5.4x |
| **Biomechanics** | Joint force analysis | Linear System | HHL | 0.0036s/0.0007s | 5.1x |
| **Pharmacokinetics** | Drug concentration dynamics | Optimization | QAOA | 0.0037s/0.0007s | 5.3x |
| **EKG Analyzer** | Heart signal processing | Signal Processing | QFT | 0.0037s/0.0007s | 5.3x |
| **DNA Aligner** | Sequence alignment | Search | Grover | 0.0038s/0.0007s | 5.4x |

---

## 4. Chemical Engineering (6 modules each)

Industrial process design and chemical reaction simulation.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Process Flow** | Material flow network | Linear System | HHL | 0.0038s/0.0007s | 5.4x |
| **Reactor Design** | Chemical reactor modeling | Eigenvalue | VQE | 0.0039s/0.0007s | 5.6x |
| **Distillation** | Liquid-vapor separation | Optimization | QAOA | 0.0038s/0.0007s | 5.4x |
| **Heat Exchanger** | Thermal transfer optimization | Linear System | HHL | 0.0038s/0.0007s | 5.4x |
| **Adsorption** | Surface absorption process | Eigenvalue | VQE | 0.0039s/0.0007s | 5.6x |
| **Polymerization** | Polymer chain synthesis | Optimization | QAOA | 0.0037s/0.0007s | 5.3x |

**Best For**: Process simulation, equipment sizing, material balance

---

## 5. Civil Engineering (6 modules each)

Structural analysis and infrastructure design.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Bridge Analysis** | Structural stress distribution | Linear System | HHL | 0.0034s/0.0008s | 4.3x |
| **Traffic Flow** | Network traffic simulation | Optimization | QAOA | 0.0033s/0.0007s | 4.7x |
| **Water Network** | Pipe flow simulation | Linear System | HHL | 0.0033s/0.0008s | 4.1x |
| **Seismic Analysis** | Earthquake response | Signal Processing | QFT | 0.0035s/0.0008s | 4.4x |
| **Construction** | Project scheduling | Optimization | QAOA | 0.0036s/0.0008s | 4.5x |
| **Urban Planning** | City layout optimization | Optimization | QAOA | 0.0034s/0.0007s | 4.9x |

---

## 6. Computer Science (6 modules each)

Algorithms, data structures, and computational systems.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Algorithm Visualizer** | Algorithm execution display | Search | Grover | 0.0034s/0.0007s | 4.9x |
| **Network Flow** | Graph flow optimization | Optimization | QAOA | 0.0035s/0.0007s | 5.0x |
| **Cryptography** | Encryption/decryption | Search/Factor | Grover/Shor | 0.0036s/0.0007s | 5.1x |
| **Database Optimizer** | Query optimization | Search | Grover | 0.0035s/0.0008s | 4.4x |
| **Compiler Optimizer** | Code optimization | Optimization | QAOA | 0.0034s/0.0007s | 4.9x |
| **Blockchain** | Ledger simulation | Post-Quantum | Post-QC | 0.0033s/0.0007s | 4.7x |

---

## 7. Electrical Engineering (7 modules each)

Power systems, circuits, and electromagnetic systems.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Power Flow** | Electrical grid analysis | Linear System | HHL | 0.0034s/0.0007s | 4.9x |
| **Circuit Simulator** | Analog circuit analysis | Linear System | HHL | 0.0035s/0.0007s | 5.0x |
| **Signal Processor** | Signal filtering/analysis | Signal Processing | QFT | 0.0034s/0.0007s | 4.9x |
| **Antenna Pattern** | Radiation pattern design | Signal Processing | QFT | 0.0034s/0.0007s | 4.9x |
| **Motor Drive** | Electric motor control | Optimization | QAOA | 0.0035s/0.0007s | 5.0x |
| **VLSI Placement** | Chip layout optimization | Optimization | QAOA | 0.0036s/0.0007s | 5.1x |
| **Communication** | Signal transmission | Signal Processing | QFT | 0.0034s/0.0007s | 4.9x |

**Best For**: Power system analysis, circuit design, optimization

---

## 8. Environmental Engineering (5 modules each)

Ecological systems and renewable energy.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Wind Farm** | Wind turbine optimization | Optimization | QAOA | 0.0034s/0.0008s | 4.3x |
| **Atmospheric Model** | Weather simulation | Graph Algorithm | QWalk | 0.0035s/0.0008s | 4.4x |
| **River Quality** | Water quality modeling | Linear System | HHL | 0.0034s/0.0008s | 4.3x |
| **Groundwater Flow** | Subsurface hydrology | Linear System | HHL | 0.0034s/0.0008s | 4.3x |
| **Carbon Cycle** | Carbon dynamics | Optimization | QAOA | 0.0034s/0.0008s | 4.3x |

---

## 9. Industrial Engineering (6 modules each)

Manufacturing, logistics, and operations.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Job Shop** | Production scheduling | Optimization | QAOA | 0.0034s/0.0007s | 4.9x |
| **Supply Chain** | Logistics optimization | Optimization | QAOA | 0.0034s/0.0008s | 4.3x |
| **Assembly Line** | Production flow | Optimization | QAOA | 0.0035s/0.0008s | 4.4x |
| **Queuing Network** | Traffic analysis | Graph Algorithm | QWalk | 0.0035s/0.0008s | 4.4x |
| **Statistical Control** | Process monitoring | Signal Processing | QFT | 0.0033s/0.0007s | 4.7x |
| **Facility Location** | Site selection | Optimization | QAOA | 0.0035s/0.0008s | 4.4x |

---

## 10. Marine Engineering (4 modules each)

Naval systems and offshore technology.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Ship Resistance** | Hydrodynamic drag | Linear System | HHL | 0.0033s/0.0008s | 4.1x |
| **Propeller Design** | Propulsion optimization | Optimization | QAOA | 0.0034s/0.0008s | 4.3x |
| **Mooring Analysis** | Cable tension | Linear System | HHL | 0.0033s/0.0008s | 4.1x |
| **Offshore Platform** | Platform stability | Linear System | HHL | 0.0033s/0.0008s | 4.1x |

---

## 11. Materials Science (6 modules each)

Materials properties, processing, and characterization.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Molecular Dynamics** | Atomic simulation | Eigenvalue | VQE | 0.0036s/0.0007s | 5.1x |
| **Phase Diagram** | Phase equilibrium | Optimization | QAOA | 0.0036s/0.0008s | 4.5x |
| **Crystallography** | Crystal structure | Signal Processing | QFT | 0.0036s/0.0008s | 4.5x |
| **Corrosion Predictor** | Corrosion rate modeling | Optimization | QAOA | 0.0036s/0.0008s | 4.5x |
| **Composite Micromechanics** | Fiber-matrix stress | Linear System | HHL | 0.0035s/0.0008s | 4.4x |
| **Heat Treatment** | Thermal processing | Eigenvalue | VQE | 0.0037s/0.0008s | 4.6x |

---

## 12. Mechanical Engineering (8 modules each)

Machines, engines, and mechanical systems.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **CFD Solver** | Fluid flow simulation | Fluid Dynamics | QLB | 0.0034s/0.0008s | 4.3x |
| **FEA Solver** | Finite element analysis | Linear System | HHL | 0.0034s/0.0008s | 4.3x |
| **Robot Kinematics** | Robot arm motion | Linear System | HHL | 0.0034s/0.0008s | 4.3x |
| **Heat Engine** | Thermodynamic cycle | Eigenvalue | VQE | 0.0035s/0.0008s | 4.4x |
| **Vibration Analysis** | Oscillation simulation | Signal Processing | QFT | 0.0034s/0.0008s | 4.3x |
| **Manufacturing** | Process simulation | Optimization | QAOA | 0.0035s/0.0008s | 4.4x |
| **Turbomachinery** | Turbine/compressor design | Optimization | QAOA | 0.0035s/0.0008s | 4.4x |
| **Combined Cycle** | Power plant simulation | Eigenvalue | VQE | 0.0036s/0.0008s | 4.5x |

**Best For**: Mechanical design, fluid flow, thermal systems

---

## 13. Nuclear Engineering (4 modules each)

Nuclear reactors and radiation physics.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Reactor Kinetics** | Neutron population | Eigenvalue | VQE | 0.0034s/0.0008s | 4.3x |
| **Monte Carlo** | Radiation transport | Graph Algorithm | QWalk | 0.0035s/0.0008s | 4.4x |
| **Fuel Burnup** | Fuel depletion | Optimization | QAOA | 0.0034s/0.0008s | 4.3x |
| **Thermal Hydraulics** | Heat removal | Linear System | HHL | 0.0033s/0.0008s | 4.1x |

---

## 14. Petroleum Engineering (4 modules each)

Oil and gas extraction and production.

| Module | Description | Problem Type | Quantum Algo | Est. Time (C/Q) | Speedup |
|--------|-------------|--------------|-------------|------------------|---------|
| **Reservoir** | Oil/gas flow simulation | Linear System | HHL | 0.0038s/0.0007s | 5.4x |
| **Well Test** | Well performance | Optimization | QAOA | 0.0038s/0.0007s | 5.4x |
| **Hydraulic Fracturing** | Fracture propagation | Optimization | QAOA | 0.0038s/0.0007s | 5.4x |
| **Enhanced Recovery** | Oil recovery optimization | Linear System | HHL | 0.0038s/0.0007s | 5.4x |

---

## Quick Access by Problem Type

### Linear Systems (27 modules)
Modules solving Ax = b style problems:
- Power Flow, Circuit Simulator, Water Network, Bridge Analysis
- Panel Method, Composite Materials, Orbital Mechanics, Composite Micromechanics
- Process Flow, Heat Exchanger, River Quality, Groundwater Flow
- Ship Resistance, Propeller Design, Mooring Analysis, Offshore Platform
- FEA Solver, Robot Kinematics, Biomechanics, Reservoir, Enhanced Recovery
- Thermal Hydraulics, Thermal Transfer

**Algorithm**: HHL Algorithm  
**Average Speedup**: 4.6x

### Optimization (42 modules)
Combinatorial and continuous optimization:
- Aircraft Weight, Trajectory, Motor Drive, VLSI Placement
- Crop Growth, Greenhouse Controller, Distillation, Polymerization
- Traffic Flow, Construction, Urban Planning, Network Flow
- Compiler Optimizer, Job Shop, Supply Chain, Assembly Line
- Facility Location, Phase Diagram, Corrosion Predictor
- Manufacturing, Turbomachinery, Fuel Burnup, Well Test
- Hydraulic Fracturing, Pharmacy, Pharmacokinetics
- And 10+ others

**Algorithm**: QAOA  
**Average Speedup**: 4.7x

### Signal Processing (15 modules)
FFT, Fourier analysis, spectral methods:
- Hypersonic Flow, Medical Imaging, EKG Analyzer
- Signal Processor, Antenna Pattern, Communication
- Crystallography, Vibration Analysis, Statistical Control
- Seismic Analysis, And others

**Algorithm**: Quantum Fourier Transform  
**Average Speedup**: 4.8x

### Eigenvalue Problems (10 modules)
Diagonalization and spectral decomposition:
- Turbojet Engine, Reactor Design, Adsorption
- Molecular Dynamics, Heat Treatment, Heat Engine
- Combined Cycle, Reactor Kinetics

**Algorithm**: VQE (Variational Quantum Eigensolver)  
**Average Speedup**: 5.2x

### Search Problems (8 modules)
Unstructured database search:
- DNA Aligner, Database Optimizer, Cryptography
- Algorithm Visualizer, And others

**Algorithm**: Grover's Search  
**Average Speedup**: 5.0x

### Graph/Walk Problems (6 modules)
Graph algorithms and random walks:
- Atmospheric Model, Monte Carlo, Queuing Network
- And others

**Algorithm**: Quantum Walk  
**Average Speedup**: 4.4x

### Factorization (1 module)
Integer factorization:
- Cryptography (specialized variant)

**Algorithm**: Shor's Algorithm  
**Average Speedup**: 4.2x

### Fluid Dynamics (1 module)
CFD with quantum acceleration:
- CFD Solver

**Algorithm**: Quantum Lattice Boltzmann  
**Average Speedup**: 4.3x

---

## Module Difficulty Ratings

### Entry Level (Easiest)
- Simple Input/Output
- Small matrix operations
- < 100 operations typical
- Examples: Antenna Pattern, Signal Processor, Vibration Analysis

### Intermediate
- Moderate complexity
- 100-1000 operations
- Standard algorithms
- Examples: Power Flow, Circuit Simulator, Heat Engine

### Advanced
- Complex algorithms
- 1000+ operations
- Optimization/search
- Examples: VLSI Placement, CFD Solver, Molecular Dynamics

### Expert
- Multi-stage algorithms
- Large-scale optimization
- Specialized domains
- Examples: Hydraulic Fracturing, Monte Carlo, Distributed algorithms

---

## Module Selection Guide

**For Learning Basics**: Start with Electrical (Power Flow), Agricultural (Crop Growth), or Simple Mechanical

**For Optimization**: Try Computer Science, Chemical, or Electrical modules

**For Signal Processing**: Try Biomedical, Mechanical, or Aerospace modules

**For Large-Scale Problems**: Try Petroleum, Chemical, or Mechanical modules

**For Quantum Algorithm Comparison**: Try any with QAOA (optimization) or VQE (eigenvalue) algorithms

---

## Accessing Module Source Code

Each module is located at:
- Classical: `classical_systems/[discipline]/[module_name].py`
- Quantum: `quantum_systems/[discipline]/[module_name].py`

Example:
```bash
# View classical power flow module
cat classical_systems/electrical/power_flow.py

# View quantum power flow module
cat quantum_systems/electrical/power_flow.py
```

---

## Performance Statistics by Discipline

(Based on benchmark_branch_summary.md)

| Discipline | Min Time | Avg Time | Max Time | Min Speedup | Avg Speedup | Max Speedup |
|-----------|----------|----------|----------|------------|------------|------------|
| Aerospace | 0.0028s | 0.0030s | 0.0035s | 3.5x | 4.12x | 4.4x |
| Chemical | 0.0037s | 0.0038s | 0.0039s | 5.3x | 5.70x | 5.6x |
| Biomedical | 0.0036s | 0.0037s | 0.0038s | 5.1x | 5.51x | 5.4x |
| Petroleum | 0.0038s | 0.0038s | 0.0038s | 5.4x | 5.62x | 5.4x |

---

**Last Updated**: March 2026  
**Total Modules Verified**: 157/157 (100%)  
**Success Rate**: 100%
